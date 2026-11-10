#!/usr/bin/env python3
"""Gera o catálogo da MP Marcenaria em PDF a partir de um catalogo.json.

Uso:
    python3 catalogo.py catalogo.json                 # PDF digital (tela, WhatsApp)
    python3 catalogo.py catalogo.json --impressao     # PDF para gráfica, com sangria de 3 mm
    python3 catalogo.py catalogo.json --conferir      # só valida, não gera
    python3 catalogo.py catalogo.json --final         # falha se houver pendência

Dependências: reportlab e Pillow.

Foto que não existe vira um quadro cinza com o nome do arquivo, para o boneco
do catálogo poder ser aprovado antes de as fotos chegarem. O relatório no fim
lista tudo que falta. Com --final, qualquer pendência impede a geração.
"""
import argparse
import io
import json
import math
import os
import re
import sys

from PIL import Image, ImageOps
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FORMATOS = {"paisagem": (297 * mm, 210 * mm), "retrato": (210 * mm, 297 * mm)}
SANGRIA = 3 * mm
PENDENTE = re.compile(r"\[(confirmar|preencher)[^\]]*\]|\{\{.*?\}\}", re.I)
FONTES_PADRAO = [
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]
TIPOS = {"capa", "texto", "indice", "abertura", "projeto", "produtos",
         "processo", "materiais", "depoimento", "contato"}


class Catalogo:
    def __init__(self, dados, base, saida, impressao=False):
        self.d = dados
        self.base = base
        self.impressao = impressao
        self.marca = dados.get("marca", {})
        self.cfg = dados.get("catalogo", {})
        self.paginas = dados.get("paginas", [])
        fmt = self.cfg.get("formato", "paisagem")
        if fmt not in FORMATOS:
            raise SystemExit(f"formato desconhecido: {fmt} (use {', '.join(FORMATOS)})")
        self.W, self.H = FORMATOS[fmt]
        self.larga = self.W > self.H
        self.b = SANGRIA if impressao else 0
        self.M = 16 * mm
        self.dpi = 300 if impressao else 150
        self.dpi_min = 250 if impressao else 100
        self.cor_texto = HexColor(self.marca.get("cor_texto", "#2B2B2B"))
        self.cor_dest = HexColor(self.marca.get("cor_destaque", "#A47148"))
        self.cor_fundo = HexColor(self.marca.get("cor_fundo", "#FFFFFF"))
        self.cinza = HexColor("#8A8A8A")
        self.avisos, self.erros = [], []
        self.n = 0
        self.c = None
        self.saida = saida
        self._fontes()

    # ---------- infraestrutura ----------
    def _fontes(self):
        self.f, self.fb = "Helvetica", "Helvetica-Bold"
        pares = list(FONTES_PADRAO)
        fx = self.marca.get("fontes")
        if fx and fx.get("normal") and fx.get("negrito"):
            pares.insert(0, (self._p(fx["normal"]), self._p(fx["negrito"])))
        for normal, negrito in pares:
            if os.path.exists(normal) and os.path.exists(negrito):
                pdfmetrics.registerFont(TTFont("MP", normal))
                pdfmetrics.registerFont(TTFont("MP-B", negrito))
                self.f, self.fb = "MP", "MP-B"
                return

    def _p(self, caminho):
        return caminho if os.path.isabs(caminho) else os.path.join(self.base, caminho)

    def nova(self, fundo=None):
        if self.n:
            self.c.showPage()
        self.n += 1
        self.c.translate(self.b, self.b)
        self.c.setFillColor(fundo or self.cor_fundo)
        self.c.rect(-self.b, -self.b, self.W + 2 * self.b, self.H + 2 * self.b, stroke=0, fill=1)

    def rodape(self):
        c = self.c
        self.rotulo(self.marca.get("nome", "").upper(), self.M, 9 * mm, 6.5, self.cinza)
        c.setFont(self.f, 7.5)
        c.setFillColor(self.cinza)
        c.drawRightString(self.W - self.M, 9 * mm, f"{self.n:02d}")

    def rotulo(self, texto, x, y, tam=7, cor=None, direita=False):
        """Texto pequeno em maiúsculas com espaçamento entre letras."""
        if not texto:
            return
        esp = tam * 0.18
        if direita:
            x -= pdfmetrics.stringWidth(texto, self.fb, tam) + esp * (len(texto) - 1)
        t = self.c.beginText(x, y)
        t.setFont(self.fb, tam)
        t.setCharSpace(esp)
        t.setFillColor(cor or self.cor_dest)
        t.textOut(texto)
        t.setCharSpace(0)  # o espaçamento fica no estado do PDF; zerar para o texto seguinte
        self.c.drawText(t)

    def texto(self, txt, x, y, larg, tam=10, cor=None, negrito=False, entre=1.45,
              max_linhas=None):
        """Escreve um bloco com quebra de linha. y é o topo. Devolve o y final."""
        if not txt:
            return y
        fonte = self.fb if negrito else self.f
        linhas = []
        for par in str(txt).split("\n"):
            linhas += simpleSplit(par, fonte, tam, larg) or [""]
        if max_linhas and len(linhas) > max_linhas:
            linhas = linhas[:max_linhas]
            linhas[-1] = linhas[-1].rstrip(" .,;") + "…"
            self.avisos.append(f"página {self.n}: texto cortado em {max_linhas} linhas: “{str(txt)[:40]}…”")
        self.c.setFont(fonte, tam)
        self.c.setFillColor(cor or self.cor_texto)
        passo = tam * entre
        y -= tam
        for ln in linhas:
            self.c.drawString(x, y, ln)
            y -= passo
        return y + passo - tam * 0.45

    def imagem(self, caminho, x, y, w, h, foco=None, sangra=""):
        """Desenha a foto cobrindo a caixa (corta o excesso). sangra: lados que
        encostam na borda da página ('l','r','t','b') e avançam na sangria."""
        if self.b:
            if "l" in sangra: x -= self.b; w += self.b
            if "r" in sangra: w += self.b
            if "b" in sangra: y -= self.b; h += self.b
            if "t" in sangra: h += self.b
        if not caminho or not os.path.exists(self._p(caminho)):
            self.erros.append(f"página {self.n}: foto não encontrada: {caminho or '(sem arquivo)'}")
            self.c.setFillColor(HexColor("#E3E0DB"))
            self.c.rect(x, y, w, h, stroke=0, fill=1)
            self.c.setFillColor(HexColor("#9A958E"))
            self.c.setFont(self.f, 8)
            self.c.drawCentredString(x + w / 2, y + h / 2, f"FOTO: {caminho or 'a definir'}")
            return
        im = ImageOps.exif_transpose(Image.open(self._p(caminho))).convert("RGB")
        iw, ih = im.size
        alvo = w / h
        fx, fy = foco or (0.5, 0.5)
        if iw / ih > alvo:
            nw = int(round(ih * alvo))
            x0 = int(min(max(fx * iw - nw / 2, 0), iw - nw))
            im = im.crop((x0, 0, x0 + nw, ih))
        else:
            nh = int(round(iw / alvo))
            y0 = int(min(max(fy * ih - nh / 2, 0), ih - nh))
            im = im.crop((0, y0, iw, y0 + nh))
        dpi_real = im.size[0] / (w / 72.0)
        if dpi_real < self.dpi_min:
            self.avisos.append(f"página {self.n}: {caminho} fica com {dpi_real:.0f} dpi neste "
                               f"tamanho (mínimo {self.dpi_min}); usar o original ou reduzir a foto na página")
        px = int(round(w / 72.0 * self.dpi))
        if im.size[0] > px:
            im = im.resize((px, max(1, int(round(px / alvo)))), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=88, optimize=True)
        buf.seek(0)
        self.c.drawImage(ImageReader(buf), x, y, w, h)

    def veu(self, x, y, w, h, forca=0.62, passos=40, de_baixo=True):
        """Degradê escuro sobre a foto para o texto ficar legível."""
        c = self.c
        c.saveState()
        for i in range(passos):
            a = forca * (1 - i / passos) ** 1.6
            c.setFillColor(Color(0, 0, 0, alpha=a))
            yy = y + i * h / passos if de_baixo else y + h - (i + 1) * h / passos
            c.rect(x, yy, w, h / passos + 0.6, stroke=0, fill=1)
        c.restoreState()

    def linha(self, x, y, w, cor=None, esp=0.6):
        self.c.setStrokeColor(cor or self.cor_dest)
        self.c.setLineWidth(esp)
        self.c.line(x, y, x + w, y)

    # ---------- contagem de páginas (para o índice) ----------
    def por_pagina(self):
        return 3 if self.larga else 4

    def quantas(self, p):
        t = p.get("tipo")
        if t == "projeto":
            extras = len(p.get("fotos", [])) - 1
            return 1 + (math.ceil(extras / 3) if extras > 0 else 0)
        if t == "produtos":
            return max(1, math.ceil(len(p.get("itens", [])) / self.por_pagina()))
        if t == "materiais":
            return max(1, math.ceil(len(p.get("itens", [])) / (8 if self.larga else 9)))
        return 1

    # ---------- páginas ----------
    def capa(self, p):
        self.nova(HexColor("#1E1E1E"))
        W, H, M = self.W, self.H, self.M
        self.imagem(p.get("imagem"), 0, 0, W, H, p.get("foco"), "lrtb")
        self.veu(-self.b, -self.b, W + 2 * self.b, H * 0.7 + self.b, 0.78)
        branco = HexColor("#FFFFFF")
        logo = self.marca.get("logo")
        if logo and os.path.exists(self._p(logo)):
            lw, lh = Image.open(self._p(logo)).size
            alt = 14 * mm
            self.c.drawImage(ImageReader(self._p(logo)), M, H - M - alt, alt * lw / lh, alt, mask="auto")
        else:
            self.rotulo(self.marca.get("nome", "").upper(), M, H - M - 8, 9, branco)
        y = M + 34 * mm
        self.rotulo((self.cfg.get("edicao") or "").upper(), M, y + 6 * mm, 7.5, branco)
        tam = 40 if self.larga else 34
        y = self.texto(p.get("titulo") or self.cfg.get("titulo", ""), M, y, W * 0.7, tam, branco,
                       negrito=True, entre=1.08, max_linhas=2)
        self.texto(p.get("subtitulo") or self.cfg.get("subtitulo", ""), M, y - 5 * mm, W * 0.6, 12,
                   branco, max_linhas=2)
        self.rotulo((self.marca.get("cidade") or "").upper(), W - M, M, 7, branco, direita=True)

    def pg_texto(self, p):
        self.nova()
        W, H, M = self.W, self.H, self.M
        tem_img = bool(p.get("imagem"))
        if tem_img and self.larga:
            self.imagem(p["imagem"], W * 0.5, 0, W * 0.5, H, p.get("foco"), "rtb")
            x, larg, topo = M, W * 0.5 - 2 * M, H - M - 14 * mm
        elif tem_img:
            self.imagem(p["imagem"], 0, H * 0.55, W, H * 0.45, p.get("foco"), "lrt")
            x, larg, topo = M, W - 2 * M, H * 0.55 - 14 * mm
        else:
            x, larg, topo = M, min(W - 2 * M, 150 * mm), H - M - 14 * mm
        self.rotulo((p.get("rotulo") or "").upper(), x, topo + 8 * mm)
        y = self.texto(p.get("titulo"), x, topo, larg, 24, negrito=True, entre=1.15, max_linhas=3)
        y -= 5 * mm
        self.linha(x, y, 18 * mm)
        y -= 7 * mm
        for par in p.get("paragrafos", []):
            y = self.texto(par, x, y, larg, 10.5, entre=1.55) - 4 * mm
        if y < 16 * mm:
            self.erros.append(f"página {self.n}: texto não coube; encurtar “{p.get('titulo','')}”")
        self.rodape()

    def indice(self, p, mapa):
        self.nova()
        W, H, M = self.W, self.H, self.M
        topo = H - M - 14 * mm
        y = self.texto(p.get("titulo", "Índice"), M, topo, W - 2 * M, 24, negrito=True) - 12 * mm
        larg = min(W - 2 * M, 170 * mm)
        for titulo, pag in mapa:
            self.c.setFont(self.f, 12)
            self.c.setFillColor(self.cor_texto)
            self.c.drawString(M, y, titulo)
            self.c.setFillColor(self.cor_dest)
            self.c.setFont(self.fb, 12)
            self.c.drawRightString(M + larg, y, f"{pag:02d}")
            self.linha(M, y - 3.5 * mm, larg, HexColor("#DDD8D0"), 0.4)
            y -= 11 * mm
        self.rodape()

    def abertura(self, p):
        self.nova(HexColor("#1E1E1E"))
        W, H, M = self.W, self.H, self.M
        self.imagem(p.get("imagem"), 0, 0, W, H, p.get("foco"), "lrtb")
        self.veu(-self.b, -self.b, W + 2 * self.b, H * 0.6 + self.b, 0.75)
        branco = HexColor("#FFFFFF")
        y = M + 30 * mm
        self.rotulo((p.get("rotulo") or "").upper(), M, y + 6 * mm, 7.5, branco)
        y = self.texto(p.get("titulo"), M, y, W * 0.7, 32, branco, negrito=True, entre=1.1, max_linhas=2)
        self.texto(p.get("texto"), M, y - 4 * mm, min(W * 0.6, 150 * mm), 11, branco, max_linhas=3)

    def projeto(self, p):
        self.nova()
        W, H, M = self.W, self.H, self.M
        fotos = p.get("fotos", [])
        if not fotos:
            self.erros.append(f"projeto “{p.get('titulo','')}”: sem fotos")
        heroi = fotos[0] if fotos else None
        if self.larga:
            lw = W * 0.62
            self.imagem(heroi, 0, 0, lw, H, p.get("foco"), "ltb")
            x, larg, topo = lw + 12 * mm, W - lw - 12 * mm - M, H - M - 10 * mm
        else:
            ih = H * 0.56
            self.imagem(heroi, 0, H - ih, W, ih, p.get("foco"), "lrt")
            x, larg, topo = M, W - 2 * M, H - ih - 16 * mm
        self.rotulo((p.get("ambiente") or "Projeto").upper(), x, topo + 6 * mm)
        y = self.texto(p.get("titulo"), x, topo, larg, 20, negrito=True, entre=1.15, max_linhas=3)
        meta = " · ".join(v for v in (p.get("local"), str(p.get("ano") or "")) if v)
        y = self.texto(meta, x, y - 3 * mm, larg, 9, self.cinza)
        y -= 4 * mm
        self.linha(x, y, 14 * mm)
        y = self.texto(p.get("descricao"), x, y - 6 * mm, larg, 10, entre=1.5, max_linhas=9)
        y -= 5 * mm
        for rot, chave in (("Materiais", "materiais"), ("Destaques", "destaques")):
            itens = p.get(chave) or []
            if itens:
                self.rotulo(rot.upper(), x, y - 7, 6.5)
                y -= 5 * mm
                for it in itens:
                    y = self.texto("— " + it, x, y, larg, 9, entre=1.4) - 1.2 * mm
                y -= 3 * mm
        if p.get("arquiteto"):
            self.rotulo("PROJETO DE ARQUITETURA", x, y - 7, 6.5)
            y = self.texto(p["arquiteto"], x, y - 5 * mm, larg, 9)
        if p.get("foto_credito"):
            self.texto("Fotos: " + p["foto_credito"], x, 18 * mm, larg, 7, self.cinza)
        if y < 16 * mm:
            self.erros.append(f"página {self.n}: ficha do projeto “{p.get('titulo','')}” não coube; encurtar")
        self.rodape() if not self.larga else self._rodape_direita(x)
        resto = fotos[1:]
        for i in range(0, len(resto), 3):
            self.galeria(resto[i:i + 3])

    def _rodape_direita(self, x):
        self.c.setFont(self.f, 7.5)
        self.c.setFillColor(self.cinza)
        self.c.drawRightString(self.W - self.M, 9 * mm, f"{self.n:02d}")

    def galeria(self, fotos):
        self.nova()
        W, H, M = self.W, self.H, self.M
        g = 4 * mm
        y0, alt = 18 * mm, H - M - 18 * mm
        x0, larg = M, W - 2 * M
        if len(fotos) == 1:
            self.imagem(fotos[0], x0, y0, larg, alt)
        elif len(fotos) == 2:
            if self.larga:
                w = (larg - g) / 2
                self.imagem(fotos[0], x0, y0, w, alt)
                self.imagem(fotos[1], x0 + w + g, y0, w, alt)
            else:
                h = (alt - g) / 2
                self.imagem(fotos[0], x0, y0 + h + g, larg, h)
                self.imagem(fotos[1], x0, y0, larg, h)
        else:
            if self.larga:
                w1 = larg * 0.62
                w2 = larg - w1 - g
                h = (alt - g) / 2
                self.imagem(fotos[0], x0, y0, w1, alt)
                self.imagem(fotos[1], x0 + w1 + g, y0 + h + g, w2, h)
                self.imagem(fotos[2], x0 + w1 + g, y0, w2, h)
            else:
                h1 = alt * 0.6
                h2 = alt - h1 - g
                w = (larg - g) / 2
                self.imagem(fotos[0], x0, y0 + h2 + g, larg, h1)
                self.imagem(fotos[1], x0, y0, w, h2)
                self.imagem(fotos[2], x0 + w + g, y0, w, h2)
        self.rodape()

    def produtos(self, p):
        itens = p.get("itens", [])
        pp = self.por_pagina()
        cols = 3 if self.larga else 2
        lins = 1 if self.larga else 2
        W, H, M = self.W, self.H, self.M
        g = 8 * mm
        precos = self.cfg.get("mostrar_precos", False)
        for ini in range(0, max(len(itens), 1), pp):
            self.nova()
            topo = H - M - 8 * mm
            self.rotulo((p.get("rotulo") or "").upper(), M, topo + 5 * mm)
            y = self.texto(p.get("titulo"), M, topo, W - 2 * M, 18, negrito=True, max_linhas=1)
            area_topo = y - 8 * mm
            cw = (W - 2 * M - g * (cols - 1)) / cols
            ch = (area_topo - 16 * mm - g * (lins - 1)) / lins
            for k, it in enumerate(itens[ini:ini + pp]):
                col, lin = k % cols, k // cols
                x = M + col * (cw + g)
                yt = area_topo - lin * (ch + g)
                ih = ch * (0.56 if self.larga else 0.52)
                self.imagem(it.get("imagem"), x, yt - ih, cw, ih, it.get("foco"))
                yy = yt - ih - 5 * mm
                self.rotulo((it.get("codigo") or "").upper(), x, yy - 6, 6.5)
                yy = self.texto(it.get("nome"), x, yy - 4 * mm, cw, 12, negrito=True, max_linhas=2)
                yy = self.texto(it.get("descricao"), x, yy - 2 * mm, cw, 8.5, entre=1.45, max_linhas=4)
                yy -= 2.5 * mm
                for rot, ch_ in (("Medidas", "medidas"), ("Material", "material"),
                                 ("Acabamento", "acabamento"), ("Prazo", "prazo")):
                    if it.get(ch_):
                        yy = self.texto(f"{rot}: {it[ch_]}", x, yy, cw, 8, self.cinza, max_linhas=2) - 1 * mm
                if precos and it.get("preco"):
                    yy = self.texto(str(it["preco"]), x, yy - 2 * mm, cw, 11, self.cor_dest, negrito=True)
                elif not precos:
                    yy = self.texto("Sob consulta", x, yy - 2 * mm, cw, 8.5, self.cor_dest, negrito=True)
                if yy < yt - ch - 2 * mm:
                    self.erros.append(f"página {self.n}: ficha de “{it.get('nome','')}” não coube; encurtar")
            self.rodape()

    def processo(self, p):
        self.nova()
        W, H, M = self.W, self.H, self.M
        topo = H - M - 12 * mm
        self.rotulo((p.get("rotulo") or "").upper(), M, topo + 6 * mm)
        y = self.texto(p.get("titulo"), M, topo, W - 2 * M, 24, negrito=True, max_linhas=2) - 12 * mm
        etapas = p.get("etapas", [])
        cols = (4 if len(etapas) > 6 else 3) if self.larga else 2
        g = 9 * mm
        cw = (W - 2 * M - g * (cols - 1)) / cols
        lins = math.ceil(len(etapas) / cols) or 1
        lh = (y - 16 * mm) / lins
        for i, e in enumerate(etapas):
            x = M + (i % cols) * (cw + g)
            yt = y - (i // cols) * lh
            self.c.setFont(self.fb, 20)
            self.c.setFillColor(self.cor_dest)
            self.c.drawString(x, yt - 18, f"{i + 1:02d}")
            self.linha(x, yt - 24, cw, HexColor("#DDD8D0"), 0.4)
            yy = self.texto(e.get("titulo"), x, yt - 30, cw, 11, negrito=True, max_linhas=2)
            yy = self.texto(e.get("texto"), x, yy - 2 * mm, cw, 9, entre=1.5, max_linhas=6)
            if yy < yt - lh:
                self.erros.append(f"página {self.n}: etapa “{e.get('titulo','')}” não coube; encurtar")
        self.rodape()

    def materiais(self, p):
        itens = p.get("itens", [])
        pp = 8 if self.larga else 9
        cols = 4 if self.larga else 3
        W, H, M = self.W, self.H, self.M
        g = 6 * mm
        for ini in range(0, max(len(itens), 1), pp):
            self.nova()
            topo = H - M - 10 * mm
            self.rotulo((p.get("rotulo") or "").upper(), M, topo + 5 * mm)
            y = self.texto(p.get("titulo"), M, topo, W - 2 * M, 20, negrito=True, max_linhas=1)
            y = self.texto(p.get("texto"), M, y - 3 * mm, min(W - 2 * M, 170 * mm), 9.5, self.cinza,
                           max_linhas=3) - 8 * mm
            lins = math.ceil(pp / cols)
            cw = (W - 2 * M - g * (cols - 1)) / cols
            ch = (y - (24 if p.get('nota') else 16) * mm - g * (lins - 1)) / lins
            for k, it in enumerate(itens[ini:ini + pp]):
                x = M + (k % cols) * (cw + g)
                yt = y - (k // cols) * (ch + g)
                sh = ch - 13 * mm
                if it.get("imagem"):
                    self.imagem(it["imagem"], x, yt - sh, cw, sh)
                else:
                    cor = it.get("cor")
                    if not cor:
                        self.erros.append(f"material “{it.get('nome','')}”: sem imagem e sem cor")
                    self.c.setFillColor(HexColor(cor or "#E3E0DB"))
                    self.c.setStrokeColor(HexColor("#DDD8D0"))
                    self.c.setLineWidth(0.4)
                    self.c.rect(x, yt - sh, cw, sh, stroke=1, fill=1)
                yy = self.texto(it.get("nome"), x, yt - sh - 3 * mm, cw, 9.5, negrito=True, max_linhas=1)
                self.texto(it.get("tipo"), x, yy - 1 * mm, cw, 7.5, self.cinza, max_linhas=1)
            if p.get("nota"):
                self.texto(p["nota"], M, 16 * mm, W - 2 * M - 20 * mm, 7, self.cinza, max_linhas=1)
            self.rodape()

    def depoimento(self, p):
        self.nova(HexColor("#F4F1EC"))
        W, H, M = self.W, self.H, self.M
        larg = min(W - 2 * M, 190 * mm)
        x = (W - larg) / 2
        self.c.setFont(self.fb, 60)
        self.c.setFillColor(self.cor_dest)
        self.c.drawString(x, H * 0.72, "“")
        y = self.texto(p.get("texto"), x, H * 0.70, larg, 17, entre=1.5, max_linhas=8)
        y -= 8 * mm
        self.linha(x, y, 14 * mm)
        y = self.texto(p.get("autor"), x, y - 6 * mm, larg, 10, negrito=True)
        self.texto(p.get("local"), x, y - 1.5 * mm, larg, 9, self.cinza)
        self.rodape()

    def contato(self, p):
        self.nova(HexColor("#1E1E1E"))
        W, H, M = self.W, self.H, self.M
        branco = HexColor("#FFFFFF")
        if p.get("imagem"):
            self.imagem(p["imagem"], 0, 0, W, H, p.get("foco"), "lrtb")
            self.c.saveState()
            self.c.setFillColor(Color(0, 0, 0, alpha=0.62))
            self.c.rect(-self.b, -self.b, W + 2 * self.b, H + 2 * self.b, stroke=0, fill=1)
            self.c.restoreState()
        topo = H - M - 22 * mm
        self.rotulo((p.get("rotulo") or "Contato").upper(), M, topo + 7 * mm, 7.5, self.cor_dest)
        y = self.texto(p.get("titulo"), M, topo, W * 0.62, 28, branco, negrito=True, entre=1.12, max_linhas=3)
        y = self.texto(p.get("texto"), M, y - 5 * mm, min(W * 0.55, 150 * mm), 11, branco, entre=1.55,
                       max_linhas=5) - 10 * mm
        m = self.marca
        zap = re.sub(r"\D", "", str(m.get("whatsapp") or ""))
        linhas = [("WhatsApp", m.get("whatsapp_exibir") or m.get("whatsapp")), ("Instagram", m.get("instagram")),
                  ("Site", m.get("site")), ("E-mail", m.get("email")), ("Endereço", m.get("endereco"))]
        for rot, val in linhas:
            if val:
                self.rotulo(rot.upper(), M, y - 7, 6.5, self.cor_dest)
                y = self.texto(str(val), M, y - 4.5 * mm, W * 0.55, 11, branco) - 4 * mm
        if zap:
            msg = (p.get("mensagem_whatsapp") or "").replace(" ", "%20")
            url = f"https://wa.me/{zap}" + (f"?text={msg}" if msg else "")
            lado = 38 * mm
            cod = qr.QrCodeWidget(url, barLevel="M")
            b = cod.getBounds()
            d = Drawing(lado, lado, transform=[lado / (b[2] - b[0]), 0, 0, lado / (b[3] - b[1]), 0, 0])
            d.add(cod)
            qx, qy = W - M - lado, M + 8 * mm
            self.c.setFillColor(branco)
            self.c.rect(qx - 3 * mm, qy - 3 * mm, lado + 6 * mm, lado + 6 * mm, stroke=0, fill=1)
            renderPDF.draw(d, self.c, qx, qy)
            self.rotulo("APONTE A CÂMERA", W - M - 3 * mm + 3 * mm, qy - 8 * mm, 6.5, branco, direita=True)
            self.c.linkURL(url, (self.b + qx, self.b + qy, self.b + qx + lado, self.b + qy + lado))
        else:
            self.erros.append("contato: marca.whatsapp vazio; sem QR e sem link")
        self.rotulo((m.get("nome") or "").upper(), M, M, 7, branco)

    # ---------- conferência e geração ----------
    def conferir(self):
        def anda(o, onde):
            if isinstance(o, dict):
                for k, v in o.items():
                    anda(v, f"{onde}.{k}")
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    anda(v, f"{onde}[{i}]")
            elif isinstance(o, str) and PENDENTE.search(o):
                self.erros.append(f"pendência em {onde}: {o[:60]}")
        anda(self.d, "catalogo")
        for campo in ("nome", "whatsapp", "instagram"):
            if not self.marca.get(campo):
                self.erros.append(f"marca.{campo} não preenchido")
        tipos = [p.get("tipo") for p in self.paginas]
        for i, t in enumerate(tipos):
            if t not in TIPOS:
                self.erros.append(f"paginas[{i}]: tipo desconhecido “{t}”")
        if tipos[:1] != ["capa"]:
            self.avisos.append("o catálogo não começa com uma capa")
        if tipos[-1:] != ["contato"]:
            self.avisos.append("o catálogo não termina com a página de contato")
        for p in self.paginas:
            if p.get("tipo") == "projeto":
                nome = p.get("titulo", "(sem título)")
                if not p.get("autorizado"):
                    self.erros.append(f"projeto “{nome}”: falta \"autorizado\": true (autorização do cliente para publicar)")
                if p.get("arquiteto") and not p.get("arquiteto_autorizou"):
                    self.avisos.append(f"projeto “{nome}”: confirmar com o arquiteto o crédito e o uso das imagens")
                if len(p.get("fotos", [])) < 2:
                    self.avisos.append(f"projeto “{nome}”: só {len(p.get('fotos', []))} foto; o ideal é uma geral e ao menos um detalhe")
                if len(p.get("descricao") or "") < 60:
                    self.avisos.append(f"projeto “{nome}”: descrição curta ou ausente")
            if p.get("tipo") == "produtos":
                for it in p.get("itens", []):
                    if not it.get("medidas"):
                        self.avisos.append(f"produto “{it.get('nome','')}”: sem medidas")
                    if self.cfg.get("mostrar_precos") and not it.get("preco"):
                        self.erros.append(f"produto “{it.get('nome','')}”: catálogo com preços e item sem preço")

    def gerar(self):
        self.c = canvas.Canvas(self.saida, pagesize=(self.W + 2 * self.b, self.H + 2 * self.b))
        self.c.setTitle(f"{self.marca.get('nome', '')} · {self.cfg.get('titulo', 'Catálogo')}")
        self.c.setAuthor(self.marca.get("nome", ""))
        mapa, pag = [], 1
        for p in self.paginas:
            if p.get("tipo") == "abertura":
                mapa.append((p.get("titulo", ""), pag))
            pag += self.quantas(p)
        acao = {"capa": self.capa, "texto": self.pg_texto, "abertura": self.abertura,
                "projeto": self.projeto, "produtos": self.produtos, "processo": self.processo,
                "materiais": self.materiais, "depoimento": self.depoimento, "contato": self.contato}
        for p in self.paginas:
            t = p.get("tipo")
            if t == "indice":
                self.indice(p, mapa)
            elif t in acao:
                acao[t](p)
        self.c.save()
        if self.impressao and self.n % 4:
            self.avisos.append(f"{self.n} páginas: para grampo (canoa) o total precisa ser múltiplo de 4; "
                               f"faltam {4 - self.n % 4}")


def main():
    ap = argparse.ArgumentParser(description="Gera o catálogo da MP Marcenaria em PDF.")
    ap.add_argument("json")
    ap.add_argument("-o", "--saida")
    ap.add_argument("--impressao", action="store_true", help="300 dpi e sangria de 3 mm")
    ap.add_argument("--conferir", action="store_true", help="só valida o JSON")
    ap.add_argument("--final", action="store_true", help="não gera se houver pendência")
    a = ap.parse_args()
    with open(a.json, encoding="utf-8") as f:
        dados = json.load(f)
    base = os.path.dirname(os.path.abspath(a.json))
    saida = a.saida or os.path.splitext(a.json)[0] + ("_impressao.pdf" if a.impressao else ".pdf")
    cat = Catalogo(dados, base, saida, a.impressao)
    cat.conferir()
    if a.conferir or (a.final and cat.erros):
        cat.saida = os.devnull
    cat.gerar()
    for titulo, lista in (("PENDÊNCIAS (impedem a versão final)", cat.erros), ("AVISOS", cat.avisos)):
        if lista:
            print(f"\n{titulo}")
            for item in dict.fromkeys(lista):
                print("  -", item)
    if cat.saida != os.devnull:
        mb = os.path.getsize(saida) / 1e6
        print(f"\n{saida}: {cat.n} páginas, {mb:.1f} MB" + ("  (boneco: há pendências)" if cat.erros else ""))
    elif a.final and cat.erros:
        print("\nNão gerado: resolva as pendências ou rode sem --final para ver o boneco.")
    sys.exit(1 if (cat.erros and (a.final or a.conferir)) else 0)


if __name__ == "__main__":
    main()
