#!/usr/bin/env python3
"""
score.py - pontua e ranqueia prospects do Growth Partner IA a partir de um CSV.

Lê templates/gp/prospects.csv (ou qualquer CSV com as mesmas colunas), aplica
os sinais e pesos de signals.json e imprime a lista em ordem de prioridade,
com o motivo de cada ponto e os vetos.

O que isto é: uma soma de sinais que você mesmo coletou. O script não acessa a
internet, não consulta o Instagram, não inventa dados. Se a coluna está vazia,
o sinal vale zero.

Colunas esperadas (vazio é permitido):
  nome, handle, whatsapp, cidade, resposta_min, anuncia, nota_google,
  seguidores, posts_30d, site, teve_agencia, ticket, achado, obs

  resposta_min  minutos até a resposta no teste do WhatsApp (ex: 850)
  anuncia       sim/nao
  site          sim/nao  (nao = sem site ou parado)
  teve_agencia  sim/nao
  ticket        ticket médio em reais, só número
  achado        o detalhe específico que vai abrir a mensagem

Uso
  python3 score.py prospects.csv
  python3 score.py prospects.csv --top 10
  python3 score.py prospects.csv --json
  python3 score.py prospects.csv --signals outro.json
"""

import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def to_float(v):
    """'4.8' -> 4.8, '4,8' -> 4.8, 'R$ 12.000' -> 12000, '1.234,56' -> 1234.56, '' -> None."""
    v = str(v or "").strip().replace("R$", "").replace(" ", "")
    if v == "":
        return None
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".")
    elif "," in v:
        v = v.replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", v):
        v = v.replace(".", "")
    try:
        return float(v)
    except ValueError:
        return None


def is_yes(v):
    return str(v or "").strip().lower() in {"sim", "s", "yes", "y", "1", "true", "x"}


def is_no(v):
    return str(v or "").strip().lower() in {"nao", "não", "n", "no", "0", "false", ""}


def check(rule, value):
    """rule like '>= 120', '<= 4', '< 300'. value already float."""
    op, num = rule.split()
    num = float(num)
    return {
        ">=": value >= num,
        "<=": value <= num,
        ">": value > num,
        "<": value < num,
        "==": value == num,
    }[op]


def score_row(row, cfg):
    pts = 0
    reasons = []
    for s in cfg["sinais"]:
        raw = row.get(s["coluna"], "")
        hit = False
        if s["tipo"] == "limiar":
            v = to_float(raw)
            hit = v is not None and check(s["regra"], v)
        elif s["tipo"] == "sim":
            hit = is_yes(raw)
        elif s["tipo"] == "nao":
            hit = is_no(raw)
        if hit:
            pts += s["pontos"]
            reasons.append((s["pontos"], s["nome"]))
    vetos = []
    for v in cfg.get("vetos", []):
        val = to_float(row.get(v["coluna"], ""))
        if val is not None and check(v["regra"], val):
            vetos.append(v["motivo"])
    return pts, reasons, vetos


def fmt_resp(row):
    v = to_float(row.get("resposta_min"))
    if v is None:
        return "WA não testado"
    if v >= 60:
        return "WA %dh%02d" % (int(v // 60), int(v % 60))
    return "WA %dmin" % int(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--signals", default=os.path.join(HERE, "signals.json"))
    a = ap.parse_args()

    with open(a.signals, encoding="utf-8") as f:
        cfg = json.load(f)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]

    if not rows:
        sys.exit("CSV vazio. Preencha templates/gp/prospects.csv com 30 a 50 negócios.")

    out = []
    for r in rows:
        pts, reasons, vetos = score_row(r, cfg)
        out.append({
            "nome": (r.get("nome") or "").strip(),
            "handle": (r.get("handle") or "").strip(),
            "whatsapp": (r.get("whatsapp") or "").strip(),
            "pontos": pts,
            "aborda": pts >= cfg["corte"] and not vetos,
            "motivos": [n for _, n in reasons],
            "vetos": vetos,
            "resposta": fmt_resp(r),
            "achado": (r.get("achado") or "").strip(),
        })
    out.sort(key=lambda x: (-x["pontos"], x["nome"]))
    if a.top:
        out = out[: a.top]

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    corte = cfg["corte"]
    n_ok = sum(1 for o in out if o["aborda"])
    print("PROSPECTS RANQUEADOS   %d na lista, %d acima do corte (%d)" % (len(out), n_ok, corte))
    print("=" * 72)
    for i, o in enumerate(out, 1):
        tag = "->" if o["aborda"] else "  "
        print("%s %2d. %3d  %-28s %-20s %s" % (tag, i, o["pontos"], o["nome"][:28], o["handle"][:20], o["resposta"]))
        for m in o["motivos"]:
            print("           + %s" % m)
        for v in o["vetos"]:
            print("           VETO: %s" % v)
        if o["aborda"] and not o["achado"]:
            print("           FALTA: o achado específico. Sem ele não há mensagem.")
    print("-" * 72)
    print("Aborde só os marcados com ->. Abaixo de %d pontos o tempo rende mais em outro." % corte)


if __name__ == "__main__":
    main()
