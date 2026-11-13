// Motor do atendimento: recebe a mensagem do cliente, conversa com o modelo,
// executa as ferramentas e entrega a resposta, direto ou via aprovação
// (modo sombra). Também guarda o que acontece quando algo falha: nenhuma
// mensagem de cliente fica sem um humano avisado.

import { novoId } from './store.js';
import { agora, carimbo, normalizarHora, dataPorExtenso } from './tempo.js';
import { promptDeSistema, versaoDoPrompt, contextoDoTurno } from './prompt.js';
import { FalhaIA, custoEstimado } from './ia.js';

const MAX_VOLTAS = 6;
const HORAS_DE_SESSAO = 12;
const MAX_MENSAGENS_API = 80;
const ESPERA_MS = Number(process.env.IA_ESPERA_MS ?? 1500);
const LIMITE_DIARIO = Number(process.env.IA_LIMITE_DIARIO ?? 1500);
// O link público é aberto a qualquer pessoa: ele não pode gastar o teto do
// dia inteiro e deixar os clientes da casa sem atendimento.
const LIMITE_PUBLICO = Number(process.env.IA_LIMITE_DIARIO_PUBLICO ?? Math.floor(LIMITE_DIARIO * 0.4));
const MINUTOS_SEM_RESPOSTA = Number(process.env.AVISO_SEM_RESPOSTA_MIN ?? 10);
const HORA = 3600_000;
// Manutenção do cache do prompt (vale 1 hora): relê entre 50 e 58 minutos
// depois do último uso, e só enquanto houve atendimento nas últimas 24 horas.
const MANTER_DEPOIS_DE_MS = 50 * 60_000;
const MANTER_ATE_MS = 58 * 60_000;
const MANTER_SEM_MOVIMENTO_MS = 24 * HORA;
const MENSAGEM_VELHA_MS = 6 * HORA; // mensagem sem resposta há mais que isso não é respondida sozinha
const AVISO_VALE_MS = 6 * HORA; // um aviso de espera cobre o que o cliente escrever nas 6 horas seguintes
const RASCUNHO_VALE_MS = 6 * HORA; // resposta sem aprovação é desfeita depois disso
const NOVA_TENTATIVA_MS = 15 * 60_000; // depois de uma falha, o assistente tenta de novo após este tempo
const EQUIPE_CALADA_MS = 12 * HORA; // conversa assumida pela equipe volta ao assistente depois disso

const semAcento = (t) => String(t).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

// Só termos que quase nunca aparecem fora de uma emergência real. O texto é
// comparado sem acentos e em minúsculas. O resto fica por conta do
// atendente, que segue a regra de emergência da skill.
const RE_EMERGENCIA =
  /(\ba deriva\b|afundando|afundou|naufrag|homem ao mar|caiu n[ao] (agua|rio)|afogando|afogamento|pegando fogo|incendio|socorro|\bvirou (o|a) (barco|lancha|jet)|\b(barco|lancha|jet|jetski) virou\b|capotou|motor parou no (meio do )?rio|\be (uma )?emergencia\b)/;

export function ehEmergencia(texto) {
  return RE_EMERGENCIA.test(semAcento(texto));
}

export function criarAtendente({ store, agenda, ia, avisar }) {
  const filas = new Map(); // conversaId -> { timer, rodando, denovo }
  const geracao = new Map(); // conversaId -> número que muda a cada fato novo na conversa
  const invalidos = new Set(); // turnos desfeitos por uma ação da equipe
  const usoPorDia = new Map();
  const usoPublicoPorDia = new Map();
  let saude = { ok: true, motivo: null, em: null };
  let cachePrompt = null;
  const agoraMs = () => new Date(carimbo()).getTime();
  const idade = (m) => agoraMs() - new Date(m.em).getTime();

  for (const u of store.lerUso()) {
    if (u.agente || u.aquecimento) continue;
    usoPorDia.set(u.dia, (usoPorDia.get(u.dia) || 0) + 1);
    if (u.publico) usoPublicoPorDia.set(u.dia, (usoPublicoPorDia.get(u.dia) || 0) + 1);
  }

  /** Qualquer fato novo na conversa (mensagem, equipe assumindo) tira a
   *  validade do turno que estiver em andamento: a resposta dele não sai. */
  const tocar = (id) => geracao.set(id, (geracao.get(id) || 0) + 1);

  // ---------- prompt ----------

  function prompt() {
    const chave = `${ia.formato?.() ?? ''}\u0000${store.ficha}\u0000${JSON.stringify(store.config.rampa)}\u0000${JSON.stringify(store.config.itensAluguel)}\u0000${store.config.nome}\u0000${store.config.cidade}\u0000${store.config.preReservaMin}\u0000${store.config.emergencia?.telefone}`;
    if (!cachePrompt || cachePrompt.chave !== chave) {
      const sistema = promptDeSistema(store);
      cachePrompt = { chave, sistema, versao: versaoDoPrompt(sistema, `${ia.modelo}:${ia.formato?.() ?? ''}`) };
    }
    return cachePrompt;
  }

  // ---------- conversas ----------

  function clienteDe(conversa) {
    return conversa.clienteId ? store.clientes.find((c) => c.id === conversa.clienteId) || null : null;
  }

  function criarConversa({ clienteId = null }) {
    const ts = carimbo();
    const c = { id: novoId('con'), clienteId, criadaEm: ts, atualizadaEm: ts, estado: 'ia', humano: null, mensagens: [], thread: null, nota: null, naoLidas: 0 };
    store.conversas.set(c.id, c);
    store.salvar(`conversa:${c.id}`);
    return c;
  }

  function conversaDoCliente(cliente) {
    for (const c of store.conversas.values()) if (c.clienteId === cliente.id) return c;
    return criarConversa({ clienteId: cliente.id });
  }

  function mensagem(conversa, campos) {
    const a = agora();
    const m = { id: novoId('msg'), em: carimbo(), dataLocal: a.data, horaLocal: a.hora, ...campos };
    conversa.mensagens.push(m);
    conversa.atualizadaEm = m.em;
    if (m.de === 'cliente') conversa.naoLidas = (conversa.naoLidas || 0) + 1;
    store.salvar(`conversa:${conversa.id}`);
    avisar(conversa.id);
    return m;
  }

  function paraEquipe(conversa, motivo) {
    conversa.estado = 'humano';
    conversa.humano = { motivo, desde: carimbo() };
    store.salvar(`conversa:${conversa.id}`);
  }

  /** Separa o que o modelo ainda não viu em: mensagens do cliente a responder
   *  e o resto (o que a equipe e o sistema disseram, e mensagens antigas que
   *  ficaram sem resposta), que vira recapitulação. */
  function pendencias(conversa) {
    const naoVistas = conversa.mensagens.filter((m) => !m.visto);
    let corte = -1;
    // Recado da marina (lembrete, retorno) não é resposta ao que o cliente pediu.
    naoVistas.forEach((m, i) => {
      if ((m.de === 'equipe' && !m.recado) || m.de === 'assistente') corte = i;
    });
    // Mensagem que ficou horas sem resposta não é respondida sozinha: quem
    // escreveu "desce amanhã" há uma semana já resolveu de outro jeito.
    const aResponder = naoVistas.filter((m, i) => i > corte && m.de === 'cliente' && idade(m) <= MENSAGEM_VELHA_MS);
    const recap = naoVistas.filter((m) => !aResponder.includes(m));
    return { naoVistas, aResponder, recap };
  }

  /** Mensagens do cliente que ninguém respondeu, descontando as que já
   *  foram cobertas por um aviso de espera recente. */
  function semResposta(conversa) {
    let ini = 0;
    for (let i = conversa.mensagens.length - 1; i >= 0; i--) {
      const m = conversa.mensagens[i];
      if (m.de === 'assistente' || (m.de === 'equipe' && !m.recado)) {
        ini = i + 1;
        break;
      }
    }
    let ultimoAviso = null;
    let primeira = null;
    let escreveu = false;
    for (const m of conversa.mensagens.slice(ini)) {
      const t = new Date(m.em).getTime();
      if (m.de === 'sistema' && m.avisoDeEspera) {
        ultimoAviso = t;
        primeira = null;
      } else if (m.de === 'cliente') {
        escreveu = true;
        const coberta = ultimoAviso !== null && t - ultimoAviso <= AVISO_VALE_MS;
        if (!coberta && !primeira) primeira = m;
      }
    }
    return { primeira, avisado: escreveu && !primeira };
  }

  // ---------- chamados ----------

  const destino = (para) => semAcento(para).split(/[^a-z0-9]+/).filter(Boolean)[0] || '';
  const PESO = { normal: 0, alta: 1, emergencia: 2 };

  function abrirChamado({ conversa, para, urgencia, resumo, origem = 'assistente', turnoId = null }) {
    const urg = ['normal', 'alta', 'emergencia'].includes(urgencia) ? urgencia : 'normal';
    const texto = String(resumo || '').slice(0, 1500);
    let substitui = null;

    if (origem === 'assistente' && conversa) {
      // Emergência relatada pelo atendente completa o chamado vermelho que
      // já está aberto, em vez de abrir outro ao lado.
      if (urg === 'emergencia') {
        const vermelho = store.chamados.find((c) => c.conversaId === conversa.id && c.urgencia === 'emergencia' && c.status === 'aberto' && !c.rascunho);
        if (vermelho) {
          vermelho.resumo = `${vermelho.resumo}\nAtendente: ${texto}`.slice(0, 4000);
          vermelho.atualizadoEm = carimbo();
          store.salvar('chamados');
          avisar();
          return vermelho;
        }
      }
      // Chamado novo para a mesma pessoa, na mesma conversa, atualiza o anterior.
      const anterior = [...store.chamados]
        .reverse()
        .find((c) => c.conversaId === conversa.id && c.origem === 'assistente' && c.status === 'aberto' && destino(c.para) === destino(para || '') && (!c.rascunho || c.rascunho === turnoId));
      if (anterior && anterior.rascunho === turnoId && turnoId) {
        anterior.resumo = texto;
        if (PESO[urg] > PESO[anterior.urgencia]) anterior.urgencia = urg;
        store.salvar('chamados');
        return anterior;
      }
      if (anterior) substitui = anterior.id;
    }

    const cli = conversa ? clienteDe(conversa) : null;
    const ch = {
      id: novoId('cha'),
      para: String(para || 'Equipe').slice(0, 120),
      urgencia: urg,
      resumo: texto,
      conversaId: conversa ? conversa.id : null,
      clienteNome: cli ? cli.nome : 'Visitante',
      origem,
      status: 'aberto',
      criadoEm: carimbo(),
      criadoDia: agora().data,
    };
    if (substitui) ch.substitui = substitui;
    if (turnoId && urg !== 'emergencia') {
      ch.rascunho = turnoId;
    } else if (substitui) {
      const velho = store.chamados.find((c) => c.id === substitui);
      velho.status = 'resolvido';
      velho.resolvidoEm = carimbo();
      velho.resolvidoPor = 'atualizado por um chamado mais novo';
    }
    store.chamados.push(ch);
    store.salvar('chamados');
    avisar();
    return ch;
  }

  function resolverChamado(id, por) {
    const ch = store.chamados.find((x) => x.id === id);
    if (!ch) return null;
    ch.status = 'resolvido';
    ch.resolvidoEm = carimbo();
    ch.resolvidoPor = por;
    store.salvar('chamados');
    avisar();
    return ch;
  }

  const temChamadoDoSistema = (conversa) => store.chamados.some((c) => c.conversaId === conversa.id && c.status === 'aberto' && c.origem === 'sistema' && !c.rascunho);

  // ---------- entrada do cliente ----------

  function receberDoCliente(conversa, { texto, foto }) {
    const emergencia = !!texto && ehEmergencia(texto);

    // Conversa que ficou com a equipe volta ao assistente quando faz sentido:
    // logo depois de uma falha passageira, ou quando a equipe já se calou há
    // muito tempo. Sem isso, uma mensagem de daqui a uma semana cairia no vazio.
    if (conversa.estado === 'humano') {
      const desde = new Date(conversa.humano?.desde || conversa.atualizadaEm).getTime();
      const ultimaDaEquipe = [...conversa.mensagens].reverse().find((m) => m.de === 'equipe' && !m.recado);
      const referencia = Math.max(desde, ultimaDaEquipe ? new Date(ultimaDaEquipe.em).getTime() : 0);
      const volta = conversa.humano?.motivo === 'falha' ? agoraMs() - desde > NOVA_TENTATIVA_MS : agoraMs() - referencia > EQUIPE_CALADA_MS;
      if (volta) {
        conversa.estado = 'ia';
        conversa.humano = null;
      }
    }

    const m = mensagem(conversa, foto ? { de: 'cliente', tipo: 'foto', arquivo: foto, texto: '' } : { de: 'cliente', texto });
    if (emergencia) m.emergencia = true;
    tocar(conversa.id);
    if (foto) agenda.marcarComprovante(conversa.id);

    // Uma mensagem nova invalida a resposta que esperava aprovação.
    for (const pend of store.rascunhos.filter((r) => r.conversaId === conversa.id)) removerRascunho(pend, true);

    // Um aviso e um chamado por conversa a cada 10 minutos: quem repete
    // "socorro" não recebe a mesma mensagem dez vezes nem enche o painel.
    const recente = store.chamados.some(
      (c) => c.conversaId === conversa.id && c.urgencia === 'emergencia' && c.origem === 'sistema' && c.status === 'aberto' && agoraMs() - new Date(c.criadoEm).getTime() < 600_000,
    );
    if (emergencia && !recente) {
      abrirChamado({
        conversa,
        para: 'Toda a equipe',
        urgencia: 'emergencia',
        resumo: `Possível emergência na água. Mensagem do cliente: "${texto.slice(0, 400)}"`,
        origem: 'sistema',
      });
      const tel = store.config.emergencia?.telefone;
      mensagem(conversa, {
        de: 'sistema',
        texto: `Emergência: ${tel ? `ligue agora para a marina no ${tel}. ` : ''}Marinha: 185. Bombeiros: 193. Todos de colete. Já chamei a equipe da marina.`,
      });
    }

    agendar(conversa.id, emergencia ? 0 : ESPERA_MS);
    return m;
  }

  function agendar(id, ms) {
    const f = filas.get(id) || { timer: null, rodando: false, denovo: false };
    filas.set(id, f);
    if (f.timer) clearTimeout(f.timer);
    f.timer = setTimeout(() => {
      f.timer = null;
      rodar(id);
    }, ms);
  }

  async function rodar(id) {
    const f = filas.get(id);
    if (!f) return;
    if (f.rodando) {
      f.denovo = true;
      return;
    }
    f.rodando = true;
    avisar(id);
    try {
      await processar(id);
    } catch (e) {
      console.error(`[atendente] erro inesperado na conversa ${id}:`, e);
    } finally {
      f.rodando = false;
      if (f.denovo) {
        f.denovo = false;
        agendar(id, 200);
      } else if (!f.timer) {
        filas.delete(id);
      }
      avisar(id);
    }
  }

  /** O cliente deve ver "digitando"? Não depois de ouvir que a equipe vai responder. */
  function ocupado(id) {
    const f = filas.get(id);
    if (f && (f.timer || f.rodando)) return true;
    if (!store.rascunhos.some((r) => r.conversaId === id)) return false;
    const conversa = store.conversas.get(id);
    return !!conversa && !semResposta(conversa).avisado;
  }

  async function ocioso() {
    while (filas.size) await new Promise((r) => setTimeout(r, 15));
  }

  /**
   * Roda de minuto em minuto. Cliente esperando há tempo demais, com resposta
   * parada na aprovação ou com a equipe na conversa, recebe um aviso honesto
   * e a equipe recebe um chamado. Também desfaz respostas que ninguém aprovou
   * e apaga conversas que nunca começaram.
   */
  function vigiar() {
    let avisos = 0;
    const agoraEm = agoraMs();

    for (const r of [...store.rascunhos]) {
      if (agoraEm - new Date(r.criadoEm).getTime() < RASCUNHO_VALE_MS) continue;
      const conversa = store.conversas.get(r.conversaId);
      removerRascunho(r, true);
      if (!conversa) continue;
      paraEquipe(conversa, 'equipe');
      if (!temChamadoDoSistema(conversa)) {
        abrirChamado({ conversa, para: 'Equipe', urgencia: 'alta', resumo: 'Uma resposta do assistente ficou horas sem aprovação e foi desfeita. O cliente continua sem resposta.', origem: 'sistema' });
      }
    }

    for (const c of [...store.conversas.values()]) {
      if (!c.mensagens.length) {
        if (!c.clienteId && agoraEm - new Date(c.criadaEm).getTime() > 24 * HORA) {
          store.conversas.delete(c.id);
          store.salvar(`conversa:${c.id}`);
        }
        continue;
      }
      const { primeira } = semResposta(c);
      if (!primeira) continue;
      if (agoraEm - new Date(primeira.em).getTime() < MINUTOS_SEM_RESPOSTA * 60_000) continue;
      if (filas.get(c.id)?.rodando) continue;
      const temRascunho = store.rascunhos.some((r) => r.conversaId === c.id);
      if (!temChamadoDoSistema(c)) {
        abrirChamado({
          conversa: c,
          para: 'Equipe',
          urgencia: 'alta',
          resumo: `Cliente sem resposta há mais de ${MINUTOS_SEM_RESPOSTA} minutos.${temRascunho ? ' Há uma resposta do assistente esperando aprovação.' : ''}`,
          origem: 'sistema',
        });
      }
      mensagem(c, { de: 'sistema', avisoDeEspera: true, texto: 'Sua mensagem está com a equipe da marina, que responde por aqui assim que puder.' });
      avisos++;
    }
    return avisos;
  }

  // ---------- turno ----------

  function semAtendente(conversa, motivo) {
    if (!temChamadoDoSistema(conversa)) {
      abrirChamado({ conversa, para: 'Equipe', urgencia: 'alta', resumo: `${motivo} Cliente aguardando resposta de uma pessoa.`, origem: 'sistema' });
    }
    if (semResposta(conversa).primeira) {
      mensagem(conversa, {
        de: 'sistema',
        avisoDeEspera: true,
        texto: 'Recebemos sua mensagem. O atendimento automático não está disponível agora; a equipe da marina responde por aqui no horário de atendimento.',
      });
    }
  }

  function limparEntrada(inp) {
    const s = (v) => (typeof v === 'string' && v.trim() ? v.trim() : null);
    return {
      tipo: s(inp.tipo),
      data: s(inp.data),
      hora: inp.hora ? normalizarHora(String(inp.hora)) || s(inp.hora) : null,
      item_aluguel: s(inp.item_aluguel),
      registro_id: s(inp.registro_id),
      detalhes: s(inp.detalhes) || '',
      status: s(inp.status) || 'confirmado',
      nome_cliente: s(inp.nome_cliente),
      embarcacao: s(inp.embarcacao),
      telefone: s(inp.telefone),
    };
  }

  function executar(bloco, ctx, acoes) {
    const inp = bloco.input && typeof bloco.input === 'object' ? bloco.input : {};
    if (bloco.name === 'consultar_agenda') return agenda.consultar(String(inp.data || ''));
    if (bloco.name === 'registrar') {
      const r = agenda.registrar(ctx, limparEntrada(inp));
      if (r.ok) acoes.push({ tipo: 'registro', id: r.registro_id, resumo: r.resumo });
      return r;
    }
    if (bloco.name === 'encaminhar') {
      const ch = abrirChamado({ conversa: ctx.conversa, para: inp.para, urgencia: inp.urgencia, resumo: inp.resumo, turnoId: ctx.turnoId });
      const resumo = `chamado para ${ch.para} (${ch.urgencia}): ${String(inp.resumo || '').slice(0, 1500)}`;
      const ja = acoes.find((a) => a.id === ch.id);
      if (ja) ja.resumo = resumo;
      else acoes.push({ tipo: 'chamado', id: ch.id, resumo });
      return { ok: true, chamado_id: ch.id, observacao: `Chamado aberto para ${ch.para}. A equipe vê no painel.` };
    }
    return { ok: false, erro: `Ferramenta desconhecida: ${bloco.name}.` };
  }

  function registrarUso(conversa, resp) {
    const dia = agora().data;
    const publico = !conversa.clienteId;
    usoPorDia.set(dia, (usoPorDia.get(dia) || 0) + 1);
    if (publico) usoPublicoPorDia.set(dia, (usoPublicoPorDia.get(dia) || 0) + 1);
    const u = resp.usage || {};
    store.registrarUso({
      dia,
      em: carimbo(),
      conversaId: conversa.id,
      publico,
      modelo: resp.model || ia.modelo,
      entrada: u.input_tokens ?? 0,
      saida: u.output_tokens ?? 0,
      cacheLeitura: u.cache_read_input_tokens ?? 0,
      cacheGravacao: u.cache_creation_input_tokens ?? 0,
      usd: custoEstimado(resp.model || ia.modelo, u),
    });
  }

  // ---------- manutenção do cache do prompt ----------
  // O prompt fica em cache na Anthropic por 1 hora, e cada leitura renova
  // esse prazo. Se passar mais de uma hora sem movimento, a mensagem seguinte
  // paga de novo a gravação, que custa 40 vezes uma leitura. Para isso não
  // acontecer, o servidor relê o cache pouco antes de ele vencer. A leitura
  // é tão barata que manter o dia inteiro custa menos que uma gravação.

  let cacheQuente = null; // { versao, inicio }: último pedido que gravou ou leu o prompt
  let ultimoAtendimento = 0; // último pedido de verdade (não de manutenção)
  let falhasDeManutencao = 0;
  let manutencaoLigada = typeof ia.aquecer === 'function';

  function cacheUsado(versao, inicio, deVerdade) {
    cacheQuente = { versao, inicio };
    if (deVerdade) ultimoAtendimento = inicio;
  }

  /** Chamada de minuto em minuto. Devolve o que fez, para os testes e o log. */
  async function manterCache() {
    if (!manutencaoLigada || !cacheQuente) return 'parado';
    if (store.config.modo === 'desligado') return 'parado';
    if (agoraMs() - ultimoAtendimento > MANTER_SEM_MOVIMENTO_MS) return 'parado';
    const { sistema, versao } = prompt();
    // A ficha ou a configuração mudou: quem grava a versão nova é a próxima conversa.
    if (versao !== cacheQuente.versao) return 'parado';
    const idadeDoCache = agoraMs() - cacheQuente.inicio;
    if (idadeDoCache < MANTER_DEPOIS_DE_MS) return 'cedo';
    if (idadeDoCache >= MANTER_ATE_MS) {
      cacheQuente = null; // já venceu: a próxima conversa grava de novo
      return 'vencido';
    }
    const inicio = agoraMs();
    cacheQuente = { versao, inicio }; // não repete o pedido enquanto este não volta
    let leu = false;
    try {
      const resp = await ia.aquecer({ sistema });
      const u = resp.usage || {};
      leu = (u.cache_read_input_tokens ?? 0) > 0;
      store.registrarUso({
        dia: agora().data,
        em: carimbo(),
        aquecimento: true,
        modelo: resp.model || ia.modelo,
        entrada: u.input_tokens ?? 0,
        saida: u.output_tokens ?? 0,
        cacheLeitura: u.cache_read_input_tokens ?? 0,
        cacheGravacao: u.cache_creation_input_tokens ?? 0,
        usd: custoEstimado(resp.model || ia.modelo, u),
      });
    } catch (e) {
      console.warn(`[cache] a manutenção do cache falhou: ${e.message}`);
    }
    if (leu) {
      falhasDeManutencao = 0;
      return 'renovado';
    }
    // Não leu nada do cache: ou o pedido falhou, ou ele não bate com o cache
    // dos pedidos de verdade. Insistir só gastaria; depois de duas vezes para.
    falhasDeManutencao++;
    if (falhasDeManutencao >= 2) {
      manutencaoLigada = false;
      console.warn('[cache] a manutenção do cache não está reaproveitando o prompt e foi desligada. O atendimento segue normal; só a primeira resposta depois de uma hora parada custa mais.');
    }
    return 'falhou';
  }

  function limparTexto(t) {
    return t
      .replace(/```[\s\S]*?```/g, '')
      .replace(/\[(REGISTRO|ENCAMINHAR)\][^\n]*(\n[^\n]+)*/g, '')
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  async function processar(id) {
    const conversa = store.conversas.get(id);
    if (!conversa) return;
    const { aResponder, recap } = pendencias(conversa);
    if (!aResponder.length || conversa.estado === 'humano') return;
    const dia = agora().data;
    if (store.config.modo === 'desligado') return semAtendente(conversa, 'Atendente virtual desligado.');
    if ((usoPorDia.get(dia) || 0) >= LIMITE_DIARIO) return semAtendente(conversa, 'Limite diário de respostas automáticas atingido.');
    if (!conversa.clienteId && (usoPublicoPorDia.get(dia) || 0) >= LIMITE_PUBLICO) {
      return semAtendente(conversa, 'Limite diário de respostas automáticas do link público atingido.');
    }

    const cliente = clienteDe(conversa);
    const { sistema, versao } = prompt();
    const turnoId = novoId('tur');
    const g0 = geracao.get(id) || 0;
    const emergencia = aResponder.some((m) => m.emergencia);

    // O histórico da API vale enquanto o prompt, as ferramentas e o modelo
    // forem os mesmos, a conversa estiver recente e não tiver crescido demais.
    const t = conversa.thread;
    const velho = t && agoraMs() - new Date(t.ultimaEm).getTime() > HORAS_DE_SESSAO * HORA;
    const recomeca = !t || t.versao !== versao || velho || t.apiMessages.length > MAX_MENSAGENS_API;
    const mensagensApi = recomeca ? [] : structuredClone(t.apiMessages);
    const historicoAnterior = recomeca ? conversa.mensagens.filter((m) => m.visto).slice(-8) : [];

    // Mensagem que esperou vai com a hora em que foi escrita, para "amanhã"
    // ser lido a partir daquele momento e não de agora.
    const notas = [conversa.nota];
    const maisAntiga = aResponder[0];
    if (idade(maisAntiga) > 30 * 60_000) {
      notas.push(
        `Atenção: a mensagem mais antiga desta leva foi escrita em ${dataPorExtenso(maisAntiga.dataLocal)}, às ${maisAntiga.horaLocal}, e ficou sem resposta até agora. "Hoje" e "amanhã" nela contam a partir daquele momento. Se o pedido era para um horário que já passou, não registre: diga isso ao cliente e pergunte se ele ainda quer.`,
      );
    }

    mensagensApi.push({ role: 'user', content: aResponder.map((m) => ({ type: 'text', text: m.tipo === 'foto' ? '(foto)' : m.texto })) });
    mensagensApi.push({
      role: 'system',
      content: contextoDoTurno({
        store,
        agenda,
        conversa,
        cliente,
        turnoId,
        recapitulacao: recap,
        historicoAnterior,
        fotos: aResponder.filter((m) => m.tipo === 'foto').length,
        emergenciaEnviada: emergencia,
        nota: notas.filter(Boolean).join('\n') || null,
      }),
    });

    const ctx = { cliente, conversa, conversaId: conversa.id, turnoId, origem: 'assistente', por: 'assistente' };
    const acoes = [];
    let final = null;
    // O turno só vale se, quando ele terminar, a conversa estiver como ele a
    // encontrou: sem mensagem nova, sem a equipe ter assumido, sem ter sido
    // apagada, e sem a equipe ter mexido no que ele estava registrando.
    const aindaVale = () => store.conversas.get(id) === conversa && (geracao.get(id) || 0) === g0 && conversa.estado === 'ia' && !invalidos.has(turnoId);

    try {
      for (let volta = 0; volta < MAX_VOLTAS && final === null; volta++) {
        const inicioDoPedido = agoraMs();
        const resp = await ia.criar({ sistema, messages: mensagensApi });
        registrarUso(conversa, resp);
        cacheUsado(versao, inicioDoPedido, true);
        if (resp.stop_reason === 'refusal') throw new FalhaIA('recusa', 'O modelo recusou responder.');
        if (!aindaVale()) break;
        mensagensApi.push({ role: 'assistant', content: resp.content });

        const usos = resp.content.filter((b) => b.type === 'tool_use');
        if (resp.stop_reason === 'tool_use' && usos.length) {
          mensagensApi.push({
            role: 'user',
            content: usos.map((b) => {
              const r = executar(b, ctx, acoes);
              return { type: 'tool_result', tool_use_id: b.id, content: JSON.stringify(r), ...(r.ok ? {} : { is_error: true }) };
            }),
          });
          continue;
        }
        if (resp.stop_reason === 'pause_turn') continue;
        // Só "end_turn" é resposta completa. Corte por tamanho, janela de
        // contexto estourada ou qualquer motivo novo não vai para o cliente.
        if (resp.stop_reason !== 'end_turn' && resp.stop_reason !== 'stop_sequence') {
          throw new FalhaIA('corte', `A resposta do modelo parou antes do fim (${resp.stop_reason}).`);
        }
        final = limparTexto(resp.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n\n'));
        if (!final) throw new FalhaIA('corte', 'O modelo não escreveu resposta ao cliente.');
      }
      if (aindaVale() && final === null) throw new FalhaIA('corte', 'O atendente não concluiu em tempo.');
      saude = { ok: true, motivo: null, em: carimbo() };
    } catch (e) {
      agenda.descartarTurno(turnoId);
      invalidos.delete(turnoId);
      const falha = e instanceof FalhaIA ? e : new FalhaIA('temporaria', 'Erro interno ao gerar a resposta.', e);
      if (!(e instanceof FalhaIA)) console.error('[atendente] erro interno:', e);
      else console.error(`[atendente] falha (${falha.tipo}): ${falha.message}`, falha.cause?.message || '');
      if (falha.tipo === 'config' || falha.tipo === 'requisicao') saude = { ok: false, motivo: falha.message, em: carimbo() };
      if (store.conversas.get(id) !== conversa) return;
      // Um 400 pode vir de histórico que a API não aceita mais: recomeça da próxima vez.
      if (falha.tipo === 'requisicao') conversa.thread = null;
      // Se chegou mensagem nova ou a equipe assumiu, quem vem depois cuida.
      if ((geracao.get(id) || 0) !== g0 || conversa.estado !== 'ia') return;
      paraEquipe(conversa, 'falha');
      if (!temChamadoDoSistema(conversa)) {
        abrirChamado({
          conversa,
          para: 'Equipe',
          urgencia: 'alta',
          resumo: `O atendente virtual não conseguiu responder (${falha.message}). Última mensagem do cliente: "${(aResponder.at(-1).texto || '(foto)').slice(0, 300)}"`,
          origem: 'sistema',
        });
      }
      if (semResposta(conversa).primeira) {
        mensagem(conversa, { de: 'sistema', avisoDeEspera: true, texto: 'Não consegui concluir seu atendimento por aqui. Já chamei a equipe da marina, que continua por este chat.' });
      }
      return;
    }

    if (!aindaVale()) {
      // A conversa mudou enquanto o modelo respondia. Nada do que este turno
      // fez vale; se sobrou mensagem do cliente, o próximo turno responde tudo.
      agenda.descartarTurno(turnoId);
      const refazer = invalidos.delete(turnoId);
      if (refazer && store.conversas.get(id) === conversa) filas.get(id).denovo = true;
      return;
    }

    const rascunho = {
      id: novoId('ras'),
      conversaId: conversa.id,
      turnoId,
      texto: final,
      criadoEm: carimbo(),
      idsVistos: [...aResponder, ...recap].map((m) => m.id),
      thread: { versao, modelo: ia.modelo, apiMessages: mensagensApi, ultimaEm: carimbo() },
      acoes,
      perguntas: aResponder.map((m) => (m.tipo === 'foto' ? '(foto)' : m.texto)),
    };

    if (store.config.modo === 'sombra' && !emergencia) {
      for (const outro of store.rascunhos.filter((r) => r.conversaId === conversa.id)) removerRascunho(outro, true);
      store.rascunhos.push(rascunho);
      store.salvar('rascunhos');
      avisar(conversa.id);
      return;
    }
    efetivar(conversa, rascunho, { texto: final, por: null });
  }

  /** Torna definitivo um turno: registros, chamados, histórico e mensagem. */
  function efetivar(conversa, rascunho, { texto, por }) {
    agenda.confirmarTurno(rascunho.turnoId);
    conversa.thread = rascunho.thread;
    conversa.nota = null;
    const editado = texto.trim() !== rascunho.texto.trim();
    if (editado) {
      conversa.nota = `A equipe editou a sua última resposta antes de enviar. O cliente recebeu este texto: "${texto.trim().slice(0, 800)}"`;
    }
    const vistos = new Set(rascunho.idsVistos);
    for (const m of conversa.mensagens) if (vistos.has(m.id)) m.visto = true;
    conversa.naoLidas = 0;
    const baloes = texto
      .split(/\n\s*\n/)
      .map((p) => p.trim())
      .filter(Boolean);
    const partes = baloes.length > 4 ? [...baloes.slice(0, 3), baloes.slice(3).join('\n\n')] : baloes;
    for (const p of partes) mensagem(conversa, { de: 'assistente', texto: p, visto: true, turno: rascunho.turnoId, ...(por ? { aprovadoPor: por, editado } : {}) });
    avisar();
  }

  // ---------- modo sombra ----------

  function removerRascunho(r, desfazer) {
    if (desfazer) agenda.descartarTurno(r.turnoId);
    store.rascunhos = store.rascunhos.filter((x) => x.id !== r.id);
    store.salvar('rascunhos');
    avisar(r.conversaId);
  }

  function aprovarRascunho(id, { texto, por }) {
    const r = store.rascunhos.find((x) => x.id === id);
    if (!r) return { ok: false, erro: 'Esta resposta não está mais pendente. O cliente pode ter mandado outra mensagem.' };
    const conversa = store.conversas.get(r.conversaId);
    if (!conversa) {
      removerRascunho(r, true);
      return { ok: false, erro: 'Esta conversa foi apagada.' };
    }
    const vencido = agenda.validarTurno(r.turnoId);
    if (vencido) return { ok: false, erro: vencido };
    const final = typeof texto === 'string' && texto.trim() ? texto.trim().slice(0, 3000) : r.texto;
    store.rascunhos = store.rascunhos.filter((x) => x.id !== id);
    store.salvar('rascunhos');
    efetivar(conversa, r, { texto: final, por });
    return { ok: true };
  }

  function descartarRascunho(id, { resposta, por }) {
    const r = store.rascunhos.find((x) => x.id === id);
    if (!r) return { ok: false, erro: 'Esta resposta não está mais pendente.' };
    const conversa = store.conversas.get(r.conversaId);
    removerRascunho(r, true);
    if (!conversa) return { ok: true };
    tocar(conversa.id);
    paraEquipe(conversa, 'equipe');
    if (typeof resposta === 'string' && resposta.trim()) mensagem(conversa, { de: 'equipe', autor: por, texto: resposta.trim().slice(0, 3000) });
    avisar(conversa.id);
    return { ok: true };
  }

  // A equipe mexeu num registro que um turno queria mudar: o rascunho dele
  // some da fila de aprovação e, se o cliente ainda espera, o turno é refeito
  // já com o que a equipe decidiu.
  agenda.definirAoInvalidar((turnoId) => {
    const r = store.rascunhos.find((x) => x.turnoId === turnoId);
    if (!r) {
      invalidos.add(turnoId); // turno ainda em andamento: ele mesmo se descarta ao terminar
      return;
    }
    store.rascunhos = store.rascunhos.filter((x) => x.id !== r.id);
    store.salvar('rascunhos');
    const conversa = store.conversas.get(r.conversaId);
    if (conversa && conversa.estado === 'ia' && pendencias(conversa).aResponder.length) agendar(conversa.id, 300);
    avisar(r.conversaId);
  });

  // ---------- ações da equipe ----------

  function pararFila(conversaId) {
    const f = filas.get(conversaId);
    if (f?.timer) {
      clearTimeout(f.timer);
      f.timer = null;
      if (!f.rodando) filas.delete(conversaId);
    }
  }

  function responderComoEquipe(conversaId, texto, autor) {
    const conversa = store.conversas.get(conversaId);
    if (!conversa) return { ok: false, erro: 'Conversa não encontrada.' };
    for (const pend of store.rascunhos.filter((r) => r.conversaId === conversaId)) removerRascunho(pend, true);
    pararFila(conversaId);
    tocar(conversaId);
    paraEquipe(conversa, 'equipe');
    conversa.naoLidas = 0;
    mensagem(conversa, { de: 'equipe', autor, texto: String(texto).trim().slice(0, 3000) });
    return { ok: true };
  }

  /** Recado da marina deixado no chat do cliente (lembrete, retorno). Não
   *  tira a conversa do assistente: ele vê o recado na próxima vez. */
  function recadoDaMarina(conversaId, texto, autor) {
    const conversa = conversaId ? store.conversas.get(conversaId) : null;
    if (!conversa) return false;
    mensagem(conversa, { de: 'equipe', autor, recado: true, texto: String(texto).trim().slice(0, 3000) });
    return true;
  }

  /** Aviso disparado por uma ação da equipe no painel (liberou, barco na água). */
  function avisarCliente(conversaId, texto) {
    const conversa = conversaId ? store.conversas.get(conversaId) : null;
    if (!conversa) return false;
    mensagem(conversa, { de: 'sistema', texto });
    return true;
  }

  function mudarEstado(conversaId, estado) {
    const conversa = store.conversas.get(conversaId);
    if (!conversa || !['ia', 'humano'].includes(estado)) return { ok: false, erro: 'Pedido inválido.' };
    tocar(conversaId);
    if (estado === 'humano') {
      for (const pend of store.rascunhos.filter((r) => r.conversaId === conversaId)) removerRascunho(pend, true);
      pararFila(conversaId);
      paraEquipe(conversa, 'equipe');
    } else {
      conversa.estado = 'ia';
      conversa.humano = null;
      store.salvar(`conversa:${conversaId}`);
      if (pendencias(conversa).aResponder.length) agendar(conversaId, 100);
    }
    avisar(conversaId);
    return { ok: true };
  }

  function marcarLida(conversaId) {
    const conversa = store.conversas.get(conversaId);
    if (conversa && conversa.naoLidas) {
      conversa.naoLidas = 0;
      store.salvar(`conversa:${conversaId}`);
    }
  }

  /** A conversa vai ser apagada: nada que esteja em andamento nela pode sobrar. */
  function esquecer(conversaId) {
    tocar(conversaId);
    pararFila(conversaId);
    for (const pend of store.rascunhos.filter((r) => r.conversaId === conversaId)) removerRascunho(pend, true);
  }

  /** Na partida: desfaz rascunhos do processo anterior e retoma quem ficou sem resposta. */
  function retomar() {
    agenda.limparRascunhos();
    if (store.rascunhos.length) {
      store.rascunhos = [];
      store.salvar('rascunhos');
    }
    let n = 0;
    for (const c of store.conversas.values()) {
      if (c.estado === 'ia' && pendencias(c).aResponder.length) {
        agendar(c.id, 500);
        n++;
      }
    }
    return n;
  }

  return {
    prompt,
    criarConversa,
    conversaDoCliente,
    clienteDe,
    receberDoCliente,
    ocupado,
    ocioso,
    vigiar,
    aprovarRascunho,
    descartarRascunho,
    responderComoEquipe,
    avisarCliente,
    recadoDaMarina,
    mudarEstado,
    marcarLida,
    esquecer,
    abrirChamado,
    resolverChamado,
    retomar,
    saude: () => saude,
    manterCache,
    usoHoje: () => usoPorDia.get(agora().data) || 0,
    usoPublicoHoje: () => usoPublicoPorDia.get(agora().data) || 0,
    limiteDiario: LIMITE_DIARIO,
    limitePublico: LIMITE_PUBLICO,
  };
}
