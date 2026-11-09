// Renderiza um HTML em PDF (para imprimir) e PNG (para mandar no WhatsApp).
// Uso: node render.js entrada.html saida.pdf saida.png largura_mm altura_mm paginas
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [html, pdf, png, wmm, hmm, paginas = '1'] = process.argv.slice(2);
  const wpx = (parseFloat(wmm) / 25.4) * 96;
  const hpx = (parseFloat(hmm) / 25.4) * 96;
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: Math.round(wpx), height: Math.round(hpx * parseInt(paginas, 10)) },
    deviceScaleFactor: 1080 / wpx,
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: pdf, width: `${wmm}mm`, height: `${hmm}mm`, printBackground: true });
  if (png) await page.screenshot({ path: png, fullPage: true });
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
