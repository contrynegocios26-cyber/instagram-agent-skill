// Teste de ponta a ponta no navegador, com o modelo de roteiro (sem custo).
// Uso: node test/e2e.mjs            (gera também as telas em docs/telas)
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

// O Playwright vem instalado no ambiente, fora do projeto.
const { chromium } = createRequire(import.meta.url)('playwright');

process.env.IA_FAKE = '1';
process.env.IA_ESPERA_MS = '150';
process.env.PAINEL_SENHA = 'equipe-teste';
process.env.ADMIN_SENHA = 'admin-teste';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const telas = path.join(aqui, '..', 'docs', 'telas');
const { criarApp } = await import('../lib/app.js');
const { agora, somarDias } = await import('../lib/tempo.js');
const { app, store, atendente } = criarApp({ dir: fs.mkdtempSync(path.join(os.tmpdir(), 'marina-e2e-')), semente: 'exemplo' });
const servidor = await new Promise((r) => {
  const s = app.listen(0, () => r(s));
});
const base = `http://localhost:${servidor.address().port}`;
const fernanda = store.clientes.find((c) => c.nome.startsWith('Fernanda'));

const navegador = await chromium.launch();
const erros = [];
const vigiar = (pagina, nome) => {
  pagina.on('pageerror', (e) => erros.push(`${nome}: ${e.message}`));
  pagina.on('console', (m) => m.type() === 'error' && !/401|409/.test(m.text()) && erros.push(`${nome} console: ${m.text()}`));
};
const passos = [];
let novo = null; // segundo visitante, aberto já no modo automático
const passo = async (nome, fn) => {
  await fn();
  passos.push(nome);
  console.log(`ok - ${nome}`);
};

try {
  // ---------- cliente no celular ----------
  const celular = await navegador.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: 'pt-BR' });
  const chat = await celular.newPage();
  vigiar(chat, 'chat');
  await chat.goto(`${base}/c/${fernanda.token}`);

  await passo('chat abre com o nome do cliente e os atalhos', async () => {
    await chat.getByText('Olá, Fernanda!').waitFor();
    await chat.getByRole('button', { name: 'Quero descer meu barco' }).waitFor();
    assert.equal(await chat.locator('#marina').textContent(), 'Marina Remanso');
  });

  await passo('cliente pede a descida e vê "digitando" (modo sombra)', async () => {
    await chat.getByLabel('Mensagem', { exact: true }).fill('desce a aquarela amanhã 10h com gelo');
    await chat.getByRole('button', { name: 'Enviar mensagem' }).click();
    await chat.locator('.balao.meu', { hasText: 'desce a aquarela' }).waitFor();
    await chat.locator('#digitando').waitFor();
  });

  // ---------- equipe no computador ----------
  const mesa = await navegador.newContext({ viewport: { width: 1280, height: 860 }, deviceScaleFactor: 2, locale: 'pt-BR' });
  const painel = await mesa.newPage();
  vigiar(painel, 'painel');
  await painel.goto(`${base}/painel`);

  await passo('painel recusa senha errada e aceita a certa', async () => {
    await painel.getByLabel('Seu nome').fill('Ana');
    await painel.getByLabel('Senha').fill('errada');
    await painel.getByRole('button', { name: 'Entrar' }).click();
    await painel.getByText('Senha incorreta.').waitFor();
    await painel.getByLabel('Senha').fill('admin-teste');
    await painel.getByRole('button', { name: 'Entrar' }).click();
    await painel.getByRole('button', { name: /Atendente: Sombra/ }).waitFor();
  });

  await passo('resposta do assistente espera aprovação, com a ação listada', async () => {
    await painel.getByRole('button', { name: /^Aprovar/ }).click();
    await painel.getByText('desce a aquarela amanhã 10h com gelo').waitFor();
    await painel.getByText(/descida .* 10h \(gelo\), confirmado/).waitFor();
    await painel.screenshot({ path: path.join(telas, 'painel-aprovar.png') });
    assert.equal(store.registros[0].rascunho !== undefined, true);
  });

  await passo('equipe edita, aprova e o cliente recebe', async () => {
    await painel.getByLabel(/Resposta do assistente/).fill('Confirmado, Fernanda: Aquarela amanhã às 10h, com gelo.');
    await painel.getByRole('button', { name: 'Aprovar e enviar' }).click();
    await chat.locator('.balao', { hasText: 'Confirmado, Fernanda: Aquarela amanhã às 10h' }).waitFor();
    await chat.locator('#agenda .item', { hasText: 'descida' }).waitFor();
    assert.equal(store.registros[0].rascunho, undefined);
    assert.equal(store.registros[0].status, 'confirmado');
    await chat.screenshot({ path: path.join(telas, 'chat-cliente.png') });
  });

  await passo('quadro da rampa mostra a descida e "Na água" avisa o cliente', async () => {
    await painel.getByRole('button', { name: /^Rampa/ }).click();
    await painel.getByRole('button', { name: '▶' }).click();
    await painel.locator('.barco', { hasText: 'Aquarela' }).waitFor();
    await painel.screenshot({ path: path.join(telas, 'painel-rampa.png') });
    await painel.getByRole('button', { name: 'Na água' }).click();
    await chat.locator('.balao.sistema', { hasText: 'está na água' }).waitFor();
    await chat.locator('#agenda .selo', { hasText: 'na água' }).waitFor();
  });

  await passo('lançamento manual respeita a lotação e aceita encaixe', async () => {
    await painel.getByRole('button', { name: '+ Lançar manualmente' }).click();
    await painel.locator('#dlg').getByLabel('Nome', { exact: true }).fill('Seu Jorge');
    await painel.locator('#dlg').getByLabel('Embarcação', { exact: true }).fill('Lancha Maré');
    await painel.locator('#dlg').getByLabel('Hora', { exact: true }).fill('7h');
    await painel.getByRole('button', { name: 'Lançar', exact: true }).click();
    await painel.getByText(/A rampa abre às 8h/).waitFor();
    await painel.getByRole('button', { name: 'Ok' }).click();
    await painel.getByRole('button', { name: '+ Lançar manualmente' }).click();
    await painel.locator('#dlg').getByLabel('Nome', { exact: true }).fill('Seu Jorge');
    await painel.locator('#dlg').getByLabel('Embarcação', { exact: true }).fill('Lancha Maré');
    await painel.locator('#dlg').getByLabel('Hora', { exact: true }).fill('10h');
    await painel.getByRole('button', { name: 'Lançar', exact: true }).click();
    await painel.locator('.barco', { hasText: 'Lancha Maré' }).waitFor();
  });

  // ---------- visitante ----------
  const outro = await navegador.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: 'pt-BR' });
  const visita = await outro.newPage();
  vigiar(visita, 'visitante');
  await visita.goto(base);

  await passo('visitante pede desconto: vira chamado para a equipe depois de aprovado', async () => {
    await visita.getByRole('button', { name: 'Quero alugar lancha ou jet' }).waitFor();
    await visita.getByLabel('Mensagem', { exact: true }).fill('quero um desconto na lancha');
    await visita.getByRole('button', { name: 'Enviar mensagem' }).click();
    await painel.getByRole('button', { name: /^Aprovar/ }).click();
    await painel.locator('.citacao', { hasText: 'quero um desconto na lancha' }).waitFor();
    assert.equal(store.chamados.filter((c) => !c.rascunho).length, 0, 'chamado ainda em rascunho');
    await painel.getByRole('button', { name: 'Aprovar e enviar' }).click();
    await visita.locator('.balao', { hasText: 'já chamei a equipe' }).waitFor();
    await painel.getByRole('button', { name: /^Chamados/ }).click();
    await painel.getByText('Para: Sandra (gerência)').waitFor();
  });

  await passo('emergência: telefones na hora e alerta vermelho no painel', async () => {
    await visita.getByLabel('Mensagem', { exact: true }).fill('socorro, o barco está à deriva perto da ilha');
    await visita.getByRole('button', { name: 'Enviar mensagem' }).click();
    await visita.locator('.balao.emergencia', { hasText: '185' }).waitFor();
    assert.equal(await visita.locator('.balao.emergencia a[href="tel:185"]').count(), 1);
    await painel.locator('.faixa.emergencia').waitFor();
    await painel.locator('.chamado.emergencia').first().waitFor();
    await visita.screenshot({ path: path.join(telas, 'chat-emergencia.png') });
    await painel.screenshot({ path: path.join(telas, 'painel-chamados.png') });
  });

  await passo('equipe assume a conversa e o cliente vê quem respondeu', async () => {
    await painel.getByRole('button', { name: /^Conversas/ }).click();
    await painel.locator('.lista button', { hasText: 'Fernanda Rocha' }).click();
    await painel.getByLabel('Responder como equipe').fill('Oi, Fernanda! Aqui é a Ana. Qualquer coisa me chama.');
    await painel.getByRole('button', { name: 'Enviar', exact: true }).click();
    await chat.locator('.balao .quem', { hasText: 'Equipe · Ana' }).waitFor();
    await chat.getByText('Equipe da marina na conversa').waitFor();
    await painel.getByText('Equipe na conversa').waitFor();
    await painel.screenshot({ path: path.join(telas, 'painel-conversa.png') });
    await chat.getByLabel('Mensagem', { exact: true }).fill('obrigada!');
    await chat.getByRole('button', { name: 'Enviar mensagem' }).click();
    await painel.locator('.msgs .balao.cliente', { hasText: 'obrigada!' }).waitFor();
    await atendente.ocioso();
    assert.equal(store.rascunhos.filter((r) => r.conversaId === atendente.conversaDoCliente(fernanda).id).length, 0, 'IA parada com a equipe na conversa');
  });

  await passo('foto do cliente aparece no chat dele e no painel, por endereço próprio', async () => {
    const imagem = await chat.screenshot(); // um PNG de verdade, do tamanho de uma foto de celular
    await chat.locator('#arquivo').setInputFiles({ name: 'casco.png', mimeType: 'image/png', buffer: imagem });
    const noChat = chat.locator('.balao.meu:not(.enviando) img');
    await noChat.waitFor();
    const src = await noChat.getAttribute('src');
    assert.match(src, /^\/api\/chat\/foto\/foto_[0-9a-f]+\.jpg\?f=/, 'endereço assinado só para esta foto');
    assert.ok(!/[?&]k=/.test(src), 'a chave da sessão não vai no endereço');
    // A imagem é procurada de novo a cada tentativa: o painel redesenha a tela quando chega novidade.
    const carregou = (seletor) => {
      const i = document.querySelector(seletor);
      if (!i) return false;
      i.scrollIntoView({ block: 'nearest' });
      return i.complete && i.naturalWidth > 0;
    };
    await chat.waitForFunction(carregou, '.balao.meu:not(.enviando) img');
    await painel.waitForFunction(carregou, '.msgs img');
    // Sem a assinatura a foto não abre (o servidor responde como se não existisse).
    const arquivo = src.split('?')[0];
    assert.equal((await chat.request.get(base + arquivo)).status(), 404);
    assert.equal((await chat.request.get(`${base + arquivo}?f=${encodeURIComponent('a.b')}`)).status(), 404);
    assert.equal((await outro.request.get(base + src)).status(), 200, 'o endereço assinado abre a foto, e só ela');
  });

  await passo('administração: clientes, configuração e relatório abrem', async () => {
    await painel.getByRole('button', { name: 'Clientes' }).click();
    await painel.getByText('Link público').waitFor();
    await painel.getByRole('cell', { name: /Carlos Menezes/ }).waitFor();
    await painel.screenshot({ path: path.join(telas, 'painel-clientes.png') });
    await painel.getByRole('button', { name: 'Configuração' }).click();
    await painel.getByLabel('Embarcações por janela').waitFor();
    assert.equal(await painel.getByLabel('Embarcações por janela').inputValue(), '4');
    assert.equal(await painel.getByLabel('Fuso horário da marina').inputValue(), 'America/Sao_Paulo');
    await painel.getByLabel('Embarcações por janela').fill('5');
    await painel.getByRole('button', { name: 'Salvar configuração' }).first().click();
    await painel.getByText('Configuração salva.').waitFor();
    await painel.getByRole('button', { name: 'Ok' }).click();
    assert.equal(store.config.rampa.capacidade, 5);
    await painel.getByRole('button', { name: 'Relatório' }).click();
    await painel.getByText('descidas agendadas').waitFor();
    await painel.screenshot({ path: path.join(telas, 'painel-relatorio.png'), fullPage: true });
  });

  await passo('agentes: resumo do dia sai na hora e a sugestão é marcada como enviada', async () => {
    await painel.getByRole('button', { name: /^Agentes/ }).click();
    await painel.getByText('Equipe de agentes').waitFor();
    await painel.locator('.cartao', { hasText: 'Resumo do dia para a equipe da rampa' }).getByRole('button', { name: 'Rodar agora' }).click();
    await painel.getByText('1 sugestão(ões) preparada(s).').waitFor();
    await painel.getByRole('button', { name: 'Ok' }).click();
    await painel.getByLabel('Texto da sugestão').waitFor();
    assert.match(await painel.getByLabel('Texto da sugestão').inputValue(), /Rampa de .* · Marina Remanso/);
    await painel.locator('.cartao', { hasText: 'Lembretes de vencimento' }).getByRole('button', { name: 'Rodar agora' }).click();
    await painel.locator('#dlg').getByRole('button', { name: 'Ok' }).click();
    await painel.screenshot({ path: path.join(telas, 'painel-agentes.png'), fullPage: true });
    await painel.locator('.cartao', { hasText: 'Resumo da rampa de' }).getByRole('button', { name: 'Marcar como enviada' }).click();
    await painel.locator('.cartao', { hasText: 'Resumo da rampa de' }).waitFor({ state: 'detached' });
    assert.equal(store.sugestoes.find((s) => s.tipo === 'briefing').status, 'feita');
  });

  await passo('modo automático: o assistente responde sem aprovação', async () => {
    await painel.getByRole('button', { name: /Atendente: Sombra/ }).click();
    await painel.getByText('Automático', { exact: true }).click();
    await painel.getByRole('button', { name: 'Salvar', exact: true }).click();
    await painel.getByRole('button', { name: /Atendente: Automático/ }).waitFor();
    novo = await (await navegador.newContext({ viewport: { width: 390, height: 780 }, locale: 'pt-BR' })).newPage();
    vigiar(novo, 'visitante2');
    await novo.goto(base);
    await novo.getByLabel('Mensagem', { exact: true }).fill('boa tarde');
    await novo.getByRole('button', { name: 'Enviar mensagem' }).click();
    await novo.locator('.balao', { hasText: 'assistente virtual da marina' }).first().waitFor();
  });

  const amanha = somarDias(agora().data, 1);

  await passo('descida pedida pelo link público espera a equipe, com aviso para conferir quem é', async () => {
    await novo.getByLabel('Mensagem', { exact: true }).fill('desce a dona lúcia amanhã 9h');
    await novo.getByRole('button', { name: 'Enviar mensagem' }).click();
    await novo.locator('#agenda .selo', { hasText: 'aguardando a equipe' }).waitFor();
    const pedido = store.registros.find((r) => r.tipo === 'descida' && r.hora === '09:00' && r.data === amanha);
    assert.equal(pedido.status, 'aguardando equipe');
    assert.equal(pedido.publico, true);
    await painel.getByRole('button', { name: /^Rampa/ }).click();
    // O pedido aparece na fila de decisão e, como o quadro está em amanhã, na janela das 9h.
    const cartao = painel.locator('.barco', { hasText: 'link público: confirme quem é' }).first();
    await cartao.waitFor();
    assert.equal(await painel.locator('.barco', { hasText: 'link público: confirme quem é' }).count(), 2);
    await painel.screenshot({ path: path.join(telas, 'painel-link-publico.png') });
    await cartao.getByRole('button', { name: 'Liberar', exact: true }).click();
    await painel.locator('#dlg').getByText('O sistema não sabe quem escreveu', { exact: false }).waitFor();
    assert.equal(pedido.status, 'aguardando equipe', 'nada é liberado antes de confirmar');
    await painel.locator('#dlg').getByRole('button', { name: 'Já confirmei, liberar' }).click();
    await novo.locator('.balao.sistema', { hasText: 'A equipe confirmou' }).waitFor();
    assert.equal(pedido.status, 'confirmado');
    await painel.waitForFunction(() => ![...document.querySelectorAll('.barco')].some((b) => b.textContent.includes('link público: confirme quem é')));
  });

  await passo('a mesma pessoa não marca duas descidas no mesmo dia', async () => {
    await novo.getByLabel('Mensagem', { exact: true }).fill('desce a dona lúcia amanhã 11h');
    await novo.getByRole('button', { name: 'Enviar mensagem' }).click();
    await novo.locator('.balao', { hasText: 'Já existe uma descida' }).waitFor();
    assert.equal(store.registros.filter((r) => r.tipo === 'descida' && r.hora === '11:00').length, 0);
  });

  await passo('janela que lotou depois do pedido só libera como encaixe', async () => {
    // Outro visitante, em outro aparelho, pede as 11h.
    const terceiro = await (await navegador.newContext({ viewport: { width: 390, height: 780 }, locale: 'pt-BR' })).newPage();
    vigiar(terceiro, 'visitante3');
    await terceiro.goto(base);
    await terceiro.getByLabel('Mensagem', { exact: true }).fill('desce a maré alta amanhã 11h');
    await terceiro.getByRole('button', { name: 'Enviar mensagem' }).click();
    await painel.locator('.barco', { hasText: 'link público: confirme quem é' }).first().waitFor();
    const pedido = store.registros.find((r) => r.tipo === 'descida' && r.hora === '11:00' && r.data === amanha);
    assert.equal(pedido.status, 'aguardando equipe');
    // Enquanto o pedido espera, a equipe lota a janela das 11h pelo painel.
    for (let i = 1; i <= store.config.rampa.capacidade; i++) {
      const r = await painel.request.post(`${base}/api/painel/registro`, {
        headers: { 'X-Painel': '1' },
        data: { tipo: 'descida', nome: `Cliente ${i}`, embarcacao: `Lancha ${i}`, data: amanha, hora: '11:00' },
      });
      assert.equal(r.status(), 200, `lançamento ${i}`);
    }
    const cartao = painel.locator('.barco', { hasText: 'janela lotada' }).first();
    await cartao.waitFor();
    await cartao.getByRole('button', { name: 'Liberar como encaixe' }).click();
    await painel.locator('#dlg').getByText('já está lotada', { exact: false }).waitFor();
    await painel.locator('#dlg').getByRole('button', { name: 'Liberar como encaixe' }).click();
    await terceiro.locator('.balao.sistema', { hasText: 'às 11h' }).waitFor();
    assert.equal(pedido.status, 'confirmado');
    await painel.locator('.janela header', { hasText: 'com encaixe' }).waitFor();
  });

  await passo('mudar a grade avisa das descidas que ficaram fora e o quadro continua mostrando', async () => {
    await painel.getByRole('button', { name: 'Configuração' }).click();
    await painel.getByLabel('Janela (minutos)').fill('45');
    await painel.getByRole('button', { name: 'Salvar configuração' }).first().click();
    await painel.locator('#dlg').getByText(/Atenção: \d+ descida\(s\) já marcada\(s\) ficaram em horários que não existem na grade nova/).waitFor();
    await painel.locator('#dlg').getByRole('button', { name: 'Ok' }).click();
    await painel.getByRole('button', { name: /^Rampa/ }).click();
    await painel.locator('.janela header', { hasText: 'fora da grade atual' }).first().waitFor();
    await painel.locator('.barco', { hasText: 'Lancha Maré' }).waitFor();
    await painel.screenshot({ path: path.join(telas, 'painel-fora-da-grade.png') });
  });

  await passo('link pessoal inválido mostra erro claro', async () => {
    const p = await celular.newPage();
    await p.goto(`${base}/c/nao-existe`);
    await p.getByText('Este link não é mais válido').waitFor();
    await p.close();
  });

  assert.deepEqual(erros, [], `erros de página: ${erros.join(' | ')}`);
  console.log(`\n${passos.length} passos ok. Telas em docs/telas/`);
} finally {
  await navegador.close();
  servidor.close();
  store.descarregar();
}
