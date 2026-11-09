#!/usr/bin/env python3
"""Resumo do funil da Jardmolas a partir do pipeline.csv.

Uso:
  python3 funil.py ../../../../jardmolas/operacao/pipeline.csv
  python3 funil.py pipeline.csv --hoje 2026-11-10

Mostra: oportunidades por etapa e valor, próximas ações vencidas e de hoje,
orçamentos sem próxima ação, perdas por motivo e carga por dono.
Linhas com empresa começando por "EXEMPLO" são ignoradas.
"""
import argparse
import csv
import datetime as dt
import sys
from collections import Counter, defaultdict

ETAPAS = ["1-conta-alvo", "2-em-contato", "3-qualificado", "4-orcamento-enviado",
          "5-negociacao-ou-teste", "6-ganho", "7-perdido", "nutricao"]
ABERTAS = set(ETAPAS[:5])


def num(v):
    try:
        return float(str(v).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
    except ValueError:
        return 0.0


def data(v):
    try:
        return dt.date.fromisoformat(str(v).strip())
    except ValueError:
        return None


def brl(x):
    s = f"{x:,.0f}"
    return "R$ " + s.replace(",", ".")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--hoje", help="AAAA-MM-DD (padrão: hoje)")
    a = p.parse_args()
    hoje = data(a.hoje) if a.hoje else dt.date.today()

    try:
        with open(a.csv, encoding="utf-8") as f:
            linhas = [r for r in csv.DictReader(f)
                      if r.get("empresa") and not r["empresa"].strip().upper().startswith("EXEMPLO")]
    except FileNotFoundError:
        sys.exit(f"Arquivo não encontrado: {a.csv}")

    print(f"FUNIL JARDMOLAS  ·  {len(linhas)} oportunidades  ·  {hoje.strftime('%d/%m/%Y')}")
    print("=" * 74)
    if not linhas:
        print("Pipeline vazio. Comece pelo Caçador de Contas e pelo Pré-vendas.")
        return

    por_etapa = defaultdict(lambda: [0, 0.0, 0.0])
    for r in linhas:
        e = r.get("etapa", "").strip() or "sem-etapa"
        v = num(r.get("valor_estimado"))
        prob = num(r.get("probabilidade")) / 100 if r.get("probabilidade") else 0
        por_etapa[e][0] += 1
        por_etapa[e][1] += v
        por_etapa[e][2] += v * prob
    print(f"  {'Etapa':<24}{'Qtde':>6}{'Valor':>16}{'Ponderado':>16}")
    for e in ETAPAS + sorted(k for k in por_etapa if k not in ETAPAS):
        if e in por_etapa:
            q, v, pond = por_etapa[e]
            print(f"  {e:<24}{q:>6}{brl(v):>16}{brl(pond):>16}")
    aberto = sum(por_etapa[e][1] for e in ABERTAS if e in por_etapa)
    pond = sum(por_etapa[e][2] for e in ABERTAS if e in por_etapa)
    print(f"  {'EM ABERTO':<24}{'':>6}{brl(aberto):>16}{brl(pond):>16}")

    vencidas, de_hoje, sem_acao = [], [], []
    for r in linhas:
        if r.get("etapa", "").strip() not in ABERTAS:
            continue
        d = data(r.get("data_proxima_acao", ""))
        if not d:
            sem_acao.append(r)
        elif d < hoje:
            vencidas.append((d, r))
        elif d == hoje:
            de_hoje.append((d, r))

    def mostra(titulo, itens):
        print(f"\n{titulo} ({len(itens)})")
        for d, r in sorted(itens, key=lambda x: x[0]):
            atraso = (hoje - d).days
            tag = f"{atraso}d atraso" if atraso > 0 else "hoje"
            print(f"  [{tag:>10}] {r['empresa'][:28]:<28} {r.get('etapa',''):<22} "
                  f"{r.get('proxima_acao','')[:40]}  ({r.get('dono','?')})")

    mostra("AÇÕES VENCIDAS", vencidas)
    mostra("AÇÕES DE HOJE", de_hoje)
    if sem_acao:
        print(f"\nOPORTUNIDADES ABERTAS SEM PRÓXIMA AÇÃO ({len(sem_acao)}): toda oportunidade precisa de data")
        for r in sem_acao:
            print(f"  {r['empresa'][:30]:<30} {r.get('etapa','')}  ({r.get('dono','?')})")

    perdidos = [r for r in linhas if r.get("etapa", "").strip() == "7-perdido"]
    if perdidos:
        print("\nPERDAS POR MOTIVO")
        for m, q in Counter((r.get("motivo_perda") or "SEM MOTIVO").strip() for r in perdidos).most_common():
            print(f"  {q:>3}  {m}")

    ganhos = por_etapa.get("6-ganho", [0])[0]
    fechados = ganhos + len(perdidos)
    if fechados:
        print(f"\nTaxa de ganho nas fechadas: {ganhos}/{fechados} = {ganhos / fechados * 100:.0f}%")

    carga = Counter(r.get("dono", "?") for r in linhas if r.get("etapa", "").strip() in ABERTAS)
    print("\nOPORTUNIDADES ABERTAS POR DONO")
    for dono, q in carga.most_common():
        print(f"  {q:>3}  {dono}")


if __name__ == "__main__":
    main()
