#!/usr/bin/env python3
"""Catalogo de molas da Jardmolas: valida, busca e gera o catalogo navegavel.

A fonte do catalogo sao duas planilhas CSV (separador ; ou , - decimal com
virgula ou ponto):
  itens.csv       um registro por peca ou familia
  aplicacoes.csv  em que maquina/equipamento cada peca serve (N linhas por peca)

Uso:
  python catalogo.py novo PASTA                     cria as duas planilhas vazias
  python catalogo.py validar PASTA                  confere campos, medidas e vinculos
  python catalogo.py buscar PASTA --texto "pro ted 540"
  python catalogo.py buscar PASTA --marca Kuhn --modelo "GA 300"
  python catalogo.py buscar PASTA --tipo torcao --d 4 --De 34 --tol 10
  python catalogo.py buscar PASTA --original 84056883
  python catalogo.py ficha PASTA JM-0001
  python catalogo.py gerar PASTA --saida catalogo.html --empresa "Jardmolas" \
        --whatsapp 5516999999999 [--titulo "Catalogo de molas"] [--fotos URL_BASE]
  python catalogo.py app PASTA --saida app.html --whatsapp 5516999999999
        (catalogo + calculadora de molas + consultor de Inconel X-750 + pedido de cotacao)
Nenhum dado e inventado: campo vazio fica vazio e aparece como "sob consulta".
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import unicodedata

CAMPOS_ITENS = [
    "codigo", "nivel", "familia", "tipo", "descricao", "setor", "material", "norma_material",
    "acabamento", "d_fio_mm", "de_mm", "di_mm", "l0_mm", "comprimento_total_mm", "espiras",
    "sentido", "extremidades", "perna1_mm", "perna2_mm", "angulo_livre_graus", "constante",
    "unidade_constante", "carga1_N", "em1_mm", "carga2_N", "em2_mm", "massa_g", "embalagem_un",
    "foto", "situacao", "giro", "observacoes",
]
CAMPOS_APLIC = ["codigo", "equipamento", "marca", "modelo", "posicao", "codigo_original",
                "qtd_por_maquina", "observacao"]
NUMERICOS = ["d_fio_mm", "de_mm", "di_mm", "l0_mm", "comprimento_total_mm", "espiras", "perna1_mm",
             "perna2_mm", "angulo_livre_graus", "constante", "carga1_N", "em1_mm", "carga2_N",
             "em2_mm", "massa_g", "embalagem_un"]
TIPOS = {
    "compressao": "Mola de compressão", "tracao": "Mola de tração", "torcao": "Mola de torção",
    "torcao-dupla": "Mola de torção dupla", "dedo": "Dedo (enleirador, molinete, recolhedor)",
    "garfo": "Garfo / dente de mola", "haste": "Haste flexível", "conica": "Mola cônica",
    "prato": "Mola prato", "arame-conformado": "Arame conformado", "outros": "Outros",
}
SETORES = {
    "agricola": "Implementos agrícolas", "sucroenergetico": "Sucroenergético e usinas",
    "industrial": "Indústria e válvulas", "mineracao": "Mineração", "transporte": "Transporte",
    "moto": "Motocicletas", "pneus": "Pneus e borracharia", "outros": "Outros",
}
NIVEIS = {"item", "familia"}
SITUACOES = {"linha", "sob-encomenda", "descontinuado", ""}
ROTULOS = [
    ("material", "Material"), ("norma_material", "Norma do material"), ("acabamento", "Acabamento"),
    ("d_fio_mm", "Fio (mm)"), ("de_mm", "Diâmetro externo (mm)"), ("di_mm", "Diâmetro interno (mm)"),
    ("l0_mm", "Comprimento livre / corpo (mm)"), ("comprimento_total_mm", "Comprimento total (mm)"),
    ("espiras", "Espiras"), ("sentido", "Sentido de enrolamento"), ("extremidades", "Extremidades"),
    ("perna1_mm", "Perna 1 (mm)"), ("perna2_mm", "Perna 2 (mm)"),
    ("angulo_livre_graus", "Ângulo livre entre pernas (°)"), ("constante", "Constante"),
    ("carga1_N", "Carga 1 (N)"), ("em1_mm", "na altura/ângulo 1"), ("carga2_N", "Carga 2 (N)"),
    ("em2_mm", "na altura/ângulo 2"), ("massa_g", "Massa (g)"), ("embalagem_un", "Embalagem (un.)"),
]


def norm(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def num(v):
    v = str(v or "").strip().replace(" ", "")
    if not v:
        return None
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".")
    else:
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return "erro"


def ler_csv(caminho, campos):
    if not os.path.exists(caminho):
        sys.exit("Nao encontrei %s. Rode: python catalogo.py novo PASTA" % caminho)
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        amostra = f.read(4096)
        f.seek(0)
        sep = ";" if amostra.count(";") >= amostra.count(",") else ","
        linhas = list(csv.DictReader(f, delimiter=sep))
    faltam = [c for c in campos if linhas and c not in linhas[0]]
    if faltam:
        sys.exit("%s: faltam as colunas %s" % (caminho, ", ".join(faltam)))
    return [{k: (v or "").strip() for k, v in l.items() if k} for l in linhas
            if any((v or "").strip() for v in l.values())]


def carregar(pasta):
    itens = ler_csv(os.path.join(pasta, "itens.csv"), CAMPOS_ITENS)
    aplic = ler_csv(os.path.join(pasta, "aplicacoes.csv"), CAMPOS_APLIC)
    return itens, aplic


def cmd_novo(a):
    os.makedirs(a.pasta, exist_ok=True)
    for nome, campos in (("itens.csv", CAMPOS_ITENS), ("aplicacoes.csv", CAMPOS_APLIC)):
        caminho = os.path.join(a.pasta, nome)
        if os.path.exists(caminho):
            print("ja existe, nao sobrescrevi: " + caminho)
            continue
        with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, delimiter=";").writerow(campos)
        print("criado: " + caminho)


def validar(itens, aplic):
    erros, avisos = [], []
    vistos = {}
    for i, it in enumerate(itens, start=2):
        c = it["codigo"]
        onde = "itens.csv linha %d (%s)" % (i, c or "sem codigo")
        if not c:
            erros.append(onde + ": codigo vazio")
            continue
        if c in vistos:
            erros.append(onde + ": codigo repetido (tambem na linha %d)" % vistos[c])
        vistos[c] = i
        if it["nivel"] not in NIVEIS:
            erros.append(onde + ": nivel deve ser 'item' ou 'familia'")
        if it["tipo"] not in TIPOS:
            erros.append(onde + ": tipo '%s' invalido; use %s" % (it["tipo"], ", ".join(TIPOS)))
        if it["setor"] not in SETORES:
            erros.append(onde + ": setor '%s' invalido; use %s" % (it["setor"], ", ".join(SETORES)))
        if it["situacao"] not in SITUACOES:
            erros.append(onde + ": situacao deve ser linha, sob-encomenda ou descontinuado")
        if not it["descricao"]:
            erros.append(onde + ": descricao vazia")
        if it["sentido"] and it["sentido"].upper() not in ("D", "E"):
            erros.append(onde + ": sentido deve ser D (direita) ou E (esquerda)")
        v = {}
        for k in NUMERICOS:
            v[k] = num(it[k])
            if v[k] == "erro":
                erros.append(onde + ": %s nao e numero ('%s')" % (k, it[k]))
                v[k] = None
            elif v[k] is not None and v[k] <= 0 and k != "angulo_livre_graus":
                erros.append(onde + ": %s deve ser maior que zero" % k)
        d, de, di = v["d_fio_mm"], v["de_mm"], v["di_mm"]
        if d and de and de <= 2 * d:
            erros.append(onde + ": diametro externo %.2f nao comporta fio %.2f" % (de, d))
        if d and de and di and abs((de - 2 * d) - di) > max(0.3, 0.02 * de):
            erros.append(onde + ": di (%.2f) nao bate com de - 2 x fio (%.2f)" % (di, de - 2 * d))
        if d and de:
            ind = (de - d) / d
            if ind < 3 or ind > 20:
                avisos.append(onde + ": indice de mola %.1f fora do usual (4 a 12) - conferir as medidas" % ind)
        if v["constante"] and not it["unidade_constante"]:
            erros.append(onde + ": constante sem unidade (N/mm ou N.mm/grau)")
        for a_, b_ in (("carga1_N", "em1_mm"), ("carga2_N", "em2_mm")):
            if v[a_] and not v[b_]:
                erros.append(onde + ": %s informada sem %s" % (a_, b_))
        if it["nivel"] == "item":
            if not d:
                avisos.append(onde + ": sem diametro do fio - nao aparece na busca por medidas")
            if not (de or di):
                avisos.append(onde + ": sem diametro da mola - nao aparece na busca por medidas")
            if not it["material"]:
                avisos.append(onde + ": sem material")
            if not it["foto"]:
                avisos.append(onde + ": sem foto")
    usados = set()
    for i, ap in enumerate(aplic, start=2):
        onde = "aplicacoes.csv linha %d" % i
        if ap["codigo"] not in vistos:
            erros.append(onde + ": codigo '%s' nao existe em itens.csv" % ap["codigo"])
        usados.add(ap["codigo"])
        if not ap["equipamento"]:
            erros.append(onde + ": equipamento vazio")
        if ap["modelo"] and not ap["marca"]:
            erros.append(onde + ": modelo '%s' sem marca" % ap["modelo"])
        q = num(ap["qtd_por_maquina"])
        if q == "erro":
            erros.append(onde + ": qtd_por_maquina nao e numero")
    chaves = {}
    for i, ap in enumerate(aplic, start=2):
        k = (ap["codigo"], norm(ap["marca"]), norm(ap["modelo"]), norm(ap["posicao"]))
        if k in chaves:
            avisos.append("aplicacoes.csv linha %d: aplicacao repetida (linha %d)" % (i, chaves[k]))
        chaves[k] = i
    for it in itens:
        if it["codigo"] and it["codigo"] not in usados and it["setor"] == "agricola":
            avisos.append("itens.csv (%s): peca agricola sem nenhuma aplicacao cadastrada" % it["codigo"])
    return erros, avisos


def cmd_validar(a):
    itens, aplic = carregar(a.pasta)
    erros, avisos = validar(itens, aplic)
    n_item = sum(1 for i in itens if i["nivel"] == "item")
    com_med = sum(1 for i in itens if i["nivel"] == "item" and num(i["d_fio_mm"]) and (num(i["de_mm"]) or num(i["di_mm"])))
    print("%d registros (%d itens, %d familias) | %d aplicacoes | itens com medidas: %d de %d" % (
        len(itens), n_item, len(itens) - n_item, len(aplic), com_med, n_item))
    for e in erros:
        print("ERRO  " + e)
    for w in avisos[: a.max_avisos]:
        print("AVISO " + w)
    if len(avisos) > a.max_avisos:
        print("... e mais %d avisos (use --max-avisos)" % (len(avisos) - a.max_avisos))
    print("RESULTADO: %s" % ("%d erro(s) - corrigir antes de gerar o catalogo" % len(erros) if erros
                             else "sem erros (%d aviso(s))" % len(avisos)))
    return 1 if erros else 0


def indice(itens, aplic):
    por = {}
    for ap in aplic:
        por.setdefault(ap["codigo"], []).append(ap)
    return por


def diam_externo(it):
    de, di, d = num(it["de_mm"]), num(it["di_mm"]), num(it["d_fio_mm"])
    if isinstance(de, float):
        return de
    if isinstance(di, float) and isinstance(d, float):
        return di + 2 * d
    return None


def comprimento(it):
    for k in ("l0_mm", "comprimento_total_mm"):
        v = num(it[k])
        if isinstance(v, float):
            return v
    return None


def buscar(itens, aplic, a):
    por = indice(itens, aplic)
    res = []
    for it in itens:
        aps = por.get(it["codigo"], [])
        pontos, motivos = 0.0, []
        if a.tipo and it["tipo"] != a.tipo:
            continue
        if a.setor and it["setor"] != a.setor:
            continue
        if a.marca or a.modelo or a.equipamento:
            ok = [ap for ap in aps
                  if (not a.marca or norm(a.marca) in norm(ap["marca"]))
                  and (not a.modelo or norm(a.modelo).replace(" ", "") in norm(ap["modelo"]).replace(" ", ""))
                  and (not a.equipamento or norm(a.equipamento) in norm(ap["equipamento"]))]
            if not ok:
                continue
            pontos += 5
            motivos.append("serve em: " + "; ".join(
                " ".join(x for x in (ap["equipamento"], ap["marca"], ap["modelo"]) if x) for ap in ok[:4]))
        if a.original:
            alvo = norm(a.original).replace(" ", "")
            ok = [ap for ap in aps if alvo and alvo in norm(ap["codigo_original"]).replace(" ", "")]
            if not ok and alvo not in norm(it["codigo"]).replace(" ", ""):
                continue
            pontos += 8
            motivos.append("codigo de referencia: " + (ok[0]["codigo_original"] if ok else it["codigo"]))
        if a.texto:
            palheiro = norm(" ".join([it[k] for k in ("codigo", "familia", "descricao", "material", "observacoes")]
                                     + [TIPOS.get(it["tipo"], ""), SETORES.get(it["setor"], "")]
                                     + [" ".join(ap.values()) for ap in aps]))
            junto = palheiro.replace(" ", "")
            termos = norm(a.texto).split()
            if not all(t in palheiro or t in junto for t in termos):
                continue
            pontos += 3
        medidas = []
        for rot, alvo, valor in (("fio", a.d, num(it["d_fio_mm"])), ("De", a.De, diam_externo(it)),
                                 ("Di", a.Di, num(it["di_mm"]) if isinstance(num(it["di_mm"]), float) else (
                                     diam_externo(it) - 2 * num(it["d_fio_mm"])
                                     if diam_externo(it) and isinstance(num(it["d_fio_mm"]), float) else None)),
                                 ("comprimento", a.L, comprimento(it))):
            if alvo is None:
                continue
            if not isinstance(valor, float):
                medidas = None
                break
            desvio = abs(valor - alvo) / alvo * 100
            tol = a.tol / 2 if rot == "fio" else a.tol
            if desvio > tol:
                medidas = None
                break
            medidas.append((rot, valor, desvio))
        if medidas is None:
            continue
        if medidas:
            pontos += 10 - sum(m[2] for m in medidas) / len(medidas) / max(a.tol, 1) * 5
            motivos.append("medidas: " + ", ".join("%s %.2f (%.1f%%)" % m for m in medidas))
        res.append((pontos, it, motivos, aps))
    res.sort(key=lambda r: (-r[0], r[1]["codigo"]))
    return res


def cmd_buscar(a):
    if not any([a.texto, a.marca, a.modelo, a.equipamento, a.original, a.tipo, a.setor,
                a.d, a.De, a.Di, a.L]):
        sys.exit("Informe ao menos um criterio de busca.")
    itens, aplic = carregar(a.pasta)
    res = buscar(itens, aplic, a)
    if a.json:
        print(json.dumps([{"codigo": r[1]["codigo"], "descricao": r[1]["descricao"], "pontos": round(r[0], 2),
                           "motivos": r[2]} for r in res[: a.limite]], ensure_ascii=False, indent=2))
        return 0
    if not res:
        print("Nada encontrado. Proximo passo: pedir as medidas completas (fio, diametro, comprimento, "
              "espiras, pernas) e a maquina, e abrir como item sob encomenda.")
        return 0
    print("%d resultado(s)%s" % (len(res), "" if len(res) <= a.limite else " - mostrando %d" % a.limite))
    for pontos, it, motivos, aps in res[: a.limite]:
        med = " | ".join("%s %s" % (r, it[k]) for k, r in (("d_fio_mm", "fio"), ("de_mm", "De"), ("di_mm", "Di"),
                                                           ("l0_mm", "L0"), ("comprimento_total_mm", "compr."))
                         if it[k])
        print("\n%s  [%s | %s%s]\n  %s" % (it["codigo"], TIPOS.get(it["tipo"], it["tipo"]),
                                         SETORES.get(it["setor"], it["setor"]),
                                         " | FAMILIA" if it["nivel"] == "familia" else "", it["descricao"]))
        print("  " + (med or "medidas sob consulta") + ("  | " + it["material"] if it["material"] else ""))
        for m in motivos:
            print("  -> " + m)
    return 0


def cmd_ficha(a):
    itens, aplic = carregar(a.pasta)
    it = next((i for i in itens if norm(i["codigo"]) == norm(a.codigo)), None)
    if not it:
        sys.exit("Codigo %s nao encontrado." % a.codigo)
    print("%s - %s" % (it["codigo"], it["descricao"]))
    print("%s | %s | %s" % (TIPOS.get(it["tipo"], it["tipo"]), SETORES.get(it["setor"], it["setor"]),
                            it["situacao"] or "situacao nao informada"))
    for k, rot in ROTULOS:
        if it[k]:
            print("  %-34s %s%s" % (rot, it[k], " " + it["unidade_constante"] if k == "constante" else ""))
    if it["observacoes"]:
        print("  Obs.: " + it["observacoes"])
    aps = [ap for ap in aplic if ap["codigo"] == it["codigo"]]
    if aps:
        print("  Aplicacoes:")
        for ap in aps:
            print("   - " + " | ".join(x for x in (ap["equipamento"], ap["marca"], ap["modelo"], ap["posicao"],
                                                   ("ref. " + ap["codigo_original"]) if ap["codigo_original"] else "",
                                                   (ap["qtd_por_maquina"] + " por maquina") if ap["qtd_por_maquina"] else "")
                                       if x))
    return 0


def cmd_gerar(a):
    itens, aplic = carregar(a.pasta)
    erros, _ = validar(itens, aplic)
    if erros and not a.forcar:
        for e in erros[:20]:
            print("ERRO  " + e)
        sys.exit("O catalogo tem %d erro(s). Corrija (ou use --forcar) antes de gerar." % len(erros))
    por = indice(itens, aplic)
    dados = []
    for it in itens:
        if it["situacao"] == "descontinuado" and not a.incluir_descontinuados:
            continue
        reg = {k: it[k] for k in CAMPOS_ITENS if it[k]}
        for k in ("d_fio_mm", "de_mm", "di_mm", "l0_mm", "comprimento_total_mm"):
            v = num(it[k])
            if isinstance(v, float):
                reg["_" + k] = v
        de = diam_externo(it)
        if de:
            reg["_de"] = de
        cp = comprimento(it)
        if cp:
            reg["_comp"] = cp
        reg["aplic"] = [{k: ap[k] for k in CAMPOS_APLIC[1:] if ap[k]} for ap in por.get(it["codigo"], [])]
        dados.append(reg)
    modelo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "catalogo-modelo.html")
    with open(modelo, encoding="utf-8") as f:
        pagina = f.read()
    cfg = {"empresa": a.empresa, "titulo": a.titulo, "whatsapp": re.sub(r"\D", "", a.whatsapp or ""),
           "fotos": a.fotos or "", "tipos": TIPOS, "setores": SETORES, "rotulos": ROTULOS,
           "atualizado": a.data or ""}
    pagina = pagina.replace("__TITULO__", html.escape(a.titulo)).replace("__EMPRESA__", html.escape(a.empresa))
    pagina = pagina.replace("/*__DADOS__*/[]", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    pagina = pagina.replace("/*__CFG__*/{}", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print("catalogo gerado: %s (%d registros, %d aplicacoes, %.0f KB)" % (
        a.saida, len(dados), sum(len(d["aplic"]) for d in dados), os.path.getsize(a.saida) / 1024))
    if not cfg["whatsapp"]:
        print("AVISO sem --whatsapp: os botoes de pedido ficam desativados")
    return 0


def cmd_app(a):
    """Gera o aplicativo: catalogo + calculadora de molas + consultor de Inconel X-750 + pedido."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    itens, aplic = carregar(a.pasta)
    erros, _ = validar(itens, aplic)
    if erros and not a.forcar:
        for e in erros[:20]:
            print("ERRO  " + e)
        sys.exit("O catalogo tem %d erro(s). Corrija (ou use --forcar) antes de gerar." % len(erros))
    por = indice(itens, aplic)
    dados = []
    for it in itens:
        if it["situacao"] == "descontinuado":
            continue
        reg = {k: it[k] for k in CAMPOS_ITENS if it[k]}
        v = num(it["d_fio_mm"])
        if isinstance(v, float):
            reg["_d_fio_mm"] = v
        if diam_externo(it):
            reg["_de"] = diam_externo(it)
        if comprimento(it):
            reg["_comp"] = comprimento(it)
        reg["aplic"] = [{k: ap[k] for k in CAMPOS_APLIC[1:] if ap[k]} for ap in por.get(it["codigo"], [])]
        dados.append(reg)
    cand = [a.materiais, os.path.join(aqui, "..", "..", "jm-engenharia-molas", "references", "materiais.json"),
            os.path.join(aqui, "..", "assets", "materiais.json")]
    mats = {}
    for c in cand:
        if c and os.path.exists(c):
            with open(c, encoding="utf-8") as f:
                mats = json.load(f)["materiais"]
            break
    campos = ("nome", "condicao", "G", "E", "rho", "temp_max", "rm", "admissivel", "modulo_vs_temp",
              "tau_relax", "sigma_relax", "preset_nao_recomendado")
    mats = {k: {c: m[c] for c in campos if c in m} for k, m in mats.items() if m["rm"]["tipo"] != "certificado"}
    with open(os.path.join(aqui, "..", "assets", "app-modelo.html"), encoding="utf-8") as f:
        pagina = f.read()
    cfg = {"empresa": a.empresa, "titulo": a.titulo, "whatsapp": re.sub(r"\D", "", a.whatsapp or ""),
           "tipos": TIPOS, "setores": SETORES, "rotulos": ROTULOS, "atualizado": a.data or ""}
    emb = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    pagina = pagina.replace("__TITULO__", html.escape(a.titulo)).replace("__EMPRESA__", html.escape(a.empresa))
    pagina = pagina.replace("/*__DADOS__*/[]", emb(dados)).replace("/*__CFG__*/{}", emb(cfg))
    pagina = pagina.replace("/*__MATS__*/{}", emb(mats))
    if a.artefato:  # pagina sem o esqueleto do documento, para publicar como artefato
        ini, fim = pagina.index("<body>") + len("<body>"), pagina.rindex("</body>")
        pagina = pagina[ini:fim].strip() + "\n"
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print("aplicativo gerado: %s (%d registros, %d materiais na calculadora, %.0f KB)" % (
        a.saida, len(dados), len(mats), os.path.getsize(a.saida) / 1024))
    if not cfg["whatsapp"]:
        print("AVISO sem --whatsapp: o botao de pedido fica so com o texto para copiar")
    return 0


def medida(v):
    n = num(v)
    if not isinstance(n, float) or n <= 0:
        raise argparse.ArgumentTypeError("medida invalida: %s" % v)
    return n


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("novo"); s.add_argument("pasta")
    s = sub.add_parser("validar"); s.add_argument("pasta"); s.add_argument("--max-avisos", type=int, default=40)
    s = sub.add_parser("buscar"); s.add_argument("pasta")
    s.add_argument("--texto"); s.add_argument("--marca"); s.add_argument("--modelo")
    s.add_argument("--equipamento"); s.add_argument("--original", help="codigo original/de referencia ou codigo JM")
    s.add_argument("--tipo", choices=list(TIPOS)); s.add_argument("--setor", choices=list(SETORES))
    s.add_argument("--d", type=medida, help="diametro do fio, mm"); s.add_argument("--De", type=medida)
    s.add_argument("--Di", type=medida); s.add_argument("--L", type=medida, help="comprimento livre ou total, mm")
    s.add_argument("--tol", type=float, default=10.0,
                   help="tolerancia da busca por medidas, %% (o fio usa metade); padrao 10")
    s.add_argument("--limite", type=int, default=15); s.add_argument("--json", action="store_true")
    s = sub.add_parser("ficha"); s.add_argument("pasta"); s.add_argument("codigo")
    s = sub.add_parser("gerar"); s.add_argument("pasta"); s.add_argument("--saida", default="catalogo.html")
    s.add_argument("--empresa", default="Jardmolas"); s.add_argument("--titulo", default="Catálogo de molas")
    s.add_argument("--whatsapp", help="numero com DDI e DDD, so digitos (ex.: 5516...)")
    s.add_argument("--fotos", help="pasta ou URL base das fotos (o campo foto e somado a ela)")
    s.add_argument("--data", help="data de atualizacao a mostrar no rodape")
    s.add_argument("--incluir-descontinuados", action="store_true"); s.add_argument("--forcar", action="store_true")
    s = sub.add_parser("app"); s.add_argument("pasta"); s.add_argument("--saida", default="app.html")
    s.add_argument("--empresa", default="Jardmolas"); s.add_argument("--titulo", default="Central de Molas")
    s.add_argument("--whatsapp"); s.add_argument("--data")
    s.add_argument("--materiais", help="materiais.json da calculadora (padrao: o da skill de engenharia)")
    s.add_argument("--artefato", action="store_true", help="gera so o corpo da pagina, para publicar como artefato")
    s.add_argument("--forcar", action="store_true")
    a = p.parse_args()
    sys.exit({"app": cmd_app, "novo": cmd_novo, "validar": cmd_validar, "buscar": cmd_buscar, "ficha": cmd_ficha,
              "gerar": cmd_gerar}[a.cmd](a) or 0)


if __name__ == "__main__":
    main()
