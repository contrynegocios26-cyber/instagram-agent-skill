"""Gera a planilha de custo, preço e capacidade dos presentes de fim de ano da MP."""
import datetime as dt
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1]

F = "Arial"
BLUE = "0000FF"
GREEN = "008000"
YELLOW = PatternFill("solid", start_color="FFFF00")
HEAD = PatternFill("solid", start_color="2B1A16")
SOFT = PatternFill("solid", start_color="F3ECE6")
thin = Side(style="thin", color="BFB3AA")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
BRL = '"R$" #,##0.00;("R$" #,##0.00);"-"'
PCT = '0%;(0%);"-"'
DATE = "dd/mm/yyyy"

KITS = ["Essencial", "Churrasco", "Premium"]
STATUS = ["Proposta enviada", "Fechado", "Em produção", "Entregue", "Perdido"]
METODOS = ["Ferro a fogo (marcador com o logo)", "Laser terceirizado", "CNC própria (entalhe em V)"]


def font(cell, color="000000", bold=False, size=10, italic=False):
    cell.font = Font(name=F, color=color, bold=bold, size=size, italic=italic)


def title(ws, text, sub):
    ws["A1"] = text
    font(ws["A1"], bold=True, size=14)
    ws["A2"] = sub
    font(ws["A2"], color="555555", size=9, italic=True)


def header(ws, row, labels, col=1):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=lab)
        c.font = Font(name=F, bold=True, color="FFFFFF", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BOX


def inp(cell, value, fmt=None, key=False):
    """Célula de entrada: texto azul; amarela se for premissa-chave a confirmar."""
    cell.value = value
    font(cell, color=BLUE)
    cell.border = BOX
    if fmt:
        cell.number_format = fmt
    if key:
        cell.fill = YELLOW


def fx(cell, formula, fmt=None, link=False, bold=False):
    cell.value = formula
    font(cell, color=GREEN if link else "000000", bold=bold)
    cell.border = BOX
    if fmt:
        cell.number_format = fmt


def label(cell, text, bold=False):
    cell.value = text
    font(cell, bold=bold)
    cell.border = BOX
    cell.alignment = Alignment(wrap_text=True, vertical="center")


def note(cell, text):
    cell.value = text
    font(cell, color="555555", size=9, italic=True)
    cell.alignment = Alignment(wrap_text=True, vertical="center")


wb = Workbook()

# ---------------------------------------------------------------- Como usar
ws = wb.active
ws.title = "Como usar"
title(ws, "Presentes de fim de ano 2026: custo, preço e capacidade",
      "MP Marcenaria · Alto Paraná (PR) · planilha criada em 09/11/2026")
linhas = [
    ("O que é", "Calcula o custo de cada kit, o preço por faixa de quantidade e quanto da fábrica cada pedido ocupa."),
    ("1. Premissas", "Preencha as células AMARELAS (custo da hora, imposto, horas disponíveis, método de gravação). Hoje elas têm valores de referência, não os números da MP."),
    ("2. Custos", "Confira a ficha de cada kit. Números em azul são entradas: troque pelo custo real (cotação da faca, embalagem, tempo cronometrado no protótipo)."),
    ("3. Preços", "Não digite nada aqui. A tabela de preço sai sozinha das duas abas anteriores. É ela que vai para o catálogo."),
    ("4. Pedidos", "Cada proposta vira uma linha. Digite cliente, kit, quantidade e status; preço, total, sinal, lucro e horas saem sozinhos. O topo avisa quando a fábrica lota."),
    ("Cores", "Azul = entrada que você pode mudar · Preto = fórmula · Verde = puxa de outra aba · Amarelo = premissa a confirmar."),
    ("Regra de preço", "Preço = custo direto ÷ (1 − imposto − comissão − margem), arredondado para cima com final ,90. Margem nunca abaixo de 25%."),
    ("Ao confirmar um número", "Apague o [confirmar] da observação ao lado. Enquanto houver [confirmar], o preço é estimativa."),
]
for i, (a, b) in enumerate(linhas, start=4):
    ws.cell(row=i, column=1, value=a)
    font(ws.cell(row=i, column=1), bold=True)
    ws.cell(row=i, column=2, value=b)
    font(ws.cell(row=i, column=2))
    ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(row=i, column=1).alignment = Alignment(vertical="top")
    ws.row_dimensions[i].height = 32
ws.column_dimensions["A"].width = 22
ws.column_dimensions["B"].width = 100

# ---------------------------------------------------------------- Premissas
p = wb.create_sheet("Premissas")
title(p, "Premissas", "Amarelo = confirmar com a MP. Todos os valores abaixo são referência até serem confirmados.")
header(p, 4, ["Parâmetro", "Valor", "Unidade", "Observação / fonte"])
rows = [
    (5, "Custo da hora de fábrica", 40, "R$/h", BRL, True, "[confirmar] mão de obra com encargos + energia e desgaste de máquina"),
    (6, "Preço da madeira maciça comprada", 5000, "R$/m³", BRL, True, "[confirmar] só entra no custo do kit que NÃO usar retalho"),
    (7, "Perda no corte e na plaina", 0.35, "%", PCT, False, "Referência para tábua colada de tiras"),
    (8, "Imposto sobre a venda", 0.08, "%", PCT, True, "[confirmar com o contador] alíquota efetiva do Simples da MP"),
    (9, "Comissão de venda ou indicação", 0, "%", PCT, False, "Use 5% quando alguém de fora trouxer o cliente"),
    (10, "Pedido mínimo", 20, "peças", "0", False, "Abaixo disso a faixa aparece como 'abaixo do mínimo'"),
    (11, "Taxa de personalização por pedido", 290, "R$", BRL, False, "Arte do logo + ferro ou ajuste da gravação. Cobrada uma vez por pedido"),
    (12, "Taxa isenta a partir de", 100, "peças", "0", False, "Argumento de venda para pedido grande"),
    (13, "Método de gravação escolhido", METODOS[1], "", None, True, "[confirmar] escolha na lista; o custo vem da tabela abaixo"),
    (14, "Horas de fábrica por dia para a campanha", 8, "h/dia", "0.0", True, "[confirmar] ex.: 2 pessoas × 4 h sem atrasar os planejados"),
    (15, "Início da produção", dt.date(2026, 11, 16), "data", DATE, False, "Depois do protótipo aprovado"),
    (16, "Última entrega", dt.date(2026, 12, 18), "data", DATE, False, "Empresas entregam presente antes das confraternizações"),
    (19, "Sinal na assinatura do pedido", 0.5, "%", PCT, False, "Restante na entrega, com NF-e"),
]
for r, a, v, u, fmt, key, obs in rows:
    label(p.cell(row=r, column=1), a)
    inp(p.cell(row=r, column=2), v, fmt, key)
    label(p.cell(row=r, column=3), u)
    note(p.cell(row=r, column=4), obs)
label(p.cell(row=17, column=1), "Dias úteis de produção")
fx(p["B17"], "=NETWORKDAYS(B15,B16)", "0")
label(p.cell(row=17, column=3), "dias")
note(p["D17"], "Segunda a sexta entre as duas datas (não desconta feriado)")
label(p.cell(row=18, column=1), "Horas de fábrica disponíveis", bold=True)
fx(p["B18"], "=B14*B17", "0", bold=True)
label(p.cell(row=18, column=3), "h")
note(p["D18"], "É o teto de venda da campanha. A aba Pedidos compara com o que já foi fechado")

header(p, 21, ["Gravação: método", "Custo por gravação (R$)", "Custo fixo por cliente (R$)", "Observação / fonte"])
grav = [
    (22, METODOS[0], 0.5, 300, "[confirmar] marcador de latão: R$ 190 (5×5 cm) a R$ 450 (10×7,5 cm); elétrico R$ 299 a R$ 850. Prazo de uns 20 dias para chegar: arriscado para entregar até 18/12. Fontes em empresas-alvo.md, parte 3"),
    (23, METODOS[1], 6, 0, "[confirmar] mercado: R$ 2 a R$ 10 por peça em lote; logo 10×5 cm a R$ 0,13/cm² dá uns R$ 6,50. Parceiro em Paranavaí ou Maringá; some o frete. Fontes em empresas-alvo.md, parte 3"),
    (24, METODOS[2], 3, 0, "[confirmar] só se a MP tiver CNC. Custo = tempo de máquina e fresa em V"),
]
for r, m, c1, c2, obs in grav:
    label(p.cell(row=r, column=1), m)
    inp(p.cell(row=r, column=2), c1, BRL)
    inp(p.cell(row=r, column=3), c2, BRL)
    note(p.cell(row=r, column=4), obs)
label(p["A26"], "Custo por gravação do método escolhido", bold=True)
fx(p["B26"], "=INDEX(B22:B24,MATCH(B13,A22:A24,0))", BRL, bold=True)
label(p["A27"], "Custo fixo por cliente do método escolhido", bold=True)
fx(p["B27"], "=INDEX(C22:C24,MATCH(B13,A22:A24,0))", BRL, bold=True)

header(p, 29, ["Faixa de quantidade", "A partir de (peças)", "Margem líquida desejada", "Observação"])
faixas = [(30, "20 a 49", 20, 0.45), (31, "50 a 99", 50, 0.40), (32, "100 a 199", 100, 0.35), (33, "200 ou mais", 200, 0.30)]
for r, f, de, m in faixas:
    label(p.cell(row=r, column=1), f)
    inp(p.cell(row=r, column=2), de, "0")
    inp(p.cell(row=r, column=3), m, PCT, key=True)
note(p["D30"], "Margem depois de imposto e comissão. Pedido pequeno dá o mesmo trabalho de arte e atendimento, por isso margem maior")
note(p["D33"], "Nunca abaixo de 25%. Se precisar baixar o preço, corte tempo de mão de obra, não margem")
for col, w in zip("ABCD", (40, 22, 24, 90)):
    p.column_dimensions[col].width = w
for r in (22, 23, 24, 30, 33):
    p.row_dimensions[r].height = 30

dv_met = DataValidation(type="list", formula1="=$A$22:$A$24", allow_blank=False)
p.add_data_validation(dv_met)
dv_met.add("B13")

# ---------------------------------------------------------------- Custos
c = wb.create_sheet("Custos")
title(c, "Ficha e custo por peça", "Azul = entrada. Cronometre o protótipo e troque as horas pelo tempo real em lote.")
header(c, 4, ["Item"] + KITS + ["Unidade", "Observação / fonte"])
crow = [
    # (linha, rótulo, valores ou fórmula-modelo, unidade, formato, observação, chave)
    (5, "Descrição", ["Tábua de servir 35×22 cm", "Tábua de churrasco 45×30 cm com canaleta e alça de couro", "Estojo de madeira com tábua 45×30 cm, faca e garfo inox"], "", None, "", False),
    (6, "Comprimento", [35, 45, 45], "cm", "0.0", "Ajuste à bitola do retalho para não gerar perda", False),
    (7, "Largura", [22, 30, 30], "cm", "0.0", "", False),
    (8, "Espessura", [2.5, 3, 3], "cm", "0.0", "", False),
    (10, "Usa retalho?", ["SIM", "SIM", "SIM"], "SIM/NÃO", None, "[confirmar] se não houver retalho suficiente, troque para NÃO e a madeira entra pelo preço do m³", True),
    (12, "Lixas, cola e consumíveis", [3, 4, 5], "R$", BRL, "[confirmar] cola PVA D4 própria para contato indireto com alimento", False),
    (13, "Óleo mineral e cera de abelha", [1.5, 2.5, 2.5], "R$", BRL, "[confirmar] acabamento atóxico, 3 demãos, cura de 24 a 48 h", False),
    (14, "Alça de couro e rebites", [0, 4, 4], "R$", BRL, "[confirmar]", False),
    (15, "Gravações por peça", [1, 1, 2], "un", "0", "Premium grava a tábua e a tampa do estojo", False),
    (17, "Faca e garfo trinchante inox (comprados)", [0, 0, 45], "R$", BRL, "[confirmar cotação no atacado] conjunto inox 8\". Referência: faca, garfo e estojo sem tábua saem R$ 60 a R$ 85 em loja de brinde", True),
    (18, "Estojo de madeira com tampa corrediça (material)", [0, 0, 8], "R$", BRL, "[confirmar] pinus ou retalho; tempo de fazer está nas horas", False),
    (19, "Embalagem (caixa kraft ou saco de algodão, papel seda, fita)", [5, 7, 4], "R$", BRL, "[confirmar cotação]", False),
    (20, "Cartão com QR impresso", [0.8, 0.8, 0.8], "R$", BRL, "Gráfica rápida, 9×5 cm, frente e verso", False),
    (21, "Horas de mão de obra por peça (lote de 50)", [0.35, 0.6, 1.0], "h", "0.00", "[cronometrar no protótipo] corte, colagem, plaina, canaleta, lixa, óleo, embalagem", True),
]
for r, lab, vals, u, fmt, obs, key in crow:
    label(c.cell(row=r, column=1), lab)
    for i, v in enumerate(vals):
        cell = c.cell(row=r, column=2 + i)
        if r == 5:
            label(cell, v)
        else:
            inp(cell, v, fmt, key)
    label(c.cell(row=r, column=5), u)
    note(c.cell(row=r, column=6), obs)

for i, col in enumerate("BCD"):
    fx(c[f"{col}9"], f"={col}6*{col}7*{col}8/1000000", "0.0000")
    fx(c[f"{col}11"], f'=IF({col}10="SIM",0,{col}9*(1+Premissas!$B$7)*Premissas!$B$6)', BRL)
    fx(c[f"{col}16"], f"={col}15*Premissas!$B$26", BRL)
    fx(c[f"{col}22"], f"={col}21*Premissas!$B$5", BRL)
    fx(c[f"{col}23"], f"={col}11+SUM({col}12:{col}14)+{col}16+SUM({col}17:{col}20)+{col}22", BRL, bold=True)
for r, lab, u, obs in [
    (9, "Volume da tábua", "m³", "Comprimento × largura × espessura"),
    (11, "Madeira da tábua", "R$", "Zero quando usa retalho"),
    (16, "Gravação", "R$", "Gravações × custo do método escolhido em Premissas"),
    (22, "Mão de obra", "R$", "Horas × custo da hora de fábrica"),
    (23, "Custo direto por peça", "R$", "Soma de tudo acima. Não inclui imposto nem margem"),
]:
    label(c.cell(row=r, column=1), lab, bold=(r == 23))
    label(c.cell(row=r, column=5), u)
    note(c.cell(row=r, column=6), obs)

dv_sn = DataValidation(type="list", formula1='"SIM,NÃO"', allow_blank=False)
c.add_data_validation(dv_sn)
dv_sn.add("B10:D10")

header(c, 26, ["Ficha técnica"] + KITS + ["", ""])
ficha = [
    ("Madeira", ["Maciça densa sem tratamento químico, umidade até 12%. Tiras coladas de retalho, 1 ou 2 espécies", "Igual, 3 cm de espessura", "Igual; estojo em pinus ou retalho"]),
    ("Detalhe", ["Bordas arredondadas, furo para pendurar opcional", "Canaleta para o caldo a 2 cm da borda, fresa meia-cana de 10 mm; alça de couro rebitada", "Tábua do kit Churrasco; estojo com tampa corrediça e berço para faca e garfo"]),
    ("Acabamento", ["Lixa até grão 220, água para levantar a fibra, lixa de novo; óleo mineral em 3 demãos e cera de abelha", "Igual", "Igual na tábua; estojo com óleo ou cera"]),
    ("Gravação", ["Logo do cliente no canto, até 8 cm", "Logo do cliente centralizado no verso ou no canto, até 12 cm", "Logo na tampa do estojo e na tábua"]),
    ("Embalagem", ["Saco de algodão cru ou caixa kraft + cartão", "Caixa kraft com papel seda + cartão", "O próprio estojo, com cinta de papel + cartão"]),
    ("Nunca usar", ["Pinus ou eucalipto autoclavado, MDF ou compensado, verniz comum", "Idem", "Idem"]),
]
for i, (lab, vals) in enumerate(ficha, start=27):
    label(c.cell(row=i, column=1), lab, bold=True)
    for j, v in enumerate(vals):
        label(c.cell(row=i, column=2 + j), v)
    c.row_dimensions[i].height = 44
for col, w in zip("ABCDEF", (44, 30, 30, 30, 10, 70)):
    c.column_dimensions[col].width = w
c.row_dimensions[5].height = 44
c.freeze_panes = "B5"

# ---------------------------------------------------------------- Preços
pr = wb.create_sheet("Preços")
title(pr, "Tabela de preço por faixa", "Não digite aqui: tudo vem de Premissas e Custos. É esta tabela que vai para o catálogo.")
header(pr, 4, ["Faixa", ""] + [f[1] for f in faixas])
label(pr["A5"], "A partir de (peças)")
label(pr["A6"], "Margem líquida desejada")
for i, col in enumerate("CDEF"):
    r = 30 + i
    fx(pr[f"{col}4"], f"=Premissas!A{r}", link=True)
    pr[f"{col}4"].font = Font(name=F, bold=True, color="FFFFFF")
    pr[f"{col}4"].fill = HEAD
    fx(pr[f"{col}5"], f"=Premissas!B{r}", "0", link=True)
    fx(pr[f"{col}6"], f"=Premissas!C{r}", PCT, link=True)

header(pr, 8, ["Preço por peça (R$)", "Custo direto (R$)", "", "", "", ""])
header(pr, 13, ["Lucro líquido por peça (R$)", "", "", "", "", ""])
header(pr, 18, ["Margem líquida real", "", "", "", "", ""])
for k, kit in enumerate(KITS):
    r = 9 + k
    label(pr.cell(row=r, column=1), kit, bold=True)
    fx(pr.cell(row=r, column=2), f"=Custos!{'BCD'[k]}23", BRL, link=True)
    label(pr.cell(row=14 + k, column=1), kit)
    label(pr.cell(row=19 + k, column=1), kit)
    for col in "CDEF":
        fx(pr[f"{col}{r}"],
           f"=ROUNDUP($B{r}/(1-Premissas!$B$8-Premissas!$B$9-{col}$6)/5,0)*5-0.1", BRL, bold=True)
        fx(pr[f"{col}{14 + k}"], f"={col}{r}*(1-Premissas!$B$8-Premissas!$B$9)-$B{r}", BRL)
        fx(pr[f"{col}{19 + k}"], f"=IF({col}{r}>0,{col}{14 + k}/{col}{r},0)", PCT)
label(pr["A24"], "Taxa de personalização", bold=True)
fx(pr["B24"],
   '="R$ "&TEXT(Premissas!B11,"0")&" por pedido abaixo de "&Premissas!B12&" peças; isenta a partir de "&Premissas!B12&"."')
pr.merge_cells("B24:F24")
note(pr["A25"], "O lucro por peça não desconta o custo fixo do ferro de marcar; a aba Pedidos desconta, pedido a pedido.")
pr.merge_cells("A25:F25")
for col, w in zip("ABCDEF", (30, 18, 16, 16, 16, 16)):
    pr.column_dimensions[col].width = w

# ---------------------------------------------------------------- Pedidos
pe = wb.create_sheet("Pedidos")
title(pe, "Pedidos e capacidade da fábrica",
      "Uma linha por kit. Cliente que mistura kits usa uma linha para cada kit, com o mesmo nome: a faixa conta o total de peças do cliente e a taxa sai uma vez só. Digite só as colunas azuis (A a F e P). A linha 13 é um exemplo: apague quando lançar o primeiro pedido real.")
FIRST, LAST = 13, 112
rng = lambda col: f"${col}${FIRST}:${col}${LAST}"
fechados = ["Fechado", "Em produção", "Entregue"]


def soma(col, status_list):
    return "+".join(f'SUMIFS({rng(col)},{rng("P")},"{s}")' for s in status_list)


resumo = [
    (3, "Horas de fábrica disponíveis", "=Premissas!B18", "0", True),
    (4, "Horas em pedidos fechados", "=" + soma("O", fechados), "0", False),
    (5, "Horas em propostas abertas", "=" + soma("O", ["Proposta enviada"]), "0", False),
    (6, "Saldo de horas", "=B3-B4", "0", False),
    (7, "Ocupação da fábrica", "=IF(B3>0,B4/B3,0)", PCT, False),
    (8, "Kits Churrasco que ainda cabem", "=IF(Custos!C21>0,INT(MAX(B6,0)/Custos!C21),0)", "0", False),
    (9, "Faturamento fechado", "=" + soma("K", fechados), BRL, False),
    (10, "Lucro estimado fechado", "=" + soma("N", fechados), BRL, False),
]
for r, lab, f, fmt, link in resumo:
    label(pe.cell(row=r, column=1), lab, bold=True)
    fx(pe.cell(row=r, column=2), f, fmt, link=link, bold=True)
note(pe["C7"], "Acima de 80%: pare de aceitar pedido grande ou aumente as horas em Premissas")
note(pe["C5"], "Se todas as propostas fecharem, somam-se a estas horas")
pe.conditional_formatting.add("B7", CellIsRule(operator="greaterThan", formula=["0.8"],
                                               fill=PatternFill("solid", start_color="F4B6B6")))
pe.conditional_formatting.add("B6", CellIsRule(operator="lessThan", formula=["0"],
                                               fill=PatternFill("solid", start_color="F4B6B6")))

cols = ["Cliente", "Cidade", "Contato (nome e WhatsApp do decisor)", "Kit", "Quantidade", "Entrega",
        "Faixa (total do cliente)", "Preço por peça", "Subtotal", "Taxa de personalização", "Total do pedido", "Sinal",
        "Custo direto total", "Lucro estimado", "Horas de fábrica", "Status"]
header(pe, 12, cols)
pe.row_dimensions[12].height = 32
for r in range(FIRST, LAST + 1):
    for col in "ABCDEF":
        cell = pe[f"{col}{r}"]
        font(cell, color=BLUE)
        cell.border = BOX
    pe[f"E{r}"].number_format = "0"
    pe[f"F{r}"].number_format = DATE
    font(pe[f"P{r}"], color=BLUE)
    pe[f"P{r}"].border = BOX
    k = f"$D{r}"
    q = f"$E{r}"
    # total de peças do mesmo cliente (sem as linhas perdidas): é ele que define a faixa
    t = (f'IF($A{r}="",{q},SUMIFS($E${FIRST}:$E${LAST},$A${FIRST}:$A${LAST},$A{r},'
         f'$P${FIRST}:$P${LAST},"<>Perdido"))')
    fx(pe[f"G{r}"], f'=IF(OR({k}="",{q}=""),"",IF({t}<Premissas!$B$10,"abaixo do mínimo",'
                    f'INDEX(Premissas!$A$30:$A$33,MATCH({t},Premissas!$B$30:$B$33,1))))')
    fx(pe[f"H{r}"], f'=IF(OR(G{r}="",G{r}="abaixo do mínimo"),"",'
                    f'INDEX(Preços!$C$9:$F$11,MATCH({k},Preços!$A$9:$A$11,0),MATCH({t},Preços!$C$5:$F$5,1)))', BRL)
    fx(pe[f"I{r}"], f'=IF(H{r}="","",H{r}*{q})', BRL)
    fx(pe[f"J{r}"], f'=IF(H{r}="","",IF(OR({t}>=Premissas!$B$12,AND($A{r}<>"",COUNTIF($A${FIRST}:$A{r},$A{r})>1)),0,Premissas!$B$11))', BRL)
    fx(pe[f"K{r}"], f'=IF(H{r}="","",I{r}+J{r})', BRL)
    fx(pe[f"L{r}"], f'=IF(K{r}="","",K{r}*Premissas!$B$19)', BRL)
    fx(pe[f"M{r}"], f'=IF(H{r}="","",INDEX(Custos!$B$23:$D$23,MATCH({k},Custos!$B$4:$D$4,0))*{q})', BRL)
    fx(pe[f"N{r}"], f'=IF(K{r}="","",K{r}*(1-Premissas!$B$8-Premissas!$B$9)-M{r}-IF(AND($A{r}<>"",COUNTIF($A${FIRST}:$A{r},$A{r})>1),0,Premissas!$B$27))', BRL)
    fx(pe[f"O{r}"], f'=IF(H{r}="","",INDEX(Custos!$B$21:$D$21,MATCH({k},Custos!$B$4:$D$4,0))*{q})', "0.0")

ex = ["EXEMPLO: apague esta linha", "Paranavaí", "nome e WhatsApp de quem decide", "Churrasco", 120,
      dt.date(2026, 12, 14)]
for col, v in zip("ABCDEF", ex):
    pe[f"{col}{FIRST}"].value = v
    pe[f"{col}{FIRST}"].fill = SOFT
pe[f"P{FIRST}"].value = "Proposta enviada"
pe[f"P{FIRST}"].fill = SOFT
pe[f"A{FIRST}"].comment = Comment("Linha de exemplo com valores fictícios para mostrar o formato. Apague antes de usar.", "MP")

dv_kit = DataValidation(type="list", formula1=f'"{",".join(KITS)}"', allow_blank=True)
dv_st = DataValidation(type="list", formula1=f'"{",".join(STATUS)}"', allow_blank=True)
pe.add_data_validation(dv_kit)
pe.add_data_validation(dv_st)
dv_kit.add(f"D{FIRST}:D{LAST}")
dv_st.add(f"P{FIRST}:P{LAST}")
widths = (30, 16, 30, 12, 11, 12, 16, 14, 14, 14, 15, 13, 15, 15, 11, 18)
for i, w in enumerate(widths):
    pe.column_dimensions[chr(65 + i)].width = w
pe.column_dimensions["A"].width = 34
pe.freeze_panes = "B13"

for sheet in wb.worksheets:
    sheet.sheet_view.showGridLines = False
    for row in sheet.iter_rows():
        for cell in row:
            if cell.font and cell.font.name != F:
                cell.font = Font(name=F, size=cell.font.size or 10, bold=cell.font.bold,
                                 italic=cell.font.italic, color=cell.font.color)

wb.save(OUT)
print("ok", OUT)
