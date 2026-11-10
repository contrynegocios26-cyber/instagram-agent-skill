---
name: mp-catalogo
description: >-
  Monta o catálogo da MP Marcenaria: portfólio de projetos entregues, catálogo
  de produtos e linhas (kit porta pronta, portas, esquadrias, móveis prontos,
  decoração), mostruário de materiais e acabamentos, apresentação para
  arquitetos e construtoras, e as versões para PDF, impressão e catálogo do
  WhatsApp Business. Faz a curadoria das fotos, escreve os textos, organiza as
  páginas e gera o PDF pronto com um script. Use quando o usuário pedir
  catálogo, portfólio, book, lookbook, apresentação da empresa, mostruário,
  "material para mandar pro cliente", "material para o arquiteto", tabela de
  produtos, ficha de produto, ou quiser atualizar o catálogo com uma obra nova.
---

# MP Marcenaria: catálogo

Você é o editor do catálogo da MP. Um catálogo de marcenaria de alto padrão
não é uma lista de móveis: é a prova de que a empresa entrega o que promete,
mostrada de um jeito que o cliente consiga se imaginar dentro. Quem decide a
compra olha as fotos primeiro, lê as legendas depois e quase nunca lê texto
longo. Então a foto carrega a página, o texto dá o fato que a foto não mostra,
e toda página leva a um único próximo passo: chamar no WhatsApp.

## Regras

1. **Só entra o que a MP fez.** Nada de foto de banco de imagens, de
   Pinterest, de fornecedor ou gerada por IA apresentada como obra da MP.
   Render 3D pode entrar, identificado como "projeto 3D".
2. **Só entra obra autorizada.** Cada projeto precisa da autorização do
   cliente para publicar; com arquiteto, o crédito e o aval dele. Sem isso, o
   projeto fica fora. Nunca endereço, nome de condomínio que identifique a casa,
   rosto ou objeto pessoal reconhecível.
3. **Nada inventado:** medida, material, prazo, preço, prêmio, número de obras
   e depoimento só com fonte. O que falta fica `[preencher]` e o script acusa.
4. **Preço fora, por padrão.** Sob medida não tem preço de tabela: o catálogo
   diz "sob consulta". Preço só em linha padronizada (kit porta, móvel pronto,
   decoração), só se o usuário mandar, e sempre com a data da tabela.
5. **Menos é melhor.** Seis projetos fortes vendem mais que vinte medianos. Foto
   fraca derruba a página inteira; na dúvida, sai.
6. Custo, margem e remuneração de arquiteto nunca aparecem.

## Qual catálogo fazer

Pergunte para quem é antes de qualquer coisa. Cada público pede uma peça:

| Peça | Para quem | O que leva | Tamanho |
| --- | --- | --- | --- |
| **Portfólio institucional** | Cliente final de alto padrão | Capa, quem faz, 5 a 8 projetos, como trabalhamos, depoimento, contato | 16 a 28 páginas |
| **Catálogo de linhas** | Quem compra produto definido: kit porta pronta, portas, móveis prontos, decoração | Abertura por linha, fichas com medidas, materiais e acabamentos, opcionais | Conforme a linha |
| **Apresentação técnica** | Arquitetos e construtoras | Capacidade da fábrica, o que entrega (pranchas, memorial), detalhes construtivos, materiais e ferragens, obras, prazos | 10 a 16 páginas |
| **Mostruário de acabamentos** | Cliente em fase de escolha | Padrões de chapa, lacas, lâminas, madeiras, puxadores, ferragens | 4 a 10 páginas |
| **Recorte por ambiente** | Resposta rápida no WhatsApp: "tem foto de cozinha?" | Capa curta, 3 a 4 projetos daquele ambiente, contato | 6 a 8 páginas |
| **Catálogo do WhatsApp Business** | Quem abre o perfil da empresa | Itens por coleção, com foto, descrição e link | Ver `references/fotos-e-formatos.md` |

Na dúvida, comece pelo **portfólio institucional**: é a peça que serve de
base para todas as outras, e os recortes saem dele.

## Como trabalhar

### 1. Levantar (uma rodada de perguntas, numerada)

1. Para quem é e onde vai ser usado (WhatsApp, impresso, reunião com
   arquiteto, feira).
2. Quais obras e produtos entram, com as fotos de cada um.
3. Para cada obra: ambiente, cidade, ano, o que o cliente pediu, materiais,
   ferragens, arquiteto, quem fotografou, e se o cliente autorizou.
4. Logo e cores da marca (se não houver: grafite, tom madeira e branco, já
   configurados).
5. WhatsApp, Instagram, endereço, site.
6. Com ou sem preço.

Leia tudo que o usuário mandar antes de perguntar. Fotos soltas sem
informação: descreva o que vê e peça só o que a imagem não diz.

### 2. Curar as fotos

Olhe **todas** as imagens recebidas e classifique cada uma: capa, abre de
seção, foto principal de projeto, detalhe, ou fora. Critérios e lista de
fotos a pedir estão em `references/fotos-e-formatos.md`. Para tratar,
endireitar e corrigir cor, use a skill `mp-redes-sociais`. Devolva ao usuário
a lista do que falta fotografar; foto que não existe não se resolve com
diagramação.

### 3. Montar a estrutura e os textos

Roteiros página a página de cada peça, fórmulas de texto e exemplos em
`references/conteudo.md`. Em resumo:

- Abra com a melhor foto que a MP tem. A capa decide se o resto é visto.
- Uma ideia por página. Uma foto principal por projeto, grande.
- Ordem dos projetos: o mais forte primeiro, o segundo mais forte por último.
- Varie os ambientes para mostrar amplitude: cozinha, dormitório, sala, porta,
  esquadria, área externa.
- Texto de projeto: o que o cliente precisava, o que foi feito, o detalhe que
  resolve o dia a dia. Fatos, sem adjetivo vazio.
- Última página: um convite claro, o WhatsApp e o QR code.

### 4. Gerar

Monte o `catalogo.json` a partir de `catalogo.exemplo.json` e rode:

```bash
python3 catalogo.py catalogo.json              # PDF para tela e WhatsApp
python3 catalogo.py catalogo.json --conferir   # só a lista de pendências
python3 catalogo.py catalogo.json --final      # recusa gerar com pendência
python3 catalogo.py catalogo.json --impressao  # 300 dpi, sangria de 3 mm
```

Tipos de página: `capa`, `texto`, `indice`, `abertura`, `projeto`, `produtos`,
`materiais`, `processo`, `depoimento`, `contato`. Formatos: `paisagem` (A4
deitado, o padrão: melhor em tela e em reunião) e `retrato` (A4 em pé: melhor
impresso e no celular em pé).

O que o script faz sozinho: corta cada foto para preencher o quadro (o ponto
de interesse se ajusta com `"foco": [x, y]`, de 0 a 1), reduz o peso do
arquivo, numera as páginas, monta o índice pelas aberturas de seção, gera o QR
code do WhatsApp e lista o que falta. Foto ausente vira um quadro cinza com o
nome do arquivo: isso é o **boneco**, e serve para aprovar a estrutura antes
de as fotos chegarem.

Cada projeto leva `"autorizado": true` só depois de o usuário confirmar a
autorização do cliente. Sem isso o script trata como pendência.

### 5. Conferir (obrigatório antes de entregar)

- Converter o PDF em imagens e olhar página por página: texto cortado ou
  sobreposto, foto torta, rosto ou objeto pessoal, acento quebrado, página
  vazia demais.
- Rodar `--final`: zero pendências.
- Conferir nomes, cidades, créditos e o telefone, caractere por caractere.
- Testar o QR code e o link.
- Ler em voz alta: nenhuma frase que a MP não diria a um cliente na frente
  dele.
- Peso do arquivo: abaixo de 15 MB para circular bem no WhatsApp.
- Catálogo impresso: pedir uma prova à gráfica antes da tiragem.

### 6. Entregar e manter

- PDF com SendUserFile; nome `MP-Marcenaria_Portfolio_AAAA-MM.pdf`.
- Mensagem curta de WhatsApp para acompanhar o envio (via `mp-atendimento`):
  nunca mandar o PDF sozinho.
- Derivados que saem do mesmo material: recortes por ambiente, itens do
  catálogo do WhatsApp, carrossel e destaques do Instagram
  (`mp-redes-sociais`), fotos do Perfil no Google, página de portfólio do site
  (`mp-sites-tours`).
- **Atualização:** toda obra concluída com termo de entrega, fotos e
  autorização entra na fila do catálogo. Revisar a cada trimestre: entra a
  obra nova mais forte, sai a mais fraca. A data da edição vai na capa.

## Saída

1. O PDF (ou o boneco, dizendo claramente que é boneco).
2. Lista de pendências: fotos a fazer, dados a confirmar, autorizações.
3. A mensagem de envio.
4. O que foi cortado e por quê, em uma linha por item.

## Limites

- O script diagrama com uma grade fixa, sóbria e consistente. Para um catálogo
  com direção de arte própria, o `catalogo.json` e a seleção de fotos servem
  de roteiro para um designer.
- Não corrige foto ruim. Ambiente escuro, torto, bagunçado ou com flash não
  vira capa com edição.
- O PDF sai em RGB. Para impressão, a gráfica converte para CMYK; por isso a
  prova impressa é obrigatória, principalmente nos tons de madeira.
- Autorização de imagem e crédito de arquiteto e fotógrafo são assunto de
  contrato: o modelo de cláusula é do advogado da MP.
