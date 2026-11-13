import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { criarStore } from '../lib/store.js';
import { semear } from '../lib/semente.js';
import { criarAgenda } from '../lib/agenda.js';
import { fixarRelogio, normalizarHora, minutosEntre, dataPorExtenso } from '../lib/tempo.js';

function montar() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'marina-'));
  const store = criarStore(dir);
  semear(store, 'exemplo');
  const agenda = criarAgenda(store);
  const por = (nome) => store.clientes.find((c) => c.nome.startsWith(nome));
  return { store, agenda, por, dir };
}

const ctxDe = (cliente, extra = {}) => ({ cliente, conversaId: `con_${cliente ? cliente.id : 'anon'}`, origem: 'assistente', ...extra });

test('tempo: normaliza horas e calcula intervalos', () => {
  assert.equal(normalizarHora('9h'), '09:00');
  assert.equal(normalizarHora('9h30'), '09:30');
  assert.equal(normalizarHora('10:30'), '10:30');
  assert.equal(normalizarHora('25h'), null);
  assert.equal(minutosEntre('2026-12-18', '22:00', '2026-12-19', '08:00'), 600);
  assert.equal(dataPorExtenso('2026-12-19'), 'sábado, 19/12/2026');
});

test('descida simples de cliente cadastrado é confirmada', () => {
  fixarRelogio('2026-12-18T19:10');
  const { agenda, por } = montar();
  const r = agenda.registrar(ctxDe(por('Fernanda')), { tipo: 'descida', data: '2026-12-19', hora: '10:00', detalhes: '2 sacos de gelo' });
  assert.equal(r.ok, true);
  assert.equal(r.status, 'confirmado');
  assert.equal(agenda.janelasDoDia('2026-12-19').find((j) => j.hora === '10:00').ocupadas, 1);
});

test('janela lotada recusa e sugere as vizinhas livres', () => {
  fixarRelogio('2026-12-18T20:30');
  const { agenda, por, store } = montar();
  for (let i = 0; i < 4; i++) {
    const r = agenda.registrar({ cliente: null, conversaId: `v${i}`, origem: 'equipe', forcar: true }, { tipo: 'descida', data: '2026-12-19', hora: '09:00', nome_cliente: `Barco ${i}` });
    assert.equal(r.ok, true);
  }
  const r = agenda.registrar(ctxDe(por('Carlos')), { tipo: 'descida', data: '2026-12-19', hora: '09:00' });
  assert.equal(r.ok, false);
  assert.match(r.erro, /lotada/);
  assert.match(r.erro, /8h30 e 9h30/);
  assert.equal(store.registros.filter((x) => x.clienteNome === 'Carlos Menezes').length, 0);
});

test('antes de a rampa abrir, fora da grade e hora passada são recusados', () => {
  fixarRelogio('2026-12-18T22:15');
  const { agenda, por } = montar();
  const c = ctxDe(por('Paulo'));
  assert.match(agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '07:00' }).erro, /abre às 8h/);
  assert.match(agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '10:15' }).erro, /10h e 10h30/);
  assert.match(agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '17:30' }).erro, /última janela/);
  assert.match(agenda.registrar(c, { tipo: 'descida', data: '2026-12-18', hora: '10:00' }).erro, /já passou/);
});

test('antecedência mínima é contada até o início da janela', () => {
  fixarRelogio('2026-12-19T10:50');
  const { agenda, por } = montar();
  const c = ctxDe(por('Fernanda'));
  const r = agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '11:00' });
  assert.equal(r.ok, false);
  assert.match(r.erro, /Antecedência mínima/);
  assert.match(r.erro, /12h/);
  assert.equal(agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '12:00' }).ok, true);
});

test('link público e cadastro com pendência nunca saem confirmados', () => {
  fixarRelogio('2026-12-19T08:05');
  const { agenda, por } = montar();
  const visitante = agenda.registrar({ cliente: null, conversaId: 'anon1', origem: 'assistente' }, { tipo: 'descida', data: '2026-12-19', hora: '11:00', nome_cliente: 'Renato', embarcacao: 'Dona Lúcia', status: 'confirmado' });
  assert.equal(visitante.status, 'aguardando equipe');
  assert.match(visitante.avisos[0], /link público/);
  const pend = agenda.registrar(ctxDe(por('Marcos')), { tipo: 'descida', data: '2026-12-19', hora: '10:00', status: 'confirmado' });
  assert.equal(pend.status, 'aguardando equipe');
  assert.match(pend.avisos[0], /pendência/);
});

test('alteração, cancelamento e troca de dia', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por } = montar();
  const c = ctxDe(por('Carlos'));
  const d = agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '09:30' });
  const dup = agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '10:00' });
  assert.equal(dup.ok, false);
  assert.match(dup.erro, /alteracao/);
  const alt = agenda.registrar(c, { tipo: 'alteracao', registro_id: d.registro_id, hora: '10:00' });
  assert.equal(alt.ok, true);
  assert.equal(agenda.porId(d.registro_id).hora, '10:00');
  assert.equal(agenda.registrar(c, { tipo: 'cancelamento', registro_id: d.registro_id }).status, 'cancelado');
  assert.equal(agenda.registrar(c, { tipo: 'descida', data: '2026-12-20', hora: '09:00' }).ok, true);
  assert.equal(agenda.ativosDe(c).length, 1);
});

test('um cliente não altera o registro de outro', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por } = montar();
  const d = agenda.registrar(ctxDe(por('Carlos')), { tipo: 'descida', data: '2026-12-19', hora: '09:30' });
  const r = agenda.registrar(ctxDe(por('Paulo')), { tipo: 'cancelamento', registro_id: d.registro_id });
  assert.equal(r.ok, false);
  assert.match(r.erro, /não pertence/);
});

test('subida respeita o limite e liga à descida do dia', () => {
  fixarRelogio('2026-12-19T07:30');
  const { agenda, por } = montar();
  const c = ctxDe(por('Carlos'));
  const d = agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '09:00' });
  fixarRelogio('2026-12-19T16:40');
  const s = agenda.registrar(c, { tipo: 'subida', hora: '17:00' });
  assert.equal(s.ok, true);
  assert.equal(agenda.porId(d.registro_id).voltaPrevista, '17:00');
  assert.match(agenda.registrar(c, { tipo: 'subida', hora: '19:00' }).erro, /limite de subida/);
});

test('reserva de aluguel nasce pré-reserva e respeita as unidades', () => {
  fixarRelogio('2026-12-17T14:00');
  const { agenda } = montar();
  const v = (n) => ({ cliente: null, conversaId: `anon${n}`, origem: 'assistente' });
  const a = agenda.registrar(v(1), { tipo: 'reserva', item_aluguel: 'lancha22', data: '2026-12-19', nome_cliente: 'Ana', status: 'confirmado' });
  assert.equal(a.status, 'pre-reserva');
  const b = agenda.registrar(v(2), { tipo: 'reserva', item_aluguel: 'lancha22', data: '2026-12-19', nome_cliente: 'Bia' });
  assert.equal(b.ok, false);
  assert.match(b.erro, /Sem unidade livre/);
  assert.equal(agenda.registrar(v(2), { tipo: 'reserva', item_aluguel: 'jet', data: '2026-12-19' }).ok, true);
  assert.equal(agenda.registrar(v(3), { tipo: 'reserva', item_aluguel: 'jet', data: '2026-12-19' }).ok, true);
  assert.equal(agenda.registrar(v(4), { tipo: 'reserva', item_aluguel: 'jet', data: '2026-12-19' }).ok, false);
  assert.match(agenda.registrar(v(4), { tipo: 'reserva', item_aluguel: 'iate', data: '2026-12-19' }).erro, /Itens válidos/);
  assert.equal(agenda.confirmarPagamento(a.registro_id, 'Zé').registro.status, 'confirmado');
});

test('turno em rascunho: a mudança só vale depois de confirmada', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por, store } = montar();
  const cli = por('Carlos');
  const d = agenda.registrar(ctxDe(cli), { tipo: 'descida', data: '2026-12-19', hora: '09:30' });
  const t1 = ctxDe(cli, { turnoId: 't1' });
  const alt = agenda.registrar(t1, { tipo: 'alteracao', registro_id: d.registro_id, hora: '10:00' });
  assert.match(alt.resumo, /10h/, 'o turno enxerga a própria mudança');
  agenda.registrar(t1, { tipo: 'servico', detalhes: 'lavagem simples, R$ 80', data: '2026-12-19' });
  assert.equal(agenda.porId(d.registro_id).hora, '09:30', 'para todos os outros, nada mudou ainda');
  assert.equal(agenda.quadro('2026-12-19').descidas[0].hora, '09:30');
  assert.equal(agenda.quadro('2026-12-19').servicos.length, 0, 'rascunho não aparece no quadro');
  assert.equal(agenda.ativosDe(t1).find((x) => x.tipo === 'descida').hora, '10:00');
  assert.equal(agenda.ativosDe(ctxDe(cli))[0].hora, '09:30');

  agenda.descartarTurno('t1');
  assert.equal(agenda.porId(d.registro_id).hora, '09:30');
  assert.equal(agenda.porId(d.registro_id).pendente, undefined);
  assert.equal(store.registros.length, 1);

  const t2 = ctxDe(cli, { turnoId: 't2' });
  agenda.registrar(t2, { tipo: 'cancelamento', registro_id: d.registro_id });
  assert.equal(agenda.porId(d.registro_id).status, 'confirmado', 'cancelamento também espera');
  // No mesmo turno: cancelada a de sábado, pode marcar outra no mesmo dia.
  assert.equal(agenda.registrar(t2, { tipo: 'descida', data: '2026-12-19', hora: '11:00' }).ok, true);
  agenda.confirmarTurno('t2');
  assert.equal(agenda.porId(d.registro_id).status, 'cancelado');
  assert.equal(agenda.porId(d.registro_id).pendente, undefined);
  assert.deepEqual(agenda.quadro('2026-12-19').descidas.map((x) => x.hora), ['11:00']);
});

test('mudança pendente segura a vaga nova sem soltar a antiga', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por, store } = montar();
  store.config.rampa.capacidade = 1;
  const f = agenda.registrar(ctxDe(por('Fernanda')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' });
  const t = ctxDe(por('Fernanda'), { turnoId: 't1' });
  assert.equal(agenda.registrar(t, { tipo: 'alteracao', registro_id: f.registro_id, hora: '11:00' }).ok, true);
  assert.match(agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' }).erro, /lotada/, 'a vaga antiga continua dela');
  assert.match(agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '11:00' }).erro, /lotada/, 'e a nova fica reservada');
  agenda.descartarTurno('t1');
  assert.equal(agenda.janelasDoDia('2026-12-19').find((j) => j.hora === '10:00').ocupadas, 1, 'sem estourar a lotação');
  assert.equal(agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '11:00' }).ok, true);
});

test('equipe mexe num registro com mudança pendente: o rascunho é desfeito e avisado', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por } = montar();
  const invalidados = [];
  agenda.definirAoInvalidar((t) => invalidados.push(t));
  const d = agenda.registrar(ctxDe(por('Carlos')), { tipo: 'descida', data: '2026-12-19', hora: '09:30' });
  agenda.registrar(ctxDe(por('Carlos'), { turnoId: 't9' }), { tipo: 'alteracao', registro_id: d.registro_id, hora: '10:00' });
  assert.equal(agenda.recusar(d.registro_id, 'Zé', 'rampa em manutenção').registro.status, 'cancelado');
  assert.deepEqual(invalidados, ['t9']);
  agenda.descartarTurno('t9');
  assert.equal(agenda.porId(d.registro_id).status, 'cancelado', 'o cancelamento da equipe não volta atrás');
  assert.equal(agenda.porId(d.registro_id).hora, '09:30');
});

test('pedido do link público não segura vaga; liberar confere a lotação', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por, store } = montar();
  store.config.rampa.capacidade = 2;
  const pub = [];
  for (let i = 0; i < 4; i++) pub.push(agenda.registrar({ cliente: null, conversaId: `anon${i}`, origem: 'assistente' }, { tipo: 'descida', data: '2026-12-19', hora: '10:00', nome_cliente: `Fulano ${i}` }));
  assert.ok(pub.every((r) => r.status === 'aguardando equipe'));
  assert.equal(agenda.janelasDoDia('2026-12-19').find((j) => j.hora === '10:00').ocupadas, 0);
  assert.equal(agenda.registrar(ctxDe(por('Carlos')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' }).status, 'confirmado');
  assert.equal(agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' }).status, 'confirmado');
  const p = agenda.pendentes().find((x) => x.id === pub[0].registro_id);
  assert.equal(p.publico, true);
  assert.equal(p.janelaLotada, true);
  const cheio = agenda.liberar(pub[0].registro_id, 'Zé');
  assert.equal(cheio.ok, false);
  assert.equal(cheio.lotada, true);
  assert.equal(agenda.liberar(pub[0].registro_id, 'Zé', { forcar: true }).registro.status, 'confirmado');
  // Cliente da casa com pendência é diferente: o pedido dele segura a vaga.
  const m = agenda.registrar(ctxDe(por('Marcos')), { tipo: 'descida', data: '2026-12-19', hora: '11:00' });
  assert.equal(m.status, 'aguardando equipe');
  assert.equal(agenda.janelasDoDia('2026-12-19').find((j) => j.hora === '11:00').ocupadas, 1);
});

test('pré-reserva vencida solta a unidade, a não ser que tenha chegado comprovante', () => {
  fixarRelogio('2026-12-17T14:00');
  const { agenda } = montar();
  const v = (n) => ({ cliente: null, conversaId: `anon${n}`, origem: 'assistente' });
  const a = agenda.registrar(v(1), { tipo: 'reserva', item_aluguel: 'lancha22', data: '2026-12-19', nome_cliente: 'Ana' });
  fixarRelogio('2026-12-17T15:30');
  assert.equal(agenda.registrar(v(2), { tipo: 'reserva', item_aluguel: 'lancha22', data: '2026-12-19' }).ok, false, 'dentro das 2 horas a unidade é dela');
  fixarRelogio('2026-12-17T16:01');
  assert.equal(agenda.pendentes().find((x) => x.id === a.registro_id).vencida, true);
  const b = agenda.registrar(v(2), { tipo: 'reserva', item_aluguel: 'lancha22', data: '2026-12-19', nome_cliente: 'Bia' });
  assert.equal(b.ok, true, 'venceu sem sinal: outra pessoa pode reservar');
  const tarde = agenda.confirmarPagamento(a.registro_id, 'Carla');
  assert.equal(tarde.ok, false);
  assert.match(tarde.erro, /venceu e Lancha 22 pés com piloto foi reservado por outra pessoa/);

  const c = agenda.registrar(v(3), { tipo: 'reserva', item_aluguel: 'lancha27', data: '2026-12-19', nome_cliente: 'Caio' });
  assert.equal(agenda.marcarComprovante('anon3'), 1);
  fixarRelogio('2026-12-17T19:00');
  assert.equal(agenda.registrar(v(4), { tipo: 'reserva', item_aluguel: 'lancha27', data: '2026-12-19' }).ok, false, 'com comprovante, espera a equipe conferir');
  assert.equal(agenda.confirmarPagamento(c.registro_id, 'Carla').ok, true);
});

test('alteração e serviço passam pelas mesmas conferências de quem registra', () => {
  fixarRelogio('2026-12-19T07:30');
  const { agenda, por } = montar();
  const c = ctxDe(por('Carlos'));
  agenda.registrar(c, { tipo: 'descida', data: '2026-12-19', hora: '09:00' });
  fixarRelogio('2026-12-19T16:40');
  const s = agenda.registrar(c, { tipo: 'subida', hora: '17:00' });
  assert.match(agenda.registrar(c, { tipo: 'alteracao', registro_id: s.registro_id, hora: '19:30' }).erro, /limite de subida/);
  assert.match(agenda.registrar(c, { tipo: 'alteracao', registro_id: s.registro_id, data: 'sábado' }).erro, /Data inválida/);
  assert.equal(agenda.registrar(c, { tipo: 'alteracao', registro_id: s.registro_id, hora: '18:00' }).ok, true);
  assert.match(agenda.registrar(c, { tipo: 'servico', detalhes: 'lavagem', data: 'amanhã cedo' }).erro, /Data inválida/);
  assert.match(agenda.registrar(c, { tipo: 'servico', detalhes: 'lavagem', data: '2026-12-01' }).erro, /já passou/);
  const sv = agenda.registrar(c, { tipo: 'servico', detalhes: 'lavagem simples, R$ 80' });
  assert.equal(agenda.porId(sv.registro_id).data, '2026-12-19');
  assert.match(agenda.registrar(c, { tipo: 'alteracao', registro_id: sv.registro_id, data: '2026-12-10' }).erro, /já passou/);
});

test('mudar a grade da rampa não esconde descidas já marcadas', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por, store } = montar();
  agenda.registrar(ctxDe(por('Carlos')), { tipo: 'descida', data: '2026-12-19', hora: '09:30' });
  agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' });
  assert.equal(agenda.foraDaGrade(), 0);
  store.config.rampa.janelaMin = 20;
  const q = agenda.quadro('2026-12-19');
  assert.deepEqual(q.horas.map((h) => [h.hora, !!h.foraDaGrade]), [['09:30', true], ['10:00', false]]);
  assert.equal(agenda.foraDaGrade(), 1);
});

test('aprovar tarde: descida cujo horário já passou não é confirmada', () => {
  fixarRelogio('2026-12-19T07:30');
  const { agenda, por } = montar();
  agenda.registrar(ctxDe(por('Carlos'), { turnoId: 'tz' }), { tipo: 'descida', data: '2026-12-19', hora: '09:00' });
  assert.equal(agenda.validarTurno('tz'), null);
  fixarRelogio('2026-12-19T09:20');
  assert.match(agenda.validarTurno('tz'), /já passou do horário/);
});

test('rascunho segura a vaga contra outra conversa e some na limpeza de partida', () => {
  fixarRelogio('2026-12-18T21:00');
  const { agenda, por, store } = montar();
  for (let i = 0; i < 3; i++) agenda.registrar({ cliente: null, conversaId: `v${i}`, origem: 'equipe' }, { tipo: 'descida', data: '2026-12-19', hora: '09:00', nome_cliente: `B${i}` });
  assert.equal(agenda.registrar(ctxDe(por('Carlos'), { turnoId: 'tx' }), { tipo: 'descida', data: '2026-12-19', hora: '09:00' }).ok, true);
  assert.equal(agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '09:00' }).ok, false);
  assert.equal(agenda.limparRascunhos(), 1);
  assert.equal(store.registros.length, 3);
  assert.equal(agenda.registrar(ctxDe(por('Paulo')), { tipo: 'descida', data: '2026-12-19', hora: '09:00' }).ok, true);
});

test('equipe libera, recusa e muda etapa', () => {
  fixarRelogio('2026-12-19T08:05');
  const { agenda, por } = montar();
  const p = agenda.registrar(ctxDe(por('Marcos')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' });
  assert.equal(agenda.pendentes().length, 1);
  assert.equal(agenda.mudarEtapa(p.registro_id, 'na_agua', 'Zé').ok, false);
  assert.equal(agenda.liberar(p.registro_id, 'Zé').registro.status, 'confirmado');
  assert.equal(agenda.mudarEtapa(p.registro_id, 'na_agua', 'Zé').registro.etapa, 'na_agua');
  assert.equal(agenda.pendentes().length, 0);
});

test('dados sobrevivem a reabrir a pasta', () => {
  fixarRelogio('2026-12-18T19:10');
  const { agenda, por, store, dir } = montar();
  agenda.registrar(ctxDe(por('Fernanda')), { tipo: 'descida', data: '2026-12-19', hora: '10:00' });
  store.descarregar();
  const outro = criarStore(dir);
  assert.equal(outro.registros.length, 1);
  assert.equal(outro.config.nome, 'Marina Remanso');
  assert.equal(outro.clientes.length, 4);
});
