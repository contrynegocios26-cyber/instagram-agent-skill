// Renders the cover variants in the same template as midia/2026-11-05.
const { chromium } = require('playwright');
const path = require('path');
const covers = [
  { id: 'atual-claro', theme: 'light', kicker: 'GUIA RÁPIDO', h: 'MDF ou madeira maciça?', sub: 'O que muda no seu móvel, no acabamento e na conta. Arraste.' },
  { id: 'pergunta', theme: 'dark', kicker: 'ANTES DE FECHAR O ORÇAMENTO', h: 'A pergunta que desmonta marceneiro enrolado.', sub: 'Faça antes de assinar. Arraste.' },
  { id: 'vendendo', theme: 'dark', kicker: 'MDF OU MADEIRA MACIÇA', h: 'Quem diz que um é sempre melhor está vendendo só um deles.', sub: 'O lugar certo de cada material. Arraste.' },
  { id: 'nunca-aqui', theme: 'dark', kicker: 'MDF OU MADEIRA MACIÇA', h: 'Nunca use MDF aqui.', sub: 'E onde ele ganha da madeira maciça. Arraste.' },
  { id: 'piso-cliche', theme: 'dark', kicker: 'MP MARCENARIA', h: 'Qualidade e capricho em cada detalhe.', sub: 'Exclusividade para transformar o seu espaço.' },
];
const html = c => `<html><body style="margin:0"><div style="width:1080px;height:1350px;box-sizing:border-box;padding:0 80px;position:relative;font-family:Inter,sans-serif;
background:${c.theme === 'dark' ? 'linear-gradient(#1a0809,#080606)' : '#f2ebe0'};color:${c.theme === 'dark' ? '#f5f0ec' : '#1d1210'}">
<div style="position:absolute;right:92px;top:158px;display:flex;gap:14px">${[...Array(8)].map((_, i) => `<span style="width:12px;height:12px;border-radius:50%;background:${c.theme === 'dark' ? '#f5f0ec' : '#1d1210'};opacity:${i ? .3 : 1}"></span>`).join('')}</div>
<div style="position:absolute;left:80px;right:80px;top:50%;transform:translateY(-50%)">
<div style="font-size:30px;font-weight:600;letter-spacing:.5px;color:${c.theme === 'dark' ? '#c9976b' : '#8a5a2e'};margin-bottom:36px">${c.kicker}</div>
<div style="font-size:${c.h.length > 40 ? 84 : 104}px;font-weight:700;line-height:1.08;letter-spacing:-2px">${c.h}</div>
<div style="font-size:44px;line-height:1.3;margin-top:36px;opacity:.72">${c.sub}</div></div>
<div style="position:absolute;left:80px;bottom:92px;font-size:30px;opacity:.75"><div style="width:72px;height:5px;background:#9c1c1c;margin-bottom:22px"></div>MP Marcenaria &nbsp;·&nbsp; @mp.marcenariaa &nbsp;·&nbsp; Alto Paraná, PR</div></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const c of covers) {
    await p.setContent(html(c));
    await p.screenshot({ path: path.join(__dirname, 'capas', c.id + '.jpg'), type: 'jpeg', quality: 88 });
  }
  await b.close();
})();
