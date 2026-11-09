---
name: jm-caderno-usina
description: >-
  Opera o serviço Caderno de Molas da Usina da Jardmolas: prepara a visita
  técnica, lê o backup do app de levantamento, gera o resumo, a lista de troca
  da entressafra e a proposta de Estoque Garantido, e escreve o e-mail de
  entrega e o follow-up. Use quando alguém falar em Caderno de Molas,
  levantamento em usina, visita técnica, backup do app (arquivo
  caderno-*.json), entressafra, Estoque Garantido, ou pedir "monta a proposta
  da usina X".
---

# jm-caderno-usina

O Caderno de Molas é a oferta principal da Jardmolas para usinas: visita
gratuita na entressafra, cada mola crítica recebe um código JM, a usina passa a
pedir pelo código e a Jardmolas vira o fornecedor padrão. Esta skill cuida do
antes, do depois e da proposta. O levantamento em si é feito no app
`01-caderno-de-molas/caderno-de-molas.html`, no celular, sem internet.

## Ferramenta

```bash
python3 caderno.py caderno-sma-2026-12-02.json                      # resumo + troca + estoque
python3 caderno.py backup.json --precos precos.csv --saida proposta.md
python3 caderno.py backup.json --usina SMA                         # backup com várias usinas
```

`exemplo-backup.json` e `precos-exemplo.csv` nesta pasta servem para testar.
Os preços do exemplo são fictícios.

## Antes da visita

1. Leia `../../01-caderno-de-molas/roteiro-visita-tecnica.md` e monte a lista de
   documentos que a usina pede para terceiros (integração de segurança).
2. Confirme com o contato: data, horário, quem acompanha, áreas liberadas,
   se a usina já está parada (medir só com equipamento parado e bloqueado).
3. Defina a sigla da usina (3 ou 4 letras, sem repetir outra já usada) e
   crie o levantamento no app em **Nova usina**.
4. Se a usina já é cliente, puxe o histórico de pedidos dela e leve impresso:
   as molas que ela já compra entram primeiro no caderno.

## Depois da visita (no mesmo dia)

1. No app: **Dados e backup**, depois **Baixar backup desta usina**. Mande o
   arquivo para o escritório.
2. Rode `caderno.py` com a tabela de preços da Jardmolas.
3. Revise com a engenharia as fichas com alerta (índice fora da faixa, medidas
   que não fecham). Se precisar, peça amostra.
4. Gere o PDF do caderno: no computador, abra o app, importe o backup, aba
   **Caderno**, **Imprimir ou salvar PDF**.
5. Escreva o e-mail de entrega (modelo abaixo) e marque a reunião em até
   7 dias.

## Modelo de e-mail de entrega

```
Assunto: Caderno de Molas [Usina] · [N] molas com código JM

[Nome], segue o Caderno de Molas da [unidade], com as [N] molas que levantamos no dia [data].

O que tem dentro:
- ficha de cada mola com medidas, material e o código JM;
- [X] molas que estão com desgaste ou quebradas e valem trocar nesta entressafra;
- o estoque mínimo que sugerimos para as [A] molas críticas.

A partir de agora, para repor, é só mandar o código e a quantidade no WhatsApp (16) 99176-0936.

Posso passar aí [dia] para repassar a lista de troca com você? Levo o orçamento dela pronto.
[Assinatura]
```

## Regras

- O caderno é da usina. Entregue o PDF sem condicionar a compra.
- Proposta de Estoque Garantido só para molas A (e B a pedido da usina).
  Termos comerciais em `../../01-caderno-de-molas/estoque-garantido.md`.
- Nunca medir equipamento em operação. Se a área não estiver bloqueada, a
  mola fica para outra visita.
- Medidas são de campo. Escreva isso no caderno (o app já escreve no rodapé).
- Sem travessão (—) e sem clichê nos textos para a usina.
