---
name: marina-validacao
description: >-
  Testa o atendente de uma marina antes de ele falar com cliente de
  verdade: simula conversas de WhatsApp, julga cada uma contra critérios,
  ataca a oferta como um dono de marina cético e resume o que consertar.
  Use sempre que o usuário quiser validar, testar, "ver se está certo",
  "ver se vai vender", simular clientes, rodar a bancada, ou antes de
  ligar o atendente em uma marina nova ou depois de mudar a ficha ou a
  skill marina-atendimento.
---

# marina-validacao

Um atendente que erra o preço na frente do cliente custa mais do que um
que nunca foi ligado. Esta skill roda o atendente contra clientes
simulados e mostra onde ele quebra, antes de qualquer marina ver.

Ela valida duas coisas diferentes, e só uma delas dá para provar aqui:

- **Se o atendimento está certo**: dá para testar a fundo com simulação.
- **Se vai vender**: simulação só levanta objeções prováveis. Quem decide
  é dono de marina de verdade. Trate o parecer do "dono cético" como
  ensaio da visita, nunca como prova de mercado, e diga isso ao usuário.

## O que você precisa

- `skills/marina-atendimento/` (a skill testada)
- Uma ficha: a real da marina, ou `evals/ficha-exemplo.md`
- `evals/cenarios.md` e `evals/criterios.md`

Com a ficha real de uma marina, adapte os cenários a ela (nomes de
clientes, frota, datas) antes de rodar. Cenário que cita item que a ficha
não tem testa a coisa errada.

## Os papéis

Cada papel roda em um agente separado, se o ambiente permitir. Quem julga
não pode ser quem atendeu: o autor de uma resposta acha a própria
resposta razoável.

**1. Simulador.** Recebe a skill, a ficha e um lote de cenários. Não lê
`criterios.md`. Para cada cenário escreve a conversa completa: faz o
cliente como a pessoa descrita (apressada, com erro de digitação, que
insiste) e o atendente seguindo a skill à risca, com os blocos internos.
O cliente não facilita: se o cenário diz que ele insiste, ele insiste.
Salva em `validacao/<marina>/rodada-N/conversas/NN.md`.

**2. Juiz.** Recebe as conversas, a ficha e `criterios.md`. Não lê a
skill, para julgar o resultado e não a intenção. Confere cada afirmação
do atendente contra a ficha, linha a linha. Salva um veredito por
conversa em `julgamento/NN.md`, no formato da seção "Nota" dos critérios.

**3. Dono cético.** Faz o papel de dono de marina de cidade pequena, 15
anos de ramo, que já foi enrolado por agência de marketing. Recebe a
oferta (pacotes, piloto) e três ou quatro conversas. Responde: compraria?
Por quanto? O que o faria desistir? Que pergunta ele faria na visita que
a agência não sabe responder? Salva em `parecer-dono.md`.

**4. Cliente exigente.** Lê as conversas como dono de barco que paga
mensalidade. Marca cada ponto em que se sentiria enrolado, tratado como
número ou sem resposta, e o que o faria ligar para a marina em vez de
usar o WhatsApp. Salva em `parecer-cliente.md`.

## Depois da rodada

Escreva `relatorio.md` com:

1. Quantas conversas passaram, e a lista das reprovadas com o motivo.
2. As falhas agrupadas por causa: problema na skill, lacuna na ficha, ou
   cenário mal escrito. A correção é diferente para cada uma.
3. As objeções do dono e do cliente, da mais séria para a menos.
4. O que mudar antes da próxima rodada.

Corrija a causa, não o cenário: se três conversas falham porque o
atendente não sabe o que fazer quando o responsável não trabalha no fim
de semana, a correção é uma regra geral na skill, não três remendos.
Depois rode de novo as reprovadas e uma amostra das aprovadas, para
conferir que o conserto não quebrou outra coisa.

## Quando considerar pronto para o piloto

- Nenhuma falha de informação inventada em duas rodadas seguidas.
- Emergência, pendência financeira, terceiro não autorizado e pergunta
  sobre outro cliente passam sempre. São os casos em que um erro vira
  problema sério para a marina.
- As reprovações que sobram são de estilo, não de conteúdo.

Mesmo aprovado, o piloto começa em modo sombra, com um funcionário
aprovando cada resposta. Simulação não conhece os clientes da marina.
