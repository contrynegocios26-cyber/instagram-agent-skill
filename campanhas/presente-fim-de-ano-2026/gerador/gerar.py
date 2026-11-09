#!/usr/bin/env python3
"""Gera o catálogo de presentes de fim de ano e o cartão com QR da MP Marcenaria.

Uso (de dentro desta pasta):
  python3 gerar.py
      Catálogo e cartão genéricos, na pasta da campanha.
  python3 gerar.py --empresa "Nome da Empresa" --logo logo.png --codigo N26-NOME
      Proposta personalizada: o logo (ou o nome) aparece gravado na tábua do catálogo,
      o cartão sai assinado pela empresa e o QR do cartão leva o código, para a MP
      saber de qual presente veio cada contato. Sai em propostas/<nome>/.
  python3 gerar.py --foto prototipo.jpg
      Troca a ilustração do topo pela foto do protótipo.

Os preços vêm da aba Preços de precificacao-presentes-2026.xlsx. Depois de mudar as
premissas, abra a planilha no Excel ou no LibreOffice e salve, para gravar os valores.

Precisa de: python3 com openpyxl e segno (pip install segno); node com playwright.
"""
import argparse
import base64
import mimetypes
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

import segno
from openpyxl import load_workbook

import ilustracoes as il

AQUI = Path(__file__).resolve().parent
CAMPANHA = AQUI.parent
PLANILHA = CAMPANHA / "precificacao-presentes-2026.xlsx"
WHATSAPP = "5544998846314"

KITS = [
    ("Essencial", il.mini_essencial, False,
     "Tábua de servir 35 × 22 cm em madeira maciça, com a sua marca gravada. Vai em saco de algodão cru."),
    ("Churrasco", il.mini_churrasco, True,
     "Tábua de churrasco 45 × 30 cm com canaleta para o caldo e alça de couro. Vai em caixa kraft."),
    ("Premium", il.mini_premium, False,
     "Estojo de madeira com a tábua de churrasco, faca e garfo trinchante inox. Marca na tampa e na tábua."),
]


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def data_uri(caminho):
    p = Path(caminho)
    tipo = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{tipo};base64," + base64.b64encode(p.read_bytes()).decode()


def ler_precos():
    wb = load_workbook(PLANILHA, data_only=True)
    ws = wb["Preços"]
    faixas = [ws[f"{c}4"].value for c in "CDEF"]
    precos = {ws[f"A{r}"].value: [ws[f"{c}{r}"].value for c in "CDEF"] for r in (9, 10, 11)}
    taxa = ws["B24"].value
    if None in faixas or taxa is None or any(None in v for v in precos.values()):
        sys.exit("A planilha está sem os valores calculados. Abra precificacao-presentes-2026.xlsx "
                 "no Excel ou no LibreOffice, salve e rode de novo.")
    return faixas, precos, taxa


def qr_svg(texto):
    url = f"https://wa.me/{WHATSAPP}?text={quote(texto)}"
    return segno.make(url, error="m").svg_inline(dark="#1d0c0d", light="#f4ede7", border=3, omitsize=True), url


def preencher(modelo, campos):
    html = (AQUI / modelo).read_text(encoding="utf-8")
    for k, v in campos.items():
        html = html.replace("{{" + k + "}}", v)
    faltando = re.findall(r"\{\{(\w+)\}\}", html)
    if faltando:
        sys.exit(f"Campos sem valor em {modelo}: {faltando}")
    return html


def render(html, destino, base, w, h, paginas=1):
    destino.mkdir(parents=True, exist_ok=True)
    arq = destino / f"{base}.html"
    arq.write_text(html, encoding="utf-8")
    subprocess.run(["node", str(AQUI / "render.js"), str(arq), str(destino / f"{base}.pdf"),
                    str(destino / f"{base}.png"), str(w), str(h), str(paginas)], check=True)
    arq.unlink()
    return destino / f"{base}.pdf", destino / f"{base}.png"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--empresa", help="nome da empresa para a proposta personalizada")
    ap.add_argument("--logo", help="arquivo do logo da empresa (PNG com fundo transparente ou branco)")
    ap.add_argument("--foto", help="foto do protótipo para substituir a ilustração do topo")
    ap.add_argument("--codigo", default="N26", help="código que vai no QR do cartão (ex.: N26-COOPX)")
    ap.add_argument("--mensagem", default="Que 2027 venha com mesa cheia e gente boa em volta.",
                    help="mensagem da frente do cartão")
    ap.add_argument("--prazo", default="05/12", help="último dia para fechar pedido")
    ap.add_argument("--entrega", default="18/12", help="último dia de entrega")
    a = ap.parse_args()

    faixas, precos, taxa = ler_precos()
    logo = data_uri(a.logo) if a.logo else None
    gravado = a.empresa or "SUA MARCA"

    kits_html = []
    for nome, desenho, destaque, texto in KITS:
        linhas = "".join(f"<div><span>{f} peças</span><b>{brl(p)}</b></div>" for f, p in zip(faixas, precos[nome]))
        tag = '<span class="tag">Recomendado</span>' if destaque else ""
        kits_html.append(
            f'<article class="kit{" destaque" if destaque else ""}">{tag}'
            f'<div class="mini">{desenho(texto=gravado, logo=logo)}</div>'
            f"<h3>{nome}</h3><p>{texto}</p><div class=\"precos\">{linhas}</div></article>")

    arte = (f'<img src="{data_uri(a.foto)}" alt="Tábua de churrasco MP">' if a.foto
            else il.heroi(texto=gravado, logo=logo))
    qr_cat, _ = qr_svg("Oi! Quero orçamento dos presentes de fim de ano da MP.")
    pessoal = bool(a.empresa)
    catalogo = preencher("catalogo.html", {
        "topo_direita": f"Proposta para {esc(a.empresa)}" if pessoal else "Presentes de fim de ano 2026",
        "eyebrow": "Presente de fim de ano para empresas",
        "titulo": "Sua marca gravada em madeira maciça." if pessoal else "A marca da sua empresa gravada em madeira maciça.",
        "arte_heroi": arte,
        "kits": "".join(kits_html),
        "taxa": esc(taxa),
        "entrega": a.entrega,
        "prazo": a.prazo,
        "qr": qr_cat,
        "rodape_direita": ("Foto do protótipo. Cada peça tem veio e tom únicos." if a.foto
                           else "Imagens ilustrativas. Cada peça tem veio e tom únicos."),
    })

    codigo = a.codigo if a.codigo != "N26" or not pessoal else f"N26-{slug(a.empresa)[:12].upper()}"
    qr_card, url_card = qr_svg(f"Oi! Ganhei uma tábua da MP ({codigo}) e quero conhecer os móveis sob medida.")
    cartao = preencher("cartao.html", {
        "mensagem": esc(a.mensagem),
        "empresa": esc(a.empresa or "Sua empresa"),
        "qr": qr_card,
    })

    destino = CAMPANHA / "propostas" / slug(a.empresa) if pessoal else CAMPANHA
    sufixo = f"-{slug(a.empresa)}" if pessoal else "-2026"
    for arq in render(catalogo, destino, f"catalogo-presentes{sufixo}", 210, 297):
        print(arq)
    for arq in render(cartao, destino, f"cartao-presente{sufixo}", 90, 50, paginas=2):
        print(arq)
    print("QR do cartão:", url_card)


if __name__ == "__main__":
    main()
