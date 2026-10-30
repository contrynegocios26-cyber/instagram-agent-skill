/* MP Marcenaria — app do cliente
   Vanilla JS, sem build. Estado no localStorage; configuração em config.js. */
(function () {
  "use strict";
  const C = window.MP_CONFIG;
  const KEY = "mp-app-v1";

  /* ---------------- utilidades ---------------- */
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const brl0 = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });
  const brl2 = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", minimumFractionDigits: 2 });
  const money = (n, cents) => (cents ? brl2 : brl0).format(n);
  const parseDate = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const fmtDate = (s, long) => parseDate(s).toLocaleDateString("pt-BR", long ? { day: "numeric", month: "long", year: "numeric" } : { day: "numeric", month: "short" }).replace(".", "");
  const todayISO = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
  const daysUntil = (s) => Math.round((parseDate(s) - parseDate(todayISO())) / 86400000);
  const metros = (m) => m.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + " m";
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const corAcab = (id) => String(id).startsWith("#") ? id : (C.acabamentos.find((a) => a.id === id) || { cor: "#A47148" }).cor;

  const ICONS = {
    home: '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
    project: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/>',
    quote: '<path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h5"/>',
    inspire: '<path d="M12 3l2.5 5.5L20 10l-4 4 1 6-5-3-5 3 1-6-4-4 5.5-1.5z"/>',
    more: '<circle cx="12" cy="12" r="1.6"/><circle cx="5" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
    whatsapp: '<path d="M20 11.5a8 8 0 0 1-11.9 7L4 20l1.5-3.9A8 8 0 1 1 20 11.5z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 1a4 4 0 0 1-2-2l1-1-1-2z"/>',
    ruler: '<path d="M3 17l14-14 4 4L7 21z"/><path d="M8 8l1.5 1.5M11 5l1.5 1.5M14 2l1.5 1.5M5 11l1.5 1.5"/>',
    photo: '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-8 8"/>',
    cube: '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M12 12l9-5M12 12v10M12 12L3 7"/>',
    check: '<path d="M5 13l4 4L19 7"/>',
    heart: '<path d="M12 21s-7-4.6-9-9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c-2 4.4-9 9-9 9z"/>',
    shield: '<path d="M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    tool: '<path d="M14.5 6.5a4 4 0 0 0 5 5L9 22l-3-3L16.5 8.5"/><path d="M3 21l3-3"/>',
    gift: '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8v13M3 13h18M12 8c-2-4-6-3-6-1s3 1 6 1zm0 0c2-4 6-3 6-1s-3 1-6 1z"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>',
    lock: '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    bell: '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    chev: '<path d="M9 6l6 6-6 6"/>',
    copy: '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    instagram: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
    download: '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 21h16"/>',
    doc: '<path d="M6 2h8l6 6v14H6z"/><path d="M14 2v6h6"/>',
    cozinha: '<path d="M4 10h16v10H4z"/><path d="M4 14h16M12 14v6M8 4v6M16 4v6"/>',
    closet: '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M9 12h1M14 12h1"/>',
    banheiro: '<path d="M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M6 12V5a2 2 0 0 1 4 0"/>',
    sala: '<rect x="3" y="5" width="18" height="11" rx="1"/><path d="M8 20h8M12 16v4"/>',
    gourmet: '<path d="M4 20h16"/><path d="M6 20V9a6 6 0 0 1 12 0v11"/><path d="M9 14h6"/>',
    lavanderia: '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="13" r="4"/><path d="M7 7h2"/>',
    escritorio: '<path d="M3 10h18M5 10v9M19 10v9"/><rect x="8" y="4" width="8" height="6" rx="1"/>',
    porta: '<rect x="6" y="3" width="12" height="18" rx="1"/><path d="M14 12h1"/>',
    x: '<path d="M6 6l12 12M18 6L6 18"/>',
    share: '<path d="M4 12v8h16v-8"/><path d="M12 3v12M8 7l4-4 4 4"/>',
    pin: '<path d="M12 21s6-5.5 6-11a6 6 0 0 0-12 0c0 5.5 6 11 6 11z"/><circle cx="12" cy="10" r="2"/>'
  };
  const icon = (n) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[n] || ""}</svg>`;

  /* ---------------- estado ---------------- */
  const defaults = () => ({
    v: 1,
    cliente: clone(C.demo.cliente),
    projeto: clone(C.demo.projeto),
    notificacoes: clone(C.demo.notificacoes),
    referencia: clone(C.referencia),
    precosConfigurados: C.precosConfigurados,
    favoritos: [],
    pedidos: [],
    aprovacoes: {},
    comprovantes: {},
    prefs: { tema: "auto", notif: true },
    oficina: false,
    draft: null
  });
  let S;
  try { const raw = localStorage.getItem(KEY); S = raw ? Object.assign(defaults(), JSON.parse(raw)) : defaults(); } catch (e) { S = defaults(); }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(Object.assign({}, S, { draft: S.draft && Object.assign({}, S.draft, { fotos: [] }) }))); } catch (e) { /* armazenamento indisponível */ } };
  const applyTheme = () => { const r = document.documentElement; if (S.prefs.tema === "auto") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", S.prefs.tema); };
  applyTheme();

  const etapaIdx = (id) => C.etapas.findIndex((e) => e.id === id);
  const etapaAtual = () => C.etapas[etapaIdx(S.projeto.etapaAtual)] || C.etapas[0];
  const totalProjeto = () => S.projeto.ambientes.reduce((a, b) => a + b.valor, 0);
  const naoLidas = () => S.notificacoes.filter((n) => !n.lida).length;
  const whats = (texto) => `https://wa.me/${C.empresa.whatsapp}?text=${encodeURIComponent(texto)}`;
  const addNotif = (titulo, texto) => { S.notificacoes.unshift({ id: "n" + Date.now(), data: todayISO(), titulo, texto, lida: false }); };

  /* ---------------- toast / sheet ---------------- */
  let toastT;
  function toast(msg) {
    const root = $("#toastRoot"); root.innerHTML = `<div class="toast" role="status">${esc(msg)}</div>`;
    clearTimeout(toastT); toastT = setTimeout(() => { root.innerHTML = ""; }, 2600);
  }
  function openSheet(html, onMount) {
    const root = $("#sheetRoot");
    root.innerHTML = `<div class="sheet-backdrop" data-action="closeSheet"><div class="sheet" role="dialog" aria-modal="true" data-stop><div class="grab"></div>${html}</div></div>`;
    document.body.style.overflow = "hidden";
    if (onMount) onMount(root.firstElementChild);
  }
  function closeSheet() { $("#sheetRoot").innerHTML = ""; document.body.style.overflow = ""; }
  const sheetHead = (t) => `<div class="sheet-head"><h2>${esc(t)}</h2><button class="icon-btn" data-action="closeSheet" aria-label="Fechar">${icon("x")}</button></div>`;
  async function copyText(txt, okMsg) {
    try { await navigator.clipboard.writeText(txt); toast(okMsg || "Copiado"); }
    catch (e) { openSheet(`${sheetHead("Copie o texto")}<textarea class="input" id="copyFallback" readonly>${esc(txt)}</textarea>`, (el) => { const ta = $("#copyFallback", el); ta.focus(); ta.select(); }); }
  }

  /* ---------------- roteamento ---------------- */
  const TABS = [
    { id: "inicio", nome: "Início", ico: "home" },
    { id: "projeto", nome: "Projeto", ico: "project" },
    { id: "orcamento", nome: "Orçamento", ico: "quote" },
    { id: "inspiracoes", nome: "Inspirações", ico: "inspire" },
    { id: "mais", nome: "Mais", ico: "more" }
  ];
  const VIEWS = {};
  function route() {
    let id = (location.hash || "#inicio").slice(1);
    if (!VIEWS[id]) id = "inicio";
    $$(".view").forEach((v) => { v.hidden = v.dataset.view !== id; });
    $("#tabs").innerHTML = TABS.map((t) => `<a class="tab" href="#${t.id}" ${t.id === id ? 'aria-current="page"' : ""}>${icon(t.ico)}<span>${t.nome}</span></a>`).join("");
    VIEWS[id]();
    $("#notifDot").hidden = naoLidas() === 0;
    window.scrollTo(0, 0);
  }
  const go = (id) => { if (location.hash === "#" + id) route(); else location.hash = id; };

  /* ================= INÍCIO ================= */
  VIEWS.inicio = function () {
    const p = S.projeto, et = etapaAtual();
    const hora = new Date().getHours();
    const saud = hora < 12 ? "Bom dia" : hora < 18 ? "Boa tarde" : "Boa noite";
    const pend = [];
    p.ambientes.forEach((a) => { if (!a.aprovado) pend.push({ cor: "accent", t: `Aprovar o projeto 3D: ${a.nome}`, d: a.detalhe, action: "goProjeto3d" }); });
    p.pagamentos.filter((x) => !x.pago).slice(0, 1).forEach((x) => { const dd = daysUntil(x.vence); pend.push({ cor: dd < 0 ? "bad" : "warn", t: `${x.desc}: ${money(x.valor)}`, d: dd < 0 ? `Venceu há ${-dd} dia(s)` : dd === 0 ? "Vence hoje" : `Vence em ${dd} dia(s), ${fmtDate(x.vence)}`, action: "goPagamentos" }); });
    const nl = naoLidas(); if (nl) pend.push({ cor: "accent", t: `${nl} novidade(s) da oficina`, d: S.notificacoes.find((n) => !n.lida).texto, action: "openNotif" });

    $("#view-inicio").innerHTML = `
      <div class="hero">
        <span class="eyebrow">${saud}, ${esc(S.cliente.primeiroNome)}</span>
        <h1>Sua casa, <em>feita sob medida</em>.</h1>
      </div>

      <section class="card status-card lift">
        <span class="eyebrow">${esc(p.titulo)}</span>
        <div class="row between" style="margin-top:6px;align-items:flex-end">
          <div><h2>${esc(et.nome)}</h2><p class="muted small">${esc(et.desc)}</p></div>
          <div class="status-big num">${p.progresso}<small style="font-size:18px">%</small></div>
        </div>
        <div class="progress" style="margin:14px 0 12px"><span style="width:${p.progresso}%"></span></div>
        <div class="row between">
          <span class="small muted">Entrega prevista <b class="num" style="color:inherit">${fmtDate(p.previsaoEntrega, true)}</b></span>
          <a class="btn sm" href="#projeto">Ver projeto</a>
        </div>
      </section>

      ${pend.length ? `<section class="stack"><span class="eyebrow">Precisa de você</span>${pend.map((x) => `<button class="todo" data-action="${x.action}"><span class="mark ${x.cor}"></span><span class="body"><b>${esc(x.t)}</b><br><span class="small muted">${esc(x.d)}</span></span>${icon("chev")}</button>`).join("")}</section>` : ""}

      <section class="stack">
        <span class="eyebrow">O que você quer fazer</span>
        <div class="actions-grid">
          <a class="action" href="#orcamento"><span class="ico">${icon("ruler")}</span>Pedir orçamento</a>
          <a class="action" href="${whats(`Olá! Sou ${S.cliente.nome} (código ${S.cliente.codigo}). Quero falar sobre meu projeto.`)}" target="_blank" rel="noopener"><span class="ico">${icon("whatsapp")}</span>Falar no WhatsApp</a>
          <a class="action" href="#projeto" data-action="goProjeto3d"><span class="ico">${icon("cube")}</span>Ver o 3D</a>
          <a class="action" href="#inspiracoes"><span class="ico">${icon("photo")}</span>Inspirações</a>
        </div>
      </section>

      <section class="card">
        <div class="card-head"><h3>Como funciona na MP</h3><a class="link" href="#projeto">Minha etapa</a></div>
        <div class="steps">${C.etapas.map((e, i) => { const cur = etapaIdx(p.etapaAtual); const cls = i < cur ? "done" : i === cur ? "now" : ""; return `<div class="step ${cls}"><span class="n">${cls === "done" ? "✓" : i + 1}</span><div><div class="t">${esc(e.nome)}</div><div class="d">${esc(e.desc)}</div></div></div>`; }).join("")}</div>
      </section>

      <section class="stack">
        <span class="eyebrow">Por que a MP</span>
        <div class="why">
          <div><b>${C.empresa.anos} anos</b><span>de móveis planejados e esquadrias de alto padrão</span></div>
          <div><b>${C.empresa.garantiaMeses / 12} anos</b><span>de garantia na estrutura e ferragens</span></div>
          <div><b>3D antes</b><span>você aprova o projeto interativo antes de qualquer corte</span></div>
          <div><b>Brasil</b><span>atendemos todo o país, com foco no Paraná</span></div>
        </div>
      </section>

      <section class="card">
        <div class="row" style="gap:14px">
          <span class="brand-mark" aria-hidden="true">MP</span>
          <div style="flex:1;min-width:0"><b>${esc(C.empresa.nome)}</b><br><span class="small muted">${esc(C.empresa.cidade)} · <a href="${C.empresa.instagramUrl}" target="_blank" rel="noopener">@${esc(C.empresa.instagram)}</a></span></div>
        </div>
      </section>`;
  };

  /* ================= PROJETO ================= */
  let viewer = null, ambSel = 0, viewer3dOpen = false;
  VIEWS.projeto = function () {
    const p = S.projeto;
    const hist = p.historico.slice().sort((a, b) => b.data.localeCompare(a.data));
    const amb3d = C.demo.projeto3d.ambientes;
    const pend = p.ambientes.find((a) => !a.aprovado);
    $("#view-projeto").innerHTML = `
      <div class="hero" style="padding-top:0">
        <span class="eyebrow">${esc(p.id)}</span>
        <h1>${esc(p.titulo)}</h1>
        <p class="muted small">Projeto com ${esc(p.arquiteto)} · ${p.ambientes.length} ambientes · ${money(totalProjeto())}</p>
      </div>

      <section class="card">
        <div class="card-head"><h3>Ambientes</h3><span class="pill ${pend ? "warn" : "good"}"><i></i>${pend ? "1 aprovação pendente" : "Tudo aprovado"}</span></div>
        ${p.ambientes.map((a, i) => `<div class="amb"><div style="min-width:0"><b>${esc(a.nome)}</b><br><span class="small muted">${esc(a.status)}. ${esc(a.detalhe)}</span>${a.aprovado ? `<br><span class="pill good" style="margin-top:6px"><i></i>Aprovado${S.aprovacoes[a.nome] ? " em " + fmtDate(S.aprovacoes[a.nome].data) : ""}</span>` : `<br><button class="btn accent sm" style="margin-top:8px" data-action="aprovar" data-i="${i}">${icon("check")} Revisar e aprovar</button>`}</div><div class="v num">${money(a.valor)}</div></div>`).join("")}
      </section>

      <section class="card" id="card3d">
        <div class="card-head"><h3>Projeto 3D interativo</h3><span class="small muted">arraste para girar</span></div>
        <div class="segmented" role="tablist">${amb3d.map((a, i) => `<button role="tab" aria-selected="${i === ambSel}" data-action="amb3d" data-i="${i}">${esc(a.nome)}</button>`).join("")}</div>
        <div class="viewer" id="viewer" style="margin-top:10px">
          ${!viewer3dOpen ? `<button class="btn primary" style="position:absolute;inset:auto;left:50%;top:50%;transform:translate(-50%,-50%)" data-action="open3d">${icon("cube")} Abrir o 3D</button>` : ""}
          <span class="viewer-hint" id="viewerHint">${esc(amb3d[ambSel].nome)} · ${(amb3d[ambSel].largura / 1000).toLocaleString("pt-BR")} × ${(amb3d[ambSel].altura / 1000).toLocaleString("pt-BR")} m</span>
        </div>
        <div class="viewer-controls">
          <button class="chip" data-action="vista" data-v="frontal">Vista frontal</button>
          <button class="chip" data-action="vista" data-v="iso">Isométrica</button>
          <button class="chip" id="chipPortas" data-action="portas" aria-pressed="false">Abrir portas</button>
        </div>
        <p class="small muted" style="margin-top:10px">Modelo volumétrico com cores e proporções reais, para aprovar layout e volumes. As cores finais seguem o acabamento escolhido.</p>
      </section>

      <section class="card">
        <div class="card-head"><h3>Linha do tempo</h3></div>
        <div class="steps">${C.etapas.map((e, i) => { const cur = etapaIdx(p.etapaAtual); const cls = i < cur ? "done" : i === cur ? "now" : ""; const h = hist.find((x) => x.etapa === e.id); return `<div class="step ${cls}"><span class="n">${cls === "done" ? "✓" : i + 1}</span><div><div class="row between"><span class="t">${esc(e.nome)}</span>${h ? `<span class="date">${fmtDate(h.data)}</span>` : ""}</div><div class="d">${h ? esc(h.texto) : esc(e.desc)}</div></div></div>`; }).join("")}</div>
      </section>

      <section class="card">
        <div class="card-head"><h3>Direto da oficina</h3><span class="small muted">${p.atualizacoes.length} atualizações</span></div>
        <div class="feed">${p.atualizacoes.map((u, i) => `<article class="post"><canvas data-wood="${esc(u.cor)}" data-seed="${i + 3}" width="168" height="168"></canvas><div><span class="small muted num">${fmtDate(u.data, true)}</span><b>${esc(u.titulo)}</b><p class="small">${esc(u.texto)}</p></div></article>`).join("")}</div>
      </section>

      <section class="card" id="cardPag">
        <div class="card-head"><h3>Pagamentos</h3><span class="small muted num">${money(p.pagamentos.filter((x) => x.pago).reduce((a, b) => a + b.valor, 0))} de ${money(totalProjeto())}</span></div>
        <div class="progress" style="margin-bottom:12px"><span style="width:${Math.round(100 * p.pagamentos.filter((x) => x.pago).reduce((a, b) => a + b.valor, 0) / totalProjeto())}%"></span></div>
        ${p.pagamentos.map((x) => { const dd = daysUntil(x.vence); const comp = S.comprovantes[x.n]; const cls = x.pago ? "paid" : dd <= 7 ? "due" : ""; return `<div class="pay ${cls}"><span class="n">${x.pago ? "✓" : x.n}</span><div style="min-width:0"><b>${esc(x.desc)}</b><br><span class="small muted">${x.pago ? "Pago" : comp ? `Comprovante enviado em ${fmtDate(comp.data)} · em análise` : dd < 0 ? `Venceu em ${fmtDate(x.vence)}` : `Vence em ${fmtDate(x.vence, true)}`}</span>${!x.pago && !comp ? `<div class="btn-row" style="margin-top:8px"><button class="btn sm" data-action="pix" data-n="${x.n}">${icon("copy")} Copiar chave Pix</button><label class="btn sm" style="cursor:pointer">${icon("share")} Enviar comprovante<input type="file" accept="image/*,.pdf" hidden data-comp="${x.n}"></label></div>` : ""}</div><div class="v num">${money(x.valor, true)}</div></div>`; }).join("")}
        <p class="small muted" style="margin-top:12px">Pagamento por Pix ou transferência para ${esc(C.empresa.pixNome)}. Para parcelar no cartão ou ajustar datas, <a href="${whats(`Olá! Sou ${S.cliente.nome}. Quero combinar o pagamento do projeto ${p.id}.`)}" target="_blank" rel="noopener">fale com a MP</a>.</p>
      </section>

      <section class="card">
        <div class="card-head"><h3>Documentos</h3></div>
        ${p.documentos.map((d) => `<div class="doc"><span class="ft">${esc(d.tipo)}</span><div class="body"><b>${esc(d.nome)}</b><span class="small muted num">${fmtDate(d.data, true)}</span></div>${d.url ? `<a class="btn sm" href="${esc(d.url)}" target="_blank" rel="noopener">${icon("download")}</a>` : `<a class="btn sm" href="${whats(`Olá! Pode me reenviar o documento "${d.nome}" do projeto ${p.id}?`)}" target="_blank" rel="noopener">Pedir</a>`}</div>`).join("")}
      </section>

      <section class="card">
        <div class="card-head"><h3>Quem cuida do seu projeto</h3></div>
        <div class="team">${p.equipe.map((e) => `<div class="person"><span class="av">${esc(e.inicial)}</span><span><b>${esc(e.nome)}</b><small>${esc(e.papel)}</small></span></div>`).join("")}</div>
        <a class="btn block" style="margin-top:12px" href="${whats(`Olá! Sou ${S.cliente.nome}, do projeto ${p.id}. `)}" target="_blank" rel="noopener">${icon("whatsapp")} Falar com a equipe</a>
      </section>`;
    $$("canvas[data-wood]", $("#view-projeto")).forEach((cv) => drawWood(cv, corAcab(cv.dataset.wood), true, Number(cv.dataset.seed)));
    if (viewer3dOpen) mount3d();
  };

  /* ---------- 3D (three.js) ---------- */
  function mount3d() {
    const box = $("#viewer"); if (!box) return;
    if (!window.THREE || !window.THREE.OrbitControls) { mountFrontal(box); return; }
    if (!viewer) viewer = create3d();
    box.insertBefore(viewer.renderer.domElement, box.firstChild);
    viewer.load(C.demo.projeto3d.ambientes[ambSel]);
    viewer.fit();
  }
  /* Reserva sem internet ou sem WebGL: vista frontal desenhada em canvas a partir do mesmo projeto. */
  function mountFrontal(box) {
    const a = C.demo.projeto3d.ambientes[ambSel];
    const idAcab = (hex) => (C.acabamentos.find((x) => x.cor.toLowerCase() === String(hex).toLowerCase()) || { id: hex }).id;
    const item = { largura: a.largura, altura: a.altura, modulos: a.modulos.map((m) => ({ x: m.x, y: m.y, w: m.w, h: m.h, cor: idAcab(a.materiais[m.frente]), frentes: m.frentes.reduce((s, f) => s + f.qtd, 0), torre: m.tipo === "torre", gavetas: m.frentes.some((f) => f.tipo === "gaveta") })) };
    const cv = document.createElement("canvas"); cv.width = 800; cv.height = 600; cv.style.cssText = "display:block;width:100%;height:100%";
    drawElevation(cv, item); box.insertBefore(cv, box.firstChild);
    box.insertAdjacentHTML("beforeend", `<span class="fallback-note">Vista frontal · o 3D interativo abre com internet</span>`);
  }
  function create3d() {
    const T = window.THREE;
    const renderer = new T.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    const scene = new T.Scene();
    const camera = new T.PerspectiveCamera(42, 4 / 3, 0.05, 100);
    const controls = new T.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.maxPolarAngle = Math.PI / 2 + 0.05; controls.minDistance = 1.2; controls.maxDistance = 14;
    scene.add(new T.HemisphereLight(0xfff6ea, 0x8a7a68, 0.95));
    const sun = new T.DirectionalLight(0xffffff, 0.75); sun.position.set(3, 6, 5); scene.add(sun);
    let group = new T.Group(); scene.add(group);
    let doors = [], drawers = [], open = false, amb = null;
    const mat = (hex, opts) => new T.MeshStandardMaterial(Object.assign({ color: new T.Color(hex), roughness: 0.65, metalness: 0.02 }, opts || {}));
    const boxMesh = (w, h, d, m, x, y, z) => { const me = new T.Mesh(new T.BoxGeometry(w / 1000, h / 1000, d / 1000), m); me.position.set((x + w / 2) / 1000, (y + h / 2) / 1000, (z + d / 2) / 1000); return me; };

    function load(a) {
      amb = a; scene.remove(group); group = new T.Group(); scene.add(group); doors = []; drawers = [];
      const W = a.largura, H = a.altura, D = a.profundidade;
      const isDark = matchMedia("(prefers-color-scheme: dark)").matches && document.documentElement.getAttribute("data-theme") !== "light" || document.documentElement.getAttribute("data-theme") === "dark";
      const wallM = mat(isDark ? 0x3a3531 : 0xe9e4dc, { roughness: 1 }); const floorM = mat(isDark ? 0x2a2622 : 0xd6cdc0, { roughness: 1 });
      group.add(boxMesh(W + 100, H, 60, wallM, -50, 0, -60));
      const floor = new T.Mesh(new T.PlaneGeometry((W + 100) / 1000, D / 1000), floorM); floor.rotation.x = -Math.PI / 2; floor.position.set(W / 2000, -0.001, D / 2000); group.add(floor);
      const T18 = 18;
      a.modulos.forEach((m) => {
        const cx = a.materiais[m.caixa], cf = a.materiais[m.frente];
        const caixa = mat(cx), frente = mat(cf);
        group.add(boxMesh(T18, m.h, m.d - T18, caixa, m.x, m.y, 0));
        group.add(boxMesh(T18, m.h, m.d - T18, caixa, m.x + m.w - T18, m.y, 0));
        group.add(boxMesh(m.w - 2 * T18, T18, m.d - T18, caixa, m.x + T18, m.y, 0));
        group.add(boxMesh(m.w - 2 * T18, T18, m.d - T18, caixa, m.x + T18, m.y + m.h - T18, 0));
        group.add(boxMesh(m.w - 2 * T18, m.h - 2 * T18, 6, caixa, m.x + T18, m.y + T18, 8));
        const nShelf = m.tipo === "roupeiro" ? 2 : m.tipo === "torre" ? 0 : 1;
        for (let i = 1; i <= nShelf; i++) group.add(boxMesh(m.w - 2 * T18, T18, m.d - T18 - 20, caixa, m.x + T18, m.y + (m.h * i) / (nShelf + 1), 10));
        if (m.nichos) m.nichos.forEach((n) => group.add(boxMesh(m.w - 2 * T18, T18, m.d - T18, mat(cx), m.x + T18, m.y + n.y, 0)));
        if (m.tipo === "balcao") { const topo = mat(isDark ? 0x4a4642 : 0xf4f2ee, { roughness: 0.35 }); group.add(boxMesh(m.w, 30, m.d + 40, topo, m.x, m.y + m.h, 0)); }
        if (m.pia) { const cuba = mat(0xb9bcc0, { metalness: 0.7, roughness: 0.3 }); group.add(boxMesh(m.w - 200, 12, m.d - 150, cuba, m.x + 100, m.y + m.h + 26, 60)); }
        const gap = 3;
        m.frentes.forEach((f) => {
          if (f.tipo === "gaveta") {
            const hh = (m.h - gap * (f.qtd + 1)) / f.qtd;
            for (let i = 0; i < f.qtd; i++) {
              const g = new T.Group(); const p = boxMesh(m.w - 2 * gap, hh, T18, frente, 0, 0, 0); g.add(p);
              g.position.set((m.x + gap) / 1000, (m.y + gap + i * (hh + gap)) / 1000, (m.d - T18) / 1000); group.add(g); drawers.push({ g, d: m.d });
              const gola = boxMesh(m.w - 2 * gap - 40, 8, 6, mat(0x8d8d8d, { metalness: 0.6, roughness: 0.3 }), 20, hh - 30, T18); g.add(gola);
            }
          } else {
            const ww = (m.w - gap * (f.qtd + 1)) / f.qtd;
            const nichoH = (m.nichos || []).reduce((s, n) => s + n.h, 0);
            for (let i = 0; i < f.qtd; i++) {
              const hingeLeft = i % 2 === 0;
              const g = new T.Group();
              let y0 = m.y + gap, hh = m.h - 2 * gap;
              if (m.tipo === "torre" && m.nichos && m.nichos.length) { const top = Math.min.apply(null, m.nichos.map((n) => n.y)); hh = top - 2 * gap; }
              const p = boxMesh(ww, hh, T18, frente, hingeLeft ? 0 : -ww, 0, 0); g.add(p);
              g.position.set((m.x + gap + i * (ww + gap) + (hingeLeft ? 0 : ww)) / 1000, y0 / 1000, (m.d - T18) / 1000);
              group.add(g); doors.push({ g, dir: hingeLeft ? -1 : 1 });
              if (m.tipo === "torre" && nichoH) { const topDoor = boxMesh(ww, m.h - hh - (m.nichos.reduce((s, n) => Math.max(s, n.y + n.h), 0) - Math.min.apply(null, m.nichos.map((n) => n.y))) - 4 * gap, T18, frente, m.x + gap + i * (ww + gap), m.y + Math.max.apply(null, m.nichos.map((n) => n.y + n.h)) + gap, m.d - T18); group.add(topDoor); }
            }
          }
        });
      });
      setOpen(open);
    }
    function setOpen(v) {
      open = v;
      doors.forEach((d) => { d.g.rotation.y = v ? d.dir * 1.75 : 0; });
      drawers.forEach((d) => { if (d.g.userData.z0 == null) d.g.userData.z0 = d.g.position.z; d.g.position.z = d.g.userData.z0 + (v ? d.d * 0.55 / 1000 : 0); });
    }
    function fit(view) {
      if (!amb) return; const W = amb.largura / 1000, H = amb.altura / 1000;
      controls.target.set(W / 2, H / 2.2, 0.3);
      if (view === "frontal") camera.position.set(W / 2, H / 2, Math.max(W, H) * 1.35 + 0.6);
      else camera.position.set(W * 1.15, H * 0.95, Math.max(W, H) * 1.05 + 0.8);
      controls.update();
    }
    function resize() { const el = renderer.domElement.parentElement; if (!el) return; const w = el.clientWidth, h = el.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
    function render() { renderer.render(scene, camera); }
    (function loop() { requestAnimationFrame(loop); if (!renderer.domElement.isConnected) return; resize(); controls.update(); render(); })();
    return { renderer, load, fit: (v) => fit(v || "iso"), setOpen: (v) => setOpen(v), get open() { return open; } };
  }

  /* ---------- aprovação com assinatura ---------- */
  function abrirAprovacao(i) {
    const a = S.projeto.ambientes[i];
    openSheet(`${sheetHead("Aprovar " + a.nome)}
      <p class="small muted">Confira o 3D e a proposta antes de assinar. Depois da aprovação o projeto segue para remedição técnica e produção, e mudanças passam a ter custo.</p>
      <div class="stack" style="gap:0">
        <label class="check"><input type="checkbox" class="apr-check"><span>Vi o projeto 3D e concordo com o layout, as medidas gerais e a posição dos pontos (água, luz, gás).</span></label>
        <label class="check"><input type="checkbox" class="apr-check"><span>Confirmo os acabamentos e as cores descritos na proposta.</span></label>
        <label class="check"><input type="checkbox" class="apr-check"><span>Li as condições de pagamento, prazo e garantia.</span></label>
      </div>
      <div class="field"><label for="signCanvas">Sua assinatura</label>
        <div class="sign" id="signWrap"><canvas id="signCanvas" aria-label="Área de assinatura"></canvas><span class="ph" id="signPh">Assine com o dedo ou o mouse</span></div>
        <div class="row between"><span class="help">${esc(S.cliente.nome)} · ${fmtDate(todayISO(), true)}</span><button class="link" data-action="signClear">Limpar</button></div>
      </div>
      <button class="btn accent block" id="btnConfirmAprov" data-action="confirmarAprovacao" data-i="${i}" disabled>${icon("check")} Aprovar ${esc(a.nome)} · ${money(a.valor)}</button>`,
      (root) => {
        const cv = $("#signCanvas", root), wrap = $("#signWrap", root), ph = $("#signPh", root), btn = $("#btnConfirmAprov", root);
        const ratio = Math.min(2, devicePixelRatio || 1);
        const size = () => { cv.width = wrap.clientWidth * ratio; cv.height = wrap.clientHeight * ratio; };
        size();
        const ctx = cv.getContext("2d"); let drawing = false, has = false, last = null;
        ctx.lineWidth = 2.2 * ratio; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue("--fg").trim() || "#2B2B2B";
        const pos = (e) => { const r = cv.getBoundingClientRect(); return { x: (e.clientX - r.left) * ratio, y: (e.clientY - r.top) * ratio }; };
        cv.addEventListener("pointerdown", (e) => { drawing = true; last = pos(e); cv.setPointerCapture(e.pointerId); });
        cv.addEventListener("pointermove", (e) => { if (!drawing) return; const p = pos(e); ctx.beginPath(); ctx.moveTo(last.x, last.y); ctx.lineTo(p.x, p.y); ctx.stroke(); last = p; has = true; ph.hidden = true; check(); });
        const up = () => { drawing = false; };
        cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
        const check = () => { btn.disabled = !(has && $$(".apr-check", root).every((c) => c.checked)); };
        $$(".apr-check", root).forEach((c) => c.addEventListener("change", check));
        root._sign = { clear: () => { ctx.clearRect(0, 0, cv.width, cv.height); has = false; ph.hidden = false; check(); }, data: () => cv.toDataURL("image/png") };
      });
  }

  /* ================= ORÇAMENTO ================= */
  const newDraft = () => ({ step: 0, ambientes: [], medidas: {}, padrao: "premium", extras: [], nome: S.cliente.nome || "", telefone: S.cliente.telefone || "", cidade: S.cliente.cidade || "", prazo: "60-90", arquiteto: "", obs: "", fotos: [], acabamentos: S.favAcab || [] });
  function estimar(d) {
    const pad = C.padroes.find((p) => p.id === d.padrao) || C.padroes[1];
    const extra = 1 + d.extras.reduce((s, id) => s + ((C.extras.find((e) => e.id === id) || { fator: 0 }).fator), 0);
    let min = 0, max = 0;
    const linhas = d.ambientes.map((id) => {
      const r = S.referencia[id]; const q = d.medidas[id] != null ? d.medidas[id] : r.unidade === "porta" ? 2 : 3;
      const f = pad.fator * (r.unidade === "porta" ? 1 : extra);
      const lmin = Math.round(q * r.min * f / 100) * 100, lmax = Math.round(q * r.max * f / 100) * 100;
      min += lmin; max += lmax;
      return { id, label: r.label, q, unidade: r.unidade || "m", min: lmin, max: lmax };
    });
    return { min, max, linhas, pad };
  }
  function resumoTexto(d, est) {
    const l = [`*Pedido de orçamento — ${C.empresa.nome}*`, `Nome: ${d.nome}`, `Telefone: ${d.telefone}`, `Cidade/obra: ${d.cidade}`, `Prazo desejado: ${prazoLabel(d.prazo)}`, d.arquiteto ? `Arquiteto(a): ${d.arquiteto}` : "", "", "*Ambientes*"];
    est.linhas.forEach((x) => l.push(`• ${x.label}: ${x.unidade === "porta" ? x.q + " porta(s)" : metros(x.q) + " de parede"}`));
    l.push("", `Padrão: ${est.pad.nome}`);
    if (d.extras.length) l.push(`Extras: ${d.extras.map((id) => C.extras.find((e) => e.id === id).nome).join(", ")}`);
    if (d.acabamentos && d.acabamentos.length) l.push(`Acabamentos que gostei: ${d.acabamentos.map((id) => (C.acabamentos.find((a) => a.id === id) || {}).nome).filter(Boolean).join(", ")}`);
    if (d.obs) l.push("", `Observações: ${d.obs}`);
    l.push("", `Estimativa pelo app: ${money(est.min)} a ${money(est.max)} (referência, não é proposta).`, d.fotos.length ? `Tenho ${d.fotos.length} foto(s)/referência(s) para enviar aqui.` : "");
    return l.join("\n").replace(/\n{3,}/g, "\n\n").trim();
  }
  const PRAZOS = { urgente: "Até 30 dias", "30-60": "30 a 60 dias", "60-90": "60 a 90 dias", "90+": "Mais de 90 dias", planejando: "Ainda planejando" };
  const prazoLabel = (p) => PRAZOS[p] || p;

  VIEWS.orcamento = function () {
    if (!S.draft) S.draft = newDraft();
    const d = S.draft, step = d.step;
    const dots = `<div class="dots" aria-label="Passo ${step + 1} de 4">${[0, 1, 2, 3].map((i) => `<i class="${i <= step ? "on" : ""}"></i>`).join("")}</div>`;
    let body = "";
    if (step === 0) {
      body = `<div class="hero" style="padding-top:0"><span class="eyebrow">Passo 1 de 4</span><h1>Quais ambientes você quer <em>planejar</em>?</h1><p class="muted small">Escolha quantos quiser. Portas e esquadrias também entram aqui.</p></div>
        <div class="choice-grid">${Object.keys(S.referencia).map((id) => { const r = S.referencia[id]; const on = d.ambientes.includes(id); return `<button class="choice" aria-pressed="${on}" data-action="togAmb" data-id="${id}"><span class="ico">${icon(r.icone)}</span><b>${esc(r.label)}</b><span>${r.unidade === "porta" ? "kit porta pronta" : "móveis planejados"}</span></button>`; }).join("")}</div>
        <button class="btn primary block" data-action="wizNext" ${d.ambientes.length ? "" : "disabled"}>Continuar</button>`;
    } else if (step === 1) {
      body = `<div class="hero" style="padding-top:0"><span class="eyebrow">Passo 2 de 4</span><h1>Quanto espaço cada ambiente tem?</h1><p class="muted small">Uma medida aproximada basta: a soma das paredes que vão receber móveis. A MP mede na obra depois.</p></div>
        <section class="card">${d.ambientes.map((id) => { const r = S.referencia[id]; const porta = r.unidade === "porta"; const v = d.medidas[id] != null ? d.medidas[id] : porta ? 2 : 3; return `<div class="measure"><div><b>${esc(r.label)}</b><br><input type="range" min="${porta ? 1 : 1}" max="${porta ? 12 : 10}" step="${porta ? 1 : 0.1}" value="${v}" data-med="${id}" aria-label="${esc(r.label)}"></div><span class="val num" id="val-${id}">${porta ? v + (v === 1 ? " porta" : " portas") : metros(v)}</span></div>`; }).join("")}</section>
        <section class="stack"><span class="eyebrow">Padrão de acabamento</span><div class="radio-list">${C.padroes.map((p) => `<button class="radio" role="radio" aria-checked="${d.padrao === p.id}" data-action="setPadrao" data-id="${p.id}"><span class="ring"></span><span><b>${esc(p.nome)}</b><span>${esc(p.desc)}</span></span><span class="tag">${p.fator < 1 ? "−" : p.fator > 1 ? "+" : ""}${Math.round(Math.abs(p.fator - 1) * 100) || "base"}${p.fator !== 1 ? " %" : ""}</span></button>`).join("")}</div></section>
        <section class="stack"><span class="eyebrow">Quer incluir</span><div class="radio-list">${C.extras.map((e) => `<button class="radio" role="checkbox" aria-checked="${d.extras.includes(e.id)}" data-action="togExtra" data-id="${e.id}"><span class="ring"></span><span><b>${esc(e.nome)}</b></span><span class="tag">+${Math.round(e.fator * 100)} %</span></button>`).join("")}</div></section>
        <div class="btn-row"><button class="btn" data-action="wizBack">Voltar</button><button class="btn primary" data-action="wizNext">Continuar</button></div>`;
    } else if (step === 2) {
      body = `<div class="hero" style="padding-top:0"><span class="eyebrow">Passo 3 de 4</span><h1>Sobre você e a obra</h1><p class="muted small">Fotos do ambiente e referências do que você gosta aceleram muito o projeto.</p></div>
        <section class="card stack">
          <div class="field"><label for="f-nome">Seu nome</label><input class="input" id="f-nome" data-f="nome" value="${esc(d.nome)}" autocomplete="name"></div>
          <div class="field"><label for="f-tel">WhatsApp</label><input class="input" id="f-tel" data-f="telefone" value="${esc(d.telefone)}" inputmode="tel" autocomplete="tel" placeholder="(44) 9 9999-9999"></div>
          <div class="field"><label for="f-cid">Cidade da obra</label><input class="input" id="f-cid" data-f="cidade" value="${esc(d.cidade)}" placeholder="Ex.: Maringá – PR"></div>
          <div class="field"><label for="f-prazo">Para quando?</label><select class="input" id="f-prazo" data-f="prazo">${Object.keys(PRAZOS).map((k) => `<option value="${k}" ${d.prazo === k ? "selected" : ""}>${PRAZOS[k]}</option>`).join("")}</select></div>
          <div class="field"><label for="f-arq">Tem arquiteto(a)? <span class="muted" style="font-weight:400">opcional</span></label><input class="input" id="f-arq" data-f="arquiteto" value="${esc(d.arquiteto)}" placeholder="Nome ou escritório"></div>
          <div class="field"><label for="f-obs">O que não pode faltar? <span class="muted" style="font-weight:400">opcional</span></label><textarea class="input" id="f-obs" data-f="obs" placeholder="Ex.: quero a geladeira embutida, torre para forno e micro-ondas, LED sob os aéreos…">${esc(d.obs)}</textarea></div>
          <div class="field"><label>Fotos do ambiente e referências</label>
            <label class="upload">${icon("photo")}<br>Toque para escolher fotos (ou prints de inspiração)<input type="file" accept="image/*" multiple id="f-fotos"></label>
            <div class="thumbs" id="thumbs">${d.fotos.map((f) => `<img src="${f}" alt="">`).join("")}</div>
            <span class="help">As fotos ficam só no seu aparelho até você enviar pelo WhatsApp.</span></div>
        </section>
        <div class="btn-row"><button class="btn" data-action="wizBack">Voltar</button><button class="btn primary" data-action="wizNext" ${d.nome && d.telefone ? "" : "disabled"} id="btnStep3">Ver estimativa</button></div>`;
    } else {
      const est = estimar(d);
      body = `<div class="hero" style="padding-top:0"><span class="eyebrow">Passo 4 de 4</span><h1>Sua estimativa</h1></div>
        <div class="estimate"><span class="eyebrow">Faixa de referência · padrão ${esc(est.pad.nome)}</span><div class="range num">${money(est.min)} <small>a</small> ${money(est.max)}</div><p class="small" style="color:var(--accent-ink)">Inclui projeto executivo, produção, entrega e instalação. Não inclui tampos de pedra, eletros, cubas e elétrica/hidráulica.</p></div>
        ${S.precosConfigurados ? "" : `<p class="small muted">Faixas de referência do app. O valor real sai do projeto executivo, depois da medição.</p>`}
        <section class="card">${est.linhas.map((x) => `<div class="summary-line"><span>${esc(x.label)} · ${x.unidade === "porta" ? x.q + " porta(s)" : metros(x.q)}</span><b class="num">${money(x.min)} – ${money(x.max)}</b></div>`).join("")}
          ${d.extras.length ? `<div class="summary-line"><span class="muted">Extras</span><span class="small muted" style="text-align:right">${d.extras.map((id) => esc(C.extras.find((e) => e.id === id).nome)).join(", ")}</span></div>` : ""}
          <div class="summary-line"><span class="muted">Prazo</span><span>${esc(prazoLabel(d.prazo))}</span></div>
        </section>
        <section class="stack">
          <a class="btn accent block" href="${whats(resumoTexto(d, est))}" target="_blank" rel="noopener" data-action="salvarPedido">${icon("whatsapp")} Enviar pedido pelo WhatsApp</a>
          <div class="btn-row"><button class="btn" data-action="copiarResumo">${icon("copy")} Copiar resumo</button><button class="btn" data-action="salvarPedidoSo">Salvar e enviar depois</button></div>
          <p class="small muted">A MP responde em horário comercial com as próximas datas de medição. ${d.fotos.length ? `Depois de abrir o WhatsApp, anexe as ${d.fotos.length} foto(s) escolhidas.` : ""}</p>
        </section>
        <button class="btn ghost block" data-action="wizBack">Voltar e ajustar</button>`;
    }
    const pedidos = S.pedidos.length ? `<section class="card"><div class="card-head"><h3>Seus pedidos salvos</h3></div>${S.pedidos.map((p) => `<div class="pedido"><div><b>${p.ambientes.map((id) => (S.referencia[id] || {}).label).filter(Boolean).join(", ")}</b><br><span class="small muted num">${fmtDate(p.data, true)} · ${money(p.min)} – ${money(p.max)}</span></div><a class="btn sm" href="${whats(p.texto)}" target="_blank" rel="noopener">Enviar</a></div>`).join("")}</section>` : "";
    $("#view-orcamento").innerHTML = `<div class="wizard-head">${dots}${step > 0 || d.ambientes.length ? `<button class="link" data-action="wizReset">Recomeçar</button>` : ""}</div>${body}${step === 0 ? pedidos : ""}`;
  };

  /* ================= INSPIRAÇÕES ================= */
  let filtro = "todos";
  VIEWS.inspiracoes = function () {
    const cats = [["todos", "Todos"]].concat(Object.keys(S.referencia).map((k) => [k, S.referencia[k].label]));
    const itens = C.inspiracoes.filter((i) => filtro === "todos" || i.ambiente === filtro || (filtro === "favoritos" && S.favoritos.includes(i.id)));
    $("#view-inspiracoes").innerHTML = `
      <div class="hero" style="padding-top:0"><span class="eyebrow">Inspirações</span><h1>Projetos que a MP <em>já fez</em>, para você imaginar o seu.</h1></div>
      <div class="filters">${cats.map(([k, l]) => `<button class="chip" aria-pressed="${filtro === k}" data-action="filtro" data-k="${k}">${esc(l)}</button>`).join("")}<button class="chip" aria-pressed="${filtro === "favoritos"}" data-action="filtro" data-k="favoritos">♥ Favoritos${S.favoritos.length ? " · " + S.favoritos.length : ""}</button></div>
      ${itens.length ? `<div class="gallery">${itens.map((i) => `<article class="insp"><canvas data-insp="${i.id}" width="480" height="480" aria-label="${esc(i.titulo)}"></canvas><button class="fav" aria-pressed="${S.favoritos.includes(i.id)}" data-action="fav" data-id="${i.id}" aria-label="Favoritar">${icon("heart")}</button><div class="body"><b>${esc(i.titulo)}</b><div class="tags">${i.tags.map((t) => `<span>${esc(t)}</span>`).join("")}</div><button class="link" data-action="queroAssim" data-amb="${i.ambiente}" style="margin-top:4px">Quero algo assim →</button></div></article>`).join("")}</div>` : `<section class="card" style="text-align:center"><p class="muted">Nenhum favorito ainda. Toque no coração dos projetos que você gostar e eles aparecem aqui e no seu pedido.</p></section>`}
      <section class="card">
        <div class="card-head"><h3>Acabamentos</h3><span class="small muted">toque para marcar os que gostou</span></div>
        <div class="swatches">${C.acabamentos.map((a) => `<button class="swatch" aria-pressed="${(S.favAcab || []).includes(a.id)}" data-action="favAcab" data-id="${a.id}"><canvas data-wood="${a.id}" data-seed="7" width="120" height="120"></canvas>${esc(a.nome)}</button>`).join("")}</div>
        <p class="small muted" style="margin-top:12px">Linhas de MDF de 18 mm com fita de borda na cor da chapa. As amostras reais vão na visita de medição.</p>
      </section>`;
    $$("canvas[data-insp]").forEach((cv) => drawElevation(cv, C.inspiracoes.find((i) => i.id === cv.dataset.insp)));
    $$("canvas[data-wood]", $("#view-inspiracoes")).forEach((cv) => { const a = C.acabamentos.find((x) => x.id === cv.dataset.wood); drawWood(cv, a.cor, a.veio, 7); });
  };

  /* ---------- desenho: madeira e elevações ---------- */
  function rng(seed) { let s = seed * 9301 + 49297; return () => { s = (s * 9301 + 49297) % 233280; return s / 233280; }; }
  function shade(hex, k) { const n = parseInt(hex.slice(1), 16); const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255; const f = (c) => Math.max(0, Math.min(255, Math.round(c * (1 + k)))); return `rgb(${f(r)},${f(g)},${f(b)})`; }
  function drawWood(cv, hex, veio, seed) {
    const ctx = cv.getContext("2d"), w = cv.width, h = cv.height, r = rng(seed || 1);
    ctx.fillStyle = hex; ctx.fillRect(0, 0, w, h);
    if (veio) {
      for (let i = 0; i < 26; i++) { ctx.beginPath(); const x = r() * w * 1.3 - w * .15; ctx.moveTo(x, 0); let xx = x; for (let y = 0; y <= h; y += h / 8) { xx += (r() - .5) * 10; ctx.lineTo(xx, y); } ctx.strokeStyle = shade(hex, (r() - .5) * .35); ctx.lineWidth = .6 + r() * 2.2; ctx.globalAlpha = .55; ctx.stroke(); }
      ctx.globalAlpha = 1;
    } else {
      for (let i = 0; i < 400; i++) { ctx.fillStyle = shade(hex, (r() - .5) * .06); ctx.fillRect(r() * w, r() * h, 2, 2); }
    }
    const g = ctx.createLinearGradient(0, 0, w, h); g.addColorStop(0, "rgba(255,255,255,.10)"); g.addColorStop(1, "rgba(0,0,0,.10)"); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  }
  function drawElevation(cv, item) {
    const ctx = cv.getContext("2d"), W = cv.width, H = cv.height;
    const dark = matchMedia("(prefers-color-scheme: dark)").matches && document.documentElement.getAttribute("data-theme") !== "light" || document.documentElement.getAttribute("data-theme") === "dark";
    ctx.fillStyle = dark ? "#2A2622" : "#EFEAE2"; ctx.fillRect(0, 0, W, H);
    const pad = 36, sc = Math.min((W - 2 * pad) / item.largura, (H - 2 * pad) / item.altura);
    const ox = (W - item.largura * sc) / 2, floorY = H - pad + 10;
    ctx.fillStyle = dark ? "#1E1B18" : "#D9D0C3"; ctx.fillRect(0, floorY, W, H - floorY);
    const X = (x) => ox + x * sc, Y = (y, h) => floorY - (y + h) * sc;
    const r = rng(11);
    item.modulos.forEach((m) => {
      const hex = corAcab(m.cor), x = X(m.x), y = Y(m.y, m.h), w = m.w * sc, h = m.h * sc;
      ctx.fillStyle = hex; ctx.fillRect(x, y, w, h);
      const acab = C.acabamentos.find((a) => a.id === m.cor);
      if (acab && acab.veio) { ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip(); ctx.globalAlpha = .35; for (let i = 0; i < w / 6; i++) { ctx.beginPath(); const xx = x + r() * w; ctx.moveTo(xx, y); ctx.lineTo(xx + (r() - .5) * 6, y + h); ctx.strokeStyle = shade(hex, (r() - .5) * .4); ctx.lineWidth = .8 + r() * 1.5; ctx.stroke(); } ctx.restore(); }
      ctx.strokeStyle = "rgba(0,0,0,.18)"; ctx.lineWidth = 1; ctx.strokeRect(x + .5, y + .5, w - 1, h - 1);
      if (m.painel) { ctx.fillStyle = "rgba(0,0,0,.14)"; for (let xx = x + 6; xx < x + w; xx += 10) ctx.fillRect(xx, y, 2.5, h); return; }
      if (m.tampo) { ctx.fillStyle = "rgba(255,255,255,.35)"; ctx.fillRect(x, y, w, 4); const legY = y + 4, legH = h - 4; ctx.fillStyle = dark ? "#2A2622" : "#EFEAE2"; ctx.fillRect(x + 8, legY + 1, w - 16, legH); ctx.fillStyle = hex; ctx.fillRect(x, legY, 8, legH); ctx.fillRect(x + w - 8, legY, 8, legH); return; }
      if (m.aberto) { ctx.fillStyle = "rgba(0,0,0,.28)"; ctx.fillRect(x + 3, y + 3, w - 6, h - 6); const n = m.nichos || Math.max(2, Math.round(m.h / 400)); const cols = m.nichos ? m.nichos : 1; for (let i = 1; i < n; i++) { ctx.fillStyle = hex; ctx.fillRect(x + 3, y + (h * i) / n, w - 6, 3); } if (m.nichos) for (let i = 1; i < cols; i++) { ctx.fillStyle = hex; ctx.fillRect(x + (w * i) / cols, y + 3, 3, h - 6); } ctx.fillStyle = "rgba(255,220,160,.35)"; ctx.fillRect(x + 3, y + 3, w - 6, 3); return; }
      if (m.torre) { ctx.fillStyle = "rgba(0,0,0,.45)"; const nh = h * .22; ctx.fillRect(x + 4, y + h * .32, w - 8, nh); ctx.fillRect(x + 4, y + h * .32 + nh + 4, w - 8, nh * .7); ctx.fillStyle = "rgba(255,255,255,.08)"; ctx.fillRect(x + 4, y + h * .32 + 4, w - 8, 3); if (m.frentes === 0) { ctx.fillStyle = "rgba(0,0,0,.18)"; ctx.fillRect(x + w / 2 - .75, y, 1.5, h * .3); ctx.fillRect(x + w / 2 - .75, y + h * .75, 1.5, h * .25); } return; }
      if (m.porta) { ctx.strokeStyle = "rgba(0,0,0,.25)"; ctx.lineWidth = 3; ctx.strokeRect(x - 3, y - 3, w + 6, h + 3); ctx.fillStyle = "rgba(0,0,0,.15)"; for (let i = 1; i < 4; i++) ctx.fillRect(x + 6, y + (h * i) / 4, w - 12, 2); ctx.fillStyle = "#9a9a9a"; ctx.fillRect(x + w - 16, y + h * .5, 9, 3); return; }
      const n = m.frentes || 0;
      if (n) {
        const horizontal = m.gavetas || m.h < 500 || (m.h < 800 && m.h < m.w / 1.8 && m.y < 400);
        for (let i = 1; i < n; i++) { ctx.fillStyle = "rgba(0,0,0,.22)"; if (horizontal) ctx.fillRect(x, y + (h * i) / n, w, 1.5); else ctx.fillRect(x + (w * i) / n, y, 1.5, h); }
        ctx.fillStyle = "rgba(0,0,0,.28)";
        if (horizontal) for (let i = 0; i < n; i++) ctx.fillRect(x + w * .2, y + (h * i) / n + 3, w * .6, 2); else ctx.fillRect(x, y + 3, w, 2.5);
      }
    });
    ctx.fillStyle = dark ? "rgba(241,236,229,.55)" : "rgba(43,43,43,.55)"; ctx.font = "500 13px Figtree, sans-serif"; ctx.textAlign = "center";
    ctx.fillText(`${(item.largura / 1000).toLocaleString("pt-BR")} m`, W / 2, H - 8);
    ctx.fillRect(ox, H - 24, item.largura * sc, 1); ctx.fillRect(ox, H - 28, 1, 8); ctx.fillRect(ox + item.largura * sc - 1, H - 28, 1, 8);
  }

  /* ================= MAIS ================= */
  let deferredInstall = null;
  window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); deferredInstall = e; if (location.hash === "#mais") route(); });
  VIEWS.mais = function () {
    const e = C.empresa;
    const item = (ico, t, s, action, right) => `<button class="list-item" data-action="${action}">${`<span class="ico">${icon(ico)}</span>`}<span><b>${esc(t)}</b>${s ? `<small>${esc(s)}</small>` : ""}</span>${right != null ? right : `<span class="chev">${icon("chev")}</span>`}</button>`;
    $("#view-mais").innerHTML = `
      <section class="card">
        <div class="profile"><span class="av">${esc(S.cliente.primeiroNome[0])}</span><div style="min-width:0"><h2>${esc(S.cliente.nome)}</h2><span class="small muted">${esc(S.cliente.cidade)} · código <span class="code">${esc(S.cliente.codigo)}</span></span></div></div>
      </section>
      ${S.oficina ? renderOficina() : ""}
      <section class="card"><div class="list">
        ${item("shield", "Garantia e cuidados", `${e.garantiaMeses / 12} anos de garantia · como cuidar dos móveis`, "openCuidados")}
        ${item("tool", "Assistência técnica", "Regulagem, ajuste ou reparo", "openAssist")}
        ${item("gift", "Indique a MP", "Seu código vale desconto para quem você indicar", "openIndicar")}
        ${deferredInstall ? item("download", "Instalar o app", "Atalho na tela inicial, funciona sem internet", "instalar") : ""}
      </div></section>
      <section class="card"><div class="list">
        <div class="list-item"><span class="ico">${icon("bell")}</span><span><b>Notificações</b><small>Novidades da oficina e lembretes de pagamento</small></span><button class="switch" role="switch" aria-checked="${S.prefs.notif}" data-action="togNotif" aria-label="Notificações"></button></div>
        <div class="list-item"><span class="ico">${icon("moon")}</span><span><b>Aparência</b></span><div class="segmented" style="padding:3px">${[["auto", "Auto"], ["light", "Claro"], ["dark", "Escuro"]].map(([k, l]) => `<button aria-selected="${S.prefs.tema === k}" data-action="tema" data-k="${k}" style="padding:5px 10px">${l}</button>`).join("")}</div></div>
      </div></section>
      <section class="card"><div class="list">
        <a class="list-item" href="${e.instagramUrl}" target="_blank" rel="noopener"><span class="ico">${icon("instagram")}</span><span><b>@${esc(e.instagram)}</b><small>Obras entregues, bastidores da oficina</small></span><span class="chev">${icon("chev")}</span></a>
        <a class="list-item" href="${whats("Olá, MP Marcenaria!")}" target="_blank" rel="noopener"><span class="ico">${icon("whatsapp")}</span><span><b>${esc(e.whatsappExibicao)}</b><small>WhatsApp · horário comercial</small></span><span class="chev">${icon("chev")}</span></a>
        ${item("info", "Sobre a MP Marcenaria", `${e.anos} anos · ${e.cidade}`, "openSobre")}
        ${item("lock", S.oficina ? "Sair do modo oficina" : "Área do marceneiro", S.oficina ? "Voltar à visão do cliente" : "Acesso com PIN", S.oficina ? "sairOficina" : "openPin")}
      </div></section>
      <p class="small muted" style="text-align:center">${esc(e.nome)} · CNPJ ${esc(e.cnpj)} · ${esc(e.email)}<br>Versão 1.0 · <button class="link" data-action="resetDemo">redefinir dados de demonstração</button></p>`;
  };
  function renderOficina() {
    const p = S.projeto;
    return `<section class="card" style="border-color:var(--warn)">
      <div class="banner">${icon("tool")} Modo oficina ativo: o que você muda aqui o cliente vê na hora.</div>
      <div class="stack" style="margin-top:14px">
        <div class="field"><label for="of-etapa">Etapa atual do projeto</label><select class="input" id="of-etapa" data-of="etapaAtual">${C.etapas.map((e) => `<option value="${e.id}" ${p.etapaAtual === e.id ? "selected" : ""}>${esc(e.nome)}</option>`).join("")}</select></div>
        <div class="field"><label for="of-prog">Progresso: <span id="of-prog-v" class="num">${p.progresso}%</span></label><input type="range" id="of-prog" min="0" max="100" step="1" value="${p.progresso}" data-of="progresso"></div>
        <div class="field"><label for="of-prev">Previsão de entrega</label><input class="input" type="date" id="of-prev" value="${p.previsaoEntrega}" data-of="previsaoEntrega"></div>
        <div class="field"><label>Parcelas pagas</label><div class="btn-row">${p.pagamentos.map((x) => `<button class="btn sm ${x.pago ? "primary" : ""}" data-action="togPago" data-n="${x.n}">${x.n}ª ${x.pago ? "paga" : "em aberto"}</button>`).join("")}</div></div>
        <div class="field"><label for="of-upd">Nova atualização da oficina</label><input class="input" id="of-upd-t" placeholder="Título (ex.: Montagem dos aéreos)"><textarea class="input" id="of-upd" placeholder="O que aconteceu hoje, em uma ou duas frases."></textarea><button class="btn sm" data-action="publicarUpd">Publicar para o cliente</button></div>
        <details class="acc"><summary>Faixas de referência da estimativa (R$ por metro / porta)</summary>
          <table class="ref-table"><thead><tr><th>Ambiente</th><th>Mín.</th><th>Máx.</th></tr></thead><tbody>${Object.keys(S.referencia).map((k) => `<tr><td>${esc(S.referencia[k].label)}</td><td><input class="input num" type="number" step="50" value="${S.referencia[k].min}" data-ref="${k}" data-k="min" style="min-height:36px;padding:4px 8px"></td><td><input class="input num" type="number" step="50" value="${S.referencia[k].max}" data-ref="${k}" data-k="max" style="min-height:36px;padding:4px 8px"></td></tr>`).join("")}</tbody></table>
          <label class="check" style="margin-top:8px"><input type="checkbox" id="of-conf" ${S.precosConfigurados ? "checked" : ""}><span>Faixas revisadas pela MP (remove o aviso de referência no app)</span></label>
        </details>
      </div></section>`;
  }

  /* ---------- sheets do "Mais" ---------- */
  function sheetCuidados() {
    openSheet(`${sheetHead("Garantia e cuidados")}
      <div class="why"><div><b>${C.empresa.garantiaMeses / 12} anos</b><span>estrutura, fita de borda e ferragens, em uso residencial normal</span></div><div><b>${C.empresa.assistenciaMeses} meses</b><span>de regulagem de portas e gavetas sem custo</span></div></div>
      <p class="small muted">A garantia não cobre danos por água parada, mau uso, excesso de peso, mudanças feitas por terceiros ou produtos abrasivos. Guarde este app: ele é seu comprovante de entrega.</p>
      <div>${C.cuidados.map((c) => `<details class="acc"><summary>${esc(c.t)}</summary><p>${esc(c.d)}</p></details>`).join("")}</div>`);
  }
  function sheetAssist() {
    openSheet(`${sheetHead("Assistência técnica")}
      <p class="small muted">Conte o que está acontecendo. Se puder, mande uma foto ou um vídeo curto pelo WhatsApp depois de enviar.</p>
      <div class="field"><label for="as-amb">Ambiente</label><select class="input" id="as-amb">${S.projeto.ambientes.map((a) => `<option>${esc(a.nome)}</option>`).join("")}<option>Outro</option></select></div>
      <div class="field"><label for="as-tipo">O que precisa</label><select class="input" id="as-tipo"><option>Porta desalinhada ou batendo</option><option>Gaveta não fecha suave</option><option>Prateleira ou peça solta</option><option>Fita de borda descolando</option><option>LED não acende</option><option>Outro</option></select></div>
      <div class="field"><label for="as-desc">Descreva</label><textarea class="input" id="as-desc" placeholder="Ex.: a porta da direita do aéreo ficou mais baixa que a da esquerda."></textarea></div>
      <button class="btn accent block" data-action="enviarAssist">${icon("whatsapp")} Enviar pelo WhatsApp</button>`);
  }
  function sheetIndicar() {
    const txt = `Fiz meus móveis planejados com a MP Marcenaria (@${C.empresa.instagram}) e recomendo. Diga que foi indicação de ${S.cliente.primeiroNome}, código ${S.cliente.codigo}, quando pedir seu orçamento: https://wa.me/${C.empresa.whatsapp}`;
    openSheet(`${sheetHead("Indique a MP")}
      <p>Quem você indicar ganha condição especial na primeira proposta, e você ganha um crédito em assistência ou no próximo ambiente. Basta a pessoa citar seu código.</p>
      <div class="estimate"><span class="eyebrow">Seu código de indicação</span><div class="range" style="font-size:30px">${esc(S.cliente.codigo)}</div></div>
      <div class="btn-row"><button class="btn primary" data-action="copyIndicar">${icon("copy")} Copiar mensagem</button><a class="btn" href="https://wa.me/?text=${encodeURIComponent(txt)}" target="_blank" rel="noopener">${icon("whatsapp")} Compartilhar</a></div>`);
    $("#sheetRoot")._txt = txt;
  }
  function sheetSobre() {
    const e = C.empresa;
    openSheet(`${sheetHead("Sobre a MP Marcenaria")}
      <p>Há ${e.anos} anos a MP projeta e produz móveis planejados, móveis prontos, esquadrias de madeira e kit porta pronta de alto padrão em ${esc(e.cidade)}. Atendemos ${e.atende.toLowerCase()}.</p>
      <p>Trabalhamos com projeto 3D aprovado antes do primeiro corte, remedição técnica com piso e forro prontos e instalação pela própria equipe. Cada projeto nasce de uma ficha de medição completa: paredes em três alturas, pontos de água, luz e gás, e o modelo de cada eletrodoméstico.</p>
      <div class="list">
        <a class="list-item" href="${e.instagramUrl}" target="_blank" rel="noopener"><span class="ico">${icon("instagram")}</span><span><b>@${esc(e.instagram)}</b><small>Instagram</small></span><span class="chev">${icon("chev")}</span></a>
        <div class="list-item"><span class="ico">${icon("pin")}</span><span><b>${esc(e.cidade)}</b><small>${esc(e.atende)}</small></span><span></span></div>
        <div class="list-item"><span class="ico">${icon("doc")}</span><span><b>CNPJ ${esc(e.cnpj)}</b><small>${esc(e.email)}</small></span><span></span></div>
      </div>`);
  }
  function sheetNotif() {
    openSheet(`${sheetHead("Notificações")}
      ${S.notificacoes.length ? `<div>${S.notificacoes.map((n) => `<div class="notif ${n.lida ? "read" : ""}"><span class="mark"></span><div><b>${esc(n.titulo)}</b><span class="small muted">${esc(n.texto)}</span></div><small class="num">${fmtDate(n.data)}</small></div>`).join("")}</div>` : `<p class="muted">Nada por aqui ainda.</p>`}
      ${naoLidas() ? `<button class="btn block" data-action="lerTodas">Marcar todas como lidas</button>` : ""}`);
  }
  function sheetPin() {
    openSheet(`${sheetHead("Área do marceneiro")}
      <p class="small muted">Digite o PIN da MP para atualizar o andamento, pagamentos e as faixas de referência que o cliente vê.</p>
      <div class="pin">${[0, 1, 2, 3].map((i) => `<input inputmode="numeric" maxlength="1" class="pin-d" aria-label="Dígito ${i + 1}" id="pin-${i}">`).join("")}</div>
      <p class="small muted" id="pinMsg" style="text-align:center;min-height:1.4em"></p>`,
      (root) => {
        const ds = $$(".pin-d", root); ds[0].focus();
        ds.forEach((d, i) => d.addEventListener("input", () => { d.value = d.value.replace(/\D/g, "").slice(-1); if (d.value && ds[i + 1]) ds[i + 1].focus(); const pin = ds.map((x) => x.value).join(""); if (pin.length === 4) { if (pin === C.pinOficina) { S.oficina = true; save(); closeSheet(); toast("Modo oficina ativado"); route(); } else { $("#pinMsg", root).textContent = "PIN incorreto."; ds.forEach((x) => { x.value = ""; }); ds[0].focus(); } } }));
      });
  }

  /* ================= ações (delegação) ================= */
  const A = {
    closeSheet: (el, e) => { if (el.classList.contains("sheet-backdrop") && e.target.closest("[data-stop]")) return; closeSheet(); },
    openNotif: () => { sheetNotif(); },
    lerTodas: () => { S.notificacoes.forEach((n) => { n.lida = true; }); save(); closeSheet(); route(); toast("Tudo lido"); },
    goProjeto3d: () => { go("projeto"); viewer3dOpen = true; setTimeout(() => { route(); const c = $("#card3d"); if (c) c.scrollIntoView({ behavior: "smooth", block: "start" }); }, 30); },
    goPagamentos: () => { go("projeto"); setTimeout(() => { const c = $("#cardPag"); if (c) c.scrollIntoView({ behavior: "smooth", block: "start" }); }, 30); },
    open3d: () => { viewer3dOpen = true; VIEWS.projeto(); const c = $("#card3d"); if (c) c.scrollIntoView({ behavior: "smooth", block: "start" }); },
    amb3d: (el) => { ambSel = Number(el.dataset.i); viewer3dOpen = true; VIEWS.projeto(); },
    vista: (el) => { if (!viewer3dOpen) A.open3d(); if (viewer) viewer.fit(el.dataset.v); },
    portas: (el) => { if (!viewer3dOpen) A.open3d(); if (viewer) { viewer.setOpen(!viewer.open); const chip = $("#chipPortas"); chip.setAttribute("aria-pressed", String(viewer.open)); chip.textContent = viewer.open ? "Fechar portas" : "Abrir portas"; } },
    aprovar: (el) => abrirAprovacao(Number(el.dataset.i)),
    signClear: () => { const r = $("#sheetRoot").firstElementChild; if (r && r._sign) r._sign.clear(); },
    confirmarAprovacao: (el) => {
      const i = Number(el.dataset.i), a = S.projeto.ambientes[i]; const r = $("#sheetRoot").firstElementChild;
      a.aprovado = true; a.status = "Aprovado"; a.detalhe = "Aguardando remedição técnica para entrar em produção.";
      S.aprovacoes[a.nome] = { data: todayISO(), assinatura: r && r._sign ? r._sign.data() : null, nome: S.cliente.nome };
      S.projeto.historico.push({ data: todayISO(), etapa: "aprovacao", texto: `${a.nome} aprovada por ${S.cliente.nome} no app.` });
      addNotif("Aprovação registrada", `${a.nome} aprovada. A MP vai confirmar a data da remedição.`);
      save(); closeSheet(); route(); toast(`${a.nome} aprovada. Obrigado!`);
    },
    pix: () => copyText(C.empresa.pixChave, "Chave Pix copiada"),
    togAmb: (el) => { const d = S.draft, id = el.dataset.id; d.ambientes = d.ambientes.includes(id) ? d.ambientes.filter((x) => x !== id) : d.ambientes.concat(id); save(); VIEWS.orcamento(); },
    setPadrao: (el) => { S.draft.padrao = el.dataset.id; save(); VIEWS.orcamento(); },
    togExtra: (el) => { const d = S.draft, id = el.dataset.id; d.extras = d.extras.includes(id) ? d.extras.filter((x) => x !== id) : d.extras.concat(id); save(); VIEWS.orcamento(); },
    wizNext: () => { S.draft.step = Math.min(3, S.draft.step + 1); save(); VIEWS.orcamento(); window.scrollTo(0, 0); },
    wizBack: () => { S.draft.step = Math.max(0, S.draft.step - 1); save(); VIEWS.orcamento(); window.scrollTo(0, 0); },
    wizReset: () => { S.draft = newDraft(); save(); VIEWS.orcamento(); },
    copiarResumo: () => copyText(resumoTexto(S.draft, estimar(S.draft)), "Resumo copiado"),
    salvarPedido: () => { salvarPedido(); toast("Pedido salvo. Abrindo o WhatsApp…"); },
    salvarPedidoSo: () => { salvarPedido(); S.draft = newDraft(); save(); VIEWS.orcamento(); toast("Pedido salvo em Orçamento"); },
    filtro: (el) => { filtro = el.dataset.k; VIEWS.inspiracoes(); },
    fav: (el) => { const id = el.dataset.id; S.favoritos = S.favoritos.includes(id) ? S.favoritos.filter((x) => x !== id) : S.favoritos.concat(id); save(); VIEWS.inspiracoes(); },
    favAcab: (el) => { const id = el.dataset.id; S.favAcab = S.favAcab || []; S.favAcab = S.favAcab.includes(id) ? S.favAcab.filter((x) => x !== id) : S.favAcab.concat(id); if (S.draft) S.draft.acabamentos = S.favAcab; save(); VIEWS.inspiracoes(); },
    queroAssim: (el) => { if (!S.draft) S.draft = newDraft(); if (!S.draft.ambientes.includes(el.dataset.amb)) S.draft.ambientes.push(el.dataset.amb); S.draft.step = 0; save(); go("orcamento"); toast(`${S.referencia[el.dataset.amb].label} adicionado ao seu pedido`); },
    openCuidados: sheetCuidados, openAssist: sheetAssist, openIndicar: sheetIndicar, openSobre: sheetSobre, openPin: sheetPin,
    copyIndicar: () => copyText($("#sheetRoot")._txt, "Mensagem copiada"),
    enviarAssist: () => { const amb = $("#as-amb").value, tipo = $("#as-tipo").value, desc = $("#as-desc").value.trim(); const txt = `*Assistência técnica — ${C.empresa.nome}*\nCliente: ${S.cliente.nome} (${S.cliente.codigo})\nProjeto: ${S.projeto.id}\nAmbiente: ${amb}\nProblema: ${tipo}${desc ? "\nDescrição: " + desc : ""}`; addNotif("Assistência solicitada", `${tipo} em ${amb}. A MP responde em horário comercial.`); save(); openSheet(`${sheetHead("Pedido pronto")}<p>Seu pedido de assistência está montado. Abra o WhatsApp para enviar; se puder, anexe uma foto ou um vídeo curto do problema.</p><section class="card"><p class="small" style="white-space:pre-wrap">${esc(txt)}</p></section><div class="btn-row"><a class="btn accent" href="${whats(txt)}" target="_blank" rel="noopener">${icon("whatsapp")} Abrir WhatsApp</a><button class="btn" data-action="copyAssist">${icon("copy")} Copiar</button></div>`); $("#sheetRoot")._txt = txt; },
    copyAssist: () => copyText($("#sheetRoot")._txt, "Mensagem copiada"),
    togNotif: () => { S.prefs.notif = !S.prefs.notif; save(); VIEWS.mais(); },
    tema: (el) => { S.prefs.tema = el.dataset.k; save(); applyTheme(); VIEWS.mais(); if (viewer && viewer3dOpen) viewer.load(C.demo.projeto3d.ambientes[ambSel]); },
    instalar: async () => { if (!deferredInstall) return; deferredInstall.prompt(); try { await deferredInstall.userChoice; } catch (e) { } deferredInstall = null; VIEWS.mais(); },
    sairOficina: () => { S.oficina = false; save(); route(); toast("Visão do cliente"); },
    togPago: (el) => { const x = S.projeto.pagamentos.find((p) => p.n === Number(el.dataset.n)); x.pago = !x.pago; if (x.pago) delete S.comprovantes[x.n]; save(); VIEWS.mais(); },
    publicarUpd: () => { const t = $("#of-upd-t").value.trim(), tx = $("#of-upd").value.trim(); if (!t) { toast("Dê um título à atualização"); return; } S.projeto.atualizacoes.unshift({ data: todayISO(), titulo: t, texto: tx, cor: ["carvalho", "branco", "grafite", "nogueira"][S.projeto.atualizacoes.length % 4] }); addNotif(t, tx || "Nova atualização da oficina."); save(); VIEWS.mais(); toast("Publicado para o cliente"); },
    resetDemo: () => { openSheet(`${sheetHead("Redefinir dados")}<p>Isso apaga aprovações, pedidos salvos, favoritos e ajustes da oficina neste aparelho e volta aos dados de demonstração.</p><div class="btn-row"><button class="btn" data-action="closeSheet">Cancelar</button><button class="btn primary" data-action="resetDemoOk">Redefinir</button></div>`); },
    resetDemoOk: () => { try { localStorage.removeItem(KEY); } catch (e) { } S = defaults(); applyTheme(); closeSheet(); route(); toast("Dados redefinidos"); }
  };
  function salvarPedido() { const d = S.draft, est = estimar(d); S.pedidos.unshift({ data: todayISO(), ambientes: d.ambientes.slice(), min: est.min, max: est.max, texto: resumoTexto(d, est) }); S.cliente.nome = d.nome || S.cliente.nome; S.cliente.primeiroNome = (d.nome || S.cliente.nome).split(" ")[0]; S.cliente.telefone = d.telefone || S.cliente.telefone; S.cliente.cidade = d.cidade || S.cliente.cidade; save(); }

  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-action]"); if (!el) return;
    const fn = A[el.dataset.action]; if (!fn) return;
    if (el.tagName === "BUTTON") e.preventDefault();
    fn(el, e);
  });
  $("#btnNotif").addEventListener("click", sheetNotif);
  document.addEventListener("input", (e) => {
    const t = e.target;
    if (t.dataset.med) { const id = t.dataset.med; const v = Number(t.value); S.draft.medidas[id] = v; const r = S.referencia[id]; $("#val-" + id).textContent = r.unidade === "porta" ? v + (v === 1 ? " porta" : " portas") : metros(v); save(); }
    if (t.dataset.f) { S.draft[t.dataset.f] = t.value; save(); const b = $("#btnStep3"); if (b) b.disabled = !(S.draft.nome && S.draft.telefone); }
    if (t.dataset.of) { const k = t.dataset.of; S.projeto[k] = k === "progresso" ? Number(t.value) : t.value; if (k === "progresso") $("#of-prog-v").textContent = t.value + "%"; if (k === "etapaAtual" && !S.projeto.historico.some((h) => h.etapa === t.value && h.data === todayISO())) { S.projeto.historico.push({ data: todayISO(), etapa: t.value, texto: `Projeto avançou para "${C.etapas[etapaIdx(t.value)].nome}".` }); addNotif("Seu projeto avançou", `Agora em: ${C.etapas[etapaIdx(t.value)].nome}.`); } save(); }
    if (t.dataset.ref) { S.referencia[t.dataset.ref][t.dataset.k] = Number(t.value) || 0; save(); }
    if (t.id === "of-conf") { S.precosConfigurados = t.checked; save(); }
  });
  document.addEventListener("change", (e) => {
    const t = e.target;
    if (t.id === "f-fotos") { const files = Array.from(t.files || []).slice(0, 8); files.forEach((f) => { const rd = new FileReader(); rd.onload = () => { S.draft.fotos.push(rd.result); const th = $("#thumbs"); if (th) th.insertAdjacentHTML("beforeend", `<img src="${rd.result}" alt="">`); }; rd.readAsDataURL(f); }); }
    if (t.dataset.comp) { const n = Number(t.dataset.comp); const f = t.files && t.files[0]; if (!f) return; S.comprovantes[n] = { data: todayISO(), nome: f.name }; addNotif("Comprovante recebido", `Comprovante da ${n}ª parcela em análise pela MP.`); save(); VIEWS.projeto(); toast("Comprovante enviado para análise"); }
  });
  window.addEventListener("hashchange", route);
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => route());

  /* PWA (ignorado onde service worker não é permitido) */
  try { if ("serviceWorker" in navigator && location.protocol.startsWith("http")) navigator.serviceWorker.register("sw.js").catch(() => { }); } catch (e) { }

  route();
})();
