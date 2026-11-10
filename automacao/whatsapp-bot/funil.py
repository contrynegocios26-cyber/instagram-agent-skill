"""Funil de atendimento da MP Marcenaria no WhatsApp.

Lógica pura: recebe o estado da conversa e a mensagem do cliente e devolve o
novo estado e as mensagens a enviar. Não fala com a internet, então dá para
testar sem conta na Meta (veja test_funil.py).

Cada mensagem de saída é um dict:
  {"tipo": "texto", "texto": "..."}
  {"tipo": "botoes", "texto": "...", "botoes": [(id, titulo), ...]}   # até 3, título até 20 caracteres
  {"tipo": "lista", "texto": "...", "botao": "...", "itens": [(id, titulo), ...]}  # até 10, título até 24
"""
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")

VENDEDOR = "[seu nome]"  # trocado pela variável VENDEDOR_NOME no app.py
EMPRESA = "MP Marcenaria"

AMBIENTES = [
    ("amb_cozinha", "Cozinha"),
    ("amb_quarto", "Quarto / closet"),
    ("amb_banheiro", "Banheiro"),
    ("amb_sala", "Sala / painel ripado"),
    ("amb_porta", "Porta / esquadria"),
    ("amb_externa", "Área externa / deck"),
    ("amb_comercial", "Loja / comércio"),
    ("amb_outro", "Outro"),
]
FASES = [("fase_planta", "Na planta/construção"), ("fase_reboco", "Reboco ou pronta"), ("fase_reforma", "Reforma")]
PRAZOS = [("prazo_3m", "Até 3 meses"), ("prazo_6m", "3 a 6 meses"), ("prazo_pesq", "Só pesquisando")]
SAIR = {"sair", "parar", "pare", "stop", "cancelar", "não quero", "nao quero", "descadastrar"}


def _titulo(opcoes, id_):
    return dict(opcoes).get(id_)


def _escolha(opcoes, msg):
    """Aceita o id do botão, o título digitado ou o número da opção."""
    if msg.get("id") and _titulo(opcoes, msg["id"]):
        return msg["id"]
    t = (msg.get("texto") or "").strip().lower()
    for i, (id_, tit) in enumerate(opcoes, 1):
        if t in (str(i), tit.lower()) or (len(t) >= 4 and t in tit.lower()):
            return id_
    return None


def temperatura(lead):
    fase, prazo = lead.get("fase"), lead.get("prazo")
    if prazo == "prazo_pesq":
        return "Frio"
    if prazo == "prazo_3m" and fase in ("fase_reboco", "fase_reforma"):
        return "Quente"
    if prazo == "prazo_3m" or fase == "fase_reboco":
        return "Quente" if lead.get("tem_medidas") else "Morno"
    return "Morno"


def resumo(lead, telefone):
    amb = _titulo(AMBIENTES, lead.get("ambiente")) or lead.get("ambiente_texto", "")
    return (
        f"NOVO LEAD WHATSAPP — {datetime.now(TZ):%d/%m %H:%M}\n"
        f"Tipo: {lead.get('tipo', 'cliente')}\n"
        f"Nome: {lead.get('nome', '')}\n"
        f"Telefone: +{telefone}\n"
        f"Cidade: {lead.get('cidade', '')}\n"
        f"Ambiente: {amb}\n"
        f"Fase da obra: {_titulo(FASES, lead.get('fase')) or ''}\n"
        f"Prazo: {_titulo(PRAZOS, lead.get('prazo')) or ''}\n"
        f"Medidas/fotos: {'enviou' if lead.get('tem_medidas') else 'não enviou'}\n"
        f"Detalhes: {lead.get('detalhes', '')}\n"
        f"Temperatura: {temperatura(lead) if lead.get('tipo') == 'cliente' else '-'}\n"
        f"Próximo passo: chamar o cliente em até 1 hora"
    )


def boas_vindas(nome, horario_comercial=True, vendedor=VENDEDOR):
    oi = f"Oi, {nome.split()[0]}!" if nome else "Oi!"
    aviso = "" if horario_comercial else (
        "\n\nAgora estamos fora do horário, mas já vou adiantar seu atendimento por aqui "
        "e o(a) " + vendedor + " te chama no primeiro horário."
    )
    return {
        "tipo": "botoes",
        "texto": (
            f"{oi} 😊 Aqui é da {EMPRESA}, de Alto Paraná. Fazemos móveis planejados, "
            "portas pivotantes, esquadrias e painéis de madeira sob medida para todo o noroeste do Paraná."
            f"{aviso}\n\nComo posso te ajudar?"
        ),
        "botoes": [("menu_orcamento", "Quero um orçamento"), ("menu_arquiteto", "Sou arquiteto(a)"),
                   ("menu_outro", "Outro assunto")],
    }


def processar(estado, msg, telefone, nome="", horario_comercial=True, vendedor=VENDEDOR):
    """estado: dict salvo da conversa ({} se é a primeira mensagem).
    msg: {"texto": str|None, "id": id de botão/lista|None, "midia": bool}
    Devolve (novo_estado, mensagens, lead_concluido: str|None)."""
    e = dict(estado or {})
    lead = e.setdefault("lead", {})
    if nome and not lead.get("nome"):
        lead["nome"] = nome
    etapa = e.get("etapa")
    texto = (msg.get("texto") or "").strip()
    out = []

    if texto.lower() in SAIR:
        e["etapa"] = "optout"
        e["optout"] = True
        return e, [{"tipo": "texto", "texto": "Tudo bem, não vamos mais te mandar mensagens automáticas. "
                    "Se precisar, é só chamar aqui. 🙏"}], None

    if etapa in (None, "concluido", "optout") or texto.lower() in {"menu", "início", "inicio", "voltar"}:
        if etapa == "concluido" and texto.lower() not in {"menu", "início", "inicio", "voltar"}:
            # conversa já está com o vendedor: o robô não se mete
            return e, [], None
        e["etapa"] = "menu"
        e.pop("optout", None)
        return e, [boas_vindas(lead.get("nome", ""), horario_comercial, vendedor)], None

    if etapa == "menu":
        id_ = msg.get("id") or {"1": "menu_orcamento", "2": "menu_arquiteto", "3": "menu_outro"}.get(texto)
        if not id_:
            low = texto.lower()
            id_ = ("menu_orcamento" if any(k in low for k in ("orç", "orc", "preço", "preco", "valor", "quanto"))
                   else "menu_arquiteto" if "arquitet" in low or "designer" in low
                   else None)
        if id_ == "menu_orcamento":
            lead["tipo"] = "cliente"
            e["etapa"] = "ambiente"
            return e, [{"tipo": "lista", "texto": "Ótimo! Para começar: qual ambiente você quer fazer?",
                        "botao": "Escolher ambiente", "itens": AMBIENTES}], None
        if id_ == "menu_arquiteto":
            lead["tipo"] = "arquiteto"
            e["etapa"] = "arq_escritorio"
            return e, [{"tipo": "texto", "texto": "Que bom falar com você! 🙌 A MP trabalha junto com arquitetos e "
                        "designers da região: medição na obra com você, 3D em cima do seu projeto e 4% de "
                        "comissão em cada serviço fechado.\n\nQual o nome do seu escritório e em que cidade você atende?"}], None
        if id_ == "menu_outro":
            lead["tipo"] = "outro"
            e["etapa"] = "outro_texto"
            return e, [{"tipo": "texto", "texto": "Claro! Me conta em uma mensagem o que você precisa que eu já passo "
                        "para a pessoa certa."}], None
        return e, [{"tipo": "texto", "texto": "Desculpa, não entendi. 😅 Toque em uma das opções abaixo:"},
                   boas_vindas(lead.get("nome", ""), True, vendedor)], None

    if etapa == "ambiente":
        id_ = _escolha(AMBIENTES, msg)
        if id_:
            lead["ambiente"] = id_
        elif texto:
            lead["ambiente"], lead["ambiente_texto"] = "amb_outro", texto
        else:
            return e, [{"tipo": "texto", "texto": "Me diz qual ambiente, por favor (pode escrever)."}], None
        e["etapa"] = "cidade"
        return e, [{"tipo": "texto", "texto": "Perfeito! Em que cidade e bairro é a obra?"}], None

    if etapa == "cidade":
        if not texto:
            return e, [{"tipo": "texto", "texto": "Me escreve a cidade e o bairro da obra, por favor."}], None
        lead["cidade"] = texto
        e["etapa"] = "fase"
        return e, [{"tipo": "botoes", "texto": "E em que fase está a obra?", "botoes": FASES}], None

    if etapa == "fase":
        id_ = _escolha(FASES, msg)
        if not id_:
            return e, [{"tipo": "botoes", "texto": "Toque na fase mais parecida com a sua obra:", "botoes": FASES}], None
        lead["fase"] = id_
        e["etapa"] = "prazo"
        dica = ("\n\nDica: o melhor momento para medir o planejado é logo depois do reboco, antes do piso. "
                "Assim já prevemos tomadas e iluminação no lugar certo." if id_ == "fase_planta" else "")
        return e, [{"tipo": "botoes", "texto": "Para quando você precisa do móvel pronto?" + dica,
                    "botoes": PRAZOS}], None

    if etapa == "prazo":
        id_ = _escolha(PRAZOS, msg)
        if not id_:
            return e, [{"tipo": "botoes", "texto": "Toque em uma opção de prazo:", "botoes": PRAZOS}], None
        lead["prazo"] = id_
        e["etapa"] = "medidas"
        return e, [{"tipo": "botoes", "texto": (
            "Última coisa: se tiver, me manda aqui **fotos do espaço**, as **medidas aproximadas** ou a **planta** "
            "(e prints de referência do que você gosta). Ajuda muito no orçamento.\n\n"
            "Cada móvel da MP é feito do zero para o seu espaço, por isso o valor sai depois de ver o projeto. "
            "E a medição na obra é por nossa conta: se você fechar o serviço, ela não é cobrada."
        ).replace("**", "*"), "botoes": [("med_depois", "Mando depois"), ("med_nao", "Não tenho")]}], None

    if etapa == "medidas":
        if msg.get("midia") or (texto and msg.get("id") is None):
            lead["tem_medidas"] = True
            if texto:
                lead["detalhes"] = (lead.get("detalhes", "") + " " + texto).strip()
            if not e.get("agradeceu_midia"):
                e["agradeceu_midia"] = True
                return e, [{"tipo": "botoes", "texto": "Recebi! 👍 Quer mandar mais alguma foto ou medida?",
                            "botoes": [("med_fim", "Já mandei tudo")]}], None
            return e, [], None
        e["etapa"] = "concluido"
        lead["concluido_em"] = datetime.now(TZ).isoformat(timespec="minutes")
        quando = "em instantes" if horario_comercial else "no primeiro horário"
        return e, [{"tipo": "texto", "texto": (
            f"Pronto, {lead.get('nome', '').split()[0] if lead.get('nome') else 'tudo certo'}! ✅ "
            f"Já passei tudo para o(a) {vendedor}, que vai te chamar {quando} aqui mesmo para combinar os próximos passos.\n\n"
            "Enquanto isso, dá uma olhada nos nossos trabalhos: instagram.com/mp.marcenariaa"
        )}], resumo(lead, telefone)

    if etapa == "arq_escritorio":
        lead["detalhes"] = texto
        lead["cidade"] = texto
        e["etapa"] = "arq_projeto"
        return e, [{"tipo": "botoes", "texto": "Obrigado! Você tem algum projeto em fase de marcenaria agora?",
                    "botoes": [("arq_sim", "Tenho, quero orçar"), ("arq_futuro", "Para os próximos"),
                               ("arq_conhecer", "Só conhecer")]}], None

    if etapa == "arq_projeto":
        escolha = {"arq_sim": "Tem projeto para orçar agora", "arq_futuro": "Projetos futuros",
                   "arq_conhecer": "Quer conhecer a MP"}.get(msg.get("id"), texto)
        lead["detalhes"] = f"{lead.get('detalhes', '')} | {escolha}"
        e["etapa"] = "concluido"
        extra = (" Se quiser, já pode mandar o projeto (PDF ou imagens) aqui." if msg.get("id") == "arq_sim" else "")
        return e, [{"tipo": "texto", "texto": (
            f"Perfeito! O(a) {vendedor} cuida pessoalmente das parcerias com escritórios e vai te chamar "
            f"{'em instantes' if horario_comercial else 'no primeiro horário'}.{extra}"
        )}], resumo(lead, telefone)

    if etapa == "outro_texto":
        lead["detalhes"] = texto or "(mídia)"
        e["etapa"] = "concluido"
        return e, [{"tipo": "texto", "texto": f"Anotado! O(a) {vendedor} vai te responder "
                    f"{'em instantes' if horario_comercial else 'no primeiro horário'}. Obrigado por chamar a MP! 🙏"}], \
            resumo(lead, telefone)

    e["etapa"] = "menu"
    return e, [boas_vindas(lead.get("nome", ""), horario_comercial, vendedor)], None
