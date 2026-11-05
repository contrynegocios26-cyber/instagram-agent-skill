#!/usr/bin/env python3
"""Gera o plano de 30 ou 90 dias do pack Web3 a partir do perfil do usuario.

Sem dependencias, sem rede. Le ~/.claude/web3/perfil.md (ou flags) e escreve
~/.claude/web3/plano.md.

    python3 plano.py --perfil ~/.claude/web3/perfil.md
    python3 plano.py --nivel zero --horas 5 --capital 0 --dias 90
"""
import argparse
import os
import re
import sys
from datetime import date, timedelta

TRILHAS = {
    "construtor": ["web3-dev", "web3-renda", "web3-onchain"],
    "operador": ["web3-defi", "web3-onchain", "web3-risco"],
    "cacador": ["web3-airdrops", "web3-renda", "web3-onchain"],
    "prestador": ["web3-renda", "web3-fundamentos", "web3-seguranca"],
}

# Semana 1 e igual para todo mundo. Cada item: (agente, tarefa, minutos).
SEMANA_BASE = [
    ("web3-seguranca", "Criar carteira nova. Seed no papel, duas copias, teste de restauracao.", 40),
    ("web3-fundamentos", "O que e uma chave, um endereco, uma transacao, o gas. Uma transacao de centavos em L2 ou testnet.", 40),
    ("web3-fundamentos", "L1, L2, stablecoin, token, NFT: vocabulario minimo, com um exemplo real de cada.", 40),
    ("web3-seguranca", "Os quatro golpes que mais tiram dinheiro de iniciante. Revogar approvals. Carteira de queima vs cofre.", 40),
    ("web3-fundamentos", "Ler um explorador de blocos: achar sua transacao, o gas pago, o contrato chamado.", 30),
    ("web3-risco", "Definir capital de risco, tamanho maximo de posicao e horario de nao operar. Gravar no perfil.", 30),
    ("web3-treino", "Treino de seguranca. Nota minima 9/10 para avancar. Repetir ate passar.", 30),
]

SEMANAS_TRILHA = {
    "construtor": [
        [("web3-dev", "Ambiente: Node, Foundry ou Hardhat, Remix. Primeiro contrato (contador) compilado e deployado na testnet.", 60),
         ("web3-dev", "Tipos, mapping, eventos, modifiers. Um token ERC-20 do zero, sem copiar.", 60),
         ("web3-dev", "Testes. Um teste por funcao publica. Nada e 'pronto' sem teste.", 60),
         ("web3-dev", "Os 5 bugs classicos: reentrancy, overflow antigo, access control, tx.origin, front-running.", 60),
         ("web3-renda", "Criar perfil em 2 plataformas de bounty. Ler 10 bounties abertos e anotar o que pedem.", 45),
         ("web3-dev", "Ler um contrato real verificado no explorador e explicar o que ele faz, linha a linha.", 60),
         ("web3-treino", "Treino de dev + seguranca.", 30)],
        [("web3-dev", "Projeto da semana: um contrato util (cofre com prazo, split de pagamento, votacao simples). Spec primeiro.", 60),
         ("web3-dev", "Implementar e testar. Cobertura das funcoes publicas.", 90),
         ("web3-dev", "Frontend minimo com wallet connect lendo e escrevendo no contrato.", 90),
         ("web3-renda", "Resolver um bounty pequeno de verdade ou abrir um PR em projeto open source Web3.", 90),
         ("web3-dev", "Deploy na testnet, README com o que faz, o que nao faz e o que falta auditar.", 45),
         ("web3-renda", "Publicar o projeto. Um post tecnico curto, com o link. Isso vira portfolio.", 45),
         ("web3-treino", "Treino de dev.", 30)],
        [("web3-renda", "Semana de prospeccao: 10 contatos, 3 propostas, 1 bounty em andamento.", 60),
         ("web3-dev", "Gas optimization e padroes: proxy, factory, pull over push.", 60),
         ("web3-onchain", "Ler o tokenomics de 2 projetos e aplicar o checklist.", 45),
         ("web3-dev", "Segundo projeto ou extensao do primeiro, orientado por um bounty real.", 90),
         ("web3-renda", "Follow-up das propostas. Registrar no diario: enviado, respondido, fechado.", 30),
         ("web3-risco", "Revisao de custos: gas gasto, tempo gasto, dinheiro recebido.", 30),
         ("web3-treino", "Treino de todos os modulos tocados.", 45)],
    ],
    "operador": [
        [("web3-defi", "Stablecoins: tipos, riscos de cada tipo, onde cada uma rende e por que.", 45),
         ("web3-defi", "Lending: depositar US$ 10 em um protocolo grande em L2. Ler o APY, a utilizacao, o risco de liquidacao.", 45),
         ("web3-defi", "AMM e liquidez: o que e impermanent loss. Rodar defi_calc.py com 3 cenarios antes de tocar em LP.", 45),
         ("web3-onchain", "O checklist de due diligence. Aplicar em 1 protocolo que voce usou.", 45),
         ("web3-risco", "Journal da primeira posicao: tese, tamanho, saida, o que invalida.", 30),
         ("web3-seguranca", "Approvals: revisar e revogar tudo que foi criado nesta semana.", 20),
         ("web3-treino", "Treino de DeFi + risco.", 30)],
        [("web3-defi", "Primeira posicao real dentro do tamanho autorizado pelo /web3-risco. Stablecoin em lending, nada alem disso.", 45),
         ("web3-onchain", "Ler 3 tokenomics. Para cada um: oferta, desbloqueios, quem detem, de onde vem o rendimento.", 60),
         ("web3-defi", "Taxas e pontes: calcular o custo total de entrar e sair antes de entrar.", 30),
         ("web3-risco", "Simular o pior cenario da posicao com risco.py. Se nao aguenta, reduzir.", 30),
         ("web3-onchain", "Tutorial de dashboards publicos: TVL, volume, receita de protocolo. Anotar 3 numeros.", 45),
         ("web3-defi", "Journal: o que a posicao rendeu em 7 dias, em moeda e em percentual, descontando gas.", 20),
         ("web3-treino", "Treino de on-chain.", 30)],
        [("web3-defi", "Segunda estrategia, so se a primeira esta registrada e entendida. Nunca duas novas na mesma semana.", 45),
         ("web3-risco", "Revisao de carteira: exposicao por protocolo, por rede, por tipo de risco.", 45),
         ("web3-onchain", "Um protocolo com a bandeira vermelha mais comum do checklist. Explicar por que nao entrar.", 45),
         ("web3-renda", "Capital tambem pode render por servico: 1 forma de monetizar o que voce aprendeu.", 30),
         ("web3-risco", "Calcular imposto estimado sobre o que rendeu. Registrar para declaracao.", 30),
         ("web3-defi", "Rebalancear ou sair, conforme a regra escrita na semana 2. Nunca por impulso.", 30),
         ("web3-treino", "Treino completo.", 45)],
    ],
    "cacador": [
        [("web3-airdrops", "O que e um airdrop retroativo, o que e Sybil, por que uma carteira bem usada vale mais que dez vazias.", 45),
         ("web3-airdrops", "Escolher 3 protocolos pelo criterio da skill. Registrar: por que esses, custo semanal estimado.", 60),
         ("web3-seguranca", "Carteira dedicada para farming, separada do cofre. Nunca a mesma seed.", 30),
         ("web3-airdrops", "Primeira rotina: 1 acao real em cada protocolo, custo de gas anotado.", 45),
         ("web3-renda", "Conteudo: um resumo honesto da semana publicado. Audiencia e ativo tambem.", 45),
         ("web3-risco", "Teto de gasto mensal em gas e taxas. Gravar.", 20),
         ("web3-treino", "Treino de airdrops + seguranca.", 30)],
        [("web3-airdrops", "Rotina semanal, dia a dia. Diversificar tipo de acao: swap, bridge, LP pequena, governanca.", 45),
         ("web3-onchain", "Ler o tokenomics anunciado de 2 projetos que ja fizeram airdrop. O que premiaram de verdade?", 45),
         ("web3-airdrops", "Rastrear: planilha com protocolo, data, acao, custo, carteira.", 30),
         ("web3-renda", "Comunidade: entrar em 2 Discords de projeto, contribuir com algo util (traducao, bug report, resposta).", 45),
         ("web3-seguranca", "Revogar approvals da semana. Verificar que nenhum link veio de DM.", 20),
         ("web3-renda", "Segundo conteudo publicado.", 45),
         ("web3-treino", "Treino de on-chain.", 30)],
        [("web3-airdrops", "Revisao fria: custo acumulado contra valor esperado. Cortar o protocolo mais caro e menos provavel.", 45),
         ("web3-renda", "Transformar a rotina em servico: guia, planilha, grupo. Primeiro preco.", 60),
         ("web3-airdrops", "Rotina semanal.", 45),
         ("web3-onchain", "Um protocolo novo pelo checklist. Entrar so se passar.", 45),
         ("web3-risco", "Teto de gasto: respeitado ou nao? Numero.", 20),
         ("web3-renda", "Terceiro conteudo. Metricas dos tres.", 45),
         ("web3-treino", "Treino completo.", 45)],
    ],
    "prestador": [
        [("web3-renda", "Mapear a habilidade para o mercado Web3: quem contrata, onde, por quanto. Tres exemplos reais.", 60),
         ("web3-renda", "Portfolio minimo: 1 peca feita para um projeto Web3 real, nao fictício.", 90),
         ("web3-fundamentos", "Vocabulario suficiente para conversar com cliente: 20 termos, um exemplo cada.", 45),
         ("web3-renda", "Perfil em 2 plataformas de freelance/bounty Web3 e em 1 comunidade do nicho.", 45),
         ("web3-seguranca", "Como receber em stablecoin sem ser enganado: endereco, rede, confirmacao, nunca 'devolver a diferenca'.", 30),
         ("web3-renda", "Tres propostas enviadas. Curtas, com a peca do portfolio.", 60),
         ("web3-treino", "Treino de fundamentos + seguranca.", 30)],
        [("web3-renda", "Follow-up das propostas. Cinco novas. Registrar taxa de resposta.", 60),
         ("web3-renda", "Precificar em USDC. Entender o que a conversao para BRL custa e como declarar.", 45),
         ("web3-fundamentos", "O produto do cliente: ler a doc de um protocolo e explicar em 5 linhas para leigo.", 45),
         ("web3-renda", "Segunda peca de portfolio, agora no nicho onde houve mais resposta.", 90),
         ("web3-renda", "Oferta publica: um post dizendo o que voce faz por projetos Web3, com os dois trabalhos.", 45),
         ("web3-risco", "Registrar: horas investidas, dinheiro recebido ou agendado.", 20),
         ("web3-treino", "Treino de fundamentos.", 30)],
        [("web3-renda", "Fechar o primeiro trabalho ou diagnosticar por que nao fechou: preco, nicho, prova ou volume.", 60),
         ("web3-renda", "Dez contatos diretos com projetos pequenos que acabaram de lancar.", 60),
         ("web3-fundamentos", "Um conceito tecnico a mais por semana, escolhido pelo que os clientes perguntam.", 45),
         ("web3-renda", "Entregar. Pedir depoimento. Pedir indicacao.", 60),
         ("web3-seguranca", "Receber: conferir rede, endereco e valor. Mover para o cofre.", 20),
         ("web3-risco", "Revisao: receita, horas, valor-hora real.", 30),
         ("web3-treino", "Treino completo.", 45)],
    ],
}

SEMANA_REVISAO = [
    ("web3-treino", "Treino de todos os modulos tocados nas 3 semanas. Anotar a nota de cada um.", 60),
    ("web3-risco", "Balanco: dinheiro que entrou, dinheiro que saiu, separados. Horas previstas contra feitas.", 45),
    ("web3-mentor", "Ler o diario inteiro. O que funcionou, o que nao, o que foi so gasto.", 45),
    ("web3-mentor", "Decidir: manter trilha, trocar trilha ou juntar duas. Escrever o porque.", 30),
    ("web3-seguranca", "Auditoria da carteira: approvals, extensoes, onde a seed esta, quem mais sabe.", 30),
    ("web3-mentor", "Novo plano de 30 dias, gerado com o perfil atualizado.", 30),
    ("", "Descanso. Sem tela de preco.", 0),
]


def ler_perfil(caminho):
    """Extrai nivel, horas, capital e trilha do perfil.md de forma tolerante."""
    dados = {"nivel": None, "horas": None, "capital": None, "trilha": None, "divida": None}
    try:
        texto = open(os.path.expanduser(caminho), encoding="utf-8").read().lower()
    except OSError:
        return dados
    m = re.search(r"horas por semana[^:]*:\s*\(?([0-9]+)", texto)
    if m:
        dados["horas"] = int(m.group(1))
    m = re.search(r"posso perder[^:]*:\s*\(?[^0-9]*([0-9][0-9.,]*)", texto)
    if m:
        dados["capital"] = float(m.group(1).replace(".", "").replace(",", "."))
    m = re.search(r"n[ií]vel em web3[^:]*:\s*\(?([a-zá-ú ]+)", texto)
    if m:
        dados["nivel"] = m.group(1).strip()
    m = re.search(r"juros acima de 2%[^:]*:\s*\(?\s*(sim|n[aã]o)", texto)
    if m:
        dados["divida"] = m.group(1).startswith("sim")
    m = re.search(r"trilha[^:]*:\s*\(?\s*(construtor|operador|ca[cç]ador|prestador)", texto)
    if m:
        dados["trilha"] = m.group(1).replace("ç", "c")
    return dados


def escolher_trilha(nivel, horas, capital, divida, habilidades_dev=False):
    if divida:
        return "construtor" if habilidades_dev else "prestador"
    if habilidades_dev and horas >= 8:
        return "construtor"
    if capital >= 3000 and horas >= 5:
        return "operador"
    if capital < 500 and horas >= 8:
        return "cacador"
    return "prestador"


def escalar(itens, horas_semana):
    """Encaixa os 7 itens da semana no tempo disponivel, cortando pelo fim."""
    orcamento = horas_semana * 60
    total = sum(m for _, _, m in itens)
    if total <= orcamento:
        return itens
    fator = orcamento / total
    return [(a, t, max(15, int(m * fator))) if m else (a, t, m) for a, t, m in itens]


def montar(trilha, horas, dias, inicio):
    semanas = [SEMANA_BASE] + SEMANAS_TRILHA[trilha] + [SEMANA_REVISAO]
    ciclo = len(semanas)
    linhas = []
    dia = 0
    while dia < dias:
        semana_idx = (dia // 7) % ciclo
        itens = escalar(semanas[semana_idx], horas)
        for agente, tarefa, minutos in itens:
            if dia >= dias:
                break
            data = inicio + timedelta(days=dia)
            tag = f"/{agente}" if agente else "—"
            linhas.append(f"| {dia + 1} | {data.strftime('%d/%m')} | {tag} | {tarefa} | {minutos} |")
            dia += 1
    return linhas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--perfil", default="~/.claude/web3/perfil.md")
    ap.add_argument("--nivel", choices=["zero", "carteira", "defi", "dev"])
    ap.add_argument("--horas", type=float)
    ap.add_argument("--capital", type=float, help="capital de risco, em qualquer moeda")
    ap.add_argument("--trilha", choices=list(TRILHAS))
    ap.add_argument("--dev", action="store_true", help="sabe ou quer aprender a programar")
    ap.add_argument("--divida", action="store_true", help="tem divida acima de 2%% ao mes")
    ap.add_argument("--dias", type=int, default=30)
    ap.add_argument("--inicio", help="AAAA-MM-DD, padrao hoje")
    ap.add_argument("--out", default="~/.claude/web3/plano.md")
    args = ap.parse_args()

    p = ler_perfil(args.perfil)
    horas = args.horas or p["horas"] or 5
    capital = args.capital if args.capital is not None else (p["capital"] or 0)
    nivel = args.nivel or p["nivel"] or "zero"
    divida = args.divida or bool(p["divida"])
    dev = args.dev or nivel == "dev"
    trilha = args.trilha or p["trilha"] or escolher_trilha(nivel, horas, capital, divida, dev)
    inicio = date.fromisoformat(args.inicio) if args.inicio else date.today()

    cab = [
        f"# Plano Web3 · {args.dias} dias · trilha {trilha.capitalize()}",
        "",
        f"- Inicio: {inicio.isoformat()}",
        f"- Horas por semana: {horas:g}",
        f"- Capital de risco declarado: {capital:g}",
        f"- Nivel: {nivel}",
        f"- Divida cara: {'sim, e por isso a trilha nao usa capital' if divida else 'nao'}",
        "",
        "Semana 1 e sempre a base (carteira, seguranca, vocabulario). Nada avanca sem nota 9/10 no treino de seguranca.",
        "",
        "| dia | data | agente | tarefa | min |",
        "| --- | --- | --- | --- | --- |",
    ]
    linhas = montar(trilha, horas, args.dias, inicio)
    saida = "\n".join(cab + linhas) + "\n"

    out = os.path.expanduser(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(saida)
    sys.stdout.write(saida)
    sys.stderr.write(f"\nplano gravado em {out}\n")


if __name__ == "__main__":
    main()
