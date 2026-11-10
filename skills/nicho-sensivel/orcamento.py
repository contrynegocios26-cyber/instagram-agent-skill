#!/usr/bin/env python3
"""Conta de verba para oferta de nicho sensível.

Exemplos:
  python3 orcamento.py --preco 197 --margem 0.50
  python3 orcamento.py --preco 297 --margem 0.60 --aprovacao 0.80 --criativos 6
  python3 orcamento.py --lead --valor-lead 40
"""
import argparse


def brl(v: float) -> str:
    s = f"{v:,.0f}" if v >= 100 else f"{v:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--preco", type=float, default=0.0, help="preço de venda (ticket médio)")
    p.add_argument("--margem", type=float, default=0.5,
                   help="margem de contribuição antes de anúncio, de 0 a 1 (padrão 0.5)")
    p.add_argument("--aprovacao", type=float, default=1.0,
                   help="taxa de aprovação do pagamento, de 0 a 1 (padrão 1.0)")
    p.add_argument("--lead", action="store_true", help="oferta de geração de lead")
    p.add_argument("--valor-lead", type=float, default=0.0,
                   help="quanto vale um lead (taxa de fechamento x margem da venda)")
    p.add_argument("--criativos", type=int, default=5, help="criativos na rodada de teste (padrão 5)")
    p.add_argument("--folga", type=float, default=0.30, help="folga sobre o equilíbrio (padrão 0.30)")
    a = p.parse_args()

    for nome, v in (("margem", a.margem), ("aprovacao", a.aprovacao), ("folga", a.folga)):
        if not 0 < v <= 1:
            p.error(f"--{nome} deve estar entre 0 e 1")
    if a.criativos < 1:
        p.error("--criativos deve ser pelo menos 1")

    if a.lead:
        if a.valor_lead <= 0:
            p.error("com --lead informe --valor-lead")
        equilibrio, evento, roas = a.valor_lead, "lead", None
    else:
        if a.preco <= 0:
            p.error("informe --preco")
        equilibrio = a.preco * a.margem * a.aprovacao
        evento, roas = "venda", a.preco / equilibrio

    alvo = equilibrio * (1 - a.folga)
    corte = 1.5 * alvo
    teste = a.criativos * (corte + alvo)
    semana = 50 * alvo

    print(f"Custo por {evento} de equilíbrio   {brl(equilibrio)}")
    if roas:
        print(f"ROAS de equilíbrio              {roas:.2f}")
        print(f"ROAS alvo                       {a.preco / alvo:.2f}")
    print(f"Custo por {evento} alvo            {brl(alvo)}")
    print(f"Corte por criativo sem {evento}    {brl(corte)} (até {brl(2 * alvo)} com sinal forte)")
    print(f"Verba de teste, {a.criativos} criativos     {brl(teste)} em 7 a 10 dias ({brl(teste / 10)} a {brl(teste / 7)} por dia)")
    print(f"Piso de escala por conjunto     {brl(semana)} por semana ({brl(semana / 7)} por dia)")
    print("Escala: +20% a 30% a cada 3 ou 4 dias; volta um degrau se passar do equilíbrio por 3 dias.")
    print(f"Primeiro mês (teste + 2 semanas de validação em 1 conjunto)  {brl(teste + 2 * semana)}")

if __name__ == "__main__":
    main()
