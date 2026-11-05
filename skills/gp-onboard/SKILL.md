---
name: gp-onboard
description: >-
  Growth Partner IA, etapa 2: implantação de um cliente novo em 7 dias. A partir
  da transcrição da reunião de onboarding, escreve o voice.md do cliente, a base
  de conhecimento e o prompt do agente de WhatsApp, o plano do primeiro mês e a
  lista de vídeos que o dono grava. Use quando o usuário disser "fechei um
  cliente", "onboarding", "montar o agente do cliente", "base de conhecimento"
  ou colar a transcrição de uma reunião com um cliente novo.
---

# gp-onboard

Implantação ruim é o motivo número um de churn no mês 4. O cliente não
cancela por preço; cancela porque o agente respondeu errado na segunda
semana e ele parou de confiar. Esta skill existe para que a implantação seja
a mesma, inteira, todas as vezes.

## Entrada

A transcrição (ou as anotações) da reunião de onboarding de 60 minutos. O
roteiro da reunião está em `templates/gp/onboarding-reuniao.md`. Se o usuário
ainda não fez a reunião, entregue o roteiro e pare. Não invente respostas que
o cliente não deu.

Se faltarem respostas essenciais (produtos, faixas de preço, prazo, raio de
atendimento, horário humano), liste o que falta como perguntas a mandar por
áudio para o cliente antes de continuar. O agente não pode chutar preço.

## Saída, nesta ordem

### 1. `voice.md` do cliente

Use `templates/voice.md` como base. Preencha com o que o cliente falou, nas
palavras dele. Marque com `[confirmar]` o que foi inferido. Salve em
`~/.claude/instagram/clientes/{slug}/voice.md`.

### 2. Base de conhecimento do agente (`kb.md`)

Use `templates/gp/kb-template.md`. Doze seções. Cada resposta do agente vem
daqui, de nenhum outro lugar. Regras:

- Preço sempre em **faixa** ("cozinhas planejadas ficam entre R$ 18 mil e
  R$ 45 mil, depende da metragem e do material"), nunca valor fechado, a
  menos que o cliente tenha tabela fixa.
- Toda pergunta frequente tem a resposta **e** a pergunta de qualificação
  que vem depois. O agente nunca responde e para.
- O que o agente **não sabe** está escrito: "Para X, o [nome do dono] fala
  com você, posso agendar?"

### 3. Prompt do agente (`agent-prompt.md`)

Use `templates/gp/agent-prompt.md`. Troque só os campos entre chaves. Não
reescreva as regras de segurança (não inventar preço, não prometer prazo,
passar para humano em reclamação, LGPD). Elas estão ali porque cada uma
custou um cliente de alguém.

### 4. Trinta conversas de teste

Escreva 30 mensagens de cliente simulado, em `testes.md`, cobrindo:
10 pedidos de orçamento normais, 5 perguntas de preço direto, 5 fora do raio
ou fora do produto, 4 reclamações, 3 mensagens confusas ou com erro de
digitação, 3 tentativas de conversar sobre outra coisa. Para cada uma, a
resposta esperada em uma linha. O usuário roda essas 30 no agente antes de
ligar. Qualquer falha em reclamação ou preço bloqueia o go-live.

### 5. Plano do primeiro mês

Rode `/ig-plan` com o `voice.md` do cliente. Objetivo único do conteúdo:
gerar mensagem no WhatsApp. Toda legenda termina com a palavra-chave que o
agente reconhece (defina-a aqui, uma só, ex: "ORÇAMENTO").

### 6. Lista de gravação para o dono

Dez vídeos crus de 20 a 40 segundos, no celular, em uma hora, que o dono
grava sem roteiro decorado. Para cada um: o que mostrar, a frase de abertura
(use `/ig-reel` para os ganchos), onde gravar. Ele manda os brutos; os
agentes cortam, legendam e montam.

### 7. Checklist de go-live

```
[ ] voice.md revisado pelo cliente (áudio de 2 min basta)
[ ] kb.md com todas as faixas de preço confirmadas pelo dono
[ ] 30 testes rodados, 0 falhas em preço e reclamação
[ ] horário de fallback humano configurado, com o número de quem atende
[ ] agenda conectada e testada com um agendamento real
[ ] planilha de métricas (templates/gp/metricas.csv) criada para o cliente
[ ] primeiro lote: 4 reels + 2 carrosséis aprovados
[ ] palavra-chave definida e no primeiro post
[ ] contrato assinado e primeira cobrança paga
[ ] reunião de entrega marcada (30 min)
```

## Tempo

Com a transcrição na mão, as saídas 1 a 6 levam cerca de 3 horas suas. Se
estiver levando mais do que 6, o problema é a reunião de onboarding, não a
skill: volte ao roteiro e colete melhor.
