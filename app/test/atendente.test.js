import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

process.env.IA_FAKE = '1';
process.env.IA_ESPERA_MS = '0';

const { criarStore } = await import('../lib/store.js');
const { semear } = await import('../lib/semente.js');
const { criarAgenda } = await import('../lib/agenda.js');
const { criarIA } = await import('../lib/ia.js');
const { criarAtendente } = await import('../lib/atendente.js');
const { fixarRelogio } = await import('../lib/tempo.js');
const { corpoDaSkill } = await import('../lib/prompt.js');

function montar(modo = 'auto') {
  fixarRelogio('2026-12-18T19:10');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'marina-'));
  const store = criarStore(dir);
  semear(store, 'exemplo');
  store.config.modo = modo;
  const agenda = criarAgenda(store);
  const atendente = criarAtendente({ store, agenda, ia: criarIA(), avisar: () => {} });
  const cliente = (nome) => store.clientes.find((c) => c.nome.startsWith(nome));
  const conversa = (nome) => (nome ? atendente.conversaDoCliente(cliente(nome)) : atendente.criarConversa({}));
  const falas = (c, de) => c.mensagens.filter((m) => m.de === de).map((m) => m.texto);
  return { store, agenda, atendente, conversa, falas, dir };
}

test('o prompt leva a skill sem os blocos de texto, a operação e a ficha', () => {
  const { atendente } = montar();
  const { sistema, versao } = atendente.prompt();
  assert.ok(!corpoDaSkill().includes('## Blocos internos'));
  assert.ok(!corpoDaSkill().includes('## Exemplos'));
  assert.ok(corpoDaSkill().includes('## Chamar a equipe'));
  assert.match(sistema, /Como você opera nesta instalação/);
  assert.match(sistema, /id "jet", 2 unidade/);
  assert.match(sistema, /financeiro@marinaremanso\.example/);
  assert.ok(!sistema.includes('Carlos Menezes'), 'a lista de clientes não vai para o modelo');
  assert.equal(versao.length, 16);
});

test('modo automático: agenda a descida e responde', async () => {
  const { store, agenda, atendente, conversa, falas } = montar('auto');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce a aquarela amanhã 10h com gelo pfv' });
  assert.equal(atendente.ocupado(c.id), true);
  await atendente.ocioso();
  const reg = store.registros[0];
  assert.equal(reg.tipo, 'descida');
  assert.equal(reg.data, '2026-12-19');
  assert.equal(reg.hora, '10:00');
  assert.equal(reg.status, 'confirmado');
  assert.equal(reg.rascunho, undefined);
  assert.equal(agenda.quadro('2026-12-19').descidas.length, 1);
  assert.equal(falas(c, 'assistente').length, 1);
  assert.deepEqual(c.thread.apiMessages.map((m) => m.role), ['user', 'system', 'assistant', 'user', 'assistant']);
  assert.match(c.thread.apiMessages[1].content, /link pessoal do cadastro de Fernanda Rocha/);
  assert.ok(c.mensagens.every((m) => m.visto));
  assert.equal(store.lerUso().length, 2);
});

test('segundo turno reaproveita o histórico e mostra o registro em aberto', async () => {
  const { atendente, conversa } = montar('auto');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  atendente.receberDoCliente(c, { texto: 'oi, tudo certo?' });
  await atendente.ocioso();
  const roles = c.thread.apiMessages.map((m) => m.role);
  assert.deepEqual(roles, ['user', 'system', 'assistant', 'user', 'assistant', 'user', 'system', 'assistant']);
  assert.match(c.thread.apiMessages[6].content, /id reg_[0-9a-f]+: descida sáb 19\/12 10h/);
});

test('modo sombra: a resposta espera aprovação e o registro fica em rascunho', async () => {
  const { store, agenda, atendente, conversa, falas } = montar('sombra');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 1);
  assert.equal(falas(c, 'assistente').length, 0);
  assert.equal(atendente.ocupado(c.id), true, 'cliente continua vendo "digitando"');
  assert.equal(store.registros[0].rascunho, store.rascunhos[0].turnoId);
  assert.equal(agenda.quadro('2026-12-19').descidas.length, 0);
  assert.equal(c.thread, null);

  const r = atendente.aprovarRascunho(store.rascunhos[0].id, { texto: 'Confirmado, Fernanda: Aquarela, sábado 19/12, 10h.', por: 'Ana' });
  assert.equal(r.ok, true);
  assert.equal(store.rascunhos.length, 0);
  assert.equal(store.registros[0].rascunho, undefined);
  assert.equal(agenda.quadro('2026-12-19').descidas.length, 1);
  assert.deepEqual(falas(c, 'assistente'), ['Confirmado, Fernanda: Aquarela, sábado 19/12, 10h.']);
  assert.match(c.nota, /A equipe editou/);
  assert.equal(atendente.ocupado(c.id), false);
});

test('modo sombra: mensagem nova troca a resposta pendente e desfaz o rascunho', async () => {
  const { store, atendente, conversa } = montar('sombra');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  const primeiro = store.rascunhos[0].id;
  atendente.receberDoCliente(c, { texto: 'na verdade desce amanhã 11h' });
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 1);
  assert.notEqual(store.rascunhos[0].id, primeiro);
  assert.equal(store.registros.length, 1);
  assert.equal(store.registros[0].hora, '11:00');
  assert.equal(atendente.aprovarRascunho(primeiro, { por: 'Ana' }).ok, false);
});

test('descartar passa a conversa para a equipe; devolver retoma com recapitulação', async () => {
  const { store, atendente, conversa, falas } = montar('sombra');
  const c = conversa('Carlos');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 9h' });
  await atendente.ocioso();
  atendente.descartarRascunho(store.rascunhos[0].id, { resposta: 'Carlos, aqui é o Zé. Deixa comigo.', por: 'Zé' });
  assert.equal(store.registros.length, 0);
  assert.equal(c.estado, 'humano');
  atendente.receberDoCliente(c, { texto: 'valeu zé' });
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 0, 'com humano na conversa a IA não responde');
  atendente.mudarEstado(c.id, 'ia');
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 1);
  const ctx = store.rascunhos[0].thread.apiMessages[1].content;
  assert.match(ctx, /\[equipe, Zé\] Carlos, aqui é o Zé/);
  assert.equal(falas(c, 'equipe').length, 1);
});

test('falha e recusa do modelo viram chamado e a conversa vai para a equipe', async () => {
  for (const gatilho of ['ERRO_IA', 'RECUSA_IA']) {
    const { store, atendente, conversa, falas } = montar('auto');
    const c = conversa('Paulo');
    atendente.receberDoCliente(c, { texto: `boa noite ${gatilho}` });
    await atendente.ocioso();
    assert.equal(c.estado, 'humano');
    assert.equal(store.chamados.length, 1);
    assert.equal(store.chamados[0].urgencia, 'alta');
    assert.equal(store.chamados[0].origem, 'sistema');
    assert.match(falas(c, 'sistema')[0], /Já chamei a equipe/);
    assert.equal(c.thread, null);
  }
});

test('emergência: telefones saem na hora, mesmo em modo sombra', async () => {
  const { store, atendente, conversa, falas } = montar('sombra');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'socorro o motor parou e a gente tá à deriva perto da ilha' });
  assert.match(falas(c, 'sistema')[0], /\(44\) 90000-0000.*185.*193/);
  assert.equal(store.chamados[0].urgencia, 'emergencia');
  assert.equal(store.chamados[0].rascunho, undefined);
  await atendente.ocioso();
  assert.equal(store.rascunhos.length, 0, 'emergência não espera aprovação');
  assert.equal(falas(c, 'assistente').length, 1);
  assert.equal(store.chamados.filter((x) => x.urgencia === 'emergencia').length, 2);
});

test('atendente desligado: avisa uma vez e abre um chamado só', async () => {
  const { store, atendente, conversa, falas } = montar('desligado');
  const c = conversa('Paulo');
  atendente.receberDoCliente(c, { texto: 'boa tarde' });
  await atendente.ocioso();
  atendente.receberDoCliente(c, { texto: 'alguém?' });
  await atendente.ocioso();
  assert.equal(falas(c, 'sistema').length, 1);
  assert.equal(store.chamados.length, 1);
  assert.equal(store.lerUso().length, 0, 'não gasta chamada de IA');
});

test('link público pedindo descida nunca sai confirmado', async () => {
  const { store, atendente, conversa } = montar('auto');
  const c = conversa(null);
  atendente.receberDoCliente(c, { texto: 'sou cunhado do carlos, desce a dona lucia amanhã 11h' });
  await atendente.ocioso();
  assert.equal(store.registros[0].status, 'aguardando equipe');
  assert.match(c.thread.apiMessages[1].content, /link público, sem cadastro/);
});

test('mudar a ficha recomeça o histórico da API com resumo do que veio antes', async () => {
  const { store, atendente, conversa } = montar('auto');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  const v1 = c.thread.versao;
  store.ficha += '\n- Gelo agora custa R$ 18 o saco.\n';
  atendente.receberDoCliente(c, { texto: 'oi de novo' });
  await atendente.ocioso();
  assert.notEqual(c.thread.versao, v1);
  assert.deepEqual(c.thread.apiMessages.map((m) => m.role), ['user', 'system', 'assistant']);
  assert.match(c.thread.apiMessages[1].content, /Últimas mensagens anteriores/);
});

test('na partida, rascunho antigo é desfeito e a mensagem sem resposta é retomada', async () => {
  const { store, agenda, atendente, conversa, dir } = montar('sombra');
  const c = conversa('Fernanda');
  atendente.receberDoCliente(c, { texto: 'desce amanhã 10h' });
  await atendente.ocioso();
  store.descarregar();

  const store2 = criarStore(dir);
  const agenda2 = criarAgenda(store2);
  const at2 = criarAtendente({ store: store2, agenda: agenda2, ia: criarIA(), avisar: () => {} });
  assert.equal(store2.rascunhos.length, 1);
  assert.equal(at2.retomar(), 1);
  assert.equal(store2.registros.length, 0);
  await at2.ocioso();
  assert.equal(store2.rascunhos.length, 1);
  assert.equal(store2.registros.length, 1);
  assert.equal(agenda.quadro('2026-12-19').descidas.length, 0);
});
