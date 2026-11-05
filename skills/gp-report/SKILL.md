---
name: gp-report
description: >-
  Growth Partner IA, etapa 3: o relatório semanal que mantém o cliente. Lê a
  planilha de métricas do cliente, calcula a conta do dinheiro (quanto ele
  faturou que veio do sistema versus quanto paga) e escreve o relatório em
  linguagem de dono de negócio, com um próximo passo. Use toda segunda-feira,
  ou quando o usuário disser "relatório", "fechar a semana", "o cliente
  perguntou se está valendo a pena".
---

# gp-report

O cliente não cancela quando o resultado cai. Cancela quando **para de ver**
o resultado. Este relatório existe para que, toda segunda, ele veja a conta.

## Entrada

O CSV de métricas do cliente (`templates/gp/metricas.csv`, uma linha por
dia) e a mensalidade que ele paga. Opcional: o alcance dos posts da semana
(o `/ig-audit` extrai).

```bash
python3 report.py metricas-cliente.csv --mensalidade 2500
python3 report.py metricas-cliente.csv --mensalidade 2500 --semana 2026-11-10
python3 report.py metricas-cliente.csv --mensalidade 2500 --json
```

O script soma a semana, compara com a anterior, calcula o retorno sobre a
mensalidade e aponta o gargalo (onde a conversão caiu). Ele não escreve o
relatório; ele entrega os números certos para você escrever.

## O relatório

Cinco linhas, nesta ordem. Nunca mais do que oito.

1. **A conta.** "Esta semana o sistema trouxe R$ 18.400 em vendas fechadas e
   mais R$ 61.000 em orçamentos abertos. Você paga R$ 2.500 por mês." Se a
   semana foi ruim, a conta aparece do mesmo jeito. Esconder uma semana ruim
   custa o cliente na semana seguinte.
2. **O funil.** Conversas, agendamentos, orçamentos, vendas. Com a variação
   contra a semana anterior em porcentagem, só onde mudou mais de 15%.
3. **O que funcionou.** Um post, um horário, uma resposta do agente. Com
   número. "O Reel do antes e depois da sala fez 3,2 vezes a média."
4. **O gargalo e o que vamos fazer.** Uma coisa só. Onde a conversão caiu e a
   ação da semana que vem.
5. **O que precisamos de você.** Se precisar. Gravar dois vídeos, confirmar
   um preço, responder um lead que o agente passou. Se não precisar, não
   escreva esta linha.

Tom: o do `voice.md` do **usuário**, falando com um dono de negócio ocupado.
Sem "performance", "engajamento", "KPIs". Sem gráfico. Passe por
`/ig-human`.

Exemplo do tamanho certo:

> Semana 10 a 16/11. 47 conversas no WhatsApp, 34 fora do horário comercial.
> Resposta média em 40 segundos. 11 visitas agendadas, 3 orçamentos
> enviados, 1 fechado: cozinha, R$ 18.400. Outros R$ 61 mil em orçamento
> aberto. O Reel do antes e depois da sala alcançou 3,2 vezes a média da
> conta; semana que vem repetimos o formato com o quarto do casal. O agente
> perdeu 2 leads que perguntaram prazo e não receberam resposta clara; já
> ajustei a base. Preciso de você: 30 segundos gravando o quarto pronto da
> Dona Marta antes da entrega de quinta.

## Alertas que o script levanta

- Tempo médio de resposta acima de 60 segundos: problema técnico, resolve
  hoje, não espera a segunda.
- Conversas caíram mais de 30% contra a semana anterior: conteúdo ou
  anúncio parou. Verificar antes de mandar o relatório.
- Zero vendas atribuídas por 3 semanas seguidas com agendamentos normais:
  o problema é o fechamento do cliente, não o sistema. Hora de uma ligação,
  não de um relatório.
- Retorno abaixo de 1x por 4 semanas: a conta não fecha para ele. Ou se
  muda a oferta, ou se devolve o cliente antes que ele cancele com raiva.

Registre o envio do relatório e a resposta do cliente em
`templates/gp/clientes.csv`. O `/gp-daily` usa isso.
