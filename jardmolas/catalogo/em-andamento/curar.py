#!/usr/bin/env python3
"""Curadoria (uma vez) da pesquisa bruta -> base do catalogo (CSV).

Le os JSON de pesquisa (scratchpad/ref/*.json), aplica as regras editoriais e grava
jardmolas/catalogo/referencias-agro.csv. Cada linha recebe situacao 'catalogo' ou 'fora: motivo'.
Nada e inventado: so se limpa, agrupa e descarta.
"""
import csv
import glob
import json
import os
import re
import sys
import unicodedata

S = "/tmp/claude-0/-home-user-instagram-agent-skill/a44018b1-0e82-5173-b144-b41abd2c67b9/scratchpad"
SAIDA = sys.argv[1] if len(sys.argv) > 1 else "/home/user/instagram-agent-skill/jardmolas/catalogo/referencias-agro.csv"
MAPA = "/home/user/instagram-agent-skill/jardmolas/skills/jm-catalogo/assets/mapa-agro.json"


def chave(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def limpo(v):
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        v = ", ".join(str(x) for x in v if x)
    return re.sub(r"\s+", " ", str(v)).strip()


SETORES = [s["nome"] for s in json.load(open(MAPA, encoding="utf-8"))["setores"]]
POR_CHAVE = {chave(s): s for s in SETORES}
ALIAS = {"plantio e semeadura": "Plantio", "pulverizacao": "Pulverização e distribuição", "colheita": "Colheita de grãos",
         "rocadeiras e transmissoes": "Roçadeiras, trituradores e pastagem", "fenacao": "Fenação e forragem",
         "cana de acucar": "Cana-de-açúcar"}


def setor_de(nome):
    s = chave(nome)
    return POR_CHAVE.get(s) or ALIAS.get(s) or next((v for k, v in POR_CHAVE.items() if s and (s in k or k in s)), "")


# ---------------------------------------------------------------- exclusoes
FORA_NOME = (
    (r"feixe", "feixe de molas (não é mola de fio)"),
    (r"mola a g[aá]s|gas spring|amortecedor a g", "mola a gás"),
    (r"mola prato|belleville|pacote de molas", "mola prato / pacote de molas (não é mola helicoidal)"),
    (r"rosca sem[- ]fim|rosca (direita|esquerda) do sem[- ]fim|flex.?auger", "rosca sem-fim / helicoide de arame (confirmar se a Jardmolas fabrica)"),
    (r"mola plana|chapa-mola|l[aâ]mina", "mola plana (não é mola de fio)"),
    (r"mola de arranque|mola do arranque|mola de partida|mola retr[aá]til|mola de recuo|recoil", "mola espiral de partida (fita)"),
    (r"\bfundid", "peça fundida (não é mola de arame)"),
    (r"^conjunto|vareta-mola|var[aã]o mola|bra[cç]o (de lat[aã]o )?com mola|bra[cç]o-mola|^kit de pino|conjunto de dedo|conjunto tensor|conjunto mola",
     "conjunto montado (não é a mola avulsa)"),
    (r"v[aá]lvula interna \(motor\)", "mola de válvula de motor (fora da linha)"),
)
PINO = re.compile(r"retr[aá]til|caracol|sem[- ]fim|dedo oco", re.I)
DUVIDA = re.compile(r"\[VERIFICAR\]|A CONFIRMAR|confirmar se [eé]|pode n[aã]o ser|inferid|atribu[ií]da pelo prefixo|marca n[aã]o (citada|explicitada)|"
                    r"natureza da refer[eê]ncia|conferir colunas|sugere mola plana", re.I)
SEM_FUNCAO = re.compile(r"^(mola|molas|mola de a[cç]o|mola completa|mola suporte|mola direita|mola com haste|mola compressor l046|"
                        r"mola da plataforma de milho|mola da ensiladeira|mola chave pequena do subsolador|mola de retorno esquerda|"
                        r"mola com amarra[cç][aã]o le, sem tucho|mola da segadeira/enleirador)$", re.I)
EXCLUIR = {  # arquivo#indice -> motivo
    "culturas#12": "tipo de mola não confirmado (provável mola voluta de fita)", "culturas#13": "tipo de mola não confirmado (provável mola voluta de fita)",
    "culturas#14": "tipo de mola não confirmado (provável mola voluta de fita)", "culturas#15": "tipo de mola não confirmado (provável mola voluta de fita)",
    "culturas#16": "tipo de mola não confirmado (provável mola voluta de fita)", "culturas#17": "tipo de mola não confirmado (pode ser bucha)",
    "culturas#4": "máquina não informada", "culturas#22": "conjunto montado (não é a mola avulsa)",
    "fenacao#50": "dente perfilado (tipo não confirmado)", "fenacao#93": "só referência de reposição para roda de reposição",
    "fenacao#94": "só referência de reposição (coberta por outro código)", "fenacao#5": "extrato da fonte desalinhado (conferir)",
    "fenacao#56": "medidas e código sem atribuição clara", "fenacao#68": "números do kit sem origem declarada",
    "plantio#17": "função não identificada", "plantio#67": "código interno de loja",
    "colheita#9": "material não informado (pode não ser de arame)", "colheita#10": "material não informado (pode não ser de arame)",
    "colheita#11": "material não informado (pode não ser de arame)", "colheita#49": "função não confirmada",
    "colheita#75": "função não identificada", "colheita#76": "função não identificada", "colheita#77": "função não identificada",
    "armazenagem-tratores#12": "aplicação não informada",
    "pecuaria-irrigacao#0": "aplicação não identificada", "pecuaria-irrigacao#30": "função não identificada",
    "solo-outros#29": "conjunto montado (não é a mola avulsa)", "solo-outros#30": "conjunto montado (não é a mola avulsa)",
    "solo-outros#14": "", "solo-outros#47": "função não identificada",
}
EXCLUIR.pop("solo-outros#14")
EXCLUIR.update({"fenacao#27": "repetida (mesma peça do código 9557100)", "fenacao#35": "só referência de reposição (provável repetição do 2684050)"})
CODIGOS = {"fenacao#11": "2904582", "fenacao#12": "2904583", "fenacao#16": "2904572", "fenacao#10": "2904584", "fenacao#13": "2904581",
           "fenacao#17": "7220950"}
MARCAS = {"fenacao#90": "Sitrex / New Holland / H&S / AGCO / Bush Hog / M&W / Otma", "fenacao#87": "Vermeer / Massey Ferguson", "culturas#2": "Nogueira / JF / Pinheiro / Cremasco", "fenacao#6": "Kuhn"}
NOTAS = {"fenacao#17": "anunciado em arame de 5,5 e de 6 mm"}

# referencias de reposicao aceitas (catalogos de pecas com numero proprio)
REPOSICAO = (
    (r"Sparex (S\.\d+)", "Sparex"), (r"Kramp (\d{6,}\w*KR|\d{9}\b|\d{6}N\b)", "Kramp"), (r"Thor (TH\w+)", "Thor"),
    (r"Shoup ((?:SH|RT)\d+)", "Shoup"), (r"Abilene Machine (AM\w+)", "Abilene"), (r"Faie (FA\d+)", "Faie"),
    (r"H&H (\d+H)", "H&H"), (r"Unifort (5067[.\d]+)", "Unifort"),
)
MARCAS_COD = ("John Deere", "Vermeer", "Vicon", "Kverneland", "Kuhn", "Tonutti", "Sitrex", "New Holland", "AGCO", "Bush Hog", "H&S",
              "M&W", "Otma", "Massey Ferguson", "Metasa")
QUALIF = re.compile(r"^(direito|esquerdo|direita|esquerda|" + "|".join(re.escape(m) for m in MARCAS_COD) + r")$", re.I)


def codigos(texto):
    """'A (direito); Marca B / C' -> [('A','direito'), ('B','Marca'), ('C','Marca')]"""
    saida = []
    texto = re.sub(r"\(([^()]*)\)", lambda m: m.group(0) if QUALIF.match(m.group(1).strip()) else "", texto)
    for parte in re.split(r"\s*;\s*", texto):
        parte = parte.strip()
        if not parte:
            continue
        q = ""
        m = re.search(r"\(([^()]*)\)\s*$", parte)
        if m:
            if QUALIF.match(m.group(1).strip()):
                q = m.group(1).strip()
            parte = parte[:m.start()].strip()
        parte = re.sub(r"\([^()]*\)", "", parte).strip()
        m = re.match(r"^(%s)\s+(.+)$" % "|".join(re.escape(x) for x in MARCAS_COD), parte)
        if m:
            q, parte = m.group(1), m.group(2)
        for c in re.split(r"\s+/\s+|,\s*", parte):
            c = c.strip(" .")
            if len(c) >= 3 and re.search(r"\d", c) and (c, q) not in saida:
                saida.append((c, q))
    return saida


def reposicao(texto):
    saida = []
    for rx, marca in REPOSICAO:
        for m in re.finditer(rx, texto):
            item = "%s %s" % (marca, m.group(1))
            if item not in saida:
                saida.append(item)
    return saida


# ---------------------------------------------------------------- nomes
NOTA = re.compile(r"\s*\((?:[^()]*?(?:n[aã]o inform|n[aã]o confirm|fun[cç][aã]o n|reposi[cç][aã]o|alternativ|similar|gen[eé]ric|conforme|"
                  r"tamb[eé]m anunciad|descri[cç][aã]o cita|c[oó]digo varia|pe[cç]a \d|avulsa|opcional)[^()]*)\)", re.I)
TROCAS = (
    (r"^Dedo de a[cç]o \(mola\)", "Dedo de mola"), (r"^Mola/dedo", "Dedo de mola"), (r"^Dente \(mola\)", "Dente de mola"),
    (r"^Mola \(dente\)", "Dente de mola"), (r"^Dente \(dedo\)", "Dedo"), (r"^Dente \(p[uú]a\)", "Dente"),
    (r"^Mola \(dedo / garfo\)", "Dedo de mola"), (r"^Mola \(dedo\)", "Dedo de mola"), (r"^Mola \(garfo\)", "Mola"),
    (r"^Bra[cç]o-dente \(mola\)", "Braço-dente de mola"), (r"^Mola comprimida", "Mola de compressão"),
    (r"^Dedo de a[cç]o do molinete", "Dedo de mola do molinete"), (r"^Dedo do molinete", "Dedo de mola do molinete"),
    (r"^Kit de dedos de a[cç]o externos do molinete.*", "Dedos de mola externos do molinete (kit)"),
    (r"^Dedo flex[ií]vel tipo reto", "Dedo flexível reto"), (r"^Dedo flex[ií]vel \(dedo reto\)", "Dedo flexível reto"),
    (r" / pick-up", ""), (r", simples, 3 espiras", ""), (r", lado esquerdo", ""), (r", \d+ mm$", ""),
    (r"\s+-\s+arame [\d,]+ mm$", ""), (r"\s+-\s+(direito|esquerdo)$", r" \1"),
)


def nome_peca(t):
    t = NOTA.sub("", t).strip(" ,;-")
    for rx, novo in TROCAS:
        t = re.sub(rx, novo, t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" ,;-")
    return t[:1].upper() + t[1:] if t else "Mola"


def tipo_de(nome):
    n = chave(nome)
    if re.search(r"\b(dedo|dedos|dente|dentes|garfo|braco dente)\b", n):
        return "dedo"
    m = re.match(r"^(?:jogo de )?molas? (?:\w+ )?de (tracao|compressao|torcao|pressao)\b", n)
    if m:
        return "compressao" if m.group(1) == "pressao" else m.group(1)
    return ""


MAQ = (  # padrao no texto bruto -> nome curto
    (r"enleirador-espalhador|enleirador espalhador", "Ancinho enleirador-espalhador"),
    (r"enleirador / espalhador|espalhador / enleirador", "Enleirador / espalhador rotativo"),
    (r"enleirador rotativo", "Enleirador rotativo"), (r"espalhador rotativo", "Espalhador rotativo"),
    (r"ancinho de rodas|ancinho enleirador \(rake\)", "Ancinho de rodas"), (r"ancinho enleirador de barras", "Ancinho de barras"),
    (r"ancinho enleirador", "Ancinho enleirador"), (r"enfardadeira de rolos", "Enfardadeira de rolos"),
    (r"fardos gigantes", "Enfardadeira de fardos gigantes"), (r"fardos retangulares", "Enfardadeira de fardos retangulares"),
    (r"enfardadeira", "Enfardadeira"), (r"recolhedor \(pick-up\)", "Recolhedor (pick-up)"), (r"segadora-condicionadora", "Segadora-condicionadora"),
    (r"vag[aã]o forrageiro", "Vagão forrageiro"), (r"desenleirador de palha", "Desenleirador de palha"), (r"enleirador de palha", "Enleirador de palha"),
    (r"ensiladeira", "Ensiladeira"), (r"plataforma de milho", "Plataforma de milho"), (r"plataforma draper", "Plataforma draper"),
    (r"plataforma de corte", "Plataforma de corte"), (r"colhedora jumil", "Colhedora de milho"), (r"colheitadeira", "Colheitadeira"),
    (r"plantad", "Plantadeira"), (r"grade", "Grade"), (r"subsolador", "Subsolador / escarificador"), (r"perfurador", "Perfurador de solo"),
    (r"autopropelido", "Pulverizador autopropelido"), (r"pulverizador estacion", "Pulverizador estacionário"), (r"pulverizador", "Pulverizador de barras"),
    (r"cardan|embreagem de fric", "Eixo cardan"), (r"trator", "Trator"), (r"colhedora de algod", "Colhedora de algodão"),
    (r"colhedora de caf", "Colhedora de café"), (r"tesoura de poda", "Tesoura de poda"), (r"rob[oô] de ordenha", "Robô de ordenha"),
    (r"ordenhadeira", "Ordenhadeira"), (r"bebedouro nipple", "Bebedouro nipple"), (r"bebedouro", "Bebedouro"),
    (r"transport\w+ de ra[cç][aã]o", "Linha de ração"), (r"coleta de ovos", "Coleta de ovos"), (r"elevador de ovos", "Elevador de ovos"),
    (r"alimenta[cç][aã]o de porcas", "Estação de alimentação de porcas"), (r"climatiza", "Climatização de aviário"),
    (r"dosador de medicamentos", "Dosador de medicamentos"), (r"aplica[cç][aã]o n[aã]o informada", ""),
    (r"canh[aã]o aspersor", "Canhão aspersor"), (r"aspersor de impacto", "Aspersor de impacto"), (r"costura", "Costuradora de sacaria"),
    (r"motosserra", "Motosserra"), (r"ro[cç]adeira", "Roçadeira costal"), (r"motocultivador", "Motocultivador"),
)


def nome_maquina(t):
    b = t.lower()
    for rx, novo in MAQ:
        if re.search(rx, b):
            return novo
    t = re.split(r"\s+[—–-]\s+|\s*\(", t)[0].strip(" ,;-")
    return t[:1].upper() + t[1:] if t else ""


MARCA_1 = ("Massey Ferguson", "John Deere", "New Holland", "Case IH", "Tatu Marchesan", "Claas", "Krone", "Nogueira", "Kuhn", "Vicon")


def marcas(t):
    t = re.sub(r"\s*\([^()]*\)", "", t)
    lista = [x.strip() for x in t.split("/") if x.strip()]
    lista = ["Kverneland" if x == "Taarup" else x for x in lista]
    for pref in MARCA_1:
        if pref in lista:
            lista.remove(pref)
            lista.insert(0, pref)
            break
    vistos = []
    for x in lista:
        if x not in vistos:
            vistos.append(x)
    return vistos


MODELOS = {  # arquivo#indice -> modelos limpos
    "armazenagem-tratores#6": "DS-9A, DS-9C, DS-9P, DS-9CW", "armazenagem-tratores#8": "263, 2630, 2635, 265, 265 S, 275, 285, 285 S, 290",
    "armazenagem-tratores#9": "243, 253, 260, 261, 2625, 263, 2635, 265, 270, 275, 283, 285, 290, 375, 375E",
    "armazenagem-tratores#11": "135, 240, 250, 270", "armazenagem-tratores#41": "FS 160, FS 220, FR 220",
    "colheita#6": "Plataformas série 200", "colheita#12": "Plataformas 2030, 2040, 2050", "colheita#39": "", "colheita#52": "Linha CR",
    "colheita#53": "CR7.90", "colheita#72": "JM370", "colheita#34": "Séries 200 e 900",
    "culturas#2": "", "culturas#5": "9970, 9986, CP690", "culturas#6": "9910, 9920, 9930, 9935, 9940, 9950, 9960, 9965, 9970, 9986",
    "culturas#7": "7660, 7760, 9935, 9970, 9976, 9986, 9996, CP690", "culturas#8": "9970, 9986", "culturas#20": "78300/001",
    "culturas#18": "78304, 78308", "culturas#19": "78316", "culturas#21": "78363, 78366",
    "fenacao#0": "GA4100TH, GA6501P, GA8121, GA8521", "fenacao#1": "Linha GA",
    "fenacao#2": "GA300GM, GA300GT, GA3200GT, GA4101GM, GA4101GTH, GA7301, GA7302DL, GA7501", "fenacao#3": "GA 7301",
    "fenacao#4": "GA 440, GA 452 GF", "fenacao#6": "GF10601, GF10802, GF13002, GF13012T, GF17002, GF422, GF5001",
    "fenacao#8": "Linhas GA e GF", "fenacao#9": "Linha GA", "fenacao#11": "Haynog 300", "fenacao#13": "Haybob 300, Haynog 300",
    "fenacao#19": "EN-9, EN-12", "fenacao#14": "Haybob 300, Haynog 300, Spin 3000, Águia 300", "fenacao#15": "Haybob 300, Haynog 300, Spin 3000, Águia 300",
    "solo-outros#41": "Haynog 300", "solo-outros#42": "Haynog 300", "fenacao#21": "6 rodas", "fenacao#22": "", "fenacao#30": "Quadrant 1100, 1150, 1200",
    "fenacao#32": "KW 4.40-4, KW 5.50-4, KW 6.40-6", "fenacao#34": "Swadro 42, 46, 700, 800, 807, 810, 900, 907",
    "fenacao#38": "KW 3.70 a 13.00", "fenacao#47": "1600HYDRO, 455DN", "fenacao#49": "TH 1100, TH 1300", "fenacao#61": "",
    "fenacao#62": "166, 565, 568, 570, 575, 580, 848, 853, 855", "fenacao#63": "Supersweep", "fenacao#64": "Séries 65 a 311",
    "fenacao#69": "Séries BR7000 e BC5000", "fenacao#75": "348", "fenacao#85": "", "fenacao#67": "Rolabar 256, 258, 259, 260",
    "pecuaria-irrigacao#4": "Slope Regulator 15 cm", "pecuaria-irrigacao#10": "FLEX-AUGER", "pecuaria-irrigacao#11": "FLEX-AUGER",
    "pecuaria-irrigacao#9": "FLEX-AUGER 55 a 125", "pecuaria-irrigacao#20": "Mixtron", "pecuaria-irrigacao#21": "Mixtron",
    "pecuaria-irrigacao#18": "EggCellent", "pecuaria-irrigacao#19": "EggCellent", "armazenagem-tratores#34": "017 a 025, MS 170 a MS 251",
    "armazenagem-tratores#37": "034 a MS 360", "pecuaria-irrigacao#22": "Big Gun SR150",
    "plantio#36": "PST2", "plantio#37": "PST2", "plantio#87": "Séries 1100, 2100 e DB", "plantio#91": "Série 1100",
    "solo-outros#7": "AST/MATIC", "solo-outros#45": "GA 300, GA 350, GA 7302", "solo-outros#46": "GA 3501, GA 3801, GA 3901, GA 4120, GA 4121, GA 8121, GA 8131",
    "solo-outros#4": "AST/MATIC 450", "solo-outros#5": "AST/MATIC 450, AST/MATIC 550",
}
NOMES = {  # arquivo#indice -> nome da peca (quando a limpeza automatica nao basta)
    "fenacao#6": "Dente de mola esquerdo do espalhador", "fenacao#7": "Dente de mola direito do espalhador",
    "fenacao#10": "Mola larga direita do rotor (garfo)", "fenacao#11": "Mola larga esquerda do rotor (garfo)",
    "fenacao#12": "Mola estreita direita do rotor (garfo)", "fenacao#13": "Mola estreita esquerda do rotor (garfo)",
    "fenacao#17": "Dedo de mola do recolhedor", "fenacao#18": "Dedo de mola do recolhedor", "fenacao#41": "Dente de mola direito do espalhador",
    "fenacao#42": "Dente de mola esquerdo do espalhador", "fenacao#47": "Dente de mola direito/esquerdo",
    "fenacao#65": "Dente de mola esquerdo", "plantio#68": "Mola do esticador da corrente", "plantio#47": "Mola de tração do rodado",
    "plantio#60": "Mola de torção esquerda da linha da semente", "plantio#70": "Mola da haste reguladora de profundidade",
    "pecuaria-irrigacao#39": "Mola da chave do inversor", "plantio#72": "Mola de compressão do kit de plantio convencional",
    "solo-outros#14": "Mola de tração do perfurador de solo", "pecuaria-irrigacao#34": "Mola esquerda do braço de acionamento",
    "fenacao#2": "Dente de mola do enleirador", "fenacao#3": "Dente de mola do enleirador", "fenacao#62": "Dente duplo do recolhedor",
    "solo-outros#43": "Mola larga esquerda do rotor (garfo)", "solo-outros#44": "Mola larga direita do rotor (garfo)",
    "solo-outros#45": "Dente de mola do enleirador", "solo-outros#46": "Dente de mola do enleirador",
    "plantio#7": "Mola do elevador (esticador)", "plantio#9": "Mola de compressão do sulcador / kit facão-disco",
    "plantio#10": "Mola de compressão do sulcador / kit facão-disco", "plantio#37": "Mola de compressão do eixo limitador de tecla",
    "plantio#53": "Mola de compressão da linha (varão guia)", "plantio#54": "Mola de compressão da linha de adubo",
    "plantio#58": "Mola de tração da roda cobridora do adubo em V (esquerda)", "plantio#62": "Mola de compressão do carrinho da roda compactadora em V",
    "plantio#76": "Mola de compressão do compactador flutuante em V", "plantio#78": "Mola de tração do compactador flutuante em V com disco",
    "plantio#77": "Mola de compressão da unidade semeadora", "plantio#119": "Mola do esticador / articulador",
    "plantio#99": "Mola de compressão externa (maior)", "plantio#89": "Mola do distribuidor de sementes (inox)",
    "colheita#0": "Dedo de mola do molinete", "colheita#1": "Dedo de mola do molinete", "colheita#2": "Dedo de mola do molinete",
    "colheita#3": "Dedo de mola do molinete", "colheita#4": "Dedo de mola do molinete", "colheita#5": "Dedo de mola do molinete",
    "colheita#12": "Dedo de mola do molinete", "colheita#13": "Dedo de mola do molinete", "colheita#37": "Mola do esticador da correia",
    "colheita#56": "Mola da flutuação", "colheita#52": "Mola do elevador de palhas", "colheita#43": "Mola da catraca do caracol (sem-fim)",
    "culturas#2": "Mola do quebra-jato (bica de descarga)", "culturas#0": "Mola do cilindro dentado", "culturas#3": "Mola da pá recolhedora",
    "culturas#7": "Mola de torção central e superior da placa de pressão", "culturas#18": "Mola helicoidal da tesoura de poda",
    "culturas#19": "Mola helicoidal da tesoura de poda", "culturas#20": "Mola da tesoura de poda", "culturas#21": "Mola da tesoura de poda de cabo extensível",
    "pecuaria-irrigacao#13": "Mola de tração inox", "pecuaria-irrigacao#15": "Mola de tração", "pecuaria-irrigacao#16": "Mola de torção direita",
    "pecuaria-irrigacao#23": "Mola do gatilho (trip)", "pecuaria-irrigacao#2": "Mola da válvula do tanque",
    "solo-outros#23": "Mola de compressão", "solo-outros#28": "Mola de compressão do cardan", "solo-outros#34": "Mola de compressão do cardan",
    "solo-outros#57": "Mola de compressão do cardan", "solo-outros#31": "Dedo flexível reto do enleirador de palha",
    "fenacao#21": "Dedo flexível reto do enleirador de palha", "armazenagem-tratores#8": "Mola da embreagem (vermelha)",
    "solo-outros#53": "Jogo de molas da embreagem de fricção (8 un.)", "solo-outros#54": "Jogo de molas da embreagem de fricção (8 un.)",
    "solo-outros#55": "Jogo de molas da embreagem de fricção (8 un.)",
}
MEDIDA_PUBLICADA = {  # medidas publicadas sem rotulo: reproduzidas como estao
    "plantio#91": "6 × 23 × 180 × 250 mm", "solo-outros#23": "12 × 50 × 85 mm", "solo-outros#24": "9 × 28 × 99 × 160 mm", "plantio#113": "12 × 43 × 141 mm",
}
SEM_MEDIDA = {"fenacao#11", "fenacao#18", "fenacao#17", "fenacao#52", "fenacao#55", "armazenagem-tratores#21", "colheita#20", "colheita#25",
              "pecuaria-irrigacao#0", "fenacao#63", "fenacao#67", "fenacao#79", "fenacao#87", "fenacao#89", "fenacao#90", "fenacao#91", "fenacao#92",
              "fenacao#62", "fenacao#64", "fenacao#76", "fenacao#80", "fenacao#82", "fenacao#88"}
SETOR_FIXO = {"fenacao#19": "Ensilagem e alimentação animal", "fenacao#21": "Cana-de-açúcar", "fenacao#22": "Cana-de-açúcar",
              "solo-outros#14": "Preparo de solo", "culturas#23": "Fruticultura e citros"}


def numero(v):
    """'590 (Kramp...)' -> ('590', nota)   '146.05 (5.75 in)' -> ('146', ...)"""
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)\s*(.*)$", v or "")
    if not m:
        return "", ""
    x = float(m.group(1).replace(",", "."))
    txt = ("%.2f" % x).rstrip("0").rstrip(".") if abs(x - round(x, 1)) > 1e-9 and x < 20 else ("%.1f" % x).rstrip("0").rstrip(".")
    return txt.replace(".", ","), m.group(2)


def diametro_ref(campo, obs, valor):
    t = campo.lower()
    if "intern" in t:
        return "interno"
    if "extern" in t:
        return "externo"
    o = obs.lower()
    if re.search(r"espira_mm\s*=\s*(ø|di[aâ]metro)\s*interno", o) or re.search(r"(ø|di[aâ]metro) interno (da espira|da mola)?\s*%s\b" % re.escape(valor.replace(",", ".")), o) \
            or re.search(r"(ø|di[aâ]metro) interno (da espira|da mola)?\s*%s\b" % re.escape(valor), o):
        return "interno"
    if re.search(r"espira_mm\s*=\s*(ø|di[aâ]metro)\s*externo", o):
        return "externo"
    return ""


def carregar():
    regs = []
    for arq in sorted(glob.glob(os.path.join(S, "ref", "*.json"))):
        base = os.path.basename(arq)[:-5]
        if base.startswith("mapa-"):
            continue
        for i, bruto in enumerate(json.load(open(arq, encoding="utf-8"))):
            if not isinstance(bruto, dict):
                continue
            r = {k: limpo(bruto.get(k)) for k in ("setor", "maquina", "marca", "modelos", "peca_pt", "peca_original", "codigo_original",
                                                 "ref_aftermarket", "arame_mm", "comprimento_mm", "espira_mm", "obs", "fonte")}
            r["id"] = "%s#%d" % (base, i)
            regs.append(r)
    return regs


def curar(r):
    """Devolve a linha curada (dict) com 'situacao'."""
    rid = r["id"]
    bruto_nome = r["peca_pt"] or r["peca_original"]
    nome = NOMES.get(rid) or nome_peca(bruto_nome)
    cods = codigos(CODIGOS.get(rid, r["codigo_original"]))
    reps = reposicao(r["ref_aftermarket"])
    lista = MARCAS[rid].split(" / ") if rid in MARCAS else marcas(r["marca"])
    if len(lista) == 1:
        cods = [(c, "" if q == lista[0] else q) for c, q in cods]
    reps = [x for x in reps if chave(x.split(" ", 1)[1]) not in {chave(c) for c, _ in cods}]
    setor = SETOR_FIXO.get(rid) or setor_de(r["setor"])
    junto = (r["maquina"] + " " + bruto_nome).lower()
    if re.search(r"cardan|cardã|embreagem de fric|limitador de torque", junto):
        setor = "Tratores, cardans e engates"
    if re.search(r"fena[cç][aã]o", r["maquina"].lower()):
        setor = "Fenação e forragem"
    maq = nome_maquina(r["maquina"])
    modelos = MODELOS[rid] if rid in MODELOS else r["modelos"]
    modelos = re.sub(r"\s*;\s*", ", ", modelos)
    modelos = re.sub(r"\b(Kuhn|Nogueira|Mainero|MacDon|Massey Ferguson|John Deere|FELCO|Tatu|Jumil|NH)\s+(?=[A-Z0-9])", "", modelos) if lista else modelos

    motivo = ""
    if rid in EXCLUIR:
        motivo = EXCLUIR[rid]
    elif not lista:
        motivo = "sem marca"
    elif not r["fonte"]:
        motivo = "sem fonte"
    elif not cods and not reps:
        motivo = "sem código de peça"
    elif not setor:
        motivo = "setor não identificado"
    else:
        for rx, m in FORA_NOME:
            if re.search(rx, bruto_nome, re.I):
                motivo = m
                break
        if not motivo and "dedo" in bruto_nome.lower() and PINO.search(bruto_nome) and not bruto_nome.lower().startswith("mola"):
            motivo = "dedo retrátil do caracol (pino, não é mola)"
        if not motivo and DUVIDA.search(r["obs"] + " " + bruto_nome):
            motivo = "evidência fraca (ver observação)"
        if not motivo and SEM_FUNCAO.match(re.sub(r"\s*\([^()]*\)", "", nome).strip()):
            motivo = "função não identificada"
        if not motivo and "rodovi" in r["obs"].lower():
            motivo = "aplicação rodoviária, não agrícola"

    arame, _ = numero(r["arame_mm"])
    compr, _ = numero(r["comprimento_mm"])
    diam, _ = numero(r["espira_mm"])
    ref = diametro_ref(r["espira_mm"], r["obs"], diam) if diam else ""
    larg = ""
    m = re.search(r"[Ll]argura (\d+(?:[.,]\d+)?) mm", r["obs"])
    if m and tipo_de(nome) == "dedo":
        larg = m.group(1).replace(".", ",")
    publicada = MEDIDA_PUBLICADA.get(rid, "")
    if rid in SEM_MEDIDA or publicada:
        arame = compr = diam = ref = larg = ""
    nota = ""
    m = re.search(r"\b(\d(?:,5)?) espiras\b", r["obs"])
    if m and tipo_de(nome) == "dedo":
        nota = m.group(0)
    nota = NOTAS.get(rid, nota)
    return {"setor": setor, "maquina": maq, "marca": " / ".join(lista), "modelos": modelos.strip(" ,;"), "peca": nome, "tipo": tipo_de(nome),
            "codigo_original": " · ".join("%s (%s)" % c if c[1] else c[0] for c in cods), "ref_reposicao": " · ".join(reps),
            "arame_mm": arame, "comprimento_mm": compr, "diametro_mm": diam, "diametro_ref": ref, "largura_mm": larg,
            "medida_publicada": publicada, "nota": nota, "situacao": "fora: " + motivo if motivo else "catalogo", "conferido": "",
            "obs_pesquisa": r["obs"], "fonte": r["fonte"], "id": rid, "_cods": [c[0] for c in cods] or reps}


def riqueza(r):
    return (bool(r["arame_mm"] or r["comprimento_mm"]), bool(r["modelos"]), len(r["_cods"]), bool(r["tipo"]), len(r["peca"]))


def unir(regs):
    """Une, dentro de cada setor, as linhas do catalogo que compartilham algum codigo. Fica a mais completa."""
    dentro = [r for r in regs if r["situacao"] == "catalogo"]
    fora = [r for r in regs if r["situacao"] != "catalogo"]
    dentro.sort(key=riqueza, reverse=True)
    donos, finais = {}, []
    for r in dentro:
        ks = [(r["setor"], chave(c)) for c in r["_cods"]]
        dono = next((donos[k] for k in ks if k in donos), None)
        if dono is None:
            finais.append(r)
            for k in ks:
                donos[k] = r
            continue
        # completa a linha dona com o que esta traz de novo
        mods = [x.strip() for x in dono["modelos"].split(",") if x.strip()]
        for x in (x.strip() for x in r["modelos"].split(",")):
            if x and chave(x).replace(" ", "") not in {chave(y).replace(" ", "") for y in mods}:
                mods.append(x)
        dono["modelos"] = ", ".join(mods)
        for campo in ("codigo_original", "ref_reposicao"):
            tem = [x for x in dono[campo].split(" · ") if x]
            for x in (x for x in r[campo].split(" · ") if x):
                if chave(re.sub(r"\(.*?\)", "", x)) not in {chave(re.sub(r"\(.*?\)", "", y)) for y in tem}:
                    tem.append(x)
            dono[campo] = " · ".join(tem)
        for c in r["_cods"]:
            if c not in dono["_cods"]:
                dono["_cods"].append(c)
                donos[(dono["setor"], chave(c))] = dono
        for m in marcas(r["marca"]):
            if m not in dono["marca"].split(" / "):
                dono["marca"] += " / " + m
        dono["fonte"] += " | " + r["fonte"] if r["fonte"] not in dono["fonte"] else ""
        dono["id"] += "+" + r["id"]
        r["situacao"] = "fora: repetida (unida à linha de mesmo código)"
        fora.append(r)
    return finais, fora


def main():
    brutos = carregar()
    curados = [curar(r) for r in brutos]
    dentro, fora = unir(curados)
    ordem = {s: i for i, s in enumerate(SETORES)}
    dentro.sort(key=lambda r: (ordem[r["setor"]], chave(r["marca"]), chave(r["maquina"]), chave(r["modelos"]), chave(r["peca"])))
    fora.sort(key=lambda r: (r["situacao"], r["id"]))
    campos = ["setor", "maquina", "marca", "modelos", "peca", "tipo", "codigo_original", "ref_reposicao", "arame_mm", "comprimento_mm",
              "diametro_mm", "diametro_ref", "largura_mm", "medida_publicada", "nota", "situacao", "conferido", "obs_pesquisa", "fonte", "id"]
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in dentro + fora:
            w.writerow(r)
    print("brutas %d | no catalogo %d | fora %d" % (len(brutos), len(dentro), len(fora)))
    from collections import Counter
    for s in SETORES:
        print("  %-40s %3d" % (s, sum(1 for r in dentro if r["setor"] == s)))
    for m, n in Counter(r["situacao"] for r in fora).most_common():
        print("  %3d %s" % (n, m))


if __name__ == "__main__":
    main()
