// Servidor web: chat do cliente, painel da equipe e administração.

import express from 'express';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import QRCode from 'qrcode';

import { criarStore, novoId, novoToken } from './store.js';
import { semear, completarConfig } from './semente.js';
import { criarAgenda } from './agenda.js';
import { criarIA } from './ia.js';
import { criarAtendente } from './atendente.js';
import { criarEquipe, AGENTES } from './equipe.js';
import { relatorio } from './relatorio.js';
import { assinar, verificar, senhaConfere, lerCookies, criarLimite } from './auth.js';
import { agora, definirFuso, FUSOS, dataValida, horaValida, normalizarHora, dataPorExtenso, dataCurta, horaFalada } from './tempo.js';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const PUBLICO = path.join(aqui, '..', 'public');
const ESPERA_LONGA_MS = Number(process.env.ESPERA_LONGA_MS ?? 25000);
const DIAS_180 = 180 * 86400;
const HORAS_12 = 12 * 3600;

function carregarSenhas(store) {
  const arq = path.join(store.dir, 'senhas.json');
  let salvas = {};
  try {
    salvas = JSON.parse(fs.readFileSync(arq, 'utf8'));
  } catch {
    /* primeira execução */
  }
  const senhas = {
    equipe: process.env.PAINEL_SENHA || salvas.equipe,
    admin: process.env.ADMIN_SENHA || salvas.admin,
  };
  let geradas = false;
  for (const papel of ['equipe', 'admin']) {
    if (!senhas[papel]) {
      senhas[papel] = crypto.randomBytes(9).toString('base64url');
      geradas = true;
    }
  }
  if (geradas) {
    fs.writeFileSync(arq, JSON.stringify({ equipe: senhas.equipe, admin: senhas.admin }, null, 2), { mode: 0o600 });
    console.log(`\nSenhas do painel geradas (guardadas em ${arq}):`);
    console.log(`  equipe: ${senhas.equipe}`);
    console.log(`  admin:  ${senhas.admin}\n`);
  }
  return senhas;
}

const texto = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

export function criarApp({ dir, semente = 'vazio' }) {
  const store = criarStore(dir);
  semear(store, semente);
  completarConfig(store);
  definirFuso(store.config.fuso);
  const agenda = criarAgenda(store);
  const ia = criarIA();
  const segredo = store.segredo();
  const senhas = carregarSenhas(store);
  const permitido = criarLimite();

  // ---------- avisos para quem está esperando (long-poll) ----------

  let versao = 1;
  const esperaPainel = new Set();
  const esperaChat = new Map();

  // Quem avisa pode estar no meio do atendimento de um cliente. Um erro ao
  // responder a um painel que estava esperando não pode subir até ali.
  function chamar(f) {
    try {
      f();
    } catch (e) {
      console.error('[avisos]', e);
    }
  }

  function avisar(conversaId) {
    versao++;
    for (const f of [...esperaPainel]) chamar(f);
    const alvos = conversaId ? [esperaChat.get(conversaId)] : [...esperaChat.values()];
    for (const grupo of alvos) if (grupo) for (const f of [...grupo]) chamar(f);
  }

  function esperar(conjunto, req, res, responder) {
    let feito = false;
    const fim = () => {
      if (feito) return;
      feito = true;
      clearTimeout(timer);
      conjunto.delete(fim);
      if (res.writableEnded) return;
      try {
        responder();
      } catch (e) {
        console.error('[servidor]', e);
        if (!res.headersSent) res.status(500).json({ erro: 'Erro interno. Tente de novo.' });
      }
    };
    const timer = setTimeout(fim, ESPERA_LONGA_MS);
    conjunto.add(fim);
    req.on('close', () => {
      feito = true;
      clearTimeout(timer);
      conjunto.delete(fim);
    });
  }

  const atendente = criarAtendente({ store, agenda, ia, avisar });
  const equipe = criarEquipe({ store, agenda, ia, avisar });

  const app = express();
  app.set('trust proxy', 1);
  app.disable('x-powered-by');

  app.use((req, res, next) => {
    res.set({
      'Content-Security-Policy':
        "default-src 'self'; img-src 'self' data: blob:; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'no-referrer',
      'X-Frame-Options': 'DENY',
    });
    if (req.path.startsWith('/api/')) res.set('Cache-Control', 'no-store');
    next();
  });

  const erro = (res, status, mensagem) => res.status(status).json({ erro: mensagem });
  const baseUrl = (req) => (process.env.URL_PUBLICA || `${req.protocol}://${req.get('host')}`).replace(/\/$/, '');

  // =====================================================================
  // Chat do cliente
  // =====================================================================

  // A chave de um cliente cadastrado carrega a marca do link pessoal: trocar o
  // link no painel derruba as sessões abertas com o link antigo.
  const marca = (token) => crypto.createHash('sha256').update(token).digest('hex').slice(0, 16);

  function conversaDaChave(req) {
    const dados = verificar(req.get('x-chat') || '', segredo, 'chat');
    const conversa = dados ? store.conversas.get(dados.c) || null : null;
    if (!conversa) return null;
    if (conversa.clienteId) {
      const cli = atendente.clienteDe(conversa);
      if (!cli || dados.t !== marca(cli.token)) return null;
    }
    return conversa;
  }

  // O endereço de cada foto leva uma assinatura própria, que só abre aquela
  // foto e vence em 12 horas. A chave da sessão nunca vai em endereço.
  const linkDaFoto = (conversa, arquivo) => `/api/chat/foto/${arquivo}?f=${encodeURIComponent(assinar({ c: conversa.id, n: arquivo }, segredo, HORAS_12, 'foto'))}`;

  function paraCliente(conversa, m) {
    return {
      id: m.id,
      de: m.de,
      autor: m.de === 'equipe' ? m.autor || 'Equipe' : undefined,
      tipo: m.tipo || 'texto',
      texto: m.texto,
      data: m.dataLocal,
      hora: m.horaLocal,
      foto: m.tipo === 'foto' ? linkDaFoto(conversa, m.arquivo) : undefined,
    };
  }

  function agendamentosDe(conversa) {
    const cliente = atendente.clienteDe(conversa);
    return agenda.ativosDe({ cliente, conversaId: conversa.id }).map((r) => ({
      id: r.id,
      tipo: r.tipo,
      titulo: r.tipo === 'reserva' ? agenda.nomeDoItem(r.item) : r.tipo === 'servico' ? r.detalhes : r.tipo,
      quando: r.data ? `${dataCurta(r.data)}${r.hora ? `, ${horaFalada(r.hora)}` : ''}` : '',
      status: r.status,
      etapa: r.etapa || null,
    }));
  }

  function estadoDoChat(conversa, depois) {
    const i = depois ? conversa.mensagens.findIndex((m) => m.id === depois) : -1;
    const registros = agendamentosDe(conversa);
    return {
      mensagens: conversa.mensagens.slice(i + 1).map((m) => paraCliente(conversa, m)),
      digitando: atendente.ocupado(conversa.id),
      comEquipe: conversa.estado === 'humano',
      registros,
      assinatura: registros.map((r) => `${r.id}${r.status}${r.etapa}${r.quando}`).join('|'),
    };
  }

  // Espaço ocupado pelas fotos, para o disco não encher.
  const LIMITE_FOTOS = Number(process.env.FOTOS_LIMITE_MB ?? 1000) * 1024 * 1024;
  const FOTOS_POR_CONVERSA = 40;
  const pastaFotos = path.dirname(store.caminhoFoto('x'));
  let bytesDeFotos = fs.readdirSync(pastaFotos).reduce((t, f) => t + fs.statSync(path.join(pastaFotos, f)).size, 0);

  function apagarFoto(nome) {
    try {
      const arq = store.caminhoFoto(nome);
      bytesDeFotos = Math.max(0, bytesDeFotos - fs.statSync(arq).size);
      fs.rmSync(arq, { force: true });
    } catch {
      /* já não existia */
    }
  }

  const sessaoDoChat = (req, res, next) => {
    req.conversa = conversaDaChave(req);
    if (!req.conversa) return erro(res, 401, 'Sessão expirada. Abra o link de novo.');
    next();
  };

  // A sessão é conferida antes de o servidor ler o corpo de até 8 MB.
  app.post('/api/chat/foto', sessaoDoChat, express.json({ limit: '8mb' }), (req, res) => {
    const conversa = req.conversa;
    if (!permitido(`foto:${conversa.id}`, 6, 600_000)) return erro(res, 429, 'Muitas fotos em pouco tempo. Aguarde um pouco.');
    if (!conversa.clienteId && !permitido(`fotoip:${req.ip}`, 12, 3600_000)) return erro(res, 429, 'Muitas fotos deste aparelho. Tente mais tarde.');
    if (conversa.mensagens.filter((x) => x.tipo === 'foto').length >= FOTOS_POR_CONVERSA) return erro(res, 429, 'Esta conversa já tem fotos demais. Fale com a equipe.');
    if (bytesDeFotos >= LIMITE_FOTOS) return erro(res, 507, 'Não consigo receber fotos agora. Fale com a equipe.');
    const m = /^data:image\/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)$/.exec(req.body?.dados || '');
    if (!m) return erro(res, 400, 'Envie uma foto JPG, PNG ou WebP.');
    const buf = Buffer.from(m[2], 'base64');
    if (buf.length < 100 || buf.length > 5 * 1024 * 1024) return erro(res, 400, 'Foto muito grande. O limite é 5 MB.');
    const assinaturas = {
      jpeg: buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff,
      png: buf.subarray(0, 4).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47])),
      webp: buf.subarray(0, 4).toString('latin1') === 'RIFF' && buf.subarray(8, 12).toString('latin1') === 'WEBP',
    };
    if (!assinaturas[m[1]]) return erro(res, 400, 'Arquivo de imagem inválido.');
    const nome = `${novoId('foto')}.${m[1] === 'jpeg' ? 'jpg' : m[1]}`;
    try {
      fs.writeFileSync(store.caminhoFoto(nome), buf);
    } catch (e) {
      console.error(`[fotos] ${e.message}`);
      return erro(res, 507, 'Não consigo receber fotos agora. Fale com a equipe.');
    }
    bytesDeFotos += buf.length;
    const msg = atendente.receberDoCliente(conversa, { foto: nome });
    res.json({ ok: true, id: msg.id });
  });

  app.use(express.json({ limit: '100kb' }));
  app.use((err, req, res, next) => {
    if (err?.type === 'entity.parse.failed' || err?.type === 'entity.too.large') return erro(res, 400, 'Pedido inválido.');
    next(err);
  });

  app.post('/api/chat/sessao', (req, res) => {
    const corpo = req.body || {};
    let conversa = null;
    if (typeof corpo.token === 'string' && corpo.token) {
      if (!permitido(`token:${req.ip}`, 30, 600_000)) return erro(res, 429, 'Muitas tentativas. Aguarde alguns minutos.');
      const cliente = store.clientes.find((c) => c.token === corpo.token);
      if (!cliente) return erro(res, 404, 'Este link não é mais válido. Peça um novo à marina.');
      conversa = atendente.conversaDoCliente(cliente);
    } else {
      const dados = verificar(corpo.chave, segredo, 'chat');
      conversa = dados ? store.conversas.get(dados.c) : null;
      if (conversa && conversa.clienteId) conversa = null; // conversa de cadastro só entra pelo link pessoal
      if (!conversa) {
        if (!permitido(`nova:${req.ip}`, 10, 3600_000)) return erro(res, 429, 'Muitas conversas abertas deste aparelho. Tente mais tarde.');
        conversa = atendente.criarConversa({});
      }
    }
    const cliente = atendente.clienteDe(conversa);
    res.json({
      chave: assinar(cliente ? { c: conversa.id, t: marca(cliente.token) } : { c: conversa.id }, segredo, DIAS_180, 'chat'),
      marina: { nome: store.config.nome, cidade: store.config.cidade, agencia: store.config.agencia || '' },
      cliente: cliente ? { primeiroNome: cliente.nome.split(' ')[0], embarcacao: cliente.embarcacao } : null,
      alugueis: (store.config.itensAluguel || []).length > 0,
      demonstracao: ia.demonstracao,
      ...estadoDoChat(conversa, null),
    });
  });

  app.get('/api/chat/novas', (req, res) => {
    const conversa = conversaDaChave(req);
    if (!conversa) return erro(res, 401, 'Sessão expirada. Abra o link de novo.');
    const depois = typeof req.query.depois === 'string' ? req.query.depois : '';
    const responder = () => res.json(estadoDoChat(conversa, depois));
    const e = estadoDoChat(conversa, depois);
    const mudou = e.mensagens.length > 0 || String(e.digitando ? 1 : 0) !== req.query.d || e.assinatura !== (req.query.r ?? '');
    if (mudou || req.query.espera !== '1') return res.json(e);
    if (!esperaChat.has(conversa.id)) esperaChat.set(conversa.id, new Set());
    esperar(esperaChat.get(conversa.id), req, res, responder);
  });

  app.post('/api/chat/enviar', (req, res) => {
    const conversa = conversaDaChave(req);
    if (!conversa) return erro(res, 401, 'Sessão expirada. Abra o link de novo.');
    const t = texto(req.body?.texto, 1200);
    if (!t) return erro(res, 400, 'Escreva uma mensagem.');
    if (!permitido(`msg:${conversa.id}`, 20, 600_000)) return erro(res, 429, 'Muitas mensagens em pouco tempo. Aguarde um instante.');
    // No link público o limite vale também por aparelho, somando todas as conversas dele.
    if (!conversa.clienteId && !permitido(`msgip:${req.ip}`, 40, 600_000)) return erro(res, 429, 'Muitas mensagens deste aparelho. Aguarde um instante.');
    const msg = atendente.receberDoCliente(conversa, { texto: t });
    res.json({ ok: true, id: msg.id });
  });

  function enviarFoto(res, nome) {
    const limpo = path.basename(String(nome));
    const arq = store.caminhoFoto(limpo);
    if (!/^foto_[0-9a-f]+\.(jpg|png|webp)$/.test(limpo) || !fs.existsSync(arq)) return erro(res, 404, 'Foto não encontrada.');
    res.set({ 'Cache-Control': 'private, max-age=3600', 'Content-Disposition': 'inline' });
    res.sendFile(arq);
  }

  app.get('/api/chat/foto/:nome', (req, res) => {
    const dados = verificar(typeof req.query.f === 'string' ? req.query.f : '', segredo, 'foto');
    const conversa = dados && dados.n === req.params.nome ? store.conversas.get(dados.c) : null;
    if (!conversa || !conversa.mensagens.some((m) => m.arquivo === req.params.nome)) return erro(res, 404, 'Foto não encontrada.');
    enviarFoto(res, req.params.nome);
  });

  // =====================================================================
  // Painel da equipe
  // =====================================================================

  function sessaoDoPainel(req) {
    const s = verificar(lerCookies(req).painel, segredo, 'painel');
    return s && (s.p === 'equipe' || s.p === 'admin') ? s : null;
  }

  function exigir(papel) {
    return (req, res, next) => {
      const s = sessaoDoPainel(req);
      if (!s) return erro(res, 401, 'Entre no painel.');
      if (papel === 'admin' && s.p !== 'admin') return erro(res, 403, 'Só o administrador pode fazer isso.');
      if (req.method !== 'GET' && req.get('x-painel') !== '1') return erro(res, 400, 'Pedido inválido.');
      req.sessao = s;
      next();
    };
  }
  const equipe_ = exigir('equipe');
  const admin = exigir('admin');

  app.post('/api/painel/login', (req, res) => {
    if (!permitido(`login:${req.ip}`, 8, 600_000)) return erro(res, 429, 'Muitas tentativas. Aguarde 10 minutos.');
    const senha = req.body?.senha;
    const nome = texto(req.body?.nome, 40) || 'Equipe';
    const papel = senhaConfere(senha, senhas.admin) ? 'admin' : senhaConfere(senha, senhas.equipe) ? 'equipe' : null;
    if (!papel) return erro(res, 401, 'Senha incorreta.');
    const seguro = req.secure || process.env.COOKIE_SEGURO === '1';
    res.set(
      'Set-Cookie',
      `painel=${encodeURIComponent(assinar({ p: papel, n: nome }, segredo, HORAS_12, 'painel'))}; Path=/; HttpOnly; SameSite=Strict; Max-Age=${HORAS_12}${seguro ? '; Secure' : ''}`,
    );
    res.json({ papel, nome });
  });

  app.post('/api/painel/sair', (req, res) => {
    res.set('Set-Cookie', 'painel=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0');
    res.json({ ok: true });
  });

  app.get('/api/painel/eu', (req, res) => {
    const s = sessaoDoPainel(req);
    if (!s) return erro(res, 401, 'Entre no painel.');
    res.json({ papel: s.p, nome: s.n });
  });

  const telefoneDe = (clienteId) => (clienteId ? store.clientes.find((c) => c.id === clienteId)?.telefone || '' : '');
  const comTelefone = (r) => ({ ...r, telefone: telefoneDe(r.clienteId) || r.telefone || '', pendente: undefined, historico: undefined });

  function nomeDaConversa(c) {
    if (!c) return { nome: 'Conversa apagada', embarcacao: '', visitante: true, telefone: '' };
    const cli = atendente.clienteDe(c);
    if (cli) return { nome: cli.nome, embarcacao: cli.embarcacao, visitante: false, telefone: cli.telefone || '' };
    const reg = store.registros.find((r) => r.conversaId === c.id && r.clienteNome && r.clienteNome !== 'Visitante');
    return { nome: reg ? `${reg.clienteNome} (visitante)` : `Visitante ${c.id.slice(-4)}`, embarcacao: reg?.embarcacao || '', visitante: true, telefone: '' };
  }

  const PESO = { emergencia: 0, alta: 1, normal: 2 };

  function estadoDoPainel(data) {
    const abertos = store.chamados
      .filter((c) => !c.rascunho && c.status === 'aberto')
      .sort((a, b) => PESO[a.urgencia] - PESO[b.urgencia] || a.criadoEm.localeCompare(b.criadoEm));
    const resolvidos = store.chamados
      .filter((c) => !c.rascunho && c.status === 'resolvido')
      .sort((a, b) => b.resolvidoEm.localeCompare(a.resolvidoEm))
      .slice(0, 15);
    const conversas = [...store.conversas.values()]
      .filter((c) => c.mensagens.length)
      .sort((a, b) => b.atualizadaEm.localeCompare(a.atualizadaEm))
      .slice(0, 150)
      .map((c) => {
        const u = c.mensagens.at(-1);
        return {
          id: c.id,
          ...nomeDaConversa(c),
          estado: c.estado,
          naoLidas: c.estado === 'humano' ? c.naoLidas || 0 : 0,
          temRascunho: store.rascunhos.some((r) => r.conversaId === c.id),
          ultima: { de: u.de, texto: u.tipo === 'foto' ? '(foto)' : u.texto.slice(0, 90), data: u.dataLocal, hora: u.horaLocal },
        };
      });
    const q = agenda.quadro(data);
    const pend = agenda.pendentes();
    return {
      v: versao,
      agora: agora(),
      marina: { nome: store.config.nome, modo: store.config.modo, fuso: store.config.fuso, avisoDoDia: store.config.avisoDoDia },
      demonstracao: ia.demonstracao,
      saude: atendente.saude(),
      ia: { usoHoje: atendente.usoHoje(), limite: atendente.limiteDiario, usoPublicoHoje: atendente.usoPublicoHoje(), limitePublico: atendente.limitePublico, modelo: ia.modelo },
      quadro: { ...q, descidas: q.descidas.map(comTelefone), subidas: q.subidas.map(comTelefone), servicos: q.servicos.map(comTelefone), reservas: q.reservas.map(comTelefone) },
      pendentes: pend.map(comTelefone),
      chamados: { abertos, resolvidos },
      rascunhos: store.rascunhos.filter((r) => store.conversas.has(r.conversaId)).map((r) => ({
        id: r.id,
        conversaId: r.conversaId,
        ...nomeDaConversa(store.conversas.get(r.conversaId)),
        perguntas: r.perguntas,
        texto: r.texto,
        acoes: r.acoes,
        criadoEm: r.criadoEm,
      })),
      conversas,
      leads: agenda.leads().slice(0, 60).map(comTelefone),
      clientes: store.clientes.map((c) => ({ id: c.id, nome: c.nome, embarcacao: c.embarcacao })),
      sugestoes: equipe.pendentes().slice(0, 100),
      agentes: equipe.resumo(),
      contadores: {
        chamados: abertos.length,
        emergencias: abertos.filter((c) => c.urgencia === 'emergencia').length,
        rascunhos: store.rascunhos.filter((r) => store.conversas.has(r.conversaId)).length,
        pendentes: pend.length,
        sugestoes: equipe.pendentes().length,
        naoLidas: conversas.reduce((t, c) => t + c.naoLidas, 0),
      },
    };
  }

  app.get('/api/painel/estado', equipe_, (req, res) => {
    const data = dataValida(req.query.data) ? req.query.data : agora().data;
    const responder = () => res.json(estadoDoPainel(data));
    if (req.query.espera !== '1' || Number(req.query.v) !== versao) return responder();
    esperar(esperaPainel, req, res, responder);
  });

  app.get('/api/painel/conversa/:id', equipe_, (req, res) => {
    const c = store.conversas.get(req.params.id);
    if (!c) return erro(res, 404, 'Conversa não encontrada.');
    atendente.marcarLida(c.id);
    res.json({
      id: c.id,
      ...nomeDaConversa(c),
      estado: c.estado,
      digitando: atendente.ocupado(c.id),
      mensagens: c.mensagens.map((m) => ({
        id: m.id,
        de: m.de,
        autor: m.autor,
        tipo: m.tipo || 'texto',
        texto: m.texto,
        data: m.dataLocal,
        hora: m.horaLocal,
        foto: m.tipo === 'foto' ? `/api/painel/foto/${m.arquivo}` : undefined,
        aprovadoPor: m.aprovadoPor,
        editado: m.editado,
      })),
    });
  });

  app.get('/api/painel/foto/:nome', equipe_, (req, res) => enviarFoto(res, req.params.nome));

  app.post('/api/painel/conversa/:id/responder', equipe_, (req, res) => {
    const t = texto(req.body?.texto, 3000);
    if (!t) return erro(res, 400, 'Escreva a resposta.');
    const r = atendente.responderComoEquipe(req.params.id, t, req.sessao.n);
    return r.ok ? res.json(r) : erro(res, 404, r.erro);
  });

  app.post('/api/painel/conversa/:id/estado', equipe_, (req, res) => {
    const r = atendente.mudarEstado(req.params.id, req.body?.estado);
    return r.ok ? res.json(r) : erro(res, 400, r.erro);
  });

  app.post('/api/painel/rascunho/:id/aprovar', equipe_, (req, res) => {
    const r = atendente.aprovarRascunho(req.params.id, { texto: req.body?.texto, por: req.sessao.n });
    return r.ok ? res.json(r) : erro(res, 409, r.erro);
  });

  app.post('/api/painel/rascunho/:id/descartar', equipe_, (req, res) => {
    const r = atendente.descartarRascunho(req.params.id, { resposta: req.body?.resposta, por: req.sessao.n });
    return r.ok ? res.json(r) : erro(res, 409, r.erro);
  });

  app.post('/api/painel/chamado/:id/resolver', equipe_, (req, res) => {
    const ch = atendente.resolverChamado(req.params.id, req.sessao.n);
    return ch ? res.json({ ok: true }) : erro(res, 404, 'Chamado não encontrado.');
  });

  app.post('/api/painel/aviso', equipe_, (req, res) => {
    const a = agora();
    store.config.avisoDoDia = { texto: texto(req.body?.texto, 500), atualizadoEm: `${dataPorExtenso(a.data)}, ${a.hora}` };
    store.salvar('config');
    avisar();
    res.json({ ok: true });
  });

  app.post('/api/painel/modo', equipe_, (req, res) => {
    const modo = req.body?.modo;
    if (!['auto', 'sombra', 'desligado'].includes(modo)) return erro(res, 400, 'Modo inválido.');
    if (modo === 'auto' && req.sessao.p !== 'admin') return erro(res, 403, 'Só o administrador liga o modo automático.');
    store.config.modo = modo;
    store.salvar('config');
    avisar();
    res.json({ ok: true });
  });

  function frase(reg) {
    const oQue = reg.tipo === 'reserva' ? `reserva de ${agenda.nomeDoItem(reg.item)}` : `${reg.tipo}${reg.embarcacao ? ` de ${reg.embarcacao}` : ''}`;
    const quando = reg.data ? ` em ${dataPorExtenso(reg.data)}${reg.hora ? `, às ${horaFalada(reg.hora)}` : ''}` : '';
    return `${oQue}${quando}`;
  }

  app.post('/api/painel/registro/:id/acao', equipe_, (req, res) => {
    const { acao } = req.body || {};
    const motivo = texto(req.body?.motivo, 300);
    const por = req.sessao.n;
    const id = req.params.id;
    const avisarCli = req.body?.avisar !== false;
    let r;
    let aviso = null;
    if (acao === 'liberar') {
      r = agenda.liberar(id, por, { forcar: req.body?.forcar === true });
      if (r.ok) aviso = `A equipe confirmou: ${frase(r.registro)}.`;
    } else if (acao === 'recusar' || acao === 'cancelar') {
      r = agenda.recusar(id, por, motivo);
      if (r.ok) aviso = `A equipe ${r.registro.status === 'cancelado' ? 'cancelou' : 'não confirmou'}: ${frase(r.registro)}.${motivo ? ` Motivo: ${motivo}` : ''}`;
    } else if (acao === 'na_agua' || acao === 'guardada' || acao === 'agendada') {
      r = agenda.mudarEtapa(id, acao, por);
      if (r.ok && acao === 'na_agua') aviso = `${r.registro.embarcacao || 'Sua embarcação'} está na água. Bom passeio!`;
      if (r.ok && acao === 'guardada') aviso = `${r.registro.embarcacao || 'Sua embarcação'} já está guardada. Até a próxima!`;
    } else if (acao === 'pagamento') {
      r = agenda.confirmarPagamento(id, por);
      if (r.ok) aviso = `Pagamento confirmado: ${frase(r.registro)} está garantida.`;
    } else if (acao === 'concluir') {
      r = agenda.concluir(id, por);
    } else {
      return erro(res, 400, 'Ação desconhecida.');
    }
    if (!r.ok) return erro(res, 409, r.erro);
    if (aviso && avisarCli) {
      const conversaId = r.registro.conversaId || [...store.conversas.values()].find((c) => c.clienteId && c.clienteId === r.registro.clienteId)?.id;
      atendente.avisarCliente(conversaId, aviso);
    }
    avisar();
    res.json({ ok: true, aviso });
  });

  app.post('/api/painel/registro', equipe_, (req, res) => {
    const b = req.body || {};
    if (!['descida', 'subida', 'servico', 'reserva'].includes(b.tipo)) return erro(res, 400, 'Tipo inválido.');
    const cliente = b.clienteId ? store.clientes.find((c) => c.id === b.clienteId) || null : null;
    if (!cliente && !texto(b.nome, 80)) return erro(res, 400, 'Escolha um cliente ou informe o nome.');
    const hora = b.hora ? normalizarHora(String(b.hora)) : null;
    if (b.hora && !hora) return erro(res, 400, 'Hora inválida.');
    const conversa = cliente ? [...store.conversas.values()].find((c) => c.clienteId === cliente.id) : null;
    const r = agenda.registrar(
      { cliente, conversaId: conversa?.id || null, origem: 'equipe', por: req.sessao.n, forcar: b.forcar === true },
      {
        tipo: b.tipo,
        data: texto(b.data, 10) || null,
        hora,
        item_aluguel: texto(b.item, 24) || null,
        detalhes: texto(b.detalhes, 500),
        status: 'confirmado',
        nome_cliente: texto(b.nome, 80) || null,
        embarcacao: texto(b.embarcacao, 80) || null,
      },
    );
    if (!r.ok) return erro(res, 409, r.erro);
    avisar();
    res.json(r);
  });

  // ---------- equipe de agentes ----------

  app.post('/api/painel/agente/:id/rodar', equipe_, async (req, res) => {
    if (!permitido(`agente:${req.sessao.n}`, 20, 600_000)) return erro(res, 429, 'Muitas execuções em pouco tempo. Aguarde um pouco.');
    const r = await equipe.rodar(req.params.id, { por: req.sessao.n });
    return r.ok ? res.json(r) : erro(res, 409, r.erro);
  });

  app.post('/api/painel/sugestao/:id', equipe_, (req, res) => {
    const { acao } = req.body || {};
    const novoTexto = texto(req.body?.texto, 3000);
    const s = store.sugestoes.find((x) => x.id === req.params.id);
    if (!s) return erro(res, 404, 'Sugestão não encontrada.');
    if (acao === 'chat') {
      if (s.status !== 'pendente') return erro(res, 409, 'Esta sugestão já foi tratada.');
      const conversaId = s.para?.conversaId || [...store.conversas.values()].find((c) => c.clienteId && c.clienteId === s.para?.clienteId)?.id;
      const cli = s.para?.clienteId ? store.clientes.find((c) => c.id === s.para.clienteId) : null;
      const conversa = conversaId ? store.conversas.get(conversaId) : cli ? atendente.conversaDoCliente(cli) : null;
      if (!conversa) return erro(res, 409, 'Esta pessoa não tem conversa no link de atendimento. Use o WhatsApp.');
      atendente.recadoDaMarina(conversa.id, novoTexto || s.texto, req.sessao.n);
    } else if (acao !== 'feita' && acao !== 'descartada') {
      return erro(res, 400, 'Ação inválida.');
    }
    const r = equipe.concluir(s.id, { acao: acao === 'descartada' ? 'descartada' : 'feita', texto: novoTexto, por: req.sessao.n });
    return r.ok ? res.json({ ok: true }) : erro(res, 409, r.erro);
  });

  app.get('/api/painel/qr', equipe_, async (req, res) => {
    const u = typeof req.query.u === 'string' ? req.query.u : '';
    if (!u.startsWith(baseUrl(req)) || u.length > 300) return erro(res, 400, 'Endereço inválido.');
    res.type('image/svg+xml').send(await QRCode.toString(u, { type: 'svg', margin: 1, width: 320 }));
  });

  // =====================================================================
  // Administração
  // =====================================================================

  const linkDoCliente = (req, c) => `${baseUrl(req)}/c/${c.token}`;

  app.get('/api/painel/admin', admin, (req, res) => {
    res.json({
      config: store.config,
      ficha: store.ficha,
      linkPublico: `${baseUrl(req)}/`,
      clientes: store.clientes.map((c) => ({ ...c, token: undefined, link: linkDoCliente(req, c) })),
    });
  });

  const hhmm = (v, padrao) => (horaValida(v) ? v : padrao);
  const inteiro = (v, min, max, padrao) => (Number.isInteger(v) && v >= min && v <= max ? v : padrao);

  app.put('/api/painel/config', admin, (req, res) => {
    const b = req.body || {};
    const c = store.config;
    const rampa = b.rampa || {};
    const nova = {
      ...c,
      nome: texto(b.nome, 80) || c.nome,
      cidade: 'cidade' in b ? texto(b.cidade, 80) : c.cidade,
      fuso: typeof b.fuso === 'string' && b.fuso in FUSOS ? b.fuso : c.fuso,
      agencia: 'agencia' in b ? texto(b.agencia, 60) : c.agencia,
      rampa: {
        abre: hhmm(rampa.abre, c.rampa.abre),
        ultimaDescida: hhmm(rampa.ultimaDescida, c.rampa.ultimaDescida),
        limiteSubida: hhmm(rampa.limiteSubida, c.rampa.limiteSubida),
        janelaMin: inteiro(rampa.janelaMin, 10, 240, c.rampa.janelaMin),
        capacidade: inteiro(rampa.capacidade, 1, 60, c.rampa.capacidade),
        antecedenciaMin: inteiro(rampa.antecedenciaMin, 0, 2880, c.rampa.antecedenciaMin),
      },
      atendimentoHumano: {
        semana: [hhmm(b.atendimentoHumano?.semana?.[0], c.atendimentoHumano.semana[0]), hhmm(b.atendimentoHumano?.semana?.[1], c.atendimentoHumano.semana[1])],
        fimDeSemana: [
          hhmm(b.atendimentoHumano?.fimDeSemana?.[0], c.atendimentoHumano.fimDeSemana[0]),
          hhmm(b.atendimentoHumano?.fimDeSemana?.[1], c.atendimentoHumano.fimDeSemana[1]),
        ],
      },
      preReservaMin: inteiro(b.preReservaMin, 10, 2880, c.preReservaMin),
      emergencia: { telefone: 'emergencia' in b ? texto(b.emergencia?.telefone, 30) : c.emergencia?.telefone || '' },
      agentes: Object.fromEntries(
        Object.keys(AGENTES).map((id) => [
          id,
          { ativo: typeof b.agentes?.[id]?.ativo === 'boolean' ? b.agentes[id].ativo : c.agentes[id].ativo, hora: hhmm(b.agentes?.[id]?.hora, c.agentes[id].hora) },
        ]),
      ),
      contatos: {
        dono: 'contatos' in b ? texto(b.contatos?.dono, 20).replace(/\D/g, '') : c.contatos.dono,
        equipe: 'contatos' in b ? texto(b.contatos?.equipe, 20).replace(/\D/g, '') : c.contatos.equipe,
      },
      linkAvaliacao: 'linkAvaliacao' in b ? texto(b.linkAvaliacao, 300) : c.linkAvaliacao,
      relacionamento: {
        diasAntesVencimento: inteiro(b.relacionamento?.diasAntesVencimento, 0, 30, c.relacionamento.diasAntesVencimento),
        diasAntesRevisao: inteiro(b.relacionamento?.diasAntesRevisao, 0, 90, c.relacionamento.diasAntesRevisao),
        diasAntesDocumento: inteiro(b.relacionamento?.diasAntesDocumento, 0, 120, c.relacionamento.diasAntesDocumento),
        diasSumido: inteiro(b.relacionamento?.diasSumido, 7, 365, c.relacionamento.diasSumido),
      },
    };
    if ('fuso' in b && !(b.fuso in FUSOS)) return erro(res, 400, 'Fuso horário desconhecido.');
    if (nova.linkAvaliacao && !/^https:\/\/[^\s]+$/.test(nova.linkAvaliacao)) return erro(res, 400, 'O link de avaliação precisa começar com https://');
    if (nova.rampa.abre >= nova.rampa.ultimaDescida) return erro(res, 400, 'A última descida precisa ser depois da abertura da rampa.');
    if (Array.isArray(b.itensAluguel)) {
      const itens = [];
      for (const it of b.itensAluguel.slice(0, 30)) {
        const id = texto(it?.id, 24).toLowerCase();
        const nome = texto(it?.nome, 60);
        if (!/^[a-z0-9-]+$/.test(id) || !nome) return erro(res, 400, 'Item de aluguel inválido: use um código com letras minúsculas, números e hífen, e um nome.');
        if (itens.some((x) => x.id === id)) return erro(res, 400, `Código de item repetido: ${id}.`);
        itens.push({ id, nome, unidades: inteiro(it.unidades, 1, 99, 1) });
      }
      nova.itensAluguel = itens;
    }
    store.config = nova;
    store.salvar('config');
    definirFuso(nova.fuso);
    avisar();
    const fora = agenda.foraDaGrade();
    res.json({
      ok: true,
      config: nova,
      aviso: fora ? `${fora} descida(s) já marcada(s) ficaram em horários que não existem na grade nova. Elas continuam no quadro; combine o novo horário com cada cliente.` : null,
    });
  });

  app.put('/api/painel/ficha', admin, (req, res) => {
    if (typeof req.body?.ficha !== 'string' || req.body.ficha.length > 40000) return erro(res, 400, 'Ficha inválida ou grande demais (limite de 40 mil caracteres).');
    store.ficha = req.body.ficha;
    store.salvar('ficha');
    res.json({ ok: true });
  });

  function camposDoCliente(b) {
    return {
      nome: texto(b.nome, 80),
      telefone: texto(b.telefone, 20).replace(/\D/g, ''),
      embarcacao: texto(b.embarcacao, 80),
      autorizados: texto(b.autorizados, 200),
      pendencia: b.pendencia === true,
      obs: texto(b.obs, 300),
      mensalidadeDia: Number.isInteger(b.mensalidadeDia) && b.mensalidadeDia >= 1 && b.mensalidadeDia <= 31 ? b.mensalidadeDia : null,
      revisaoEm: dataValida(b.revisaoEm) ? b.revisaoEm : '',
      documentoVence: dataValida(b.documentoVence) ? b.documentoVence : '',
      semLembretes: b.semLembretes === true,
    };
  }

  app.post('/api/painel/cliente', admin, (req, res) => {
    const campos = camposDoCliente(req.body || {});
    if (!campos.nome) return erro(res, 400, 'Informe o nome do cliente.');
    const c = { id: novoId('cli'), token: novoToken(), ...campos };
    store.clientes.push(c);
    store.salvar('clientes');
    res.json({ ok: true, cliente: { ...c, token: undefined, link: linkDoCliente(req, c) } });
  });

  app.put('/api/painel/cliente/:id', admin, (req, res) => {
    const c = store.clientes.find((x) => x.id === req.params.id);
    if (!c) return erro(res, 404, 'Cliente não encontrado.');
    const campos = camposDoCliente(req.body || {});
    if (!campos.nome) return erro(res, 400, 'Informe o nome do cliente.');
    Object.assign(c, campos);
    if (req.body?.novoLink === true) c.token = novoToken();
    store.salvar('clientes');
    avisar();
    res.json({ ok: true, cliente: { ...c, token: undefined, link: linkDoCliente(req, c) } });
  });

  function apagarConversa(c) {
    atendente.esquecer(c.id);
    for (const m of c.mensagens) if (m.arquivo) apagarFoto(m.arquivo);
    for (const r of store.registros) if (r.conversaId === c.id) r.conversaId = null;
    for (const ch of store.chamados) if (ch.conversaId === c.id) ch.conversaId = null;
    store.salvar('registros');
    store.salvar('chamados');
    store.conversas.delete(c.id);
    store.salvar(`conversa:${c.id}`);
  }

  app.delete('/api/painel/cliente/:id', admin, (req, res) => {
    const c = store.clientes.find((x) => x.id === req.params.id);
    if (!c) return erro(res, 404, 'Cliente não encontrado.');
    for (const conv of [...store.conversas.values()]) if (conv.clienteId === c.id) apagarConversa(conv);
    for (const r of store.registros) {
      if (r.clienteId === c.id) {
        r.clienteId = null;
        r.clienteNome = 'Cliente removido';
      }
    }
    store.clientes = store.clientes.filter((x) => x.id !== c.id);
    store.salvar('clientes');
    store.salvar('registros');
    avisar();
    res.json({ ok: true });
  });

  app.delete('/api/painel/conversa/:id', admin, (req, res) => {
    const c = store.conversas.get(req.params.id);
    if (!c) return erro(res, 404, 'Conversa não encontrada.');
    apagarConversa(c);
    avisar();
    res.json({ ok: true });
  });

  app.get('/api/painel/relatorio', admin, (req, res) => {
    const de = dataValida(req.query.de) ? req.query.de : null;
    const ate = dataValida(req.query.ate) ? req.query.ate : null;
    res.json(relatorio(store, { de, ate }));
  });

  app.get('/api/painel/exportar', admin, (req, res) => {
    res.set('Content-Disposition', `attachment; filename="marina-dados-${agora().data}.json"`);
    res.json({
      exportadoEm: agora(),
      config: store.config,
      ficha: store.ficha,
      clientes: store.clientes.map((c) => ({ ...c, token: undefined })),
      registros: store.registros,
      chamados: store.chamados,
      sugestoes: store.sugestoes,
      conversas: [...store.conversas.values()].map((c) => ({ id: c.id, clienteId: c.clienteId, estado: c.estado, criadaEm: c.criadaEm, mensagens: c.mensagens })),
    });
  });

  // =====================================================================
  // Páginas
  // =====================================================================

  const pagina = (arquivo) => (req, res) => res.set('Cache-Control', 'no-cache').sendFile(path.join(PUBLICO, arquivo));
  app.get('/', pagina('chat.html'));
  app.get('/c/:token', pagina('chat.html'));
  app.get('/painel', pagina('painel.html'));
  app.get('/saude', (req, res) => res.json({ ok: true }));
  app.use(express.static(PUBLICO, { index: false, maxAge: '10m' }));

  app.use((req, res) => (req.path.startsWith('/api/') ? erro(res, 404, 'Não encontrado.') : res.status(404).type('text').send('Página não encontrada.')));
  app.use((err, req, res, next) => {
    console.error('[servidor]', err);
    if (res.headersSent) return next(err);
    erro(res, 500, 'Erro interno. Tente de novo.');
  });

  return { app, store, agenda, atendente, equipe, senhas };
}
