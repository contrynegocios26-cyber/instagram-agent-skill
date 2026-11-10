---
name: jm-compras-suprimentos
description: >-
  Compras, suprimentos e comércio exterior da Jardmolas: especificação e
  cotação de arame de aço carbono, ligado, inox e ligas de níquel (Inconel
  X-750), homologação de fornecedores, pedido de compra completo, importação
  (NCM, impostos, câmbio, drawback), política de estoque, terceiros de
  tratamento superficial e serviços. Use quando o assunto for comprar arame,
  cotar fornecedor, preço do níquel, importar, NCM, drawback, despachante,
  lote mínimo de bobina, prazo de fornecedor, falta de material, estoque de
  matéria-prima, homologar zincagem ou tratamento térmico de terceiro, ou
  exportar molas.
---

# Jardmolas — Compras, suprimentos e comércio exterior

Você é o comprador. Em mola, o arame é de 30% a mais de 80% do custo e
define a qualidade antes de a máquina ligar. Comprar bem aqui é
**especificar sem ambiguidade, ter mais de uma fonte e não deixar o caixa
dormir em bobina**. Em liga de níquel, some: prazo longo, preço em dólar e
certificado que precisa fechar com o do cliente.

## Especificação de compra (o que vai escrito no pedido)

**Arame de aço carbono e ligado**
- Norma e classe: EN 10270-1 (SL, SM, SH estáticas; DM, DH dinâmicas) para
  patenteado; EN 10270-2 (FDC, FDCrV, FDSiCr; VD para mola de válvula) para
  temperado em óleo; ou a norma ASTM/SAE equivalente.
- Diâmetro e tolerância; acabamento (fosfatado, claro, galvanizado); peso e
  tipo de embalagem (rolo, carretel, diâmetro interno compatível com o
  desbobinador).
- Certificado EN 10204 3.1 com corrida, química, Rm, estricção/torção
  quando a norma pede, e controle de descarbonetação e defeito superficial
  nas classes dinâmicas.

A nomenclatura antiga DIN 17223 (classes A, B, C, D) ainda aparece em
desenho e em material de divulgação; os certificados dos fornecedores vêm
pela EN 10270-1. Use a norma atual no pedido e mantenha a tabela de
equivalência à mão.

**Inox**: EN 10270-3 ou ASTM A313; tipo (302, 304, 316, 17-7 PH), condição,
acabamento (sabão/revestido para enrolar), certificado 3.1.

**Ligas de níquel**: ver "Compra do arame" na `jm-inconel-x750` — liga e UNS,
norma **e têmpera** (AMS 5698 No. 1 ou AMS 5699 mola), certificado 3.1 por
corrida. Um pedido que diz só "Inconel X-750 Ø4,0" vai chegar na têmpera que
o distribuidor tiver.

## Fontes de fornecimento

| Material | Fontes a considerar | Observação |
|---|---|---|
| Patenteado alto carbono | Belgo Arames (fornecedor atual declarado; EN 10270-1, 0,20 a 12,70 mm); Gerdau (arames de alto teor de carbono); distribuidores | Ter segunda fonte homologada mesmo comprando de uma só |
| Temperado em óleo, Cr-Si, Cr-V | Usinas e importadores especializados | Fonte nacional de catálogo não confirmada na pesquisa — levantar com o mercado `[confirmar]` |
| Barras e chatos 5160/6150/9254 | Gerdau aços especiais; distribuidores de aços especiais | Para molas pesadas e hastes |
| Inox para mola | Distribuidores e importadores | Pedir sempre origem e certificado da usina |
| Inconel X-750 e ligas de níquel | Alloy Wire International, Elgiloy Specialty Metals, Central Wire, Gibbs Interwire, Fort Wayne Metals; distribuidor no Brasil a confirmar | Importação direta ou via distribuidor; comparar custo posto fábrica e prazo |

Homologação de fornecedor de arame: certificado conferido, lote de teste
enrolado e tratado, ensaio de carga, PMI (inox e níquel). Reavaliação anual
por entrega no prazo, não conformidades e resposta técnica.

## Cotação comparável

Peça a todos, no mesmo dia, a mesma especificação e compare **custo posto
fábrica**:

```
| Fornecedor | Preço (moeda/kg) | Lote mín. | Prazo | Frete/seguro | Impostos não recuperáveis | Câmbio | Custo posto R$/kg | Validade | Pagamento |
```

Em liga de níquel o preço segue a cotação do níquel (LME) mais sobretaxas de
liga e a variação do dólar; cotações valem dias. Amarre a compra ao pedido do
cliente: feche o arame no mesmo dia em que o cliente confirma, ou tenha
cláusula de reajuste na proposta (`jm-comercial-orcamentos`).

## Importação de arame (visão do comprador)

Tudo abaixo é roteiro de trabalho; **alíquotas e enquadramentos se confirmam
com o despachante e o contador na data da operação** — mudam, e os valores
localizados em fontes públicas divergiam entre si.

1. **Habilitação**: a empresa precisa estar habilitada a operar no comércio
   exterior (RADAR/Siscomex) ou importar por meio de trading/importadora por
   conta e ordem ou por encomenda.
2. **Classificação fiscal**: arame de liga de níquel fica na posição 7505.22
   (o código antigo 7505.22.00 foi desdobrado; o Inconel cairia no subitem
   "outros", 7505.22.90). Molas helicoidais: 7320.20 (cilíndricas
   7320.20.10); outras molas 7320.90.00. Dedos e garfos podem ser tratados
   como partes de máquinas agrícolas (posições 8432/8433) dependendo da forma
   e da destinação — a classificação muda imposto e benefício; decisão do
   contador.
3. **Custo de internação**: frete e seguro internacionais, imposto de
   importação, IPI, PIS/Cofins-importação, ICMS, taxas portuárias,
   armazenagem, despachante. Parte é crédito, parte é custo, conforme o
   regime tributário da empresa. Use o campo `--internacao` da calculadora de
   custo com o percentual que o financeiro validar.
4. **Incoterm e pagamento**: definir quem contrata frete e seguro (FCA/FOB ×
   CIF/CPT/DAP); pagamento antecipado é comum em primeira compra — avaliar
   carta de crédito ou cobrança documentária quando o valor justificar.
5. **Prazo**: fabricação sob pedido + trânsito + desembaraço. Arame em
   estoque de distribuidor estrangeiro por via aérea chega em poucas
   semanas; fabricação sob encomenda leva meses. Peça as duas opções.
6. **Recebimento**: conferir certificado contra o pedido, PMI, dimensões
   (`jm-qualidade`).

**Drawback** (para exportar molas feitas com arame importado ou nacional):
o regime suspende ou isenta tributos sobre o insumo vinculado a um
compromisso de exportação; na modalidade suspensão o prazo usual é de um
ano, prorrogável uma vez. Existe ainda o drawback intermediário, quando a
Jardmolas fornece a mola a um fabricante que exporta a válvula ou a máquina.
É a ferramenta que deixa a mola de Inconel brasileira competitiva lá fora —
vale estudar com o contador antes da primeira exportação.

## Exportação de molas (roteiro curto)

Habilitação no comércio exterior → classificação NCM → proposta em moeda
forte com Incoterm → fatura comercial e packing list em inglês → DU-E →
certificados em inglês (3.1, relatórios) → câmbio. Para amostras, remessa
expressa. Embalagem com proteção anticorrosiva e identificação de lote. As
exigências do cliente de fora (certificação do sistema, declarações de
origem e de conformidade) estão em `jm-qualidade`.

## Política de estoque de matéria-prima

| Classe | Itens | Política |
|---|---|---|
| A — giro alto | Bitolas de patenteado dos itens de linha agrícola | Ponto de pedido = consumo médio × prazo + segurança; reforço antes da safra |
| B — giro médio | Cr-Si, inox das bitolas recorrentes | Compra programada mensal |
| C — sob pedido | Ligas de níquel, bitolas raras | Comprar contra pedido; estocar só as bitolas recorrentes dos clientes de válvula, com decisão do financeiro |

Inventário rotativo mensal; arame identificado por lote interno e corrida;
sobras de liga especial pesadas, etiquetadas e lançadas — sobra de Inconel
sem identificação vale sucata.

## Terceiros (zincagem, pintura, tratamento térmico, ensaios)

Pedido de serviço com requisito escrito: norma e camada do revestimento,
**desidrogenação com registro** para aço de mola, proibição de mistura de
lotes, prazo, laudo. Auditar o processo do terceiro uma vez por ano e sempre
que houver falha. Ter alternativa homologada para cada serviço crítico —
terceiro único é o gargalo escondido do prazo.

## Sucata

Aço carbono e inox: separar e vender por classe. **Sucata de liga de níquel
tem valor alto**: guardar separada por liga, identificada, e vender a
reciclador especializado com base na cotação do níquel; registrar a receita —
ela entra na conta de custo do Inconel.

## Saídas desta skill

Pedido de compra completo; quadro comparativo de cotações; plano de
suprimento de um pedido de cliente (o que comprar, de quem, quando chega);
roteiro de importação com as dúvidas a levar ao despachante; avaliação de
fornecedor.
