#!/usr/bin/env python3
"""Calculadora de mola da Jardmolas: rigidez, tensão, peso, custo e preço.

Sem dependências. Unidades: mm, N, N.mm, kg, R$.

Exemplos:
  python3 calc_mola.py compressao --d 6 --De 50 --nt 10 --L0 120 --Lt 90 --Rm 1600
  python3 calc_mola.py tracao --d 3 --De 25 --nb 20 --x 30 --Fi 20 --Rm 1800
  python3 calc_mola.py torcao --d 8 --De 40 --nb 4 --angulo 45 --braco1 180 --braco2 60 --Rm 1500

Custo e preço (qualquer tipo):
  ... --arame-kg 12.50 --perda 5 --pecas-hora 120 --custo-hora 150 \\
      --setup-min 60 --lote 500 --tratamento-kg 2.0 --acabamento 0.30 \\
      --embalagem 0.10 --impostos 8 --comissao 5 --frete 3 --margem 25

Os limites de tensão impressos são referências de projeto para triagem, não
substituem o ensaio. Rm vem do certificado do lote de arame.
"""
import argparse
import math
import sys

RHO = 7.85e-6  # kg/mm3, aço
G_PADRAO = 79300.0  # N/mm2, módulo de cisalhamento do aço-mola
E_PADRAO = 206000.0  # N/mm2, módulo de elasticidade


def wahl(c):
    return (4 * c - 1) / (4 * c - 4) + 0.615 / c


def ki_torcao(c):
    return (4 * c * c - c - 1) / (4 * c * (c - 1))


def massa_kg(d, comprimento_mm):
    return RHO * math.pi * d * d / 4 * comprimento_mm


def fmt(x, casas=2):
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def avisos_geometria(c, extras):
    av = []
    if c < 4:
        av.append(f"Índice de mola C = {fmt(c,1)} (< 4): difícil de enrolar, tensão alta na face interna.")
    if c > 16:
        av.append(f"Índice de mola C = {fmt(c,1)} (> 16): mola instável, tende a embolar na caixa.")
    return av + extras


def checar_tensao(nome, tensao, rm, frac_ref, rotulo_ref):
    if not rm:
        return f"  {nome}: {fmt(tensao,0)} N/mm²   (informe --Rm do certificado para comparar)"
    uso = tensao / rm * 100
    ref = frac_ref * 100
    status = "OK" if uso <= ref else "ACIMA DA REFERÊNCIA"
    return (f"  {nome}: {fmt(tensao,0)} N/mm² = {fmt(uso,0)}% de Rm "
            f"(referência {rotulo_ref}: até {fmt(ref,0)}%)  -> {status}")


def compressao(a):
    d, De = a.d, a.De
    Dm = De - d
    c = Dm / d
    na = a.na if a.na else a.nt - 2
    if na <= 0:
        sys.exit("Espiras ativas <= 0. Confira --nt ou --na.")
    G = a.G or G_PADRAO
    k = G * d ** 4 / (8 * Dm ** 3 * na)
    ls = a.nt * d
    out = ["MOLA DE COMPRESSÃO", "=" * 72,
           f"  Arame d = {fmt(d)} mm | Ø ext = {fmt(De)} mm | Ø médio = {fmt(Dm)} mm | C = {fmt(c,2)}",
           f"  Espiras totais = {fmt(a.nt,1)} | ativas = {fmt(na,1)} | G = {fmt(G,0)} N/mm²",
           f"  Rigidez k = {fmt(k,3)} N/mm",
           f"  Comprimento sólido aprox. = {fmt(ls,1)} mm (pontas fechadas e esmerilhadas)"]
    kw = wahl(c)
    if a.L0:
        out.append(f"  Comprimento livre L0 = {fmt(a.L0,1)} mm")
        if a.Lt:
            f_t = k * (a.L0 - a.Lt)
            tau = kw * 8 * f_t * Dm / (math.pi * d ** 3)
            out.append(f"  Carga em Lt = {fmt(a.Lt,1)} mm: {fmt(f_t,1)} N ({fmt(f_t/9.80665,1)} kgf)")
            out.append(checar_tensao("Tensão de cisalhamento em Lt", tau, a.Rm, 0.45, "estática"))
        f_s = k * (a.L0 - ls)
        tau_s = kw * 8 * f_s * Dm / (math.pi * d ** 3)
        out.append(f"  Carga no sólido: {fmt(f_s,1)} N")
        out.append(checar_tensao("Tensão no sólido", tau_s, a.Rm, 0.50, "no sólido"))
        esbeltez = a.L0 / Dm
        extra = []
        if esbeltez > 4:
            extra.append(f"L0/Dm = {fmt(esbeltez,1)} (> 4): risco de flambagem; prever guia (pino ou tubo).")
    else:
        extra = []
    comp = math.pi * Dm * a.nt + (a.extra_mm or 0)
    out.append(f"  Comprimento de arame aprox. = {fmt(comp,0)} mm")
    for av in avisos_geometria(c, extra):
        out.append("  ! " + av)
    out.append("  Fadiga (dedos, válvulas): use bem menos que a referência estática; jateamento e")
    out.append("  pré-setagem mudam a vida. Valide em teste.")
    return out, massa_kg(d, comp)


def tracao(a):
    d, De = a.d, a.De
    Dm = De - d
    c = Dm / d
    G = a.G or G_PADRAO
    k = G * d ** 4 / (8 * Dm ** 3 * a.nb)
    kw = wahl(c)
    fi = a.Fi or 0.0
    out = ["MOLA DE TRAÇÃO", "=" * 72,
           f"  Arame d = {fmt(d)} mm | Ø ext = {fmt(De)} mm | Ø médio = {fmt(Dm)} mm | C = {fmt(c,2)}",
           f"  Espiras do corpo = {fmt(a.nb,1)} | G = {fmt(G,0)} N/mm²",
           f"  Rigidez k = {fmt(k,3)} N/mm | tensão inicial Fi = {fmt(fi,1)} N"]
    if a.x is not None:
        f = fi + k * a.x
        tau = kw * 8 * f * Dm / (math.pi * d ** 3)
        out.append(f"  Carga com {fmt(a.x,1)} mm de abertura: {fmt(f,1)} N ({fmt(f/9.80665,1)} kgf)")
        out.append(checar_tensao("Tensão no corpo", tau, a.Rm, 0.40, "estática"))
    comp = math.pi * Dm * a.nb + (a.extra_mm if a.extra_mm is not None else 2 * math.pi * Dm)
    out.append(f"  Comprimento de arame aprox. = {fmt(comp,0)} mm (corpo + 2 ganchos)")
    for av in avisos_geometria(c, ["Em mola de tração quem quebra primeiro costuma ser o gancho: raio de dobra generoso."]):
        out.append("  ! " + av)
    return out, massa_kg(d, comp)


def torcao(a):
    d, De = a.d, a.De
    Dm = De - d
    c = Dm / d
    E = a.E or E_PADRAO
    b1, b2 = a.braco1 or 0.0, a.braco2 or 0.0
    ne = a.nb + (b1 + b2) / (3 * math.pi * Dm)
    k_rad = E * d ** 4 / (64 * Dm * ne)
    k_grau = k_rad * math.pi / 180
    out = ["MOLA DE TORÇÃO / DEDO", "=" * 72,
           f"  Arame d = {fmt(d)} mm | Ø ext = {fmt(De)} mm | Ø médio = {fmt(Dm)} mm | C = {fmt(c,2)}",
           f"  Espiras do corpo = {fmt(a.nb,2)} | braços {fmt(b1,0)} e {fmt(b2,0)} mm | espiras equivalentes = {fmt(ne,2)}",
           f"  Rigidez = {fmt(k_grau,1)} N.mm por grau ({fmt(k_rad,0)} N.mm/rad)"]
    if a.angulo is not None:
        m = k_grau * a.angulo
        sigma = ki_torcao(c) * 32 * m / (math.pi * d ** 3)
        out.append(f"  Momento em {fmt(a.angulo,1)}°: {fmt(m,0)} N.mm")
        if b1:
            out.append(f"  Força na ponta do braço de {fmt(b1,0)} mm: {fmt(m/b1,1)} N ({fmt(m/b1/9.80665,2)} kgf)")
        out.append(checar_tensao("Tensão de flexão", sigma, a.Rm, 0.70, "estática"))
        voltas = a.angulo / 360
        di_carga = Dm * a.nb / (a.nb + voltas) - d
        out.append(f"  Ø interno sob carga (fechando) aprox. = {fmt(di_carga,1)} mm: confira o pino.")
    comp = math.pi * Dm * a.nb + b1 + b2 + (a.extra_mm or 0)
    out.append(f"  Comprimento de arame aprox. = {fmt(comp,0)} mm")
    for av in avisos_geometria(c, []):
        out.append("  ! " + av)
    out.append("  Dedo de enleirador = torção em fadiga com impacto: o ponto crítico é o raio de dobra")
    out.append("  no olhal e na saída da espira. Valide com teste de campo (hectares).")
    return out, massa_kg(d, comp)


def custo_preco(a, massa):
    linhas = ["", "PESO, CUSTO E PREÇO", "=" * 72,
              f"  Peso por peça aprox. = {fmt(massa*1000,1)} g ({fmt(1/massa,0) if massa else '-'} peças por kg)"]
    if a.arame_kg is None:
        linhas.append("  (informe --arame-kg e os demais custos para calcular custo e preço)")
        return linhas
    perda = (a.perda or 0) / 100
    material = massa * a.arame_kg * (1 + perda)
    conv = (a.custo_hora / a.pecas_hora) if (a.custo_hora and a.pecas_hora) else 0.0
    trat = massa * (a.tratamento_kg or 0)
    acab = a.acabamento or 0
    emb = a.embalagem or 0
    soma_pct = sum(x or 0 for x in (a.impostos, a.comissao, a.frete, a.margem))
    if soma_pct >= 100:
        sys.exit("Impostos + comissão + frete + margem >= 100%. Revise os percentuais.")
    div = 1 - soma_pct / 100

    def unit(lote):
        setup = ((a.setup_min or 0) / 60 * (a.custo_hora or 0)) / lote if lote else 0
        return material + conv + trat + acab + emb + setup, setup

    linhas += [f"  Material: {fmt(material,4)} | Conversão: {fmt(conv,4)} | Tratamento: {fmt(trat,4)} | "
               f"Acabamento: {fmt(acab,4)} | Embalagem: {fmt(emb,4)}  (R$/peça)",
               f"  Impostos {fmt(a.impostos or 0,1)}% + comissão {fmt(a.comissao or 0,1)}% + "
               f"frete {fmt(a.frete or 0,1)}% + margem {fmt(a.margem or 0,1)}% = {fmt(soma_pct,1)}% do preço",
               "",
               f"  {'Lote':>8} {'Setup/peça':>12} {'Custo/peça':>12} {'Preço/peça':>12} {'Preço do lote':>15}",
               "  " + "-" * 62]
    lotes = sorted({x for x in (50, 100, 500, 1000, a.lote) if x})
    for lote in lotes:
        c, s = unit(lote)
        p = c / div
        marca = "  <- lote informado" if lote == a.lote else ""
        linhas.append(f"  {lote:>8} {fmt(s,4):>12} {fmt(c,4):>12} {fmt(p,2):>12} {fmt(p*lote,2):>15}{marca}")
    linhas += ["",
               "  Preço = custo ÷ (1 − impostos − comissão − frete − margem). Margem aqui é a margem de",
               "  contribuição alvo. Confira a alíquota real do Simples/regime com o contador [confirmar]."]
    return linhas


def main():
    p = argparse.ArgumentParser(description="Calculadora de mola Jardmolas")
    sub = p.add_subparsers(dest="tipo", required=True)

    def comuns(sp):
        sp.add_argument("--d", type=float, required=True, help="diâmetro do arame (mm)")
        sp.add_argument("--De", type=float, required=True, help="diâmetro externo (mm)")
        sp.add_argument("--Rm", type=float, help="resistência à tração do arame (N/mm²), do certificado")
        sp.add_argument("--extra-mm", type=float, help="arame extra (hastes, olhais) em mm")
        sp.add_argument("--arame-kg", type=float, help="preço do arame (R$/kg)")
        sp.add_argument("--perda", type=float, help="perda de material (%%)")
        sp.add_argument("--pecas-hora", type=float, help="produtividade (peças/hora)")
        sp.add_argument("--custo-hora", type=float, help="custo da hora máquina + operador (R$/h)")
        sp.add_argument("--setup-min", type=float, help="tempo de setup (min)")
        sp.add_argument("--lote", type=int, help="tamanho do lote")
        sp.add_argument("--tratamento-kg", type=float, help="tratamento térmico/jato (R$/kg)")
        sp.add_argument("--acabamento", type=float, help="pintura/óleo (R$/peça)")
        sp.add_argument("--embalagem", type=float, help="embalagem (R$/peça)")
        sp.add_argument("--impostos", type=float, help="impostos sobre venda (%%)")
        sp.add_argument("--comissao", type=float, help="comissão (%%)")
        sp.add_argument("--frete", type=float, help="frete (%%)")
        sp.add_argument("--margem", type=float, help="margem de contribuição alvo (%%)")

    c = sub.add_parser("compressao")
    comuns(c)
    c.add_argument("--nt", type=float, required=True, help="espiras totais")
    c.add_argument("--na", type=float, help="espiras ativas (padrão: totais - 2)")
    c.add_argument("--L0", type=float, help="comprimento livre (mm)")
    c.add_argument("--Lt", type=float, help="comprimento de trabalho (mm)")
    c.add_argument("--G", type=float, help="módulo de cisalhamento (N/mm²)")

    t = sub.add_parser("tracao")
    comuns(t)
    t.add_argument("--nb", type=float, required=True, help="espiras do corpo")
    t.add_argument("--x", type=float, help="abertura de trabalho (mm)")
    t.add_argument("--Fi", type=float, help="tensão inicial (N)")
    t.add_argument("--G", type=float, help="módulo de cisalhamento (N/mm²)")

    o = sub.add_parser("torcao")
    comuns(o)
    o.add_argument("--nb", type=float, required=True, help="espiras do corpo")
    o.add_argument("--angulo", type=float, help="ângulo de trabalho (graus)")
    o.add_argument("--braco1", type=float, help="comprimento do braço 1 / haste (mm)")
    o.add_argument("--braco2", type=float, help="comprimento do braço 2 (mm)")
    o.add_argument("--E", type=float, help="módulo de elasticidade (N/mm²)")

    a = p.parse_args()
    if a.De <= a.d:
        sys.exit("O diâmetro externo precisa ser maior que o do arame.")
    linhas, massa = {"compressao": compressao, "tracao": tracao, "torcao": torcao}[a.tipo](a)
    linhas += custo_preco(a, massa)
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
