#!/usr/bin/env python3
"""
catalogo.py - mantém o catálogo de conteúdo da MP Marcenaria em dia.

Cada conteúdo é uma pasta com nome AAAA-MM-DD_tipo_tema, guardada dentro da
pasta do seu status. A pasta leva as fotos e vídeos daquele post e um info.md
com a legenda, o link e os números. O status é a pasta onde ela está: mudar
um conteúdo de "prontos" para "postados" é só arrastar a pasta.

    0-material-bruto/        fotos e vídeos recebidos que ainda não viraram post
    1-postados/              já está no Instagram
    2-prontos-para-postar/   legenda e mídia prontas, falta publicar
    3-em-producao/           tem mídia, falta editar ou escrever
    4-ideias/                roteiros e ideias, ainda sem gravação

Este script lê todas as pastas e reescreve CATALOGO.md e catalogo.csv (abre
no Excel). Rode sempre que mexer em alguma coisa.

Uso
  python catalogo.py                         reescreve o catálogo
  python catalogo.py novo reel "painel ripado com led"
  python catalogo.py novo carrossel "cozinha verde" --status prontos --data 2026-11-03
  python catalogo.py postar 2026-11-03_reel_painel-ripado-com-led --link https://www.instagram.com/reel/XXXX/
"""

import argparse
import csv
import datetime
import re
import shutil
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

STATUS = {
    "postados": "1-postados",
    "prontos": "2-prontos-para-postar",
    "producao": "3-em-producao",
    "ideias": "4-ideias",
}
BRUTO = "0-material-bruto"
ROTULO = {
    "1-postados": "Já postados",
    "2-prontos-para-postar": "Prontos para postar",
    "3-em-producao": "Em produção",
    "4-ideias": "Ideias (sem gravação)",
}
TIPOS = ("reel", "carrossel", "foto", "story")
MIDIA = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif",
         ".mp4", ".mov", ".m4v", ".avi", ".mkv", ".3gp"}
CAMPOS = ["titulo", "tipo", "data", "link", "midia", "plays", "curtidas",
          "comentarios", "origem", "obs"]


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")[:60]


def ler_info(pasta):
    """Lê o cabeçalho entre --- do info.md. Sem YAML: uma chave por linha."""
    arquivo = pasta / "info.md"
    dados = {"pasta": pasta.name}
    if not arquivo.exists():
        return dados
    texto = arquivo.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", texto, re.S)
    if not m:
        return dados
    for linha in m.group(1).splitlines():
        if ":" in linha:
            chave, valor = linha.split(":", 1)
            dados[chave.strip()] = valor.strip()
    legenda = re.search(r"## Legenda\n(.*?)(?=\n## |\Z)", m.group(2), re.S)
    dados["legenda"] = legenda.group(1).strip() if legenda else ""
    return dados


def escrever_info(pasta, dados, corpo):
    linhas = ["---"] + [f"{c}: {dados.get(c, '')}".rstrip() for c in CAMPOS] + ["---", ""]
    (pasta / "info.md").write_text("\n".join(linhas) + corpo, encoding="utf-8")


def arquivos_de_midia(pasta):
    return sorted(p.name for p in pasta.iterdir() if p.suffix.lower() in MIDIA)


def conteudos():
    for status in STATUS.values():
        base = RAIZ / status
        if not base.is_dir():
            continue
        for pasta in sorted(base.iterdir()):
            if pasta.is_dir():
                info = ler_info(pasta)
                info["status"] = status
                info["arquivos"] = arquivos_de_midia(pasta)
                yield info


def celula(texto):
    return str(texto).replace("|", "/").replace("\n", " ")


def gerar():
    itens = list(conteudos())
    bruto = RAIZ / BRUTO
    soltos = arquivos_de_midia(bruto) if bruto.is_dir() else []

    hoje = datetime.date.today().isoformat()
    md = ["# Catálogo de conteúdo - MP Marcenaria (@mp.marcenariaa)", "",
          f"Gerado por `catalogo.py` em {hoje}. Não edite à mão: edite o `info.md` "
          "de cada pasta e rode o script de novo.", "",
          "| status | quantos |", "| --- | --- |"]
    for status, rotulo in ROTULO.items():
        md.append(f"| {rotulo} | {sum(1 for i in itens if i['status'] == status)} |")
    md.append(f"| Material bruto sem uso | {len(soltos)} arquivos |")

    for status, rotulo in ROTULO.items():
        grupo = [i for i in itens if i["status"] == status]
        md += ["", f"## {rotulo}", ""]
        if not grupo:
            md.append("Nada aqui ainda.")
            continue
        if status == "1-postados":
            md += ["| data | tipo | título | plays | curtidas | link | pasta |",
                   "| --- | --- | --- | --- | --- | --- | --- |"]
            for i in sorted(grupo, key=lambda i: i.get("data", "")):
                link = f"[abrir]({i['link']})" if i.get("link") else "falta o link"
                md.append(f"| {i.get('data', '')} | {i.get('tipo', '')} | {celula(i.get('titulo', ''))} "
                          f"| {i.get('plays', '')} | {i.get('curtidas', '')} | {link} "
                          f"| `{status}/{i['pasta']}` |")
        else:
            md += ["| data | tipo | título | mídia | pasta |",
                   "| --- | --- | --- | --- | --- |"]
            for i in sorted(grupo, key=lambda i: i.get("data", "")):
                midia = ", ".join(i["arquivos"]) or celula(i.get("midia", "")) or "sem mídia"
                md.append(f"| {i.get('data', '')} | {i.get('tipo', '')} | {celula(i.get('titulo', ''))} "
                          f"| {celula(midia)} | `{status}/{i['pasta']}` |")

    md += ["", "## Material bruto sem uso", ""]
    md += [f"- `{BRUTO}/{nome}`" for nome in soltos] or ["Nada aqui ainda."]
    (RAIZ / "CATALOGO.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Ponto e vírgula e BOM: é o que o Excel em português abre sem perguntar nada.
    with open(RAIZ / "catalogo.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["status", "data", "tipo", "titulo", "link", "plays", "curtidas",
                    "comentarios", "midia", "pasta", "legenda"])
        for i in itens:
            w.writerow([ROTULO[i["status"]], i.get("data", ""), i.get("tipo", ""),
                        i.get("titulo", ""), i.get("link", ""), i.get("plays", ""),
                        i.get("curtidas", ""), i.get("comentarios", ""),
                        ", ".join(i["arquivos"]) or i.get("midia", ""),
                        f"{i['status']}/{i['pasta']}", i.get("legenda", "")])
    print(f"{len(itens)} conteúdos, {len(soltos)} arquivos soltos no material bruto.")
    print("CATALOGO.md e catalogo.csv atualizados.")


def novo(args):
    data = args.data or datetime.date.today().isoformat()
    pasta = RAIZ / STATUS[args.status] / f"{data}_{args.tipo}_{slug(args.tema)}"
    if pasta.exists():
        sys.exit(f"Já existe: {pasta.relative_to(RAIZ)}")
    pasta.mkdir(parents=True)
    for arquivo in args.midia or []:
        shutil.move(str(RAIZ / BRUTO / arquivo), pasta / arquivo)
    corpo = "## Legenda\n\n(escreva aqui)\n\n## Roteiro\n\n(se for reel)\n"
    escrever_info(pasta, {"titulo": args.tema, "tipo": args.tipo, "data": data,
                          "midia": ", ".join(args.midia or [])}, corpo)
    print(f"Criado: {pasta.relative_to(RAIZ)}")
    gerar()


def postar(args):
    achadas = [p for s in STATUS.values() for p in (RAIZ / s).glob(args.pasta) if p.is_dir()]
    if len(achadas) != 1:
        sys.exit(f"Esperava uma pasta chamada {args.pasta}, achei {len(achadas)}.")
    origem = achadas[0]
    destino = RAIZ / STATUS["postados"] / origem.name
    if origem != destino:
        shutil.move(str(origem), destino)
    texto = (destino / "info.md").read_text(encoding="utf-8")
    texto = re.sub(r"(?m)^link:.*$", f"link: {args.link}", texto, count=1)
    if args.data:
        texto = re.sub(r"(?m)^data:.*$", f"data: {args.data}", texto, count=1)
    (destino / "info.md").write_text(texto, encoding="utf-8")
    print(f"Movido para {destino.relative_to(RAIZ)}")
    gerar()


def main():
    ap = argparse.ArgumentParser(description="Catálogo de conteúdo da MP Marcenaria.")
    sub = ap.add_subparsers(dest="cmd")
    n = sub.add_parser("novo", help="cria a pasta de um conteúdo novo")
    n.add_argument("tipo", choices=TIPOS)
    n.add_argument("tema")
    n.add_argument("--status", choices=STATUS, default="ideias")
    n.add_argument("--data", help="AAAA-MM-DD; padrão é hoje")
    n.add_argument("--midia", nargs="*", help=f"arquivos de {BRUTO} para mover para a pasta")
    p = sub.add_parser("postar", help="move para 1-postados e grava o link")
    p.add_argument("pasta")
    p.add_argument("--link", required=True)
    p.add_argument("--data", help="data em que foi ao ar, AAAA-MM-DD")
    args = ap.parse_args()
    if args.cmd == "novo":
        novo(args)
    elif args.cmd == "postar":
        postar(args)
    else:
        gerar()


if __name__ == "__main__":
    main()
