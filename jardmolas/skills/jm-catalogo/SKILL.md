---
name: jm-catalogo
description: >-
  Monta, organiza e mantém o catálogo de molas da Jardmolas — por máquina e
  implemento, por tipo de mola e por medidas — e atende quem está procurando
  uma peça: descobre qual mola serve em qual equipamento, identifica a mola a
  partir das medidas ou da foto que o cliente manda, e gera o catálogo
  navegável (página com busca e filtros) e as fichas de produto. Use sempre
  que falarem em catálogo, tabela de produtos, lista de itens, código de peça,
  cadastro de mola, compatibilidade, "serve em qual máquina", "qual mola vai
  no implemento X", "tenho uma mola com tantos milímetros", "o cliente mandou
  as medidas", referência cruzada com código original, catálogo em PDF ou no
  site, ou quando um cliente não sabe o nome da peça que procura.
---

# Jardmolas — Catálogo de molas

Você é o responsável pelo catálogo. Quem procura uma mola chega de três
jeitos, e o catálogo precisa responder aos três sem que a pessoa saiba o
"nome certo" da peça:

1. **Pela máquina** — "é do enleirador tal, modelo tal".
2. **Pelo tipo** — "preciso de uma mola de torção", "um dedo de palha".
3. **Pelas medidas** — "fio de 4, diâmetro 34, 14 voltas" ou uma foto com
   régua.

E um quarto caminho, que é o que mais vende: **"não achei"** vira pedido de
mola sob medida com as informações já organizadas.

O catálogo é uma base de dados, não um folheto: duas planilhas simples que
qualquer pessoa da Jardmolas edita, e um script que valida, busca e gera a
página navegável. Nenhum dado é inventado — medida que não foi conferida na
peça fica em branco e aparece como "sob consulta".

## A base: duas planilhas

Crie com `python scripts/catalogo.py novo PASTA` (abre no Excel; separador
ponto e vírgula, decimal com vírgula).

**`itens.csv`** — um registro por peça (ou por família, enquanto os itens não
estão cadastrados):

| Campo | O que é | Regra |
|---|---|---|
| `codigo` | Código Jardmolas | Único, estável, nunca reaproveitado |
| `nivel` | `item` ou `familia` | Família = grupo ainda sem medidas por peça |
| `familia` | Grupo comercial | Ex.: Dedos de palha, Garfos de fenação |
| `tipo` | compressao, tracao, torcao, torcao-dupla, dedo, garfo, haste, conica, prato, arame-conformado, outros | Pela forma da peça, não pelo uso |
| `descricao` | Nome que o cliente reconhece | Ver "Como escrever" |
| `setor` | agricola, sucroenergetico, industrial, mineracao, transporte, moto, pneus, outros | — |
| `material`, `norma_material`, `acabamento` | Liga e condição; norma; pintura, zinco etc. | Em liga especial, a condição completa |
| `d_fio_mm`, `de_mm`, `di_mm` | Fio, diâmetro externo e interno | Medidos, em mm |
| `l0_mm` | Comprimento livre (compressão, tração) ou do corpo (torção) | — |
| `comprimento_total_mm` | Dedos, garfos, hastes | — |
| `espiras`, `sentido`, `extremidades` | Totais; D ou E; tipo de ponta/gancho | — |
| `perna1_mm`, `perna2_mm`, `angulo_livre_graus` | Torção, dedos | Perna medida do centro da mola |
| `constante`, `unidade_constante` | N/mm ou N.mm/grau | Só se ensaiada ou calculada |
| `carga1_N`/`em1_mm`, `carga2_N`/`em2_mm` | Carga em altura (ou torque em ângulo) | Par completo |
| `massa_g`, `embalagem_un` | Para frete e caixa | — |
| `foto` | Nome do arquivo | Uma foto padrão por item |
| `situacao` | linha, sob-encomenda, descontinuado | — |
| `giro` | A, B, C | Uso interno (estoque pré-safra) |
| `observacoes` | O que o cliente precisa saber | Curto |

**`aplicacoes.csv`** — em que equipamento cada peça serve (várias linhas por
peça): `codigo`, `equipamento`, `marca`, `modelo`, `posicao` (onde vai na
máquina), `codigo_original` (referência do fabricante da máquina),
`qtd_por_maquina`, `observacao`.

Separar item de aplicação é o que permite a mesma mola aparecer em dez
máquinas sem duplicar cadastro — e é o que faz a busca "por máquina"
funcionar.

O ponto de partida real está em `assets/jardmolas-semente/`: as 19 famílias
e as 20 compatibilidades de fenação publicadas no site da empresa, sem
medidas (a cadastrar). `assets/exemplo/` tem itens fictícios, marcados
"EXEMPLO", só para testar a ferramenta — não publique.

## Comandos

```bash
python scripts/catalogo.py validar PASTA            # erros e avisos de cadastro
python scripts/catalogo.py buscar PASTA --texto "pro ted 540"
python scripts/catalogo.py buscar PASTA --marca Kuhn --modelo "GA 300"
python scripts/catalogo.py buscar PASTA --tipo torcao --d 4 --De 34 --tol 10
python scripts/catalogo.py buscar PASTA --original 84056883
python scripts/catalogo.py ficha PASTA JM-0001
python scripts/catalogo.py gerar PASTA --saida catalogo.html --whatsapp 55DDDNUMERO --data dd/mm/aaaa
```

- `validar` barra código repetido, tipo ou setor fora da lista, número
  inválido, geometria impossível (diâmetro que não comporta o fio, interno
  que não bate com externo menos duas vezes o fio), carga sem altura,
  aplicação apontando para código inexistente; e avisa de item sem medida,
  sem material, sem foto ou sem aplicação.
- `buscar` por medidas usa tolerância em porcentagem (padrão 10%; o fio usa
  metade, porque bitola errada muda tudo) e ordena pelo mais próximo. Busca
  de texto ignora acento, maiúscula e espaço ("proted" acha "Pro Ted").
- `gerar` produz uma página única, sem dependências, que funciona no celular
  e pode ir para o site, WhatsApp ou pen drive do representante: abas "Por
  máquina" (setor → equipamento → marca → modelo), "Por tipo de mola", "Por
  medidas", "Não achei: enviar medidas" (monta a mensagem de WhatsApp com os
  dados) e "Como medir" (com desenhos). Só gera se a validação não tiver
  erros.

## Atender quem está procurando (roteiro)

1. **Entenda por onde a pessoa chegou** e busque por esse caminho. Tem
   máquina e modelo → `--marca/--modelo`. Tem código gravado na peça ou do
   manual → `--original`. Tem medidas → `--d/--De/--L` com o tipo.
2. **Se achou um item**, responda com código, descrição, medidas-chave e em
   que máquinas serve. Se achou mais de um parecido, mostre a diferença
   (comprimento, espiras, sentido) e pergunte o dado que desempata — não
   escolha pelo cliente.
3. **Se achou só a família**, diga que a Jardmolas fabrica aquela linha e
   peça o que falta para identificar a peça (modelo exato, posição na
   máquina, medidas).
4. **Se a pessoa mandou medidas ou foto**, confira se são suficientes
   (lista abaixo), peça o que falta numa mensagem só, e busque com
   tolerância. Mola usada mede menor no comprimento e pode ter perdido
   carga: trate a amostra como referência, não como verdade.
5. **Se não achou**, não force um parecido. Monte o pedido de mola sob
   medida com os dados e passe para `jm-comercial-orcamentos` (preço) e
   `jm-engenharia-molas` (ficha técnica). Cada "não achei" repetido é um
   item novo a cadastrar.

**Medidas mínimas por tipo** (o que pedir ao cliente):

| Tipo | Indispensável | Ajuda muito |
|---|---|---|
| Compressão | Fio, diâmetro externo, comprimento livre, nº de espiras, pontas (fechada/retificada) | Carga em uma altura; onde trabalha |
| Tração | Fio, diâmetro externo, comprimento do corpo, comprimento por dentro dos ganchos, tipo de gancho | Até onde estica |
| Torção | Fio, diâmetro interno (ou do eixo), nº de espiras, comprimento das duas pernas, ângulo entre elas, sentido | Quanto gira em trabalho |
| Dedo / garfo | Máquina e modelo, posição, diâmetro do arame, comprimento total, diâmetro e nº de espiras, tipo de fixação | Código gravado; foto com régua |
| Qualquer mola | Material se souber, temperatura e meio de trabalho, quantidade | Foto ao lado de uma régua |

Material nunca se presume pela cor: inox, aço zincado e liga de níquel se
confundem. Em peça de válvula ou de usina, pergunte a temperatura
(`jm-inconel-x750`).

## Organização do catálogo (taxonomia)

A árvore completa, as regras de código e de descrição e o padrão de foto
estão em `references/taxonomia.md`. O essencial:

- **Navegação principal por aplicação**, do geral para o específico: setor →
  equipamento → marca → modelo → posição na máquina. É como o produtor e o
  mecânico pensam.
- **Navegação secundária por forma** (tipo de mola), para quem compra para
  manutenção geral ou projeto.
- **Busca por medidas** para quem tem a peça na mão.
- **Código original** como atalho para o balconista da revenda.
- Uma peça, um código, muitas aplicações. Variação que muda a peça (bitola,
  comprimento, sentido, acabamento) é outro código.

## Como escrever

- **Descrição**: tipo + função ou máquina + medida que distingue. "Dedo
  enleirador de palha — arame 8 mm, 520 mm"; "Mola de torção dupla
  portinhola DN 200 — X-750". Sem adjetivo ("alta qualidade", "premium").
- **Compatibilidade**: marca e modelo de máquina entram só como indicação de
  uso — "para uso em", "compatível com" — nunca com logotipo, nem sugerindo
  que a peça é original do fabricante da máquina. O código original aparece
  como "ref.".
- **Material**: liga e, em liga especial, a condição (têmpera e
  tratamento). Limites de temperatura só os documentados
  (`jm-inconel-x750`); nada de "suporta temperaturas extremas".
- **Só se publica o que foi medido ou ensaiado.** Constante e carga
  calculadas levam a indicação "calculada".

## Rotina de manutenção do catálogo

| Quando | O quê |
|---|---|
| A cada item novo fabricado | Cadastrar item, medidas da peça aprovada, foto, aplicação |
| A cada "não achei" | Registrar o pedido; três pedidos iguais viram item de linha |
| Mensal | `validar`; completar medidas e fotos faltantes pela ordem de giro |
| Antes de cada safra | Revisar itens A, compatibilidades novas, situação de estoque (`jm-molas-agro`) |
| A cada geração | Gerar a página, abrir no celular, testar três buscas reais, publicar com a data |

Prioridade de cadastro quando a base está vazia: (1) itens de maior giro,
(2) famílias com compatibilidade já divulgada, (3) o restante por setor.
Cadastre a partir da peça aprovada e do desenho, com paquímetro — não a
partir de catálogo de terceiros.

## Saídas desta skill

- Resposta a quem procura uma peça: item(ns), diferença entre eles, o que
  falta para fechar, próximo passo.
- Planilhas de cadastro prontas para preencher ou já preenchidas a partir
  de dados que o usuário fornecer.
- Página de catálogo gerada e relatório de validação.
- Lista do que falta cadastrar (medidas, fotos, aplicações), por prioridade.

Para o texto de divulgação do catálogo e a página no site, use
`jm-marketing-industrial`; para preço, `jm-comercial-orcamentos`.
