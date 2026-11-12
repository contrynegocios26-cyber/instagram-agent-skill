# Relatório de validação: marina-atendimento

Marina fictícia (Marina Remanso), 26 cenários, três rodadas em 12/11/2026.
Cada rodada teve agentes separados para simular e para julgar; quem julgou
não leu a skill.

## Resultado

| Rodada | Conversas | Aprovadas | Fato inventado (preço, horário, vaga) | Observação |
|---|---|---|---|---|
| 1 | 26 | 24 | 0 | Critérios mais frouxos; pareceres do dono e do cliente muito negativos |
| 2 | 26 | 20 | 0 | Critérios endurecidos (G8 e G9) depois da rodada 1 |
| 3 | 9 (as 6 reprovadas e 3 de controle) | 9 | 0 | Duas aprovações no limite (02 e 23) |

As rodadas não são comparáveis em número, porque os critérios ficaram mais
duros da 1 para a 2. O que se mantém nas três: nenhum preço, horário, vaga
ou conta errada contra a ficha.

## O que cada rodada mudou

**Depois da rodada 1** (juízes, dono cético e cliente exigente):

- Chave Pix e prazo de pré-reserva na ficha: três vendas morriam em "a
  chave eu não tenho aqui".
- Plantão: todo encaminhamento vai para alguém que está trabalhando
  naquele momento. Antes, cliente na porta no sábado era mandado para o
  financeiro, que só atende na segunda.
- Número não cadastrado nunca tem descida confirmada pelo atendente, nem
  dizendo ser autorizado. Antes, o cunhado era barrado e o "marido" de
  outro número passava.
- Pendência financeira: o atendente não barra nem cobra; chama a equipe
  com urgência.
- Reclamação de cliente da casa vai ao plantão na hora.
- Áudio e foto não travam a conversa.
- Menos cerimônia com cliente da casa e confirmação direta de pedido
  completo.
- Oferta: preço fechado, piloto sem custo, número e dados da marina,
  critério de sucesso.

**Depois da rodada 2:**

- O atendente não promete pela equipe nem inventa canal ("fale com ele na
  rampa").
- Não oferece "chamar alguém" como saída para pressão: lotação,
  habilitação, opinião sobre o rio e tentativa de manipulação terminam
  nele.
- Aciona a equipe já na primeira resposta em reclamação, pendência e
  emergência.
- Oferece preparação na mensagem de confirmação.

**Depois da rodada 3** (ajustes ainda não testados):

- Aviso das 72 horas sempre que falar em sinal.
- Encaixe em consulta não vira registro próprio.
- Não diz "a equipe assume a conversa".

## O que a simulação não prova

- Que um dono de marina compra. O parecer do dono é um agente fazendo o
  papel; serve de ensaio para a visita.
- Que o atendente funciona com a ficha de uma marina real. A ficha de
  teste foi escrita para ser completa; a real terá buracos.
- Que funciona ligado ao WhatsApp, à planilha da fila e ao Pix. Nada disso
  foi montado ainda.
- Áudio e foto: a simulação assumiu que o atendente não ouve nem vê.
- Simulador e atendente são o mesmo agente na conversa, o que tende a
  deixar o cliente simulado mais fácil do que um cliente real.

## Objeções do dono que ainda estão abertas

1. Como o número de WhatsApp volta ao aplicativo comum se cancelar.
2. Quem atualiza a fila quando o cliente combina direto na rampa.
3. Quem paga pelo erro do atendente.
4. Custo por mensagem da API e do modelo.
5. Se o atendente consegue ouvir áudio, que é como muito cliente fala.

## Onde está cada coisa

- `rodada-N/conversas/NN.md`: as conversas simuladas.
- `rodada-N/julgamento/NN.md`: o veredito de cada uma, com a frase exata
  de cada falha.
- `rodada-1/parecer-dono.md` e `rodada-1/parecer-cliente.md`: os dois
  pareceres.
