#!/usr/bin/env python3
"""
daily.py - o gerente do Growth Partner IA. Lê clientes.csv e pipeline.csv e
imprime as ações de hoje em ordem de impacto.

clientes.csv (uma linha por cliente):
  nome, mensalidade, inicio, fim_contrato, ultimo_relatorio, ultimo_contato,
  retorno_s1, retorno_s2, retorno_s3, retorno_s4, piloto, status, obs
    datas em AAAA-MM-DD; retorno_sN = retorno sobre a mensalidade nas últimas
    4 semanas (s1 = mais recente), número tipo 2.3; piloto = sim/nao;
    status = ativo | risco | pausado | encerrado

pipeline.csv (uma linha por prospect):
  nome, handle, estagio, data_estagio, reuniao, valor_proposta, obs
    estagio = contatado | respondeu | auditoria | reuniao | proposta |
              fechado | perdido
    data_estagio = quando entrou neste estágio; reuniao = data/hora da reunião

Uso
  python3 daily.py
  python3 daily.py --clientes c.csv --pipeline p.csv --meta-contatos 30
  python3 daily.py --hoje 2026-11-12          # para testar
"""

import argparse
import csv
import datetime as dt
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GP = os.path.normpath(os.path.join(HERE, "..", "..", "templates", "gp"))

PRIO = {"maxima": 0, "alta": 1, "media": 2, "baixa": 3}


def d(v):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return dt.date.fromisoformat(v[:10])
    except ValueError:
        return None


def f(v):
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


def yes(v):
    return str(v or "").strip().lower() in {"sim", "s", "yes", "1", "true"}


def read(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [r for r in csv.DictReader(fh) if (r.get("nome") or "").strip()]


def brl(x):
    s = "%.0f" % x
    g = []
    while s:
        g.insert(0, s[-3:])
        s = s[:-3]
    return "R$ " + ".".join(g)


def client_actions(rows, today):
    acts = []
    for r in rows:
        nome = r["nome"].strip()
        status = (r.get("status") or "ativo").strip().lower()
        if status in {"encerrado", "pausado"}:
            continue
        mens = f(r.get("mensalidade")) or 0
        if status == "risco":
            acts.append(("maxima", "RISCO", nome, "marcado como risco. Primeira ação do dia.", mens))
        ult_rel = d(r.get("ultimo_relatorio"))
        monday = today - dt.timedelta(days=today.weekday())
        if today.weekday() >= 1 and (ult_rel is None or ult_rel < monday):
            acts.append(("alta", "ENTREGA", nome, "relatório da semana não enviado. Enviar hoje.", mens))
        rets = [f(r.get("retorno_s%d" % i)) for i in (1, 2, 3)]
        rets = [x for x in rets if x is not None]
        if len(rets) == 3 and all(x < 1 for x in rets):
            acts.append(("alta", "RISCO", nome, "retorno %.1fx, %.1fx, %.1fx nas últimas 3 semanas. Ligar hoje e rever a oferta." % tuple(rets), mens * 4))
        ult_cont = d(r.get("ultimo_contato"))
        if ult_cont and (today - ult_cont).days >= 14:
            acts.append(("media", "RELAC", nome, "%d dias sem falar com o dono. Áudio de 1 minuto." % (today - ult_cont).days, mens))
        fim = d(r.get("fim_contrato"))
        if fim and 0 <= (fim - today).days <= 30:
            acts.append(("alta", "RENOV", nome, "contrato vence em %d dias. Preparar renovação com os números." % (fim - today).days, mens * 3))
        ini = d(r.get("inicio"))
        if yes(r.get("piloto")) and ini and 60 <= (today - ini).days <= 75:
            acts.append(("media", "CASO", nome, "piloto com %d dias. Gravar o depoimento esta semana." % (today - ini).days, mens))
    return acts


def pipeline_actions(rows, today, meta):
    acts = []
    novos_hoje = 0
    for r in rows:
        nome = r["nome"].strip()
        est = (r.get("estagio") or "").strip().lower()
        de = d(r.get("data_estagio"))
        dias = (today - de).days if de else None
        val = f(r.get("valor_proposta")) or 0
        reun = d(r.get("reuniao"))
        if est == "contatado" and de == today:
            novos_hoje += 1
        if est == "reuniao" and reun and 0 <= (reun - today).days <= 1:
            when = "hoje" if reun == today else "amanhã"
            acts.append(("alta", "NOVO", nome, "reunião %s. Montar a conta dele (orçamentos perdidos x ticket x fechamento)." % when, val or 2500))
        elif est == "proposta" and dias is not None and dias >= 2:
            acts.append(("alta", "NOVO", nome, "proposta há %d dias sem resposta. Follow-up curto, uma pergunta só." % dias, val or 2500))
        elif est == "respondeu" and dias is not None and dias >= 1:
            acts.append(("alta", "NOVO", nome, "respondeu há %d dia(s) e não recebeu a auditoria. Gravar e mandar hoje." % dias, 2500))
        elif est == "contatado" and dias in (3, 7, 14):
            acts.append(("media", "FOLLOW", nome, "follow-up do dia %d." % dias, 1000))
        elif est == "perdido" and dias is not None and dias >= 90:
            acts.append(("baixa", "LISTA", nome, "perdido há %d dias. Volta para a lista." % dias, 500))
    if novos_hoje < meta:
        acts.append(("alta", "PROSPEC", "", "%d/%d contatos hoje. Duas horas de prospecção antes de qualquer entrega." % (novos_hoje, meta), meta * 100))
    return acts, novos_hoje


def weekly(clientes, pipeline, today):
    ativos = [r for r in clientes if (r.get("status") or "ativo").strip().lower() in {"ativo", "risco"}]
    mrr = sum(f(r.get("mensalidade")) or 0 for r in ativos)
    semana = today - dt.timedelta(days=7)
    novos = [r for r in clientes if d(r.get("inicio")) and d(r.get("inicio")) >= semana]
    enc = [r for r in clientes if (r.get("status") or "").strip().lower() == "encerrado" and d(r.get("fim_contrato")) and d(r.get("fim_contrato")) >= semana]
    contatados = [r for r in pipeline if d(r.get("data_estagio")) and d(r.get("data_estagio")) >= semana]
    por = {}
    for r in contatados:
        e = (r.get("estagio") or "").strip().lower()
        por[e] = por.get(e, 0) + 1
    print("  RESUMO DA SEMANA")
    print("    MRR %s   ativos %d   novos %d   encerrados %d" % (brl(mrr), len(ativos), len(novos), len(enc)))
    print("    pipeline movido na semana: " + ", ".join("%s %d" % (k, v) for k, v in sorted(por.items())) if por else "    pipeline parado na semana")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clientes", default=os.path.join(GP, "clientes.csv"))
    ap.add_argument("--pipeline", default=os.path.join(GP, "pipeline.csv"))
    ap.add_argument("--meta-contatos", type=int, default=30)
    ap.add_argument("--hoje", help="AAAA-MM-DD, para testar")
    a = ap.parse_args()

    today = dt.date.fromisoformat(a.hoje) if a.hoje else dt.date.today()
    clientes = read(a.clientes)
    pipeline = read(a.pipeline)
    if not clientes and not pipeline:
        sys.exit("Sem dados. Preencha templates/gp/clientes.csv e templates/gp/pipeline.csv.")

    acts = client_actions(clientes, today)
    pacts, _ = pipeline_actions(pipeline, today, a.meta_contatos)
    acts += pacts
    acts.sort(key=lambda x: (PRIO[x[0]], -x[4]))

    ativos = [r for r in clientes if (r.get("status") or "ativo").strip().lower() in {"ativo", "risco"}]
    mrr = sum(f(r.get("mensalidade")) or 0 for r in ativos)
    dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    print("HOJE  %s %s        MRR %s   %d clientes   pipeline %d" % (
        dias[today.weekday()], today.strftime("%d/%m"), brl(mrr), len(ativos),
        sum(1 for r in pipeline if (r.get("estagio") or "").strip().lower() not in {"fechado", "perdido"})))
    print("=" * 72)
    if today.weekday() == 0:
        weekly(clientes, pipeline, today)
    top, rest = acts[:5], acts[5:]
    for i, (p, tag, nome, msg, _) in enumerate(top, 1):
        print(" %d. [%-7s] %-22s %s" % (i, tag, nome[:22], msg))
    if not top:
        print("  nada urgente. Então: 30 contatos, e conteúdo da semana.")
    if rest:
        print("-" * 72)
        print(" resto do dia: " + "; ".join("%s (%s)" % (n or tag.lower(), m.split(". ")[0].rstrip(".")) for _, tag, n, m, _ in rest))
    if len([x for x in acts if x[0] in {"maxima", "alta"}]) > 5:
        print(" AVISO: mais de cinco ações de alta prioridade. Falta assistente ou sobrou cliente errado.")


if __name__ == "__main__":
    main()
