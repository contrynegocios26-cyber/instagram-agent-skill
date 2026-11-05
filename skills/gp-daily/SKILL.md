---
name: gp-daily
description: >-
  Growth Partner IA, o gerente: lê o painel de todos os clientes e o pipeline
  de prospecção e diz as cinco ações de hoje, em ordem de impacto. Use toda
  manhã, ou quando o usuário disser "o que eu faço hoje", "como estão os
  clientes", "reunião de segunda", "estou perdido com as contas".
---

# gp-daily

Com 1 cliente você sabe tudo de cabeça. Com 4, esquece o relatório de um.
Com 8, perde um cliente sem perceber que a resposta do agente estava
quebrada há dez dias. O gerente existe para que nada disso aconteça.

## Entrada

Dois arquivos, mantidos pelo usuário:

- `templates/gp/clientes.csv`: um cliente por linha, com mensalidade, data de
  início, último relatório enviado, última conversa com o dono, retorno das
  últimas 4 semanas, status.
- `templates/gp/pipeline.csv`: um prospect por linha, com estágio
  (contatado, respondeu, auditoria enviada, reunião marcada, proposta,
  fechado, perdido) e a data da última ação.

```bash
python3 daily.py                                 # usa os dois CSVs em templates/gp
python3 daily.py --clientes c.csv --pipeline p.csv
python3 daily.py --meta-contatos 30
```

## O que o script faz

Aplica as regras abaixo e devolve a lista de ações do dia, ordenada por
quanto dinheiro está em jogo. Você não decide o que olhar; o script decide,
você executa.

**Clientes (dinheiro recorrente em risco):**

| Regra | Ação | Prioridade |
| --- | --- | --- |
| Relatório da semana não enviado e já é terça | Enviar hoje | Alta |
| Retorno abaixo de 1x por 3 semanas | Ligar hoje para rever a oferta | Alta |
| Sem contato com o dono há 14 dias | Mandar áudio de 1 minuto | Média |
| Contrato vence em 30 dias | Preparar renovação com os números | Alta |
| Piloto completando 60 dias | Gravar depoimento esta semana | Média |
| Status "risco" marcado manualmente | Primeira ação do dia | Máxima |

**Pipeline (dinheiro novo):**

| Regra | Ação | Prioridade |
| --- | --- | --- |
| Reunião marcada para hoje ou amanhã | Preparar a conta dele | Alta |
| Proposta enviada há mais de 2 dias sem resposta | Follow-up curto | Alta |
| Respondeu e não recebeu auditoria em 24h | Gravar e mandar hoje | Alta |
| Contatado há 3, 7 ou 14 dias sem resposta | Follow-up do dia correspondente | Média |
| Contatos novos hoje abaixo da meta | Completar antes de qualquer entrega | Alta |
| Perdido há mais de 90 dias | Volta para a lista | Baixa |

## Saída

```
HOJE  terça 12/11          MRR R$ 11.500   6 clientes   pipeline 23
========================================================================
 1. [RISCO]  Planejados Reis     retorno 0,6x há 3 semanas. Ligar hoje.
 2. [NOVO]   Marcenaria Alvorada  reunião amanhã 10h. Montar a conta dele.
 3. [ENTREGA] Studio Lume         relatório da semana atrasado. Enviar.
 4. [NOVO]   Casa & Madeira       proposta há 4 dias. Follow-up curto.
 5. [PROSPEC] 0/30 contatos hoje. Duas horas de prospecção antes das 12h.
------------------------------------------------------------------------
 resto do dia: Móveis Dutra (áudio, 15 dias sem falar), 3 follow-ups de dia 3
```

Cinco ações no topo, o resto embaixo. Se o topo tem mais de cinco, o dia
está errado, não a lista: ou falta o assistente, ou sobrou cliente ruim.

## Segunda-feira

Na segunda o script também imprime o resumo da semana: MRR, churn, clientes
novos, contatos feitos, taxa de resposta, reuniões, fechamentos. Compare com
as metas da seção 11 do projeto. Uma métrica abaixo da meta vira a
prioridade da semana. Duas abaixo, pare de aceitar cliente novo até
consertar a operação.
