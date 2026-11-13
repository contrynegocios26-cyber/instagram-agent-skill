import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

process.env.IA_FAKE = '1';
process.env.IA_ESPERA_MS = '0';
process.env.ESPERA_LONGA_MS = '200';
process.env.PAINEL_SENHA = 'senha-equipe';
process.env.ADMIN_SENHA = 'senha-admin';

const { criarApp } = await import('../lib/app.js');
const { fixarRelogio } = await import('../lib/tempo.js');

async function subir() {
  fixarRelogio(null);
  const ctx = criarApp({ dir: fs.mkdtempSync(path.join(os.tmpdir(), 'marina-http-')), semente: 'exemplo' });
  const servidor = await new Promise((r) => {
    const s = ctx.app.listen(0, () => r(s));
  });
  const base = `http://localhost:${servidor.address().port}`;
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
    const tipo = r.headers.get('content-type') || '';
    return { status: r.status, dados: tipo.includes('json') ? await r.json() : null, headers: r.headers };
  };
  const entrar = async (senha, nome = 'Teste') => {
    const r = await pedir('POST', '/api/painel/login', { corpo: { senha, nome } });
    return r.headers.get('set-cookie')?.split(';')[0] || null;
  };
  const sessao = async (corpo = {}) => (await pedir('POST', '/api/chat/sessao', { corpo })).dados;
  return { ...ctx, base, pedir, entrar, sessao, fechar: () => servidor.close() };
}

test('painel exige login, papel certo e cabeçalho próprio', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  assert.equal((await s.pedir('GET', '/api/painel/estado')).status, 401);
  assert.equal((await s.pedir('GET', '/api/painel/admin')).status, 401);
  assert.equal(await s.entrar('errada'), null);

  const equipe = await s.entrar('senha-equipe', 'Zé');
  assert.equal((await s.pedir('GET', '/api/painel/estado', { cookie: equipe })).status, 200);
  for (const [m, c] of [['GET', '/api/painel/admin'], ['GET', '/api/painel/exportar'], ['GET', '/api/painel/relatorio'], ['PUT', '/api/painel/ficha'], ['POST', '/api/painel/cliente']]) {
    assert.equal((await s.pedir(m, c, { cookie: equipe, corpo: m === 'GET' ? undefined : {} })).status, 403, `${m} ${c}`);
  }
  assert.equal((await s.pedir('POST', '/api/painel/modo', { cookie: equipe, corpo: { modo: 'auto' } })).status, 403);
  assert.equal((await s.pedir('POST', '/api/painel/modo', { cookie: equipe, corpo: { modo: 'desligado' } })).status, 200);
  assert.equal((await s.pedir('POST', '/api/painel/modo', { cookie: equipe, corpo: { modo: 'sombra' }, painel: false })).status, 400, 'sem X-Painel');

  const admin = await s.entrar('senha-admin');
  assert.equal((await s.pedir('POST', '/api/painel/modo', { cookie: admin, corpo: { modo: 'auto' } })).status, 200);
  const exp = await s.pedir('GET', '/api/painel/exportar', { cookie: admin });
  assert.equal(exp.status, 200);
  assert.ok(exp.dados.clientes.every((c) => c.token === undefined), 'exportação não leva os links pessoais');
  assert.equal((await s.pedir('GET', '/api/painel/estado', { cookie: 'painel=forjado.abc' })).status, 401);
});

test('cabeçalhos de segurança e páginas', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const r = await fetch(`${s.base}/`);
  assert.equal(r.status, 200);
  assert.match(r.headers.get('content-security-policy'), /default-src 'self'/);
  assert.equal(r.headers.get('x-content-type-options'), 'nosniff');
  assert.equal(r.headers.get('referrer-policy'), 'no-referrer');
  assert.equal((await fetch(`${s.base}/painel`)).status, 200);
  assert.equal((await fetch(`${s.base}/../lib/app.js`)).status, 404);
  assert.equal((await fetch(`${s.base}/api/nada`)).status, 404);
  assert.equal((await fetch(`${s.base}/saude`)).status, 200);
});

test('chat: chave obrigatória, texto validado e limite de mensagens', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'oi' } })).status, 401);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'oi' }, chave: 'abc.def' })).status, 401);
  const v = await s.sessao();
  assert.equal(v.cliente, null);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: '   ' }, chave: v.chave })).status, 400);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { corpo: {}, chave: v.chave })).status, 400);
  const longo = await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'a'.repeat(5000) }, chave: v.chave });
  assert.equal(longo.status, 200);
  const conversa = [...s.store.conversas.values()].find((c) => c.mensagens.length);
  assert.equal(conversa.mensagens[0].texto.length, 1200);
  let ultimo;
  for (let i = 0; i < 20; i++) ultimo = await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: `m${i}` }, chave: v.chave });
  assert.equal(ultimo.status, 429);
  await s.atendente.ocioso();
});

test('conversa anônima é retomada pela chave; a de cadastro só pelo link', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const a = await s.sessao();
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'boa tarde' }, chave: a.chave });
  const b = await s.sessao({ chave: a.chave });
  assert.equal(b.mensagens[0].texto, 'boa tarde');

  const cli = s.store.clientes[0];
  const c = await s.sessao({ token: cli.token });
  assert.equal(c.cliente.primeiroNome, 'Carlos');
  const semToken = await s.sessao({ chave: c.chave });
  assert.equal(semToken.cliente, null, 'chave de cadastro não abre sessão sem o link');
  assert.equal((await s.pedir('POST', '/api/chat/sessao', { corpo: { token: 'inventado' } })).status, 404);
  await s.atendente.ocioso();
});

test('trocar o link pessoal derruba o link e as sessões antigas', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  const cli = s.store.clientes[0];
  const antigo = cli.token;
  const ses = await s.sessao({ token: antigo });
  assert.equal((await s.pedir('GET', '/api/chat/novas?depois=&d=0&r=', { chave: ses.chave })).status, 200);
  const r = await s.pedir('PUT', `/api/painel/cliente/${cli.id}`, { cookie: admin, corpo: { nome: cli.nome, novoLink: true } });
  assert.equal(r.status, 200);
  assert.notEqual(cli.token, antigo);
  assert.equal((await s.pedir('POST', '/api/chat/sessao', { corpo: { token: antigo } })).status, 404);
  assert.equal((await s.pedir('GET', '/api/chat/novas?depois=&d=0&r=', { chave: ses.chave })).status, 401);
  assert.equal((await s.sessao({ token: cli.token })).cliente.primeiroNome, 'Carlos');
});

test('foto: só imagem de verdade, e só o dono e a equipe veem', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const dono = await s.sessao();
  const outro = await s.sessao();
  const jpg = Buffer.concat([Buffer.from([0xff, 0xd8, 0xff, 0xe0]), Buffer.alloc(300, 1)]).toString('base64');
  const falso = Buffer.from('<script>alert(1)</script>'.repeat(10)).toString('base64');
  assert.equal((await s.pedir('POST', '/api/chat/foto', { corpo: { dados: `data:image/jpeg;base64,${falso}` }, chave: dono.chave })).status, 400);
  assert.equal((await s.pedir('POST', '/api/chat/foto', { corpo: { dados: `data:text/html;base64,${falso}` }, chave: dono.chave })).status, 400);
  assert.equal((await s.pedir('POST', '/api/chat/foto', { corpo: { dados: `data:image/jpeg;base64,${jpg}` } })).status, 401);
  assert.equal((await s.pedir('POST', '/api/chat/foto', { corpo: { dados: `data:image/jpeg;base64,${jpg}` }, chave: dono.chave })).status, 200);
  const novas = await s.pedir('GET', '/api/chat/novas?depois=&d=0&r=', { chave: dono.chave });
  const url = novas.dados.mensagens.find((m) => m.tipo === 'foto').foto;
  const ver = (k) => fetch(`${s.base}${url}?k=${encodeURIComponent(k)}`);
  const ok = await ver(dono.chave);
  assert.equal(ok.status, 200);
  assert.equal(ok.headers.get('content-type'), 'image/jpeg');
  assert.equal((await ver(outro.chave)).status, 404);
  assert.equal((await ver('')).status, 404);
  const nome = url.split('/').pop();
  assert.equal((await fetch(`${s.base}/api/painel/foto/${nome}`)).status, 401);
  const equipe = await s.entrar('senha-equipe');
  assert.equal((await fetch(`${s.base}/api/painel/foto/${nome}`, { headers: { Cookie: equipe } })).status, 200);
  assert.equal((await fetch(`${s.base}/api/painel/foto/..%2Fconfig.json`, { headers: { Cookie: equipe } })).status, 404);
  await s.atendente.ocioso();
});

test('espera longa devolve na hora quando chega mensagem e sozinha quando não chega', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const v = await s.sessao();
  const t0 = Date.now();
  const vazio = await s.pedir('GET', '/api/chat/novas?espera=1&depois=&d=0&r=', { chave: v.chave });
  assert.ok(Date.now() - t0 >= 150, 'esperou o tempo limite');
  assert.equal(vazio.dados.mensagens.length, 0);
  const espera = s.pedir('GET', '/api/chat/novas?espera=1&depois=&d=0&r=', { chave: v.chave });
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'oi' }, chave: v.chave });
  assert.equal((await espera).dados.mensagens[0].texto, 'oi');
  await s.atendente.ocioso();
});

test('configuração inválida é recusada e a válida entra no prompt', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  const v1 = s.atendente.prompt().versao;
  const ruim = await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { itensAluguel: [{ id: 'Jet Ski!', nome: 'Jet', unidades: 1 }] } });
  assert.equal(ruim.status, 400);
  const invertido = await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { rampa: { abre: '18:00', ultimaDescida: '09:00' } } });
  assert.equal(invertido.status, 400);
  const bom = await s.pedir('PUT', '/api/painel/config', { cookie: admin, corpo: { rampa: { capacidade: 6 }, itensAluguel: [{ id: 'pontoon', nome: 'Pontoon', unidades: 2 }] } });
  assert.equal(bom.status, 200);
  assert.equal(s.store.config.rampa.capacidade, 6);
  assert.equal(s.store.config.rampa.abre, '08:00', 'campo ausente mantém o valor');
  assert.match(s.atendente.prompt().sistema, /id "pontoon", 2 unidade/);
  assert.notEqual(s.atendente.prompt().versao, v1);
  assert.equal((await s.pedir('PUT', '/api/painel/ficha', { cookie: admin, corpo: { ficha: 'x'.repeat(40001) } })).status, 400);
});

test('excluir cliente apaga conversa e foto e tira o nome dos registros', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin');
  await s.pedir('POST', '/api/painel/modo', { cookie: admin, corpo: { modo: 'auto' } });
  const cli = s.store.clientes.find((c) => c.nome.startsWith('Fernanda'));
  const ses = await s.sessao({ token: cli.token });
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'desce amanhã 10h' }, chave: ses.chave });
  await s.atendente.ocioso();
  assert.equal(s.store.registros.length, 1);
  assert.equal((await s.pedir('DELETE', `/api/painel/cliente/${cli.id}`, { cookie: admin, corpo: {} })).status, 200);
  assert.equal(s.store.conversas.size, 0);
  assert.equal(s.store.registros[0].clienteNome, 'Cliente removido');
  assert.equal(s.store.registros[0].clienteId, null);
  assert.equal((await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'oi' }, chave: ses.chave })).status, 401);
});

test('muitas senhas erradas bloqueiam novas tentativas', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  let r;
  for (let i = 0; i < 9; i++) r = await s.pedir('POST', '/api/painel/login', { corpo: { senha: `x${i}`, nome: 'a' } });
  assert.equal(r.status, 429);
  assert.equal((await s.pedir('POST', '/api/painel/login', { corpo: { senha: 'senha-admin', nome: 'a' } })).status, 429);
});

test('equipe: libera pedido pendente, confirma pagamento, lança reserva e o cliente é avisado', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin', 'Ana');
  await s.pedir('POST', '/api/painel/modo', { cookie: admin, corpo: { modo: 'auto' } });

  // Cliente com pendência pede descida: fica aguardando a equipe.
  const marcos = s.store.clientes.find((c) => c.nome.startsWith('Marcos'));
  const ses = await s.sessao({ token: marcos.token });
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'desce o jet amanhã 10h' }, chave: ses.chave });
  await s.atendente.ocioso();
  let estado = (await s.pedir('GET', '/api/painel/estado', { cookie: admin })).dados;
  assert.equal(estado.pendentes.length, 1);
  assert.equal(estado.pendentes[0].status, 'aguardando equipe');
  assert.equal(estado.pendentes[0].telefone, marcos.telefone);
  const id = estado.pendentes[0].id;

  assert.equal((await s.pedir('POST', `/api/painel/registro/${id}/acao`, { cookie: admin, corpo: { acao: 'na_agua' } })).status, 409, 'não vai para a água antes de liberar');
  const lib = await s.pedir('POST', `/api/painel/registro/${id}/acao`, { cookie: admin, corpo: { acao: 'liberar' } });
  assert.equal(lib.status, 200);
  let novas = (await s.pedir('GET', '/api/chat/novas?depois=&d=0&r=', { chave: ses.chave })).dados;
  assert.match(novas.mensagens.at(-1).texto, /A equipe confirmou: descida de Jet "MT-07" em .* às 10h\./);
  assert.equal(novas.registros[0].status, 'confirmado');
  assert.equal((await s.pedir('POST', `/api/painel/registro/${id}/acao`, { cookie: admin, corpo: { acao: 'liberar' } })).status, 409, 'já liberado');

  // Cancelar com motivo, sem avisar.
  const antes = novas.mensagens.length;
  const canc = await s.pedir('POST', `/api/painel/registro/${id}/acao`, { cookie: admin, corpo: { acao: 'cancelar', motivo: 'teste', avisar: false } });
  assert.equal(canc.status, 200);
  novas = (await s.pedir('GET', '/api/chat/novas?depois=&d=0&r=', { chave: ses.chave })).dados;
  assert.equal(novas.mensagens.length, antes, 'sem aviso quando a equipe desmarca a caixa');
  assert.equal(novas.registros.length, 0);

  // Reserva lançada pela equipe e pagamento de pré-reserva feita pelo assistente.
  const hoje = estado.agora.data;
  const manual = await s.pedir('POST', '/api/painel/registro', { cookie: admin, corpo: { tipo: 'reserva', nome: 'Seu Jorge', item: 'lancha22', data: hoje, detalhes: '6 pessoas' } });
  assert.equal(manual.status, 200);
  assert.equal(manual.dados.status, 'confirmado');
  const repetida = await s.pedir('POST', '/api/painel/registro', { cookie: admin, corpo: { tipo: 'reserva', nome: 'Outro', item: 'lancha22', data: hoje } });
  assert.equal(repetida.status, 409);
  assert.match(repetida.dados.erro, /Sem unidade livre/);
  assert.equal((await s.pedir('POST', '/api/painel/registro', { cookie: admin, corpo: { tipo: 'descida', data: hoje, hora: '10h' } })).status, 400, 'sem cliente nem nome');

  const v = await s.sessao();
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'quero o jet hoje, pode reservar' }, chave: v.chave });
  await s.atendente.ocioso();
  const pre = s.store.registros.find((r) => r.tipo === 'reserva' && r.status === 'pre-reserva');
  assert.ok(pre, 'pré-reserva criada pelo assistente');
  const pago = await s.pedir('POST', `/api/painel/registro/${pre.id}/acao`, { cookie: admin, corpo: { acao: 'pagamento' } });
  assert.equal(pago.status, 200);
  const doVisitante = (await s.pedir('GET', '/api/chat/novas?depois=&d=0&r=', { chave: v.chave })).dados;
  assert.match(doVisitante.mensagens.at(-1).texto, /Pagamento confirmado: reserva de Jet Sea-Doo .* está garantida\./);

  estado = (await s.pedir('GET', '/api/painel/estado', { cookie: admin })).dados;
  assert.equal(estado.quadro.aluguel.find((i) => i.id === 'lancha22').livres, 0);
  assert.equal(estado.quadro.aluguel.find((i) => i.id === 'jet').livres, 1);
});

test('equipe: aviso do dia, assumir e devolver conversa, QR e relatório', async (t) => {
  const s = await subir();
  t.after(s.fechar);
  const admin = await s.entrar('senha-admin', 'Ana');
  await s.pedir('POST', '/api/painel/modo', { cookie: admin, corpo: { modo: 'auto' } });

  await s.pedir('POST', '/api/painel/aviso', { cookie: admin, corpo: { texto: 'Rio baixo: cuidado com os bancos de areia.' } });
  const v = await s.sessao();
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'boa tarde' }, chave: v.chave });
  await s.atendente.ocioso();
  const conversa = [...s.store.conversas.values()].find((c) => c.mensagens.length);
  assert.match(conversa.thread.apiMessages[1].content, /Aviso do dia \(atualizado em .*\): Rio baixo/);

  assert.equal((await s.pedir('POST', `/api/painel/conversa/${conversa.id}/estado`, { cookie: admin, corpo: { estado: 'humano' } })).status, 200);
  await s.pedir('POST', '/api/chat/enviar', { corpo: { texto: 'tem alguém aí?' }, chave: v.chave });
  await s.atendente.ocioso();
  let fio = (await s.pedir('GET', `/api/painel/conversa/${conversa.id}`, { cookie: admin })).dados;
  assert.equal(fio.mensagens.at(-1).texto, 'tem alguém aí?', 'IA parada com a equipe na conversa');
  assert.equal((await s.pedir('POST', `/api/painel/conversa/${conversa.id}/estado`, { cookie: admin, corpo: { estado: 'ia' } })).status, 200);
  await s.atendente.ocioso();
  fio = (await s.pedir('GET', `/api/painel/conversa/${conversa.id}`, { cookie: admin })).dados;
  assert.equal(fio.mensagens.at(-1).de, 'assistente', 'devolvida, a IA responde o que ficou pendente');
  assert.equal((await s.pedir('POST', `/api/painel/conversa/${conversa.id}/estado`, { cookie: admin, corpo: { estado: 'outro' } })).status, 400);
  assert.equal((await s.pedir('POST', '/api/painel/conversa/con_nao_existe/responder', { cookie: admin, corpo: { texto: 'oi' } })).status, 404);

  const qr = await fetch(`${s.base}/api/painel/qr?u=${encodeURIComponent(`${s.base}/`)}`, { headers: { Cookie: admin } });
  assert.equal(qr.status, 200);
  assert.match(qr.headers.get('content-type'), /svg/);
  assert.equal((await fetch(`${s.base}/api/painel/qr?u=${encodeURIComponent('https://outro.site/')}`, { headers: { Cookie: admin } })).status, 400);

  const rel = (await s.pedir('GET', '/api/painel/relatorio', { cookie: admin })).dados;
  assert.equal(rel.conversas, 1);
  assert.equal(rel.mensagensCliente, 2);
  assert.equal(rel.respostasAssistente >= 2, true);
  assert.equal(rel.ia.chamadas >= 2, true);
  assert.equal(rel.ia.usd, null, 'modelo de roteiro não tem preço');

  assert.equal((await s.pedir('DELETE', `/api/painel/conversa/${conversa.id}`, { cookie: admin, corpo: {} })).status, 200);
  assert.equal(s.store.conversas.has(conversa.id), false);
});
