#!/usr/bin/env python3
"""Ferramentas de risco do pack Web3. Sem dependencias, sem rede.

    python3 risco.py tamanho --capital 5000 --risco-pct 2 --perda-pct 40
    python3 risco.py carteira posicoes.tsv
    python3 risco.py balanco ~/.claude/web3/diario.md [--semana 2026-11-02]
    python3 risco.py drawdown --capital 5000 --sequencia -20 -15 30 -10

posicoes.tsv: cabecalho  nome  protocolo  rede  tipo  valor
diario.md:    linhas     DATA | ENTRADA/SAIDA/NOTA | categoria | valor MOEDA | obs
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

LIMITE_EXPOSICAO = 0.30
LIMITE_POSICAO_PADRAO = 0.10


def cmd_tamanho(a):
    perda_max = a.capital * a.risco_pct / 100
    tamanho = perda_max / (a.perda_pct / 100)
    teto = a.capital * a.teto_pct / 100
    print(f"capital de risco {a.capital:.2f}  ·  perda maxima aceita {a.risco_pct:g}% = {perda_max:.2f}")
    print(f"pior cenario da posicao: -{a.perda_pct:g}%")
    print(f"  tamanho pela perda:   {tamanho:.2f}")
    print(f"  teto por posicao:     {teto:.2f}  ({a.teto_pct:g}% do capital)")
    final = min(tamanho, teto)
    print(f"  -> ENTRA NO MAXIMO:   {final:.2f}")
    if final < 20:
        print("  (abaixo de 20: gas provavelmente come o resultado. Ou nao entra, ou e aprendizado com valor a zero.)")


def ler_tsv(caminho):
    linhas = [l.rstrip("\n") for l in open(caminho, encoding="utf-8") if l.strip()]
    cab = [c.strip().lower() for c in linhas[0].split("\t")]
    for l in linhas[1:]:
        campos = [c.strip() for c in l.split("\t")]
        yield dict(zip(cab, campos))


def cmd_carteira(a):
    pos = list(ler_tsv(a.arquivo))
    total = sum(float(p["valor"]) for p in pos)
    print(f"CARTEIRA  ·  {len(pos)} posicoes  ·  total {total:.2f}\n")
    alertas = []
    for chave in ("protocolo", "rede", "tipo"):
        soma = defaultdict(float)
        for p in pos:
            soma[p.get(chave, "?")] += float(p["valor"])
        print(f"por {chave}")
        for k, v in sorted(soma.items(), key=lambda kv: -kv[1]):
            pct = v / total if total else 0
            flag = "  <- acima de 30%" if pct > LIMITE_EXPOSICAO and chave != "tipo" else ""
            print(f"  {k:<24}{v:>12.2f}  {pct * 100:>5.1f}%{flag}")
            if flag:
                alertas.append(f"{chave} {k} com {pct * 100:.0f}%")
        print()
    print("maiores posicoes")
    for p in sorted(pos, key=lambda p: -float(p["valor"]))[:5]:
        pct = float(p["valor"]) / total if total else 0
        teto = 0.40 if p.get("tipo", "") == "stable-lending" else LIMITE_POSICAO_PADRAO
        flag = f"  <- acima de {teto * 100:.0f}%" if pct > teto else ""
        print(f"  {p.get('nome', '?'):<24}{float(p['valor']):>12.2f}  {pct * 100:>5.1f}%{flag}")
    if alertas:
        print("\nREDUZIR: " + "; ".join(alertas))


LINHA = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(ENTRADA|SAIDA|NOTA)\s*\|\s*([^|]*)\|\s*([^|]*)\|?(.*)$", re.I)


def cmd_balanco(a):
    caminho = os.path.expanduser(a.arquivo)
    try:
        linhas = open(caminho, encoding="utf-8").read().splitlines()
    except OSError:
        sys.exit(f"nao achei {caminho}")
    ini = date.fromisoformat(a.semana) if a.semana else None
    fim = ini + timedelta(days=7) if ini else None
    ent, sai = defaultdict(float), defaultdict(float)
    notas = []
    for l in linhas:
        m = LINHA.match(l)
        if not m:
            continue
        d = date.fromisoformat(m.group(1))
        if ini and not (ini <= d < fim):
            continue
        tipo, cat, val = m.group(2).upper(), m.group(3).strip() or "-", m.group(4).strip()
        if tipo == "NOTA":
            notas.append(f"{d}  {m.group(5).strip()}")
            continue
        num = re.search(r"-?[0-9][0-9.,]*", val.replace(" ", ""))
        if not num:
            continue
        v = float(num.group(0).replace(".", "").replace(",", ".")) if num.group(0).count(",") == 1 and num.group(0).count(".") >= 1 \
            else float(num.group(0).replace(",", "."))
        (ent if tipo == "ENTRADA" else sai)[cat] += v
    te, ts = sum(ent.values()), sum(sai.values())
    periodo = f"semana de {ini}" if ini else "todo o diario"
    print(f"BALANCO  ·  {periodo}\n")
    print(f"  entrou   {te:>10.2f}   (" + " · ".join(f"{k} {v:.2f}" for k, v in ent.items()) + ")")
    print(f"  saiu     {ts:>10.2f}   (" + " · ".join(f"{k} {v:.2f}" for k, v in sai.items()) + ")")
    print(f"  liquido  {te - ts:>+10.2f}")
    if a.horas:
        print(f"  horas    {a.horas:>10g}   valor/hora {(te - ts) / a.horas:.2f}")
    if notas:
        print("\nNOTAS\n  " + "\n  ".join(notas))
    if te == 0 and ts > 0:
        print("\n  -> so saida, nenhuma entrada. Leve isso para o /web3-mentor: a trilha pode estar errada.")


def cmd_drawdown(a):
    cap = a.capital
    pico = cap
    pior = 0
    print(f"capital {cap:.2f}")
    for i, pct in enumerate(a.sequencia, 1):
        cap *= 1 + pct / 100
        pico = max(pico, cap)
        dd = (cap - pico) / pico * 100
        pior = min(pior, dd)
        print(f"  {i:>2}. {pct:>+6.1f}%  ->  {cap:>10.2f}   drawdown {dd:>6.1f}%")
    print(f"\n  final {cap:.2f}  ({(cap / a.capital - 1) * 100:+.1f}%)   pior drawdown {pior:.1f}%")
    falta = (a.capital / cap - 1) * 100 if cap > 0 else float("inf")
    if cap < a.capital:
        print(f"  para voltar ao inicio precisa de +{falta:.1f}%. Perda de 50% exige ganho de 100%. E por isso o tamanho vem antes da tese.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("tamanho")
    p.add_argument("--capital", type=float, required=True)
    p.add_argument("--risco-pct", type=float, default=2.0, help="perda maxima aceita, %% do capital")
    p.add_argument("--perda-pct", type=float, required=True, help="pior cenario da posicao, %%")
    p.add_argument("--teto-pct", type=float, default=10.0, help="teto por posicao, %% do capital")
    p.set_defaults(fn=cmd_tamanho)
    p = sub.add_parser("carteira")
    p.add_argument("arquivo")
    p.set_defaults(fn=cmd_carteira)
    p = sub.add_parser("balanco")
    p.add_argument("arquivo", nargs="?", default="~/.claude/web3/diario.md")
    p.add_argument("--semana", help="AAAA-MM-DD do inicio da semana")
    p.add_argument("--horas", type=float)
    p.set_defaults(fn=cmd_balanco)
    p = sub.add_parser("drawdown")
    p.add_argument("--capital", type=float, required=True)
    p.add_argument("--sequencia", type=float, nargs="+", required=True, help="variacoes em %%, ex -20 -15 30")
    p.set_defaults(fn=cmd_drawdown)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
