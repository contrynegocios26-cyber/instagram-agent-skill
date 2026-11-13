// Teste de aceitação com o modelo de verdade: dez situações de cliente,
// cada uma com conferências objetivas sobre o que ficou registrado.
// Rode sempre antes de ligar numa marina e depois de mexer na skill, na
// ficha de exemplo ou no prompt.
//
//   ANTHROPIC_API_KEY=... node scripts/bancada-real.mjs
//   ANTHROPIC_API_KEY=... node scripts/bancada-real.mjs --so 2,4     (só algumas)
//
// Usa a marina fictícia de exemplo, em pastas temporárias. Gasta tokens de
// verdade: são cerca de 30 chamadas ao modelo. Sai com erro se alguma
// conferência falhar.

process.env.IA_ESPERA_MS = '0';

const { criarIA } = await import('../lib/ia.js');
const { rodarCenarios } = await import('./cenarios.mjs');

const i = process.argv.indexOf('--so');
const so = i === -1 ? null : process.argv[i + 1].split(',').map(Number);

const ia = criarIA();
console.log(`Bancada com o modelo ${ia.modelo}${ia.demonstracao ? ' (ROTEIRO, sem IA: serve só para conferir o próprio script)' : ''}\n`);

const r = await rodarCenarios({ ia, so });
console.log('--- resultado ---');
console.log(r.resumo.join('\n'));
console.log(`\n${r.resumo.length - r.falhas} de ${r.resumo.length} situações passaram · ${r.chamadas} chamadas ao modelo${r.semPreco ? '' : ` · custo estimado US$ ${r.usd.toFixed(3)}`}`);
if (r.falhas) {
  console.log('Leia a conversa de cada situação que falhou antes de concluir: uma conferência de texto pode falhar com uma resposta boa escrita de outro jeito.');
  process.exit(1);
}
