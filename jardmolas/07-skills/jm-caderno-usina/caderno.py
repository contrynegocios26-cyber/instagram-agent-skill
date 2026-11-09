#!/usr/bin/env python3
"""
caderno.py - lê o backup do app Caderno de Molas e escreve, em Markdown:
  1. o resumo do levantamento,
  2. a lista do que trocar nesta entressafra,
  3. a tabela da proposta de Estoque Garantido (com valores, se houver tabela de preços).

Uso
  python3 caderno.py caderno-sma-2026-12-02.json
  python3 caderno.py backup.json --precos precos.csv --saida proposta-sma.md
  python3 caderno.py backup.json --usina SMA

precos.csv (separado por ponto e vírgula, com cabeçalho):
  codigo;preco_unitario
  JM-SMA-001;38,50
  JM-SMA-002;412,00

Sem dependências. Os preços são da Jardmolas; o script só multiplica.
"""
import argparse
import csv
import json
import math
import sys
from datetime import date

ESTADOS = {"ok": "Boa", "desgaste": "Desgaste", "quebrada": "Quebrada", "faltando": "Faltando"}
TIPOS = {"compressao": "Compressão", "tracao": "Tração", "torcao": "Torção", "dedo": "Dedo", "prato": "Prato", "outra": "Outra"}


def num(v):
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def br(v, casas=2):
    if v is None:
        return ""
    s = "{:,.{c}f}".format(v, c=casas)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def codigo(lev, m):
    return "JM-{}-{:03d}".format((lev.get("sigla") or "XXX").upper(), int(m.get("seq") or 0))


def medidas(m):
    partes = []
    for k, rot in (("d", "d"), ("De", "De"), ("L0", "L0"), ("Li", "Li"), ("Nt", "Nt"), ("Nb", "N"), ("L1", "L1"), ("L2", "L2")):
        v = num(m.get(k))
        if v:
            partes.append("{} {}".format(rot, br(v, 1).rstrip("0").rstrip(",")))
    return " · ".join(partes) or "sem medidas"


def ler_precos(caminho):
    precos = {}
    with open(caminho, encoding="utf-8-sig") as f:
        for linha in csv.DictReader(f, delimiter=";"):
            cod = (linha.get("codigo") or "").strip().upper()
            val = (linha.get("preco_unitario") or "").strip().replace(".", "").replace(",", ".")
            if cod and val:
                precos[cod] = float(val)
    return precos


def relatorio(lev, precos):
    ms = sorted(lev.get("molas", []), key=lambda m: int(m.get("seq") or 0))
    pecas = sum(num(m.get("qtd")) or 0 for m in ms)
    criticas = [m for m in ms if m.get("crit") == "A"]
    trocar = [m for m in ms if m.get("estado") in ("desgaste", "quebrada", "faltando")]
    trocar.sort(key=lambda m: (m.get("crit") or "Z", -(num(m.get("qtd")) or 0)))
    L = []
    nome = " · ".join(x for x in (lev.get("cliente"), lev.get("unidade")) if x)
    L.append("# Caderno de Molas: {}".format(nome))
    L.append("")
    L.append("Levantamento em {} por {}. Contato na usina: {}.".format(
        lev.get("data") or "?", lev.get("tecnico") or "?", lev.get("contato") or "?"))
    if lev.get("exemplo"):
        L.append("")
        L.append("> Atenção: este backup é o EXEMPLO de demonstração do app, com medidas ilustrativas.")
    L.append("")
    L.append("## Resumo")
    L.append("")
    L.append("| Modelos de mola | Peças instaladas | Críticas A | Para trocar agora |")
    L.append("| ---: | ---: | ---: | ---: |")
    L.append("| {} | {} | {} | {} |".format(len(ms), br(pecas, 0), len(criticas), len(trocar)))
    L.append("")
    areas = {}
    for m in ms:
        a = m.get("area") or "Outra"
        areas.setdefault(a, [0, 0, 0])
        areas[a][0] += 1
        areas[a][1] += num(m.get("qtd")) or 0
        areas[a][2] += 1 if m.get("crit") == "A" else 0
    L.append("| Área | Modelos | Peças | Críticas A |")
    L.append("| --- | ---: | ---: | ---: |")
    for a, (i, p, c) in areas.items():
        L.append("| {} | {} | {} | {} |".format(a, i, br(p, 0), c))
    L.append("")
    L.append("## Trocar nesta entressafra")
    L.append("")
    if trocar:
        L.append("| Código | Onde | Função | Estado | Crit. | Qtd. | Medidas |")
        L.append("| --- | --- | --- | --- | --- | ---: | --- |")
        for m in trocar:
            onde = " · ".join(x for x in (m.get("equip"), m.get("tag")) if x)
            L.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                codigo(lev, m), onde, m.get("funcao") or "", ESTADOS.get(m.get("estado"), ""),
                m.get("crit") or "", br(num(m.get("qtd")), 0), medidas(m)))
    else:
        L.append("Nenhuma mola marcada para troca.")
    L.append("")
    L.append("## Proposta de Estoque Garantido")
    L.append("")
    L.append("A Jardmolas mantém na fábrica o estoque mínimo abaixo, reservado para esta usina, e repõe a cada retirada. "
             "Prazo de entrega, reajuste e vigência: ver a proposta comercial (01-caderno-de-molas/estoque-garantido.md).")
    L.append("")
    tem_preco = bool(precos)
    cab = "| Código | Função | Tipo | Crit. | Instaladas | Na usina | Estoque mín. |"
    sep = "| --- | --- | --- | --- | ---: | ---: | ---: |"
    if tem_preco:
        cab += " Preço unit. (R$) | Valor do estoque (R$) |"
        sep += " ---: | ---: |"
    L.append(cab)
    L.append(sep)
    total = 0.0
    sem_preco = []
    for m in ms:
        est = num(m.get("estoque"))
        if not est:
            continue
        cod = codigo(lev, m)
        linha = "| {} | {} | {} | {} | {} | {} | {} |".format(
            cod, m.get("funcao") or "", TIPOS.get(m.get("tipo"), ""), m.get("crit") or "",
            br(num(m.get("qtd")), 0), br(num(m.get("reserva")), 0), br(est, 0))
        if tem_preco:
            pu = precos.get(cod)
            if pu is None:
                sem_preco.append(cod)
                linha += " [preço] | |"
            else:
                total += pu * est
                linha += " {} | {} |".format(br(pu), br(pu * est))
        L.append(linha)
    if tem_preco:
        L.append("")
        L.append("**Valor do estoque reservado: R$ {}**".format(br(total)))
        if sem_preco:
            L.append("")
            L.append("Sem preço na tabela: " + ", ".join(sem_preco))
    so_original = [codigo(lev, m) for m in ms if m.get("original") == "nao"]
    if so_original:
        L.append("")
        L.append("A usina só aceita peça original em: " + ", ".join(so_original) + ". Para essas, oferecer laudo do lote e a ficha técnica para homologação antes de cotar.")
    L.append("")
    L.append("## Próximos passos")
    L.append("")
    L.append("1. Enviar o Caderno em PDF (aba Caderno do app) para {}.".format(lev.get("contato") or "o contato da usina"))
    L.append("2. Marcar a reunião de entrega em até 7 dias após a visita.")
    L.append("3. Orçar as {} molas da lista de troca já com o código JM.".format(len(trocar)))
    L.append("4. Apresentar o Estoque Garantido para as {} molas críticas A.".format(len(criticas)))
    L.append("")
    L.append("_Gerado em {} a partir do backup do app Caderno de Molas._".format(date.today().strftime("%d/%m/%Y")))
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Resumo e proposta a partir do backup do Caderno de Molas.")
    p.add_argument("backup", help="arquivo .json baixado no app")
    p.add_argument("--precos", help="CSV codigo;preco_unitario")
    p.add_argument("--usina", help="sigla da usina, se o backup tiver várias")
    p.add_argument("--saida", help="grava em arquivo em vez de imprimir")
    a = p.parse_args(argv)
    with open(a.backup, encoding="utf-8") as f:
        dados = json.load(f)
    levs = dados.get("levantamentos") or []
    if a.usina:
        levs = [l for l in levs if (l.get("sigla") or "").upper() == a.usina.upper()]
    if not levs:
        print("Nenhum levantamento encontrado no arquivo.", file=sys.stderr)
        return 2
    precos = ler_precos(a.precos) if a.precos else {}
    texto = "\n\n---\n\n".join(relatorio(l, precos) for l in levs)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(texto + "\n")
        print("Gravado em " + a.saida)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
