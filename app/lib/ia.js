// Chamada ao modelo. Uma única função, criar(), usada pelo atendente.
// Com IA_FAKE=1 responde um roteiro simples, sem rede e sem custo, para
// demonstração e testes.

import Anthropic from '@anthropic-ai/sdk';
import { FERRAMENTAS } from './prompt.js';
import { agora, somarDias, normalizarHora } from './tempo.js';

export const MODELO = process.env.IA_MODELO || 'claude-opus-5-5';
const ESFORCOS = ['low', 'medium', 'high', 'xhigh', 'max'];
const ESFORCO = ESFORCOS.includes(process.env.IA_ESFORCO) ? process.env.IA_ESFORCO : null;
const TTL_1H = (process.env.IA_CACHE_TTL || '1h') === '1h';

// Fallback do lado do servidor quando um classificador de segurança recusa
// um pedido: a API refaz a chamada no modelo que a Anthropic recomenda.
// Só existe nestes modelos; desligue com IA_FALLBACK=off.
const COM_FALLBACK = /^claude-(opus-5|sonnet-5-5|fable-5)/.test(MODELO) && process.env.IA_FALLBACK !== 'off';

// USD por milhão de tokens. Gravação em cache: 1,25x (5 min) ou 2x (1 h).
const PRECOS = {
  'claude-opus-5-5': { entrada: 4, saida: 20, leitura: 0.2 },
  'claude-sonnet-5-5': { entrada: 2, saida: 10, leitura: 0.1 },
  'claude-haiku-5-5': { entrada: 0.1, saida: 0.5, leitura: 0.01 },
};

/** Custo estimado em USD de uma resposta, ou null se o modelo não está na tabela. */
export function custoEstimado(modelo, uso) {
  const p = PRECOS[modelo];
  if (!p || !uso) return null;
  const gravacao1h = uso.cache_creation?.ephemeral_1h_input_tokens ?? 0;
  const gravacao5m = (uso.cache_creation_input_tokens ?? 0) - gravacao1h;
  return (
    ((uso.input_tokens ?? 0) * p.entrada +
      gravacao5m * p.entrada * 1.25 +
      gravacao1h * p.entrada * 2 +
      (uso.cache_read_input_tokens ?? 0) * p.leitura +
      (uso.output_tokens ?? 0) * p.saida) /
    1e6
  );
}

export class FalhaIA extends Error {
  /** @param {'config'|'requisicao'|'temporaria'|'recusa'|'corte'} tipo */
  constructor(tipo, mensagem, causa) {
    super(mensagem);
    this.tipo = tipo;
    this.cause = causa;
  }
}

function criarReal() {
  const client = new Anthropic({ timeout: 120_000, maxRetries: 2 });

  return async function criar({ sistema, messages }) {
    const req = {
      model: MODELO,
      max_tokens: 16000,
      // Prefixo estável, igual em todas as conversas da marina: fica em cache.
      system: [{ type: 'text', text: sistema, cache_control: TTL_1H ? { type: 'ephemeral', ttl: '1h' } : { type: 'ephemeral' } }],
      tools: FERRAMENTAS,
      messages,
      // Cache automático para o final da conversa, que cresce a cada turno.
      cache_control: { type: 'ephemeral' },
    };
    if (ESFORCO) req.output_config = { effort: ESFORCO };

    try {
      if (COM_FALLBACK) {
        return await client.beta.messages.create({ ...req, betas: ['server-side-fallback-2026-07-01'], fallbacks: 'default' });
      }
      return await client.messages.create(req);
    } catch (e) {
      if (e instanceof Anthropic.AuthenticationError || e instanceof Anthropic.PermissionDeniedError) {
        throw new FalhaIA('config', 'Chave da API da Anthropic inválida ou sem permissão.', e);
      }
      if (e instanceof Anthropic.NotFoundError) {
        throw new FalhaIA('config', `Modelo "${MODELO}" não encontrado para esta chave.`, e);
      }
      if (e instanceof Anthropic.BadRequestError) {
        throw new FalhaIA('requisicao', `A API recusou o pedido: ${e.message}`, e);
      }
      if (e instanceof Anthropic.RateLimitError) {
        throw new FalhaIA('temporaria', 'Limite de uso da API atingido no momento.', e);
      }
      if (e instanceof Anthropic.APIConnectionError) {
        throw new FalhaIA('temporaria', 'Sem conexão com a API da Anthropic.', e);
      }
      if (e instanceof Anthropic.APIError) {
        throw new FalhaIA('temporaria', `Erro ${e.status ?? ''} da API da Anthropic.`, e);
      }
      throw e;
    }
  };
}

// ---------- modo demonstração ----------

let seq = 0;
const usoFake = { input_tokens: 120, output_tokens: 60, cache_read_input_tokens: 9000, cache_creation_input_tokens: 0 };
const msg = (content, stop_reason) => ({ id: `msg_fake_${++seq}`, model: 'fake', role: 'assistant', content, stop_reason, usage: usoFake });
const texto = (t) => msg([{ type: 'text', text: t }], 'end_turn');
const usar = (name, input) => msg([{ type: 'tool_use', id: `toolu_fake_${++seq}`, name, input }], 'tool_use');
const vazio = { data: null, hora: null, item_aluguel: null, registro_id: null, detalhes: '', status: 'confirmado', nome_cliente: null, embarcacao: null };

function criarFake() {
  return async function criar({ messages }) {
    const ultima = messages[messages.length - 1];

    if (ultima.role === 'user' && Array.isArray(ultima.content) && ultima.content.some((b) => b.type === 'tool_result')) {
      const res = ultima.content.filter((b) => b.type === 'tool_result').map((b) => JSON.parse(b.content));
      const ruim = res.find((r) => !r.ok);
      if (ruim) return texto(`Não consegui registrar. ${ruim.erro}`);
      const partes = res.map((r) => (r.chamado_id ? 'já chamei a equipe' : `${r.resumo}${r.avisos?.length ? ' (a equipe confirma)' : ''}`));
      return texto(`Certo: ${partes.join('; ')}.`);
    }

    const doCliente = [...messages].reverse().find((m) => m.role === 'user' && Array.isArray(m.content) && m.content.some((b) => b.type === 'text'));
    const fala = (doCliente?.content || []).map((b) => b.text || '').join(' ').toLowerCase();
    const contexto = [...messages].reverse().find((m) => m.role === 'system')?.content || '';

    if (fala.includes('erro_ia')) throw new FalhaIA('temporaria', 'Falha simulada.');
    if (fala.includes('recusa_ia')) return msg([], 'refusal');

    const hoje = agora().data;
    const data = fala.includes('amanhã') || fala.includes('amanha') ? somarDias(hoje, 1) : hoje;
    const horaBruta = [...fala.matchAll(/\b(\d{1,2}(?:h\d{0,2}|:\d{2}))/g)].at(-1)?.[1];
    const hora = horaBruta ? normalizarHora(horaBruta) : null;
    const idAberto = contexto.match(/id (reg_[0-9a-f]+)/)?.[1] || null;

    if (/cancel/.test(fala) && idAberto) return usar('registrar', { ...vazio, tipo: 'cancelamento', registro_id: idAberto });
    if (/desc(e|er|ida)/.test(fala) && hora) return usar('registrar', { ...vazio, tipo: 'descida', data, hora, detalhes: fala.includes('gelo') ? 'gelo' : '' });
    if (/(voltando|subir|sobe)/.test(fala) && hora) return usar('registrar', { ...vazio, tipo: 'subida', data: hoje, hora });
    if (/(reservar|quero o jet|fechar)/.test(fala)) return usar('registrar', { ...vazio, tipo: 'reserva', data, item_aluguel: 'jet', status: 'pre-reserva', nome_cliente: 'Visitante' });
    if (/(desconto|reclama|gerente|equipe|humano)/.test(fala)) {
      return usar('encaminhar', { para: 'Sandra (gerência)', urgencia: 'alta', resumo: `Cliente pediu: ${fala.slice(0, 200)}` });
    }
    if (contexto.includes('detectou emergência')) {
      return usar('encaminhar', { para: 'Zé (plantão)', urgencia: 'emergencia', resumo: `Emergência relatada: ${fala.slice(0, 200)}` });
    }
    return texto('Olá! Sou o assistente virtual da marina, em modo de demonstração.\n\nPosso agendar a descida do seu barco ou passar valores de aluguel.');
  };
}

export function criarIA() {
  if (process.env.IA_FAKE === '1') return { criar: criarFake(), modelo: 'fake', demonstracao: true };
  return { criar: criarReal(), modelo: MODELO, demonstracao: false };
}
