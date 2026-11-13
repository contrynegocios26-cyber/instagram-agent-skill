#!/usr/bin/env python3
"""Catalogos impressos da linha agricola da Jardmolas (HTML pronto para virar PDF A4).

Gera dois arquivos:
  catalogo-tecnico.html       detalhado: onde vai cada mola, por implemento
  catalogo-apresentacao.html  8 paginas, para imprimir e entregar ao cliente

Uso:
  python impressos.py --fotos PASTA_FOTOS --saida PASTA [--whatsapp 55DDDNUMERO]
        [--telefone "(16) 0000-0000"] [--email x@y] [--site jardmolas.com.br]
        [--endereco "..."] [--sangria 3] [--data mm/aaaa]
Depois: python pdf.py PASTA   (ou abrir o HTML no navegador e imprimir em PDF, A4, sem margens)

As posicoes vem de assets/aplicacoes-agro.json. Nenhuma medida e inventada: o catalogo
tecnico traz colunas de codigo e medidas em branco para o cadastro dos itens.
"""
import argparse
import base64
import html
import io
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
TIPO = {"compressao": "Compressão", "tracao": "Tração", "torcao": "Torção", "dedo": "Dedo",
        "garfo": "Garfo / dente", "outros": "Especial"}
E = html.escape


def b64(caminho):
    ext = caminho.rsplit(".", 1)[-1].lower()
    with open(caminho, "rb") as f:
        return "data:image/%s;base64,%s" % ("png" if ext == "png" else "jpeg", base64.b64encode(f.read()).decode())


class Fotos:
    def __init__(self, pasta):
        self.pasta = pasta

    def uma(self, nome):
        for ext in ("jpg", "png"):
            c = os.path.join(self.pasta, "%s.%s" % (nome, ext))
            if os.path.exists(c):
                return b64(c)
        return ""

    def serie(self, prefixo, n=8):
        return [x for x in (self.uma("%s-%d" % (prefixo, i)) for i in range(1, n + 1)) if x]


def qr(texto):
    try:
        import qrcode
    except ImportError:
        return ""
    img = qrcode.make(texto, box_size=8, border=1)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = """
@page{size:%(pw)smm %(ph)smm;margin:0}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font:11.5pt/1.45 Inter,"DejaVu Sans",Arial,sans-serif;color:#1d2320}
:root{--verde:#0b5a1e;--verde2:#2c9a45;--amarelo:#ffd800;--tinta:#1d2320;--cinza:#5b665f;--linha:#cfd6d0;--fundo:#f3f5f2}
.pg{width:%(pw)smm;height:%(ph)smm;padding:%(mt)smm %(ml)smm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
h1,h2,h3{font-family:"Inter Display",Inter,Arial,sans-serif;margin:0;line-height:1.12}
h2{font-size:24pt;font-weight:800;color:var(--verde)}
h3{font-size:13.5pt;font-weight:700;margin:6mm 0 2mm}
p{margin:0 0 2.2mm}
.olho{font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--verde2);margin-bottom:1.5mm}
.faixa{display:inline-block;width:14mm;height:2.2mm;background:var(--amarelo);margin-bottom:3mm}
.rodape{position:absolute;left:%(ml)smm;right:%(ml)smm;bottom:%(mb)smm;display:flex;justify-content:space-between;font-size:8pt;color:var(--cinza);border-top:.3mm solid var(--linha);padding-top:1.5mm}
table{border-collapse:collapse;width:100%%;font-size:10pt;line-height:1.32}
th{background:var(--verde);color:#fff;text-align:left;padding:2mm 2mm;font-weight:600;font-size:8.8pt}
td{padding:2.3mm 2mm;border-bottom:.2mm solid var(--linha);vertical-align:top}
tr{page-break-inside:avoid}
.tag{display:inline-block;font-size:8pt;font-weight:700;padding:.3mm 1.6mm;border-radius:2mm;white-space:nowrap}
.tag.l{background:var(--verde2);color:#fff}.tag.s{background:#e6ebe6;color:#3b4640}
.branco{border-bottom:.2mm solid #9aa59e;height:6mm}
.pg.col{display:flex;flex-direction:column}
.notas{flex:1;min-height:0;margin-top:7mm;margin-bottom:12mm;display:flex;flex-direction:column}
.notas .t{font-size:8.8pt;font-weight:600;background:#e6ebe6;padding:2mm;display:grid;grid-template-columns:16%% 34%% 30%% 20%%}
.notas .l{flex:1;background:repeating-linear-gradient(#fff 0,#fff 8.6mm,#aab4ad 8.6mm,#aab4ad 8.85mm)}
.grade{display:grid;gap:3mm}
.foto{background:#fff;border:.25mm solid var(--linha);border-radius:1.5mm;display:flex;align-items:center;justify-content:center;overflow:hidden}
.foto img{max-width:100%%;max-height:100%%;object-fit:contain;display:block}
.amb{width:100%%;object-fit:cover;display:block;border-radius:1.5mm}
.capa{padding:0;background:var(--verde);color:#fff}
.capa .img{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.42}
.capa .cont{position:absolute;left:%(ml)smm;right:%(ml)smm;bottom:%(mc)smm}
.capa h1{font-size:46pt;font-weight:800;letter-spacing:-.01em}
.capa .sub{font-size:15pt;max-width:120mm;margin-top:4mm;opacity:.95}
.capa .logo{position:absolute;top:%(mc)smm;left:%(ml)smm;background:#fff;border-radius:2mm;padding:3mm 4mm}
.capa .logo img{height:22mm;display:block}
.capa .ed{position:absolute;top:%(mc)smm;right:%(ml)smm;font-size:8pt;letter-spacing:.14em;text-transform:uppercase;font-weight:700;text-align:right}
.num{font:800 34pt/1 "Inter Display",Inter,Arial;color:var(--verde)}
.cx{background:var(--fundo);border-radius:2mm;padding:4mm}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:7mm}
ul{margin:0 0 2mm;padding-left:4.5mm}li{margin-bottom:1mm}
.campo{display:flex;gap:2mm;align-items:flex-end;margin-bottom:5mm;font-size:10pt}
.campo span{white-space:nowrap}.campo i{flex:1;border-bottom:.25mm solid #7d8a82;height:4mm}
"""


def pagina(conteudo, rodape="", classe=""):
    return '<section class="pg %s">%s%s</section>' % (
        classe, conteudo, '<div class="rodape">%s</div>' % rodape if rodape else "")


def grade_fotos(fotos, colunas, altura):
    return '<div class="grade" style="grid-template-columns:repeat(%d,1fr)">%s</div>' % (colunas, "".join(
        '<div class="foto" style="height:%smm"><img src="%s" alt=""></div>' % (altura, f) for f in fotos))


def tabela_maquina(m, tecnico=True):
    cab = ("<tr><th style='width:23%'>Onde vai na máquina</th><th style='width:24%'>Peça</th><th style='width:9%'>Tipo</th>"
           "<th>Função</th><th style='width:11%'>Fornecimento</th>" +
           ("<th style='width:11%'>Código JM</th>" if tecnico else "") + "</tr>")
    linhas = "".join(
        "<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td><span class='tag %s'>%s</span></td>%s</tr>" % (
            E(l[0]), E(l[1]), E(TIPO.get(l[2], l[2])), E(l[3]), "l" if l[4] == "linha" else "s",
            "Linha" if l[4] == "linha" else "Sob medida", "<td><div class='branco'></div></td>" if tecnico else "")
        for l in m["linhas"])
    return "<h3>%s</h3><table>%s%s</table>" % (E(m["nome"]), cab, linhas)


def tecnico(d, F, c):
    rod = "<span>Jardmolas · Catálogo técnico de molas para implementos agrícolas · %s</span><span>%s</span>" % (
        E(c["data"]), E(c["site"]))
    P = []
    P.append(pagina(
        '<div class="img" style="background-image:url(%s)"></div><div class="logo"><img src="%s" alt="Jardmolas"></div>'
        '<div class="ed">Catálogo técnico<br>Linha agrícola · %s</div><div class="cont"><span class="faixa"></span>'
        '<h1>Molas para implementos agrícolas</h1><p class="sub">Onde vai cada mola, implemento por implemento: '
        'posição na máquina, tipo de peça, função e o que informar para pedir.</p></div>' % (
            F.uma("amb-ancinho-1"), F.uma("logo"), E(c["data"])), classe="capa"))
    total = sum(len(m["linhas"]) for g in d["grupos"] for m in g["maquinas"])
    indice = "".join("<tr><td><b>%s</b></td><td>%s</td></tr>" % (
        E(g["nome"]), E(" · ".join(m["nome"] for m in g["maquinas"]))) for g in d["grupos"])
    P.append(pagina(
        '<div class="olho">Como usar</div><h2>Do implemento à mola certa</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<div class="cols2"><div><p>Este catálogo está organizado como o produtor e o mecânico pensam: pela máquina. '
        'Em cada implemento, a tabela mostra <b>onde a mola vai</b>, que peça é, para que serve e como a Jardmolas a fornece.</p>'
        '<p><span class="tag l">Linha</span> família fabricada em série pela Jardmolas — consulte o modelo da sua máquina.<br>'
        '<span class="tag s">Sob medida</span> fabricada por desenho ou por amostra, em qualquer quantidade.</p>'
        '<p>A coluna <b>Código JM</b> fica em branco para o vendedor anotar o item cadastrado para a máquina do cliente.</p></div>'
        '<div class="cx"><b>Para pedir, informe:</b><ul><li>máquina, marca e modelo, e a posição da mola nela;</li>'
        '<li>diâmetro do arame, diâmetro externo e comprimento;</li><li>número de espiras e formato das pontas, ganchos ou pernas;</li>'
        '<li>código gravado na peça ou do manual, se houver;</li><li>quantidade.</li></ul>'
        '<b>Sem a peça original?</b> Envie uma foto ao lado de uma régua pelo WhatsApp %s.</div></div>'
        '<h3>Conteúdo — %d implementos, %d posições de mola</h3><table><tr><th style="width:30%%">Grupo</th><th>Implementos</th></tr>%s</table>' % (
            E(c["telefone_zap"]), sum(len(g["maquinas"]) for g in d["grupos"]), total, indice), rod))
    # tipos de peca, com fotos reais
    blocos = [("Dedos enleiradores de palha", "enleirador", 8), ("Dedos desenleiradores de palha", "desenleirador", 8),
              ("Garfos e dentes para fenação", "feno", 8), ("Molas de compressão", "compressao", 8),
              ("Molas de tração", "tracao", 5), ("Molas de torção, capim e atuadores", None, 0)]
    for i in range(0, len(blocos), 3):
        corpo = '<div class="olho">Peças</div><h2>%s</h2><span class="faixa" style="margin-top:3mm"></span>' % (
            "As famílias de peças" if i == 0 else "As famílias de peças (continuação)")
        for titulo, pre, n in blocos[i:i + 3]:
            fs = F.serie(pre, n) if pre else F.serie("torcao", 1) + F.serie("capim", 2) + F.serie("atuador", 4)
            corpo += "<h3>%s</h3>%s" % (E(titulo), grade_fotos(fs[:8], 4, 28))
        corpo += '<p style="font-size:8pt;color:var(--cinza);margin-top:3mm">Fotos de peças fabricadas pela Jardmolas. Formas e medidas variam conforme a máquina: a peça é identificada pelo modelo do implemento ou pela amostra.</p>'
        P.append(pagina(corpo, rod))
    # grupos: quebra em paginas por altura estimada
    for g in d["grupos"]:
        cab = '<div class="olho">Onde vai cada mola</div><h2>%s</h2><span class="faixa" style="margin-top:3mm"></span><p>%s</p>' % (
            E(g["nome"]), E(g["intro"]))
        atual, alt = cab, 48
        for m in g["maquinas"]:
            h = 22 + sum(10 + 4.6 * max(len(l[1]) // 22, len(l[3]) // 26, len(l[0]) // 20) for l in m["linhas"])
            if alt + h > 240:
                P.append(pagina(atual, rod))
                atual, alt = '<div class="olho">Onde vai cada mola</div><h2>%s (continuação)</h2><span class="faixa" style="margin-top:3mm"></span>' % E(g["nome"]), 26
            atual += tabela_maquina(m)
            alt += h
        notas = ('<div class="notas"><div class="t"><span>Código JM</span><span>Descrição</span><span>Arame × diâmetro × comprimento</span>'
                 '<span>Máquina / modelo</span></div><div class="l"></div></div>') if alt < 200 else ""
        P.append(pagina(atual + notas, rod, "col"))
    comp = "".join("<tr><td><b>%s</b></td><td>%s</td></tr>" % (E(k), E(" · ".join(v))) for k, v in d["compat_feno"].items())
    P.append(pagina(
        '<div class="olho">Fenação</div><h2>Compatibilidade de garfos e dentes</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<p>Garfos e molas de reposição para uso nas máquinas abaixo. Informe o modelo e a posição do garfo (braço interno ou externo) para receber o item certo.</p>'
        '<table><tr><th style="width:22%%">Marca</th><th>Modelos</th></tr>%s</table>'
        '<p style="font-size:8pt;color:var(--cinza);margin-top:2mm">Marcas e modelos são citados só para indicar em que equipamento a peça pode ser usada; pertencem aos respectivos fabricantes. Não encontrou seu modelo? Fabricamos por amostra.</p>'
        '<h3 style="margin-top:8mm">Materiais e acabamentos</h3><table><tr><th style="width:30%%">Material</th><th>Onde entra</th><th style="width:26%%">Proteção usual</th></tr>'
        '<tr><td><b>Arame patenteado de alto carbono</b><br>EN 10270-1 (antiga DIN 17223)</td><td>Dedos, garfos, molas de tração e de compressão de arame fino e médio</td><td>Oleado, pintado ou zincado</td></tr>'
        '<tr><td><b>SAE 9254</b> — cromo-silício</td><td>Molas de linha de plantio e de desarme: choque e fadiga</td><td>Pintura</td></tr>'
        '<tr><td><b>SAE 6150</b> — cromo-vanádio</td><td>Molas de alta solicitação</td><td>Pintura</td></tr>'
        '<tr><td><b>SAE 5160</b> — cromo, alto carbono</td><td>Molas pesadas de barra</td><td>Pintura</td></tr>'
        '<tr><td><b>SAE 1070</b></td><td>Molas de uso geral</td><td>Oleado, pintado ou zincado</td></tr>'
        '<tr><td><b>Inox 302/304</b></td><td>Contato com calda, fertilizante e umidade</td><td>—</td></tr></table>' % comp, rod))
    P.append(pagina(
        '<div class="olho">Guia</div><h2>Como medir sua mola</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<p>Use paquímetro e meça a peça menos gasta. Mola usada costuma estar mais curta que a nova: informe sempre a máquina.</p>'
        '<div class="cols2"><div><h3>Compressão</h3><ul><li>Diâmetro do arame.</li><li>Diâmetro externo, no meio da mola.</li><li>Comprimento livre, sem carga.</li><li>Número total de espiras.</li><li>Pontas: fechadas? retificadas (planas)?</li></ul>'
        '<h3>Tração</h3><ul><li>Arame e diâmetro externo do corpo.</li><li>Comprimento do corpo (só as espiras).</li><li>Comprimento por dentro dos ganchos.</li><li>Tipo de gancho e posição entre eles.</li></ul></div>'
        '<div><h3>Torção</h3><ul><li>Arame e diâmetro interno (ou o do eixo).</li><li>Número de espiras.</li><li>Comprimento de cada perna, a partir do centro.</li><li>Ângulo entre as pernas com a mola solta.</li><li>Sentido: direita ou esquerda.</li></ul>'
        '<h3>Dedos e garfos</h3><ul><li>Marca e modelo da máquina e posição do dedo.</li><li>Diâmetro do arame.</li><li>Comprimento total e da haste reta.</li><li>Diâmetro e número de espiras; simples ou duplo.</li><li>Fixação: olhal, gancho ou parafuso.</li></ul></div></div>'
        '<h3 style="margin-top:6mm">Ficha de pedido</h3><div class="cx">' + "".join(
            '<div class="campo"><span>%s</span><i></i></div>' % t for t in (
                "Cliente / fazenda / usina:", "Máquina, marca e modelo:", "Posição da mola na máquina:",
                "Tipo de peça:", "Arame (mm):  ________   Diâmetro externo (mm):  ________   Comprimento (mm):",
                "Espiras:  ________   Pontas / ganchos / pernas:", "Código original ou gravado na peça:",
                "Quantidade:  ________   Prazo desejado:")) + '</div>', rod))
    P.append(contracapa(F, c, "Peça pela máquina, pelas medidas ou pela amostra."))
    return P


def contracapa(F, c, frase):
    q = qr("https://wa.me/" + c["whatsapp"]) if c["whatsapp"] else ""
    return pagina(
        '<div class="cont" style="bottom:auto;top:%smm"><div style="background:#fff;border-radius:2mm;padding:3mm 4mm;display:inline-block"><img src="%s" style="height:24mm;display:block" alt="Jardmolas"></div>'
        '<h1 style="font-size:26pt;margin-top:14mm;max-width:150mm">%s</h1><span class="faixa" style="margin-top:6mm"></span>'
        '<div style="display:flex;gap:10mm;align-items:flex-end;margin-top:8mm"><div style="font-size:12pt;line-height:1.7">'
        '%s%s%s%s%s</div>%s</div></div>' % (
            c["mc_num"], F.uma("logo"), E(frase),
            "<b>WhatsApp</b> %s<br>" % E(c["telefone_zap"]) if c["telefone_zap"] else "",
            "<b>Telefone</b> %s<br>" % E(c["telefone"]) if c["telefone"] else "",
            "<b>E-mail</b> %s<br>" % E(c["email"]) if c["email"] else "",
            "<b>Site</b> %s<br>" % E(c["site"]) if c["site"] else "",
            E(c["endereco"]),
            '<div style="background:#fff;padding:2.5mm;border-radius:2mm;text-align:center;color:#1d2320;font-size:7.5pt"><img src="%s" style="width:30mm;display:block"><b>Peça pelo WhatsApp</b></div>' % q if q else ""),
        classe="capa")


def apresentacao(d, F, c):
    rod = "<span>Jardmolas · Molas para implementos agrícolas</span><span>%s</span>" % E(c["site"])
    P = []
    P.append(pagina(
        '<div class="img" style="background-image:url(%s);opacity:.5"></div><div class="logo"><img src="%s" alt="Jardmolas"></div>'
        '<div class="ed">Linha agrícola</div><div class="cont"><span class="faixa"></span>'
        '<h1>Molas que aguentam a safra</h1><p class="sub">Dedos, garfos e molas para implementos agrícolas. '
        'Fabricados em Jardinópolis-SP desde 2008.</p></div>' % (F.uma("amb-feno-1"), F.uma("logo")), classe="capa"))
    P.append(pagina(
        '<div class="olho">A Jardmolas</div><h2>Fábrica de molas no coração do polo canavieiro</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<div class="cols2"><div><p style="font-size:13pt">Fabricamos molas originais e de reposição para implementos agrícolas e para a indústria, '
        'sob desenho ou a partir da peça que você tem na mão.</p>'
        '<p>No campo, mola e dedo são peças de desgaste: quando quebram, a máquina para no meio da janela de plantio ou de colheita. '
        'Por isso trabalhamos com arame de procedência certificada, tratamento térmico controlado e itens de giro em estoque antes da safra.</p></div>'
        '<div><img class="amb" style="height:74mm" src="%s" alt=""></div></div>'
        '<div class="grade" style="grid-template-columns:repeat(3,1fr);margin-top:8mm">'
        '<div class="cx"><div class="num">2008</div>ano de fundação, em Jardinópolis-SP</div>'
        '<div class="cx"><div class="num">+2.000</div>itens no catálogo de reposição</div>'
        '<div class="cx"><div class="num">Brasil</div>atendimento em todo o país, direto e por representantes</div></div>'
        '<h3 style="margin-top:8mm">O que fabricamos para o campo</h3>'
        '<div class="cols2"><ul><li>Dedos enleiradores e desenleiradores de palha de cana</li><li>Garfos e dentes para enleiradores, espalhadores e enfardadeiras de feno</li>'
        '<li>Molas para colheita de sementes de capim e de amendoim</li></ul><ul><li>Molas de compressão, tração e torção para plantadeiras, subsoladores, cultivadores e colheitadeiras</li>'
        '<li>Molas para atuadores, carretas canavieiras e usinas</li><li>Qualquer mola sob medida</li></ul></div>' % F.uma("amb-plantio-1"), rod))
    P.append(pagina(
        '<div class="olho">Palha de cana</div><h2>Dedos enleiradores e desenleiradores</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<div class="cols2"><div><p style="font-size:13pt">Nossa linha mais conhecida. O dedo trabalha raspando o solo, batendo em toco e pedra, hora após hora.</p>'
        '<ul><li>Arame patenteado de alto carbono, com certificado do fabricante</li><li>Alívio de tensões controlado: é o que faz o dedo durar a safra</li>'
        '<li>Modelos para os principais enleiradores e desenleiradores do mercado, e sob amostra</li></ul></div>'
        '<div><img class="amb" style="height:52mm" src="%s" alt=""></div></div><h3>Enleiradores</h3>%s<h3>Desenleiradores</h3>%s' % (
            F.uma("amb-cana-1"), grade_fotos(F.serie("enleirador", 8), 4, 36), grade_fotos(F.serie("desenleirador", 8)[:4], 4, 36)), rod))
    comp = " · ".join("%s %s" % (k, ", ".join(v)) for k, v in d["compat_feno"].items())
    P.append(pagina(
        '<div class="olho">Fenação</div><h2>Garfos e dentes para feno</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<div class="cols2"><div><p style="font-size:13pt">Garfos retos, curvos e duplos para enleiradores, espalhadores e enfardadeiras.</p>'
        '<p>Troque em jogo antes da safra de feno: garfo cansado deixa capim no chão e sobrecarrega os vizinhos.</p></div>'
        '<div><img class="amb" style="height:46mm" src="%s" alt=""></div></div>%s'
        '<div class="cx" style="margin-top:5mm"><b>Para uso em:</b> %s.<br><span style="font-size:8pt;color:var(--cinza)">Marcas e modelos citados só para indicar em que equipamento a peça pode ser usada; pertencem aos respectivos fabricantes.</span></div>' % (
            F.uma("amb-ancinho-1"), grade_fotos(F.serie("feno", 8), 4, 50), E(comp)), rod))
    P.append(pagina(
        '<div class="olho">Plantio, solo e colheita</div><h2>Molas de compressão, tração e torção</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<div class="cols2"><div><p style="font-size:13pt">A pressão da linha de plantio, o desarme da haste do subsolador, a tensão da correia da colheitadeira: tudo depende de uma mola com a carga certa.</p></div>'
        '<div><img class="amb" style="height:40mm" src="%s" alt=""></div></div>'
        '<h3>Compressão</h3>%s<h3>Tração</h3>%s<h3>Torção, capim e atuadores</h3>%s' % (
            F.uma("amb-solo-1"), grade_fotos(F.serie("compressao", 8)[:4], 4, 42), grade_fotos(F.serie("tracao", 5)[:4], 4, 42),
            grade_fotos((F.serie("torcao", 1) + F.serie("capim", 2) + F.serie("atuador", 4))[:4], 4, 42)), rod))
    resumo = "".join("<tr><td><b>%s</b></td><td>%s</td></tr>" % (
        E(g["nome"]), E("; ".join("%s: %s" % (m["nome"], ", ".join(sorted({l[0].split(" (")[0].lower() for l in m["linhas"]}))) for m in g["maquinas"])))
        for g in d["grupos"])
    P.append(pagina(
        '<div class="olho">Guia rápido</div><h2>Onde vai cada mola</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<p>Um resumo por implemento. O catálogo técnico traz a tabela completa, com tipo de peça e função em cada posição.</p>'
        '<table><tr><th style="width:24%%">Implemento</th><th>Posições que levam mola</th></tr>%s</table>' % resumo, rod))
    P.append(pagina(
        '<div class="olho">Sob medida</div><h2>Não achou? Fabricamos pela sua amostra</h2><span class="faixa" style="margin-top:3mm"></span>'
        '<div class="cols2"><div><p style="font-size:13pt">Traga a peça, o desenho ou só as medidas. Fabricamos a partir de uma unidade.</p>'
        '<h3>Como pedir</h3><ol style="padding-left:5mm;margin:0"><li style="margin-bottom:2mm"><b>Diga a máquina:</b> marca, modelo e onde a mola vai.</li>'
        '<li style="margin-bottom:2mm"><b>Meça ou fotografe:</b> arame, diâmetro, comprimento e espiras — ou mande foto ao lado de uma régua.</li>'
        '<li style="margin-bottom:2mm"><b>Informe a quantidade</b> e receba prazo e preço.</li></ol></div>'
        '<div class="cx"><b>Materiais</b><ul><li>Arame patenteado de alto carbono (EN 10270-1)</li><li>SAE 1070, 5160, 6150 e 9254</li><li>Inox 302/304 para calda e fertilizante</li></ul>'
        '<b>O que acompanha</b><ul><li>Certificado do arame</li><li>Laudo do lote quando solicitado</li><li>Identificação por lote na embalagem</li></ul></div></div>'
        '<img class="amb" style="height:92mm;margin-top:8mm" src="%s" alt="">' % F.uma("amb-tracao-1"), rod))
    P.append(contracapa(F, c, "Sua máquina não pode parar na safra. Fale com a fábrica."))
    return P


def documento(titulo, paginas, medidas):
    return ("<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>%s</title><style>%s</style></head><body>%s</body></html>"
            % (E(titulo), CSS % medidas, "".join(paginas)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fotos", required=True)
    p.add_argument("--saida", required=True)
    p.add_argument("--whatsapp", default="")
    p.add_argument("--telefone", default="")
    p.add_argument("--email", default="")
    p.add_argument("--site", default="jardmolas.com.br")
    p.add_argument("--endereco", default="Distrito Industrial I · Jardinópolis-SP")
    p.add_argument("--sangria", type=float, default=0, help="sangria em mm para grafica (0 = A4 exato)")
    p.add_argument("--data", default="")
    a = p.parse_args()
    with open(os.path.join(AQUI, "..", "assets", "aplicacoes-agro.json"), encoding="utf-8") as f:
        d = json.load(f)
    F = Fotos(a.fotos)
    z = "".join(ch for ch in a.whatsapp if ch.isdigit())
    zap_fmt = "(%s) %s-%s" % (z[2:4], z[4:9], z[9:]) if len(z) == 13 else a.whatsapp
    s = a.sangria
    med = {"pw": 210 + 2 * s, "ph": 297 + 2 * s, "mt": 16 + s, "ml": 15 + s, "mb": 9 + s, "mc": 20 + s}
    c = {"whatsapp": z, "telefone_zap": zap_fmt, "telefone": a.telefone, "email": a.email, "site": a.site,
         "endereco": a.endereco, "data": a.data, "mc_num": 30 + s}
    os.makedirs(a.saida, exist_ok=True)
    suf = "-sangria" if s else ""
    for nome, titulo, pags in (("catalogo-tecnico", "Catálogo técnico Jardmolas — linha agrícola", tecnico(d, F, c)),
                               ("catalogo-apresentacao", "Jardmolas — linha agrícola", apresentacao(d, F, c))):
        caminho = os.path.join(a.saida, nome + suf + ".html")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(documento(titulo, pags, med))
        print("%s: %d paginas" % (caminho, len(pags)))


if __name__ == "__main__":
    main()
