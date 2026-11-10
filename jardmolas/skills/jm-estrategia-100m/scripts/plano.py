#!/usr/bin/env python3
"""Modelo de crescimento ate a meta de faturamento - Jardmolas.

Uso:
  python plano.py --receita-atual 6 --meta-usd 100 --cambio 5.40 --anos 12
  python plano.py --receita-atual 6 --meta-usd 100 --cambio 5.40 --anos 12 \
      --organico 0.30 --receita-por-func 0.45 --giro-ativo 2.0 --capital-giro 0.25

--receita-atual em milhoes de reais por ano; --meta-usd em milhoes de dolares.
--organico: crescimento organico anual que a empresa julga sustentavel (fracao).
--receita-por-func: receita por funcionario, R$ milhoes/ano (para estimar equipe).
--giro-ativo: receita / ativo fixo (para estimar investimento em fabrica).
--capital-giro: capital de giro como fracao da receita.
Nao ha numero de mercado embutido: todos os parametros sao premissas do usuario.
"""
import argparse
import math


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--receita-atual", type=float, required=True)
    p.add_argument("--meta-usd", type=float, default=100.0)
    p.add_argument("--cambio", type=float, required=True)
    p.add_argument("--anos", type=int, required=True)
    p.add_argument("--organico", type=float, help="crescimento organico anual sustentavel, fracao")
    p.add_argument("--receita-por-func", type=float)
    p.add_argument("--giro-ativo", type=float)
    p.add_argument("--capital-giro", type=float)
    a = p.parse_args()

    meta = a.meta_usd * a.cambio
    mult = meta / a.receita_atual
    cagr = mult ** (1.0 / a.anos) - 1
    print("Meta: US$ %.0f mi = R$ %.0f mi/ano (cambio %.2f)" % (a.meta_usd, meta, a.cambio))
    print("Receita atual: R$ %.1f mi/ano -> multiplicar por %.0fx em %d anos" % (a.receita_atual, mult, a.anos))
    print("Crescimento composto necessario: %.1f%% ao ano" % (cagr * 100))
    print("Tempo para chegar la a taxas constantes: " + " | ".join(
        "%d%%/ano: %.1f anos" % (t * 100, math.log(mult) / math.log(1 + t)) for t in (0.15, 0.25, 0.35, 0.50)))

    print("\n%4s %12s" % ("ano", "receita R$mi") + ("%14s %12s %14s" % ("so organico", "lacuna", "func. estim.")
                                                   if a.organico or a.receita_por_func else ""))
    for n in range(0, a.anos + 1):
        r = a.receita_atual * (1 + cagr) ** n
        linha = "%4d %12.1f" % (n, r)
        if a.organico is not None:
            o = a.receita_atual * (1 + a.organico) ** n
            linha += "%14.1f %12.1f" % (o, r - o)
        elif a.receita_por_func:
            linha += "%14s %12s" % ("-", "-")
        if a.receita_por_func:
            linha += "%14.0f" % (r / a.receita_por_func)
        print(linha)

    if a.organico is not None:
        o_final = a.receita_atual * (1 + a.organico) ** a.anos
        print("\nSo com crescimento organico de %.0f%%/ano chega-se a R$ %.0f mi (%.0f%% da meta)." % (
            a.organico * 100, o_final, o_final / meta * 100))
        if o_final < meta:
            print("Lacuna de R$ %.0f mi/ano a cobrir com aquisicoes, novos mercados ou mais prazo." % (meta - o_final))
    if a.giro_ativo:
        print("Ativo fixo necessario na meta (receita / giro %.1f): R$ %.0f mi" % (a.giro_ativo, meta / a.giro_ativo))
    if a.capital_giro:
        print("Capital de giro na meta (%.0f%% da receita): R$ %.0f mi" % (a.capital_giro * 100, meta * a.capital_giro))
    if a.receita_por_func:
        print("Equipe na meta (R$ %.2f mi por funcionario): %.0f pessoas" % (a.receita_por_func, meta / a.receita_por_func))


if __name__ == "__main__":
    main()
