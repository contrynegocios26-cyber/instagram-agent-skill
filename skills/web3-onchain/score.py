#!/usr/bin/env python3
"""Nota de due diligence do pack Web3. Sem dependencias, sem rede.

    python3 score.py --modelo > projeto.json   # formulario
    python3 score.py projeto.json              # nota + bandeiras

Preencha com fatos e fontes. Campo desconhecido fica null e pontua zero.
"""
import argparse
import json
import sys
from datetime import date

MODELO = {
    "nome": "ProjetoX",
    "fontes": ["explorador", "docs", "dashboard de receita"],
    "oferta": {
        "circulante_sobre_total": 0.35,
        "desbloqueio_90d_pct": 0.18,
        "equipe_mais_investidores_pct": 0.45,
        "top10_holders_pct_excl_contratos": 0.30,
        "dono_pode_mintar": False,
        "dono_pode_pausar": False,
        "dono_pode_mudar_taxa": False,
        "lista_negra": False,
        "timelock_ou_multisig": True,
    },
    "liquidez": {
        "liquidez_usd": 2500000,
        "liquidez_travada_meses": 12,
        "volume_sobre_liquidez": 0.8,
        "slippage_1pct_posicao": 0.004,
        "taxa_na_transferencia": False,
        "honeypot": False,
    },
    "contrato": {
        "verificado": True,
        "auditoria_publica": True,
        "proxy_atualizavel": True,
        "proxy_com_timelock": True,
        "idade_meses": 14,
        "incidentes": 0,
    },
    "uso": {
        "explica_em_uma_frase": True,
        "receita_90d_usd": 400000,
        "tendencia_receita_90d": -0.4,
        "usuarios_ativos_tendencia_90d": 0.1,
        "equipe_publica": True,
        "captura_valor": "taxa",
    },
}


def g(d, k):
    return d.get(k) if isinstance(d, dict) else None


def bloco_oferta(o, ver, ama, nsei):
    p = 0
    v = g(o, "circulante_sobre_total")
    if v is None: nsei.append("circulante sobre total")
    else: p += 5 if v >= 0.5 else 3 if v >= 0.25 else 1
    v = g(o, "desbloqueio_90d_pct")
    if v is None: nsei.append("desbloqueio em 90 dias")
    else:
        p += 5 if v <= 0.03 else 3 if v <= 0.10 else 1
        if v > 0.10: ama.append(f"desbloqueio de {v*100:.0f}% da oferta em 90 dias")
    v = g(o, "equipe_mais_investidores_pct")
    if v is None: nsei.append("alocacao equipe + investidores")
    else:
        p += 5 if v <= 0.30 else 3 if v <= 0.50 else 0
        if v > 0.50: ama.append(f"equipe + investidores detem {v*100:.0f}%")
    v = g(o, "top10_holders_pct_excl_contratos")
    if v is None: nsei.append("top 10 holders")
    else:
        p += 5 if v <= 0.20 else 3 if v <= 0.40 else 0
        if v > 0.50: ver.append(f"top 10 holders nao identificados com {v*100:.0f}%")
    poderes = [k for k in ("dono_pode_mintar", "dono_pode_pausar", "dono_pode_mudar_taxa", "lista_negra") if g(o, k)]
    protegido = g(o, "timelock_ou_multisig")
    if not poderes: p += 5
    elif protegido: p += 2; ama.append("dono tem poderes (" + ", ".join(poderes) + "), com timelock/multisig")
    else: ver.append("dono tem poderes sem timelock/multisig: " + ", ".join(poderes))
    return p


def bloco_liquidez(l, ver, ama, nsei):
    p = 0
    v = g(l, "liquidez_usd")
    if v is None: nsei.append("liquidez em USD")
    else: p += 5 if v >= 1_000_000 else 3 if v >= 100_000 else 1
    v = g(l, "liquidez_travada_meses")
    if v is None: nsei.append("liquidez travada / quem detem os LP tokens")
    else:
        p += 5 if v >= 12 else 3 if v >= 3 else 0
        if v == 0: ver.append("liquidez nao travada")
    v = g(l, "volume_sobre_liquidez")
    if v is None: nsei.append("volume sobre liquidez")
    else:
        p += 5 if 0.05 <= v <= 3 else 2
        if v > 5: ama.append("volume muito acima da liquidez (lavagem?)")
    v = g(l, "slippage_1pct_posicao")
    if v is None: nsei.append("slippage para sair")
    else:
        p += 5 if v <= 0.01 else 3 if v <= 0.03 else 0
        if v > 0.05: ama.append(f"slippage de {v*100:.1f}% para sair")
    if g(l, "honeypot"): ver.append("honeypot: nao da para vender")
    elif g(l, "taxa_na_transferencia"): ama.append("taxa na transferencia"); p += 2
    elif g(l, "honeypot") is None: nsei.append("honeypot / taxa na transferencia")
    else: p += 5
    return p


def bloco_contrato(c, ver, ama, nsei):
    p = 0
    v = g(c, "verificado")
    if v is None: nsei.append("contrato verificado")
    elif v: p += 6
    else: ver.append("contrato nao verificado")
    v = g(c, "auditoria_publica")
    if v is None: nsei.append("auditoria")
    elif v: p += 5
    else: ama.append("sem auditoria publica")
    if g(c, "proxy_atualizavel"):
        if g(c, "proxy_com_timelock"): p += 3; ama.append("proxy atualizavel, com timelock")
        else: ver.append("proxy atualizavel sem timelock")
    elif g(c, "proxy_atualizavel") is None: nsei.append("proxy atualizavel")
    else: p += 5
    v = g(c, "idade_meses")
    if v is None: nsei.append("idade do contrato")
    else: p += 5 if v >= 12 else 3 if v >= 3 else 1
    v = g(c, "incidentes")
    if v is None: nsei.append("incidentes")
    elif v == 0: p += 4
    else: ama.append(f"{v} incidente(s) de seguranca"); p += 1
    return p


def bloco_uso(u, ver, ama, nsei):
    p = 0
    v = g(u, "explica_em_uma_frase")
    if v is None: nsei.append("o que faz, em uma frase")
    elif v: p += 4
    else: ama.append("nao da para explicar em uma frase")
    v = g(u, "receita_90d_usd")
    if v is None: nsei.append("receita real em 90 dias")
    else:
        p += 6 if v >= 1_000_000 else 4 if v >= 100_000 else 2 if v > 0 else 0
        if v == 0: ama.append("receita real zero")
    v = g(u, "tendencia_receita_90d")
    if v is None: nsei.append("tendencia de receita")
    else:
        p += 5 if v >= 0 else 2 if v >= -0.3 else 0
        if v < -0.3: ama.append(f"receita 90d em queda de {abs(v)*100:.0f}%")
    v = g(u, "usuarios_ativos_tendencia_90d")
    if v is None: nsei.append("tendencia de usuarios")
    else: p += 4 if v >= 0 else 1
    v = g(u, "equipe_publica")
    if v is None: nsei.append("equipe")
    elif v: p += 3
    else: ama.append("equipe anonima: exige liquidez travada e contrato imutavel")
    v = g(u, "captura_valor")
    if v is None: nsei.append("captura de valor")
    elif v in ("taxa", "queima", "receita", "governanca_sobre_receita"): p += 3
    else: ama.append("token so com 'utilidade' vaga")
    return p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--modelo", action="store_true", help="imprime o formulario JSON")
    a = ap.parse_args()
    if a.modelo or not a.arquivo:
        print(json.dumps(MODELO, indent=2, ensure_ascii=False))
        return
    d = json.load(open(a.arquivo, encoding="utf-8"))
    ver, ama, nsei = [], [], []
    blocos = [
        ("oferta e distribuicao", bloco_oferta(d.get("oferta"), ver, ama, nsei)),
        ("liquidez e mercado", bloco_liquidez(d.get("liquidez"), ver, ama, nsei)),
        ("contrato e seguranca", bloco_contrato(d.get("contrato"), ver, ama, nsei)),
        ("uso real e receita", bloco_uso(d.get("uso"), ver, ama, nsei)),
    ]
    nota = sum(p for _, p in blocos)
    if ver: faixa = "NAO ENTRA (veto por bandeira vermelha)"
    elif nota >= 80: faixa = "mapeado"
    elif nota >= 60: faixa = "cautela"
    elif nota >= 40: faixa = "so carteira de queima, valor a zero"
    else: faixa = "nao entra"
    print(f"ANALISE  ·  {d.get('nome', '?')}  ·  {date.today().isoformat()}\n")
    for nome, p in blocos:
        print(f"  {nome:<24}{p:>3} / 25")
    print(f"  {'nota':<24}{nota:>3} / 100   ·   faixa: {faixa}\n")
    print("BANDEIRAS VERMELHAS (veto)\n  " + ("\n  ".join(ver) if ver else "nenhuma") + "\n")
    print("BANDEIRAS AMARELAS\n  " + ("\n  ".join(ama) if ama else "nenhuma") + "\n")
    print("NAO SEI (pontuou zero)\n  " + ("\n  ".join(nsei) if nsei else "nenhum") + "\n")
    print("Nota alta = riscos conhecidos mapeados. Nunca = 'bom investimento'. Tamanho e /web3-risco.")


if __name__ == "__main__":
    main()
