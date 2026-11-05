#!/usr/bin/env python3
"""Quiz do pack Web3. Le banco.json, sorteia questoes, grava progresso.

    python3 quiz.py --modulo seguranca [--n 10]
    python3 quiz.py --tudo
    python3 quiz.py --progresso
    python3 quiz.py --listar
    python3 quiz.py --modulo defi --respostas 1,3,2,...   # modo nao interativo (mesma seed)

Sem dependencias, sem rede. Progresso em ~/.claude/web3/progresso.json.
"""
import argparse
import json
import os
import random
import sys
from collections import defaultdict
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
MINIMO = {"seguranca": 9, "fundamentos": 7, "defi": 8, "onchain": 7, "airdrops": 7, "dev": 8, "renda": 6, "risco": 8}


def carregar_banco():
    return json.load(open(os.path.join(AQUI, "banco.json"), encoding="utf-8"))


def carregar_progresso(caminho):
    try:
        return json.load(open(os.path.expanduser(caminho), encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def salvar_progresso(caminho, prog):
    caminho = os.path.expanduser(caminho)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    json.dump(prog, open(caminho, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def perguntar(i, q, resposta_pronta=None):
    print(f"\n[{i}] {q['pergunta']}")
    for n, op in enumerate(q["opcoes"], 1):
        print(f"   {n}. {op}")
    if resposta_pronta is not None:
        r = resposta_pronta
        print(f"   > {r}")
    else:
        while True:
            try:
                r = input("   > ").strip()
            except EOFError:
                print("\n(entrada encerrada, rodada abandonada)")
                sys.exit(1)
            if r.isdigit() and 1 <= int(r) <= len(q["opcoes"]):
                break
            print("   digite o numero da opcao")
    r = int(r)
    certo = r == q["resposta"]
    if certo:
        print("   certo. " + q["explicacao"])
    else:
        print(f"   errado. resposta: {q['resposta']}. {q['explicacao']}")
        print(f"   -> /{q['agente']}")
    return certo


def rodada(banco, modulo, n, prog, seed=None, respostas=None):
    qs = [q for q in banco if q["modulo"] == modulo]
    if not qs:
        sys.exit(f"modulo '{modulo}' nao existe. use --listar")
    rng = random.Random(seed)
    escolhidas = rng.sample(qs, min(n, len(qs)))
    print(f"\nTREINO  ·  {date.today().isoformat()}  ·  modulo {modulo}  ·  {len(escolhidas)} questoes")
    erradas = []
    for i, q in enumerate(escolhidas, 1):
        pronta = respostas[i - 1] if respostas and i - 1 < len(respostas) else None
        if not perguntar(i, q, pronta):
            erradas.append(q)
    certas = len(escolhidas) - len(erradas)
    nota = round(10 * certas / len(escolhidas), 1)
    minimo = MINIMO.get(modulo, 7)
    registro = prog.setdefault(modulo, {"ultima": 0, "melhor": 0, "rodadas": 0})
    registro["ultima"] = nota
    registro["melhor"] = max(registro["melhor"], nota)
    registro["rodadas"] += 1
    registro["data"] = date.today().isoformat()
    status = "LIBERADO" if nota >= minimo else f"ABAIXO DO MINIMO ({minimo}/10)"
    print(f"\n  {len(escolhidas)} questoes  ·  {certas} certas  ·  nota {nota:g}/10  ·  melhor {registro['melhor']:g}/10  ·  {status}")
    if erradas:
        print("\n  errou")
        for q in erradas:
            print(f"    {q['id']}  {q['pergunta'][:70]}")
            print(f"         -> /{q['agente']}")
    return nota


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modulo")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--tudo", action="store_true")
    ap.add_argument("--progresso", action="store_true")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--seed", type=int, help="sorteio reproduzivel")
    ap.add_argument("--respostas", help="respostas separadas por virgula, para modo nao interativo")
    ap.add_argument("--arquivo-progresso", default="~/.claude/web3/progresso.json")
    a = ap.parse_args()

    banco = carregar_banco()
    prog = carregar_progresso(a.arquivo_progresso)

    if a.listar:
        cont = defaultdict(int)
        for q in banco:
            cont[q["modulo"]] += 1
        for m, c in sorted(cont.items()):
            print(f"  {m:<14}{c:>3} questoes   minimo {MINIMO.get(m, 7)}/10")
        print(f"  {'total':<14}{len(banco):>3}")
        return
    if a.progresso:
        if not prog:
            print("nenhum treino gravado ainda")
            return
        print(f"PROGRESSO  ·  {os.path.expanduser(a.arquivo_progresso)}\n")
        for m, r in sorted(prog.items()):
            minimo = MINIMO.get(m, 7)
            st = "liberado" if r["melhor"] >= minimo else "abaixo"
            print(f"  {m:<14} ultima {r['ultima']:>4g}  melhor {r['melhor']:>4g}  rodadas {r['rodadas']:>2}  minimo {minimo}  {st}  ({r.get('data', '')})")
        seg = prog.get("seguranca", {}).get("melhor", 0)
        print("\n  transacoes reais: " + ("liberadas" if seg >= 9 else "BLOQUEADAS ate 9/10 em seguranca"))
        return

    respostas = [int(x) for x in a.respostas.split(",")] if a.respostas else None
    if a.tudo:
        modulos = sorted({q["modulo"] for q in banco})
        for m in modulos:
            rodada(banco, m, min(a.n, 5), prog, a.seed, None)
    elif a.modulo:
        rodada(banco, a.modulo, a.n, prog, a.seed, respostas)
    else:
        ap.print_help()
        return
    salvar_progresso(a.arquivo_progresso, prog)
    print(f"\nprogresso gravado em {os.path.expanduser(a.arquivo_progresso)}")


if __name__ == "__main__":
    main()
