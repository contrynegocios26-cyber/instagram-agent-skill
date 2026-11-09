# Financeiro, custos e preço

Vale para Financeiro, Engenheiro de Aplicação, Canais, Grandes Contas, OEM e Fechamento. Os percentuais abaixo são **estrutura**; os números da Jardmolas entram quando o dono responder (Perguntas de abertura, itens 8 e 9 de `empresa.md`).

## 1. Custo-padrão de uma mola (por peça)

```
material   = peso (kg) × preço do arame (R$/kg) × (1 + perda)
conversão  = custo da hora (máquina + operador) ÷ peças por hora
setup      = (minutos de setup ÷ 60 × custo da hora) ÷ tamanho do lote
tratamento = peso × R$/kg (alívio de tensões, jateamento) ou R$/peça se terceirizado
acabamento = pintura, óleo, zinco (R$/peça)
embalagem  = caixa, saco, etiqueta (R$/peça)
custo      = soma de tudo
```

- **Custo da hora** = (depreciação da máquina + energia + manutenção + operador com encargos + rateio de despesas indiretas) ÷ horas produtivas do mês. Se não existir, comece com uma estimativa marcada [confirmar] e refine.
- **Peso**: `scripts/calc_mola.py` calcula pelo comprimento de arame (espiras + hastes + olhais).
- **Setup pesa muito em lote pequeno.** É por isso que o preço tem faixas de quantidade.

## 2. Preço

```
preço = custo ÷ (1 − impostos − comissão − frete − margem de contribuição alvo)
```

Exemplo de uso:
```bash
python3 scripts/calc_mola.py compressao --d 6 --De 50 --nt 10 --L0 120 --Lt 90 --Rm 1600 \
  --arame-kg {{R$/kg}} --perda 5 --pecas-hora {{n}} --custo-hora {{R$/h}} --setup-min {{min}} \
  --lote {{n}} --tratamento-kg {{R$/kg}} --acabamento {{R$}} --embalagem {{R$}} \
  --impostos {{%}} --comissao {{%}} --frete {{%}} --margem {{%}}
```
O script imprime custo e preço para lotes de 50, 100, 500, 1.000 e o lote informado.

- **Impostos**: a Jardmolas é EPP. No Simples Nacional a alíquota efetiva depende do faturamento dos últimos 12 meses e do anexo; fora do Simples entram ICMS, IPI, PIS e COFINS. **Confirmar com o contador** antes de fechar a tabela.
- **NCM**: molas de aço costumam cair na posição 7320. Alguns estados incluem itens dessa posição em listas de substituição tributária de autopeças. Verificar com o contador se alguma venda (principalmente fora de SP) cai em ST [confirmar].
- **Frete**: CIF embute no preço (use o % médio da região); FOB o cliente paga.

## 3. Política de preço por canal (estrutura a definir com o dono)

| Canal | Base | Regra |
|---|---|---|
| Produtor e prestador (direto) | Tabela cheia | Faixas de quantidade; à vista com desconto pequeno ({{x}}%) |
| Revenda e cooperativa | Tabela cheia − {{x}}% | Desconto que garanta à revenda margem de {{y}}% vendendo pela tabela cheia; pedido mínimo {{R$}}; reposição em {{n}} dias |
| Usina e grupo (contrato anual) | Preço negociado por volume | Preço travado por {{n}} meses com **cláusula de reajuste do arame**; programação de entregas |
| OEM e indústria | Preço por lote e previsão | Lote econômico, previsão trimestral, reajuste do arame |

**Regra de conflito de canal:** o preço direto ao produtor nunca fica abaixo do preço que a revenda da mesma região pratica. Se o produtor está na área de uma revenda parceira, ofereça comprar pela revenda ou venda pela tabela cheia.

**Cláusula de reajuste do arame (sugestão):** se o preço do arame variar mais de {{5}}% desde a proposta, o preço da mola é reajustado na proporção do peso do material no custo. Compras registra o preço do arame por bitola e a data de cada reajuste.

**Desconto só com troca**: volume maior, entrega programada, pagamento antecipado ou contrato. Nunca desconto seco para "fechar hoje".

## 4. Crédito e cobrança

- Cliente novo: consulta de crédito, limite inicial pequeno, primeira compra antecipada ou com prazo curto.
- Prazos típicos no B2B do agro: 28/35/42 dias. Usinas grandes costumam pagar em prazos longos e só com cadastro aprovado: isso consome caixa e precisa entrar no fluxo.
- "Pagamento na safra" para produtor só com garantia e decisão do dono.
- Régua de cobrança: lembrete D−3, cobrança D+1, ligação D+5, bloqueio de novos pedidos D+15 [definir com o dono].

## 5. Caixa com sazonalidade

- **Fluxo de caixa de 13 semanas**, atualizado toda segunda.
- A entressafra pede caixa para comprar arame e produzir estoque de giro dos dedos antes de abril. Contratos de reposição programada e pedidos antecipados de revenda financiam esse estoque.
- Na safra o caixa entra, mas com prazo de usina. Na entressafra, OEM e indústria seguram o faturamento.

## 6. Indicadores do Financeiro

- Margem de contribuição por produto, por cliente e por canal (mensal).
- Ponto de equilíbrio mensal em R$.
- Prazo médio de recebimento e de pagamento; giro de estoque (arame e produto acabado).
- Inadimplência em % da carteira.
- Preço médio do arame por bitola e variação no mês.
- Custo de frete em % do faturamento.
