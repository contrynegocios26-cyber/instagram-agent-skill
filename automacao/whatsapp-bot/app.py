"""Servidor do robô de WhatsApp da MP Marcenaria (WhatsApp Cloud API oficial da Meta).

Recebe as mensagens pelo webhook, roda o funil (funil.py), responde o cliente,
salva o lead em leads.csv e avisa o vendedor no WhatsApp dele.

Variáveis de ambiente (veja .env.example):
  WA_TOKEN, WA_PHONE_ID, WA_VERIFY_TOKEN, WA_APP_SECRET, VENDEDOR_WHATSAPP, VENDEDOR_NOME
"""
import csv, hashlib, hmac, json, os, threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from flask import Flask, abort, request

from funil import AMBIENTES, FASES, PRAZOS, processar

TOKEN = os.environ.get("WA_TOKEN", "")
PHONE_ID = os.environ.get("WA_PHONE_ID", "")
VERIFY = os.environ.get("WA_VERIFY_TOKEN", "")
APP_SECRET = os.environ.get("WA_APP_SECRET", "")
VENDEDOR_TEL = os.environ.get("VENDEDOR_WHATSAPP", "")  # ex.: 5544999998888
VENDEDOR_NOME = os.environ.get("VENDEDOR_NOME", "vendedor")
DADOS = Path(os.environ.get("DADOS_DIR", "dados"))
TZ = ZoneInfo("America/Sao_Paulo")
API = "https://graph.facebook.com/v21.0"

DADOS.mkdir(exist_ok=True)
_lock = threading.Lock()
app = Flask(__name__)


def horario_comercial(agora=None):
    a = agora or datetime.now(TZ)
    if a.weekday() == 6:
        return False
    if a.weekday() == 5:
        return 8 <= a.hour < 12
    return 8 <= a.hour < 18


def _estado_path(tel):
    return DADOS / f"conversa_{tel}.json"


def carregar(tel):
    p = _estado_path(tel)
    return json.loads(p.read_text()) if p.exists() else {}


def salvar(tel, e):
    _estado_path(tel).write_text(json.dumps(e, ensure_ascii=False, indent=1))


def enviar(tel, m):
    if m["tipo"] == "texto":
        body = {"type": "text", "text": {"body": m["texto"], "preview_url": True}}
    elif m["tipo"] == "botoes":
        body = {"type": "interactive", "interactive": {
            "type": "button", "body": {"text": m["texto"]},
            "action": {"buttons": [{"type": "reply", "reply": {"id": i, "title": t}} for i, t in m["botoes"]]}}}
    else:
        body = {"type": "interactive", "interactive": {
            "type": "list", "body": {"text": m["texto"]},
            "action": {"button": m["botao"], "sections": [{"title": "Opções", "rows": [
                {"id": i, "title": t} for i, t in m["itens"]]}]}}}
    payload = {"messaging_product": "whatsapp", "to": tel, **body}
    if not TOKEN:
        print("[simulação] ->", tel, json.dumps(payload, ensure_ascii=False)[:300])
        return
    r = requests.post(f"{API}/{PHONE_ID}/messages", json=payload,
                      headers={"Authorization": f"Bearer {TOKEN}"}, timeout=15)
    if r.status_code >= 300:
        print("Erro ao enviar:", r.status_code, r.text[:300])


def registrar_lead(tel, estado, resumo):
    lead = estado.get("lead", {})
    novo = not Path(DADOS / "leads.csv").exists()
    with _lock, open(DADOS / "leads.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["data", "telefone", "nome", "tipo", "cidade", "ambiente", "fase", "prazo",
                        "tem_medidas", "detalhes", "status"])
        w.writerow([datetime.now(TZ).strftime("%d/%m/%Y %H:%M"), tel, lead.get("nome", ""), lead.get("tipo", ""),
                    lead.get("cidade", ""), lead.get("ambiente_texto") or dict(AMBIENTES).get(lead.get("ambiente"), ""),
                    dict(FASES).get(lead.get("fase"), ""), dict(PRAZOS).get(lead.get("prazo"), ""), lead.get("tem_medidas", False),
                    lead.get("detalhes", ""), "Novo"])
    if VENDEDOR_TEL:
        # Funciona dentro da janela de 24 h: o vendedor deve mandar qualquer mensagem
        # para o número da MP uma vez por dia (ex.: "bom dia"). Fora disso, use o
        # modelo "aviso_novo_lead" de templates.md.
        enviar(VENDEDOR_TEL, {"tipo": "texto", "texto": resumo})


def assinatura_ok(req):
    if not APP_SECRET:
        return True
    sig = req.headers.get("X-Hub-Signature-256", "")
    esperado = "sha256=" + hmac.new(APP_SECRET.encode(), req.get_data(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, esperado)


@app.get("/webhook")
def verificar():
    if VERIFY and request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY:
        return request.args.get("hub.challenge", "")
    abort(403)


@app.post("/webhook")
def receber():
    if not assinatura_ok(request):
        abort(403)
    dados = request.get_json(silent=True) or {}
    for entry in dados.get("entry", []):
        for ch in entry.get("changes", []):
            v = ch.get("value", {})
            nomes = {c["wa_id"]: c.get("profile", {}).get("name", "") for c in v.get("contacts", [])}
            for m in v.get("messages", []):
                tel = m["from"]
                if tel == VENDEDOR_TEL:
                    continue  # mensagens do vendedor só abrem a janela de 24 h
                msg = {"texto": None, "id": None, "midia": False}
                if m["type"] == "text":
                    msg["texto"] = m["text"]["body"]
                elif m["type"] == "interactive":
                    it = m["interactive"]
                    r = it.get("button_reply") or it.get("list_reply") or {}
                    msg["id"], msg["texto"] = r.get("id"), r.get("title")
                elif m["type"] == "button":  # resposta a botão de modelo
                    msg["texto"] = m["button"].get("text")
                elif m["type"] in ("image", "video", "document", "audio"):
                    msg["midia"] = True
                    msg["texto"] = (m.get(m["type"], {}) or {}).get("caption")
                with _lock:
                    estado = carregar(tel)
                    novo, saidas, resumo = processar(estado, msg, tel, nomes.get(tel, ""),
                                                     horario_comercial(), VENDEDOR_NOME)
                    salvar(tel, novo)
                for s in saidas:
                    enviar(tel, s)
                if resumo:
                    registrar_lead(tel, novo, resumo)
    return "ok"


@app.get("/")
def saude():
    return "Robô MP Marcenaria no ar"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
