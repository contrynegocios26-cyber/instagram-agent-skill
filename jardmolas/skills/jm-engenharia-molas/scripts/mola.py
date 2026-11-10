#!/usr/bin/env python3
"""Calculadora de molas helicoidais de fio redondo - Jardmolas.

Compressao, tracao, torcao e mola de valvula de retencao dupla portinhola.
Unidades: mm, N, MPa (N/mm2), N.mm, graus, graus Celsius.

Metodo: formulas classicas (SMI / EN 13906-1/-2/-3 / Shigley). O resultado e
uma verificacao de projeto; a mola so e liberada depois do ensaio de carga
do lote-piloto. Rm do certificado do arame sempre vence o Rm estimado.

Uso:
  python mola.py materiais
  python mola.py compressao --material sae1070-sh --d 3 --De 25 --Na 8 --L0 60 --L1 50 --L2 40
  python mola.py tracao     --material inox302 --d 2 --De 16 --Nb 20 --Fi 15 --L1 80 --L2 110
  python mola.py torcao     --material x750-no1 --d 4 --De 34 --Nb 14 --perna1 40 --perna2 40 --ang1 20 --ang2 105
  python mola.py portinhola --material x750-no1 --d 4 --De 34 --Nb 14 --perna1 40 --perna2 40 \
        --raio 95 --pre-ang 20 --abertura 85 --montagem independente
  python mola.py dimensionar --material x750-mola --k 12 --Fmax 300 --De-max 30 --L0 70
Acrescente --json para saida em JSON, --temp T para corrigir G/E pela temperatura
e --Rm X para usar o limite de resistencia do certificado do arame.
"""
import argparse
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(AQUI, "..", "references", "materiais.json")

BITOLAS = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70,
           0.80, 0.90, 1.00, 1.10, 1.20, 1.25, 1.40, 1.50, 1.60, 1.80, 2.00,
           2.20, 2.25, 2.50, 2.80, 3.00, 3.20, 3.50, 3.80, 4.00, 4.50, 5.00,
           5.50, 6.00, 6.50, 7.00, 8.00, 9.00, 10.0, 11.0, 12.0, 12.7, 14.0,
           16.0]


def carregar():
    with open(BANCO, encoding="utf-8") as f:
        return json.load(f)


def material(nome):
    banco = carregar()["materiais"]
    if nome not in banco:
        sys.exit("Material '%s' nao existe. Rode: python mola.py materiais" % nome)
    return banco[nome]


def interp(tabela, x):
    """Interpolacao linear em [[x, y], ...]; fora da faixa devolve None."""
    pts = sorted(tabela)
    if x < pts[0][0] or x > pts[-1][0]:
        return None
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 != x0 else y0
    return pts[-1][1]


def rm_estimado(mat, d):
    """Limite de resistencia a tracao minimo estimado (MPa) para a bitola d."""
    modelo = mat["rm"]
    if modelo["tipo"] == "potencia":  # Rm = A / d^m
        for f in modelo["faixas"]:
            if f["dmin"] <= d <= f["dmax"]:
                return f["A"] / d ** f["m"] * modelo.get("fator", 1.0), None
        return None, "bitola %.2f mm fora da faixa do modelo de Rm" % d
    if modelo["tipo"] == "tabela":  # [[dmax, Rm], ...]
        for dmax, rm in modelo["faixas"]:
            if d <= dmax:
                return rm, None
        return None, "bitola %.2f mm acima da faixa tabelada de Rm" % d
    if modelo["tipo"] == "certificado":
        return None, "este material nao tem Rm tabelado no banco"
    return None, "modelo de Rm desconhecido"


def modulos(mat, temp):
    """Devolve (G, E, avisos) corrigidos para a temperatura de servico."""
    avisos = []
    G, E = mat["G"], mat["E"]
    if temp is not None and temp > 40:
        fator = None
        if "modulo_vs_temp" in mat:
            fator = interp(mat["modulo_vs_temp"], temp)
        if fator is None:
            avisos.append("sem curva de modulo x temperatura para este material: "
                          "G e E mantidos a 20 C - a mola real fica mais mole a quente")
        else:
            G, E = G * fator, E * fator
    if temp is not None and temp > mat.get("temp_max", 1e9):
        avisos.append("temperatura %.0f C acima do limite recomendado para molas deste "
                      "material/condicao (%.0f C): relaxacao acelerada, trocar material ou tratamento"
                      % (temp, mat["temp_max"]))
    return G, E, avisos


def wahl(C):
    return (4 * C - 1) / (4 * C - 4) + 0.615 / C


def checa_indice(C, avisos):
    if C < 4:
        avisos.append("indice C=%.2f < 4: dificil de enrolar, risco de trinca no fio e ferramental especial" % C)
    elif C > 12:
        avisos.append("indice C=%.2f > 12: mola instavel, enrosca no manuseio e tolerancias abrem" % C)


def base(args):
    mat = material(args.material)
    d, De = args.d, args.De
    D = De - d
    if D <= d:
        sys.exit("Diametro externo menor ou igual a 2x o fio: geometria impossivel.")
    avisos = []
    G, E, av = modulos(mat, args.temp)
    avisos += av
    if args.Rm:
        Rm, origem = args.Rm, "certificado do arame (informado)"
    else:
        Rm, erro = rm_estimado(mat, d)
        origem = "estimado pelo banco de materiais (minimo de norma/aproximacao)"
        if erro:
            avisos.append(erro + " - informe --Rm do certificado")
    C = D / d
    checa_indice(C, avisos)
    return mat, d, De, D, C, G, E, Rm, origem, avisos


# ---------------------------------------------------------------- compressao
EXTREMIDADES = {
    "fechada-retificada": (2, 0),  # (espiras inativas, espiras extras no solido)
    "fechada": (2, 1),
    "aberta-retificada": (1, 0),
    "aberta": (0, 1),
}


def compressao(args):
    mat, d, De, D, C, G, E, Rm, origem, avisos = base(args)
    Na = args.Na
    inativas, extra = EXTREMIDADES[args.extremidades]
    Nt = Na + inativas
    Ls = (Nt + extra) * d
    L0 = args.L0
    if L0 <= Ls:
        sys.exit("Comprimento livre (%.2f) menor que o comprimento solido (%.2f)." % (L0, Ls))
    k = G * d ** 4 / (8 * D ** 3 * Na)
    Kw1 = wahl(C)
    Kw2 = 1 + 0.5 / C

    def ponto(L):
        F = k * (L0 - L)
        tau = 8 * F * D / (math.pi * d ** 3)
        return {"L": L, "flecha": L0 - L, "F": F, "tau": tau, "tau_wahl": tau * Kw1}

    pontos = {}
    for nome, L in (("L1", args.L1), ("L2", args.L2)):
        if L is not None:
            if L < Ls:
                avisos.append("%s=%.2f mm esta abaixo do comprimento solido %.2f mm" % (nome, L, Ls))
            pontos[nome] = ponto(L)
    solido = ponto(Ls)
    if args.extremidades == "fechada-retificada":
        passo = (L0 - 2 * d) / Na
    elif args.extremidades == "fechada":
        passo = (L0 - 3 * d) / Na
    elif args.extremidades == "aberta-retificada":
        passo = L0 / (Na + 1)
    else:
        passo = (L0 - d) / Na
    ang_helice = math.degrees(math.atan(passo / (math.pi * D)))
    if ang_helice > 12:
        avisos.append("angulo de helice %.1f graus > 12: formulas perdem precisao" % ang_helice)

    # Folga minima entre espiras na carga maxima (EN 13906-1: Sa ~ (0,0015 D^2/d + 0,1 d) Na)
    Sa = (0.0015 * D ** 2 / d + 0.1 * d) * Na
    Lmin = Ls + Sa
    if "L2" in pontos and pontos["L2"]["L"] < Lmin:
        avisos.append("L2=%.2f mm deixa menos folga que o minimo recomendado (Ls+Sa=%.2f mm): "
                      "risco de espiras batendo e carga fora da reta" % (pontos["L2"]["L"], Lmin))

    # Tensao admissivel estatica (criterio SMI)
    adm = mat["admissivel"]["compressao"]
    veredito = None
    if Rm:
        lim_sem = adm["sem_preset"] * Rm
        lim_com = adm["com_preset"] * Rm
        t1 = solido["tau"] * Kw1
        t2 = solido["tau"] * Kw2
        if t1 <= lim_sem:
            veredito = "OK ate o solido sem pre-assentamento (%.0f <= %.0f MPa)" % (t1, lim_sem)
        elif mat.get("preset_nao_recomendado"):
            veredito = ("ACIMA do admissivel no solido (%.0f > %.0f MPa). Nesta liga o pre-assentamento a frio "
                        "nao e recomendado para servico quente: limite o curso por batente ou reprojete" % (t1, lim_sem))
            avisos.append("tensao no solido acima do admissivel sem presetting; confira se a mola chega ao solido em servico")
        elif t2 <= lim_com:
            veredito = ("So fecha ate o solido COM pre-assentamento/presetting "
                        "(%.0f MPa com Kw2 <= %.0f MPa); sem preset a mola perde altura" % (t2, lim_com))
        else:
            veredito = ("SOBRETENSIONADA no solido (%.0f MPa com Kw2 > %.0f MPa): a mola toma assentamento "
                        "permanente. Limite o curso ou reprojete" % (t2, lim_com))
            avisos.append("tensao no solido acima do admissivel mesmo com presetting")
        if "L2" in pontos:
            uso = pontos["L2"]["tau_wahl"] / lim_sem
            pontos["L2"]["uso_admissivel_sem_preset"] = uso

    # Flambagem (EN 13906-1), nu = coeficiente de apoio
    nu = args.apoio
    razao = G / E
    arg = (1 - razao) / (0.5 + razao) * (math.pi * D / (nu * L0)) ** 2
    if arg >= 1:
        flamb = {"flamba": False, "flecha_critica": None}
    else:
        sK = L0 * 0.5 / (1 - razao) * (1 - math.sqrt(1 - arg))
        flamb = {"flamba": True, "flecha_critica": sK, "L_critico": L0 - sK}
        Lmenor = min([p["L"] for p in pontos.values()] or [Ls])
        if L0 - Lmenor > sK:
            avisos.append("FLAMBAGEM: a flecha de trabalho passa da critica (%.1f mm). "
                          "Guiar por pino/camisa ou reduzir L0/D (hoje %.1f)" % (sK, L0 / D))

    # Fadiga (somente acos carbono/baixa liga - dados de Zimmerli, vida infinita)
    fadiga = None
    if "L1" in pontos and "L2" in pontos and Rm:
        a, b = sorted([pontos["L1"]["tau_wahl"], pontos["L2"]["tau_wahl"]])
        ta, tm = (b - a) / 2, (b + a) / 2
        fadiga = {"tau_alternada": ta, "tau_media": tm}
        if mat.get("zimmerli"):
            Ssu = 0.67 * Rm
            for nome, (Ssa, Ssm) in (("sem_shot_peening", (241.0, 379.0)), ("com_shot_peening", (398.0, 534.0))):
                Sse = Ssa / (1 - Ssm / Ssu)  # Goodman
                n = 1 / (ta / Sse + tm / Ssu)
                fadiga["fs_vida_infinita_" + nome] = n
            if fadiga["fs_vida_infinita_com_shot_peening"] < 1.3:
                avisos.append("fadiga: fator de seguranca para vida infinita abaixo de 1,3 mesmo com shot peening "
                              "- so serve para vida limitada; reduza a amplitude de tensao se a aplicacao e ciclica")
        else:
            fadiga["nota"] = ("sem dados de fadiga tabelados para este material: validar por ensaio "
                              "de ciclagem ou dados do fabricante do arame")

    rho = mat["rho"]
    comp_fio = math.pi * D * Nt / math.cos(math.radians(ang_helice))
    massa = comp_fio * math.pi * d ** 2 / 4 * rho * 1e-9  # kg
    freq = d * 1e-3 / (2 * math.pi * Na * (D * 1e-3) ** 2) * math.sqrt(G * 1e6 / (2 * rho))
    dDe = 0.1 * (passo ** 2 - 0.8 * passo * d - 0.2 * d ** 2) / D

    return {
        "tipo": "compressao", "material": mat["nome"], "condicao": mat.get("condicao", ""),
        "d": d, "De": De, "D": D, "Di": D - d, "C": C, "Na": Na, "Nt": Nt, "extremidades": args.extremidades,
        "L0": L0, "Ls": Ls, "passo": passo, "angulo_helice": ang_helice,
        "G": G, "E": E, "Rm": Rm, "Rm_origem": origem,
        "k": k, "Kw": Kw1, "pontos": pontos, "solido": solido, "veredito_estatico": veredito,
        "L_min_trabalho": Lmin, "flambagem": flamb, "fadiga": fadiga,
        "De_no_solido": De + dDe, "comprimento_fio": comp_fio, "massa_g": massa * 1000,
        "frequencia_natural_Hz": freq, "avisos": avisos,
    }


# -------------------------------------------------------------------- tracao
def tracao(args):
    mat, d, De, D, C, G, E, Rm, origem, avisos = base(args)
    Nb = args.Nb
    Na = Nb + G / E  # os dois ganchos somam G/E espiras ativas
    k = G * d ** 4 / (8 * D ** 3 * Na)
    Kw = wahl(C)
    corpo = (Nb + 1) * d
    L0 = args.L0 if args.L0 else corpo + 2 * (D - d)  # ganchos inteiros sobre o centro
    Fi = args.Fi
    tau_i = 8 * Fi * D / (math.pi * d ** 3)
    # Faixa preferida de tensao inicial (Shigley): tau_i = 231/exp(0,105C) +- 6,9(4 - (C-3)/6,5) MPa
    centro = 231.0 / math.exp(0.105 * C)
    banda = 6.9 * (4 - (C - 3) / 6.5)
    faixa = (centro - banda, centro + banda)
    fator_G = G / 79300.0
    faixa = (faixa[0] * fator_G, faixa[1] * fator_G)
    if not (faixa[0] <= tau_i <= faixa[1]):
        avisos.append("tensao inicial %.0f MPa fora da faixa fabricavel (%.0f a %.0f MPa): "
                      "a maquina nao segura essa pre-carga com repetibilidade" % (tau_i, faixa[0], faixa[1]))
    adm = mat["admissivel"]["tracao"]
    r1 = D / 2  # raio medio do gancho
    Ka = (4 * (2 * r1 / d) ** 2 - (2 * r1 / d) - 1) / (4 * (2 * r1 / d) * ((2 * r1 / d) - 1))

    def ponto(L):
        F = Fi + k * (L - L0)
        tau = 8 * F * D / (math.pi * d ** 3) * Kw
        sig = F * (Ka * 16 * D / (math.pi * d ** 3) + 4 / (math.pi * d ** 2))
        p = {"L": L, "flecha": L - L0, "F": F, "tau_wahl": tau, "sigma_gancho": sig}
        if Rm:
            p["uso_corpo"] = tau / (adm["corpo"] * Rm)
            p["uso_gancho_flexao"] = sig / (adm["gancho_flexao"] * Rm)
        return p

    pontos = {}
    for nome, L in (("L1", args.L1), ("L2", args.L2)):
        if L is not None:
            if L < L0:
                avisos.append("%s menor que o comprimento livre: mola de tracao nao trabalha comprimida" % nome)
            pontos[nome] = ponto(L)
    veredito = None
    if Rm and pontos:
        pior = max(pontos.values(), key=lambda p: p["F"])
        if pior["uso_corpo"] <= 1 and pior["uso_gancho_flexao"] <= 1:
            veredito = "OK estatico (corpo %.0f%%, gancho %.0f%% do admissivel)" % (
                pior["uso_corpo"] * 100, pior["uso_gancho_flexao"] * 100)
        else:
            veredito = "SOBRETENSIONADA (corpo %.0f%%, gancho %.0f%% do admissivel)" % (
                pior["uso_corpo"] * 100, pior["uso_gancho_flexao"] * 100)
            avisos.append("gancho costuma quebrar antes do corpo: aumente o raio do gancho, "
                          "use gancho reduzido/olhal girante ou reduza a carga")
    comp_fio = math.pi * D * (Nb + 2)
    massa = comp_fio * math.pi * d ** 2 / 4 * mat["rho"] * 1e-9
    return {
        "tipo": "tracao", "material": mat["nome"], "condicao": mat.get("condicao", ""),
        "d": d, "De": De, "D": D, "Di": D - d, "C": C, "Nb": Nb, "Na": Na, "L0": L0, "comprimento_corpo": corpo,
        "G": G, "E": E, "Rm": Rm, "Rm_origem": origem, "k": k, "Kw": Kw,
        "Fi": Fi, "tau_inicial": tau_i, "faixa_tau_inicial": faixa,
        "pontos": pontos, "veredito_estatico": veredito,
        "comprimento_fio": comp_fio, "massa_g": massa * 1000, "avisos": avisos,
    }


# -------------------------------------------------------------------- torcao
def torcao_core(mat, d, De, D, C, E, Rm, Nb, perna1, perna2, avisos, sentido_fecha=True):
    Na = Nb + (perna1 + perna2) / (3 * math.pi * D)
    k_volta = E * d ** 4 / (10.8 * D * Na)      # N.mm por volta (SMI, inclui atrito)
    k_grau = k_volta / 360.0
    Ki = (4 * C ** 2 - C - 1) / (4 * C * (C - 1))  # fibra interna
    Ko = (4 * C ** 2 + C - 1) / (4 * C * (C + 1))
    adm = mat["admissivel"]["torcao"]
    return {"Na": Na, "k_volta": k_volta, "k_grau": k_grau, "Ki": Ki, "Ko": Ko, "adm": adm}


def torcao_ponto(core, d, D, Nb, ang, Rm):
    M = core["k_grau"] * ang
    sig = core["Ki"] * 32 * M / (math.pi * d ** 3)
    voltas = ang / 360.0
    D_fech = D * Nb / (Nb + voltas)
    p = {"angulo": ang, "M": M, "sigma": sig, "Di_fechado": D_fech - d,
         "comprimento_corpo": (Nb + 1 + voltas) * d}
    if Rm:
        p["uso_sem_alivio_favoravel"] = sig / (core["adm"]["aliviada"] * Rm)
        p["uso_com_tensao_residual_favoravel"] = sig / (core["adm"]["residual_favoravel"] * Rm)
    return p


def torcao(args):
    mat, d, De, D, C, G, E, Rm, origem, avisos = base(args)
    core = torcao_core(mat, d, De, D, C, E, Rm, args.Nb, args.perna1, args.perna2, avisos)
    pontos = {}
    for nome, ang in (("ang1", args.ang1), ("ang2", args.ang2)):
        if ang is not None:
            pontos[nome] = torcao_ponto(core, d, D, args.Nb, ang, Rm)
    for nome, p in pontos.items():
        if args.pino and p["Di_fechado"] < args.pino * 1.1:
            avisos.append("%s: diametro interno fechado %.2f mm deixa menos de 10%% de folga sobre o pino "
                          "de %.2f mm - a mola trava no eixo" % (nome, p["Di_fechado"], args.pino))
    veredito = None
    if Rm and pontos:
        pior = max(pontos.values(), key=lambda p: p["M"])
        if pior["uso_sem_alivio_favoravel"] <= 1:
            veredito = "OK estatico (%.0f%% do admissivel de mola aliviada)" % (pior["uso_sem_alivio_favoravel"] * 100)
        elif pior["uso_com_tensao_residual_favoravel"] <= 1:
            veredito = ("So passa se trabalhar FECHANDO as espiras e sem alivio que remova a tensao residual "
                        "favoravel (%.0f%% do limite superior)" % (pior["uso_com_tensao_residual_favoravel"] * 100))
        else:
            veredito = "SOBRETENSIONADA em flexao (%.0f%% do limite superior)" % (
                pior["uso_com_tensao_residual_favoravel"] * 100)
            avisos.append("tensao de flexao acima do admissivel: aumentar fio, espiras ou diametro")
    comp_fio = math.pi * D * args.Nb + args.perna1 + args.perna2
    massa = comp_fio * math.pi * d ** 2 / 4 * mat["rho"] * 1e-9
    return {
        "tipo": "torcao", "material": mat["nome"], "condicao": mat.get("condicao", ""),
        "d": d, "De": De, "D": D, "Di": D - d, "C": C, "Nb": args.Nb, "Na_equivalente": core["Na"],
        "perna1": args.perna1, "perna2": args.perna2, "E": E, "Rm": Rm, "Rm_origem": origem,
        "k_Nmm_por_grau": core["k_grau"], "k_Nmm_por_volta": core["k_volta"], "Ki": core["Ki"],
        "pontos": pontos, "veredito_estatico": veredito,
        "comprimento_corpo_livre": (args.Nb + 1) * d,
        "comprimento_fio": comp_fio, "massa_g": massa * 1000, "avisos": avisos,
    }


# ---------------------------------------------------------------- portinhola
def portinhola(args):
    """Mola de torcao de valvula de retencao dupla portinhola (API 594 tipo wafer).

    Cada portinhola e um meio-disco articulado no pino central. O momento da
    pressao diferencial dp sobre um meio-disco de raio R em relacao a aresta
    reta e M = dp * (pi R^2 / 2) * (4R / 3pi + e) ; com e=0 -> M = 2 dp R^3 / 3.
    """
    mat, d, De, D, C, G, E, Rm, origem, avisos = base(args)
    core = torcao_core(mat, d, De, D, C, E, Rm, args.Nb, args.perna1, args.perna2, avisos)
    n = args.molas_por_portinhola
    R, e = args.raio, args.excentricidade
    area = math.pi * R ** 2 / 2
    braco = 4 * R / (3 * math.pi) + e
    # "entre-portinholas": cada perna apoia numa portinhola -> a mola deflete 2x o curso
    # "independente": uma perna na portinhola, outra no batente/corpo -> deflete 1x o curso
    mult = 2.0 if args.montagem == "entre-portinholas" else 1.0
    fechada = torcao_ponto(core, d, D, args.Nb, args.pre_ang, Rm)
    aberta = torcao_ponto(core, d, D, args.Nb, args.pre_ang + mult * args.abertura, Rm)
    M_fech = fechada["M"] * n
    M_aber = aberta["M"] * n
    dp_abre = M_fech / (area * braco)        # MPa
    dp_total = M_aber / (area * braco)
    if args.pino and aberta["Di_fechado"] < args.pino * 1.1:
        avisos.append("valvula toda aberta: diametro interno da mola %.2f mm com menos de 10%% de folga "
                      "sobre o pino de %.2f mm" % (aberta["Di_fechado"], args.pino))
    veredito = None
    if Rm:
        uso = aberta["uso_sem_alivio_favoravel"]
        veredito = ("OK estatico na abertura total (%.0f%% do admissivel)" % (uso * 100) if uso <= 1 else
                    "ACIMA do admissivel na abertura total (%.0f%%): a mola relaxa e a valvula perde "
                    "o fechamento rapido" % (uso * 100))
    avisos.append("pressao de abertura calculada so com a mola: peso da portinhola, atrito do pino e "
                  "posicao de montagem (fluxo ascendente/horizontal) entram por fora")
    out = {
        "tipo": "portinhola", "material": mat["nome"], "condicao": mat.get("condicao", ""),
        "d": d, "De": De, "D": D, "C": C, "Nb": args.Nb, "E": E, "Rm": Rm, "Rm_origem": origem,
        "k_Nmm_por_grau": core["k_grau"], "molas_por_portinhola": n, "montagem": args.montagem,
        "deflexao_total_mola_graus": args.pre_ang + mult * args.abertura,
        "raio_portinhola": R, "area_portinhola_mm2": area, "braco_mm": braco,
        "fechada": fechada, "aberta": aberta,
        "torque_fechada_por_portinhola_Nmm": M_fech, "torque_aberta_por_portinhola_Nmm": M_aber,
        "dp_inicio_abertura_kPa": dp_abre * 1000, "dp_abertura_total_kPa": dp_total * 1000,
        "dp_inicio_abertura_mca": dp_abre * 1e6 / 9806.65,
        "veredito_estatico": veredito, "avisos": avisos,
    }
    if args.dp_alvo:
        M_alvo = args.dp_alvo / 1000.0 * area * braco / n
        out["pre_angulo_para_dp_alvo_graus"] = M_alvo / core["k_grau"]
    return out


# --------------------------------------------------------------- dimensionar
def dimensionar(args):
    """Varre bitolas e devolve molas de compressao que atendem k, Fmax e espaco."""
    mat = material(args.material)
    G, E, avisos = modulos(mat, args.temp)
    adm = mat["admissivel"]["compressao"]
    achados = []
    for d in BITOLAS:
        Rm, erro = (args.Rm, None) if args.Rm else rm_estimado(mat, d)
        if not Rm:
            continue
        De = args.De_max
        while De >= max(args.De_min or 0, 5 * d):
            D = De - d
            C = D / d
            if 4 <= C <= 12:
                Na = G * d ** 4 / (8 * D ** 3 * args.k)
                if 2.5 <= Na <= 40:
                    Na_r = round(Na * 4) / 4.0
                    k = G * d ** 4 / (8 * D ** 3 * Na_r)
                    Ls = (Na_r + 2) * d
                    tau = 8 * args.Fmax * D / (math.pi * d ** 3) * wahl(C)
                    L_Fmax = args.L0 - args.Fmax / k
                    Sa = (0.0015 * D ** 2 / d + 0.1 * d) * Na_r
                    if tau <= adm["sem_preset"] * Rm and L_Fmax >= Ls + Sa:
                        massa = math.pi * D * (Na_r + 2) * math.pi * d ** 2 / 4 * mat["rho"] * 1e-6
                        achados.append({"d": d, "De": round(De, 2), "C": round(C, 2), "Na": Na_r,
                                        "k": round(k, 3), "Ls": round(Ls, 2), "L_em_Fmax": round(L_Fmax, 2),
                                        "tau_wahl_Fmax": round(tau), "uso": round(tau / (adm["sem_preset"] * Rm), 2),
                                        "massa_g": round(massa, 1)})
            De -= max(0.5, 0.02 * args.De_max)
    achados.sort(key=lambda a: (a["massa_g"], -a["uso"]))
    vistos, saida = set(), []
    for a in achados:
        if a["d"] not in vistos:
            vistos.add(a["d"])
            saida.append(a)
    if not saida:
        avisos.append("nenhuma combinacao atende: afrouxe De-max, L0, k ou troque o material")
    return {"tipo": "dimensionar", "material": mat["nome"], "condicao": mat.get("condicao", ""),
            "k_alvo": args.k, "Fmax": args.Fmax, "L0": args.L0, "candidatas": saida[:8], "avisos": avisos}


# ---------------------------------------------------------------------- saida
def f(x, casas=2):
    return "-" if x is None else ("%." + str(casas) + "f") % x


def imprimir(r):
    t = r["tipo"]
    L = []
    if t == "dimensionar":
        L.append("DIMENSIONAMENTO - %s %s" % (r["material"], r["condicao"]))
        L.append("alvo: k=%.2f N/mm, Fmax=%.1f N, L0=%.1f mm" % (r["k_alvo"], r["Fmax"], r["L0"]))
        L.append("%6s %7s %6s %6s %8s %7s %9s %9s %5s %8s" % (
            "d", "De", "C", "Na", "k", "Ls", "L(Fmax)", "tau(MPa)", "uso", "massa g"))
        for a in r["candidatas"]:
            L.append("%6.2f %7.2f %6.2f %6.2f %8.3f %7.2f %9.2f %9d %5.2f %8.1f" % (
                a["d"], a["De"], a["C"], a["Na"], a["k"], a["Ls"], a["L_em_Fmax"],
                a["tau_wahl_Fmax"], a["uso"], a["massa_g"]))
    else:
        L.append("MOLA DE %s - %s %s" % (t.upper(), r["material"], r["condicao"]))
        L.append("fio d=%.2f  De=%.2f  D=%.2f  C=%.2f" % (r["d"], r["De"], r["D"], r["C"]))
        if r.get("Rm"):
            L.append("Rm=%.0f MPa (%s)" % (r["Rm"], r["Rm_origem"]))
        else:
            L.append("Rm nao disponivel: verificacao de tensao admissivel nao foi feita")
    if t == "compressao":
        L.append("Na=%.2f  Nt=%.2f  %s  L0=%.2f  Ls=%.2f  passo=%.2f  helice=%.1f graus" % (
            r["Na"], r["Nt"], r["extremidades"], r["L0"], r["Ls"], r["passo"], r["angulo_helice"]))
        L.append("G=%.0f MPa  constante k=%.3f N/mm  Wahl=%.3f" % (r["G"], r["k"], r["Kw"]))
        for nome, p in list(r["pontos"].items()) + [("solido", r["solido"])]:
            L.append("  %-6s L=%7.2f  flecha=%6.2f  F=%8.1f N  tau=%5.0f  tau_Wahl=%5.0f MPa" % (
                nome, p["L"], p["flecha"], p["F"], p["tau"], p["tau_wahl"]))
        L.append("comprimento minimo de trabalho recomendado: %.2f mm" % r["L_min_trabalho"])
        fl = r["flambagem"]
        L.append("flambagem: " + ("nao flamba nesse apoio" if not fl["flamba"] else
                                  "flecha critica %.1f mm (L=%.1f mm)" % (fl["flecha_critica"], fl["L_critico"])))
        if r["fadiga"]:
            fa = r["fadiga"]
            L.append("fadiga: tau_alt=%.0f  tau_med=%.0f MPa" % (fa["tau_alternada"], fa["tau_media"]))
            if "fs_vida_infinita_sem_shot_peening" in fa:
                L.append("  fator de seguranca vida infinita (Goodman-Zimmerli): sem jato %.2f | com shot peening %.2f" % (
                    fa["fs_vida_infinita_sem_shot_peening"], fa["fs_vida_infinita_com_shot_peening"]))
            else:
                L.append("  " + fa["nota"])
        L.append("De no solido=%.2f mm  fio=%.0f mm  massa=%.1f g  freq. natural=%.0f Hz" % (
            r["De_no_solido"], r["comprimento_fio"], r["massa_g"], r["frequencia_natural_Hz"]))
    elif t == "tracao":
        L.append("Nb=%.2f  Na=%.2f  L0=%.2f  corpo=%.2f  k=%.3f N/mm  Fi=%.1f N (tau_i=%.0f MPa, faixa %.0f-%.0f)" % (
            r["Nb"], r["Na"], r["L0"], r["comprimento_corpo"], r["k"], r["Fi"], r["tau_inicial"],
            r["faixa_tau_inicial"][0], r["faixa_tau_inicial"][1]))
        for nome, p in r["pontos"].items():
            L.append("  %-4s L=%7.2f  F=%8.1f N  tau_Wahl=%5.0f  sigma_gancho=%5.0f MPa" % (
                nome, p["L"], p["F"], p["tau_wahl"], p["sigma_gancho"]))
        L.append("fio=%.0f mm  massa=%.1f g" % (r["comprimento_fio"], r["massa_g"]))
    elif t == "torcao":
        L.append("Nb=%.2f  Na equiv.=%.2f  pernas %.1f/%.1f mm  E=%.0f MPa" % (
            r["Nb"], r["Na_equivalente"], r["perna1"], r["perna2"], r["E"]))
        L.append("constante: %.2f N.mm/grau  (%.0f N.mm/volta)  Ki=%.3f" % (
            r["k_Nmm_por_grau"], r["k_Nmm_por_volta"], r["Ki"]))
        for nome, p in r["pontos"].items():
            L.append("  %-4s %6.1f graus  M=%8.1f N.mm  sigma=%5.0f MPa  Di fechado=%.2f  corpo=%.2f mm" % (
                nome, p["angulo"], p["M"], p["sigma"], p["Di_fechado"], p["comprimento_corpo"]))
        L.append("fio=%.0f mm  massa=%.1f g" % (r["comprimento_fio"], r["massa_g"]))
    elif t == "portinhola":
        L.append("Nb=%.2f  constante %.2f N.mm/grau  molas por portinhola: %d  montagem: %s (mola deflete ate %.0f graus)" % (
            r["Nb"], r["k_Nmm_por_grau"], r["molas_por_portinhola"], r["montagem"], r["deflexao_total_mola_graus"]))
        L.append("portinhola: raio %.1f mm  area %.0f mm2  braco %.1f mm" % (
            r["raio_portinhola"], r["area_portinhola_mm2"], r["braco_mm"]))
        for nome in ("fechada", "aberta"):
            p = r[nome]
            L.append("  %-8s %6.1f graus  M=%8.1f N.mm/mola  sigma=%5.0f MPa  Di=%.2f mm" % (
                nome, p["angulo"], p["M"], p["sigma"], p["Di_fechado"]))
        L.append("dp inicio de abertura: %.2f kPa (%.3f mca)   dp abertura total: %.2f kPa" % (
            r["dp_inicio_abertura_kPa"], r["dp_inicio_abertura_mca"], r["dp_abertura_total_kPa"]))
        if "pre_angulo_para_dp_alvo_graus" in r:
            L.append("pre-angulo para o dp alvo: %.1f graus" % r["pre_angulo_para_dp_alvo_graus"])
    if r.get("veredito_estatico"):
        L.append("VEREDITO: " + r["veredito_estatico"])
    for a in r["avisos"]:
        L.append("AVISO: " + a)
    print("\n".join(L))


def listar():
    banco = carregar()
    print("%-16s %-44s %7s %7s %6s  %s" % ("chave", "material", "G MPa", "E MPa", "Tmax C", "confianca"))
    for chave, m in banco["materiais"].items():
        print("%-16s %-44s %7d %7d %6s  %s" % (
            chave, (m["nome"] + " " + m.get("condicao", ""))[:44], m["G"], m["E"],
            m.get("temp_max", "-"), m.get("confianca", "")))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def comuns(s, geometria=True):
        s.add_argument("--material", required=True)
        s.add_argument("--temp", type=float, help="temperatura de servico, C")
        s.add_argument("--Rm", type=float, help="limite de resistencia do certificado do arame, MPa")
        s.add_argument("--json", action="store_true")
        if geometria:
            s.add_argument("--d", type=float, required=True, help="diametro do fio, mm")
            s.add_argument("--De", type=float, required=True, help="diametro externo, mm")

    sub.add_parser("materiais")

    s = sub.add_parser("compressao"); comuns(s)
    s.add_argument("--Na", type=float, required=True, help="espiras ativas")
    s.add_argument("--L0", type=float, required=True, help="comprimento livre, mm")
    s.add_argument("--L1", type=float); s.add_argument("--L2", type=float)
    s.add_argument("--extremidades", choices=list(EXTREMIDADES), default="fechada-retificada")
    s.add_argument("--apoio", type=float, default=0.5,
                   help="coeficiente de flambagem: 0.5 pratos paralelos guiados (padrao), 0.7 um apoio articulado, "
                        "1 dois articulados, 2 um lado livre")

    s = sub.add_parser("tracao"); comuns(s)
    s.add_argument("--Nb", type=float, required=True, help="espiras do corpo")
    s.add_argument("--Fi", type=float, required=True, help="tensao inicial (pre-carga), N")
    s.add_argument("--L0", type=float, help="comprimento livre entre faces internas dos ganchos, mm")
    s.add_argument("--L1", type=float); s.add_argument("--L2", type=float)

    def torc(s):
        s.add_argument("--Nb", type=float, required=True, help="espiras do corpo")
        s.add_argument("--perna1", type=float, default=0.0); s.add_argument("--perna2", type=float, default=0.0)
        s.add_argument("--pino", type=float, help="diametro do pino/eixo, mm")

    s = sub.add_parser("torcao"); comuns(s); torc(s)
    s.add_argument("--ang1", type=float, help="deflexao angular na montagem, graus")
    s.add_argument("--ang2", type=float, help="deflexao angular maxima, graus")

    s = sub.add_parser("portinhola"); comuns(s); torc(s)
    s.add_argument("--raio", type=float, required=True, help="raio da portinhola (meio-disco), mm")
    s.add_argument("--excentricidade", type=float, default=0.0, help="distancia da aresta reta ao centro do pino, mm")
    s.add_argument("--pre-ang", dest="pre_ang", type=float, required=True, help="pre-deflexao com valvula fechada, graus")
    s.add_argument("--abertura", type=float, default=85.0, help="curso da portinhola ate abertura total, graus")
    s.add_argument("--molas-por-portinhola", dest="molas_por_portinhola", type=int, default=1)
    s.add_argument("--montagem", choices=["independente", "entre-portinholas"], default="independente",
                   help="independente: uma perna na portinhola e outra no batente (mola deflete 1x o curso); "
                        "entre-portinholas: cada perna numa portinhola (mola deflete 2x o curso)")
    s.add_argument("--dp-alvo", dest="dp_alvo", type=float, help="pressao de inicio de abertura desejada, kPa")

    s = sub.add_parser("dimensionar"); comuns(s, geometria=False)
    s.add_argument("--k", type=float, required=True, help="constante desejada, N/mm")
    s.add_argument("--Fmax", type=float, required=True, help="carga maxima de trabalho, N")
    s.add_argument("--L0", type=float, required=True)
    s.add_argument("--De-max", dest="De_max", type=float, required=True)
    s.add_argument("--De-min", dest="De_min", type=float)

    args = p.parse_args()
    if args.cmd == "materiais":
        return listar()
    r = {"compressao": compressao, "tracao": tracao, "torcao": torcao,
         "portinhola": portinhola, "dimensionar": dimensionar}[args.cmd](args)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        imprimir(r)


if __name__ == "__main__":
    main()
