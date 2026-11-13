// Confere se o cache do prompt está funcionando e quanto custa uma resposta.
// Manda o mesmo pedido duas vezes: na segunda, quase toda a entrada tem de
// vir do cache. Sai com erro se não vier.
//
//   node scripts/sonda-custo.mjs
//
// Precisa de ANTHROPIC_API_KEY e gasta tokens de verdade (poucos centavos).
// Rode de novo sempre que mexer em lib/prompt.js ou lib/ia.js.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const { criarStore } = await import('../lib/store.js');
const { semear } = await import('../lib/semente.js');
const { criarAgenda } = await import('../lib/agenda.js');
const { criarIA, custoEstimado } = await import('../lib/ia.js');
const { promptDeSistema, contextoDoTurno } = await import('../lib/prompt.js');

const store = criarStore(fs.mkdtempSync(path.join(os.tmpdir(), 'marina-sonda-')));
semear(store, 'exemplo');
const agenda = criarAgenda(store);
const ia = criarIA();
if (ia.demonstracao) {
  console.error('IA_FAKE=1: a sonda precisa do modelo de verdade.');
  process.exit(2);
}

const sistema = promptDeSistema(store);
const conversa = { id: 'con_sonda', mensagens: [] };
const pedido = () => ({
  sistema,
  messages: [
    { role: 'user', content: [{ type: 'text', text: 'oi, boa tarde' }] },
    { role: 'system', content: contextoDoTurno({ store, agenda, conversa, cliente: null, turnoId: null, fotos: 0 }) },
  ],
});

let segunda = null;
for (const n of [1, 2]) {
  let r;
  try {
    r = await ia.criar(pedido());
  } catch (e) {
    console.error(`\nFALHA no pedido ${n}: ${e.message}`);
    console.error('Confira a chave ANTHROPIC_API_KEY no arquivo .env e se a conta da Anthropic tem crédito.');
    process.exit(1);
  }
  const u = r.usage;
  const usd = custoEstimado(r.model, u);
  console.log(
    `pedido ${n}: entrada ${u.input_tokens} · cache gravado ${u.cache_creation_input_tokens ?? 0} · cache lido ${u.cache_read_input_tokens ?? 0} · saída ${u.output_tokens}${usd === null ? '' : ` · US$ ${usd.toFixed(4)}`}`,
  );
  if (n === 2) segunda = u;
}
store.descarregar();
if (!segunda.cache_read_input_tokens) {
  console.error('\nFALHA: o segundo pedido não leu nada do cache. Algo no prompt muda entre um pedido e outro.');
  process.exit(1);
}
console.log('\nCache funcionando: o segundo pedido leu o prompt do cache.');

// Manutenção do cache: o pedido sem resposta (max_tokens 0) tem de ler o
// mesmo cache dos pedidos de verdade. É ele que o servidor manda de hora em
// hora para o prompt não precisar ser gravado de novo.
if (!ia.aquecer) {
  console.log('Manutenção do cache: desligada (IA_MANTER_CACHE=off ou IA_CACHE_TTL diferente de 1h).');
} else {
  try {
    const r = await ia.aquecer({ sistema });
    const u = r.usage;
    const usd = custoEstimado(r.model, u);
    console.log(
      `manutenção: entrada ${u.input_tokens} · cache gravado ${u.cache_creation_input_tokens ?? 0} · cache lido ${u.cache_read_input_tokens ?? 0} · saída ${u.output_tokens}${usd === null ? '' : ` · US$ ${usd.toFixed(4)}`}`,
    );
    if (u.cache_read_input_tokens > 0 && !u.output_tokens) {
      console.log('Manutenção do cache funcionando: releu o prompt sem gerar resposta.');
    } else {
      console.log('ATENÇÃO: a manutenção do cache não releu o prompt. O servidor percebe isso e desliga a manutenção sozinho; o atendimento não é afetado. Avise quem cuida do aplicativo.');
    }
  } catch (e) {
    console.log(`ATENÇÃO: a manutenção do cache foi recusada pela API (${e.message}). O servidor desliga a manutenção sozinho; o atendimento não é afetado.`);
  }
}
