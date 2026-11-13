// Motor do atendimento: recebe a mensagem do cliente, conversa com o modelo,
// executa as ferramentas e entrega a resposta, direto ou via aprovação
// (modo sombra). Também guarda o que acontece quando algo falha: nenhuma
// mensagem de cliente fica sem um humano avisado.

import { novoId } from './store.js';
import { agora, carimbo, normalizarHora } from './tempo.js';
import { promptDeSistema, versaoDoPrompt, contextoDoTurno } from './prompt.js';
import { FalhaIA, custoEstimado } from './ia.js';

const MAX_VOLTAS = 6;
const HORAS_DE_SESSAO = 12;
const MAX_MENSAGENS_API = 80;
const ESPERA_MS = Number(process.env.IA_ESPERA_MS ?? 1500);
const LIMITE_DIARIO = Number(process.env.IA_LIMITE_DIARIO ?? 1500);
const MINUTOS_SEM_RESPOSTA = Number(process.env.AVISO_SEM_RESPOSTA_MIN ?? 10);

// Só termos que quase nunca aparecem fora de uma emergência real. O resto
// fica por conta do atendente, que segue a regra de emergência da skill.
const RE_EMERGENCIA =
  /(\b[àa] deriva\b|afundando|afundou|naufrag|homem ao mar|caiu n[ao] (água|agua|rio)|afogando|afogamento|pegando fogo|inc[eê]ndio|socorro|virou (o|a) (barco|lancha|jet)|capotou|motor parou no (meio do )?rio|é (uma )?emerg[eê]ncia)/i;

export function criarAtendente({ store, agenda, ia, avisar }) {
  const filas = new Map(); // conversaId -> { timer, rodando, denovo }
  const usoPorDia = new Map();
  let saude = { ok: true, motivo: null, em: null };
  let cachePrompt = null;
  const agoraMs = () => new Date(carimbo()).getTime();

  for (const u of store.lerUso()) usoPorDia.set(u.dia, (usoPorDia.get(u.dia) || 0) + 1);

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
    const c = { id: novoId('con'), clienteId, criadaEm: ts, atualizadaEm: ts, estado: 'ia', mensagens: [], thread: null, nota: null, naoLidas: 0 };
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

  /** Separa o que o modelo ainda não viu em: mensagens do cliente a responder
   *  e o resto (o que a equipe e o sistema disseram), que vira recapitulação. */
  function pendencias(conversa) {
    const naoVistas = conversa.mensagens.filter((m) => !m.visto);
    let corte = -1;
    naoVistas.forEach((m, i) => {
      if (m.de === 'equipe' || m.de === 'assistente') corte = i;
    });
    const aResponder = naoVistas.filter((m, i) => i > corte && m.de === 'cliente');
    const recap = naoVistas.filter((m) => !aResponder.includes(m));
    return { naoVistas, aResponder, recap };
  }

  // ---------- chamados ----------

  function abrirChamado({ conversa, para, urgencia, resumo, origem = 'assistente', turnoId = null }) {
    const cli = conversa ? clienteDe(conversa) : null;
    const ch = {
      id: novoId('cha'),
      para: String(para || 'Equipe').slice(0, 120),
      urgencia: ['normal', 'alta', 'emergencia'].includes(urgencia) ? urgencia : 'normal',
      resumo: String(resumo || '').slice(0, 1500),
      conversaId: conversa ? conversa.id : null,
      clienteNome: cli ? cli.nome : 'Visitante',
      origem,
      status: 'aberto',
      criadoEm: carimbo(),
    };
    if (turnoId && ch.urgencia !== 'emergencia') ch.rascunho = turnoId;
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

  // ---------- entrada do cliente ----------

  function receberDoCliente(conversa, { texto, foto }) {
    const emergencia = !!texto && RE_EMERGENCIA.test(texto);
    const m = mensagem(conversa, foto ? { de: 'cliente', tipo: 'foto', arquivo: foto, texto: '' } : { de: 'cliente', texto });
    if (emergencia) m.emergencia = true;

    // Uma mensagem nova invalida a resposta que esperava aprovação.
    const pend = store.rascunhos.find((r) => r.conversaId === conversa.id);
    if (pend) removerRascunho(pend, true);

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

  /** Primeira mensagem do cliente que ainda não teve resposta de ninguém. */
  function semResposta(conversa) {
    let primeira = null;
    let avisado = false;
    for (let i = conversa.mensagens.length - 1; i >= 0; i--) {
      const m = conversa.mensagens[i];
      if (m.de === 'assistente' || m.de === 'equipe') break;
      if (m.de === 'cliente') primeira = m;
      if (m.de === 'sistema' && m.avisoDeEspera) avisado = true;
    }
    return { primeira, avisado: !!primeira && avisado };
  }

  /** O cliente deve ver "digitando"? Não depois de ouvir que a equipe vai responder. */
  function ocupado(id) {
    const f = filas.get(id);
    if (f && (f.timer || f.rodando)) return true;
    if (!store.rascunhos.some((r) => r.conversaId === id)) return false;
    const conversa = store.conversas.get(id);
    return !!conversa && !semResposta(conversa).avisado;
  }

  /**
   * Roda de minuto em minuto. Cliente esperando há tempo demais, com resposta
   * parada na aprovação ou com a equipe na conversa, recebe um aviso honesto
   * e a equipe recebe um chamado. Também apaga conversas que nunca começaram.
   */
  function vigiar() {
    let avisos = 0;
    const agoraEm = agoraMs();
    for (const c of [...store.conversas.values()]) {
      if (!c.mensagens.length) {
        if (!c.clienteId && agoraEm - new Date(c.criadaEm).getTime() > 86_400_000) {
          store.conversas.delete(c.id);
          store.salvar(`conversa:${c.id}`);
        }
        continue;
      }
      const { primeira, avisado } = semResposta(c);
      if (!primeira || avisado) continue;
      if (agoraEm - new Date(primeira.em).getTime() < MINUTOS_SEM_RESPOSTA * 60_000) continue;
      if (filas.get(c.id)?.rodando) continue;
      const temRascunho = store.rascunhos.some((r) => r.conversaId === c.id);
      if (!store.chamados.some((ch) => ch.conversaId === c.id && ch.status === 'aberto' && ch.origem === 'sistema' && !ch.rascunho)) {
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

  async function ocioso() {
    while (filas.size) await new Promise((r) => setTimeout(r, 15));
  }

  // ---------- turno ----------

  function limiteAtingido() {
    return (usoPorDia.get(agora().data) || 0) >= LIMITE_DIARIO;
  }

  function semAtendente(conversa, motivo) {
    const jaAberto = store.chamados.some((c) => c.conversaId === conversa.id && c.status === 'aberto' && c.origem === 'sistema' && !c.rascunho);
    if (!jaAberto) {
      abrirChamado({ conversa, para: 'Equipe', urgencia: 'alta', resumo: `${motivo} Cliente aguardando resposta de uma pessoa.`, origem: 'sistema' });
    }
    const ultimoAviso = [...conversa.mensagens].reverse().find((m) => m.de === 'sistema' && m.avisoDesligado);
    const faz2h = !ultimoAviso || agoraMs() - new Date(ultimoAviso.em).getTime() > 2 * 3600 * 1000;
    if (faz2h) {
      mensagem(conversa, {
        de: 'sistema',
        avisoDesligado: true,
        avisoDeEspera: true,
        texto: 'Recebemos sua mensagem. O atendimento automático está desligado agora; a equipe da marina responde por aqui no horário de atendimento.',
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
      acoes.push({ tipo: 'chamado', id: ch.id, resumo: `chamado para ${ch.para} (${ch.urgencia}): ${ch.resumo}` });
      return { ok: true, chamado_id: ch.id, observacao: `Chamado aberto para ${ch.para}. A equipe vê no painel.` };
    }
    return { ok: false, erro: `Ferramenta desconhecida: ${bloco.name}.` };
  }

  function registrarUso(conversa, resp) {
    const dia = agora().data;
    usoPorDia.set(dia, (usoPorDia.get(dia) || 0) + 1);
    const u = resp.usage || {};
    store.registrarUso({
      dia,
      em: carimbo(),
      conversaId: conversa.id,
      modelo: resp.model || ia.modelo,
      entrada: u.input_tokens ?? 0,
      saida: u.output_tokens ?? 0,
      cacheLeitura: u.cache_read_input_tokens ?? 0,
      cacheGravacao: u.cache_creation_input_tokens ?? 0,
      usd: custoEstimado(resp.model || ia.modelo, u),
    });
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
    if (store.config.modo === 'desligado') return semAtendente(conversa, 'Atendente virtual desligado.');
    if (limiteAtingido()) return semAtendente(conversa, 'Limite diário de respostas automáticas atingido.');

    const cliente = clienteDe(conversa);
    const { sistema, versao } = prompt();
    const turnoId = novoId('tur');
    const emergencia = aResponder.some((m) => m.emergencia);

    // O histórico da API vale enquanto o prompt, as ferramentas e o modelo
    // forem os mesmos, a conversa estiver recente e não tiver crescido demais.
    let t = conversa.thread;
    const velho = t && agoraMs() - new Date(t.ultimaEm).getTime() > HORAS_DE_SESSAO * 3600 * 1000;
    const recomeca = !t || t.versao !== versao || velho || t.apiMessages.length > MAX_MENSAGENS_API;
    const mensagensApi = recomeca ? [] : structuredClone(t.apiMessages);
    const historicoAnterior = recomeca ? conversa.mensagens.filter((m) => m.visto).slice(-8) : [];

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
        nota: conversa.nota,
      }),
    });

    const ctx = { cliente, conversa, conversaId: conversa.id, turnoId, origem: 'assistente', por: 'assistente' };
    const acoes = [];
    let final = null;

    try {
      for (let volta = 0; volta < MAX_VOLTAS && final === null; volta++) {
        const resp = await ia.criar({ sistema, messages: mensagensApi });
        registrarUso(conversa, resp);
        if (resp.stop_reason === 'refusal') throw new FalhaIA('recusa', 'O modelo recusou responder.');
        if (resp.stop_reason === 'max_tokens') throw new FalhaIA('corte', 'A resposta foi cortada por tamanho.');
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
        final = limparTexto(resp.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n\n'));
        if (!final) throw new FalhaIA('corte', 'O modelo não escreveu resposta ao cliente.');
      }
      if (final === null) throw new FalhaIA('corte', 'O atendente não concluiu em tempo.');
      saude = { ok: true, motivo: null, em: carimbo() };
    } catch (e) {
      agenda.descartarTurno(turnoId);
      const falha = e instanceof FalhaIA ? e : new FalhaIA('temporaria', 'Erro interno ao gerar a resposta.', e);
      if (!(e instanceof FalhaIA)) console.error('[atendente] erro interno:', e);
      else console.error(`[atendente] falha (${falha.tipo}): ${falha.message}`, falha.cause?.message || '');
      if (falha.tipo === 'config' || falha.tipo === 'requisicao') saude = { ok: false, motivo: falha.message, em: carimbo() };
      // Um 400 pode vir de histórico que a API não aceita mais: recomeça da próxima vez.
      if (falha.tipo === 'requisicao') conversa.thread = null;
      conversa.estado = 'humano';
      abrirChamado({
        conversa,
        para: 'Equipe',
        urgencia: 'alta',
        resumo: `O atendente virtual não conseguiu responder (${falha.message}). Última mensagem do cliente: "${(aResponder.at(-1).texto || '(foto)').slice(0, 300)}"`,
        origem: 'sistema',
      });
      mensagem(conversa, { de: 'sistema', avisoDeEspera: true, texto: 'Não consegui concluir seu atendimento por aqui. Já chamei a equipe da marina, que continua por este chat.' });
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
    for (const p of partes) mensagem(conversa, { de: 'assistente', texto: p, visto: true, ...(por ? { aprovadoPor: por, editado } : {}) });
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
    conversa.estado = 'humano';
    if (typeof resposta === 'string' && resposta.trim()) mensagem(conversa, { de: 'equipe', autor: por, texto: resposta.trim().slice(0, 3000) });
    store.salvar(`conversa:${conversa.id}`);
    avisar(conversa.id);
    return { ok: true };
  }

  // ---------- ações da equipe ----------

  function responderComoEquipe(conversaId, texto, autor) {
    const conversa = store.conversas.get(conversaId);
    if (!conversa) return { ok: false, erro: 'Conversa não encontrada.' };
    const pend = store.rascunhos.find((r) => r.conversaId === conversaId);
    if (pend) removerRascunho(pend, true);
    const f = filas.get(conversaId);
    if (f?.timer) {
      clearTimeout(f.timer);
      f.timer = null;
      if (!f.rodando) filas.delete(conversaId);
    }
    conversa.estado = 'humano';
    conversa.naoLidas = 0;
    mensagem(conversa, { de: 'equipe', autor, texto: String(texto).trim().slice(0, 3000) });
    return { ok: true };
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
    conversa.estado = estado;
    store.salvar(`conversa:${conversaId}`);
    avisar(conversaId);
    if (estado === 'ia' && pendencias(conversa).aResponder.length) agendar(conversaId, 100);
    return { ok: true };
  }

  function marcarLida(conversaId) {
    const conversa = store.conversas.get(conversaId);
    if (conversa && conversa.naoLidas) {
      conversa.naoLidas = 0;
      store.salvar(`conversa:${conversaId}`);
    }
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
    mudarEstado,
    marcarLida,
    abrirChamado,
    resolverChamado,
    retomar,
    saude: () => saude,
    usoHoje: () => usoPorDia.get(agora().data) || 0,
    limiteDiario: LIMITE_DIARIO,
  };
}
