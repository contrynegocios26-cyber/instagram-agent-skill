"""Ilustrações vetoriais das tábuas, faca e garfo usadas no catálogo.

Servem enquanto não há foto do protótipo. Cada função devolve um <g> SVG com
os próprios <defs>, identificados por um prefixo para poder repetir na página.
"""
import math
import random

CLARAS = ["#d2a06c", "#c99660", "#dcae7c", "#c58f5a"]
ESCURAS = ["#7d4b2d", "#73432a", "#86522f"]
FUNDO = "#140a0a"


def _onda(x0, x1, y, amp, rng, passo=28):
    fase = rng.uniform(0, 6.28)
    freq = rng.uniform(0.008, 0.02)
    d = f"M{x0:.1f},{y:.1f}"
    x = x0
    while x < x1:
        nx = min(x + passo, x1)
        cx = (x + nx) / 2
        cy = y + amp * math.sin(freq * cx + fase) + rng.uniform(-amp * 0.3, amp * 0.3)
        ny = y + amp * math.sin(freq * nx + fase) * 0.6
        d += f" Q{cx:.1f},{cy:.1f} {nx:.1f},{ny:.1f}"
        x = nx
    return d


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tabua(pid, w, h, *, canaleta=False, alca=False, furo=False, texto="SUA MARCA",
          subtitulo="BOAS FESTAS · 2026", logo=None, seed=1):
    """Tábua de tiras coladas, vista de cima, com a marca gravada a fogo."""
    rng = random.Random(seed)
    r = min(w, h) * 0.06
    defs = [
        f'<clipPath id="{pid}c"><rect width="{w}" height="{h}" rx="{r:.1f}"/></clipPath>',
        f'<linearGradient id="{pid}s" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#fff" stop-opacity=".16"/>'
        f'<stop offset=".45" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".30"/></linearGradient>',
        f'<filter id="{pid}b" x="-10%" y="-30%" width="120%" height="160%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="{seed}" result="n"/>'
        f'<feDisplacementMap in="SourceGraphic" in2="n" scale="1.8" result="d"/>'
        f'<feGaussianBlur in="d" stdDeviation="0.35"/></filter>',
        f'<filter id="{pid}h" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.6"/></filter>',
        # logo: o que é escuro vira queimado, o que é claro some na madeira
        f'<filter id="{pid}L"><feColorMatrix type="matrix" values="0 0 0 0 .16  0 0 0 0 .08  0 0 0 0 .04  '
        f'-.45 -.885 -.165 1.5 0" result="q"/>'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="{seed}" result="n"/>'
        f'<feDisplacementMap in="q" in2="n" scale="1.5"/></filter>',
    ]
    g = [f'<g clip-path="url(#{pid}c)">']
    y, escura_antes = 0.0, True
    while y < h:
        alt = rng.uniform(0.09, 0.17) * h
        if y + alt > h - 0.06 * h:
            alt = h - y
        escura = (not escura_antes) and rng.random() < 0.35
        cor = rng.choice(ESCURAS if escura else CLARAS)
        g.append(f'<rect x="0" y="{y:.1f}" width="{w}" height="{alt + 0.6:.1f}" fill="{cor}"/>')
        for k in range(max(3, int(alt / 5))):
            gy = y + (k + rng.uniform(0.2, 0.8)) * alt / max(3, int(alt / 5))
            g.append(f'<path d="{_onda(-10, w + 10, gy, rng.uniform(0.6, 2.2), rng)}" fill="none" '
                     f'stroke="{"#2a120a" if escura else "#3a1d0e"}" stroke-opacity="{rng.uniform(0.08, 0.22):.2f}" '
                     f'stroke-width="{rng.uniform(0.5, 1.4):.2f}"/>')
        if y > 0:
            g.append(f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="#2a140a" stroke-opacity=".35" stroke-width=".8"/>')
        escura_antes = escura
        y += alt
    g.append(f'<rect width="{w}" height="{h}" fill="url(#{pid}s)"/>')

    if canaleta:
        m, gw = h * 0.075, h * 0.03
        g.append(f'<rect x="{m:.1f}" y="{m:.1f}" width="{w - 2 * m:.1f}" height="{h - 2 * m:.1f}" rx="{r * 1.2:.1f}" '
                 f'fill="none" stroke="#2b1309" stroke-opacity=".5" stroke-width="{gw:.1f}"/>')
        o = gw * 0.3
        g.append(f'<rect x="{m + o:.1f}" y="{m + o:.1f}" width="{w - 2 * m:.1f}" height="{h - 2 * m:.1f}" rx="{r * 1.2:.1f}" '
                 f'fill="none" stroke="#ffe9cf" stroke-opacity=".16" stroke-width="{gw * 0.3:.1f}"/>')

    cx, cy = w / 2, h / 2
    if logo:
        lw, lh = w * 0.42, h * 0.42
        g.append(f'<image href="{logo}" x="{cx - lw / 2:.1f}" y="{cy - lh / 2:.1f}" width="{lw:.1f}" height="{lh:.1f}" '
                 f'preserveAspectRatio="xMidYMid meet" filter="url(#{pid}L)" opacity=".92"/>')
    elif texto:
        t = _esc(texto.upper())
        tam = min(w * 0.085, (w * 0.7) / max(len(t) * 0.68, 1))
        sub = _esc(subtitulo) if subtitulo else ""
        ty = cy + tam * 0.3 - (tam * 0.45 if sub else 0)
        bloco = (f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Inter" font-weight="800" '
                 f'font-size="{tam:.1f}" letter-spacing="{tam * 0.06:.1f}">{t}</text>')
        if sub:
            st = tam * 0.34
            bloco += (f'<text x="{cx:.1f}" y="{ty + tam * 0.95:.1f}" text-anchor="middle" font-family="Inter" '
                      f'font-weight="600" font-size="{st:.1f}" letter-spacing="{st * 0.32:.1f}">{sub}</text>')
        g.append(f'<g fill="#4a2410" opacity=".35" filter="url(#{pid}h)">{bloco}</g>')
        g.append(f'<g fill="#2a1208" opacity=".88" filter="url(#{pid}b)">{bloco}</g>')
    g.append("</g>")
    g.append(f'<rect x=".8" y=".8" width="{w - 1.6}" height="{h - 1.6}" rx="{r:.1f}" fill="none" '
             f'stroke="#fff3e3" stroke-opacity=".22" stroke-width="1.6"/>')

    if furo or alca:
        hx, hy, hr = w - h * 0.045, cy, h * 0.016
        g.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr:.1f}" fill="{FUNDO}" stroke="#2a140a" stroke-width="1"/>')
        if alca:
            a = h * 0.2
            laco = (f"M{hx:.1f},{hy:.1f} C{hx + a * 1.3:.1f},{hy - a:.1f} {hx + a * 1.3:.1f},{hy + a:.1f} {hx:.1f},{hy:.1f}")
            g.append(f'<path d="{laco}" fill="none" stroke="#3d2216" stroke-width="{h * 0.028:.1f}" stroke-linecap="round"/>')
            g.append(f'<path d="{laco}" fill="none" stroke="#c9a27c" stroke-opacity=".55" stroke-width=".9" stroke-dasharray="3 3"/>')
    return "<defs>" + "".join(defs) + "</defs>" + "".join(g)


def _cabo(pid):
    defs = (f'<linearGradient id="{pid}w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3520"/>'
            f'<stop offset="1" stop-color="#2a160c"/></linearGradient>'
            f'<radialGradient id="{pid}r"><stop offset="0" stop-color="#fbfcfd"/><stop offset="1" stop-color="#8d959c"/></radialGradient>'
            f'<linearGradient id="{pid}a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f4f6"/>'
            f'<stop offset=".55" stop-color="#c3c9ce"/><stop offset="1" stop-color="#8f979e"/></linearGradient>')
    g = (f'<rect x="0" y="-11" width="122" height="22" rx="9" fill="url(#{pid}w)"/>'
         f'<path d="M6,-4 Q60,-7 116,-3 M8,4 Q62,2 114,5" stroke="#1a0c06" stroke-opacity=".35" fill="none"/>'
         + "".join(f'<circle cx="{x}" cy="0" r="3.2" fill="url(#{pid}r)"/>' for x in (26, 61, 96))
         + f'<rect x="120" y="-12.5" width="11" height="25" rx="2.5" fill="url(#{pid}a)" stroke="#7d858c" stroke-width=".6"/>')
    return defs, g


def faca(pid):
    defs, cabo = _cabo(pid)
    lamina = (f'<path d="M131,-11 L312,-11 Q334,-10 338,-2 Q300,13 222,15 L131,15 Z" fill="url(#{pid}a)" '
              f'stroke="#7d858c" stroke-width=".7"/>'
              f'<path d="M135,-8 L308,-8" stroke="#fff" stroke-opacity=".7" stroke-width="1"/>')
    return f"<defs>{defs}</defs>{cabo}{lamina}"


def garfo(pid):
    defs, cabo = _cabo(pid)
    cabeca = (f'<rect x="131" y="-3.5" width="88" height="7" rx="2" fill="url(#{pid}a)" stroke="#7d858c" stroke-width=".6"/>'
              f'<rect x="214" y="-11" width="20" height="22" rx="5" fill="url(#{pid}a)" stroke="#7d858c" stroke-width=".6"/>'
              f'<path d="M232,-10 L318,-6.5 L322,-4.5 L232,-3 Z M232,3 L322,4.5 L318,6.5 L232,10 Z" '
              f'fill="url(#{pid}a)" stroke="#7d858c" stroke-width=".6"/>')
    return f"<defs>{defs}</defs>{cabo}{cabeca}"


SOMBRA = ('<filter id="{id}" x="-20%" y="-20%" width="140%" height="150%">'
          '<feDropShadow dx="0" dy="{dy}" stdDeviation="{sd}" flood-color="#000" flood-opacity=".6"/></filter>')


def heroi(texto="SUA MARCA", logo=None):
    s = SOMBRA.format(id="hs", dy=14, sd=16) + SOMBRA.format(id="hk", dy=8, sd=6)
    return (f'<svg viewBox="0 0 640 470" xmlns="http://www.w3.org/2000/svg"><defs>{s}</defs>'
            f'<g transform="translate(78,64) rotate(-7 225 150)" filter="url(#hs)">'
            f'{tabua("h", 450, 300, canaleta=True, alca=True, texto=texto, logo=logo, seed=7)}</g>'
            f'<g transform="translate(200,425) rotate(-12) scale(1.05)" filter="url(#hk)">{faca("hf")}</g></svg>')


def mini_essencial(texto="SUA MARCA", logo=None):
    s = SOMBRA.format(id="es", dy=10, sd=10)
    return (f'<svg viewBox="0 0 520 330" xmlns="http://www.w3.org/2000/svg"><defs>{s}</defs>'
            f'<g transform="translate(85,50) rotate(-5 175 110)" filter="url(#es)">'
            f'{tabua("e", 350, 220, furo=True, texto=texto, subtitulo=None, logo=logo, seed=3)}</g></svg>')


def mini_churrasco(texto="SUA MARCA", logo=None):
    s = SOMBRA.format(id="cs", dy=10, sd=10)
    return (f'<svg viewBox="0 0 560 360" xmlns="http://www.w3.org/2000/svg"><defs>{s}</defs>'
            f'<g transform="translate(40,32) rotate(-5 225 150)" filter="url(#cs)">'
            f'{tabua("c", 450, 300, canaleta=True, alca=True, texto=texto, subtitulo=None, logo=logo, seed=11)}</g></svg>')


def mini_premium(texto="SUA MARCA", logo=None):
    s = SOMBRA.format(id="ps", dy=10, sd=10) + SOMBRA.format(id="pk", dy=6, sd=4)
    return (f'<svg viewBox="0 0 560 360" xmlns="http://www.w3.org/2000/svg"><defs>{s}</defs>'
            f'<g transform="translate(40,20) rotate(-5 225 150)" filter="url(#ps)">'
            f'{tabua("p", 450, 300, canaleta=True, texto=texto, subtitulo=None, logo=logo, seed=5)}</g>'
            f'<g transform="translate(95,300) rotate(-9)" filter="url(#pk)">{faca("pf")}</g>'
            f'<g transform="translate(120,335) rotate(-9)" filter="url(#pk)">{garfo("pg")}</g></svg>')
