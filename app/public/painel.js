// Painel da equipe. Uma página só, sem bibliotecas. O servidor manda o
// estado inteiro a cada mudança (long-poll) e a tela é redesenhada.

const $ = (id) => document.getElementById(id);
const conteudo = $('conteudo');
const dlg = $('dlg');

let eu = null;
let E = null; // último estado recebido
let aba = 'rampa';
let dataQuadro = '';
let aberta = null; // id da conversa aberta
let fio = null; // dados da conversa aberta
let adm = null; // dados de administração
let rel = null; // relatório
let relPeriodo = { de: '', ate: '' };
let controle = null;
let somLigado = false;
let audio = null;
const local = new Map(); // valores digitados que sobrevivem ao redesenho
let antes = { chamados: 0, rascunhos: 0, emergencias: 0, pendentes: 0, naoLidas: 0 };

// ---------- utilidades ----------

function h(tag, attrs, ...filhos) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') e.className = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
    else if (k === 'value') e.value = v;
    else if (['checked', 'disabled', 'hidden', 'selected'].includes(k)) e[k] = true;
    else e.setAttribute(k, v === true ? '' : v);
  }
  for (const f of filhos.flat(3)) {
    if (f === null || f === undefined || f === false) continue;
    e.append(f.nodeType ? f : document.createTextNode(String(f)));
  }
  return e;
}

const botao = (rotulo, onclick, classe = '') => h('button', { class: `botao ${classe}`, type: 'button', onclick }, rotulo);

/** Campo cujo valor digitado é guardado em `local` e reposto a cada redesenho. */
function campo(tag, chave, padrao, attrs = {}) {
  const e = h(tag, { ...attrs, 'data-chave': chave });
  e.value = local.has(chave) ? local.get(chave) : padrao ?? '';
  return e;
}
const valor = (chave, padrao = '') => (local.has(chave) ? local.get(chave) : padrao);

conteudo.addEventListener('input', (ev) => {
  const c = ev.target.dataset?.chave;
  if (c) local.set(c, ev.target.type === 'checkbox' ? ev.target.checked : ev.target.value);
});

async function api(metodo, caminho, corpo, sinal) {
  const r = await fetch(caminho, {
    method: metodo,
    headers: { 'X-Painel': '1', ...(corpo ? { 'Content-Type': 'application/json' } : {}) },
    body: corpo ? JSON.stringify(corpo) : undefined,
    signal: sinal,
  });
  const dados = await r.json().catch(() => ({}));
  if (r.status === 401) mostrarLogin();
  if (!r.ok) throw Object.assign(new Error(dados.erro || 'Falha de conexão.'), { status: r.status });
  return dados;
}

async function agir(fn) {
  try {
    await fn();
  } catch (e) {
    if (e.status !== 401) aviso(e.message);
  }
}

function fecharDialogo() {
  if (dlg.open) dlg.close();
}

function dialogo(titulo, corpo, botoes) {
  dlg.replaceChildren(h('h2', {}, titulo), corpo, h('div', { class: 'rodape' }, botao('Cancelar', fecharDialogo), ...botoes));
  if (!dlg.open) dlg.showModal();
}

function aviso(mensagem) {
  dlg.replaceChildren(h('p', {}, mensagem), h('div', { class: 'rodape' }, botao('Ok', fecharDialogo, 'primario')));
  if (!dlg.open) dlg.showModal();
}

const dataBr = (iso) => (iso ? iso.split('-').reverse().join('/') : '');
const horaBr = (hhmm) => (hhmm ? hhmm.replace(':', 'h').replace(/h00$/, 'h') : '');
// Sempre no fuso da marina, não no do aparelho de quem olha o painel.
const instante = (iso) => (iso ? new Date(iso).toLocaleString('pt-BR', { timeZone: E?.marina.fuso, day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '');

function somarDias(iso, n) {
  const d = new Date(`${iso}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function linkWhats(telefone, texto) {
  let d = String(telefone || '').replace(/\D/g, '');
  if (!d) return null;
  if (d.length <= 11) d = `55${d}`;
  return `https://wa.me/${d}?text=${encodeURIComponent(texto)}`;
}

function whats(telefone, texto, rotulo = 'WhatsApp') {
  const url = linkWhats(telefone, texto);
  return url ? h('a', { class: 'botao', href: url, target: '_blank', rel: 'noopener noreferrer' }, rotulo) : null;
}

async function copiar(texto, mensagem = 'Link copiado.') {
  try {
    await navigator.clipboard.writeText(texto);
    aviso(mensagem);
  } catch {
    aviso(texto);
  }
}

/** Caixa de marcar cujo estado sobrevive ao redesenho, como campo(). */
function caixa(chave, padrao) {
  return h('input', { type: 'checkbox', 'data-chave': chave, checked: local.has(chave) ? local.get(chave) : !!padrao });
}

// ---------- som e avisos ----------

function bip(vezes = 1) {
  if (!somLigado) return;
  audio = audio || new AudioContext();
  for (let i = 0; i < vezes; i++) {
    const o = audio.createOscillator();
    const g = audio.createGain();
    o.frequency.value = 880;
    g.gain.value = 0.08;
    o.connect(g).connect(audio.destination);
    o.start(audio.currentTime + i * 0.3);
    o.stop(audio.currentTime + i * 0.3 + 0.18);
  }
}

$('som').addEventListener('click', () => {
  somLigado = !somLigado;
  $('som').textContent = somLigado ? 'Som ligado' : 'Ativar som';
  bip();
});

// ---------- login ----------

function mostrarLogin() {
  controle?.abort();
  E = null;
  $('app').hidden = true;
  $('login').hidden = false;
}

$('login').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  $('loginErro').textContent = '';
  try {
    const r = await fetch('/api/painel/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ senha: $('loginSenha').value, nome: $('loginNome').value }),
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.erro);
    $('loginSenha').value = '';
    entrar(d);
  } catch (e) {
    $('loginErro').textContent = e.message || 'Não foi possível entrar.';
  }
});

$('sair').addEventListener('click', async () => {
  await fetch('/api/painel/sair', { method: 'POST' });
  mostrarLogin();
});

function entrar(sessao) {
  eu = sessao;
  $('login').hidden = true;
  $('app').hidden = false;
  $('quem').textContent = `${eu.nome}${eu.papel === 'admin' ? ' (admin)' : ''}`;
  escutar();
}

// ---------- estado ----------

const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

async function escutar() {
  controle?.abort();
  const meu = new AbortController();
  controle = meu;
  let primeira = true;
  while (!meu.signal.aborted) {
    try {
      const q = new URLSearchParams({ espera: primeira || !E ? '0' : '1', v: E ? E.v : 0, data: dataQuadro });
      const novo = await api('GET', `/api/painel/estado?${q}`, null, meu.signal);
      primeira = false;
      if (meu.signal.aborted) return;
      receber(novo);
    } catch (e) {
      if (meu.signal.aborted || e.status === 401) return;
      await dormir(3000);
    }
  }
}

function receber(novo) {
  const c = novo.contadores;
  if (c.emergencias > antes.emergencias) bip(4);
  else if (c.chamados > antes.chamados || c.rascunhos > antes.rascunhos || c.pendentes > antes.pendentes || c.naoLidas > antes.naoLidas) bip(1);
  antes = c;
  const mudou = !E || E.v !== novo.v;
  E = novo;
  const total = c.chamados + c.rascunhos + c.pendentes + c.naoLidas;
  document.title = `${total ? `(${total}) ` : ''}Painel · ${E.marina.nome}`;
  desenhar();
  if (mudou && aberta && aba === 'conversas') carregarFio(aberta);
}

async function atualizar() {
  escutar();
}

// ---------- moldura ----------

// Os mesmos fusos que o servidor aceita (lib/tempo.js).
const FUSOS = {
  'America/Sao_Paulo': 'Horário de Brasília (PR, SP, SC, RS, MG, RJ, GO…)',
  'America/Campo_Grande': 'Mato Grosso do Sul (1 hora a menos que Brasília)',
  'America/Cuiaba': 'Mato Grosso (1 hora a menos que Brasília)',
  'America/Manaus': 'Amazonas, Rondônia e Roraima (1 hora a menos que Brasília)',
  'America/Rio_Branco': 'Acre (2 horas a menos que Brasília)',
  'America/Noronha': 'Fernando de Noronha (1 hora a mais que Brasília)',
};

const MODOS = {
  auto: ['Automático', 'ok', 'O assistente responde direto ao cliente.'],
  sombra: ['Sombra', 'espera', 'O assistente escreve e alguém da equipe aprova antes de enviar.'],
  desligado: ['Desligado', 'alerta', 'O assistente não responde. As mensagens vão para a equipe.'],
};

function desenharMoldura() {
  $('marina').textContent = E.marina.nome;
  const [rotulo, classe] = MODOS[E.marina.modo];
  $('modo').textContent = `Atendente: ${rotulo}`;
  $('modo').className = `selo ${classe}`;

  const c = E.contadores;
  const abas = [
    ['rampa', 'Rampa', c.pendentes],
    ['aprovar', 'Aprovar', c.rascunhos],
    ['chamados', 'Chamados', c.chamados, c.emergencias > 0],
    ['conversas', 'Conversas', c.naoLidas],
    ['interessados', 'Interessados', 0],
    ['agentes', 'Agentes', c.sugestoes],
  ];
  if (eu.papel === 'admin') abas.push(['clientes', 'Clientes', 0], ['config', 'Configuração', 0], ['relatorio', 'Relatório', 0]);
  $('abas').replaceChildren(
    ...abas.map(([id, rotuloAba, n, vermelho]) =>
      h(
        'button',
        { type: 'button', 'aria-current': aba === id ? 'true' : null, onclick: () => trocarAba(id) },
        rotuloAba,
        n ? h('span', { class: `conta-n${vermelho ? ' vermelho' : ''}` }, n) : null,
      ),
    ),
  );

  const faixas = [];
  if (c.emergencias) {
    faixas.push(h('div', { class: 'faixa emergencia', role: 'alert' }, `EMERGÊNCIA: ${c.emergencias} chamado(s) aberto(s). `, h('button', { class: 'link', type: 'button', onclick: () => trocarAba('chamados') }, 'Ver agora')));
  }
  if (!E.saude.ok) faixas.push(h('div', { class: 'faixa aviso' }, `O assistente está fora do ar: ${E.saude.motivo} As mensagens estão indo para a equipe.`));
  if (E.ia.usoHoje >= E.ia.limite) faixas.push(h('div', { class: 'faixa aviso' }, 'O limite diário de respostas automáticas foi atingido. As mensagens estão indo para a equipe.'));
  else if (E.ia.usoPublicoHoje >= E.ia.limitePublico) {
    faixas.push(h('div', { class: 'faixa aviso' }, 'O link público atingiu o limite de respostas automáticas de hoje. Quem escrever por ele vai direto para a equipe; os clientes com link pessoal continuam atendidos.'));
  }
  if (E.demonstracao) faixas.push(h('div', { class: 'faixa info' }, 'Modo de demonstração: as respostas vêm de um roteiro simples, sem inteligência artificial e sem custo.'));
  $('alertas').replaceChildren(...faixas);
}

function trocarAba(id) {
  aba = id;
  if (id === 'clientes' || id === 'config') carregarAdm();
  if (id === 'relatorio') carregarRelatorio();
  desenhar();
}

function desenhar() {
  if (!E) return;
  const foco = document.activeElement?.dataset?.chave;
  const sel = foco ? [document.activeElement.selectionStart, document.activeElement.selectionEnd] : null;
  const rolagem = window.scrollY;
  const msgs = conteudo.querySelector('.msgs');
  const noFim = msgs ? msgs.scrollHeight - msgs.scrollTop - msgs.clientHeight < 80 : true;
  const rolagemMsgs = msgs ? msgs.scrollTop : 0;

  desenharMoldura();
  const telas = { rampa: telaRampa, aprovar: telaAprovar, chamados: telaChamados, conversas: telaConversas, interessados: telaInteressados, agentes: telaAgentes, clientes: telaClientes, config: telaConfig, relatorio: telaRelatorio };
  conteudo.replaceChildren(...[telas[aba]()].flat().filter(Boolean));

  window.scrollTo(0, rolagem);
  const novoMsgs = conteudo.querySelector('.msgs');
  if (novoMsgs) novoMsgs.scrollTop = noFim ? novoMsgs.scrollHeight : rolagemMsgs;
  if (foco) {
    const alvo = conteudo.querySelector(`[data-chave="${CSS.escape(foco)}"]`);
    if (alvo) {
      alvo.focus();
      try {
        if (sel && sel[0] !== null) alvo.setSelectionRange(sel[0], sel[1]);
      } catch {
        /* campo sem seleção de texto */
      }
    }
  }
}

$('modo').addEventListener('click', () => {
  const caixa = h(
    'div',
    { class: 'opcoes' },
    Object.entries(MODOS).map(([id, [rotulo, , explicacao]]) =>
      h(
        'label',
        {},
        h('input', { type: 'radio', name: 'modo', value: id, checked: E.marina.modo === id, disabled: id === 'auto' && eu.papel !== 'admin' }),
        h('b', {}, rotulo),
        h('small', {}, explicacao + (id === 'auto' && eu.papel !== 'admin' ? ' Só o administrador liga.' : '')),
      ),
    ),
  );
  dialogo('Modo do atendente', caixa, [
    botao(
      'Salvar',
      () =>
        agir(async () => {
          const modo = dlg.querySelector('input[name=modo]:checked')?.value;
          await api('POST', '/api/painel/modo', { modo });
          fecharDialogo();
        }),
      'primario',
    ),
  ]);
});

// ---------- rampa ----------

function acaoRegistro(id, acao, extra = {}) {
  return agir(async () => {
    await api('POST', `/api/painel/registro/${id}/acao`, { acao, ...extra });
    fecharDialogo();
  });
}

function pedirMotivo(titulo, id, acao) {
  const motivo = h('input', { placeholder: 'Motivo (opcional, o cliente vê)', maxlength: 300 });
  const avisar = h('input', { type: 'checkbox', checked: true });
  dialogo(titulo, h('div', { class: 'pilha' }, motivo, h('label', { class: 'caixa' }, avisar, 'Avisar o cliente pelo chat')), [
    botao('Confirmar', () => acaoRegistro(id, acao, { motivo: motivo.value, avisar: avisar.checked }), 'perigo'),
  ]);
}

/** Liberar um pedido que espera a equipe. Dois casos pedem confirmação:
 *  pedido que veio do link público (o sistema não sabe quem escreveu) e
 *  janela que já está cheia (só entra como encaixe). */
function liberarPedido(r) {
  const avisos = [];
  if (r.publico) {
    avisos.push(
      h('p', {}, h('b', {}, 'Pedido do link público. '), `O sistema não sabe quem escreveu: a pessoa disse ser ${r.clienteNome || 'cliente'}${r.embarcacao ? `, da embarcação ${r.embarcacao}` : ''}. Confirme com o cliente pelo telefone do cadastro antes de liberar.`),
    );
  }
  if (r.janelaLotada) {
    avisos.push(h('p', {}, h('b', {}, `A janela das ${horaBr(r.hora)} já está lotada. `), 'Se liberar, esta embarcação entra como encaixe, além da capacidade da rampa.'));
  }
  if (!avisos.length) return acaoRegistro(r.id, 'liberar');
  return dialogo('Liberar pedido', h('div', { class: 'pilha' }, avisos), [
    botao(r.janelaLotada ? 'Liberar como encaixe' : 'Já confirmei, liberar', () => acaoRegistro(r.id, 'liberar', { forcar: !!r.janelaLotada }), 'ok'),
  ]);
}

function seloStatus(r) {
  if (r.vencida) return h('span', { class: 'selo alerta' }, 'pré-reserva vencida');
  if (r.status === 'aguardando equipe') return h('span', { class: 'selo espera' }, 'aguardando a equipe');
  if (r.status === 'pre-reserva') return h('span', { class: 'selo espera' }, 'aguardando o sinal');
  if (r.etapa === 'na_agua') return h('span', { class: 'selo' }, 'na água');
  if (r.etapa === 'guardada') return h('span', { class: 'selo neutro' }, 'guardada');
  if (r.status === 'concluido') return h('span', { class: 'selo neutro' }, 'concluído');
  return h('span', { class: 'selo ok' }, 'confirmado');
}

function cartaoRegistro(r) {
  const acoes = [];
  if (r.status === 'aguardando equipe') {
    acoes.push(botao(r.janelaLotada ? 'Liberar como encaixe' : 'Liberar', () => liberarPedido(r), 'ok'), botao('Recusar', () => pedirMotivo('Recusar pedido', r.id, 'recusar'), 'perigo'));
  } else if (r.tipo === 'reserva' && r.status === 'pre-reserva') {
    acoes.push(botao('Confirmar pagamento', () => acaoRegistro(r.id, 'pagamento'), 'ok'), botao('Liberar unidade', () => pedirMotivo('Cancelar pré-reserva', r.id, 'cancelar'), 'perigo'));
  } else if (r.tipo === 'descida' && r.status === 'confirmado') {
    if (r.etapa === 'agendada') acoes.push(botao('Na água', () => acaoRegistro(r.id, 'na_agua'), 'primario grande'), botao('Cancelar', () => pedirMotivo('Cancelar descida', r.id, 'cancelar')));
    if (r.etapa === 'na_agua') acoes.push(botao('Guardada', () => acaoRegistro(r.id, 'guardada'), 'ok grande'), botao('Voltar para agendada', () => acaoRegistro(r.id, 'agendada', { avisar: false })));
  } else if ((r.tipo === 'subida' || r.tipo === 'servico') && r.status === 'confirmado') {
    acoes.push(botao('Concluir', () => acaoRegistro(r.id, 'concluir'), 'ok'));
  } else if (r.tipo === 'reserva' && r.status === 'confirmado') {
    acoes.push(botao('Cancelar reserva', () => pedirMotivo('Cancelar reserva', r.id, 'cancelar')));
  }
  if (r.conversaId) acoes.push(botao('Conversa', () => abrirConversa(r.conversaId)));
  const w = whats(r.telefone, `Olá! Aqui é da ${E.marina.nome}.`);
  if (w) acoes.push(w);

  const titulo = r.tipo === 'reserva' ? r.itemNome || r.item : r.embarcacao || r.clienteNome;
  const quando = [r.data ? dataBr(r.data) : '', horaBr(r.hora)].filter(Boolean).join(' · ');
  return h(
    'div',
    { class: `cartao barco${r.etapa === 'guardada' ? ' guardada' : ''}${r.status === 'aguardando equipe' || r.vencida ? ' espera' : ''}` },
    h('div', { class: 'linha' }, h('span', { class: 'nome cresce' }, titulo), seloStatus(r)),
    h('div', { class: 'suave' }, [r.tipo, r.clienteNome, quando].filter(Boolean).join(' · ')),
    r.detalhes ? h('div', {}, r.detalhes) : null,
    r.voltaPrevista ? h('div', {}, `Volta prevista: ${horaBr(r.voltaPrevista)}`) : null,
    r.origem === 'equipe' ? h('small', {}, 'lançado pela equipe') : null,
    r.publico && r.status === 'aguardando equipe' ? h('div', {}, h('span', { class: 'selo alerta' }, 'link público: confirme quem é')) : null,
    r.janelaLotada ? h('div', {}, h('span', { class: 'selo alerta' }, 'janela lotada')) : null,
    acoes.length ? h('div', { class: 'acoes' }, acoes) : null,
  );
}

function lancarManual() {
  const q = E.quadro;
  const tipo = h('select', {}, [['descida', 'Descida'], ['subida', 'Subida'], ['servico', 'Serviço'], ['reserva', 'Reserva de aluguel']].map(([v, t]) => h('option', { value: v }, t)));
  const cliente = h('select', {}, h('option', { value: '' }, 'Outra pessoa (digitar o nome)'), E.clientes.map((c) => h('option', { value: c.id }, `${c.nome} · ${c.embarcacao}`)));
  const nome = h('input', { placeholder: 'Nome', maxlength: 80 });
  const embarcacao = h('input', { placeholder: 'Embarcação', maxlength: 80 });
  const data = h('input', { type: 'date', value: q.data });
  const hora = h('input', { placeholder: 'Hora, ex.: 10h ou 10:30', maxlength: 5 });
  const item = h('select', {}, q.aluguel.map((i) => h('option', { value: i.id }, i.nome)));
  const detalhes = h('input', { placeholder: 'Detalhes (gelo, lavagem, nº de pessoas)', maxlength: 300 });
  const forcar = h('input', { type: 'checkbox' });
  const lItem = h('label', { hidden: true }, 'Item', item);
  const lNome = h('label', {}, 'Nome', nome);
  const lEmb = h('label', {}, 'Embarcação', embarcacao);
  const ajustar = () => {
    lItem.hidden = tipo.value !== 'reserva';
    lNome.hidden = lEmb.hidden = !!cliente.value;
  };
  tipo.addEventListener('change', ajustar);
  cliente.addEventListener('change', ajustar);
  dialogo(
    'Lançar manualmente',
    h(
      'div',
      { class: 'formulario' },
      h('label', {}, 'Tipo', tipo),
      h('label', {}, 'Cliente', cliente),
      lNome,
      lEmb,
      h('label', {}, 'Data', data),
      h('label', {}, 'Hora', hora),
      lItem,
      h('label', { class: 'larga' }, 'Detalhes', detalhes),
      h('label', { class: 'caixa larga' }, forcar, 'Encaixe: ignorar lotação e antecedência'),
    ),
    [
      botao(
        'Lançar',
        () =>
          agir(async () => {
            await api('POST', '/api/painel/registro', {
              tipo: tipo.value,
              clienteId: cliente.value || null,
              nome: nome.value,
              embarcacao: embarcacao.value,
              data: data.value,
              hora: hora.value,
              item: item.value,
              detalhes: detalhes.value,
              forcar: forcar.checked,
            });
            fecharDialogo();
          }),
        'primario',
      ),
    ],
  );
}

function telaRampa() {
  const q = E.quadro;
  const mudarData = (d) => {
    dataQuadro = d === E.agora.data ? '' : d;
    atualizar();
  };
  const topo = h(
    'div',
    { class: 'linha' },
    botao('◀', () => mudarData(somarDias(q.data, -1))),
    h('input', { type: 'date', value: q.data, 'aria-label': 'Dia', onchange: (ev) => ev.target.value && mudarData(ev.target.value) }),
    botao('▶', () => mudarData(somarDias(q.data, 1))),
    q.data !== E.agora.data ? botao('Hoje', () => mudarData(E.agora.data)) : null,
    h('strong', { class: 'cresce' }, q.dia),
    botao('+ Lançar manualmente', lancarManual, 'primario'),
  );

  const avisoDia = h(
    'div',
    { class: 'cartao pilha' },
    h('label', { class: 'campo' }, 'Aviso do dia (o assistente repete isto quando perguntam do rio, da rampa ou do tempo)', campo('textarea', 'aviso', E.marina.avisoDoDia?.texto, { maxlength: 500, rows: 2 })),
    h(
      'div',
      { class: 'linha' },
      h('small', { class: 'cresce' }, E.marina.avisoDoDia?.atualizadoEm ? `Atualizado em ${E.marina.avisoDoDia.atualizadoEm}` : E.marina.avisoDoDia?.texto ? '' : 'Ainda não preenchido'),
      botao('Salvar aviso', () =>
        agir(async () => {
          await api('POST', '/api/painel/aviso', { texto: valor('aviso', E.marina.avisoDoDia?.texto || '') });
          local.delete('aviso');
        }),
      ),
    ),
  );

  const partes = [topo, avisoDia];

  if (E.pendentes.length) {
    partes.push(h('h2', {}, `Aguardando decisão da equipe (${E.pendentes.length})`), h('div', { class: 'grade' }, E.pendentes.map(cartaoRegistro)));
  }

  partes.push(h('h2', {}, 'Descidas'));
  // q.horas traz todo horário que tem barco, inclusive os que ficaram fora
  // da grade depois de uma mudança na configuração.
  if (!q.horas.length) partes.push(h('div', { class: 'vazio' }, 'Nenhuma descida marcada para este dia.'));
  for (const j of q.horas) {
    partes.push(
      h(
        'section',
        { class: 'janela' },
        h(
          'header',
          {},
          h('b', {}, horaBr(j.hora)),
          j.foraDaGrade
            ? h('span', { class: 'selo alerta' }, 'fora da grade atual: combine novo horário')
            : h('span', { class: `selo ${j.livres === 0 ? 'alerta' : 'neutro'}` }, `${j.ocupadas}/${j.capacidade}${j.ocupadas > j.capacidade ? ' com encaixe' : j.livres === 0 ? ' lotada' : ''}`),
        ),
        h('div', { class: 'grade' }, q.descidas.filter((d) => d.hora === j.hora).map(cartaoRegistro)),
      ),
    );
  }

  if (q.subidas.length) partes.push(h('h2', {}, 'Subidas avisadas'), h('div', { class: 'grade' }, q.subidas.map(cartaoRegistro)));
  if (q.servicos.length) partes.push(h('h2', {}, 'Serviços pedidos'), h('div', { class: 'grade' }, q.servicos.map(cartaoRegistro)));
  if (q.aluguel.length) {
    partes.push(
      h('h2', {}, 'Aluguel'),
      h('div', { class: 'linha' }, q.aluguel.map((i) => h('span', { class: `selo ${i.livres ? 'ok' : 'alerta'}` }, `${i.nome}: ${i.livres} de ${i.unidades} livre(s)`))),
    );
    if (q.reservas.length) partes.push(h('div', { class: 'grade janela' }, q.reservas.map(cartaoRegistro)));
  }
  return partes;
}

// ---------- aprovar ----------

function telaAprovar() {
  if (!E.rascunhos.length) {
    return h(
      'div',
      { class: 'vazio' },
      E.marina.modo === 'sombra'
        ? 'Nenhuma resposta esperando aprovação. Quando um cliente escrever, a resposta do assistente aparece aqui antes de ser enviada.'
        : `O atendente está em modo ${MODOS[E.marina.modo][0].toLowerCase()}: nada passa por aprovação.`,
    );
  }
  return h(
    'div',
    { class: 'pilha' },
    E.rascunhos.map((r) => {
      const chave = `ras:${r.id}`;
      return h(
        'div',
        { class: 'cartao pilha' },
        h('div', { class: 'linha' }, h('h3', { class: 'cresce' }, r.nome), h('small', {}, [r.embarcacao, instante(r.criadoEm)].filter(Boolean).join(' · '))),
        h('div', {}, h('small', {}, 'O cliente escreveu:'), r.perguntas.map((p) => h('div', { class: 'citacao' }, p))),
        h('label', { class: 'campo' }, 'Resposta do assistente (pode editar antes de enviar)', campo('textarea', chave, r.texto, { rows: 4, maxlength: 3000 })),
        r.acoes.length ? h('div', {}, h('small', {}, 'Ao aprovar, também fica valendo:'), h('ul', { class: 'lista-acoes' }, r.acoes.map((a) => h('li', {}, a.resumo)))) : null,
        h(
          'div',
          { class: 'linha' },
          botao(
            'Aprovar e enviar',
            () =>
              agir(async () => {
                await api('POST', `/api/painel/rascunho/${r.id}/aprovar`, { texto: valor(chave, r.texto) });
                local.delete(chave);
              }),
            'primario grande',
          ),
          botao(
            'Descartar e assumir a conversa',
            () =>
              agir(async () => {
                await api('POST', `/api/painel/rascunho/${r.id}/descartar`, {});
                local.delete(chave);
                abrirConversa(r.conversaId);
              }),
            'perigo',
          ),
          botao('Ver conversa', () => abrirConversa(r.conversaId)),
        ),
      );
    }),
  );
}

// ---------- chamados ----------

function cartaoChamado(c) {
  return h(
    'div',
    { class: `cartao chamado ${c.urgencia}` },
    h(
      'div',
      { class: 'linha' },
      h('h3', { class: 'cresce' }, `Para: ${c.para}`),
      h('span', { class: `selo ${c.urgencia === 'normal' ? 'neutro' : c.urgencia === 'alta' ? 'espera' : 'alerta'}` }, c.urgencia === 'emergencia' ? 'EMERGÊNCIA' : `urgência ${c.urgencia}`),
    ),
    h('small', {}, `${c.clienteNome} · ${instante(c.criadoEm)}${c.origem === 'sistema' ? ' · aberto pelo sistema' : ''}`),
    h('p', {}, c.resumo),
    c.status === 'aberto'
      ? h(
          'div',
          { class: 'linha' },
          c.conversaId ? botao('Abrir conversa', () => abrirConversa(c.conversaId), 'primario') : null,
          botao('Marcar como resolvido', () => agir(() => api('POST', `/api/painel/chamado/${c.id}/resolver`, {})), 'ok'),
        )
      : h('small', {}, `Resolvido por ${c.resolvidoPor || 'equipe'} · ${instante(c.resolvidoEm)}`),
  );
}

function telaChamados() {
  const { abertos, resolvidos } = E.chamados;
  return [
    abertos.length ? h('div', { class: 'pilha' }, abertos.map(cartaoChamado)) : h('div', { class: 'vazio' }, 'Nenhum chamado aberto.'),
    resolvidos.length ? h('details', {}, h('summary', {}, h('h2', {}, `Resolvidos recentes (${resolvidos.length})`)), h('div', { class: 'pilha' }, resolvidos.map(cartaoChamado))) : null,
  ];
}

// ---------- conversas ----------

async function carregarFio(id) {
  try {
    const d = await api('GET', `/api/painel/conversa/${id}`);
    if (aberta !== id) return;
    fio = d;
    if (aba === 'conversas') desenhar();
  } catch (e) {
    if (e.status === 404) {
      aberta = null;
      fio = null;
      desenhar();
    }
  }
}

function abrirConversa(id) {
  aba = 'conversas';
  aberta = id;
  fio = null;
  desenhar();
  carregarFio(id);
}

function telaConversas() {
  const lista = h(
    'div',
    { class: 'lista' },
    E.conversas.length
      ? E.conversas.map((c) =>
          h(
            'button',
            { type: 'button', 'aria-current': aberta === c.id ? 'true' : null, onclick: () => abrirConversa(c.id) },
            h(
              'span',
              { class: 'linha' },
              h('b', { class: 'cresce' }, c.nome),
              c.temRascunho ? h('span', { class: 'selo espera' }, 'aprovar') : null,
              c.estado === 'humano' ? h('span', { class: 'selo ok' }, 'equipe') : null,
              c.naoLidas ? h('span', { class: 'conta-n' }, c.naoLidas) : null,
            ),
            h('span', { class: 'trecho' }, `${c.ultima.de === 'cliente' ? '' : '↪ '}${c.ultima.texto}`),
            h('small', {}, `${dataBr(c.ultima.data)} ${c.ultima.hora}`),
          ),
        )
      : h('div', { class: 'vazio' }, 'Nenhuma conversa ainda.'),
  );

  let painelFio;
  if (!aberta) {
    painelFio = h('div', { class: 'vazio fio-vazio' }, 'Escolha uma conversa.');
  } else if (!fio || fio.id !== aberta) {
    painelFio = h('div', { class: 'vazio' }, 'Carregando…');
  } else {
    const chave = `resp:${fio.id}`;
    const comEquipe = fio.estado === 'humano';
    painelFio = h(
      'div',
      { class: 'cartao fio' },
      h(
        'header',
        {},
        h(
          'div',
          { class: 'linha' },
          h('button', { class: 'link voltar', type: 'button', onclick: () => { aberta = null; fio = null; desenhar(); } }, '← Conversas'),
          h('h3', { class: 'cresce' }, fio.nome),
          h('span', { class: `selo ${comEquipe ? 'ok' : ''}` }, comEquipe ? 'Equipe na conversa' : 'Assistente respondendo'),
        ),
        h(
          'div',
          { class: 'linha' },
          h('small', { class: 'cresce' }, fio.embarcacao || (fio.visitante ? 'Link público, sem cadastro' : '')),
          comEquipe
            ? botao('Devolver ao assistente', () => agir(() => api('POST', `/api/painel/conversa/${fio.id}/estado`, { estado: 'ia' })))
            : botao('Assumir a conversa', () => agir(() => api('POST', `/api/painel/conversa/${fio.id}/estado`, { estado: 'humano' }))),
          whats(fio.telefone, `Olá! Aqui é da ${E.marina.nome}.`),
          eu.papel === 'admin'
            ? botao(
                'Apagar',
                () =>
                  dialogo('Apagar conversa', h('p', {}, 'As mensagens e as fotos desta conversa serão apagadas para sempre. Os registros da rampa continuam.'), [
                    botao(
                      'Apagar',
                      () =>
                        agir(async () => {
                          await api('DELETE', `/api/painel/conversa/${fio.id}`, {});
                          aberta = null;
                          fio = null;
                          fecharDialogo();
                        }),
                      'perigo',
                    ),
                  ]),
                'perigo',
              )
            : null,
        ),
      ),
      h(
        'div',
        { class: 'msgs' },
        fio.mensagens.map((m) =>
          h(
            'div',
            { class: `balao ${m.de}` },
            m.tipo === 'foto' ? h('a', { href: m.foto, target: '_blank', rel: 'noopener' }, h('img', { src: m.foto, alt: 'Foto enviada pelo cliente', loading: 'lazy' })) : m.texto,
            h(
              'small',
              {},
              [
                { cliente: 'cliente', assistente: 'assistente', equipe: `equipe${m.autor ? `, ${m.autor}` : ''}`, sistema: 'aviso automático' }[m.de],
                m.aprovadoPor ? `${m.editado ? 'editado e ' : ''}aprovado por ${m.aprovadoPor}` : null,
                `${dataBr(m.data)} ${m.hora}`,
              ]
                .filter(Boolean)
                .join(' · '),
            ),
          ),
        ),
        fio.digitando ? h('div', { class: 'balao assistente suave' }, 'assistente preparando resposta…') : null,
      ),
      h(
        'form',
        {
          onsubmit: (ev) => {
            ev.preventDefault();
            agir(async () => {
              const t = valor(chave).trim();
              if (!t) return;
              await api('POST', `/api/painel/conversa/${fio.id}/responder`, { texto: t });
              local.delete(chave);
            });
          },
        },
        campo('textarea', chave, '', { rows: 2, maxlength: 3000, placeholder: 'Responder como equipe', 'aria-label': 'Responder como equipe' }),
        h('div', { class: 'linha' }, h('small', { class: 'cresce' }, comEquipe ? 'O assistente está parado nesta conversa.' : 'Ao responder, você assume a conversa e o assistente para.'), h('button', { class: 'botao primario' }, 'Enviar')),
      ),
    );
  }
  return h('div', { class: `conversas${aberta ? ' aberta' : ''}` }, lista, painelFio);
}

// ---------- interessados ----------

function telaInteressados() {
  if (!E.leads.length) return h('div', { class: 'vazio' }, 'Nenhum interessado ou reclamação em aberto.');
  const nomes = { 'lead-aluguel': 'Aluguel', 'lead-vaga': 'Vaga', 'lead-venda': 'Compra de embarcação', reclamacao: 'Reclamação' };
  return h(
    'div',
    { class: 'grade' },
    E.leads.map((r) =>
      h(
        'div',
        { class: `cartao pilha${r.tipo === 'reclamacao' ? ' chamado alta' : ''}` },
        h('div', { class: 'linha' }, h('h3', { class: 'cresce' }, r.clienteNome), h('span', { class: `selo ${r.tipo === 'reclamacao' ? 'alerta' : ''}` }, nomes[r.tipo])),
        h('small', {}, [instante(r.criadoEm), r.data ? `para ${dataBr(r.data)}` : '', r.embarcacao].filter(Boolean).join(' · ')),
        r.detalhes ? h('div', {}, r.detalhes) : null,
        h('div', { class: 'linha' }, r.conversaId ? botao('Conversa', () => abrirConversa(r.conversaId), 'primario') : null, botao('Concluir', () => acaoRegistro(r.id, 'concluir'), 'ok'), whats(r.telefone, `Olá! Aqui é da ${E.marina.nome}.`)),
      ),
    ),
  );
}

// ---------- agentes ----------

const DESTINO = { cliente: 'Cliente', interessado: 'Interessado', dono: 'Dono da marina', equipe: 'Equipe da rampa', agencia: 'Agência' };

function cartaoSugestao(s) {
  const chave = `sug:${s.id}`;
  const textoAtual = () => valor(chave, s.texto);
  const concluir = (acao) =>
    agir(async () => {
      await api('POST', `/api/painel/sugestao/${s.id}`, { acao, texto: textoAtual() });
      local.delete(chave);
    });
  const agente = E.agentes.find((a) => a.id === s.agente)?.nome || s.agente;
  const temChat = !!(s.para.clienteId || s.para.conversaId);
  return h(
    'div',
    { class: 'cartao pilha' },
    h('div', { class: 'linha' }, h('h3', { class: 'cresce' }, s.titulo), h('span', { class: 'selo' }, agente), s.viaIA ? h('span', { class: 'selo neutro' }, 'texto da IA') : null),
    h('small', {}, `Para: ${DESTINO[s.para.quem] || ''}${s.para.nome && s.para.quem !== 'equipe' && s.para.quem !== 'dono' && s.para.quem !== 'agencia' ? ` · ${s.para.nome}` : ''}${s.para.telefone ? ` · ${s.para.telefone}` : ' · sem WhatsApp cadastrado'} · ${instante(s.criadoEm)}`),
    campo('textarea', chave, s.texto, { rows: Math.min(14, Math.max(3, s.texto.split('\n').length + 1)), maxlength: 3000, 'aria-label': 'Texto da sugestão' }),
    h(
      'div',
      { class: 'linha' },
      s.para.telefone ? botao('Abrir no WhatsApp', () => window.open(linkWhats(s.para.telefone, textoAtual()), '_blank', 'noopener'), 'primario') : null,
      temChat ? botao('Deixar no chat do cliente', () => concluir('chat')) : null,
      botao('Copiar texto', () => copiar(textoAtual(), 'Texto copiado.')),
      botao('Marcar como enviada', () => concluir('feita'), 'ok'),
      botao('Descartar', () => concluir('descartada'), 'perigo'),
    ),
  );
}

function cartaoAgente(a) {
  return h(
    'div',
    { class: 'cartao pilha' },
    h('div', { class: 'linha' }, h('h3', { class: 'cresce' }, a.nome), h('span', { class: `selo ${a.ativo ? 'ok' : 'neutro'}` }, a.ativo ? 'ligado' : 'desligado')),
    h('div', {}, a.oQue),
    h('small', {}, `Roda ${a.quando}, a partir das ${horaBr(a.hora)}. ${a.ultimaEm ? `Última vez: ${a.ultimaEm}.` : 'Ainda não rodou.'}`),
    a.erro ? h('small', { class: 'erro' }, `Na última vez a IA falhou e os textos-modelo foram usados. ${a.erro}`) : null,
    h(
      'div',
      { class: 'linha' },
      botao('Rodar agora', () =>
        agir(async () => {
          const r = await api('POST', `/api/painel/agente/${a.id}/rodar`, {});
          aviso(r.criadas ? `${r.criadas} sugestão(ões) preparada(s).` : 'Nada novo para sugerir agora.');
        }),
      ),
      a.pendentes ? h('small', {}, `${a.pendentes} sugestão(ões) esperando`) : null,
    ),
  );
}

function telaAgentes() {
  return [
    h('h2', {}, `Sugestões para conferir e enviar (${E.sugestoes.length})`),
    E.sugestoes.length
      ? h('div', { class: 'pilha' }, E.sugestoes.map(cartaoSugestao))
      : h('div', { class: 'vazio' }, 'Nenhuma sugestão esperando. Os agentes preparam mensagens e resumos; nada é enviado sem alguém da equipe conferir.'),
    h('h2', {}, 'Equipe de agentes'),
    h('small', {}, 'O atendente conversa com o cliente. Estes cinco trabalham nos bastidores e deixam o texto pronto para a equipe enviar pelo WhatsApp da marina.'),
    h('div', { class: 'grade janela' }, E.agentes.map(cartaoAgente)),
  ];
}

// ---------- administração ----------

async function carregarAdm() {
  try {
    adm = await api('GET', '/api/painel/admin');
    desenhar();
  } catch {
    /* tratado em api() */
  }
}

function mostrarQr(titulo, url) {
  dialogo(titulo, h('div', { class: 'pilha' }, h('img', { class: 'qr', src: `/api/painel/qr?u=${encodeURIComponent(url)}`, alt: 'Código QR do link' }), h('small', {}, url)), [botao('Copiar link', () => copiar(url), 'primario')]);
}

function formCliente(c) {
  const f = {
    nome: h('input', { value: c?.nome || '', maxlength: 80 }),
    telefone: h('input', { value: c?.telefone || '', maxlength: 20, inputmode: 'tel', placeholder: 'DDD e número' }),
    embarcacao: h('input', { value: c?.embarcacao || '', maxlength: 80, placeholder: 'Lancha "Nome", 24 pés' }),
    autorizados: h('input', { value: c?.autorizados || '', maxlength: 200, placeholder: 'Quem mais pode pedir descida' }),
    obs: h('input', { value: c?.obs || '', maxlength: 300, placeholder: 'Ex.: fala direto com o dono' }),
    pendencia: h('input', { type: 'checkbox', checked: !!c?.pendencia }),
    novoLink: h('input', { type: 'checkbox' }),
    mensalidadeDia: h('input', { type: 'number', min: 1, max: 31, value: c?.mensalidadeDia ?? '', placeholder: 'ex.: 10' }),
    revisaoEm: h('input', { type: 'date', value: c?.revisaoEm || '' }),
    documentoVence: h('input', { type: 'date', value: c?.documentoVence || '' }),
    semLembretes: h('input', { type: 'checkbox', checked: !!c?.semLembretes }),
  };
  dialogo(
    c ? 'Editar cliente' : 'Novo cliente',
    h(
      'div',
      { class: 'formulario' },
      h('label', {}, 'Nome', f.nome),
      h('label', {}, 'WhatsApp', f.telefone),
      h('label', { class: 'larga' }, 'Embarcação', f.embarcacao),
      h('label', { class: 'larga' }, 'Autorizados', f.autorizados),
      h('label', { class: 'larga' }, 'Observação para o assistente', f.obs),
      h('label', {}, 'Dia do vencimento da mensalidade', f.mensalidadeDia),
      h('label', {}, 'Próxima revisão do motor', f.revisaoEm),
      h('label', {}, 'Documento da embarcação vence em', f.documentoVence),
      h('label', { class: 'caixa larga' }, f.semLembretes, 'Não preparar lembretes para este cliente'),
      h('label', { class: 'caixa larga' }, f.pendencia, 'Pendência no cadastro (o assistente não confirma descida e chama a equipe)'),
      c ? h('label', { class: 'caixa larga' }, f.novoLink, 'Gerar link novo (o link antigo para de funcionar)') : null,
    ),
    [
      botao(
        'Salvar',
        () =>
          agir(async () => {
            const corpo = {
              nome: f.nome.value,
              telefone: f.telefone.value,
              embarcacao: f.embarcacao.value,
              autorizados: f.autorizados.value,
              obs: f.obs.value,
              pendencia: f.pendencia.checked,
              novoLink: f.novoLink.checked,
              mensalidadeDia: f.mensalidadeDia.value ? Number(f.mensalidadeDia.value) : null,
              revisaoEm: f.revisaoEm.value,
              documentoVence: f.documentoVence.value,
              semLembretes: f.semLembretes.checked,
            };
            await api(c ? 'PUT' : 'POST', c ? `/api/painel/cliente/${c.id}` : '/api/painel/cliente', corpo);
            fecharDialogo();
            await carregarAdm();
          }),
        'primario',
      ),
    ],
  );
}

function telaClientes() {
  if (!adm) return h('div', { class: 'vazio' }, 'Carregando…');
  const convite = (c) => `Olá, ${c.nome.split(' ')[0]}! Aqui é da ${adm.config.nome}. Agora você pode pedir a descida do seu barco a qualquer hora por este link: ${c.link}`;
  return [
    h(
      'div',
      { class: 'cartao pilha' },
      h('h3', {}, 'Link público'),
      h('small', {}, 'Para quem não é cliente: aluguel, vaga e dúvidas. Coloque na bio do Instagram, na mensagem automática do WhatsApp e num QR na recepção.'),
      h('div', { class: 'linha' }, h('code', { class: 'cresce' }, adm.linkPublico), botao('Copiar', () => copiar(adm.linkPublico)), botao('QR', () => mostrarQr('Link público', adm.linkPublico))),
    ),
    h('div', { class: 'linha' }, h('h2', { class: 'cresce' }, `Clientes (${adm.clientes.length})`), botao('+ Novo cliente', () => formCliente(null), 'primario')),
    adm.clientes.length
      ? h(
          'div',
          { class: 'cartao tabela' },
          h(
            'table',
            {},
            h('thead', {}, h('tr', {}, ['Cliente', 'Embarcação', 'Link pessoal', ''].map((t) => h('th', {}, t)))),
            h(
              'tbody',
              {},
              adm.clientes.map((c) =>
                h(
                  'tr',
                  {},
                  h('td', {}, h('b', {}, c.nome), h('br'), h('small', {}, c.telefone || 'sem WhatsApp'), c.pendencia ? [' ', h('span', { class: 'selo espera' }, 'pendência')] : null),
                  h('td', {}, c.embarcacao, c.autorizados ? [h('br'), h('small', {}, `Autorizados: ${c.autorizados}`)] : null),
                  h('td', {}, h('div', { class: 'linha' }, botao('Copiar', () => copiar(c.link)), whats(c.telefone, convite(c), 'Enviar no WhatsApp'), botao('QR', () => mostrarQr(c.nome, c.link)))),
                  h(
                    'td',
                    {},
                    h(
                      'div',
                      { class: 'linha' },
                      botao('Editar', () => formCliente(c)),
                      botao(
                        'Excluir',
                        () =>
                          dialogo('Excluir cliente', h('p', {}, `Excluir ${c.nome}? O link pessoal para de funcionar e a conversa dele é apagada.`), [
                            botao(
                              'Excluir',
                              () =>
                                agir(async () => {
                                  await api('DELETE', `/api/painel/cliente/${c.id}`, {});
                                  fecharDialogo();
                                  await carregarAdm();
                                }),
                              'perigo',
                            ),
                          ]),
                        'perigo',
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        )
      : h('div', { class: 'vazio' }, 'Nenhum cliente cadastrado. Cada cliente recebe um link pessoal para pedir a descida do barco.'),
  ];
}

function telaConfig() {
  if (!adm) return h('div', { class: 'vazio' }, 'Carregando…');
  const c = adm.config;
  const k = (nome, padrao, attrs = {}) => campo('input', `cfg:${nome}`, padrao, attrs);
  const itens = local.has('cfg:itens') ? local.get('cfg:itens') : c.itensAluguel.map((i) => ({ ...i }));
  const guardarItens = () => local.set('cfg:itens', itens);
  const num = (chave, padrao) => Number(valor(chave, padrao));

  const salvarConfig = () =>
    agir(async () => {
      const r = await api('PUT', '/api/painel/config', {
        nome: valor('cfg:nome', c.nome),
        cidade: valor('cfg:cidade', c.cidade),
        fuso: valor('cfg:fuso', c.fuso),
        agencia: valor('cfg:agencia', c.agencia),
        rampa: {
          abre: valor('cfg:abre', c.rampa.abre),
          ultimaDescida: valor('cfg:ultima', c.rampa.ultimaDescida),
          limiteSubida: valor('cfg:subida', c.rampa.limiteSubida),
          janelaMin: num('cfg:janela', c.rampa.janelaMin),
          capacidade: num('cfg:cap', c.rampa.capacidade),
          antecedenciaMin: num('cfg:antec', c.rampa.antecedenciaMin),
        },
        atendimentoHumano: {
          semana: [valor('cfg:hs0', c.atendimentoHumano.semana[0]), valor('cfg:hs1', c.atendimentoHumano.semana[1])],
          fimDeSemana: [valor('cfg:hf0', c.atendimentoHumano.fimDeSemana[0]), valor('cfg:hf1', c.atendimentoHumano.fimDeSemana[1])],
        },
        preReservaMin: num('cfg:pre', c.preReservaMin),
        emergencia: { telefone: valor('cfg:tel', c.emergencia?.telefone || '') },
        itensAluguel: itens.map((i) => ({ id: i.id, nome: i.nome, unidades: Number(i.unidades) })),
        agentes: Object.fromEntries(E.agentes.map((a) => [a.id, { ativo: valor(`cfg:ag:${a.id}:ativo`, c.agentes[a.id].ativo), hora: valor(`cfg:ag:${a.id}:hora`, c.agentes[a.id].hora) }])),
        contatos: { dono: valor('cfg:dono', c.contatos.dono), equipe: valor('cfg:equipe', c.contatos.equipe) },
        linkAvaliacao: valor('cfg:aval', c.linkAvaliacao),
        relacionamento: {
          diasAntesVencimento: num('cfg:dv', c.relacionamento.diasAntesVencimento),
          diasAntesRevisao: num('cfg:dr', c.relacionamento.diasAntesRevisao),
          diasAntesDocumento: num('cfg:dd', c.relacionamento.diasAntesDocumento),
          diasSumido: num('cfg:ds', c.relacionamento.diasSumido),
        },
      });
      adm.config = r.config;
      for (const chave of [...local.keys()]) if (chave.startsWith('cfg:')) local.delete(chave);
      aviso(r.aviso ? `Configuração salva. Atenção: ${r.aviso}` : 'Configuração salva.');
      desenhar();
    });

  // O relógio da marina: é por ele que o sistema confere horário de rampa e antecedência.
  const seletorFuso = h('select', { 'data-chave': 'cfg:fuso' }, Object.entries(FUSOS).map(([id, rotulo]) => h('option', { value: id }, rotulo)));
  seletorFuso.value = valor('cfg:fuso', c.fuso);

  const linhaItem = (it, i) =>
    h(
      'div',
      { class: 'linha' },
      h('input', { class: 'cresce', value: it.nome, placeholder: 'Nome (ex.: Jet Sea-Doo)', maxlength: 60, 'aria-label': 'Nome do item', 'data-chave': `item:${i}:nome`, oninput: (ev) => { it.nome = ev.target.value; guardarItens(); } }),
      h('input', { class: 'cresce', value: it.id, placeholder: 'código (ex.: jet)', maxlength: 24, 'aria-label': 'Código do item', 'data-chave': `item:${i}:id`, oninput: (ev) => { it.id = ev.target.value; guardarItens(); } }),
      h('input', { class: 'cresce', type: 'number', min: 1, max: 99, value: it.unidades, 'aria-label': 'Unidades', 'data-chave': `item:${i}:unidades`, oninput: (ev) => { it.unidades = ev.target.value; guardarItens(); } }),
      botao('Remover', () => { itens.splice(i, 1); guardarItens(); desenhar(); }),
    );

  return [
    h('h2', {}, 'Marina e regras que o sistema confere'),
    h(
      'div',
      { class: 'cartao pilha' },
      h(
        'div',
        { class: 'formulario' },
        h('label', {}, 'Nome da marina', k('nome', c.nome, { maxlength: 80 })),
        h('label', {}, 'Cidade', k('cidade', c.cidade, { maxlength: 80 })),
        h('label', {}, 'Fuso horário da marina', seletorFuso),
        h('label', {}, 'Telefone de emergência (24h)', k('tel', c.emergencia?.telefone || '', { maxlength: 30 })),
        h('label', {}, 'Rampa abre às', k('abre', c.rampa.abre, { type: 'time' })),
        h('label', {}, 'Última descida', k('ultima', c.rampa.ultimaDescida, { type: 'time' })),
        h('label', {}, 'Limite de subida', k('subida', c.rampa.limiteSubida, { type: 'time' })),
        h('label', {}, 'Janela (minutos)', k('janela', c.rampa.janelaMin, { type: 'number', min: 10, max: 240 })),
        h('label', {}, 'Embarcações por janela', k('cap', c.rampa.capacidade, { type: 'number', min: 1, max: 60 })),
        h('label', {}, 'Antecedência mínima (minutos)', k('antec', c.rampa.antecedenciaMin, { type: 'number', min: 0, max: 2880 })),
        h('label', {}, 'Equipe atende, semana: de', k('hs0', c.atendimentoHumano.semana[0], { type: 'time' })),
        h('label', {}, 'até', k('hs1', c.atendimentoHumano.semana[1], { type: 'time' })),
        h('label', {}, 'Pré-reserva vale (minutos)', k('pre', c.preReservaMin, { type: 'number', min: 10, max: 2880 })),
        h('label', {}, 'Equipe atende, fim de semana: de', k('hf0', c.atendimentoHumano.fimDeSemana[0], { type: 'time' })),
        h('label', {}, 'até', k('hf1', c.atendimentoHumano.fimDeSemana[1], { type: 'time' })),
        h('label', {}, 'Agência (aparece no rodapé)', k('agencia', c.agencia || '', { maxlength: 60 })),
      ),
      h('h3', {}, 'Itens de aluguel'),
      h('small', {}, 'O sistema controla quantas unidades estão livres por dia. Preços e condições ficam na ficha.'),
      itens.map(linhaItem),
      h('div', { class: 'linha' }, botao('+ Item', () => { itens.push({ id: '', nome: '', unidades: 1 }); guardarItens(); desenhar(); }), h('span', { class: 'cresce' }), botao('Salvar configuração', salvarConfig, 'primario')),
    ),
    h('h2', {}, 'Equipe de agentes'),
    h(
      'div',
      { class: 'cartao pilha' },
      h('small', {}, 'Cada agente prepara sugestões na aba Agentes, no horário marcado. Nada é enviado sem alguém conferir.'),
      E.agentes.map((a) =>
        h(
          'div',
          { class: 'linha' },
          h('label', { class: 'caixa cresce' }, caixa(`cfg:ag:${a.id}:ativo`, c.agentes[a.id].ativo), h('span', {}, h('b', {}, a.nome), ` · ${a.quando}`)),
          h('label', { class: 'campo' }, 'a partir das', k(`ag:${a.id}:hora`, c.agentes[a.id].hora, { type: 'time' })),
        ),
      ),
      h(
        'div',
        { class: 'formulario' },
        h('label', {}, 'WhatsApp do dono (recebe o resumo da semana)', k('dono', c.contatos.dono, { maxlength: 20, inputmode: 'tel' })),
        h('label', {}, 'WhatsApp da equipe da rampa (recebe o resumo do dia)', k('equipe', c.contatos.equipe, { maxlength: 20, inputmode: 'tel' })),
        h('label', { class: 'larga' }, 'Link para avaliar a marina no Google (vai na mensagem de pós-passeio)', k('aval', c.linkAvaliacao, { maxlength: 300, placeholder: 'https://' })),
        h('label', {}, 'Lembrar do vencimento quantos dias antes', k('dv', c.relacionamento.diasAntesVencimento, { type: 'number', min: 0, max: 30 })),
        h('label', {}, 'Lembrar da revisão quantos dias antes', k('dr', c.relacionamento.diasAntesRevisao, { type: 'number', min: 0, max: 90 })),
        h('label', {}, 'Lembrar do documento quantos dias antes', k('dd', c.relacionamento.diasAntesDocumento, { type: 'number', min: 0, max: 120 })),
        h('label', {}, 'Cliente "sumido" depois de quantos dias sem sair', k('ds', c.relacionamento.diasSumido, { type: 'number', min: 7, max: 365 })),
      ),
      h('div', { class: 'linha' }, h('span', { class: 'cresce' }), botao('Salvar configuração', salvarConfig, 'primario')),
    ),
    h('h2', {}, 'Ficha da marina'),
    h(
      'div',
      { class: 'cartao pilha' },
      h('small', {}, 'É tudo o que o assistente sabe sobre a marina: preços, políticas, equipe e tom. O que não estiver aqui, ele chama a equipe.'),
      campo('textarea', 'ficha', adm.ficha, { class: 'ficha', maxlength: 40000, 'aria-label': 'Ficha da marina', spellcheck: 'false' }),
      h(
        'div',
        { class: 'linha' },
        h('span', { class: 'cresce' }),
        botao(
          'Salvar ficha',
          () =>
            agir(async () => {
              const ficha = valor('ficha', adm.ficha);
              await api('PUT', '/api/painel/ficha', { ficha });
              adm.ficha = ficha;
              local.delete('ficha');
              aviso('Ficha salva. As próximas respostas já usam a versão nova.');
            }),
          'primario',
        ),
      ),
    ),
    h('h2', {}, 'Dados'),
    h('div', { class: 'cartao linha' }, h('small', { class: 'cresce' }, 'Os dados são da marina. Baixe uma cópia completa quando quiser.'), h('a', { class: 'botao', href: '/api/painel/exportar', download: '' }, 'Baixar todos os dados')),
  ];
}

// ---------- relatório ----------

async function carregarRelatorio() {
  try {
    const q = new URLSearchParams(Object.entries(relPeriodo).filter(([, v]) => v));
    rel = await api('GET', `/api/painel/relatorio?${q}`);
    desenhar();
  } catch {
    /* tratado em api() */
  }
}

function tempo(seg) {
  if (seg === null || seg === undefined) return '–';
  if (seg < 90) return `${Math.round(seg)} s`;
  if (seg < 5400) return `${Math.round(seg / 60)} min`;
  return `${(seg / 3600).toFixed(1).replace('.', ',')} h`;
}

function telaRelatorio() {
  if (!rel) return h('div', { class: 'vazio' }, 'Carregando…');
  const n = (valorN, rotulo) => h('div', { class: 'cartao numero' }, h('b', {}, valorN), h('span', {}, rotulo));
  const usd = (v) => (v === null || v === undefined ? '–' : `US$ ${v.toFixed(v < 1 ? 3 : 2).replace('.', ',')}`);
  const pct = (v) => (v === null || v === undefined ? '–' : `${Math.round(v * 100)}%`);
  return [
    h(
      'div',
      { class: 'linha' },
      h('label', { class: 'campo' }, 'De', h('input', { type: 'date', value: relPeriodo.de, onchange: (ev) => { relPeriodo.de = ev.target.value; carregarRelatorio(); } })),
      h('label', { class: 'campo' }, 'Até', h('input', { type: 'date', value: relPeriodo.ate, onchange: (ev) => { relPeriodo.ate = ev.target.value; carregarRelatorio(); } })),
      h('small', { class: 'cresce' }, relPeriodo.de || relPeriodo.ate ? '' : 'Todo o período'),
      botao('Atualizar', carregarRelatorio),
    ),
    h('h2', {}, 'Atendimento'),
    h(
      'div',
      { class: 'numeros' },
      n(rel.conversas, 'conversas'),
      n(rel.mensagensCliente, 'mensagens de clientes'),
      n(rel.respostasAssistente, 'respostas do assistente'),
      n(rel.respostasEquipe, 'respostas da equipe'),
      n(tempo(rel.tempoResposta.medianaSeg), 'tempo de resposta típico'),
      n(tempo(rel.tempoResposta.p90Seg), '9 em cada 10 respondidas em até'),
      n(rel.foraDoHorario.mensagens, 'mensagens fora do horário da equipe'),
      n(rel.foraDoHorario.respondidasPeloAssistente, 'delas respondidas pelo assistente'),
      n(rel.conversasComEquipe, 'conversas em que a equipe entrou'),
      n(`${rel.aprovacoes.aprovadas - rel.aprovacoes.editadas} / ${rel.aprovacoes.aprovadas}`, 'respostas aprovadas sem edição (modo sombra)'),
    ),
    h('h2', {}, 'Rampa e vendas'),
    h(
      'div',
      { class: 'numeros' },
      n(rel.descidas.total, 'descidas agendadas'),
      n(rel.descidas.peloAssistente, 'agendadas pelo assistente'),
      n(rel.descidas.pelaEquipe, 'lançadas pela equipe'),
      n(rel.subidas, 'subidas avisadas'),
      n(rel.servicos, 'serviços pedidos'),
      n(rel.reservas.confirmadas, 'reservas de aluguel confirmadas'),
      n(rel.reservas.preReservas, 'pré-reservas à espera do sinal'),
      n(rel.leads.aluguel + rel.leads.vaga + rel.leads.venda, 'interessados registrados'),
      n(rel.chamados.total, 'chamados para a equipe'),
      n(rel.chamados.emergencia, 'chamados de emergência'),
    ),
    h('h2', {}, 'Custo da inteligência artificial (estimativa)'),
    h(
      'div',
      { class: 'numeros' },
      n(usd(rel.ia.usd), 'total no período'),
      n(usd(rel.ia.usdPorResposta), 'por resposta do assistente'),
      n(rel.ia.chamadas, 'chamadas ao modelo'),
      n(pct(rel.ia.parteLidaDoCache), 'da entrada lida do cache'),
    ),
    rel.ia.chamadasSemPreco
      ? h('div', { class: 'faixa aviso' }, `${rel.ia.chamadasSemPreco} chamada(s) deste período não têm preço na tabela do aplicativo e ficaram fora do total. O gasto real é maior do que o mostrado: confira a fatura da Anthropic.`)
      : null,
    h(
      'small',
      {},
      `Modelo: ${rel.ia.modelos.filter(Boolean).join(', ') || E.ia.modelo}. O valor é calculado pelos tokens de cada chamada e pela tabela de preços; a fatura da Anthropic é a referência.${rel.ia.manutencoesDeCache ? ` Das chamadas, ${rel.ia.manutencoesDeCache} foram manutenção do cache (releituras baratas que evitam regravar o prompt).` : ''}`,
    ),
  ];
}

// ---------- início ----------

(async () => {
  try {
    const r = await fetch('/api/painel/eu');
    if (r.ok) entrar(await r.json());
    else mostrarLogin();
  } catch {
    mostrarLogin();
  }
})();
