// Ponte para testar o atendente com um modelo que não está atrás da API:
// outra sessão do Claude, ou uma pessoa, faz o papel do modelo respondendo
// em arquivos. O programa manda exatamente o que mandaria à API (prompt de
// sistema, ferramentas e mensagens) e executa as ferramentas de verdade.
//
//   node scripts/ponte.mjs --dir <pasta> [--so 1,2,3]
//
// A cada execução o programa repete as conversas desde o começo usando as
// respostas já gravadas (resposta-1.json, resposta-2.json, ...). Quando
// falta uma resposta, grava pedido-N.json e para. Quando não falta mais
// nenhuma, grava RESULTADO.txt.
//
// Formato de resposta-N.json:
//   {"content": [{"type": "tool_use", "name": "registrar", "input": {...}}]}
//   {"content": [{"type": "text", "text": "mensagem ao cliente"}]}

import fs from 'node:fs';
import path from 'node:path';

process.env.IA_ESPERA_MS = '0';

const { FERRAMENTAS } = await import('../lib/prompt.js');
const { rodarCenarios } = await import('./cenarios.mjs');

const arg = (nome) => {
  const i = process.argv.indexOf(nome);
  return i === -1 ? null : process.argv[i + 1];
};
const dir = arg('--dir');
if (!dir) {
  console.error('Informe a pasta de trabalho: --dir <pasta>');
  process.exit(2);
}
const so = arg('--so')?.split(',').map(Number) ?? null;
fs.mkdirSync(dir, { recursive: true });

let n = 0;

function conferir(resposta, numero) {
  if (!resposta || !Array.isArray(resposta.content) || !resposta.content.length) throw new Error('falta "content" com ao menos um bloco');
  let k = 0;
  for (const b of resposta.content) {
    if (b.type === 'text') {
      if (typeof b.text !== 'string' || !b.text.trim()) throw new Error('bloco de texto vazio');
    } else if (b.type === 'tool_use') {
      const f = FERRAMENTAS.find((x) => x.name === b.name);
      if (!f) throw new Error(`ferramenta desconhecida: ${b.name}`);
      if (!b.input || typeof b.input !== 'object') throw new Error(`"input" ausente em ${b.name}`);
      // As ferramentas são estritas na API: todo campo é obrigatório e não há campo extra.
      const faltam = f.input_schema.required.filter((c) => !(c in b.input));
      const sobram = Object.keys(b.input).filter((c) => !(c in f.input_schema.properties));
      if (faltam.length) throw new Error(`${b.name}: faltam os campos ${faltam.join(', ')} (use null quando não se aplica)`);
      if (sobram.length) throw new Error(`${b.name}: campos que não existem: ${sobram.join(', ')}`);
      for (const [campo, def] of Object.entries(f.input_schema.properties)) {
        if (def.enum && !def.enum.includes(b.input[campo])) throw new Error(`${b.name}.${campo}: valor fora da lista (${def.enum.join(', ')})`);
      }
      b.id = `toolu_ponte_${numero}_${++k}`;
    } else {
      throw new Error(`tipo de bloco não aceito: ${b.type}`);
    }
  }
  const usa = resposta.content.some((b) => b.type === 'tool_use');
  return { id: `msg_ponte_${numero}`, model: 'ponte', role: 'assistant', content: resposta.content, stop_reason: usa ? 'tool_use' : 'end_turn', usage: {} };
}

const ia = {
  modelo: 'ponte',
  demonstracao: false,
  redigir: null,
  formato: () => 'ponte',
  criar: async ({ sistema, messages }) => {
    n++;
    if (n === 1) {
      fs.writeFileSync(path.join(dir, 'sistema.md'), sistema);
      fs.writeFileSync(path.join(dir, 'ferramentas.json'), JSON.stringify(FERRAMENTAS, null, 2));
    }
    const arq = path.join(dir, `resposta-${n}.json`);
    // Sem a resposta, ou com resposta inválida, o programa para aqui mesmo:
    // nada do que viria depois faz sentido sem ela.
    if (!fs.existsSync(arq)) {
      fs.writeFileSync(path.join(dir, `pedido-${n}.json`), JSON.stringify({ numero: n, messages }, null, 2));
      console.log(`AGUARDANDO resposta-${n}.json (leia pedido-${n}.json)`);
      process.exit(0);
    }
    try {
      return conferir(JSON.parse(fs.readFileSync(arq, 'utf8')), n);
    } catch (e) {
      console.log(`ERRO em resposta-${n}.json: ${e.message}. Corrija o arquivo e rode de novo.`);
      process.exit(2);
    }
  },
};

const linhas = [];
const r = await rodarCenarios({ ia, so, diga: (l) => linhas.push(l) });
linhas.push('--- resultado ---', ...r.resumo, '', `${r.resumo.length - r.falhas} de ${r.resumo.length} situações passaram · ${n} respostas do modelo`);
fs.writeFileSync(path.join(dir, 'RESULTADO.txt'), linhas.join('\n'));
console.log(`FIM. ${r.resumo.length - r.falhas} de ${r.resumo.length} situações passaram. Veja RESULTADO.txt`);
