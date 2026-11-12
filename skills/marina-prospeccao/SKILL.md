---
name: marina-prospeccao
description: >-
  Prospecta marinas para uma agência de IA: analisa a presença digital e o
  atendimento de uma marina, dá nota de 0 a 100, estima o dinheiro que ela
  perde e entrega diagnóstico, proposta com pacote mensal e mensagem de
  abordagem. Use sempre que o usuário citar uma marina, garagem náutica,
  guardaria de barcos ou locadora de lancha e jet e quiser prospectar,
  abordar, vender, "fazer um diagnóstico", "montar proposta", "o que falar
  com o dono" ou preparar uma visita, mesmo que não diga "prospecção".
---

# marina-prospeccao

O dono de marina não compra "inteligência artificial". Ele compra parar de
perder reserva no sábado, quando o WhatsApp tem 80 mensagens e a equipe está
na rampa descendo barco. O trabalho desta skill é achar essa perda na marina
específica, com evidência, e transformar em uma proposta que ele entende em
dois minutos.

## Antes de começar

Leia `agencia.md` na pasta de trabalho, se existir. Ele traz o nome da
agência, quem assina, os preços e o tom. Se não existir, copie
`assets/agencia-modelo.md`, preencha o que o usuário já contou e pergunte só
o que faltar. Sem esse arquivo, use os pacotes de `references/pacotes.md`.

## 1. Juntar o que é público

Do usuário você precisa de pouco: nome da marina e cidade. Todo o resto você
busca, se tiver ferramenta de busca ou de leitura de página:

- Instagram: seguidores, frequência de posts, data do último post, se tem
  link e WhatsApp na bio, se os destaques mostram preço e serviços.
- Perfil do Google: nota, número de avaliações, se o dono responde, horário,
  fotos, telefone.
- Site: existe? Tem preço, frota, botão de reserva?
- Anúncios de embarcações: OLX, Marketplace, site próprio.
- O que ela vende: vaga seca ou molhada, descida e subida, aluguel de lancha
  e jet, passeio, venda, manutenção, combustível, restaurante.

Se não tiver como buscar, peça ao usuário prints do Instagram e do Google.
Dois prints bastam para começar.

Só escreva o que você viu. Em cidade pequena o dono conhece cada número do
próprio negócio, e um dado inventado derruba a proposta inteira. O que não
deu para verificar entra como "não verificado", nunca como estimativa
disfarçada de fato.

## 2. Cliente oculto

Esta é a evidência que fecha a venda, e só o usuário consegue produzir. Peça
que ele mande, de um número pessoal, uma mensagem de cliente comum:

> Oi, boa tarde! Queria alugar um jet no sábado, pra 2 pessoas. Tem
> disponível? Qual o valor?

Um envio em horário comercial e outro no sábado ou depois das 19h. Ele anota
quanto tempo levou a resposta, se respondeu preço e disponibilidade, e se
tentou fechar a reserva ou só informou.

Se o usuário ainda não fez o teste, entregue o diagnóstico mesmo assim, com
esse bloco marcado como pendente, e explique que vale a pena fazer antes da
visita.

## 3. Dar a nota

Use `references/rubrica.md`. São cinco blocos que somam 100. Para cada bloco,
escreva a nota, a evidência e o que ela custa para a marina em linguagem de
dono: reserva perdida, cliente que foi para o vizinho, vendedor que não
retornou o lead.

## 4. Estimar a perda

Faça a conta só com números que a marina confirmou ou que o usuário
informou, e mostre a conta aberta:

```
mensagens sem resposta por fim de semana
  x taxa de quem fecharia
  x valor médio da diária
  x fins de semana de temporada
```

Sem dados, não chute um total. Deixe a fórmula montada com os campos em
branco: preencher junto com o dono na visita convence mais do que um número
pronto, porque o número passa a ser dele.

## 5. Escolher o pacote

Recomende um pacote só, o que resolve o bloco de pior nota. Oferecer três
opções a quem nunca comprou isso trava a decisão. Os outros entram em uma
linha, como próximo passo. Regras de escolha em `references/pacotes.md`.

## O que entregar

Sempre estes quatro arquivos, em `prospeccao/<nome-da-marina>/`:

**diagnostico.md**, uma página:

```
# Diagnóstico: <Marina>
Nota geral: NN/100
## O que está bom
## Onde está perdendo dinheiro   (3 pontos, cada um com evidência)
## A conta                        (fórmula aberta)
## Não verificado
```

**proposta.md**, uma página: o problema nas palavras do dono, o que será
feito, o que ele precisa fornecer, prazo de implantação, valor de
implantação e mensalidade, e a oferta de piloto de 30 dias. Sem jargão:
"atendente que responde no WhatsApp na hora", não "agente de IA com LLM".

**abordagem.md**: a primeira mensagem de WhatsApp, com no máximo quatro
linhas, que cita um fato concreto da marina e pede 15 minutos. Mais duas
variações e um follow-up para três dias depois. Nada de elogio genérico nem
de "tudo bem?" solto.

**visita.md**: roteiro da conversa presencial. Cinco perguntas para
descobrir volume e dor (quantas mensagens no sábado, quem responde, quantas
descidas por dia, como controla a fila, quantos leads de venda por mês), as
três objeções prováveis com resposta, e o pedido final.

Depois dos arquivos, diga ao usuário em três linhas: a nota, o principal
ponto de perda e o que falta verificar.

## Tom

Português do Brasil, direto, de quem conhece a rotina de rampa e
temporada. O diagnóstico aponta problema sem humilhar: o dono montou a
marina, e a proposta é tirar trabalho das costas dele, não dizer que ele
faz errado.

## Limites

- Não prometa resultado em número ("dobrar as reservas"). Prometa o que é
  controlável: tempo de resposta, atendimento fora do horário, follow-up.
- Aluguel de jet e lancha tem exigência de habilitação da Marinha. A
  proposta diz que o atendente pergunta sobre a habilitação e encaminha
  para a equipe; quem define a regra é a marina.
- Nada é enviado ao dono sem o usuário ler e aprovar.
