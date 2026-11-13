// Converte os HTML dos catalogos impressos em PDF. Uso: node pdf.js PASTA
// Precisa do Playwright (Chromium). Alternativa: abrir o HTML no navegador e imprimir em PDF, sem margens, com graficos de fundo.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const pasta = path.resolve(process.argv[2] || '.');
  const b = await chromium.launch();
  for (const f of fs.readdirSync(pasta).filter(x => x.endsWith('.html'))) {
    const p = await b.newPage();
    await p.goto('file://' + path.join(pasta, f));
    const estouro = await p.evaluate(() => [...document.querySelectorAll('.pg')].map((s, i) => {
      const r = s.querySelector('.rodape'); const limite = r ? r.getBoundingClientRect().top : s.getBoundingClientRect().bottom;
      let fundo = 0; for (const e of s.children) if (!e.classList.contains('rodape') && !e.classList.contains('img')) fundo = Math.max(fundo, e.getBoundingClientRect().bottom);
      return s.classList.contains('capa') ? null : (fundo > limite + 1 ? (i + 1) : null) }).filter(Boolean));
    const saida = path.join(pasta, f.replace('.html', '.pdf'));
    await p.pdf({ path: saida, preferCSSPageSize: true, printBackground: true });
    console.log(saida + (estouro.length ? '  ATENCAO: conteudo passando do rodape nas paginas ' + estouro.join(', ') : '  ok'));
    await p.close();
  }
  await b.close();
})();
