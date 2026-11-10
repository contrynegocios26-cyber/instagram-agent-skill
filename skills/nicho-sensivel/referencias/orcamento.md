# Quanto gastar

Verba não é opinião, é conta. Rode `orcamento.py` com os números do cliente.

```
python3 orcamento.py --preco 197 --margem 0.50
python3 orcamento.py --preco 297 --margem 0.60 --aprovacao 0.80 --criativos 6
python3 orcamento.py --preco 0 --lead --valor-lead 40          # geração de lead
```

## A lógica

- **Margem de contribuição** = o que sobra do preço depois de produto, frete,
  imposto, taxa de gateway, comissão e reembolso médio, antes do anúncio.
- **CPA de equilíbrio** = preço x margem x taxa de aprovação do pagamento.
  Acima dele, cada venda dá prejuízo.
- **ROAS de equilíbrio** = preço / CPA de equilíbrio.
- **CPA alvo** = 70% do equilíbrio. Os 30% são o lucro e a folga para a
  semana ruim.
- **Corte por criativo:** gastou 1,5x o CPA alvo sem venda, pausa. Com
  sinal intermediário forte (clique barato, checkout iniciado), vai até 2x.
- **Verba de teste** = criativos x 1,5 x CPA alvo, mais 1 CPA alvo por
  criativo de reserva para os que derem sinal. É dinheiro para comprar
  informação, e o cliente precisa saber que pode não voltar.
- **Piso de escala:** a Meta estabiliza um conjunto por volta de 50
  conversões por semana. Verba semanal por conjunto = 50 x CPA alvo. Abaixo
  disso, otimize para um evento mais alto no funil ou consolide conjuntos.

## Fases

| fase | duração | objetivo | regra de saída |
| --- | --- | --- | --- |
| Teste | 7 a 10 dias | achar 1 ou 2 criativos abaixo do CPA de equilíbrio | nenhum achou: muda o ângulo ou a oferta, não a verba |
| Validação | 2 semanas | segurar o CPA alvo com o piso de escala | CPA estável por 7 dias seguidos |
| Escala | contínua | subir 20% a 30% de verba a cada 3 ou 4 dias | CPA passou do equilíbrio por 3 dias: volta um degrau |

## O que encarece nicho sensível

- Público 18+ e sem remarketing personalizado em saúde no Google: o topo de
  funil carrega mais peso.
- Criativo sem antes e depois e sem promessa de prazo converte menos no
  clique frio. Compense com página melhor e oferta mais clara, não com
  promessa.
- Reembolso e chargeback: entre na margem com o número real do cliente. Em
  oferta nova, use 10% até ter dado.
- Pagamento por boleto e Pix pendente: use a taxa de aprovação real.

## Faixas honestas para conversar com o cliente

Não existe verba mínima universal, e o número sai do script. Para dar ordem
de grandeza: um produto de R$ 197 com 50% de margem pede perto de R$ 900 só
para julgar cinco criativos e perto de R$ 7.700 de mídia no primeiro mês,
contando duas semanas de validação. Fora produção de criativo e gestão. Se o
cliente não tem a verba do primeiro mês, diga antes de começar: o teste até
acha o criativo, mas não haverá dinheiro para provar que ele escala. Nesse
caso, concentre em uma plataforma e otimize para um evento mais alto no
funil.

Benchmarks de CPM e CPA de terceiros variam demais por conta, época e
criativo para servir de promessa. Prometa processo e critério de corte,
nunca resultado.
