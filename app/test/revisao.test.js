// Um teste para cada defeito apontado na revisão de código de 13/11/2026.
// O número no nome é o do achado no relatório do revisor.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import Anthropic from '@anthropic-ai/sdk';

process.env.IA_FAKE = '1';
process.env.IA_ESPERA_MS = '0';
process.env.ESPERA_LONGA_MS = '200';
process.env.PAINEL_SENHA = 'senha-equipe';
process.env.ADMIN_SENHA = 'senha-admin';

const { criarStore } = await import('../lib/store.js');
const { semear } = await import('../lib/semente.js');
const { criarAgenda } = await import('../lib/agenda.js');
const { criarIA, criarReal } = await import('../lib/ia.js');
const { criarAtendente, ehEmergencia } = await import('../lib/atendente.js');
const { criarEquipe } = await import('../lib/equipe.js');
const { relatorio } = await import('../lib/relatorio.js');
const { criarApp } = await import('../lib/app.js');
const { fixarRelogio } = await import('../lib/tempo.js');

function motor({ modo = 'auto', ia = criarIA(), agora = '2026-12-18T19:10' } = {}) {
  fixarRelogio(agora);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'marina-rev-'));
  const store = criarStore(dir);
  semear(store, 'exemplo');
  store.config.modo = modo;
  const agenda = criarAgenda(store);
  const atendente = criarAtendente({ store, agenda, ia, avisar: () => {} });
  const cliente = (nome) => store.clientes.find((c) => c.nome.startsWith(nome));
  const conversa = (nome) => (nome ? atendente.conversaDoCliente(cliente(nome)) : atendente.criarConversa({}));
  const falas = (c, de) => c.mensagens.filter((m) => m.de === de).map((m) => m.texto);
  return { store, agenda, atendente, conversa, cliente, falas, dir };
}

/** Modelo de roteiro em que a primeira chamada fica presa até soltar(). */
function iaComPortao() {
  const base = criarIA();
  let soltar;
  const portao = new Promise((r) => (soltar = r));
  let chamadas = 0;
  let avisarChegada;
  const chegou = new Promise((r) => (avisarChegada = r));
  return {
    ...base,
    criar: async (p) => {
      chamadas++;
      if (chamadas === 1) {
        avisarChegada();
        await portao;
      }
      return base.criar(p);
    },
    soltar: () => soltar(),
    chegou,
    chamadas: () => chamadas,
  };
}

async function servidor() {
  fixarRelogio(null);
  const ctx = criarApp({ dir: fs.mkdtempSync(path.join(os.tmpdir(), 'marina-rev-http-')), semente: 'exemplo' });
  const srv = await new Promise((r) => {
    const s = ctx.app.listen(0, () => r(s));
  });
  const base = `http://localhost:${srv.address().port}`;
  const pedir = async (metodo, caminho, { corpo, cookie, chave, painel = true } = {}) => {
    const r = await fetch(base + caminho, {
      method: metodo,
      headers: {
        ...(corpo !== undefined ? { 'Content-Type': 'application/json' } : {}),
        ...(cookie ? { Cookie: cookie } : {}),
        ...(cookie && painel ? { 'X-Painel': '1' } : {}),
        ...(chave ? { 'X-Chat': chave } : {}),
      },
      body: corpo !== undefined ? JSON.stringify(corpo) : undefined,
    });
    return { status: r.status, dados: (r.headers.get('content-type') || '').includes('json') ? await r.json() : null };
  };
  const entrar = async (senha, nome = 'Teste') => (await fetch(`${base}/api/painel/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ senha, nome }) })).headers.get('set-cookie')?.split(';')[0];
  const sessao = async (corpo = {}) => (await pedir('POST', '/api/chat/sessao', { corpo })).dados;
  return { ...ctx, base, pedir, entrar, sessao, fechar: () => srv.close() };
}

test('achado 1: a chave do chat não vale como login do painel, nem o contrário', async (t) => {
  const s = await servidor();
  t.after(s.fechar);
  const visitante = await s.sessao();
  const falso = `painel=${encodeURIComponent(visitante.chave)}`;
  assert.equal((await s.pedir('GET', '/api/painel/estado', { cookie: falso })).status, 401);
  assert.equal((await s.pedir('POST', '/api/painel/modo', { cookie: falso, corpo: { modo: 'desligado' } })).status, 401);
  assert.equal((await s.pedir('GET', '/api/painel/eu', { cookie: falso })).status, 401);
  assert.equal(s.store.config.modo, 'sombra', 'o modo não mudou');
  const equipe = await s.entrar('senha-equipe');
  const comoChat = decodeURIComponent(equipe.split('=')[1]);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { chave: comoChat, corpo: { texto: 'oi' } })).status, 401);
  assert.equal((await s.pedir('GET', '/api/painel/estado', { cookie: equipe })).status, 200, 'o login de verdade continua valendo');
});

test('achado 2: o link pessoal não aparece em sugestão, exportação nem no pedido à IA', async (t) => {
  const s = await servidor();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  const fernanda = s.store.clientes.find((c) => c.nome.startsWith('Fernanda'));
  // Ela saiu há 60 dias e sumiu.
  s.store.registros.push({ id: 'reg_velho', tipo: 'descida', clienteId: fernanda.id, clienteNome: fernanda.nome, data: '2026-01-01', hora: '10:00', status: 'confirmado', etapa: 'guardada', origem: 'equipe', criadoEm: '2026-01-01T12:00:00.000Z', detalhes: '' });
  let pedidoIA = null;
  const equipe = criarEquipe({ store: s.store, agenda: s.agenda, ia: { modelo: 'x', redigir: async (p) => ((pedidoIA = p), { saida: { textos: [] }, usage: {}, model: 'x' }) } });
  await equipe.rodar('relacionamento');
  const retomada = s.store.sugestoes.find((x) => x.tipo === 'retomada');
  assert.ok(retomada, 'a sugestão de retomada foi criada');
  const exportado = await (await fetch(`${s.base}/api/painel/exportar`, { headers: { Cookie: admin } })).text();
  for (const c of s.store.clientes) {
    assert.ok(!retomada.texto.includes(c.token));
    assert.ok(!exportado.includes(c.token), 'exportação sem link pessoal');
    assert.ok(!JSON.stringify(pedidoIA).includes(c.token), 'pedido à IA sem link pessoal');
  }
});

test('achado 3: o link público tem cota própria de IA e limite por aparelho', async (t) => {
  // Cota: 2 chamadas no dia para o link público, sem tocar no cliente da casa.
  const { store, atendente, conversa, falas } = motor();
  const dia = '2026-12-18';
  for (let i = 0; i < atendente.limitePublico; i++) store.registrarUso({ dia, publico: true });
  const { atendente: at2, conversa: conv2, falas: falas2, store: st2 } = (() => {
    const m = motor();
    for (let i = 0; i < m.atendente.limitePublico; i++) m.store.registrarUso({ dia, publico: true });
    const agenda = criarAgenda(m.store);
    const novo = criarAtendente({ store: m.store, agenda, ia: criarIA(), avisar: () => {} });
    return { ...m, atendente: novo, conversa: (nome) => (nome ? novo.conversaDoCliente(m.cliente(nome)) : novo.criarConversa({})) };
  })();
  const anon = conv2(null);
  at2.receberDoCliente(anon, { texto: 'boa noite' });
  await at2.ocioso();
  assert.equal(falas2(anon, 'assistente').length, 0, 'link público sem cota não gasta IA');
  assert.match(falas2(anon, 'sistema')[0], /atendimento automático não está disponível/);
  assert.match(st2.chamados[0].resumo, /link público/);
  const casa = conv2('Fernanda');
  at2.receberDoCliente(casa, { texto: 'desce amanhã 10h' });
  await at2.ocioso();
  assert.equal(falas2(casa, 'assistente').length, 1, 'cliente da casa continua atendido');
  assert.ok(atendente && conversa && falas && store);

  // Limite por aparelho somando conversas do link público.
  const s = await servidor();
  t.after(s.fechar);
  let ultimo;
  for (let conv = 0; conv < 3 && (!ultimo || ultimo.status !== 429); conv++) {
    const v = await s.sessao();
    for (let i = 0; i < 20; i++) {
      ultimo = await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: `m${i}` }, chave: v.chave });
      if (ultimo.status === 429) break;
    }
  }
  assert.equal(ultimo.status, 429);
  assert.match(ultimo.dados.erro, /deste aparelho/);
  assert.equal((await s.pedir('POST', '/api/chat/foto', { corpo: { dados: 'x' } })).status, 401, 'foto sem sessão é recusada antes de qualquer coisa');
  await s.atendente.ocioso();
});

test('achado 4: pedido do link público chega ao painel marcado e com o telefone que a pessoa deixou', async (t) => {
  const s = await servidor();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  await s.pedir('POST', '/api/painel/modo', { cookie: admin, corpo: { modo: 'auto' } });
  const anon = s.atendente.criarConversa({});
  s.agenda.registrar({ cliente: null, conversaId: anon.id, origem: 'assistente' }, { tipo: 'descida', data: '2030-01-05', hora: '10:00', nome_cliente: 'Carlos Menezes', embarcacao: 'Dona Lúcia' });
  s.agenda.registrar({ cliente: null, conversaId: anon.id, origem: 'assistente' }, { tipo: 'lead-vaga', nome_cliente: 'Eduardo', telefone: '(44) 99888-7777', detalhes: 'lancha 24 pés' });
  const estado = (await s.pedir('GET', '/api/painel/estado', { cookie: admin })).dados;
  assert.equal(estado.pendentes[0].publico, true, 'o cartão sabe que veio do link público');
  assert.equal(estado.pendentes[0].clienteNome, 'Carlos Menezes');
  assert.equal(estado.leads[0].telefone, '44998887777');
});

test('achado 5: mensagem nova durante o turno, no modo sombra, deixa uma resposta só', async () => {
  const ia = iaComPortao();
  const { store, agenda, atendente, conversa, falas } = motor({ modo: 'sombra', ia });
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await ia.chegou;
  atendente.receberDoCliente(c, { texto: 'melhor: desce amanhã 11h com gelo' });
  ia.soltar();
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 1, 'uma resposta esperando, não duas');
  assert.equal(store.registros.length, 1, 'e um registro só');
  assert.equal(store.registros[0].hora, '11:00');
  assert.equal(store.registros[0].rascunho, store.rascunhos[0].turnoId);
  assert.deepEqual(store.rascunhos[0].perguntas, ['desce amanhã 10h', 'melhor: desce amanhã 11h com gelo']);
  assert.equal(atendente.aprovarRascunho(store.rascunhos[0].id, { por: 'Ana' }).ok, true);
  assert.equal(agenda.quadro('2026-12-19').descidas.length, 1, 'depois de aprovada, a descida está no quadro');
  assert.equal(falas(c, 'assistente').length, 1, 'o cliente recebe uma confirmação');
});

test('achado 5: a equipe assume durante o turno e a resposta da IA não sai', async () => {
  const ia = iaComPortao();
  const { store, atendente, conversa, falas } = motor({ modo: 'auto', ia });
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await ia.chegou;
  atendente.responderComoEquipe(c.id, 'Fernanda, aqui é o Zé. Deixa que eu vejo.', 'Zé');
  ia.soltar();
  await atendente.ocioso();
  assert.equal(falas(c, 'assistente').length, 0);
  assert.equal(store.registros.length, 0, 'o que a IA ia registrar foi desfeito');
  assert.equal(c.estado, 'humano');
});

test('achado 6: a equipe cancela um registro com mudança em rascunho e a resposta pendente sai da fila', async () => {
  const { store, agenda, atendente, conversa } = motor({ modo: 'auto' });
  const c = conversa('Carlos');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 9h30' });
  await atendente.ocioso();
  const descida = store.registros[0];
  store.config.modo = 'sombra';
  atendente.receberDoCliente(c, { texto: 'cancela a descida' });
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 1);
  assert.equal(descida.status, 'confirmado', 'o cancelamento ainda espera aprovação');
  assert.equal(descida.pendente.campos.status, 'cancelado');
  assert.equal(agenda.recusar(descida.id, 'Zé', 'rampa fechada').ok, true);
  assert.equal(descida.status, 'cancelado');
  assert.equal(descida.pendente, undefined);
  await atendente.ocioso();
  assert.ok(store.rascunhos.every((r) => r.turnoId !== 'x') && store.rascunhos.length <= 1, 'o rascunho antigo foi trocado por um novo turno');
  assert.equal(descida.status, 'cancelado', 'nada ressuscita a descida');
});

test('achado 7: apagar a conversa com resposta em andamento não quebra o painel nem o atendimento', async (t) => {
  const s = await servidor();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  const v = await s.sessao();
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'quero um desconto' }, chave: v.chave });
  await s.atendente.ocioso();
  assert.equal(s.store.rascunhos.length, 1);
  const id = s.store.rascunhos[0].conversaId;
  assert.equal((await s.pedir('DELETE', `/api/painel/conversa/${id}`, { cookie: admin, corpo: {} })).status, 200);
  assert.equal(s.store.rascunhos.length, 0, 'o rascunho foi junto');
  assert.equal(s.store.chamados.filter((c) => c.rascunho).length, 0);
  const estado = await s.pedir('GET', '/api/painel/estado', { cookie: admin });
  assert.equal(estado.status, 200);
  // Um rascunho órfão, se existisse, também não derruba a tela.
  s.store.rascunhos.push({ id: 'ras_orfao', conversaId: 'con_sumiu', turnoId: 't', texto: 'x', criadoEm: new Date().toISOString(), acoes: [], perguntas: [] });
  assert.equal((await s.pedir('GET', '/api/painel/estado', { cookie: admin })).status, 200);
  const outro = await s.sessao();
  const emerg = await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'socorro estamos afundando' }, chave: outro.chave });
  assert.equal(emerg.status, 200);
  assert.ok(s.store.chamados.some((c) => c.urgencia === 'emergencia'));
  await s.atendente.ocioso();
});

test('achado 8: mensagem que ficou dias sem resposta não é respondida sozinha, e chega ao modelo com a data', async () => {
  const { store, atendente, conversa, falas } = motor({ modo: 'desligado', agora: '2026-12-10T15:00' });
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce a aquarela amanhã 10h' });
  await atendente.ocioso();
  assert.equal(falas(c, 'sistema').length, 1);
  // Dez dias depois o atendente volta em modo automático.
  fixarRelogio('2026-12-20T09:00');
  store.config.modo = 'auto';
  assert.equal(atendente.retomar(), 0, 'nada a retomar: a mensagem é velha');
  await atendente.ocioso();
  assert.equal(store.registros.length, 0, 'nenhuma descida marcada por conta de mensagem antiga');
  atendente.receberDoCliente(c, { texto: 'bom dia' });
  await atendente.ocioso();
  const contexto = c.thread.apiMessages[1].content;
  assert.match(contexto, /10\/12 15:00 \[cliente\] desce a aquarela amanhã 10h/, 'a mensagem antiga vai como contexto, com a data');
  assert.deepEqual(c.thread.apiMessages[0].content.map((b) => b.text), ['bom dia'], 'só a mensagem nova é para responder');
});

test('achado 8: mensagem que esperou mais de meia hora vai com a hora em que foi escrita', async () => {
  const { store, atendente, conversa } = motor({ modo: 'sombra', agora: '2026-12-18T19:00' });
  const c = conversa('Carlos');
  atendente.responderComoEquipe(c.id, 'Carlos, já te respondo.', 'Zé');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 9h' });
  fixarRelogio('2026-12-18T20:10');
  atendente.mudarEstado(c.id, 'ia');
  await atendente.ocioso();
  assert.match(store.rascunhos[0].thread.apiMessages[1].content, /mensagem mais antiga desta leva foi escrita em sexta, 18\/12\/2026, às 19:00/);
});

test('achado 9: emergência é reconhecida com e sem acento, e não em frases comuns', () => {
  for (const frase of ['estamos à deriva, o motor não pega', 'À deriva perto da ilha', 'barco a deriva', 'o barco virou', 'virou a lancha aqui', 'tá afundando', 'Socorro!', 'É uma emergência', 'e emergencia', 'caiu na água e não sabe nadar', 'tem gente se afogando', 'o jet tá pegando fogo', 'INCÊNDIO no barco', 'homem ao mar']) {
    assert.equal(ehEmergencia(frase), true, frase);
  }
  for (const frase of ['qual o telefone de emergência?', 'o motor parou ontem, vocês consertam?', 'virou o ano e eu não fui', 'desce a aquarela amanhã 10h', 'tem colete pra criança?', 'a deriva continental kk'.replace('a deriva', 'adriva')]) {
    assert.equal(ehEmergencia(frase), false, frase);
  }
});

test('achado 9: "à deriva" com crase dispara os telefones mesmo com a IA desligada', async () => {
  const { store, atendente, conversa, falas } = motor({ modo: 'desligado' });
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'estamos à deriva, o motor não pega' });
  assert.match(falas(c, 'sistema')[0], /^Emergência: ligue agora para a marina no \(44\) 90000-0000\. Marinha: 185\. Bombeiros: 193/);
  assert.equal(store.chamados[0].urgencia, 'emergencia');
  await atendente.ocioso();
});

test('achado 10: depois de uma falha passageira o assistente volta a responder', async () => {
  const { store, atendente, conversa, falas } = motor({ modo: 'auto', agora: '2026-12-18T19:00' });
  const c = conversa('Paulo');
  atendente.receberDoCliente(c, { texto: 'boa noite ERRO_IA' });
  await atendente.ocioso();
  assert.equal(c.estado, 'humano');
  assert.equal(c.humano.motivo, 'falha');
  // Cinco minutos depois ainda é cedo; a mensagem fica com a equipe, sem novo aviso.
  fixarRelogio('2026-12-18T19:05');
  atendente.receberDoCliente(c, { texto: 'alô?' });
  await atendente.ocioso();
  assert.equal(c.estado, 'humano');
  assert.equal(falas(c, 'sistema').length, 1, 'não repete o pedido de desculpas');
  // Uma semana depois, às 22h, ele escreve de novo: o assistente responde.
  fixarRelogio('2026-12-25T22:00');
  atendente.receberDoCliente(c, { texto: 'desce a serena amanhã 9h' });
  await atendente.ocioso();
  assert.equal(c.estado, 'ia');
  assert.equal(falas(c, 'assistente').length, 1);
  assert.equal(store.registros.find((r) => r.tipo === 'descida').data, '2026-12-26');
});

test('achado 10: conversa assumida pela equipe volta ao assistente depois de 12 horas de silêncio', async () => {
  const { atendente, conversa, falas } = motor({ modo: 'auto', agora: '2026-12-18T10:00' });
  const c = conversa('Carlos');
  atendente.responderComoEquipe(c.id, 'Carlos, resolvido por aqui.', 'Sandra');
  fixarRelogio('2026-12-18T15:00');
  atendente.receberDoCliente(c, { texto: 'obrigado' });
  await atendente.ocioso();
  assert.equal(c.estado, 'humano', 'cinco horas depois ainda é da equipe');
  assert.equal(falas(c, 'assistente').length, 0);
  fixarRelogio('2026-12-19T08:00');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  assert.equal(c.estado, 'ia');
  assert.equal(falas(c, 'assistente').length, 1);
});

test('achado 10: o aviso de espera vale por 6 horas; depois disso sai outro, com chamado', async () => {
  const { store, atendente, conversa, falas } = motor({ modo: 'auto', agora: '2026-12-18T10:00' });
  const c = conversa('Paulo');
  atendente.responderComoEquipe(c.id, 'Dr. Paulo, um instante.', 'Sandra');
  atendente.receberDoCliente(c, { texto: 'e a minha mensalidade?' });
  fixarRelogio('2026-12-18T10:15');
  assert.equal(atendente.vigiar(), 1);
  const primeiro = store.chamados[0];
  atendente.resolverChamado(primeiro.id, 'Sandra');
  fixarRelogio('2026-12-18T11:00');
  atendente.receberDoCliente(c, { texto: 'alguém?' });
  fixarRelogio('2026-12-18T11:30');
  assert.equal(atendente.vigiar(), 0, 'dentro de 6 horas o aviso anterior ainda cobre');
  fixarRelogio('2026-12-18T20:00');
  atendente.receberDoCliente(c, { texto: 'continuo esperando' });
  fixarRelogio('2026-12-18T20:11');
  assert.equal(atendente.vigiar(), 1, 'passadas 6 horas, novo aviso');
  assert.equal(falas(c, 'sistema').length, 2);
  assert.equal(store.chamados.filter((x) => x.status === 'aberto').length, 1, 'e novo chamado, já que o anterior foi fechado');
  await atendente.ocioso();
});

test('achado 14: resposta em dois balões conta uma vez; custo não some por causa de modelo sem preço', async () => {
  const { store, atendente, conversa } = motor({ modo: 'auto' });
  const c = conversa(null);
  atendente.receberDoCliente(c, { texto: 'boa tarde' });
  await atendente.ocioso();
  assert.equal(c.mensagens.filter((m) => m.de === 'assistente').length, 2, 'o roteiro responde em dois balões');
  store.registrarUso({ dia: '2026-12-18', modelo: 'claude-opus-5-5', usd: 0.02 });
  store.registrarUso({ dia: '2026-12-18', modelo: 'modelo-novo', usd: null });
  const r = relatorio(store, {});
  assert.equal(r.respostasAssistente, 1);
  assert.equal(r.ia.usd, 0.02);
  assert.equal(r.ia.chamadasSemPreco, 2, 'a do roteiro e a do modelo novo');
});

test('achado 14: registro feito às 22h entra no dia da marina, não no dia do servidor', async () => {
  const { store, agenda, cliente } = motor({ agora: '2026-12-18T22:30' });
  agenda.registrar({ cliente: cliente('Carlos'), conversaId: 'c', origem: 'assistente' }, { tipo: 'descida', data: '2026-12-19', hora: '09:00' });
  assert.equal(store.registros[0].criadoDia, '2026-12-18');
  assert.equal(relatorio(store, { de: '2026-12-18', ate: '2026-12-18' }).descidas.total, 1);
});

test('achado 15b: erro 400 em conversa com histórico não sai testando formatos', async () => {
  let n = 0;
  const falha = async () => {
    n++;
    throw Anthropic.APIError.generate(400, { type: 'error', error: { message: 'historico' } }, 'historico', new Headers());
  };
  const criar = criarReal({ beta: { messages: { create: falha } }, messages: { create: falha } }, { fallback: true });
  await assert.rejects(criar({ sistema: 's', messages: [{ role: 'user', content: 'a' }, { role: 'assistant', content: [{ type: 'text', text: 'b' }] }, { role: 'user', content: 'c' }] }), (e) => e.tipo === 'requisicao');
  assert.equal(n, 1);
  assert.equal(criar.formato(), '11111');
});

test('achado 15c: resposta que não terminou direito não vai para o cliente', async () => {
  const ia = { modelo: 'x', formato: () => 'x', criar: async () => ({ model: 'x', usage: {}, stop_reason: 'model_context_window_exceeded', content: [{ type: 'text', text: 'Confirmado: desc' }] }) };
  const { store, atendente, conversa, falas } = motor({ modo: 'auto', ia });
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  assert.equal(falas(c, 'assistente').length, 0);
  assert.equal(c.estado, 'humano');
  assert.match(store.chamados[0].resumo, /parou antes do fim/);
});

test('menores: arquivo de uso com linha cortada não impede a partida; falha de gravação não derruba', () => {
  const { store, dir } = motor();
  store.registrarUso({ dia: '2026-12-18', usd: 0.01 });
  fs.appendFileSync(path.join(dir, 'uso.jsonl'), '{"dia":"2026-12-18","us');
  assert.equal(store.lerUso().length, 1);
  // Pasta de conversas some: gravar falha, mas não lança.
  fs.rmSync(path.join(dir, 'conversas'), { recursive: true });
  store.conversas.set('con_x', { id: 'con_x', mensagens: [] });
  store.salvar('conversa:con_x');
  const erroOriginal = console.error;
  console.error = () => {};
  try {
    assert.equal(store.descarregar(), false);
  } finally {
    console.error = erroOriginal;
  }
  fs.mkdirSync(path.join(dir, 'conversas'));
  assert.equal(store.descarregar(), true, 'na tentativa seguinte grava');
});

test('menores: rodar um agente na mão antes da hora não cancela a rodada do dia', async () => {
  const { store, agenda } = motor({ agora: '2026-12-18T07:00' });
  const equipe = criarEquipe({ store, agenda, ia: { redigir: null, modelo: 'x' } });
  await equipe.rodar('relacionamento', { por: 'Ana' });
  fixarRelogio('2026-12-18T08:40');
  assert.equal(equipe.deveRodar('relacionamento'), true);
  await equipe.tique();
  assert.equal(equipe.deveRodar('relacionamento'), false);
});

test('chamado novo para a mesma pessoa troca o anterior, sem empilhar', async () => {
  const { store, atendente, conversa } = motor({ modo: 'auto' });
  const c = conversa(null);
  atendente.receberDoCliente(c, { texto: 'quero desconto na lancha' });
  await atendente.ocioso();
  atendente.receberDoCliente(c, { texto: 'e quero falar com o gerente agora' });
  await atendente.ocioso();
  const paraSandra = store.chamados.filter((x) => x.para.startsWith('Sandra'));
  assert.equal(paraSandra.length, 2);
  assert.equal(paraSandra.filter((x) => x.status === 'aberto').length, 1, 'só o mais novo fica aberto');
  assert.equal(paraSandra[0].resolvidoPor, 'atualizado por um chamado mais novo');
});

test('o cliente não recebe o campo de detalhes do registro, que pode ter anotação para a equipe', async (t) => {
  const s = await servidor();
  t.after(s.fechar);
  const marcos = s.store.clientes.find((c) => c.nome.startsWith('Marcos'));
  const conv = s.atendente.conversaDoCliente(marcos);
  s.agenda.registrar({ cliente: marcos, conversaId: conv.id, origem: 'assistente' }, { tipo: 'descida', data: '2030-01-05', hora: '10:00', detalhes: 'cadastro com pendência' });
  const ses = await s.sessao({ token: marcos.token });
  assert.equal(ses.registros.length, 1);
  assert.ok(!JSON.stringify(ses.registros).includes('pendência'));
});

test('achado 13: salvar uma grade que deixa descidas fora avisa quem está configurando', async (t) => {
  const s = await servidor();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  const carlos = s.store.clientes.find((c) => c.nome.startsWith('Carlos'));
  s.agenda.registrar({ cliente: carlos, conversaId: null, origem: 'equipe' }, { tipo: 'descida', data: '2030-01-05', hora: '09:30' });
  const r = await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { rampa: { janelaMin: 20 } } });
  assert.equal(r.status, 200);
  assert.match(r.dados.aviso, /1 descida\(s\) já marcada\(s\)/);
  const estado = (await s.pedir('GET', '/api/painel/estado?data=2030-01-05', { cookie: admin })).dados;
  assert.deepEqual(estado.quadro.horas.map((h) => h.hora), ['09:30']);
});

// ---------------------------------------------------------------------
// Depois da revisão: custo (manutenção do cache), fuso e limites.
// ---------------------------------------------------------------------

/** IA de mentira com manutenção de cache. `leitura` é o que cada manutenção diz ter lido do cache. */
function iaComCache(leitura = () => 9000) {
  const base = criarIA();
  const manutencoes = [];
  return {
    ...base,
    modelo: 'claude-opus-5-5',
    manutencoes,
    aquecer: async ({ sistema }) => {
      manutencoes.push(sistema);
      const lido = leitura(manutencoes.length);
      if (lido instanceof Error) throw lido;
      return { model: 'claude-opus-5-5', content: [], stop_reason: 'max_tokens', usage: { input_tokens: 4, output_tokens: 0, cache_read_input_tokens: lido, cache_creation_input_tokens: lido ? 0 : 9000 } };
    },
  };
}

test('manutenção do cache: relê o prompt perto de 1 hora, só depois de um atendimento de verdade', async () => {
  const ia = iaComCache();
  const { store, atendente, conversa } = motor({ modo: 'auto', ia, agora: '2026-12-18T09:00' });
  assert.equal(await atendente.manterCache(), 'parado', 'sem atendimento ainda não há cache para manter');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'boa tarde' });
  await atendente.ocioso();
  fixarRelogio('2026-12-18T09:20');
  assert.equal(await atendente.manterCache(), 'cedo');
  fixarRelogio('2026-12-18T09:52');
  assert.equal(await atendente.manterCache(), 'renovado');
  assert.equal(await atendente.manterCache(), 'cedo', 'no mesmo minuto não repete');
  fixarRelogio('2026-12-18T10:44');
  assert.equal(await atendente.manterCache(), 'renovado', 'a manutenção anterior conta como uso do cache');
  assert.equal(ia.manutencoes.length, 2);
  assert.equal(ia.manutencoes[0], atendente.prompt().sistema, 'com o mesmo prompt dos atendimentos');
  const linhas = store.lerUso().filter((u) => u.aquecimento);
  assert.equal(linhas.length, 2);
  assert.ok(linhas[0].usd > 0 && linhas[0].usd < 0.005, 'uma leitura custa uma fração de centavo');
  assert.equal(atendente.usoHoje(), 1, 'manutenção não conta no limite diário de respostas');
  assert.equal(relatorio(store, {}).ia.manutencoesDeCache, 2);
});

test('manutenção do cache: para sozinha quando não faz sentido', async () => {
  // Perdeu a janela: o cache já venceu, não adianta pedir.
  let m = motor({ modo: 'auto', ia: iaComCache(), agora: '2026-12-18T09:00' });
  m.atendente.receberDoCliente(m.conversa('Fernanda'), { texto: 'oi' });
  await m.atendente.ocioso();
  fixarRelogio('2026-12-18T10:05');
  assert.equal(await m.atendente.manterCache(), 'vencido');
  assert.equal(await m.atendente.manterCache(), 'parado');

  // A ficha mudou: o cache antigo não serve mais.
  const ia = iaComCache();
  m = motor({ modo: 'auto', ia, agora: '2026-12-18T09:00' });
  m.atendente.receberDoCliente(m.conversa('Fernanda'), { texto: 'oi' });
  await m.atendente.ocioso();
  m.store.ficha += '\nNova regra.';
  fixarRelogio('2026-12-18T09:52');
  assert.equal(await m.atendente.manterCache(), 'parado');

  // Atendente desligado.
  m = motor({ modo: 'auto', ia: iaComCache(), agora: '2026-12-18T09:00' });
  m.atendente.receberDoCliente(m.conversa('Fernanda'), { texto: 'oi' });
  await m.atendente.ocioso();
  m.store.config.modo = 'desligado';
  fixarRelogio('2026-12-18T09:52');
  assert.equal(await m.atendente.manterCache(), 'parado');
  assert.equal(ia.manutencoes.length, 0);

  // Um dia inteiro sem cliente: para de manter até o próximo atendimento.
  const ia2 = iaComCache();
  m = motor({ modo: 'auto', ia: ia2, agora: '2026-12-18T09:00' });
  m.atendente.receberDoCliente(m.conversa('Fernanda'), { texto: 'oi' });
  await m.atendente.ocioso();
  let hora = new Date('2026-12-18T09:00:00');
  let ultimo = '';
  for (let i = 0; i < 40; i++) {
    hora = new Date(hora.getTime() + 52 * 60_000);
    fixarRelogio(`${hora.getFullYear()}-${String(hora.getMonth() + 1).padStart(2, '0')}-${String(hora.getDate()).padStart(2, '0')}T${String(hora.getHours()).padStart(2, '0')}:${String(hora.getMinutes()).padStart(2, '0')}`);
    ultimo = await m.atendente.manterCache();
  }
  assert.equal(ultimo, 'parado');
  assert.ok(ia2.manutencoes.length >= 26 && ia2.manutencoes.length <= 28, `manteve só durante 24 horas (${ia2.manutencoes.length} vezes)`);
});

test('manutenção do cache: se não reaproveita o cache, desliga em vez de gastar', async () => {
  const avisos = [];
  const original = console.warn;
  console.warn = (t) => avisos.push(String(t));
  try {
    const ia = iaComCache(() => 0); // a API diz que não leu nada do cache
    const m = motor({ modo: 'auto', ia, agora: '2026-12-18T09:00' });
    m.atendente.receberDoCliente(m.conversa('Fernanda'), { texto: 'oi' });
    await m.atendente.ocioso();
    fixarRelogio('2026-12-18T09:52');
    assert.equal(await m.atendente.manterCache(), 'falhou');
    fixarRelogio('2026-12-18T10:44');
    assert.equal(await m.atendente.manterCache(), 'falhou');
    fixarRelogio('2026-12-18T11:36');
    assert.equal(await m.atendente.manterCache(), 'parado', 'depois de duas vezes não tenta mais');
    assert.equal(ia.manutencoes.length, 2);
    assert.ok(avisos.some((t) => /foi desligada/.test(t)));

    // Pedido recusado pela API: desliga na hora, e o atendimento continua funcionando.
    const ia2 = iaComCache(() => Object.assign(new Error('formato recusado'), { tipo: 'requisicao' }));
    const m2 = motor({ modo: 'auto', ia: ia2, agora: '2026-12-18T09:00' });
    const c = m2.conversa('Fernanda');
    m2.atendente.receberDoCliente(c, { texto: 'oi' });
    await m2.atendente.ocioso();
    fixarRelogio('2026-12-18T09:52');
    assert.equal(await m2.atendente.manterCache(), 'falhou');
    fixarRelogio('2026-12-18T09:53');
    assert.equal(await m2.atendente.manterCache(), 'parado');
    assert.equal(ia2.manutencoes.length, 1);
    m2.atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
    await m2.atendente.ocioso();
    assert.equal(m2.store.registros.length, 1);

    // Falha passageira (rede, limite de uso): tenta de novo no minuto seguinte, sem desligar.
    const ia3 = iaComCache((n) => (n === 1 ? Object.assign(new Error('sem conexão'), { tipo: 'temporaria' }) : 9000));
    const m3 = motor({ modo: 'auto', ia: ia3, agora: '2026-12-18T09:00' });
    m3.atendente.receberDoCliente(m3.conversa('Fernanda'), { texto: 'oi' });
    await m3.atendente.ocioso();
    fixarRelogio('2026-12-18T09:52');
    assert.equal(await m3.atendente.manterCache(), 'falhou');
    fixarRelogio('2026-12-18T09:53');
    assert.equal(await m3.atendente.manterCache(), 'renovado');
    assert.equal(m3.store.lerUso().filter((u) => u.aquecimento).length, 1, 'só o pedido que deu certo entra no custo');
  } finally {
    console.warn = original;
  }
});

test('modo de demonstração não faz manutenção de cache', async () => {
  const { atendente, conversa } = motor({ modo: 'auto', agora: '2026-12-18T09:00' });
  atendente.receberDoCliente(conversa('Fernanda'), { texto: 'oi' });
  await atendente.ocioso();
  fixarRelogio('2026-12-18T09:52');
  assert.equal(await atendente.manterCache(), 'parado');
});

test('fuso da marina: muda pelo painel, vale na hora e não aceita valor inventado', async (t) => {
  const s = await servidor();
  const { agora: agoraDaMarina, definirFuso } = await import('../lib/tempo.js');
  t.after(() => {
    definirFuso('America/Sao_Paulo');
    s.fechar();
  });
  const admin = await s.entrar('senha-admin');
  const antes = agoraDaMarina();
  const r = await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { fuso: 'America/Campo_Grande' } });
  assert.equal(r.status, 200);
  assert.equal(s.store.config.fuso, 'America/Campo_Grande');
  const depois = agoraDaMarina();
  const diferenca = (antes.minutos - depois.minutos + 1440) % 1440;
  assert.ok(diferenca >= 59 && diferenca <= 61, `Mato Grosso do Sul está 1 hora atrás de Brasília (diferença de ${diferenca} min)`);
  assert.equal((await s.pedir('GET', '/api/painel/estado', { cookie: admin })).dados.marina.fuso, 'America/Campo_Grande');
  const ruim = await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { fuso: 'Marte/Olympus' } });
  assert.equal(ruim.status, 400);
  assert.equal(s.store.config.fuso, 'America/Campo_Grande');
  // Salvar outra coisa sem mandar o fuso não mexe nele.
  await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { nome: 'Marina Teste' } });
  assert.equal(s.store.config.fuso, 'America/Campo_Grande');
});

test('achado 3: fotos têm teto de disco; cheio, a marina não cai e o cliente é avisado', async (t) => {
  const antes = process.env.FOTOS_LIMITE_MB;
  process.env.FOTOS_LIMITE_MB = '0.0001'; // cerca de 100 bytes
  const s = await servidor();
  t.after(() => {
    if (antes === undefined) delete process.env.FOTOS_LIMITE_MB;
    else process.env.FOTOS_LIMITE_MB = antes;
    s.fechar();
  });
  const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');
  const dados = `data:image/png;base64,${Buffer.concat([png, Buffer.alloc(200)]).toString('base64')}`;
  const v = await s.sessao();
  const primeira = await s.pedir('POST', '/api/chat/foto', { corpo: { dados }, chave: v.chave });
  assert.equal(primeira.status, 200, 'a primeira cabe');
  const segunda = await s.pedir('POST', '/api/chat/foto', { corpo: { dados }, chave: v.chave });
  assert.equal(segunda.status, 507);
  assert.match(segunda.dados.erro, /Não consigo receber fotos agora/);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'oi' }, chave: v.chave })).status, 200, 'o texto continua funcionando');
  await s.atendente.ocioso();
});

test('achado 6: resposta parada na aprovação por mais de 6 horas é desfeita e a vaga volta', async () => {
  const { store, agenda, atendente, conversa } = motor({ modo: 'sombra', agora: '2026-12-18T08:00' });
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 1);
  assert.equal(agenda.janelasDoDia('2026-12-19').find((j) => j.hora === '10:00').ocupadas, 1, 'o rascunho segura a vaga');
  fixarRelogio('2026-12-18T13:00');
  atendente.vigiar();
  assert.equal(store.rascunhos.length, 1, 'com 5 horas ainda espera');
  fixarRelogio('2026-12-18T14:30');
  atendente.vigiar();
  assert.equal(store.rascunhos.length, 0, 'depois de 6 horas sai da fila');
  assert.equal(store.registros.length, 0, 'e o registro em rascunho é desfeito');
  assert.equal(agenda.janelasDoDia('2026-12-19').find((j) => j.hora === '10:00').ocupadas, 0, 'a vaga volta');
  await atendente.ocioso();
});
