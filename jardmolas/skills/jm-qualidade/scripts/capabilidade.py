#!/usr/bin/env python3
"""Capabilidade de processo (Cp, Cpk, Pp, Ppk) e carta X-barra/R - Jardmolas.

Uso:
  python capabilidade.py --lie 95 --lse 105 --valores 99.8 100.4 101.1 ...
  python capabilidade.py --lie 95 --lse 105 --arquivo medidas.csv --subgrupo 5
O arquivo pode ter um valor por linha ou valores separados por virgula/;.
--subgrupo N: tamanho do subgrupo racional (pecas consecutivas). Com subgrupo,
Cp/Cpk usam o desvio dentro do subgrupo (R-barra/d2) e Pp/Ppk o desvio total.
Sem subgrupo (N=1) usa amplitude movel.
"""
import argparse
import math
import re
import statistics as st
import sys

D2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078}
A2 = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308}
D3 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
D4 = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}


def fi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def para_numero(t):
    t = t.strip().replace(" ", "")
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?", t):
        return float(t.replace(",", "."))
    return None


def ler(args):
    """Le medidas de --valores ou de um arquivo; devolve (valores, campos ignorados)."""
    if args.valores:
        return args.valores, 0
    txt = open(args.arquivo, encoding="utf-8-sig").read()
    linhas = [l for l in txt.splitlines() if l.strip()]
    tem_ponto_virgula = any(";" in l or "\t" in l for l in linhas)
    valores, ignorados = [], 0
    for l in linhas:
        if tem_ponto_virgula:
            campos = re.split(r"[;\t]", l)
        elif l.count(",") >= 2 or (l.count(",") == 1 and len(linhas) == 1 and " " not in l.strip()):
            campos = l.split(",")           # virgula como separador de valores
        else:
            campos = l.split()              # um valor por linha (ou separados por espaco); virgula = decimal
        if args.coluna:
            campos = campos[args.coluna - 1:args.coluna]
        for c in campos:
            if not c.strip():
                continue
            v = para_numero(c)
            if v is None:
                ignorados += 1
            else:
                valores.append(v)
    return valores, ignorados


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--lie", type=float, help="limite inferior de especificacao")
    p.add_argument("--lse", type=float, help="limite superior de especificacao")
    p.add_argument("--valores", type=float, nargs="+")
    p.add_argument("--arquivo")
    p.add_argument("--subgrupo", type=int, default=1)
    p.add_argument("--coluna", type=int, help="numero da coluna (1 = primeira) em arquivo separado por ; ou tab")
    a = p.parse_args()
    if a.lie is None and a.lse is None:
        sys.exit("Informe --lie e/ou --lse.")
    if not a.valores and not a.arquivo:
        sys.exit("Informe --valores ou --arquivo.")
    x, ignorados = ler(a)
    k = a.subgrupo
    if k < 1 or k > 10:
        sys.exit("--subgrupo deve estar entre 1 e 10.")
    if k > 1:
        x = x[:len(x) - len(x) % k]  # so subgrupos completos, para a media bater com a carta
    n = len(x)
    if n < 10:
        sys.exit("Menos de 10 medidas lidas (%d): nao da para falar em capabilidade." % n)
    print("lidas %d medidas (primeiras: %s)%s" % (n, ", ".join("%g" % v for v in x[:3]),
          " | %d campo(s) nao numerico(s) ignorado(s)" % ignorados if ignorados else ""))
    if a.arquivo and not a.coluna and ignorados > n / 4:
        print("AVISO: muitos campos ignorados - o arquivo tem mais de uma coluna? Use --coluna.")
    media, s_total = st.mean(x), st.stdev(x)
    if s_total == 0:
        sys.exit("Todas as medidas sao iguais: resolucao do instrumento insuficiente para avaliar capabilidade.")
    if k == 1:
        mr = [abs(b - c) for b, c in zip(x[1:], x)]
        s_dentro = st.mean(mr) / D2[2]
        carta = "individuais: LC=%.4f LIC=%.4f LSC=%.4f | amplitude movel media=%.4f LSC=%.4f" % (
            media, media - 3 * s_dentro, media + 3 * s_dentro, st.mean(mr), D4[2] * st.mean(mr))
        fora = [i + 1 for i, v in enumerate(x) if abs(v - media) > 3 * s_dentro]
    else:
        grupos = [x[i:i + k] for i in range(0, n - n % k, k)]
        if len(grupos) < 5:
            sys.exit("Menos de 5 subgrupos completos.")
        xb = [st.mean(g) for g in grupos]
        r = [max(g) - min(g) for g in grupos]
        rbar, xbb = st.mean(r), st.mean(xb)
        s_dentro = rbar / D2[k]
        carta = "X-barra: LC=%.4f LIC=%.4f LSC=%.4f | R: LC=%.4f LIC=%.4f LSC=%.4f" % (
            xbb, xbb - A2[k] * rbar, xbb + A2[k] * rbar, rbar, D3[k] * rbar, D4[k] * rbar)
        fora = [i + 1 for i, (m, rr) in enumerate(zip(xb, r))
                if abs(m - xbb) > A2[k] * rbar or rr > D4[k] * rbar]

    if s_dentro == 0:
        sys.exit("Variacao dentro do subgrupo igual a zero: resolucao do instrumento insuficiente.")
    def indices(s):
        cp = (a.lse - a.lie) / (6 * s) if a.lie is not None and a.lse is not None else None
        lados = []
        if a.lse is not None:
            lados.append((a.lse - media) / (3 * s))
        if a.lie is not None:
            lados.append((media - a.lie) / (3 * s))
        return cp, min(lados)

    cp, cpk = indices(s_dentro)
    pp, ppk = indices(s_total)
    ppm = 0.0
    if a.lse is not None:
        ppm += (1 - fi((a.lse - media) / s_total)) * 1e6
    if a.lie is not None:
        ppm += fi((a.lie - media) / s_total) * 1e6
    reais = sum(1 for v in x if (a.lse is not None and v > a.lse) or (a.lie is not None and v < a.lie))

    print("n=%d  media=%.4f  desvio total=%.4f  desvio dentro=%.4f  min=%.4f  max=%.4f" % (
        n, media, s_total, s_dentro, min(x), max(x)))
    print("Cp=%s  Cpk=%.2f  |  Pp=%s  Ppk=%.2f" % (
        "-" if cp is None else "%.2f" % cp, cpk, "-" if pp is None else "%.2f" % pp, ppk))
    print("fora de especificacao: %d medidas reais | estimado %.0f ppm (assumindo distribuicao normal)" % (reais, ppm))
    print("carta " + carta)
    print("pontos fora de controle (%s): %s" % ("medida" if k == 1 else "subgrupo", fora or "nenhum"))
    pequeno = n < 30
    if pequeno:
        print("AMOSTRA PEQUENA (%d medidas): Cpk apenas indicativo - junte ao menos 30, de preferencia 100 "
              "(ou 25 subgrupos), antes de decidir." % n)
    if fora:
        print("LEITURA: processo instavel - achar a causa especial antes de confiar no Cpk.")
    elif cpk >= 1.67:
        print("LEITURA: capaz com folga (Cpk >= 1,67)." + ("" if pequeno else " Pode reduzir frequencia de inspecao."))
    elif cpk >= 1.33:
        print("LEITURA: capaz (Cpk >= 1,33). Manter plano de controle.")
    elif cpk >= 1.0:
        print("LEITURA: no limite (1,00 <= Cpk < 1,33). Centrar o processo e reduzir variacao; inspecao reforcada.")
    else:
        print("LEITURA: NAO capaz (Cpk < 1,00). Inspecao 100% ate corrigir; rever tolerancia com a engenharia.")
    if cp is not None and cp - cpk > 0.3:
        print("Processo descentrado: Cp %.2f contra Cpk %.2f - ajustar a media rende mais que reduzir variacao." % (cp, cpk))


if __name__ == "__main__":
    main()
