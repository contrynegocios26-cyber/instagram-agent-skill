---
name: web3-onchain
description: >-
  O analista on-chain. Due diligence de token e protocolo com checklist e
  nota: oferta, desbloqueios, concentração de holders, liquidez, contrato,
  equipe, receita real, uso real. Use quando o usuário perguntar "esse token
  é bom?", "é rug?", "o que é tokenomics", "como ler um explorador",
  "analisa esse projeto", "posso confiar nesse protocolo", ou antes de
  qualquer agente colocar dinheiro em algo novo.
---

# web3-onchain

O agente que lê antes de qualquer um gastar. Em Web3 quase tudo é público:
quem detém o token, quando ele desbloqueia, se a liquidez está travada, se o
dono do contrato pode mintar, pausar ou mudar taxa. Quem não lê está
apostando contra quem leu.

Uma ferramenta mora nesta pasta e ela roda:

```bash
python3 score.py projeto.json          # nota 0-100 e bandeiras vermelhas
python3 score.py --modelo > projeto.json   # gera o formulário vazio
```

## O que o analista faz e não faz

Faz: coleta os fatos públicos, aplica o checklist, dá uma nota, lista as
bandeiras vermelhas, diz o que ainda não se sabe. Não faz: previsão de preço,
"vai subir", "entra agora". Nota alta significa "os riscos conhecidos estão
mapeados", nunca "é bom investimento". Preço é `/web3-risco` com tamanho, e
mesmo assim só tamanho.

## O checklist, em quatro blocos

O usuário preenche com o agente, campo por campo, usando explorador de blocos,
site do projeto, docs, dashboards públicos de TVL e receita, e ferramenta de
verificação de contrato. Cada campo recebe o valor e a **fonte**. Campo sem
fonte é "não sei", e "não sei" pontua zero.

### 1. Oferta e distribuição

- Oferta total, oferta circulante, e a relação. Circulante muito menor que
  total significa pressão vendedora futura.
- **Cronograma de desbloqueio** (vesting): quanto desbloqueia nos próximos 3
  meses, para quem. Desbloqueio grande de investidor à vista é bandeira.
- Alocação: equipe, investidores, comunidade, tesouro. Equipe + investidores
  acima de 50% é bandeira.
- **Top 10 holders**: percentual, excluindo contratos conhecidos (pool,
  staking, ponte). Acima de 50% em carteiras não identificadas é bandeira
  vermelha.
- O dono do contrato pode mintar mais? Pausar? Mudar taxa? Colocar endereço
  em lista negra? Cada "sim" sem timelock ou multisig é bandeira.

### 2. Liquidez e mercado

- Onde se negocia e quanto de liquidez tem em cada lugar.
- Liquidez da pool principal **travada ou queimada**? Por quanto tempo? Quem
  detém os LP tokens?
- Volume diário contra liquidez. Volume muito acima da liquidez com poucos
  holders é lavagem.
- Slippage para vender 1% da sua posição planejada. Se não dá para sair, não
  dá para entrar.
- Taxa na transferência (tax token)? Lista de permissões para vender
  (honeypot)? Ferramenta de verificação de contrato responde.

### 3. Contrato e segurança

- Contrato verificado no explorador? Não verificado = não entra, ponto.
- Auditoria pública, por quem, de que versão, e as questões abertas.
- Proxy atualizável? Quem pode atualizar? Com que atraso?
- Idade do contrato e histórico de incidentes.
- Para protocolos: oráculo usado, pontes das quais depende, dependências que
  já quebraram.

### 4. Uso real e receita

- O que o protocolo faz, em uma frase para leigo. Se não dá para explicar,
  bandeira.
- **Receita real** (taxas pagas por usuários), não emissão. Fonte: dashboard
  público. Receita zero com TVL alto significa que o TVL veio por incentivo e
  vai embora com ele.
- Usuários ativos, tendência em 90 dias.
- Equipe: pública ou anônima. Anônima não é veto, mas exige liquidez travada
  e contrato imutável para compensar.
- Como o token captura valor: taxa, queima, governança sobre receita, ou só
  "utilidade" vaga. Só "utilidade" vaga é bandeira.

## A nota

`score.py` pontua cada bloco, aplica as bandeiras vermelhas como veto (uma
bandeira vermelha de contrato ou liquidez derruba qualquer nota para
"não entra") e imprime:

```
ANÁLISE  ·  ProjetoX  ·  2026-11-05

  oferta e distribuição   14 / 25
  liquidez e mercado      22 / 25
  contrato e segurança    20 / 25
  uso real e receita       9 / 25
  nota                    65 / 100   ·   faixa: cautela

BANDEIRAS VERMELHAS (veto)
  nenhuma

BANDEIRAS AMARELAS
  desbloqueio de 18% da oferta em 60 dias, investidores
  receita 90d em queda de 40%

NÃO SEI (pontuou zero)
  quem detém os LP tokens
```

Faixas: 80+ mapeado, 60 a 79 cautela, 40 a 59 só com carteira de queima e
valor a zero, abaixo de 40 não entra. Bandeira vermelha ignora a faixa.

## Reler na saída, não só na entrada

Toda posição aberta é reanalisada a cada 30 dias ou em qualquer anúncio
grande. O que mudou no desbloqueio, na receita, no top 10. A maioria das
perdas evitáveis vem de quem analisou uma vez e nunca mais olhou.
