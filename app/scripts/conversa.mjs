// Conversa de teste direto no motor do atendente, com o modelo de verdade.
// Serve para experimentar frases de cliente antes de ligar numa marina.
//
//   node scripts/conversa.mjs --cliente Fernanda --agora 2026-12-18T19:10 "desce a aquarela amanhã 10h" "com 2 sacos de gelo"
//   node scripts/conversa.mjs --visitante "quanto é o jet no sábado?"
//
// Usa a marina fictícia de exemplo numa pasta temporária. Precisa de
// ANTHROPIC_API_KEY e gasta tokens de verdade (centavos por conversa).

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

process.env.IA_ESPERA_MS = '0';
const args = process.argv.slice(2);
const opcao = (nome) => {
  const i = args.indexOf(nome);
  return i === -1 ? null : args.splice(i, 2)[1];
};
const nomeCliente = opcao('--cliente');
const agoraFixo = opcao('--agora');
const pasta = opcao('--dados');
const visitante = args.includes('--visitante') && args.splice(args.indexOf('--visitante'), 1);
const falas = args;
if (!falas.length) {
  console.error('Passe ao menos uma mensagem de cliente entre aspas.');
  process.exit(2);
}

const { criarStore } = await import('../lib/store.js');
const { semear } = await import('../lib/semente.js');
const { criarAgenda } = await import('../lib/agenda.js');
const { criarIA } = await import('../lib/ia.js');
const { criarAtendente } = await import('../lib/atendente.js');
const { fixarRelogio } = await import('../lib/tempo.js');

if (agoraFixo) fixarRelogio(agoraFixo);
const store = criarStore(pasta || fs.mkdtempSync(path.join(os.tmpdir(), 'marina-conversa-')));
semear(store, 'exemplo');
store.config.modo = 'auto';
const agenda = criarAgenda(store);
const ia = criarIA();
const atendente = criarAtendente({ store, agenda, ia, avisar: () => {} });

const cliente = nomeCliente ? store.clientes.find((c) => c.nome.toLowerCase().startsWith(nomeCliente.toLowerCase())) : null;
if (nomeCliente && !cliente) {
  console.error(`Cliente "${nomeCliente}" não existe na marina de exemplo. Opções: ${store.clientes.map((c) => c.nome.split(' ')[0]).join(', ')}.`);
  process.exit(2);
}
const conversa = cliente && !visitante ? atendente.conversaDoCliente(cliente) : atendente.criarConversa({});
console.log(`Modelo: ${ia.modelo} · quem fala: ${cliente ? cliente.nome : 'visitante (link público)'}${agoraFixo ? ` · agora: ${agoraFixo}` : ''}\n`);

let vistas = 0;
let apiVistas = 0;
for (const fala of falas) {
  atendente.receberDoCliente(conversa, { texto: fala });
  await atendente.ocioso();
  for (const m of conversa.mensagens.slice(vistas)) console.log(`[${m.de}] ${m.texto}`);
  vistas = conversa.mensagens.length;
  const api = conversa.thread?.apiMessages || [];
  for (const m of api.slice(apiVistas)) {
    if (!Array.isArray(m.content)) continue;
    for (const b of m.content) {
      if (b.type === 'tool_use') console.log(`    > ${b.name} ${JSON.stringify(b.input)}`);
      if (b.type === 'tool_result') console.log(`    < ${b.content}`);
    }
  }
  apiVistas = api.length;
  console.log('');
}

const uso = store.lerUso();
const soma = (k) => uso.reduce((t, u) => t + (u[k] || 0), 0);
const usd = uso.some((u) => u.usd === null) ? null : uso.reduce((t, u) => t + u.usd, 0);
console.log('--- registros ---');
for (const r of store.registros) console.log(`${r.id} ${agenda.descrever(r)} · ${r.clienteNome}`);
console.log('--- chamados ---');
for (const c of store.chamados) console.log(`[${c.urgencia}] para ${c.para}: ${c.resumo}`);
console.log('--- uso ---');
console.log(
  `${uso.length} chamadas · entrada ${soma('entrada')} · cache lido ${soma('cacheLeitura')} · cache gravado ${soma('cacheGravacao')} · saída ${soma('saida')}${usd === null ? '' : ` · custo estimado US$ ${usd.toFixed(4)}`}`,
);
store.descarregar();
