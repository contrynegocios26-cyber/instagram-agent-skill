#!/usr/bin/env python3
"""Catalogo de referencias de mercado: molas por setor e por implemento, com codigo original.

Le arquivos JSON (lista de registros) e gera um HTML A4 pronto para PDF, mais um CSV de
conferencia com a fonte de cada linha.

Campos de cada registro: setor, maquina, marca, modelos, peca_pt, peca_original,
codigo_original, ref_aftermarket, arame_mm, comprimento_mm, espira_mm, obs, fonte.

Uso:
  python referencias.py --dados PASTA_JSON --saida PASTA [--logo logo.png] [--whatsapp 55DDDNUMERO]
        [--telefone "(DD) 0000-0000"] [--email x@y] [--site dominio] [--data mm/aaaa]
  node pdf.js PASTA
Nada e inventado: registro sem codigo (original ou de reposicao) ou sem fonte fica de fora.
"""
import argparse
import base64
import csv
import glob
import html
import io
import json
import os
import re
import unicodedata

E = html.escape
ORDEM = ["Fenação e forragem", "Cana-de-açúcar", "Amendoim", "Plantio", "Preparo de solo", "Colheita de grãos",
         "Pulverização e distribuição", "Roçadeiras e transmissões"]
RESUMO = {
    "Fenação e forragem": "Dentes, dedos e garfos de enleiradores, espalhadores, ancinhos e enfardadeiras.",
    "Cana-de-açúcar": "Dedos de enleiradores de palha e molas de colhedoras, plantadoras e transbordos.",
    "Amendoim": "Dedos e molas de arrancadores-invertedores e recolhedoras.",
    "Plantio": "Molas da linha, do disco de corte, do sulcador, das rodas e do marcador de plantadeiras e semeadoras.",
    "Preparo de solo": "Molas de limpadores, de desarme de hastes e hastes flexíveis de grades, subsoladores e cultivadores.",
    "Colheita de grãos": "Dedos de molinete, dedos retráteis e molas de plataformas e colheitadeiras.",
    "Pulverização e distribuição": "Molas de barras, válvulas e bicos de pulverizadores; molas de distribuidores.",
    "Roçadeiras e transmissões": "Molas de embreagens, esticadores e flutuação de roçadeiras, segadoras e cardans.",
}


def chave(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def limpo(v):
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        v = ", ".join(str(x) for x in v if x)
    return re.sub(r"\s+", " ", str(v)).strip()


def carregar(pasta):
    reg, descartados = [], 0
    for arq in sorted(glob.glob(os.path.join(pasta, "*.json"))):
        with open(arq, encoding="utf-8") as f:
            dados = json.load(f)
        for r in dados:
            r = {k: limpo(r.get(k)) for k in ("setor", "maquina", "marca", "modelos", "peca_pt", "peca_original",
                                              "codigo_original", "ref_aftermarket", "arame_mm", "comprimento_mm",
                                              "espira_mm", "obs", "fonte")}
            if not (r["codigo_original"] or r["ref_aftermarket"]) or not r["fonte"] or not r["marca"]:
                descartados += 1
                continue
            r["peca"] = r["peca_pt"] or r["peca_original"]
            reg.append(r)
    vistos, unicos = set(), []
    for r in reg:
        k = (chave(r["marca"]), chave(r["codigo_original"] or r["ref_aftermarket"]), chave(r["maquina"]))
        if k in vistos:
            continue
        vistos.add(k)
        unicos.append(r)
    return unicos, descartados + len(reg) - len(unicos)


def medidas(r):
    p = []
    for campo, rot in (("arame_mm", "arame"), ("comprimento_mm", "compr."), ("espira_mm", "espira")):
        v = r[campo]
        if v:
            p.append("%s %s%s" % (rot, v, "" if re.search(r"[a-zA-Z\"]", v) else " mm"))
    return " · ".join(p)


def desenho(maquina, peca):
    """Icone esquematico pelo tipo de peca (SVG simples, traco preto)."""
    t = chave(peca + " " + maquina)
    if any(x in t for x in ("dedo", "dente", "garfo", "tine", "haste")):
        return '<svg viewBox="0 0 60 36"><circle cx="14" cy="13" r="7"/><circle cx="14" cy="13" r="3.5"/><path d="M19 18 L56 32"/><path d="M14 6 L14 2 L6 2"/></svg>'
    if "tracao" in t or "tração" in peca.lower():
        return '<svg viewBox="0 0 60 36"><circle cx="8" cy="18" r="5"/><polyline points="13,18 17,8 21,28 25,8 29,28 33,8 37,28 41,8 45,28 47,18"/><circle cx="52" cy="18" r="5"/></svg>'
    if "torcao" in t or "grampo" in t:
        return '<svg viewBox="0 0 60 36"><circle cx="26" cy="20" r="10"/><circle cx="26" cy="20" r="6"/><path d="M26 10 L56 10"/><path d="M18 26 L4 34"/></svg>'
    return '<svg viewBox="0 0 60 36"><polyline points="8,6 52,9 8,13 52,17 8,21 52,25 8,29 52,32"/><path d="M8 4 H52 M8 34 H52"/></svg>'


CSS = """
@page{size:A4;margin:14mm 13mm 17mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font:9.6pt/1.4 Inter,"DejaVu Sans",Arial,sans-serif;color:#1d2320}
:root{--verde:#0b5a1e;--verde2:#2c9a45;--amarelo:#ffd800;--cinza:#5b665f;--linha:#cfd6d0;--fundo:#f3f5f2}
h1,h2,h3{font-family:"Inter Display",Inter,Arial,sans-serif;margin:0;line-height:1.1}
.capa{height:266mm;margin:-14mm -13mm 0;padding:22mm 18mm;background:var(--verde);color:#fff;position:relative;page-break-after:always}
.capa .logo{background:#fff;border-radius:2mm;padding:3mm 4mm;display:inline-block}.capa .logo img{height:22mm;display:block}
.capa .ed{position:absolute;top:24mm;right:18mm;text-align:right;font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;font-weight:700}
.capa .cont{position:absolute;left:18mm;right:18mm;bottom:24mm}
.capa h1{font-size:44pt;font-weight:800;letter-spacing:-.01em}
.capa p{font-size:14pt;max-width:135mm;margin:5mm 0 0}
.faixa{display:block;width:16mm;height:2.4mm;background:var(--amarelo);margin:0 0 5mm}
.nums{display:flex;gap:10mm;margin-top:12mm}.nums b{display:block;font:800 30pt/1 "Inter Display",Inter,Arial}.nums span{font-size:9.5pt;opacity:.9}
.pagina{page-break-after:always}
h2{font-size:21pt;font-weight:800;color:var(--verde)}
.olho{font-size:8pt;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--verde2);margin-bottom:1.2mm}
.setor{page-break-before:always;background:var(--verde);color:#fff;margin:0 -13mm 6mm;padding:9mm 13mm 8mm;display:flex;justify-content:space-between;align-items:flex-end;gap:8mm}
.setor h2{color:#fff;font-size:26pt}.setor p{margin:2mm 0 0;font-size:10.5pt;max-width:120mm;opacity:.95}
.setor .n{font:800 46pt/0.9 "Inter Display",Inter,Arial;color:var(--amarelo)}
.maq{margin:0 0 7mm}
.maq h3{font-size:13pt;font-weight:700;display:flex;align-items:center;gap:3mm;margin:0 0 2mm;page-break-after:avoid}
.maq h3 svg{width:15mm;height:9mm;fill:none;stroke:#1d2320;stroke-width:1.6;flex:none}
.maq h3 small{font:500 8.5pt Inter,Arial;color:var(--cinza);margin-left:auto}
table{border-collapse:collapse;width:100%;font-size:8.7pt;line-height:1.3}
thead{display:table-header-group}
th{background:#e6ebe6;text-align:left;padding:1.6mm 1.8mm;font-weight:700;font-size:7.8pt;letter-spacing:.03em;text-transform:uppercase;color:#2f3a34;border-bottom:.4mm solid var(--verde)}
td{padding:1.7mm 1.8mm;border-bottom:.2mm solid var(--linha);vertical-align:top}
tr{page-break-inside:avoid}
td.cod{font:600 8.8pt "JetBrains Mono","DejaVu Sans Mono",monospace;white-space:nowrap;color:var(--verde)}
td.cod small{display:block;font:400 7.4pt Inter,Arial;color:var(--cinza);white-space:normal}
td.marca{font-weight:700;white-space:nowrap}
.orig{display:block;font-size:7.6pt;color:var(--cinza)}
.cx{background:var(--fundo);border-radius:2mm;padding:4.5mm;page-break-inside:avoid}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:7mm}
ul{margin:0 0 2mm;padding-left:4.5mm}li{margin-bottom:1.1mm}
.idx{columns:3;column-gap:6mm;font-size:8pt;line-height:1.5}
.idx div{break-inside:avoid}.idx b{font-family:"JetBrains Mono","DejaVu Sans Mono",monospace;color:var(--verde)}
.campo{display:flex;gap:2mm;align-items:flex-end;margin-bottom:5mm}.campo i{flex:1;border-bottom:.25mm solid #7d8a82;height:4mm}
"""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dados", required=True)
    p.add_argument("--saida", required=True)
    p.add_argument("--logo", default="")
    p.add_argument("--empresa", default="Jardmolas")
    p.add_argument("--whatsapp", default="")
    p.add_argument("--telefone", default="")
    p.add_argument("--email", default="")
    p.add_argument("--site", default="")
    p.add_argument("--data", default="")
    a = p.parse_args()
    reg, fora = carregar(a.dados)
    setores = [s for s in ORDEM if any(r["setor"] == s for r in reg)] + sorted(
        {r["setor"] for r in reg if r["setor"] not in ORDEM})
    logo = ""
    if a.logo and os.path.exists(a.logo):
        with open(a.logo, "rb") as f:
            logo = "data:image/png;base64," + base64.b64encode(f.read()).decode()
    z = re.sub(r"\D", "", a.whatsapp)
    zap = "(%s) %s-%s" % (z[2:4], z[4:9], z[9:]) if len(z) == 13 else a.whatsapp
    marcas = sorted({r["marca"] for r in reg}, key=chave)
    H = []
    H.append('<section class="capa">%s<div class="ed">Catálogo de referências<br>%s</div><div class="cont"><span class="faixa"></span>'
             '<h1>Molas para implementos agrícolas</h1><p>Por setor, por implemento e por máquina — com o código original de cada peça.</p>'
             '<div class="nums"><div><b>%d</b><span>peças com código</span></div><div><b>%d</b><span>marcas de máquinas</span></div>'
             '<div><b>%d</b><span>setores</span></div></div></div></section>' % (
                 '<div class="logo"><img src="%s" alt="%s"></div>' % (logo, E(a.empresa)) if logo else "<h2 style='color:#fff'>%s</h2>" % E(a.empresa),
                 E(a.data), len(reg), len(marcas), len(setores)))
    linhas_idx = "".join("<tr><td><b>%02d</b></td><td><b>%s</b></td><td>%s</td><td style='text-align:right'>%d</td></tr>" % (
        i, E(s), E(RESUMO.get(s, "")), sum(1 for r in reg if r["setor"] == s)) for i, s in enumerate(setores, 1))
    H.append('<section class="pagina"><div class="olho">Como usar</div><h2>Ache a mola pela sua máquina</h2><span class="faixa" style="margin-top:3mm"></span>'
             '<div class="cols2"><div><p>Cada seção é um setor; dentro dela, cada bloco é um tipo de implemento. As linhas trazem a <b>marca</b> e o <b>modelo</b> '
             'da máquina, o <b>nome da peça</b>, o <b>código original</b> do fabricante da máquina e, quando publicadas, as <b>medidas</b>.</p>'
             '<p>Com o código original em mãos, peça a cotação: fabricamos a mola equivalente a partir do código, do desenho ou de uma amostra.</p></div>'
             '<div class="cx"><b>Para pedir, informe:</b><ul><li>marca e modelo da máquina;</li><li>código original da peça (desta tabela ou gravado na peça);</li>'
             '<li>quantidade;</li><li>se possível, uma foto da peça ao lado de uma régua.</li></ul>%s</div></div>'
             '<h3 style="font-size:13pt;margin:8mm 0 2mm">Conteúdo</h3><table><thead><tr><th style="width:8%%">Seção</th><th style="width:27%%">Setor</th><th>O que traz</th><th style="width:10%%;text-align:right">Peças</th></tr></thead><tbody>%s</tbody></table>'
             '<p style="font-size:8pt;color:var(--cinza);margin-top:6mm">Marcas, modelos e códigos originais pertencem aos respectivos fabricantes e são citados exclusivamente como referência de aplicação. '
             'As peças fornecidas pela %s são de fabricação própria e não são peças originais dos fabricantes das máquinas. Códigos e medidas reunidos de catálogos e anúncios públicos de peças de reposição; confirme a aplicação pelo modelo e pelo número de série da sua máquina antes de pedir.</p></section>' % (
                 "<b>WhatsApp:</b> %s" % E(zap) if zap else "", linhas_idx, E(a.empresa)))
    for i, s in enumerate(setores, 1):
        do_setor = [r for r in reg if r["setor"] == s]
        H.append('<div class="setor"><div><div class="olho" style="color:var(--amarelo)">Seção %02d</div><h2>%s</h2><p>%s</p></div><div class="n">%02d</div></div>' % (
            i, E(s), E(RESUMO.get(s, "")), i))
        maqs = {}
        for r in do_setor:
            maqs.setdefault(r["maquina"] or "Outros", []).append(r)
        for nome in sorted(maqs, key=lambda n: (-len(maqs[n]), chave(n))):
            rs = sorted(maqs[nome], key=lambda r: (chave(r["marca"]), chave(r["modelos"]), chave(r["peca"])))
            corpo = ""
            for r in rs:
                cod = E(r["codigo_original"] or "—")
                if r["ref_aftermarket"]:
                    cod += "<small>ref. reposição %s</small>" % E(r["ref_aftermarket"])
                peca = E(r["peca"])
                if r["peca_original"] and chave(r["peca_original"]) != chave(r["peca"]):
                    peca += '<span class="orig">%s</span>' % E(r["peca_original"])
                corpo += "<tr><td class='marca'>%s</td><td>%s</td><td>%s</td><td class='cod'>%s</td><td>%s</td></tr>" % (
                    E(r["marca"]), E(r["modelos"] or "—"), peca, cod, E(" · ".join(x for x in (medidas(r), r["obs"]) if x)))
            H.append('<div class="maq"><h3>%s%s<small>%d %s</small></h3><table><thead><tr><th style="width:14%%">Marca</th><th style="width:21%%">Modelo da máquina</th>'
                     '<th style="width:25%%">Peça</th><th style="width:17%%">Código original</th><th>Medidas e observações</th></tr></thead><tbody>%s</tbody></table></div>' % (
                         desenho(nome, rs[0]["peca"]), E(nome[:1].upper() + nome[1:]), len(rs), "peça" if len(rs) == 1 else "peças", corpo))
    # indice de codigos
    idx = []
    for r in reg:
        for c in re.split(r"[,;/]| ou ", r["codigo_original"]):
            c = c.strip()
            if len(c) >= 4:
                idx.append((c, r))
    idx.sort(key=lambda x: chave(x[0]))
    H.append('<section style="page-break-before:always"><div class="olho">Índice</div><h2>Códigos originais</h2><span class="faixa" style="margin-top:3mm"></span>'
             '<div class="idx">%s</div></section>' % "".join(
                 "<div><b>%s</b> %s · %s</div>" % (E(c), E(r["marca"]), E(r["peca"][:38])) for c, r in idx))
    H.append('<section style="page-break-before:always"><div class="olho">Pedido</div><h2>Não achou sua máquina?</h2><span class="faixa" style="margin-top:3mm"></span>'
             '<p style="font-size:11pt;max-width:150mm">Fabricamos molas de compressão, tração e torção, dedos e garfos a partir do código original, do desenho ou de uma amostra — em qualquer quantidade.</p>'
             '<div class="cx" style="margin-top:6mm">%s</div><p style="margin-top:8mm;font-size:11pt">%s</p></section>' % (
                 "".join('<div class="campo"><span>%s</span><i></i></div>' % t for t in (
                     "Cliente:", "Máquina, marca e modelo:", "Peça e posição na máquina:", "Código original:",
                     "Arame (mm):  ________   Diâmetro (mm):  ________   Comprimento (mm):", "Quantidade:")),
                 " &nbsp;·&nbsp; ".join(x for x in ("<b>WhatsApp</b> " + E(zap) if zap else "", "<b>Telefone</b> " + E(a.telefone) if a.telefone else "",
                                                     E(a.email), E(a.site)) if x)))
    os.makedirs(a.saida, exist_ok=True)
    doc = "<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>Catálogo de referências — molas para implementos agrícolas</title><style>%s</style></head><body>%s</body></html>" % (CSS, "".join(H))
    with open(os.path.join(a.saida, "catalogo-referencias.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    with open(os.path.join(a.saida, "catalogo-referencias-fontes.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["setor", "maquina", "marca", "modelos", "peca", "codigo_original", "ref_reposicao", "arame_mm",
                    "comprimento_mm", "espira_mm", "obs", "fonte", "conferido (sim/nao)"])
        for r in sorted(reg, key=lambda r: (r["setor"], chave(r["maquina"]), chave(r["marca"]))):
            w.writerow([r["setor"], r["maquina"], r["marca"], r["modelos"], r["peca"], r["codigo_original"], r["ref_aftermarket"],
                        r["arame_mm"], r["comprimento_mm"], r["espira_mm"], r["obs"], r["fonte"], ""])
    print("%d pecas, %d marcas, %d setores (%d registros descartados por falta de codigo, marca, fonte ou repeticao)" % (
        len(reg), len(marcas), len(setores), fora))
    for s in setores:
        print("  %-32s %d" % (s, sum(1 for r in reg if r["setor"] == s)))


if __name__ == "__main__":
    main()
