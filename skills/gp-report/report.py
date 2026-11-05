#!/usr/bin/env python3
"""
report.py - soma a semana de um cliente do Growth Partner IA e calcula a conta.

Lê o CSV de métricas (uma linha por dia, formato de templates/gp/metricas.csv),
soma a semana pedida (segunda a domingo), compara com a anterior, calcula o
retorno sobre a mensalidade e aponta o gargalo do funil.

Colunas esperadas:
  data            AAAA-MM-DD
  conversas       conversas novas no WhatsApp
  fora_horario    quantas dessas chegaram fora do horário comercial
  resposta_seg    tempo médio de resposta do agente, em segundos
  agendamentos    visitas/consultas agendadas
  orcamentos      orçamentos enviados
  vendas          vendas fechadas atribuídas ao sistema
  valor_vendas    soma em reais das vendas fechadas
  valor_aberto    soma em reais dos orçamentos ainda abertos
  passados_humano conversas que o agente passou para humano
  obs             texto livre

Uso
  python3 report.py metricas.csv --mensalidade 2500
  python3 report.py metricas.csv --mensalidade 2500 --semana 2026-11-10
  python3 report.py metricas.csv --mensalidade 2500 --json
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys

NUM = ["conversas", "fora_horario", "agendamentos", "orcamentos", "vendas",
       "valor_vendas", "valor_aberto", "passados_humano"]


def parse_num(v):
    """'4.8' -> 4.8, '4,8' -> 4.8, 'R$ 12.000' -> 12000, '1.234,56' -> 1234.56, '' -> None."""
    v = str(v or "").strip().replace("R$", "").replace(" ", "")
    if v == "":
        return None
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".")
    elif "," in v:
        v = v.replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", v):
        v = v.replace(".", "")
    try:
        return float(v)
    except ValueError:
        return None


def num(v):
    x = parse_num(v)
    return 0.0 if x is None else x


def brl(x):
    s = "%.2f" % x
    inteiro, dec = s.split(".")
    grupos = []
    while inteiro:
        grupos.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    return "R$ " + ".".join(grupos) + "," + dec


def monday_of(d):
    return d - dt.timedelta(days=d.weekday())


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = []
        for r in csv.DictReader(f):
            d = (r.get("data") or "").strip()
            if not d:
                continue
            try:
                r["_d"] = dt.date.fromisoformat(d)
            except ValueError:
                sys.exit("Data inválida: %r (use AAAA-MM-DD)" % d)
            rows.append(r)
    if not rows:
        sys.exit("CSV sem linhas. Preencha templates/gp/metricas.csv, uma linha por dia.")
    return rows


def week_sum(rows, monday):
    sunday = monday + dt.timedelta(days=6)
    sel = [r for r in rows if monday <= r["_d"] <= sunday]
    tot = {k: sum(num(r.get(k)) for r in sel) for k in NUM}
    resp = [num(r.get("resposta_seg")) for r in sel if str(r.get("resposta_seg") or "").strip()]
    tot["resposta_seg"] = (sum(resp) / len(resp)) if resp else None
    tot["dias"] = len(sel)
    tot["obs"] = [r.get("obs", "").strip() for r in sel if (r.get("obs") or "").strip()]
    return tot


def rate(a, b):
    return (a / b) if b else 0.0


def delta(cur, prev):
    if not prev:
        return None
    return (cur - prev) / prev * 100.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--mensalidade", type=float, required=True, help="mensalidade do cliente em reais")
    ap.add_argument("--semana", help="qualquer data da semana desejada (AAAA-MM-DD); padrão: última semana completa")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = load(a.csv)
    if a.semana:
        monday = monday_of(dt.date.fromisoformat(a.semana))
    else:
        last = max(r["_d"] for r in rows)
        monday = monday_of(last)
        if last.weekday() < 6 and monday == monday_of(dt.date.today()):
            monday -= dt.timedelta(days=7)
    cur = week_sum(rows, monday)
    prev = week_sum(rows, monday - dt.timedelta(days=7))
    if cur["dias"] == 0:
        sys.exit("Nenhuma linha na semana de %s. Confira as datas." % monday)

    semanal = a.mensalidade * 12 / 52
    retorno = rate(cur["valor_vendas"], semanal)
    funil = {
        "conversa->agendamento": rate(cur["agendamentos"], cur["conversas"]),
        "agendamento->orcamento": rate(cur["orcamentos"], cur["agendamentos"]),
        "orcamento->venda": rate(cur["vendas"], cur["orcamentos"]),
    }
    funil_prev = {
        "conversa->agendamento": rate(prev["agendamentos"], prev["conversas"]),
        "agendamento->orcamento": rate(prev["orcamentos"], prev["agendamentos"]),
        "orcamento->venda": rate(prev["vendas"], prev["orcamentos"]),
    }
    gargalo = None
    pior = 0.0
    for k in funil:
        if funil_prev[k] > 0:
            queda = funil_prev[k] - funil[k]
            if queda > pior and queda > 0.05:
                pior, gargalo = queda, k
    if gargalo is None:
        # sem semana anterior, aponta a etapa mais fraca em termos absolutos
        ref = {"conversa->agendamento": 0.20, "agendamento->orcamento": 0.60, "orcamento->venda": 0.25}
        gaps = {k: ref[k] - funil[k] for k in funil}
        k = max(gaps, key=gaps.get)
        gargalo = k if gaps[k] > 0 else None

    alertas = []
    if cur["resposta_seg"] is not None and cur["resposta_seg"] > 60:
        alertas.append("Resposta média de %.0fs. Acima de 60s é problema técnico: resolver hoje." % cur["resposta_seg"])
    d_conv = delta(cur["conversas"], prev["conversas"])
    if d_conv is not None and d_conv < -30:
        alertas.append("Conversas caíram %.0f%% contra a semana anterior. Conteúdo ou anúncio parou? Verificar antes de enviar." % abs(d_conv))
    if cur["vendas"] == 0 and cur["agendamentos"] >= 5:
        alertas.append("Agendamentos normais e zero venda. Se repetir 3 semanas, o gargalo é o fechamento do cliente: ligar, não relatar.")
    if retorno < 1 and cur["dias"] >= 5:
        alertas.append("Retorno de %.1fx sobre a mensalidade nesta semana. Quatro semanas assim e a conta não fecha para ele." % retorno)

    out = {
        "semana": "%s a %s" % (monday.strftime("%d/%m"), (monday + dt.timedelta(days=6)).strftime("%d/%m")),
        "dias_com_dados": cur["dias"],
        "conversas": int(cur["conversas"]),
        "fora_horario": int(cur["fora_horario"]),
        "resposta_seg": cur["resposta_seg"],
        "agendamentos": int(cur["agendamentos"]),
        "orcamentos": int(cur["orcamentos"]),
        "vendas": int(cur["vendas"]),
        "valor_vendas": cur["valor_vendas"],
        "valor_aberto": cur["valor_aberto"],
        "passados_humano": int(cur["passados_humano"]),
        "mensalidade_semanal": semanal,
        "retorno_x": retorno,
        "funil": funil,
        "variacao_pct": {k: delta(cur[k], prev[k]) for k in ["conversas", "agendamentos", "orcamentos", "vendas", "valor_vendas"]},
        "gargalo": gargalo,
        "alertas": alertas,
        "obs": cur["obs"],
    }
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    def dl(k):
        v = out["variacao_pct"][k]
        return "" if v is None or abs(v) < 15 else "  (%+.0f%%)" % v

    print("SEMANA %s   %d dias com dados" % (out["semana"], cur["dias"]))
    print("=" * 64)
    print("  A CONTA")
    print("    vendas fechadas pelo sistema   %s%s" % (brl(cur["valor_vendas"]), dl("valor_vendas")))
    print("    orçamentos em aberto           %s" % brl(cur["valor_aberto"]))
    print("    mensalidade (proporcional)     %s" % brl(semanal))
    print("    retorno                        %.1fx" % retorno)
    print()
    print("  O FUNIL")
    print("    conversas        %4d%s   (%d fora do horário)" % (cur["conversas"], dl("conversas"), cur["fora_horario"]))
    if cur["resposta_seg"] is not None:
        print("    resposta média   %4.0fs" % cur["resposta_seg"])
    print("    agendamentos     %4d%s   %.0f%% das conversas" % (cur["agendamentos"], dl("agendamentos"), funil["conversa->agendamento"] * 100))
    print("    orçamentos       %4d%s   %.0f%% dos agendamentos" % (cur["orcamentos"], dl("orcamentos"), funil["agendamento->orcamento"] * 100))
    print("    vendas           %4d%s   %.0f%% dos orçamentos" % (cur["vendas"], dl("vendas"), funil["orcamento->venda"] * 100))
    print("    passados p/ humano %2d" % cur["passados_humano"])
    print()
    print("  GARGALO   %s" % (gargalo or "nenhum acima do esperado"))
    for al in alertas:
        print("  ALERTA    %s" % al)
    for o in cur["obs"]:
        print("  obs       %s" % o)
    print("-" * 64)
    print("Agora escreva as cinco linhas (SKILL.md). A conta vem primeiro.")


if __name__ == "__main__":
    main()
