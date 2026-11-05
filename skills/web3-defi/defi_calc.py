#!/usr/bin/env python3
"""Calculadora DeFi do pack Web3. Sem dependencias, sem rede.

    python3 defi_calc.py apy --apr 8 --compostos 365
    python3 defi_calc.py il --variacao 2.0 [--apr 40 --dias 30]
    python3 defi_calc.py custo --valor 500 --entrada 1.2 --saida 1.2 --ponte 3 --apr 6 --dias 30
    python3 defi_calc.py liq --colateral 1000 --divida 600 --ltv-liq 0.8
"""
import argparse
import math
import sys


def apr_para_apy(apr_pct, n):
    r = apr_pct / 100.0
    if n <= 0:
        return apr_pct
    return ((1 + r / n) ** n - 1) * 100.0


def impermanent_loss(k):
    """Perda vs segurar numa pool 50/50 quando o preco relativo muda por fator k."""
    if k <= 0:
        raise ValueError("variacao deve ser > 0")
    return (2 * math.sqrt(k) / (1 + k) - 1) * 100.0


def cmd_apy(a):
    apy = apr_para_apy(a.apr, a.compostos)
    print(f"APR {a.apr:.2f}%  com {a.compostos} composicoes/ano  ->  APY {apy:.2f}%")
    for d in (7, 30, 90, 365):
        print(f"  {d:>3} dias sobre 100: +{100 * ((1 + a.apr / 100 / a.compostos) ** (a.compostos * d / 365) - 1):.2f}")


def cmd_il(a):
    il = impermanent_loss(a.variacao)
    print(f"preco relativo x{a.variacao:g}  ->  impermanent loss {il:.2f}% (vs segurar os dois)")
    if a.apr is not None:
        ganho = a.apr / 100 * a.dias / 365 * 100
        liquido = ganho + il
        print(f"taxas a {a.apr:g}% APR por {a.dias} dias: +{ganho:.2f}%")
        print(f"liquido vs segurar: {liquido:+.2f}%  ->  {'LP compensa' if liquido > 0 else 'SEGURAR era melhor'}")
    print("\ntabela de referencia:")
    for k in (1.1, 1.25, 1.5, 2, 3, 5, 0.5, 0.2):
        print(f"  x{k:<5g} {impermanent_loss(k):>7.2f}%")


def cmd_custo(a):
    bruto = a.valor * a.apr / 100 * a.dias / 365
    custo = a.entrada + a.saida + a.ponte
    liquido = bruto - custo
    be = custo / (a.valor * a.apr / 100) * 365 if a.apr > 0 else float("inf")
    print(f"valor {a.valor:.2f}  APR {a.apr:g}%  {a.dias} dias")
    print(f"  rendimento bruto     {bruto:>9.2f}")
    print(f"  custo entrada+saida  {-(a.entrada + a.saida):>9.2f}")
    print(f"  ponte                {-a.ponte:>9.2f}")
    print(f"  liquido              {liquido:>9.2f}   ({liquido / a.valor * 100:+.2f}% no periodo)")
    if math.isfinite(be):
        print(f"  break-even em        {be:>9.0f} dias")
    if liquido <= 0:
        print("\n  -> a posicao PERDE dinheiro neste prazo. Aumente o valor, o prazo, ou nao entre.")


def cmd_liq(a):
    if a.divida <= 0:
        print("sem divida, sem liquidacao")
        return
    ltv = a.divida / a.colateral
    preco_liq = a.ltv_liq and (a.divida / (a.colateral * a.ltv_liq))
    queda = (1 - preco_liq) * 100
    print(f"colateral {a.colateral:.2f}  divida {a.divida:.2f}  LTV atual {ltv * 100:.1f}%  LTV de liquidacao {a.ltv_liq * 100:.0f}%")
    print(f"  o colateral pode cair {queda:.1f}% antes da liquidacao (preco relativo x{preco_liq:.3f})")
    if queda < 30:
        print("  -> margem abaixo de 30%. Em cripto isso acontece em um fim de semana. Reduza a divida.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("apy", help="APR para APY")
    p.add_argument("--apr", type=float, required=True)
    p.add_argument("--compostos", type=int, default=365, help="composicoes por ano")
    p.set_defaults(fn=cmd_apy)

    p = sub.add_parser("il", help="impermanent loss")
    p.add_argument("--variacao", type=float, required=True, help="fator de preco relativo, ex 2.0 = dobrou")
    p.add_argument("--apr", type=float, help="APR em taxas, para comparar")
    p.add_argument("--dias", type=int, default=30)
    p.set_defaults(fn=cmd_il)

    p = sub.add_parser("custo", help="rendimento liquido descontando gas e ponte")
    p.add_argument("--valor", type=float, required=True)
    p.add_argument("--apr", type=float, required=True)
    p.add_argument("--dias", type=int, default=30)
    p.add_argument("--entrada", type=float, default=0, help="gas de entrada, na mesma moeda")
    p.add_argument("--saida", type=float, default=0)
    p.add_argument("--ponte", type=float, default=0)
    p.set_defaults(fn=cmd_custo)

    p = sub.add_parser("liq", help="distancia ate a liquidacao")
    p.add_argument("--colateral", type=float, required=True)
    p.add_argument("--divida", type=float, required=True)
    p.add_argument("--ltv-liq", type=float, default=0.8, help="LTV de liquidacao do protocolo, ex 0.8")
    p.set_defaults(fn=cmd_liq)

    a = ap.parse_args()
    try:
        a.fn(a)
    except ValueError as e:
        sys.exit(f"erro: {e}")


if __name__ == "__main__":
    main()
