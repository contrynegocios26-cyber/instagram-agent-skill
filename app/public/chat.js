// Chat do cliente. Sem bibliotecas: busca a sessão, mostra as mensagens e
// fica esperando novidades do servidor (long-poll).

const $ = (id) => document.getElementById(id);
const GUARDA = 'marina-chat-chave';
const token = location.pathname.startsWith('/c/') ? decodeURIComponent(location.pathname.slice(3)) : null;

const caixa = $('mensagens');
const campo = $('texto');
let chave = null;
let ultimoId = '';
let digitando = false;
let digitandoDesde = 0;
let assinatura = '';
let ultimoDia = '';
let comEquipe = false;
const pendentes = []; // balões otimistas ainda não confirmados pelo servidor

function el(tag, classe, texto) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (texto !== undefined) e.textContent = texto;
  return e;
}

function pertoDoFim() {
  return caixa.scrollHeight - caixa.scrollTop - caixa.clientHeight < 120;
}
function rolar(forcar) {
  if (forcar || pertoDoFim()) caixa.scrollTop = caixa.scrollHeight;
}

function rotuloDoDia(data) {
  const hoje = new Date();
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const ontem = new Date(hoje.getTime() - 86400000);
  if (data === iso(hoje)) return 'Hoje';
  if (data === iso(ontem)) return 'Ontem';
  const [a, m, d] = data.split('-');
  return `${d}/${m}/${a}`;
}

function balao(m) {
  const meu = m.de === 'cliente';
  const b = el('div', `balao${meu ? ' meu' : ''}${m.de === 'sistema' ? ' sistema' : ''}`);
  if (m.de === 'sistema' && /^Emergência/.test(m.texto)) b.classList.add('emergencia');
  if (m.de === 'equipe') b.append(el('span', 'quem', `Equipe · ${m.autor || 'Marina'}`));
  if (m.tipo === 'foto') {
    const img = el('img');
    img.alt = 'Foto enviada';
    img.loading = 'lazy';
    img.src = m.local || `${m.foto}?k=${encodeURIComponent(chave)}`;
    b.append(img);
  } else if (b.classList.contains('emergencia')) {
    // Na emergência, cada telefone vira um link de ligação.
    for (const parte of m.texto.split(/(\(\d{2}\)\s?\d{4,5}-?\d{4}|\b1\d{2}\b)/)) {
      if (/^(\(\d{2}\)|1\d{2}$)/.test(parte)) {
        const a = el('a', '', parte);
        a.href = `tel:${parte.replace(/\D/g, '')}`;
        b.append(a);
      } else if (parte) {
        b.append(document.createTextNode(parte));
      }
    }
  } else {
    b.append(document.createTextNode(m.texto));
  }
  if (m.hora && m.de !== 'sistema') b.append(el('span', 'hora', m.hora));
  return b;
}

function removerDigitando() {
  $('digitando')?.remove();
}

function mostrarDigitando() {
  removerDigitando();
  if (!digitando) return;
  const b = el('div', 'balao digitando');
  b.id = 'digitando';
  const p = el('span', 'pontos');
  p.append(el('i'), el('i'), el('i'));
  b.append(p);
  if (Date.now() - digitandoDesde > 12000) b.append(el('small', '', 'Só um instante…'));
  caixa.append(b);
}

function acrescentar(mensagens) {
  const noFim = pertoDoFim();
  removerDigitando();
  for (const m of mensagens) {
    if (m.de === 'cliente') {
      const i = pendentes.findIndex((p) => (m.tipo === 'foto' ? p.tipo === 'foto' : p.texto === m.texto));
      if (i !== -1) pendentes.splice(i, 1)[0].no.remove();
    }
    if (m.data && m.data !== ultimoDia) {
      ultimoDia = m.data;
      caixa.append(el('div', 'dia', rotuloDoDia(m.data)));
    }
    caixa.append(balao(m));
    ultimoId = m.id;
  }
  for (const p of pendentes) caixa.append(p.no); // otimistas ficam sempre no fim
  mostrarDigitando();
  if (noFim) rolar(true);
}

const ROTULOS = { confirmado: ['ok', 'confirmado'], 'aguardando equipe': ['espera', 'aguardando a equipe'], 'pre-reserva': ['espera', 'aguardando o sinal'] };

function mostrarAgenda(registros) {
  const caixaAgenda = $('agenda');
  caixaAgenda.replaceChildren();
  caixaAgenda.hidden = registros.length === 0;
  for (const r of registros) {
    const item = el('div', 'item');
    item.append(el('b', '', r.titulo), document.createTextNode(r.quando));
    const [classe, rotulo] = r.etapa === 'na_agua' ? ['agua', 'na água'] : ROTULOS[r.status] || ['espera', r.status];
    item.append(document.createElement('br'), el('span', `selo ${classe}`, rotulo));
    caixaAgenda.append(item);
  }
}

function aplicar(d) {
  if (d.digitando !== digitando) {
    digitando = d.digitando;
    digitandoDesde = digitando ? Date.now() : 0;
  }
  if (d.comEquipe !== comEquipe) {
    comEquipe = d.comEquipe;
    $('status').textContent = comEquipe ? 'Equipe da marina na conversa' : 'Assistente virtual · responde na hora';
  }
  if (d.assinatura !== assinatura) {
    assinatura = d.assinatura;
    mostrarAgenda(d.registros);
  }
  acrescentar(d.mensagens);
}

async function api(caminho, corpo) {
  const r = await fetch(caminho, {
    method: corpo ? 'POST' : 'GET',
    headers: { 'X-Chat': chave, ...(corpo ? { 'Content-Type': 'application/json' } : {}) },
    body: corpo ? JSON.stringify(corpo) : undefined,
  });
  const dados = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error(dados.erro || 'Falha de conexão.'), { status: r.status });
  return dados;
}

const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

async function escutar() {
  let falhas = 0;
  for (;;) {
    try {
      const q = new URLSearchParams({ espera: '1', depois: ultimoId, d: digitando ? '1' : '0', r: assinatura });
      aplicar(await api(`/api/chat/novas?${q}`));
      if (falhas) $('status').textContent = comEquipe ? 'Equipe da marina na conversa' : 'Assistente virtual · responde na hora';
      falhas = 0;
    } catch (e) {
      if (e.status === 401) return telaDeErro('Sua sessão expirou. Abra de novo o link que a marina enviou.');
      falhas++;
      $('status').textContent = 'Sem conexão. Tentando de novo…';
      await dormir(Math.min(15000, 1000 * 2 ** falhas));
    }
  }
}

function avisoLocal(textoAviso) {
  const b = el('div', 'balao sistema', textoAviso);
  caixa.append(b);
  rolar(true);
  setTimeout(() => b.remove(), 6000);
}

async function enviar(textoMsg) {
  const t = textoMsg.trim();
  if (!t || !chave) return;
  const no = balao({ de: 'cliente', texto: t });
  no.classList.add('enviando');
  const p = { texto: t, no };
  pendentes.push(p);
  removerDigitando();
  caixa.append(no);
  rolar(true);
  try {
    await api('/api/chat/enviar', { texto: t });
  } catch (e) {
    const i = pendentes.indexOf(p);
    if (i !== -1) pendentes.splice(i, 1);
    no.remove();
    campo.value = t;
    ajustarAltura();
    avisoLocal(e.message);
  }
}

function ajustarAltura() {
  campo.style.height = 'auto';
  campo.style.height = `${Math.min(campo.scrollHeight, 132)}px`;
  $('btnEnviar').disabled = !campo.value.trim() || !chave;
  // Os atalhos somem enquanto a pessoa digita e voltam com o campo vazio.
  $('atalhos').hidden = !chave || !!campo.value.trim();
}

$('form').addEventListener('submit', (ev) => {
  ev.preventDefault();
  const t = campo.value;
  campo.value = '';
  ajustarAltura();
  enviar(t);
  campo.focus();
});
campo.addEventListener('input', ajustarAltura);
campo.addEventListener('keydown', (ev) => {
  const celular = matchMedia('(pointer: coarse)').matches;
  if (ev.key === 'Enter' && !ev.shiftKey && !celular && !ev.isComposing) {
    ev.preventDefault();
    $('form').requestSubmit();
  }
});

// ---------- foto ----------

function reduzir(arquivo) {
  return new Promise((resolver, rejeitar) => {
    const url = URL.createObjectURL(arquivo);
    const img = new Image();
    img.onload = () => {
      const max = 1600;
      const escala = Math.min(1, max / Math.max(img.width, img.height));
      const c = document.createElement('canvas');
      c.width = Math.round(img.width * escala);
      c.height = Math.round(img.height * escala);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url);
      resolver(c.toDataURL('image/jpeg', 0.82));
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      rejeitar(new Error('Não consegui ler essa imagem.'));
    };
    img.src = url;
  });
}

$('btnFoto').addEventListener('click', () => $('arquivo').click());
$('arquivo').addEventListener('change', async () => {
  const arquivo = $('arquivo').files[0];
  $('arquivo').value = '';
  if (!arquivo || !chave) return;
  let p = null;
  try {
    const dados = await reduzir(arquivo);
    const no = balao({ de: 'cliente', tipo: 'foto', local: dados });
    no.classList.add('enviando');
    p = { tipo: 'foto', no };
    pendentes.push(p);
    caixa.append(no);
    rolar(true);
    await api('/api/chat/foto', { dados });
  } catch (e) {
    if (p) {
      pendentes.splice(pendentes.indexOf(p), 1);
      p.no.remove();
    }
    avisoLocal(e.message);
  }
});

// ---------- início ----------

function telaDeErro(mensagem) {
  caixa.replaceChildren(el('div', 'erro-tela', mensagem));
  $('status').textContent = 'Indisponível';
  campo.disabled = true;
  $('btnEnviar').disabled = true;
  $('btnFoto').disabled = true;
  $('atalhos').hidden = true;
}

function montarAtalhos(d) {
  const frases = d.cliente
    ? ['Quero descer meu barco', 'Estou voltando, pode subir', 'Quero falar com a equipe']
    : [...(d.alugueis ? ['Quero alugar lancha ou jet'] : []), 'Quero guardar meu barco na marina', 'Quero falar com a equipe'];
  const caixaAtalhos = $('atalhos');
  for (const f of frases) {
    const b = el('button', '', f);
    b.type = 'button';
    b.addEventListener('click', () => enviar(f));
    caixaAtalhos.append(b);
  }
}

async function iniciar() {
  let salvo = null;
  try {
    salvo = token ? null : localStorage.getItem(GUARDA);
  } catch {
    /* navegador sem armazenamento: segue sem retomar */
  }
  let d;
  try {
    const r = await fetch('/api/chat/sessao', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(token ? { token } : { chave: salvo }) });
    d = await r.json();
    if (!r.ok) return telaDeErro(d.erro || 'Não foi possível abrir o atendimento.');
  } catch {
    return telaDeErro('Sem conexão. Verifique a internet e abra de novo.');
  }
  chave = d.chave;
  if (!token) {
    try {
      localStorage.setItem(GUARDA, chave);
    } catch {
      /* sem armazenamento */
    }
  }
  document.title = `Atendimento · ${d.marina.nome}`;
  $('marina').textContent = d.marina.nome;
  $('privMarina').textContent = d.marina.nome;
  $('status').textContent = 'Assistente virtual · responde na hora';

  const ola = d.cliente ? `Olá, ${d.cliente.primeiroNome}! ` : '';
  caixa.append(
    el(
      'div',
      'intro',
      `${ola}Você está falando com o assistente virtual da ${d.marina.nome}${d.demonstracao ? ' (modo de demonstração)' : ''}. A equipe assume a conversa quando for preciso.`,
    ),
  );
  campo.disabled = false;
  montarAtalhos(d);
  aplicar(d);
  rolar(true);
  ajustarAltura();
  escutar();
}

$('btnPriv').addEventListener('click', () => $('dlgPriv').showModal());
setInterval(() => digitando && mostrarDigitando() && rolar(), 4000);
iniciar();
