#!/usr/bin/env python3
"""
mola.py - calculadora de molas helicoidais da Jardmolas.

Sem dependências. Unidades: mm, N, graus.

Exemplos
  python3 mola.py compressao --d 6 --De 45 --L0 110 --Nt 10
  python3 mola.py compressao --d 6 --De 45 --L0 110 --Nt 10 --pontas abertas --curso 30
  python3 mola.py tracao --d 3 --De 24 --Nb 35 --Li 150 --F0 20
  python3 mola.py torcao --d 4 --De 32 --Nb 6 --L1 60 --L2 40 --giro 45
  python3 mola.py compressao --d 6 --De 45 --L0 110 --Nt 10 --json

O que faz
  Calcula constante (dureza), altura fechada, força, tensão corrigida (Wahl),
  esbeltez, peso e comprimento de arame, e marca o que um engenheiro de molas
  conferiria antes de aceitar o pedido.

O que não faz
  Não substitui o projeto pela norma (EN 13906 / DIN 2089) nem o certificado
  do arame. A resistência do arame é uma ESTIMATIVA para classes DIN 17223 /
  EN 10270-1 de arame trefilado. Para 5160, 6150, 9254 e inox, informe --Rm
  com o valor do certificado.
"""
import argparse
import json
import math
import sys

G_ACO = 79300.0     # N/mm2, módulo de cisalhamento do aço para molas
E_ACO = 206000.0    # N/mm2, módulo de elasticidade
G_INOX = 69000.0
E_INOX = 193000.0
KGF = 9.80665
DENSIDADE = 7.85e-3  # g/mm3

PONTAS = {
    # nome: (espiras ativas = Nt - x, altura fechada = (Nt + y) * d)
    "fechadas_esmerilhadas": (2.0, 0.0),
    "fechadas": (2.0, 1.0),
    "abertas": (0.0, 1.0),
    "abertas_esmerilhadas": (1.0, 0.0),
}


def rm_estimado(d):
    """Resistência mínima aproximada do arame trefilado (MPa) pela bitola."""
    return 2230.0 * d ** -0.19


def wahl(C):
    return (4 * C - 1) / (4 * C - 4) + 0.615 / C


def fator_flexao(C):
    """Fator de correção de tensão de flexão para molas de torção."""
    return (4 * C * C - C - 1) / (4 * C * (C - 1))


def base(d, De):
    if d <= 0 or De <= 0:
        raise ValueError("d e De precisam ser maiores que zero.")
    Dm = De - d
    Di = De - 2 * d
    if Di <= 0:
        raise ValueError("O diâmetro externo precisa ser maior que duas vezes o arame. Confira se De foi medido por fora.")
    return Dm, Di, Dm / d


def compressao(a):
    G = G_INOX if a.inox else G_ACO
    Dm, Di, C = base(a.d, a.De)
    x, y = PONTAS[a.pontas]
    Na = a.Nt - x
    if Na <= 0.5:
        raise ValueError("Espiras ativas insuficientes para esse tipo de ponta.")
    k = G * a.d ** 4 / (8 * Dm ** 3 * Na)
    Ls = (a.Nt + y) * a.d
    r = {
        "tipo": "compressao",
        "Dm_mm": Dm, "Di_mm": Di, "indice_C": C, "espiras_ativas": Na,
        "k_N_mm": k, "k_kgf_mm": k / KGF, "altura_fechada_mm": Ls,
    }
    alertas = []
    Rm = a.Rm or rm_estimado(a.d)
    r["Rm_MPa"] = Rm
    r["Rm_origem"] = "informado" if a.Rm else "estimado pela bitola (DIN 17223)"
    tau_adm = 0.5 * Rm
    if a.L0:
        curso_max = a.L0 - Ls
        r["L0_mm"] = a.L0
        r["curso_ate_fechar_mm"] = curso_max
        if curso_max <= 0:
            alertas.append("Comprimento livre menor que a altura fechada. Medida errada ou espiras contadas a mais.")
        else:
            Fs = k * curso_max
            tau_s = wahl(C) * 8 * Fs * Dm / (math.pi * a.d ** 3)
            r.update({"forca_fechada_N": Fs, "forca_fechada_kgf": Fs / KGF, "tensao_fechada_MPa": tau_s})
            if tau_s > tau_adm:
                alertas.append(
                    "Tensão com a mola fechada ({:.0f} MPa) acima de 50% do Rm ({:.0f} MPa). "
                    "Aceitável se o curso de trabalho for limitado; senão a mola assenta (perde altura). "
                    "Pedir o curso real de trabalho.".format(tau_s, tau_adm))
            esb = a.L0 / Dm
            r["esbeltez_L0_Dm"] = esb
            if esb > 4:
                alertas.append("Esbeltez {:.1f}: risco de flambagem. Perguntar se trabalha com guia (pino ou tubo).".format(esb))
            passo = curso_max / Na + a.d
            fio = a.Nt * math.hypot(math.pi * Dm, passo)
            r["arame_por_peca_m"] = fio / 1000
            r["peso_por_peca_g"] = math.pi * a.d ** 2 / 4 * fio * DENSIDADE
    if a.curso:
        F = k * a.curso
        tau = wahl(C) * 8 * F * Dm / (math.pi * a.d ** 3)
        r.update({"curso_trabalho_mm": a.curso, "forca_trabalho_N": F, "forca_trabalho_kgf": F / KGF, "tensao_trabalho_MPa": tau})
        if tau > 0.45 * Rm:
            alertas.append("Tensão de trabalho acima de 45% do Rm: vida em fadiga curta se o ciclo for repetitivo (peneira, válvula que bate).")
        if a.L0 and a.curso >= a.L0 - Ls:
            alertas.append("O curso pedido fecha a mola. Rever L0 ou espiras.")
    return r, alertas + indice_alertas(C)


def tracao(a):
    G = G_INOX if a.inox else G_ACO
    Dm, Di, C = base(a.d, a.De)
    Na = a.Nb + G / (E_INOX if a.inox else E_ACO)
    k = G * a.d ** 4 / (8 * Dm ** 3 * Na)
    corpo = (a.Nb + 1) * a.d
    r = {"tipo": "tracao", "Dm_mm": Dm, "Di_mm": Di, "indice_C": C, "espiras_ativas": Na,
         "k_N_mm": k, "k_kgf_mm": k / KGF, "corpo_fechado_mm": corpo, "tensao_inicial_N": a.F0}
    alertas = []
    if a.Li and a.Li < corpo:
        alertas.append("Comprimento por dentro dos ganchos menor que o corpo. Confira as medidas.")
    if a.alongamento:
        F = a.F0 + k * a.alongamento
        r.update({"alongamento_mm": a.alongamento, "forca_N": F, "forca_kgf": F / KGF})
        tau = wahl(C) * 8 * F * Dm / (math.pi * a.d ** 3)
        Rm = a.Rm or rm_estimado(a.d)
        r["tensao_corpo_MPa"] = tau
        if tau > 0.45 * Rm:
            alertas.append("Tensão no corpo alta para tração. O gancho é o ponto que quebra primeiro: avaliar raio do gancho.")
    if not a.F0:
        alertas.append("Tensão inicial não informada. Medir na amostra (força para começar a abrir as espiras).")
    return r, alertas + indice_alertas(C)


def torcao(a):
    E = E_INOX if a.inox else E_ACO
    Dm, Di, C = base(a.d, a.De)
    Na = a.Nb + (a.L1 + a.L2) / (3 * math.pi * Dm)
    k_rad = E * a.d ** 4 / (64 * Dm * Na)
    k_grau = k_rad * math.pi / 180
    r = {"tipo": "torcao", "Dm_mm": Dm, "Di_mm": Di, "indice_C": C, "espiras_ativas": Na,
         "k_Nmm_grau": k_grau, "k_kgfcm_grau": k_grau / 98.0665}
    alertas = []
    if a.giro:
        M = k_grau * a.giro
        sigma = fator_flexao(C) * 32 * M / (math.pi * a.d ** 3)
        Rm = a.Rm or rm_estimado(a.d)
        Di_carregada = Dm * a.Nb / (a.Nb + a.giro / 360) - a.d
        r.update({"giro_graus": a.giro, "momento_Nm": M / 1000, "tensao_flexao_MPa": sigma,
                  "Di_carregada_mm": Di_carregada, "eixo_max_recomendado_mm": 0.9 * Di_carregada})
        if sigma > 0.7 * Rm:
            alertas.append("Tensão de flexão acima de 70% do Rm. Mola de torção trabalha bem até ~70% em uso estático; menos em fadiga.")
    alertas.append("Mola de torção deve ser carregada no sentido que FECHA as espiras. Confirmar o sentido de enrolamento com a amostra.")
    return r, alertas + indice_alertas(C)


def indice_alertas(C):
    if C < 4:
        return ["Índice {:.1f} (abaixo de 4): enrolamento difícil, tensão alta na face interna.".format(C)]
    if C > 14:
        return ["Índice {:.1f} (acima de 14): mola instável, embola em caixa e varia muito de medida.".format(C)]
    return []


def imprimir(r, alertas):
    nomes = {
        "Dm_mm": ("Diâmetro médio", "mm"), "Di_mm": ("Diâmetro interno", "mm"), "indice_C": ("Índice D/d", ""),
        "espiras_ativas": ("Espiras ativas", ""), "k_N_mm": ("Constante", "N/mm"), "k_kgf_mm": ("Constante", "kgf/mm"),
        "altura_fechada_mm": ("Altura fechada", "mm"), "L0_mm": ("Comprimento livre", "mm"),
        "curso_ate_fechar_mm": ("Curso até fechar", "mm"), "forca_fechada_N": ("Força fechada", "N"),
        "forca_fechada_kgf": ("Força fechada", "kgf"), "tensao_fechada_MPa": ("Tensão fechada", "MPa"),
        "Rm_MPa": ("Rm do arame", "MPa"), "esbeltez_L0_Dm": ("Esbeltez L0/Dm", ""),
        "arame_por_peca_m": ("Arame por peça", "m"), "peso_por_peca_g": ("Peso por peça", "g"),
        "curso_trabalho_mm": ("Curso de trabalho", "mm"), "forca_trabalho_N": ("Força de trabalho", "N"),
        "forca_trabalho_kgf": ("Força de trabalho", "kgf"), "tensao_trabalho_MPa": ("Tensão de trabalho", "MPa"),
        "corpo_fechado_mm": ("Corpo fechado", "mm"), "tensao_inicial_N": ("Tensão inicial", "N"),
        "alongamento_mm": ("Alongamento", "mm"), "forca_N": ("Força", "N"), "forca_kgf": ("Força", "kgf"),
        "tensao_corpo_MPa": ("Tensão no corpo", "MPa"), "k_Nmm_grau": ("Constante", "N·mm/grau"),
        "k_kgfcm_grau": ("Constante", "kgf·cm/grau"), "giro_graus": ("Giro", "graus"), "momento_Nm": ("Momento", "N·m"),
        "tensao_flexao_MPa": ("Tensão de flexão", "MPa"), "Di_carregada_mm": ("Diâmetro interno carregada", "mm"),
        "eixo_max_recomendado_mm": ("Eixo máximo recomendado", "mm"),
    }
    print("MOLA DE " + r["tipo"].upper().replace("COMPRESSAO", "COMPRESSÃO").replace("TRACAO", "TRAÇÃO").replace("TORCAO", "TORÇÃO"))
    print("=" * 52)
    for k, v in r.items():
        if k in nomes and v is not None:
            nome, un = nomes[k]
            val = "{:,.2f}".format(v).replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(v, float) else str(v)
            print("  {:<30} {:>12} {}".format(nome, val, un))
    if "Rm_origem" in r:
        print("  (Rm {})".format(r["Rm_origem"]))
    print("-" * 52)
    if alertas:
        for al in alertas:
            print("  ! " + al)
    else:
        print("  Sem alertas.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Calculadora de molas Jardmolas (mm, N).")
    sub = p.add_subparsers(dest="tipo", required=True)

    def comuns(sp):
        sp.add_argument("--d", type=float, required=True, help="diâmetro do arame, mm")
        sp.add_argument("--De", type=float, required=True, help="diâmetro externo, mm")
        sp.add_argument("--Rm", type=float, help="resistência do arame do certificado, MPa")
        sp.add_argument("--inox", action="store_true", help="arame inox")
        sp.add_argument("--json", action="store_true", help="saída em JSON")

    c = sub.add_parser("compressao")
    comuns(c)
    c.add_argument("--Nt", type=float, required=True, help="espiras totais")
    c.add_argument("--L0", type=float, help="comprimento livre, mm")
    c.add_argument("--pontas", choices=list(PONTAS), default="fechadas_esmerilhadas")
    c.add_argument("--curso", type=float, help="curso de trabalho, mm")

    t = sub.add_parser("tracao")
    comuns(t)
    t.add_argument("--Nb", type=float, required=True, help="espiras do corpo")
    t.add_argument("--Li", type=float, help="comprimento por dentro dos ganchos, mm")
    t.add_argument("--F0", type=float, default=0.0, help="tensão inicial, N")
    t.add_argument("--alongamento", type=float, help="quanto estica em trabalho, mm")

    o = sub.add_parser("torcao")
    comuns(o)
    o.add_argument("--Nb", type=float, required=True, help="espiras do corpo")
    o.add_argument("--L1", type=float, default=0.0, help="perna 1, mm (do centro da espira)")
    o.add_argument("--L2", type=float, default=0.0, help="perna 2, mm")
    o.add_argument("--giro", type=float, help="giro de trabalho, graus")

    a = p.parse_args(argv)
    try:
        r, al = {"compressao": compressao, "tracao": tracao, "torcao": torcao}[a.tipo](a)
    except ValueError as e:
        print("ERRO: " + str(e), file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"resultado": r, "alertas": al}, ensure_ascii=False, indent=2))
    else:
        imprimir(r, al)
    return 0


if __name__ == "__main__":
    sys.exit(main())
