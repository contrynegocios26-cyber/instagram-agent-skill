#!/usr/bin/env python3
"""Catalogo de aplicacoes e referencias: molas para implementos agricolas, por setor e por marca de maquina.

Junta tres camadas:
  1. o mapa de onde vai mola (assets/mapa-agro.json): setor > implemento > posicao > tipo de mola;
  2. a base de referencias (CSV): marca e modelo da maquina, peca, codigo original, medidas publicadas e fonte;
  3. a identidade da empresa: logo, fotos da linha propria e paginas de apoio (como medir, quando trocar, pedido).

Gera um HTML em A4 ja paginado (sumario, abas de setor, indice de codigos e de marcas). O PDF sai com pdf.js.

Uso:
  python referencias.py --base referencias-agro.csv --saida PASTA --logo logo.png --fotos PASTA_FOTOS
        [--whatsapp 55DDDNUMERO] [--telefone "(DD) 0000-0000"] [--email x@y] [--site dominio]
        [--endereco "..."] [--data mm/aaaa] [--nome catalogo-molas-agro]
  node pdf.js PASTA catalogo-molas-agro.html

Base (CSV com ';'): setor; maquina; marca; modelos; peca; tipo; codigo_original; ref_reposicao; arame_mm;
comprimento_mm; diametro_mm; diametro_ref; largura_mm; medida_publicada; nota; situacao; conferido; obs_pesquisa; fonte.
So entram as linhas com situacao = catalogo. Nada e inventado: sem codigo, sem marca ou sem fonte a linha nao entra.
"""
import argparse
import base64
import csv
import html
import io
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
E = html.escape
TIPOS = ("compressao", "tracao", "torcao", "dedo", "")

# Fotos usadas quando existem na pasta --fotos (o que faltar e simplesmente omitido).
FOTO_CAPA = ("amb-plantio-1.jpg", 0.50)
FOTOS_EMPRESA = (("amb-solo-1.jpg", 0.55), ("amb-tracao-1.jpg", 0.5), ("amb-torcao-1.jpg", 0.45))
FOTO_SETOR = {"Preparo de solo": ("amb-solo-1.jpg", 0.66), "Plantio": ("amb-plantio-1.jpg", 0.52),
              "Cana-de-açúcar": ("amb-cana-1.jpg", 0.56), "Fenação e forragem": ("amb-feno-1.jpg", 0.50)}
FOTO_TIPO = {"compressao": "compressao-5.jpg", "tracao": "tracao-2.jpg", "torcao": "torcao-1.jpg", "dedo": "feno-3.jpg"}
LINHA_SETOR = {
    "Cana-de-açúcar": ("Linha Jardmolas para a palha da cana", "dedos enleiradores e desenleiradores",
                       [("enleirador-1.jpg", "Dedo enleirador"), ("enleirador-3.jpg", "Dedo enleirador"), ("enleirador-6.jpg", "Dedo enleirador"),
                        ("desenleirador-2.jpg", "Dedo desenleirador"), ("desenleirador-5.jpg", "Dedo desenleirador"), ("desenleirador-8.jpg", "Dedo desenleirador")]),
    "Fenação e forragem": ("Linha Jardmolas para fenação", "garfos para enleiradores, espalhadores e enfardadeiras",
                           [("feno-1.jpg", "Garfo duplo"), ("feno-3.jpg", "Garfo duplo"), ("feno-5.jpg", "Garfo duplo"),
                            ("feno-7.jpg", "Garfo duplo"), ("capim-1.jpg", "Sementes de capim"), ("capim-2.jpg", "Sementes de capim")]),
}
GALERIA = (  # duas paginas: (titulo da pagina, chamada, familias: (titulo, texto, arquivos))
    ("Dedos e garfos", "Nossa linha para a palha da cana e para a fenação.", (
        ("Dedos enleiradores de palha", "rodas e rotores de enleiradores de palha de cana", ["enleirador-%d.jpg" % k for k in range(1, 9)]),
        ("Dedos desenleiradores de palha", "desenleiradores (aleiradores) de palha de cana", ["desenleirador-%d.jpg" % k for k in range(1, 9)]),
        ("Garfos de fenação", "enleiradores, espalhadores e enfardadeiras de feno", ["feno-%d.jpg" % k for k in range(1, 9)]))),
    ("Molas helicoidais", "Compressão, tração e torção, de linha ou sob medida.", (
        ("Molas de compressão", "linhas de plantio, desarme de hastes, esticadores, válvulas", ["compressao-%d.jpg" % k for k in range(1, 9)]),
        ("Molas de tração, de torção e especiais", "retorno, tensionadores, travas e colheita de sementes de capim",
         ["tracao-%d.jpg" % k for k in range(1, 6)] + ["torcao-1.jpg", "capim-1.jpg", "capim-2.jpg"]),
        ("Molas para atuadores", "retorno de atuadores, em implementos e na indústria", ["atuador-%d.jpg" % k for k in range(1, 5)]))),
)

IMAGENS = {}  # classe css -> data uri


def chave(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def imagem(classe, caminho, largura, proporcao=None, foco=0.5, qualidade=84):
    """Registra a imagem (recortada e reduzida) como classe CSS. Devolve a classe, ou '' se o arquivo nao existe."""
    if not caminho or not os.path.exists(caminho):
        return ""
    if classe in IMAGENS:
        return classe
    try:
        from PIL import Image
        im = Image.open(caminho)
        png = caminho.lower().endswith(".png")
        if not png:
            im = im.convert("RGB")
        w, h = im.size
        if proporcao:
            alvo = w / proporcao
            if alvo <= h:
                topo = max(0, min(h - alvo, h * foco - alvo / 2))
                im = im.crop((0, int(topo), w, int(topo + alvo)))
            else:
                larg = h * proporcao
                esq = (w - larg) / 2
                im = im.crop((int(esq), 0, int(esq + larg), h))
        if im.size[0] > largura:
            im = im.resize((largura, round(im.size[1] * largura / im.size[0])), Image.LANCZOS)
        buf = io.BytesIO()
        if png:
            im.save(buf, format="PNG", optimize=True)
            mime = "image/png"
        else:
            im.save(buf, format="JPEG", quality=qualidade, optimize=True, progressive=True)
            mime = "image/jpeg"
        dados = buf.getvalue()
    except ImportError:
        with open(caminho, "rb") as f:
            dados = f.read()
        mime = "image/png" if caminho.lower().endswith(".png") else "image/jpeg"
    IMAGENS[classe] = "data:%s;base64,%s" % (mime, base64.b64encode(dados).decode())
    return classe


def ler_base(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    if not linhas or "situacao" not in linhas[0]:
        sys.exit("Base sem a coluna 'situacao' (use ';' como separador).")
    dentro, problemas = [], []
    for n, r in enumerate(linhas, 2):
        r = {k: re.sub(r"\s+", " ", (v or "")).strip() for k, v in r.items() if k}
        if r.get("situacao", "").lower() != "catalogo":
            continue
        falta = [c for c in ("setor", "marca", "peca", "fonte") if not r.get(c)]
        if not (r.get("codigo_original") or r.get("ref_reposicao")):
            falta.append("codigo_original ou ref_reposicao")
        if r.get("tipo", "") not in TIPOS:
            falta.append("tipo invalido (%s)" % r["tipo"])
        if falta:
            problemas.append("linha %d: falta %s" % (n, ", ".join(falta)))
            continue
        dentro.append(r)
    return dentro, problemas, len(linhas)


def codigos(texto):
    """'A (direito) · B' -> [['A','direito'], ['B','']]"""
    saida = []
    for parte in (x.strip() for x in texto.split("·")):
        if not parte:
            continue
        m = re.match(r"^(.*?)\s*\(([^()]*)\)$", parte)
        saida.append([m.group(1), m.group(2)] if m else [parte, ""])
    return saida


def medidas(r):
    p = []
    if r.get("arame_mm"):
        p.append("arame " + r["arame_mm"])
    if r.get("diametro_mm"):
        p.append({"interno": "Ø int. ", "externo": "Ø ext. "}.get(r.get("diametro_ref", ""), "Ø ") + r["diametro_mm"])
    if r.get("comprimento_mm"):
        p.append("compr. " + r["comprimento_mm"])
    if r.get("largura_mm"):
        p.append("larg. " + r["largura_mm"])
    if p:
        p[-1] += " mm"
    return p + [x for x in (r.get("medida_publicada"), r.get("nota")) if x]


def lista_e(itens):
    itens = list(itens)
    return itens[0] if len(itens) == 1 else ", ".join(itens[:-1]) + " e " + itens[-1]


# ------------------------------------------------------------------ paginas fixas
def pagina_empresa(c, pasta):
    trio = "".join('<i class="im %s"></i>' % cl for cl in (
        imagem("im-emp%d" % n, os.path.join(pasta, arq), 820, (1.25 if n == 0 else 1.0) * 54.3 / 58, foco) for n, (arq, foco) in enumerate(FOTOS_EMPRESA)) if cl)
    return (
        '<div class="olho">A empresa</div><h2>Jardmolas, a marca da qualidade</h2><span class="faixa"></span>'
        '<p class="lead" style="max-width:165mm">Fabricamos molas originais e de reposição desde 2008, em Jardinópolis-SP, na região de Ribeirão Preto. '
        'Atendemos clientes em todo o Brasil, com rede de distribuidores e representantes e um catálogo com mais de 2.000 itens.</p>'
        '<div class="nums"><div><b>2008</b><span>ano de fundação</span></div><div><b>+2.000</b><span>itens em catálogo</span></div>'
        '<div><b>Brasil</b><span>clientes em todo o país, com distribuidores e representantes</span></div>'
        '<div><b>Sob medida</b><span>pelo código original, pelo desenho ou pela amostra</span></div></div>'
        + ('<div class="trio">%s</div>' % trio if trio else "") +
        '<div class="cols3" style="margin-top:5mm">'
        '<div><h3>Linha agrícola</h3><span class="faixa" style="margin:2mm 0 3mm"></span><ul>'
        '<li>Dedos enleiradores e desenleiradores de palha de cana</li><li>Garfos para enleiradores, espalhadores e enfardadeiras de feno</li>'
        '<li>Molas de compressão, tração e torção para implementos</li><li>Molas para atuadores</li><li>Molas para recolhedor de amendoim</li></ul></div>'
        '<div><h3>Indústria e usinas</h3><span class="faixa" style="margin:2mm 0 3mm"></span><ul>'
        '<li>Molas para válvulas de retenção dupla portinhola</li><li>Molas para válvulas de segurança</li><li>Molas para atuadores</li>'
        '<li>Molas de compressão para indústrias e usinas</li><li>Molas para peneiras vibratórias</li></ul></div>'
        '<div><h3>Materiais</h3><span class="faixa" style="margin:2mm 0 3mm"></span><ul>'
        '<li>Arame de aço patenteado e SAE&nbsp;1070</li><li>Aços-liga SAE&nbsp;5160, 6150 e 9254</li><li>Inox 302 e 304</li>'
        '<li>Ligas especiais, como Inconel&nbsp;X‑750</li></ul></div></div>'
        '<div class="cx verde" style="margin-top:6mm;display:grid;grid-template-columns:1fr auto;gap:8mm;align-items:center">'
        '<div><h3>Este catálogo</h3><p style="margin:1.5mm 0 0;font-size:9.6pt">Reúne onde vai mola em %d setores do agro e os códigos de referência das principais marcas de máquinas, '
        'para você achar a peça pela máquina e pedir pelo código, pelo desenho ou pela amostra.</p></div>'
        '<div style="font-size:10pt;line-height:1.7;white-space:nowrap">%s</div></div>' % (
            c["n_setores"], "<br>".join(x for x in ("<b>WhatsApp</b> " + E(c["zap"]) if c["zap"] else "", "<b>Telefone</b> " + E(c["telefone"]) if c["telefone"] else "",
                                                     E(c["site"])) if x)))


def pagina_galeria(pasta):
    paginas = []
    for np_, (titulo_pg, chamada, familias) in enumerate(GALERIA):
        blocos = ""
        for nf, (titulo, texto, arquivos) in enumerate(familias):
            figs = "".join('<figure><i class="%s"></i></figure>' % cl for cl in (
                imagem("im-g%d%d-%d" % (np_, nf, k), os.path.join(pasta, arq), 520) for k, arq in enumerate(arquivos)) if cl)
            if figs:
                blocos += ('<div class="famg"><h3>%s <small>%s</small></h3><div class="fotos" style="grid-template-columns:repeat(4,1fr)">%s</div></div>'
                           % (E(titulo), E(texto), figs))
        if blocos:
            paginas.append('<div class="olho">Linha de fabricação Jardmolas</div><h2>%s</h2><span class="faixa" style="margin-bottom:3mm"></span>'
                           '<p class="lead" style="max-width:165mm;margin:0">%s <span style="font-size:8.6pt;color:var(--cinza)">Bitolas, medidas e acabamentos sob consulta.</span></p>%s'
                           % (E(titulo_pg), E(chamada), blocos))
    return paginas


def pagina_como(c, setores, pasta):
    ex_pos = next(((i["nome"], p) for s in setores if s["nome"] == "Plantio" for i in s["implementos"] for p in i["posicoes"]), None)
    ex_ref = next(((m["marca"], r) for s in setores for m in s["marcas"] for r in m["linhas"]
                   if r["modelos"] and r["cods"] and r["med"] and r["tipo"] and len(r["modelos"]) < 30), None)
    nomes = {"compressao": "Compressão", "tracao": "Tração", "torcao": "Torção", "dedo": "Dedo / garfo"}
    exemplo = ""
    if ex_pos:
        exemplo += ('<div class="tit" style="margin-top:0">1 · Onde vai mola <small>o implemento, o lugar da mola nele, como ela é chamada no mercado e o tipo</small></div>'
                    '<table><thead><tr><th style="width:31%%">Posição na máquina</th><th style="width:25%%">Mola</th><th style="width:19%%">Tipo</th><th>Função</th></tr></thead>'
                    '<tbody><tr class="grupo"><td colspan="4">%s</td></tr><tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr></tbody></table>' % (
                        E(ex_pos[0]), E(ex_pos[1][0]), E(ex_pos[1][1]), E(" / ".join(nomes[t] for t in ex_pos[1][2].split("+"))), E(ex_pos[1][3])))
    if ex_ref:
        marca, r = ex_ref
        exemplo += ('<div class="tit" style="margin-top:4mm">2 · Códigos de referência por marca <small>a máquina, a peça e o número com que o fabricante a identifica</small></div>'
                    '<table><thead><tr><th style="width:25%%">Máquina · modelo</th><th style="width:30%%">Peça</th><th style="width:20%%">Código original</th>'
                    '<th>Medidas publicadas</th></tr></thead><tbody><tr class="grupo"><td colspan="4">%s</td></tr><tr>'
                    '<td><span class="mq">%s</span><span class="md">%s</span></td><td>%s</td><td class="cod">%s</td><td class="med">%s</td></tr></tbody></table>' % (
                        E(marca), E(r["maq"]), E(r["modelos"]), E(r["peca"]), E(r["cods"][0][0]), E(" · ".join(r["med"]))))

    def cart(tipo, titulo, texto, itens):
        cl = imagem("im-tipo-" + tipo, os.path.join(pasta, FOTO_TIPO[tipo]), 420) if pasta else ""
        return '<div class="tipo">%s<div><h3>%s</h3><p>%s</p></div></div>' % ('<i class="%s"></i>' % cl if cl else "", titulo, texto)
    return (
        '<div class="olho">Como usar</div><h2>Ache a mola pela sua máquina</h2><span class="faixa"></span>'
        '<p class="lead" style="max-width:165mm">Este catálogo é organizado como o produtor e o mecânico pensam: pelo <b>setor</b> e pela <b>máquina</b>.</p>'
        '<div class="passos">'
        '<div><b>1</b><h3>Ache o setor</h3><p>São %d setores, do trator à armazenagem. A aba numerada na lateral e o sumário levam direto a ele.</p></div>'
        '<div><b>2</b><h3>Veja onde vai mola</h3><p>Implemento por implemento: a posição na máquina, o nome da mola, o tipo e a função.</p></div>'
        '<div><b>3</b><h3>Confira o código</h3><p>Por marca de máquina: modelo, peça, código original e medidas publicadas. O índice no fim leva do código à página.</p></div>'
        '<div><b>4</b><h3>Peça</h3><p>Pelo código, pelo desenho ou pela amostra. Sem código e sem medida, mande uma foto da peça ao lado de uma régua%s.</p></div></div>'
        '<h3 style="margin:6.5mm 0 3mm">O que fabricamos</h3><div class="cols4">%s%s%s%s</div>'
        '<h3 style="margin:6.5mm 0 3mm">Como ler as tabelas</h3>%s'
        '<p class="nota" style="margin-top:4mm"><b>Medidas:</b> arame = diâmetro do arame · Ø = diâmetro da espira (int. ou ext. quando a fonte informa) · compr. = comprimento · '
        'larg. = largura do dedo ou garfo. São as medidas publicadas pelo mercado: confirme na peça antes de pedir. <b>Ref.</b> = número da mesma peça em catálogos de reposição. '
        'Marcas, modelos e códigos pertencem aos seus fabricantes e são citados só como referência de aplicação (nota completa na contracapa).</p>' % (
            c["n_setores"], " pelo WhatsApp" if c["zap"] else "",
            cart("compressao", "Compressão", "Trabalha apertada: pressão de linha, desarme de haste, esticadores, válvulas.",
                 ["arame e diâmetro externo", "comprimento livre e nº de espiras", "pontas fechadas ou retificadas"]),
            cart("tracao", "Tração", "Trabalha esticada: retorno de braços, limpadores, tensionadores, flutuação.",
                 ["arame e diâmetro externo", "comprimento entre ganchos", "tipo e posição dos ganchos"]),
            cart("torcao", "Torção", "Trabalha girando: travas, catracas, portinholas, retorno de alavancas.",
                 ["arame e diâmetro interno", "nº de espiras, pernas e ângulo", "sentido de enrolamento"]),
            cart("dedo", "Dedos e garfos", "Molas de torção de perna longa: enleiradores, molinetes, recolhedores.",
                 ["máquina e posição", "arame e comprimento total", "espiras e fixação"]),
            exemplo))


def zigue(x0, x1, y0, y1, n):
    pts = []
    for k in range(2 * n + 1):
        pts.append("%.1f,%.1f" % (x0 + (x1 - x0) * k / (2 * n), y0 if k % 2 == 0 else y1))
    return " ".join(pts)


def cota_h(x0, x1, y, rotulo, acima=False):
    return ('<path class="c" d="M%s %sH%s M%s %sv6 M%s %sv6"/><text x="%s" y="%s" text-anchor="middle">%s</text>'
            % (x0, y, x1, x0, y - 3, x1, y - 3, (x0 + x1) / 2, y - 3 if acima else y + 10, rotulo))


def cota_v(x, y0, y1, rotulo):
    return ('<path class="c" d="M%s %sV%s M%s %sh6 M%s %sh6"/><text x="%s" y="%s">%s</text>'
            % (x, y0, y1, x - 3, y0, x - 3, y1, x + 5, (y0 + y1) / 2 + 3, rotulo))


def pagina_medir(c):
    comp = ('<svg viewBox="0 0 240 132"><polyline class="m" points="%s"/><path class="m" d="M44 34V96M196 34V96"/>%s%s'
            '<path class="c" d="M70 34L62 18"/><text x="38" y="15">d · arame</text></svg>') % (
                zigue(44, 196, 96, 34, 8), cota_h(44, 196, 112, "L0 · comprimento livre"), cota_v(210, 34, 96, "De"))
    trac = ('<svg viewBox="0 0 240 132"><polyline class="m" points="%s"/><circle class="m" cx="55" cy="64" r="15"/><circle class="m" cx="185" cy="64" r="15"/>%s%s'
            '%s<path class="c" d="M100 42L92 24"/><text x="70" y="21">d · arame</text></svg>') % (
                zigue(70, 170, 86, 42, 13), cota_h(70, 170, 100, "Lc · corpo"), cota_h(42, 198, 119, "Li · por dentro dos ganchos"), cota_v(212, 42, 86, "De"))
    torc = ('<svg viewBox="0 0 240 132"><circle class="m" cx="86" cy="76" r="27"/><circle class="m" cx="86" cy="76" r="19"/>'
            '<path class="m" d="M86 49H214M66 94L28 126"/>%s<path class="c" d="M67 76H105"/><text x="78" y="72">Di</text>'
            '<path class="c" d="M127.3 61.9A44 44 0 0 1 52.3 104.3"/><text x="116" y="112">ângulo</text><text x="20" y="108">L2</text>'
            '<path class="c" d="M113 76L138 84"/><text x="141" y="88">d · arame</text></svg>') % cota_h(86, 214, 38, "L1 · perna", True)
    dedo = ('<svg viewBox="0 0 240 132"><polyline class="m" points="%s"/><polyline class="m" points="%s"/>'
            '<path class="m" d="M86 30V44H114V30M56 38L42 124M144 38L158 124"/>%s%s'
            '<path class="c" d="M130 20L140 9"/><text x="143" y="11">Ø da espira</text><path class="c" d="M47 100L68 108"/><text x="71" y="112">d · arame</text></svg>') % (
                zigue(56, 86, 38, 22, 4), zigue(114, 144, 22, 38, 4), cota_h(56, 144, 50, "largura"), cota_v(176, 22, 124, "compr. total"))

    def des(svg, titulo, itens):
        return '<div class="des">%s<h3>%s</h3><ol>%s</ol></div>' % (svg, titulo, "".join("<li>%s</li>" % i for i in itens))
    return (
        '<div class="olho">Como medir</div><h2>Cinco medidas resolvem quase todo pedido</h2><span class="faixa"></span>'
        '<p class="lead" style="max-width:165mm">Use paquímetro. Meça a mola solta, sem carga, e de preferência uma peça nova ou a menos gasta do jogo.</p>'
        '<div class="cols2" style="gap:4mm;margin-top:4mm">%s%s%s%s</div>'
        '<div class="cx" style="margin-top:4.5mm;display:grid;grid-template-columns:1fr 1fr;gap:7mm"><div><h3 style="font-size:10.6pt">Diga também</h3><ul style="margin:1.6mm 0 0">'
        '<li>marca e modelo da máquina e onde a mola vai;</li><li>código original, se existir;</li><li>ambiente: adubo, calda, vinhaça, água, calor;</li><li>quantidade e prazo.</li></ul></div>'
        '<div><h3 style="font-size:10.6pt">Não tem como medir?</h3><p style="margin:1.6mm 0 0">Envie uma foto da peça ao lado de uma régua%s, ou mande a amostra. '
        'Mola quebrada também serve: mande os pedaços.</p></div></div>' % (
            des(comp, "Compressão", ["<b>d</b>: diâmetro do arame", "<b>De</b>: diâmetro externo, no meio da mola", "<b>L0</b>: comprimento livre",
                                     "total de espiras, de ponta a ponta", "pontas: fechadas? retificadas (planas)?"]),
            des(trac, "Tração", ["<b>d</b>: diâmetro do arame", "<b>De</b>: diâmetro externo do corpo", "<b>Lc</b>: comprimento do corpo",
                                 "<b>Li</b>: comprimento por dentro dos ganchos", "tipo e posição dos ganchos (alinhados ou a 90°)"]),
            des(torc, "Torção", ["<b>d</b>: diâmetro do arame", "<b>Di</b>: diâmetro interno (ou o do eixo)", "espiras do corpo",
                                 "<b>L1</b> e <b>L2</b>: cada perna, medida do centro", "ângulo entre as pernas, com a mola solta, e sentido: direita ou esquerda"]),
            des(dedo, "Dedos e garfos", ["<b>d</b>: diâmetro do arame", "comprimento total", "largura entre as pernas",
                                         "diâmetro e número de espiras", "fixação: olhal, gancho, grampo ou parafuso"]),
            " pelo WhatsApp %s" % E(c["zap"]) if c["zap"] else ""))


def pagina_trocar(c):
    sinais = (
        ("A mola de compressão ficou mais curta", "Compare com uma nova. Se o comprimento livre caiu, a mola cedeu e já não dá a carga: a linha perde pressão e a profundidade deixa de repetir."),
        ("As espiras encostam em trabalho", "Mola que fecha por completo bate espira com espira, perde o curso e quebra cedo. É sinal de mola cedida ou de regulagem além do curso."),
        ("A mola de tração não fecha mais", "Solta, a mola de tração de espiras encostadas deve fechar por completo. Se sobra vão entre as espiras, ela foi esticada além do limite e perdeu carga: troque."),
        ("Gancho aberto ou gasto", "O gancho é o ponto mais solicitado da mola de tração. Desgaste no apoio, gancho aberto ou trinca na dobra pedem troca imediata."),
        ("Trinca, ferrugem funda ou marca de batida", "A fadiga começa na superfície. Risco fundo, ponto de corrosão ou amassado na espira viram trinca com o trabalho."),
        ("Dedo torto, aberto ou fora de linha", "Dedos e garfos quebram na espira ou na dobra junto à fixação. Um dedo desalinhado sobrecarrega os vizinhos e solta pedaços na máquina."),
    )
    return (
        '<div class="olho">Quando trocar</div><h2>Seis sinais de que a mola chegou ao fim</h2><span class="faixa"></span>'
        '<p class="lead" style="max-width:165mm">Mola não avisa com barulho: ela perde carga aos poucos e a máquina passa a trabalhar fora do ajuste. Confira na revisão de entressafra.</p>'
        '<div style="margin-top:3mm">%s</div>'
        '<h3 style="margin:6.5mm 0 0">Revisão de entressafra em cinco passos</h3><div class="rev">'
        '<div><b>1</b><h3>Limpe e olhe</h3><p>Com a máquina lavada, passe por todas as posições de mola. A tabela "Onde vai mola" do setor serve de lista.</p></div>'
        '<div><b>2</b><h3>Compare</h3><p>Meça o comprimento livre e confira com a peça de reserva ou com as vizinhas do mesmo jogo.</p></div>'
        '<div><b>3</b><h3>Acione</h3><p>Mova braços, linhas e travas com a mão. Mola boa devolve a peça inteira, sem folga.</p></div>'
        '<div><b>4</b><h3>Anote</h3><p>Código, posição e quantidade das que vão trocar. Tire as medidas das que não têm código.</p></div>'
        '<div><b>5</b><h3>Peça antes</h3><p>Mola sob medida tem prazo de fabricação. Peça na entressafra, não na véspera.</p></div></div>'
        '<div class="cols3" style="margin-top:6mm">'
        '<div class="cx"><h3 style="font-size:10.6pt">Troque em jogo</h3><p style="margin:1.6mm 0 0;font-size:8.6pt">Molas que trabalham juntas, como as das linhas de plantio e os dedos de um mesmo rotor, '
        'devem ser trocadas em conjunto. Misturar nova com cansada desiguala a carga.</p></div>'
        '<div class="cx"><h3 style="font-size:10.6pt">Guarde uma de reserva</h3><p style="margin:1.6mm 0 0;font-size:8.6pt">Uma peça nova guardada serve de padrão de medida para a próxima compra '
        'e de comparação na revisão.</p></div>'
        '<div class="cx"><h3 style="font-size:10.6pt">Material certo</h3><p style="margin:1.6mm 0 0;font-size:8.6pt">Em contato com calda, adubo ou vinhaça, diga o ambiente no pedido: '
        'ele define o material e o acabamento da mola.</p></div></div>' % "".join(
            '<div class="sinal"><b class="n">%d</b><div><h3>%s</h3><p>%s</p></div></div>' % (n, E(t), E(x)) for n, (t, x) in enumerate(sinais, 1)))


def pagina_pedido(c):
    campos = ("Cliente / fazenda / usina:", "Máquina, marca e modelo:", "Setor e posição da mola na máquina:", "Código original (da peça ou do manual):",
              "Tipo:  ( ) compressão   ( ) tração   ( ) torção   ( ) dedo / garfo", "Arame (mm):  ________   Diâmetro externo (mm):  ________   Comprimento (mm):",
              "Espiras:  ________   Pontas / ganchos / pernas:", "Ambiente de trabalho (adubo, calda, água, calor):", "Quantidade:  ________   Prazo desejado:",
              "Contato (nome, telefone, e-mail):", "Observações:", "")
    return (
        '<div class="olho">Pedido</div><h2>Não achou sua máquina? Fabricamos pela amostra</h2><span class="faixa"></span>'
        '<p class="lead" style="max-width:160mm">Molas de compressão, tração e torção, dedos e garfos, a partir do código original, do desenho ou da peça que você tem na mão.</p>'
        '<h3 style="margin:6mm 0 3mm">Ficha de pedido</h3><div class="cx" style="padding:7mm 6mm 1mm">%s</div>'
        '<div class="cx verde" style="margin-top:6mm;display:grid;grid-template-columns:1fr auto;gap:8mm;align-items:center"><div><h3>Envie esta ficha</h3>'
        '<p style="margin:1.5mm 0 0;font-size:10pt;line-height:1.7">%s</p></div>%s</div>' % (
            "".join('<div class="campo"><span>%s</span><i></i></div>' % t for t in campos),
            "<br>".join(x for x in ("<b>WhatsApp</b> " + E(c["zap"]) if c["zap"] else "", "<b>Telefone</b> " + E(c["telefone"]) if c["telefone"] else "",
                                    "<b>E-mail</b> " + E(c["email"]) if c["email"] else "", E(c["site"])) if x),
            '<div style="background:#fff;border-radius:2mm;padding:2mm"><img src="%s" alt="" style="width:27mm;display:block"></div>' % c["qr"] if c["qr"] else ""))


def qr(texto):
    try:
        import qrcode
    except ImportError:
        return ""
    buf = io.BytesIO()
    qrcode.make(texto, box_size=8, border=1).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", required=True, help="CSV de referencias (situacao = catalogo entra)")
    p.add_argument("--saida", required=True)
    p.add_argument("--mapa", default=os.path.join(AQUI, "..", "assets", "mapa-agro.json"))
    p.add_argument("--logo", default="")
    p.add_argument("--fotos", default="", help="pasta com as fotos da empresa (opcional)")
    p.add_argument("--empresa", default="Jardmolas")
    p.add_argument("--whatsapp", default="")
    p.add_argument("--telefone", default="")
    p.add_argument("--email", default="")
    p.add_argument("--site", default="")
    p.add_argument("--endereco", default="")
    p.add_argument("--data", default="")
    p.add_argument("--nome", default="catalogo-molas-agro")
    a = p.parse_args()

    with open(a.mapa, encoding="utf-8") as f:
        mapa = json.load(f)["setores"]
    nomes = [s["nome"] for s in mapa]
    regs, problemas, total = ler_base(a.base)
    por_chave = {chave(n): n for n in nomes}
    for r in regs:
        if chave(r["setor"]) not in por_chave:
            problemas.append("setor fora do mapa: %s (%s %s)" % (r["setor"], r["marca"], r["codigo_original"]))
    regs = [r for r in regs if chave(r["setor"]) in por_chave]

    z = re.sub(r"\D", "", a.whatsapp)
    legal = ("Marcas, modelos e códigos originais pertencem aos respectivos fabricantes e são citados exclusivamente como referência de aplicação. "
             "As peças fornecidas pela %s são de fabricação própria; não são peças originais dos fabricantes das máquinas. "
             "Códigos e medidas reunidos de catálogos e anúncios públicos de peças de reposição: confirme a aplicação pelo modelo e pelo número de série da máquina antes de pedir. "
             "As posições de mola são as típicas de cada implemento e variam conforme o fabricante.") % E(a.empresa)
    cfg = {"empresa": a.empresa, "zap": "(%s) %s-%s" % (z[2:4], z[4:9], z[9:]) if len(z) == 13 else a.whatsapp, "telefone": a.telefone,
           "email": a.email, "site": a.site, "endereco": a.endereco, "data": a.data, "qr": qr("https://wa.me/" + z) if z else "", "n_setores": len(mapa)}
    cfg["logo"] = bool(a.logo and os.path.exists(a.logo) and imagem("lg", a.logo, 640))
    pasta = a.fotos
    if pasta:
        imagem("im-capa", os.path.join(pasta, FOTO_CAPA[0]), 1500, 210 / 176, FOTO_CAPA[1], 86)

    setores = []
    for n, s in enumerate(mapa, 1):
        blocos = {}
        for r in (r for r in regs if por_chave[chave(r["setor"])] == s["nome"]):
            marcas = [m.strip() for m in r["marca"].split("/") if m.strip()]
            linha = {"maq": r.get("maquina", ""), "modelos": r.get("modelos", ""), "peca": r["peca"], "tipo": r.get("tipo", ""),
                     "cods": codigos(r.get("codigo_original", "")), "reps": [x.strip() for x in r.get("ref_reposicao", "").split("·") if x.strip()],
                     "med": medidas(r), "marcas": marcas, "tambem": lista_e(marcas[1:]) if len(marcas) > 1 else ""}
            blocos.setdefault(chave(marcas[0]), {"marca": marcas[0], "linhas": []})["linhas"].append(linha)
        marcas_setor = []
        for b in sorted(blocos.values(), key=lambda b: chave(b["marca"])):
            b["linhas"].sort(key=lambda r: (chave(r["maq"]), chave(r["modelos"]) == "", chave(r["modelos"]), chave(r["peca"])))
            marcas_setor.append(b)
        foto = ""
        if pasta and s["nome"] in FOTO_SETOR:
            arq, foco = FOTO_SETOR[s["nome"]]
            foto = imagem("im-s%d" % n, os.path.join(pasta, arq), 1335, 180 / 42, foco)
        linha_j = None
        if pasta and s["nome"] in LINHA_SETOR:
            titulo, texto, itens = LINHA_SETOR[s["nome"]]
            figs = [{"cls": cl, "leg": leg} for cl, leg in ((imagem("im-l%d-%d" % (n, k), os.path.join(pasta, arq), 300), leg) for k, (arq, leg) in enumerate(itens)) if cl]
            if figs:
                linha_j = {"titulo": titulo, "texto": texto, "itens": figs}
        setores.append({"n": n, "nome": s["nome"], "curto": s.get("curto") or s["nome"].lower(), "resumo": s["resumo"], "implementos": s["implementos"], "marcas": marcas_setor,
                        "foto": foto, "linha": linha_j})

    totais = {"setores": len(setores), "implementos": sum(len(s["implementos"]) for s in setores),
              "posicoes": sum(len(i["posicoes"]) for s in setores for i in s["implementos"]), "refs": len(regs),
              "marcas": len({chave(m) for r in regs for m in r["marca"].split("/")})}
    paginas = {"empresa": pagina_empresa(cfg, pasta), "galeria": pagina_galeria(pasta) if pasta else [], "como": pagina_como(cfg, setores, pasta),
               "medir": pagina_medir(cfg), "trocar": pagina_trocar(cfg), "pedido": pagina_pedido(cfg)}
    dados = {"cfg": cfg, "setores": setores, "totais": totais, "legal": legal, "paginas": paginas}
    with open(os.path.join(AQUI, "..", "assets", "referencias-modelo.html"), encoding="utf-8") as f:
        pagina = f.read()
    css = "".join((".%s{background-image:url(%s)}" if k != "lg" else "i.%s{background-image:url(%s)}") % (k, v) for k, v in IMAGENS.items())
    pagina = pagina.replace("__TITULO__", "%s — molas para implementos agrícolas" % E(a.empresa))
    pagina = pagina.replace("/*__IMAGENS__*/", css)
    pagina = pagina.replace("/*__DADOS__*/{}", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    os.makedirs(a.saida, exist_ok=True)
    destino = os.path.join(a.saida, a.nome + ".html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(pagina)

    print("%(setores)d setores | %(implementos)d implementos | %(posicoes)d posicoes de mola | %(refs)d referencias | %(marcas)d marcas" % totais)
    for s in setores:
        print("  %02d %-40s %3d referencias  %s" % (s["n"], s["nome"], sum(len(m["linhas"]) for m in s["marcas"]), ", ".join(m["marca"] for m in s["marcas"])[:80]))
    print("base: %d linhas, %d no catalogo, %d fora" % (total, len(regs), total - len(regs)))
    for x in problemas:
        print("  ATENCAO " + x)
    print("imagens embutidas: %d (%.1f MB)" % (len(IMAGENS), sum(len(v) for v in IMAGENS.values()) * 0.75 / 1e6))
    print(destino)


if __name__ == "__main__":
    main()
