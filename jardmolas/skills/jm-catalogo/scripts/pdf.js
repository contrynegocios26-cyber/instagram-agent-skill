// Converte em PDF os HTML de uma pasta. Uso: node pdf.js PASTA [arquivo.html]
// Precisa do Playwright (Chromium). Alternativa: abrir o HTML no navegador e imprimir em PDF, A4, sem margens, com graficos de fundo.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const pasta = path.resolve(process.argv[2] || '.');
  const so = process.argv[3];
  const b = await chromium.launch();
  for (const f of fs.readdirSync(pasta).filter(x => x.endsWith('.html') && (!so || x === so))) {
    const p = await b.newPage();
    const erros = [];
    p.on('pageerror', e => erros.push(e.message));
    await p.goto('file://' + path.join(pasta, f));
    // catalogos paginados por script avisam quando terminaram
    await p.waitForFunction('window.__pronto === undefined || window.__pronto === true', null, { timeout: 120000 });
    const info = await p.evaluate(() => {
      if (window.__paginas) return { paginas: window.__paginas, estouro: window.__estouro || [] };
      const estouro = [...document.querySelectorAll('.pg')].map((s, i) => {
        const r = s.querySelector('.rodape'); if (!r || s.classList.contains('capa')) return null;
        let fundo = 0; for (const e of s.children) if (!e.classList.contains('rodape') && !e.classList.contains('img')) fundo = Math.max(fundo, e.getBoundingClientRect().bottom);
        return fundo > r.getBoundingClientRect().top + 1 ? i + 1 : null }).filter(Boolean);
      return { paginas: document.querySelectorAll('.pg').length, estouro };
    });
    const saida = path.join(pasta, f.replace('.html', '.pdf'));
    await p.pdf({ path: saida, preferCSSPageSize: true, printBackground: true });
    console.log(path.basename(saida) + ': ' + info.paginas + ' paginas' +
      (info.estouro.length ? '  ATENCAO: conteudo cortado nas paginas ' + info.estouro.join(', ') : '  ok') +
      (erros.length ? '  ERRO DE SCRIPT: ' + erros.join(' | ') : ''));
    await p.close();
  }
  await b.close();
})();
