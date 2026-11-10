#!/usr/bin/env python3
"""Custo e preco de venda de molas por faixa de quantidade - Jardmolas.

Exemplo (aco carbono, em reais):
  python custo.py --massa-g 18.7 --arame 14.50 --perda 0.05 --qtds 500 2000 10000 \
      --setup-h 1.5 --taxa-maq 120 --pecas-h 1800 --forno-peca 0.03 --acab-kg 6 \
      --inspecao-peca 0.02 --embalagem-peca 0.01 --indiretos 0.25 \
      --impostos 0.18 --comissao 0.03 --margem 0.20

Exemplo (liga importada, arame em dolar):
  python custo.py --massa-g 62 --arame-usd 95 --cambio 5.40 --internacao 0.35 --perda 0.10 \
      --qtds 50 200 1000 --setup-h 3 --taxa-maq 150 --pecas-h 400 --forno-lote 900 \
      --extra "decapagem:1.20" --extra "ensaio 100%:0.80" --databook-lote 350 \
      --indiretos 0.25 --impostos 0.18 --margem 0.30

Todos os percentuais sao fracoes (0.18 = 18%). O script nao conhece os numeros
da fabrica: taxa-hora, impostos e margem vem do usuario/financeiro.
Preco = custo total / (1 - impostos - comissao - frete - margem).
"""
import argparse
import json
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--massa-g", type=float, required=True, help="massa de fio por peca, g (da ficha tecnica)")
    p.add_argument("--arame", type=float, help="preco do arame posto fabrica, R$/kg")
    p.add_argument("--arame-usd", type=float, help="preco do arame, US$/kg (alternativa a --arame)")
    p.add_argument("--cambio", type=float, help="R$/US$")
    p.add_argument("--internacao", type=float, default=0.0,
                   help="fracao sobre o valor em reais: frete internacional, seguro, impostos nao recuperaveis, despachante")
    p.add_argument("--perda", type=float, default=0.05, help="perda de material (setup, pontas, refugo)")
    p.add_argument("--qtds", type=int, nargs="+", required=True, help="faixas de quantidade a cotar")
    p.add_argument("--setup-h", type=float, default=0.0, help="horas de setup por lote")
    p.add_argument("--taxa-maq", type=float, default=0.0, help="R$/h da maquina com operador")
    p.add_argument("--pecas-h", type=float, required=True, help="producao em regime, pecas/h")
    p.add_argument("--forno-peca", type=float, default=0.0, help="tratamento termico, R$/peca")
    p.add_argument("--forno-lote", type=float, default=0.0, help="tratamento termico, R$/carga de forno (ciclos longos)")
    p.add_argument("--pecas-carga", type=int, default=0, help="pecas por carga de forno (0 = lote inteiro numa carga)")
    p.add_argument("--acab-kg", type=float, default=0.0, help="acabamento superficial, R$/kg")
    p.add_argument("--acab-peca", type=float, default=0.0, help="acabamento superficial, R$/peca")
    p.add_argument("--inspecao-peca", type=float, default=0.0)
    p.add_argument("--embalagem-peca", type=float, default=0.0)
    p.add_argument("--extra", action="append", default=[], help='operacao extra por peca: "nome:valor"')
    p.add_argument("--databook-lote", type=float, default=0.0, help="documentacao/ensaios por lote, R$")
    p.add_argument("--ferramental", type=float, default=0.0, help="ferramental dedicado, R$ (cobrado a parte ou diluido)")
    p.add_argument("--diluir-ferramental", action="store_true", help="diluir o ferramental no preco da peca")
    p.add_argument("--indiretos", type=float, default=0.0, help="custos indiretos de fabricacao, fracao sobre a transformacao")
    p.add_argument("--impostos", type=float, required=True, help="impostos sobre a venda (por dentro), fracao")
    p.add_argument("--comissao", type=float, default=0.0)
    p.add_argument("--frete", type=float, default=0.0, help="frete de venda como fracao do preco (CIF)")
    p.add_argument("--margem", type=float, required=True, help="margem liquida alvo sobre o preco")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.arame is None:
        if a.arame_usd is None or a.cambio is None:
            sys.exit("Informe --arame (R$/kg) ou --arame-usd com --cambio.")
        arame = a.arame_usd * a.cambio * (1 + a.internacao)
    else:
        arame = a.arame
    divisor = 1 - a.impostos - a.comissao - a.frete - a.margem
    if divisor <= 0:
        sys.exit("Impostos + comissao + frete + margem passam de 100% do preco.")
    extras = []
    for e in a.extra:
        try:
            nome, valor = e.rsplit(":", 1)
            extras.append((nome.strip(), float(valor)))
        except ValueError:
            sys.exit('--extra deve ser "nome:valor", recebi: %s' % e)

    kg = a.massa_g / 1000.0
    linhas = []
    for q in a.qtds:
        material = kg * (1 + a.perda) * arame
        maquina = (a.setup_h * a.taxa_maq) / q + a.taxa_maq / a.pecas_h
        cargas = 1 if not a.pecas_carga else -(-q // a.pecas_carga)
        forno = a.forno_peca + a.forno_lote * cargas / q
        acab = a.acab_kg * kg + a.acab_peca
        outros = a.inspecao_peca + a.embalagem_peca + sum(v for _, v in extras) + a.databook_lote / q
        transformacao = maquina + forno + acab + outros
        indiretos = transformacao * a.indiretos
        ferr = a.ferramental / q if a.diluir_ferramental else 0.0
        custo = material + transformacao + indiretos + ferr
        preco = custo / divisor
        minimo = custo / (1 - a.impostos - a.comissao - a.frete)
        # sensibilidade: arame 10% mais caro, mesma margem
        preco_arame10 = (custo + 0.10 * material) / divisor
        linhas.append({
            "quantidade": q, "material": material, "maquina": maquina, "forno": forno,
            "acabamento": acab, "outros": outros, "indiretos": indiretos, "ferramental_diluido": ferr,
            "custo_unitario": custo, "preco_unitario": preco, "preco_minimo_margem_zero": minimo,
            "total_lote": preco * q, "margem_reais_lote": preco * q * a.margem,
            "peso_material_no_custo": material / custo,
            "preco_se_arame_sobe_10pct": preco_arame10,
        })
    saida = {"arame_R$_kg": arame, "massa_g": a.massa_g, "perda": a.perda, "impostos": a.impostos,
             "comissao": a.comissao, "frete": a.frete, "margem": a.margem,
             "ferramental_a_parte": 0.0 if a.diluir_ferramental else a.ferramental, "faixas": linhas}
    if a.json:
        print(json.dumps(saida, ensure_ascii=False, indent=2))
        return
    print("Arame: R$ %.2f/kg | massa %.1f g | perda %.0f%% | impostos %.1f%% | comissao %.1f%% | frete %.1f%% | margem %.1f%%" % (
        arame, a.massa_g, a.perda * 100, a.impostos * 100, a.comissao * 100, a.frete * 100, a.margem * 100))
    print("%9s %9s %9s %9s %9s %9s %9s %10s %10s %12s %7s" % (
        "qtd", "material", "maquina", "forno", "acabam.", "outros", "indiret.", "CUSTO/pc", "PRECO/pc", "total lote", "%mat"))
    for l in linhas:
        print("%9d %9.3f %9.3f %9.3f %9.3f %9.3f %9.3f %10.3f %10.3f %12.2f %6.0f%%" % (
            l["quantidade"], l["material"], l["maquina"], l["forno"], l["acabamento"], l["outros"],
            l["indiretos"], l["custo_unitario"], l["preco_unitario"], l["total_lote"],
            l["peso_material_no_custo"] * 100))
    print("Piso de negociacao (margem zero) por faixa: " + " | ".join(
        "%d: R$ %.3f" % (l["quantidade"], l["preco_minimo_margem_zero"]) for l in linhas))
    print("Se o arame subir 10%%, preco para manter a margem: " + " | ".join(
        "%d: R$ %.3f" % (l["quantidade"], l["preco_se_arame_sobe_10pct"]) for l in linhas))
    if a.ferramental and not a.diluir_ferramental:
        print("Ferramental cobrado a parte: R$ %.2f" % a.ferramental)


if __name__ == "__main__":
    main()
