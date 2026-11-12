# O que as maiores fábricas de molas fazem — e o que a Jardmolas adota

Data: 12/11/2026. Levantamento por busca na web (trechos de páginas públicas; os sites não foram abertos um a um). Não foi encontrado ranking público de fabricantes por faturamento — os relatórios que trazem esses números são pagos. O que segue é o que as empresas divulgam sobre como atendem o cliente, que é o que dá para copiar.

"Copiar" aqui é adotar a prática, com conteúdo, marca e dados próprios da Jardmolas — nunca texto, imagem ou catálogo de terceiros.

## 1. Quem são as referências

| Empresa | Onde | Por que é referência | Fonte |
|---|---|---|---|
| **Lesjöfors** | Suécia, grupo global | Linha agrícola própria (dentes de mola para fenação e preparo de solo, torção e torção dupla); mais de 10.000 itens de estoque com entrega em 2–3 dias; loja online; modelo 3D de quase toda mola; configurador de molas de compressão, tração e torção; aplicativo de catálogo com busca por código, por veículo e por referência original | lesjoforsab.com (agricultura, stock springs, CAD), notícias do aplicativo |
| **Acxess Spring / The Spring Store** | EUA | Calculadora online gratuita (compressão, tração, torção) que devolve análise completa, desenho em PDF e **cotação instantânea**; localizador de mola de estoque por medidas com faixa de ±10%; "testador de força" online | acxesspring.com, thespringstore.com |
| **Kilen (grupo Lesjöfors)** | Europa | Aplicativo que lê o código de barras da etiqueta da caixa e mostra os dados da mola | garagewire.co.uk |
| **BPW, Fecon, Liebherr** (peças, não molas) | Europa/EUA | QR na peça ou na máquina que abre a lista de peças e os dados técnicos; identificação por foto, QR ou código | newsroom BPW, rermag.com, liebherr.com |
| **Molas Brusque** | Brusque-SC | Citada na imprensa do setor como líder em molas agrícolas no Brasil; declara mais de 40 anos e capacidade acima de 3 mil toneladas de aço por ano; molas e arames conformados para agrícola, automotivo e linha branca | comprerural.com (matéria promocional; números declarados pela empresa) |
| **thyssenkrupp Springs & Stabilizers; Rassini-NHK (Fabrini)** | Brasil | Maiores em molas automotivas (helicoidais, feixes); escala, certificação automotiva, exportação | imprensa setorial |
| **Kramp e catálogos de peças agrícolas** | Europa | Cada dente/dedo listado com comprimento total, bitola do arame, diâmetro interno da espira, marca a que serve e referência original | páginas de revenda |

Concorrentes brasileiros em molas agrícolas e de liga especial (Molas Piracicaba, Incomolas, Molas Eliane, RC Molas, Vibramol) estão no levantamento anterior; nenhum deles oferece, nas páginas encontradas, calculadora, busca por medidas ou catálogo por máquina.

## 2. As dez práticas que valem copiar

| # | Prática | Quem faz | Situação na Jardmolas |
|---|---|---|---|
| 1 | Catálogo por máquina, marca e modelo | Lesjöfors, Kramp | **Feito** — base e aplicativo; falta cadastrar itens e medidas |
| 2 | Busca por medidas com tolerância | The Spring Store, Lesjöfors | **Feito** no aplicativo |
| 3 | Busca por código original (referência cruzada) | Lesjöfors, Kramp | **Feito** — depende de cadastrar as referências |
| 4 | Calculadora de molas aberta ao cliente | Acxess, Lesjöfors | **Feito** — compressão, tração e torção, com os mesmos cálculos da engenharia |
| 5 | Pedido de cotação já preenchido a partir do cálculo | Acxess (cotação instantânea) | **Feito em parte** — o pedido sai preenchido para o WhatsApp; preço automático é a etapa seguinte |
| 6 | Guia "como medir sua mola" | Lee Spring, Acxess, Lesjöfors | **Feito** |
| 7 | Ficha técnica por item (medidas, material, embalagem, foto padrão) | Kramp, Lesjöfors | Estrutura pronta; falta o cadastro |
| 8 | QR na etiqueta que abre o item | Kilen, BPW, Fecon | **Preparado** — cada item tem endereço próprio (`#item-CÓDIGO`); falta imprimir o QR na etiqueta |
| 9 | Itens de linha em estoque com prazo declarado | Lesjöfors (2–3 dias) | Decisão de estoque pré-safra (PCP e financeiro) |
| 10 | Modelo 3D / desenho para o engenheiro do cliente | Lesjöfors, Acxess | Não feito — só vale para clientes de projeto (válvulas, montadoras) |

## 3. O que a Jardmolas passa a ter que os grandes não têm

**Consultor de Inconel X-750 por temperatura.** O cliente informa a temperatura da mola e o aplicativo mostra, para as três condições da liga, a tensão de projeto naquela temperatura e qual condição serve — com os dados do boletim do fabricante da liga. Nenhuma das referências encontradas oferece isso; é o diferencial para o engenheiro de válvulas.

**Verificação a quente na calculadora.** Além de constante e cargas, a calculadora avisa quando a mola "passa a frio" e relaxa em serviço.

## 4. O aplicativo

Arquivo único (`catalogo/app.html`), funciona no celular, sem instalação e sem servidor: pode ir para o site, para o WhatsApp do vendedor ou para o tablet do balcão da revenda. Cinco áreas: achar a peça · calcular mola · Inconel X-750 · pedir cotação · como medir.

Gerado pela skill `jm-catalogo`:

```
python skills/jm-catalogo/scripts/catalogo.py app catalogo --saida catalogo/app.html --whatsapp 55DDDNUMERO
```

A calculadora do aplicativo foi comparada com a calculadora de engenharia em 14 molas (98 valores): resultados idênticos.

Limites, para não prometer o que não entrega: não dá preço, não registra pedido em sistema, não tem login. O catálogo dentro dele tem hoje só as 19 famílias do site, sem medidas por item.

## 5. Próximos passos, em ordem de retorno

1. **Cadastrar os itens de maior giro** (dedos de palha e garfos de fenação) com medidas, foto e máquina — é o que faz as buscas 1 a 3 funcionarem de verdade.
2. **Publicar o aplicativo no site** e pôr o link na assinatura do WhatsApp e nas propostas.
3. **QR na etiqueta da caixa** apontando para o item no aplicativo.
4. **Preço automático para itens de linha** (tabela por quantidade) — é a "cotação instantânea" dos americanos, começando pelo que já tem preço de tabela.
5. **Estoque declarado** dos itens A antes da safra, com prazo escrito no catálogo.
6. **Desenho em PDF da mola calculada**, para clientes de válvula e montadora.

## 6. O que não foi possível confirmar

Faturamento e ranking das fábricas (relatórios pagos); linha de produtos e certificações da Molas Brusque (site não aberto); quem é o maior fabricante mundial de dentes de mola agrícolas; as funções exatas dos configuradores de Gutekunst e Lee Spring (não apareceram na busca).
