---
name: gp-prospect
description: >-
  Growth Partner IA, etapa 1: prospecção. Monta a lista diária de negócios
  locais, pontua cada um por sinais de dor (WhatsApp sem resposta, Instagram
  parado, já anuncia), escreve a primeira mensagem personalizada e o roteiro do
  vídeo de auditoria. Use quando o usuário disser "prospectar", "lista de
  prospects", "quem eu contato hoje", "mensagem para marcenaria", "30 contatos"
  ou colar um perfil e perguntar se vale abordar.
---

# gp-prospect

A receita de hoje é a prospecção de 60 dias atrás. Esta skill existe para que
30 contatos por dia aconteçam todo dia útil, com mensagem que ninguém mais
mandou, para o negócio certo.

Leia `~/.claude/instagram/voice.md` (a voz de quem prospecta, não do cliente)
e `templates/gp/oferta.md` antes de escrever qualquer mensagem.

## Entrada

Uma destas três coisas:

1. **"Monta a lista de hoje"**: nicho e região. A skill devolve os critérios de
   busca (Google Maps, Instagram, hashtag local) e a planilha vazia em
   `templates/gp/prospects.csv` para o usuário preencher com 30 a 50 nomes.
   Não invente negócios. Não finja ter pesquisado o que não pesquisou.
2. **Um CSV preenchido** (o `prospects.csv`): a skill roda `score.py`, ranqueia
   e escreve a mensagem para os 10 primeiros.
3. **Um perfil colado** (bio, últimos posts, link, horário em que o usuário
   testou o WhatsApp e quando foi respondido): pontua esse um e escreve a
   mensagem.

## Pontuação

```bash
python3 score.py prospects.csv              # ranqueia
python3 score.py prospects.csv --top 10     # só os 10 melhores
python3 score.py prospects.csv --json
```

Os sinais e os pesos estão em `signals.json`. O que mais pesa é o teste de
resposta do WhatsApp feito pelo usuário, porque é a única dor que o prospect
não consegue negar na reunião. Peça sempre esse teste antes de abordar:
mandar "Oi, queria um orçamento de [produto]" fora do horário comercial e
anotar quando chegou a resposta.

Abaixo de 8 pontos, não aborde. O tempo vai para quem tem produto bom e
atendimento ruim, não para quem precisa ser convencido de que marketing
existe.

## A primeira mensagem

Três partes, nesta ordem, e nada mais:

1. **O achado específico.** Um projeto, um post, uma avaliação do Google.
   Pelo nome. "Vi a cozinha com ilha em nogueira que vocês postaram em
   outubro." Se não houver achado específico, não há mensagem.
2. **A dor comprovada.** O teste do WhatsApp, com horários. "Mandei mensagem
   ontem às 20h12 como cliente, fui respondido hoje às 9h40."
3. **O pedido pequeno.** "Gravei 4 minutos mostrando como resolver isso e
   encher a agenda. Posso mandar aqui?"

Máximo de 60 palavras. Sem "espero que esteja bem", sem "me chamo", sem
"somos uma agência". Sem emoji além de um, se a voz do usuário usar. Passe
por `/ig-human` antes de entregar.

Escreva **três variações** por prospect: uma pelo achado, uma pela dor, uma
pela conta (quantos orçamentos ele perde por mês com o tempo de resposta que
tem). O usuário manda uma. As outras servem de follow-up nos dias 3 e 7.

## O vídeo de auditoria (3 a 5 minutos, tela gravada)

Roteiro em `templates/gp/roteiro-auditoria.md`. Resumo:

- 0:00 Nome dele, o achado, por que você gravou.
- 0:30 Tela: o teste do WhatsApp, com os horários na tela.
- 1:30 Tela: o perfil, três coisas que custam venda (use `/ig-profile`).
- 3:00 Tela: o sistema rodando num cliente ou no seu negócio. Agente
  respondendo em segundos, agendamento caindo na agenda.
- 4:00 "Isso se monta em 7 dias. 20 minutos de conversa para eu entender
  seu volume. Qual horário amanhã, 10h ou 16h?"

Grave uma vez por prospect. Não reaproveite o mesmo vídeo com nome trocado,
a pessoa percebe.

## Follow-up

Dia 3: a segunda variação. Dia 7: a terceira, com a conta. Dia 14: "Fecho o
arquivo?" Depois disso, para. Quatro mensagens em duas semanas, nunca mais do
que isso. Quem não respondeu a quatro mensagens específicas não é cliente
agora; volta para a lista em 90 dias.

## Saída

```
PROSPECTS DE HOJE   terça 12/11   nicho: planejados   região: Curitiba
==================================================================
 1.  17  Marcenaria Alvorada     @marcenariaalvorada   WA 13h40 sem resp.
         msg A: Vi a cozinha com ilha em nogueira...
         msg B: ...
         msg C: ...
 2.  15  Planejados Reis         @planejadosreis       WA 2h10, anuncia
         ...
```

Números: contatos mandados, respostas, auditorias enviadas, reuniões
marcadas. Registre em `templates/gp/pipeline.csv`. O `/gp-daily` lê isso.

Nada é enviado por esta skill. O usuário manda cada mensagem.
