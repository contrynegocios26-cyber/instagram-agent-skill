import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const { criarStore } = await import('../lib/store.js');
const { semear, completarConfig } = await import('../lib/semente.js');
const { criarAgenda } = await import('../lib/agenda.js');
const { criarEquipe, segundaDe } = await import('../lib/equipe.js');
const { fixarRelogio } = await import('../lib/tempo.js');
const { FalhaIA } = await import('../lib/ia.js');

function montar({ redigir = null, agora = '2026-12-18T12:00' } = {}) {
  fixarRelogio(agora);
  const store = criarStore(fs.mkdtempSync(path.join(os.tmpdir(), 'marina-equipe-')));
  semear(store, 'exemplo');
  const agenda = criarAgenda(store);
  const equipe = criarEquipe({ store, agenda, ia: { redigir, modelo: 'teste' }, urlBase: 'https://marina.exemplo' });
  const cli = (nome) => store.clientes.find((c) => c.nome.startsWith(nome));
  const descida = (nome, data, hora, detalhes = '') => agenda.registrar({ cliente: cli(nome), conversaId: null, origem: 'equipe', forcar: true }, { tipo: 'descida', data, hora, detalhes });
  return { store, agenda, equipe, cli, descida };
}

test('segundaDe acha a segunda-feira da semana', () => {
  assert.equal(segundaDe('2026-12-18'), '2026-12-14'); // sexta
  assert.equal(segundaDe('2026-12-14'), '2026-12-14'); // segunda
  assert.equal(segundaDe('2026-12-20'), '2026-12-14'); // domingo
});

test('operação: resumo do dia, atualizado enquanto está pendente', async () => {
  const { store, equipe, descida, agenda } = montar({ agora: '2026-12-19T06:40' });
  descida('Carlos', '2026-12-19', '09:00', 'gelo');
  descida('Fernanda', '2026-12-19', '10:00');
  let r = await equipe.rodar('operacao');
  assert.equal(r.criadas, 1);
  const s = store.sugestoes[0];
  assert.match(s.texto, /Rampa de sábado, 19\/12\/2026 · Marina Remanso/);
  assert.match(s.texto, /Descidas: 2/);
  assert.match(s.texto, /9h · Lancha "Dona Lúcia", 24 pés · gelo/);
  assert.equal(s.para.telefone, '44999000002');
  assert.equal(s.viaIA, false);

  assert.equal((await equipe.rodar('operacao')).criadas, 0, 'nada mudou');
  descida('Paulo', '2026-12-19', '11:00');
  assert.equal((await equipe.rodar('operacao')).criadas, 1);
  assert.equal(store.sugestoes.length, 1, 'atualiza a pendente em vez de criar outra');
  assert.match(store.sugestoes[0].texto, /Descidas: 3/);

  equipe.concluir(s.id, { acao: 'feita', por: 'Zé' });
  descida('Marcos', '2026-12-19', '12:00');
  assert.equal((await equipe.rodar('operacao')).criadas, 0, 'pela agenda, um resumo por dia');
  assert.equal((await equipe.rodar('operacao', { por: 'Zé' })).criadas, 1, 'pedido na mão, sai um novo');
  assert.equal(store.sugestoes.length, 2);
  assert.equal(agenda.quadro('2026-12-19').descidas.length, 4);
});

test('relacionamento: vencimento, revisão, documento, retomada e pós-passeio', async () => {
  const { store, equipe, cli, descida, agenda } = montar({ agora: '2026-10-20T09:00' });
  // Fernanda saiu em 20/10 e depois sumiu; Paulo sai em 17/12 e guarda o barco.
  descida('Fernanda', '2026-10-20', '10:00');
  fixarRelogio('2026-12-17T08:00');
  const p = descida('Paulo', '2026-12-17', '10:00');
  agenda.mudarEtapa(p.registro_id, 'na_agua', 'Zé');
  agenda.mudarEtapa(p.registro_id, 'guardada', 'Zé');
  cli('Paulo').revisaoEm = '2026-12-28';
  cli('Paulo').documentoVence = '2027-01-10';
  cli('Marcos').mensalidadeDia = 20; // tem pendência: fica fora do lembrete
  fixarRelogio('2026-12-18T08:40');

  const r = await equipe.rodar('relacionamento');
  const por = (tipo) => store.sugestoes.filter((s) => s.tipo === tipo);
  assert.equal(r.criadas, store.sugestoes.length);

  assert.equal(por('vencimento').length, 1);
  assert.match(por('vencimento')[0].texto, /Olá, Carlos!.*mensalidade da vaga da Lancha "Dona Lúcia", 24 pés vence dia 20\/12/);
  assert.ok(!/atras|multa|cobran/i.test(por('vencimento')[0].texto));

  assert.match(por('revisao')[0].texto, /revisão do motor da Lancha "Serena", 29 pés está prevista para 28\/12/);
  assert.match(por('documento')[0].texto, /documento da Lancha "Serena", 29 pés vence em 10\/01/);

  assert.equal(por('retomada').length, 1);
  assert.match(por('retomada')[0].texto, /Olá, Fernanda!.*pelo seu link: https:\/\/marina\.exemplo\/c\//);

  assert.equal(por('pos-passeio').length, 1);
  assert.match(por('pos-passeio')[0].texto, /Olá, Paulo!.*passeio de 17\/12.*https:\/\/g\.page\/r\/marina-remanso-exemplo\/review/);
  assert.equal(por('pos-passeio')[0].para.telefone, '44999003344');

  assert.equal((await equipe.rodar('relacionamento')).criadas, 0, 'cada lembrete sai uma vez');

  cli('Carlos').semLembretes = true;
  fixarRelogio('2027-01-18T08:40');
  await equipe.rodar('relacionamento');
  assert.equal(por('vencimento').length, 1, 'cliente que pediu para não receber fica fora');
});

test('vendas: retorno só para interessado de 1 a 14 dias, com o telefone que ele deixou', async () => {
  const { store, agenda, equipe } = montar({ agora: '2026-12-01T10:00' });
  const visita = (n) => ({ cliente: null, conversaId: `con_v${n}`, origem: 'assistente' });
  agenda.registrar(visita(1), { tipo: 'lead-vaga', nome_cliente: 'Eduardo Lima', detalhes: 'lancha 24 pés', telefone: '(44) 99911-2233' });
  fixarRelogio('2026-12-17T10:00');
  agenda.registrar(visita(2), { tipo: 'lead-aluguel', nome_cliente: 'Amanda', data: '2026-12-20', detalhes: 'jet, sem habilitação' });
  fixarRelogio('2026-12-18T10:05');
  agenda.registrar(visita(3), { tipo: 'lead-venda', nome_cliente: 'Rogério', detalhes: 'Focker 215' });

  const r = await equipe.rodar('vendas');
  assert.equal(r.criadas, 1, 'o de 17 dias é velho demais e o de hoje ainda é cedo');
  const s = store.sugestoes[0];
  assert.equal(s.tipo, 'retorno');
  assert.match(s.texto, /Olá, Amanda! Aqui é da Marina Remanso\. Você perguntou sobre aluguel para 20\/12/);
  assert.equal(store.registros[0].telefone, '44999112233', 'telefone guardado só com números');
  fixarRelogio('2026-12-19T10:05');
  assert.equal((await equipe.rodar('vendas')).criadas, 1, 'no dia seguinte entra o Rogério');
  assert.match(store.sugestoes[1].texto, /embarcação à venda/);
});

test('gerente e conteúdo: uma vez por semana, com os números da semana anterior', async () => {
  const { store, equipe, descida } = montar({ agora: '2026-12-08T09:00' });
  descida('Carlos', '2026-12-09', '09:00');
  descida('Fernanda', '2026-12-12', '10:00');
  fixarRelogio('2026-12-14T07:00');
  assert.equal(equipe.deveRodar('gerente'), false, 'antes da hora');
  fixarRelogio('2026-12-14T09:10');
  assert.deepEqual((await equipe.tique()).sort(), ['conteudo', 'gerente', 'operacao', 'relacionamento']);
  const resumo = store.sugestoes.find((s) => s.tipo === 'resumo');
  assert.match(resumo.texto, /Resumo da semana \(07\/12 a 13\/12\) · Marina Remanso/);
  assert.match(resumo.texto, /Rampa: 2 descidas agendadas/);
  assert.equal(resumo.para.telefone, '44999000001');
  const ideias = store.sugestoes.find((s) => s.tipo === 'conteudo');
  assert.match(ideias.texto, /1\. Reels.*2\. Carrossel.*3\. Story/s);
  assert.match(ideias.texto, /Jet Sea-Doo/);

  fixarRelogio('2026-12-16T12:00');
  assert.deepEqual((await equipe.tique()).sort(), ['operacao', 'relacionamento', 'vendas'], 'os semanais não repetem; os diários sim');
  fixarRelogio('2026-12-21T09:30');
  assert.equal(equipe.deveRodar('gerente'), true, 'semana nova');
});

test('agente desligado não roda pela agenda', async () => {
  const { store, equipe } = montar({ agora: '2026-12-18T12:00' });
  store.config.agentes.operacao.ativo = false;
  store.config.agentes.vendas.ativo = false;
  const feitos = await equipe.tique();
  assert.ok(!feitos.includes('operacao') && !feitos.includes('vendas'));
  assert.ok(feitos.includes('relacionamento'));
});

test('IA reescreve o texto; se tirar a data ou falhar, vale o texto-modelo', async () => {
  let pedido = null;
  const redigir = async (p) => {
    pedido = p;
    return {
      saida: { textos: p.dados.itens.map((i, n) => ({ chave: i.chave, texto: n === 0 ? `Oi, Carlos! Passando para lembrar que a vaga vence dia ${i.dados.vencimento}. Abraço da Remanso.` : 'Oi! Passando para lembrar da revisão.' })) },
      usage: { input_tokens: 900, output_tokens: 120 },
      model: 'claude-opus-5-5',
    };
  };
  const { store, equipe, cli } = montar({ redigir });
  cli('Paulo').revisaoEm = '2026-12-28';
  const r = await equipe.rodar('relacionamento');
  assert.equal(r.viaIA, true);
  assert.match(pedido.sistema, /Lembrete de vencimento é só lembrete/);
  assert.match(pedido.sistema, /# Ficha da marina/);
  assert.equal(pedido.dados.itens.length, 2);
  const venc = store.sugestoes.find((s) => s.tipo === 'vencimento');
  const rev = store.sugestoes.find((s) => s.tipo === 'revisao');
  assert.match(venc.texto, /Abraço da Remanso/);
  assert.equal(venc.viaIA, true);
  assert.match(rev.texto, /prevista para 28\/12/, 'a IA tirou a data: fica o modelo');
  assert.equal(rev.viaIA, false);
  const uso = store.lerUso();
  assert.equal(uso.length, 1);
  assert.equal(uso[0].agente, 'relacionamento');
  assert.equal(uso[0].usd.toFixed(4), '0.0060');

  const falha = montar({
    redigir: async () => {
      throw new FalhaIA('temporaria', 'Limite de uso da API atingido no momento.');
    },
  });
  const r2 = await falha.equipe.rodar('relacionamento');
  assert.equal(r2.criadas, 1);
  assert.match(r2.erro, /Limite de uso/);
  assert.match(falha.store.sugestoes[0].texto, /Só um lembrete/);
});

test('sugestão é concluída uma vez só, com o texto editado', async () => {
  const { store, equipe } = montar();
  await equipe.rodar('relacionamento');
  const s = store.sugestoes[0];
  const r = equipe.concluir(s.id, { acao: 'feita', texto: 'Texto que eu mandei.', por: 'Ana' });
  assert.equal(r.ok, true);
  assert.equal(s.texto, 'Texto que eu mandei.');
  assert.equal(s.feitaPor, 'Ana');
  assert.equal(equipe.concluir(s.id, { acao: 'descartada', por: 'Ana' }).ok, false);
  assert.equal(equipe.pendentes().length, 0);
  assert.equal(equipe.resumo().find((a) => a.id === 'relacionamento').pendentes, 0);
});

test('configuração antiga ganha os campos da equipe de agentes', () => {
  const { store } = montar();
  delete store.config.agentes;
  store.config.contatos = { dono: '4499' };
  completarConfig(store);
  assert.equal(store.config.agentes.gerente.hora, '07:30');
  assert.equal(store.config.contatos.dono, '4499');
  assert.equal(store.config.contatos.equipe, '');
  assert.equal(store.config.relacionamento.diasSumido, 45);
  assert.equal(store.config.nome, 'Marina Remanso');
});
