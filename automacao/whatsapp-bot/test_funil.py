"""Simula conversas completas sem precisar da Meta. Rode: python3 test_funil.py"""
from funil import processar

TEL = "5544999999999"


def conversa(passos, nome="Ana Souza", hc=True):
    estado, ultimo = {}, None
    for p in passos:
        estado, msgs, lead = processar(estado, p, TEL, nome, hc)
        for m in msgs:
            assert m["tipo"] in ("texto", "botoes", "lista")
            if m["tipo"] == "botoes":
                assert 1 <= len(m["botoes"]) <= 3 and all(len(t) <= 20 for _, t in m["botoes"]), m["botoes"]
            if m["tipo"] == "lista":
                assert len(m["itens"]) <= 10 and all(len(t) <= 24 for _, t in m["itens"])
        if lead:
            ultimo = lead
    return estado, ultimo


def t(texto=None, id=None, midia=False):
    return {"texto": texto, "id": id, "midia": midia}


# cliente completo, quente
e, lead = conversa([t("oi"), t(id="menu_orcamento"), t(id="amb_cozinha"), t("Paranavaí, Jd. Ouro Branco"),
                    t(id="fase_reboco"), t(id="prazo_3m"), t(midia=True), t(id="med_fim")])
assert e["etapa"] == "concluido" and "Temperatura: Quente" in lead and "Cozinha" in lead, lead

# cliente que digita em vez de tocar
e, lead = conversa([t("bom dia"), t("quanto custa um guarda roupa?"), t("2"), t("Loanda"), t("reforma"),
                    t("só pesquisando"), t(id="med_nao")])
assert "Quarto / closet" in lead and "Temperatura: Frio" in lead, lead

# arquiteto
e, lead = conversa([t("olá"), t(id="menu_arquiteto"), t("Studio X, Maringá"), t(id="arq_sim")])
assert "Tipo: arquiteto" in lead and "orçar agora" in lead

# depois de concluído o robô fica quieto
e2, msgs, _ = processar(e, t("tudo bem?"), TEL)
assert msgs == []

# opt-out
e3, msgs, _ = processar({}, t("parar"), TEL)
assert e3["optout"] and "não vamos mais" in msgs[0]["texto"]

# fora do horário
_, msgs, _ = processar({}, t("oi"), TEL, "Ana", horario_comercial=False)
assert "fora do horário" in msgs[0]["texto"]

print("OK: todos os cenários passaram")
