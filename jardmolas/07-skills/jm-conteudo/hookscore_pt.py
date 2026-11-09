#!/usr/bin/env python3
"""
hookscore_pt.py - o hookscore.py da skill ig-reel, adaptado para português.

Não muda o cálculo do original. Troca as listas de palavras (o que cria
tensão, aberturas fracas, imperativos, números falados, "você") e as
expressões de palavra, número e nome próprio para aceitar acento e unidades
de oficina (mm, kg, kgf, safra).

Uso
  python3 hookscore_pt.py ganchos.txt          # um gancho por linha, em ranking
  python3 hookscore_pt.py --hook "Você só vê esse dedo quando ele quebra"

Serve para comparar ganchos entre si e pegar os erros clássicos (saudação,
"neste vídeo", gancho sem nada concreto). Não prevê visualização: quem decide
é a retenção dos 3 primeiros segundos no painel do Instagram.

Precisa do hookscore.py original. Procura em: variável HOOKSCORE, na pasta
skills/ig-reel deste repositório e em ~/.claude/skills/ig-reel.
"""
import importlib.util
import os
import re
import sys
from pathlib import Path


def _achar_original():
    candidatos = [
        os.environ.get("HOOKSCORE", ""),
        str(Path(__file__).resolve().parents[3] / "skills" / "ig-reel" / "hookscore.py"),
        str(Path.home() / ".claude" / "skills" / "ig-reel" / "hookscore.py"),
    ]
    for c in candidatos:
        if c and Path(c).is_file():
            return c
    sys.exit("Não achei o hookscore.py da skill ig-reel. Instale skills/ig-reel ou defina HOOKSCORE=/caminho/hookscore.py")


SRC = _achar_original()
spec = importlib.util.spec_from_file_location("hookscore", SRC)
hs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hs)

hs.WORD_RE = re.compile(r"[\w$%'’-]+", re.UNICODE)
hs.NUMBER_RE = re.compile(
    r"R\$\s?\d[\d.,]*"
    r"|\b\d[\d.,]*\s?"
    r"(?:%|kg\b|kgf\b|mm\b|cm\b|m\b|t\b|s\b|seg\b|segundos?\b|min\b|minutos?\b|horas?\b|h\b"
    r"|dias?\b|semanas?\b|meses\b|m[eê]s\b|anos?\b|safras?\b|modelos?\b|mil\b)?",
    re.IGNORECASE)
hs.PROPER_RE = re.compile(r"(?<!^)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b")
hs.SPOKEN_NUMBERS = {
    "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete", "oito",
    "nove", "dez", "onze", "doze", "quinze", "vinte", "trinta", "quarenta",
    "cinquenta", "cem", "cento", "mil", "milhão", "milhões", "dúzia", "metade",
    "dobro", "triplo",
}
hs.MONEY_WORDS = {"reais", "real", "centavos", "conto", "contos", "prejuízo",
                  "lucro", "custo", "preço", "quilos", "quilo", "kg"}
hs.STAKES = {
    "pare", "para", "nunca", "errado", "errada", "erro", "erros", "perdeu",
    "perde", "perder", "perdendo", "custa", "custou", "custo", "quebrou",
    "quebra", "quebrada", "quebrado", "quebrar", "quebram", "falha", "falhou",
    "falhar", "ninguém", "não", "nao", "nem", "sem", "parada", "parou", "parar",
    "aguenta", "aguentar", "aguentou", "grátis", "gratuita", "gratuito", "caro",
    "barato", "antes", "até", "mas", "só", "problema", "risco", "perigo",
    "cuidado", "verdade", "segredo", "pior", "melhor", "desperdício", "primeiro",
    "primeira", "ainda", "já", "contra", "versus", "vs", "x", "mentira",
    "rompeu", "rompida", "rompido", "estourou", "gastou", "gasto", "cansa",
    "cansado", "cansou", "frouxo", "batendo", "vazando", "errou", "erra",
    "esquece", "esqueceu", "fora", "troca", "trocar", "trocou",
}
hs.WEAK_OPENERS = [
    "bom dia", "boa tarde", "boa noite", "oi", "olá", "ola", "e aí", "e ai",
    "pessoal", "galera", "gente", "hoje", "então", "entao", "bom", "bem",
    "basicamente", "sinceramente", "vamos", "vou", "eu queria", "eu quero",
    "neste vídeo", "nesse vídeo", "no vídeo", "aqui é", "esse é o", "este é o",
    "isso é", "tem um", "existe", "você sabia", "voce sabia", "já pensou", "sabe",
    "fala", "salve",
]
hs.IMPERATIVES = {
    "pare", "para", "copia", "copie", "salva", "salve", "mede", "meça", "veja",
    "confira", "confere", "troca", "troque", "nunca", "sempre", "faça", "faz",
    "manda", "mande", "use", "usa", "testa", "teste", "compara", "compare",
    "guarda", "guarde", "anota", "anote", "olha", "aperta", "aperte", "chuta",
    "pergunta", "pergunte", "não", "nao",
}
hs.DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:para de rolar|pare de rolar|não passa|nao passa)"),
     "Abre com 'para de rolar'."),
    (re.compile(r"(?i)\b(?:neste vídeo|nesse vídeo|no vídeo de hoje|vou (?:te )?mostrar)\b"),
     "Preâmbulo de vídeo."),
    (re.compile(r"(?i)^\s*(?:oi|olá|ola|bom dia|boa tarde|boa noite|e aí|fala galera|fala pessoal|salve)\b"),
     "Saudação."),
    (hs.HASHTAG_RE, "Hashtag no gancho."),
    (hs.EMOJI_RE, "Emoji no gancho."),
]


def check_address(text):
    low = text.lower()
    w = [x.lower().strip("'’") for x in hs.words(text)]
    if re.search(r"\b(você|vocês|voce|seu|sua|seus|suas|te|tu|teu|tua)\b", low):
        return 100.0, "fala com quem assiste"
    if w and w[0] in hs.IMPERATIVES:
        return 90.0, f"abre no imperativo (\"{w[0]}\")"
    if re.search(r"\b(eu|meu|minha|me|nós|nosso|nossa|a gente)\b", low):
        return 70.0, "primeira pessoa"
    return 35.0, "terceira pessoa"


hs.check_address = check_address

if __name__ == "__main__":
    hs.main()
