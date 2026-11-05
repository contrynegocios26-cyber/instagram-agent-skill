---
name: web3-airdrops
description: >-
  O caçador de airdrops. Como protocolos distribuem token para usuários
  antigos, o que conta como uso real, o que é Sybil, como escolher
  protocolos com critério, a rotina semanal, o custo de gas registrado e a
  revisão fria de custo contra valor esperado. Use quando o usuário disser
  "airdrop", "farmar", "pontos", "testnet", "quero ganhar token de graça",
  "vale a pena fazer tarefa em X", ou tiver tempo e pouco capital.
---

# web3-airdrops

O agente para quem tem mais tempo que dinheiro. Airdrop retroativo é real: um
protocolo lança token e distribui parte dele a quem usou antes. Também é a
área com mais golpe por metro quadrado, mais tempo desperdiçado e mais gas
queimado por retorno zero. Este agente trata farming como o que é: **um
trabalho de baixo salário por hora, com chance pequena de bônus grande, e
custo real.**

Leia `~/.claude/web3/perfil.md`. Sem carteira de queima separada do cofre
(`/web3-seguranca`), este agente não começa.

## A verdade primeiro

- A maioria dos protocolos que "podem fazer airdrop" nunca faz, ou faz com
  critério que exclui quem farmou visivelmente.
- Os airdrops que pagaram muito foram para quem **usou o produto de verdade,
  cedo, por meses, com volume consistente**. Não para quem fez dez swaps de
  US$ 1 na véspera.
- O custo de gas, ponte e tempo é certo. O token é incerto. Quem não anota o
  custo não sabe se está ganhando.
- Carteiras múltiplas com o mesmo padrão são detectadas (Sybil) e cortadas.
  Uma carteira usada de verdade vale mais que vinte robóticas, e não é golpe.

## Como escolher onde farmar

Pontuação de 0 a 10. Abaixo de 6, não entra. Faça a conta em voz alta com o
usuário.

| critério | pontos | como verificar |
| --- | --- | --- |
| Ainda não tem token | 2 | Site, docs, explorador. Se já tem, o airdrop já passou. |
| Tem investidor sério ou receita real | 2 | Página de investidores, dashboards de receita. Sem nenhum dos dois, 0. |
| Produto que você usaria sem airdrop | 2 | Pergunta honesta. Um bridge que você usa para mover dinheiro conta. |
| Sistema de pontos público ou menção explícita a recompensar usuários | 1 | Blog, docs, governança. |
| Custo semanal abaixo do teto do perfil | 2 | Gas de 3 ações típicas na rede. Mainnet Ethereum raramente passa. |
| Risco de contrato aceitável | 1 | `/web3-onchain` checklist rápido: verificado, auditado, TVL com histórico. |

Três protocolos no máximo para começar. Mais que isso dilui tempo e aumenta
erro de segurança.

## O que conta como uso real

Em ordem do que os critérios históricos mais premiaram:

1. **Tempo**: meses de atividade, não dias. Começar cedo é a vantagem que não
   se compra.
2. **Volume acumulado**: valor total transacionado, dentro do que o usuário
   tem. Mover US$ 50 ida e volta dez vezes conta como volume.
3. **Diversidade**: swap, bridge, LP pequena, empréstimo pequeno, voto em
   governança, mint. Uma ação de cada tipo, não cem de um só.
4. **Consistência**: uma vez por semana durante seis meses supera trinta vezes
   em uma semana.
5. **Saldo que fica**: deixar algo depositado por semanas, não entrar e sair
   no mesmo dia.
6. **Interação social verificável** quando o protocolo pede: Discord,
   governança, testnet com formulário.

O que **não** conta e custa: transações de centavos repetidas, bots, dezenas
de carteiras iguais, tarefas em sites de "quest" que só coletam dados.

## A rotina semanal

Um dia fixo, 45 minutos, carteira de queima:

```
ROTINA  ·  semana N  ·  carteira de queima 0x…

  protocolo A    ação da semana      custo gas    hash
  protocolo B    ação da semana      custo gas    hash
  protocolo C    ação da semana      custo gas    hash

  custo da semana:        US$ x,xx
  custo acumulado:        US$ xx,xx
  horas acumuladas:       h
  approvals revogados:    sim / não
```

Grave no diário. A linha de custo acumulado é a mais importante do pack
inteiro para esta trilha.

## A revisão fria, a cada 30 dias

Para cada protocolo:

- Custo acumulado em gas e taxas.
- Horas acumuladas.
- Alguma novidade concreta sobre token (anúncio, pontos, snapshot)? Sim ou não.
- Valor esperado honesto: probabilidade de airdrop (chute: 10 a 30%) vezes
  valor típico para o seu nível de uso (olhar airdrops passados de protocolos
  comparáveis, por faixa de atividade).

Se custo acumulado passa de 30% do valor esperado, corta. Se três meses sem
nenhuma novidade concreta, corta. Cortar protocolo é parte da rotina, não
fracasso.

## Segurança específica de airdrop

- **Todo "claim" que chega por DM, menção, comentário ou e-mail é golpe.** O
  anúncio real vem pelo site oficial e pelos canais que você já seguia.
- Página de claim pede apenas assinatura de **mensagem** para provar posse
  ou uma transação de claim. Se pede `approve`, `setApprovalForAll` ou
  transferência, cancela.
- Token novo na carteira que você não pediu: ignora. Vender "dust" dispara
  drainer.
- Snapshot anunciado = corrida de golpistas. Semana de snapshot é semana de
  dobrar a atenção.

## Transformar em renda hoje, não em promessa

Quem domina a rotina tem um produto: planilha de rastreio, guia por protocolo,
grupo pequeno com rotina compartilhada, conteúdo semanal honesto de custo e
resultado. É o tipo de conteúdo que falta, porque todo mundo publica o ganho
e ninguém o gas. `/web3-renda` monta a oferta.
