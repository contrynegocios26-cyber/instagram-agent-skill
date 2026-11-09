# Diagnóstico do site jardmolas.com.br (SEO, conversão e confiança)

Data da leitura: 09/11/2026. Foram baixadas e lidas as 54 URLs do sitemap (`/sitemap.xml`), incluindo a home, mais `/robots.txt` e as URLs `/empresa` e `/sobre`, que dão 404. Títulos, descrições, H1, dados estruturados, formulários e links foram extraídos do HTML. A ordem dos resultados de busca citada aqui veio da ferramenta de busca usada nesta pesquisa, não do Google Brasil com localização em Ribeirão Preto. Ela serve como indicação. A posição real tem que ser conferida no Google Search Console (relatório "Desempenho") e numa busca anônima feita na região.

---

## 1. Resumo em cinco linhas

1. O site já tem as páginas certas, com nomes que o comprador usa (dedo enleirador, válvula dupla portinhola, peneira vibratória). Mas elas não respondem às três perguntas de quem compra reposição: **serve na minha máquina?**, **qual a medida?** e **em quanto tempo chega?**
2. O caminho até o orçamento tem atrito e defeito técnico: o WhatsApp flutuante pede 4 campos antes de abrir a conversa, um link de WhatsApp tem o número errado e o link de telefone não funciona no celular.
3. O formulário é igual em todas as páginas. Ele pede "Empresa" como obrigatória, não tem campo para medida, modelo de máquina, quantidade ou foto, e termina com "Em breve retornaremos o contato", sem prazo.
4. Nenhuma página tem dados estruturados (JSON-LD), a home não tem H1 e há páginas vazias no sitemap (`/teste` e três cópias de `/nova-linha-de-molas...`).
5. A melhor prova de venda do site (dedos que fizeram 200 hectares sem quebra, com depoimentos de operadores) está numa página que não recebe link de nenhuma outra: `/dedos-enleiradores-e-desenleiradores-de-palha-jardmolas`.

---

## 2. O que o site faz bem para quem compra

| Ponto forte | Onde | Por que ajuda a vender |
|---|---|---|
| Menu separado por setor e por aplicação (Implementos, Industrial e Sucroenergético, Mineração, Transporte Canavieiro...) | Menu principal | O comprador acha a linha dele em dois cliques. Cada página tem a palavra que ele digita no Google. |
| Matéria-prima com nome e norma: Belgo Arames, DIN 17223 classes A a D, SAE 1070, 5160, 6150, 9254 | `/materia-prima` | Para o engenheiro, norma e aço citados valem mais que adjetivo. Junto com o laudo por lote, é um argumento técnico que a loja de peças não tem. |
| Laudo técnico por lote e certificado de matéria-prima junto com a mola | `/molas-de-tracao-para-implementos-agricolas`, `/mola-para-peneira-vibratoria`, posts de válvulas | É o documento que o comprador de usina e o fabricante de válvula pedem para cadastrar fornecedor. |
| A página de feno lista modelos de máquina: New Holland ProTed 450 a 880T, ProRotor 290 a 450, Kuhn GA 300 GM, GA 1031, GA 1032+, VB 3100, VBP 3200, Haybob | `/molas-para-enleiradores-e-enfardadeiras-de-feno` | É a única página com compatibilidade. Esse é o formato que faz o produtor achar a peça. Falta escrever "compatível com". |
| A página de válvula dupla portinhola diz o que mandar para orçar (detalhes técnicos, carga, pressão, temperatura, ambiente químico) e cita inox 302, 304 e Inconel | `/molas-para-valvulas-dupla-portinhola` | Começa a falar a língua do engenheiro. Precisa virar tabela e formulário. |
| Prova de campo com número: "Mais de 200 hectares e nenhuma quebra", "O do concorrente, a cada 2 hectares, quebrava um dedo" | `/dedos-enleiradores-e-desenleiradores-de-palha-jardmolas` | É o melhor argumento de venda do site. Está escondido (ver item 4.10). |
| Post do amendoim escrito com vocabulário de campo (arranquio, recolhimento, torção, arrancões por pedra e torrão) | `/mola-para-recolhedor-de-amendoim-como-escolher-a-certa` | Apareceu em primeiro na busca "mola recolhedor amendoim". O tema tem pouca concorrência. |
| 14 depoimentos com nome, incluindo cliente desde 2014 e um fabricante que compra "Molas de Enleirador para nossa linha de montagem" | Home e landing dos dedos | Matéria-prima para avaliações no Google (ver `google-perfil-e-ads.md`). |
| Base técnica: HTTPS, imagens em WebP, canonical em todas as páginas, Google Tag Manager instalado (GTM-WD9FZPZJ), reCAPTCHA no formulário | Todas as páginas | Não há obstáculo técnico grande para medir conversões e indexar. |
| Já aparece em buscas comerciais | Busca "molas agrícolas fabricante reposição implementos" (1º, com `/fabricante-de-molas-originais-e-de-reposicao`), "mola para peneira vibratória fabricante" (4º), "mola recolhedor amendoim" (1º, post do blog) | O domínio tem autoridade para subir. O problema é o que a página entrega depois do clique. |

---

## 3. O que aparece hoje nas buscas (quem ranqueia e com que tipo de página)

| Busca | Quem aparece na frente | Tipo de página que ganha | Jardmolas |
|---|---|---|---|
| dedo enleirador de palha (comprar) | Agromaxxi (R$ 42,00, "aço temperado, 3/8, 500 g, para DMB, Civemasa, Tatu e Dria"), O Agricultor (categoria com preço por tipo: reto, com olhal, tipo 8), Agridisco (código DMB 6.03.01.00.00.013, R$ 31,50), Mercado Livre (kits de 10 e 40) | Página de produto de loja com **preço, medida, peso e marca compatível** | Não apareceu |
| enleirador de palha de cana (modelo) | DMB (páginas do Giropalha e do enleirador de 6 rodas, catálogo em PDF), MF Rural (anúncios) | Ficha técnica do fabricante da máquina | Não apareceu |
| mola recolhedor enfardadeira | Loja Nogueira (código 7220950R, R$ 134,16, AP-41N e Express 4030), Agritork (kits de 10 e 15 molas, "altura 70 mm, largura 160 mm, arame 6 mm"), Loja Novo Campo, Loja JF, Mercado Livre | Produto com **código da peça original e medida** | Não apareceu |
| mola recolhedor amendoim | Jardmolas (post do blog), depois molas de enfardadeira (Nogueira, JF) | Post explicativo | **1º lugar**, mas com post, não com página de produto |
| mola para peneira vibratória fabricante | Molas Eliane (blog e produto), Mix Molas, AMF Molas, Jardmolas, Ciamol | Página de produto de fábrica de molas e posts | 4º |
| mola válvula retenção dupla portinhola | Bray, Vaportec, PWR Mission, AVK, Genebre, Varb, Alcval | Página do **fabricante da válvula** | Não apareceu |
| molas usina entressafra | Artigo USP, Jardmolas (originais e reposição), Quimatic, Ciamol, Solisteel, TecMol | Misto: artigo e página de fornecedor | Aparece |
| fábrica de molas Ribeirão Preto | SSM Molas (Facebook), Guaru Molas (página de SEO por cidade, empresa de Guarulhos), Stock Industrial, Soberana, RC Molas, Normadin (Ribeirão Preto, desde 1994) | Página por cidade e Perfil da Empresa | Não apareceu |
| molas sob medida (SP) | Brizante, Silvana Molas, Lutec, Inam, Molas Elias, Lafer, EKF (orçamento por WhatsApp), Somol | Página de serviço com "amostra ou desenho" | Não apareceu |

Fontes das buscas: [Agromaxxi](https://www.agromaxxi.com.br/produto/dedo-enleirador-de-palha/), [O Agricultor](https://www.oagricultor.com.br/index/categoria/pe-as-para-enleirador-e-desenleirador-de-palha/), [Agridisco](https://www.agridisco.com/603010000013-P), [DMB Giropalha](https://www.dmb.com.br/linha-canavieira/outros-equipamentos/enleirador-de-palha-giropalha), [Loja Nogueira](https://www.lojanogueira.com.br/produto/7220950r/mola-do-recolhedor), [Agritork](https://loja.agritork.com.br/tratores/mola-recolhedor-enfardadeira-nogueira-jf-6mm), [Molas Eliane](https://molaseliane.com.br/molas-para-peneiras-vibratorias/), [PWR Mission](https://pwrmission.com.br/valvulas-de-retencao-dupla-portinhola/), [Guaru Molas](https://www.guarumolas.com.br/mola-industrial/molas-de-torcao/molas-de-torcao-industrial/fabrica-de-mola-de-torcao-no-ribeirao-preto), [Normadin](https://normadin.com.br/en/home-english/), [EKF Molas](https://ekfmolas.com.br/).

**O que isso ensina:** quem ganha a venda de reposição agrícola é a página que mostra **marca compatível, código de referência, medida e preço ou prazo**. O site da Jardmolas tem fábrica, matéria-prima e laudo, coisa que as lojas não têm. Mas falta a parte que as lojas têm.

---

## 4. Falhas de conversão (o que faz o comprador desistir antes de pedir orçamento)

### 4.1 O WhatsApp flutuante pede 4 campos antes de abrir a conversa
O botão verde de todas as páginas abre um formulário com **Nome, Empresa, Email e Telefone, todos obrigatórios**. Só depois disso ele abre o WhatsApp, com a mensagem "Olá, meu nome é {nome} e sou representante da empresa {empresa}...". O produtor rural no celular, no meio do talhão, desiste. A frase "sou representante da empresa" também não serve para quem é dono de fazenda ou mecânico.

### 4.2 Um link de WhatsApp tem o número errado
No topo de todas as páginas há um link `api.whatsapp.com/send?phone=55016991760936`. O "0" depois do 55 faz o WhatsApp não achar o número. O outro link do topo usa `5516991760936`, que está correto.

### 4.3 O telefone não é clicável no celular
O link de ligar é `tel:(16)99176-0936 / (16) 99176-1463 / (16) 99188-1941 / (16) 3663-5901`: os quatro números estão num só link. No celular, a ligação não completa. Cada número precisa ter o seu link, com o fixo e o comercial separados.

### 4.4 Formulário genérico e "Em breve retornaremos o contato"
- Ele é o mesmo em todas as páginas: Nome, Mensagem, Empresa*, Telefone*, Email*, Cidade, UF.
- Não tem campo para máquina (marca e modelo), medidas, quantidade, foto ou desenho.
- "Empresa" obrigatória afasta o produtor pessoa física.
- "Em breve retornaremos o contato" não diz em quanto tempo, nem por qual canal.
- A página `/orcamento` não tem nada além desse formulário.

### 4.5 A galeria de produtos não identifica nada
"Confira alguns modelos de..." mostra de 2 a 17 fotos por página com o botão "EXPANDIR". Nenhuma foto tem nome, código, medida ou máquina. O texto alternativo é sempre o nome da página ("Dedos para Enleiradores de Palha"). O comprador não consegue dizer "quero o modelo da foto 3".

### 4.6 Nenhuma página diz como medir nem o que mandar
Exceção parcial: válvula dupla portinhola. O comprador não sabe se precisa mandar foto, amostra, código da peça original ou medida, e quais medidas.

### 4.7 Falta o que o comprador pergunta primeiro
Prazo de entrega, prazo de resposta, frete (CIF ou FOB), pedido mínimo, se vende peça avulsa, horário de atendimento e condição de garantia. Nada disso aparece em página nenhuma.

### 4.8 O mesmo CTA serve para todos
O agricultor, o mecânico, o comprador de usina e o engenheiro de válvula veem o mesmo "SOLICITE UM ORÇAMENTO". Cada um precisa de uma mensagem e de um campo diferentes.

### 4.9 Não há caminho para quem tem a mola na mão e não sabe o nome dela
Este é o espaço do **Identificador de Molas** (`/identificador-de-molas`): o cliente mede com paquímetro, a página calcula e manda o orçamento pronto pelo WhatsApp. Ele precisa estar em todas as páginas de produto, acima da dobra.

### 4.10 A melhor prova de venda está numa página órfã
A página `/dedos-enleiradores-e-desenleiradores-de-palha-jardmolas` tem "Mais de 200 hectares e nenhuma quebra", "O do concorrente, a cada 2 hectares, quebrava um dedo. Hoje fiz, até agora, 10 hectares, e o da Jardmolas não quebrou nenhum" e "Fechamos o dia com 22 hectares e não quebrou nenhum dedo". Nenhuma página do site aponta para ela, e ela compete com `/dedo-enleirador-de-palha` pela mesma busca.

---

## 5. Falhas de SEO

| # | Falha | Evidência | Efeito |
|---|---|---|---|
| 5.1 | **Home sem H1** | A home só tem H2. O primeiro é "Fabricante de molas para os Setores Agrícolas e Industriais noBrasil" (sem espaço em "no Brasil"). | O Google perde o sinal principal do tema da página mais forte do site. |
| 5.2 | **Nenhum dado estruturado** | 0 blocos JSON-LD nas 54 páginas. Não há LocalBusiness, Product, Service, FAQPage nem BreadcrumbList. | Perde visibilidade em busca local e em respostas de IA, e o Google tem que adivinhar endereço e telefone. |
| 5.3 | **Títulos genéricos ou longos demais** | Produto: "Molas industriais - Jardmolas" (29 caracteres), "Mola para choque - Jardmolas" (28). Blog: 11 dos 12 posts da listagem têm título entre 61 e 75 caracteres e são cortados na busca. | Títulos sem aplicação, máquina ou benefício perdem clique para as lojas. |
| 5.4 | **Meta description padrão repetida** | "Há 16 anos, a JARDMOLAS vem se consolidando..." aparece em `/orcamento`, `/blog`, `/teste`, nas três `/nova-linha...`, em `/alta-procura...`, em `/dedos-enleiradores-e-desenleiradores...`, na home e na política de privacidade. | Descrição duplicada e com idade errada (ver 6.1). |
| 5.5 | **Páginas vazias indexáveis e no sitemap** | `/teste` (só o título "Teste"), `/nova-linha-de-molas-oferece-maior-resistencia-no-campo` e as cópias `-Ogu17o` e `-996nme` (vazias), `/alta-procura-por-molas-duraveis-para-implementos-agricolas` (só o título). Todas têm canonical para si mesmas. | Conteúdo raso e duplicado puxa para baixo a avaliação do site inteiro. |
| 5.6 | **Páginas de categoria quase sem texto** | Mineração: 12 palavras. Moto, Pneus, Transporte Rodoviário: 13 cada. Transporte Canavieiro: 22. Molas Industriais: 41. Implementos Agrícolas: 68. | Essas páginas deveriam ranquear para os termos amplos ("molas para mineração", "molas industriais") e não têm conteúdo para isso. |
| 5.7 | **Páginas de produto com texto de "artigo genérico"** | "Neste artigo, exploramos..." aparece em páginas de produto. A página de compressão para usinas fala de "brinquedos", "dispositivos médicos" e "nanotecnologia". | O comprador de usina não se reconhece. O Google vê conteúdo genérico e igual ao de qualquer fábrica de molas. |
| 5.8 | **Faltam medidas, códigos e compatibilidade** | Só a página de feno cita máquinas, e sem escrever "compatível com". Nenhuma página traz bitola, comprimento, número de espiras ou código. | Quem busca "dedo DMB Giropalha" ou "mola 7220950R" cai na loja concorrente. |
| 5.9 | **Erros de cópia** | Em `/molas-do-cabecalho-para-carretas` há o subtítulo "Como Funcionam as Molas Para Tela de Cobertura?". Em `/molas-do-enleirador-de-capim`, o título fala de enleirador, mas o texto fala de "Mola Prata Mil" para "ceifadeiras utilizadas na colheita de sementes de capim". | Confunde o leitor e o Google. [confirmar com a Jardmolas o que é a "Mola Prata Mil" e em qual máquina ela trabalha] |
| 5.10 | **Canibalização** | Dedo enleirador: `/dedo-enleirador-de-palha`, a landing `/dedos-enleiradores-e-desenleiradores...` e 5 posts sobre o mesmo tema. Também `/mola-para-moto` com `/mola-para-descanso-de-moto` e `/molas-para-pneus` com `/molas-para-montadoras-de-pneu`. | Várias páginas fracas disputam a mesma busca em vez de uma página forte. |
| 5.11 | **Faltam páginas de alto potencial** | Não há página de produto para amendoim (só o post), para mola de enfardadeira separada do enleirador, para usinas na entressafra, nem página local (Ribeirão Preto e região). | São buscas com intenção de compra e pouca concorrência boa. |
| 5.12 | **Blog sem data, sem autor e sem link para o produto certo** | A listagem não mostra datas. Os posts não têm autor nem link interno para a página de produto correspondente com texto âncora descritivo. | O post não passa autoridade para a página que vende. |
| 5.13 | **Imagem de compartilhamento quebrada na home** | `og:image` aponta para `https://jardmolas.com.br/placeholder.jpg?400x400`. | Quando alguém manda o link da home no WhatsApp, a prévia sai sem foto. Isso pesa num negócio que vende pelo WhatsApp. |
| 5.14 | **Texto alternativo repetido e logos sem alt** | Pelo menos 4 imagens por página sem `alt`. As fotos de produto repetem o mesmo alt. | Perde busca de imagens ("dedo enleirador foto") e acessibilidade. |
| 5.15 | **`keywords` vazia e erro de digitação** | `<meta name="keywords" content="">`. H1 "Molas sob-medida", com hífen, e "WhastApp" no post do amendoim. | Detalhe, mas aparece para o cliente. |

---

## 6. Falhas de confiança

| # | Problema | Onde | Correção |
|---|---|---|---|
| 6.1 | **Idade da empresa em três versões**: "Há 16 anos" (meta description), "17 anos" (textos) e "fundação em 01/03/2008" (página Empresa). Em novembro de 2026, isso dá 18 anos. | Home, Empresa, várias páginas | Escrever "desde 2008", que não envelhece. |
| 6.2 | **Garantia sem prazo**: "Garantia superior ao mercado", "Garantia estendida", "Garantia Robusta" | Dedos, feno, peneira, cabeçalho, tela, atuadores | Publicar prazo, o que cobre e como acionar. [confirmar com a Jardmolas]. Concorrentes publicam: um kit no Mercado Livre diz "Garantia de fábrica: 30 dias" e a Agritork diz "garantia de 10 dias". |
| 6.3 | **"Fabricação conforme ISO 9001" e "processos certificados ISO 9001"** | `/molas-para-atuadores-em-implementos-agricolas`, `/molas-para-atuadores-industriais-e-usinas` | Se não houver certificado, retirar já: o comprador de usina pede o certificado no cadastro. Se houver, mostrar número, organismo certificador e validade. [confirmar com a Jardmolas] |
| 6.4 | **Números sem fonte**: "Aumento de até 20% na produtividade do canavial", "Redução de custos com herbicidas", "Entrega imediata para todo o Brasil" | `/dedo-desenleirador-de-palha` | Retirar ou citar a fonte. Trocar "entrega imediata" pelo prazo real por região. [confirmar com a Jardmolas] |
| 6.5 | **Tabela técnica que um engenheiro vai contestar**: "Temperatura máxima 550 °C" para mola em inox 302/304 e "980 °C" para Inconel | `/molas-para-valvulas-dupla-portinhola` | Catálogos de válvula dupla portinhola usam limites bem menores para a mola. O da [PWR Mission](https://pwrmission.com.br/wp-content/uploads/2022/09/catalogo_dupla_portinhola.pdf) indica inox 316 até 250 °F (121 °C), Inconel 600 até 600 °F (316 °C) e Inconel X-750 até 1000 °F (538 °C). O valor "550" pode ter vindo de °F lido como °C. Revisar com a engenharia da Jardmolas antes de qualquer outra mudança nessa página. |
| 6.6 | **Superlativos sem dado**: "líder", "domina o mercado brasileiro", "a fabricante de molas agrícolas mais bem avaliada do mercado", "melhor fabricante de molas agrícolas do Brasil" | Home, Empresa, formulário | Trocar por fatos verificáveis: desde 2008, mais de 2.000 modelos, arame Belgo com certificado, laudo por lote, clientes como fabricante de implemento (com autorização). |
| 6.7 | **"Equipe técnica composta por engenheiros e metalurgistas", "softwares avançados de simulação"** | Válvulas, sob medida | Mostrar: nome e função do responsável técnico, foto do laboratório ou da bancada de ensaio. [confirmar com a Jardmolas] |
| 6.8 | **Endereço diferente nos cadastros**: o site diz Rua Artur Costacurta, 340. Diretórios mostram 340 e 450, e a Econodata lista uma filial no 450 ([Econodata](https://www.econodata.com.br/consulta-empresa/09394583000157-jardmolas-industria-e-comercio-de-molas-ltda), [Solutudo](https://www.solutudo.com.br/empresas/sp/jardinopolis/metalurgica)). | Diretórios externos | Definir um endereço de atendimento e padronizar nome, endereço e telefone em todos os cadastros e no Perfil da Empresa. [confirmar com a Jardmolas] |
| 6.9 | **Depoimentos sem contexto** | Home, landing dos dedos | Acrescentar cidade, tipo de operação e máquina (com autorização), e levar os clientes a avaliar no Google (ver `google-perfil-e-ads.md`). |
| 6.10 | **Texto ambíguo sobre certificado**: "Orgulhamo-nos de possuir o certificado Belgo Arames, um selo de qualidade reconhecido internacionalmente" | `/materia-prima` | A certificação é do fornecedor do arame. Escrever: "usamos arame Belgo Arames e entregamos o certificado do lote de arame junto com o laudo da mola". Mostrar um exemplo (com dados ocultos). |
| 6.11 | **Norma antiga sem equivalência** | `/materia-prima` | A DIN 17223 parte 1 foi substituída pela EN 10270-1. Citar as duas ("DIN 17223 classes A a D, hoje EN 10270-1") evita a pergunta do engenheiro. |
| 6.12 | **Nenhuma foto da fábrica, das máquinas de enrolar, de ensaio ou do estoque** | Site inteiro | Fotos reais pesam mais que qualquer selo. Ver as sugestões em cada página da pasta `paginas/`. |

---

## 7. Lista de correções em ordem de impacto

Impacto é o efeito esperado em número de orçamentos. Esforço: **baixo** (até 1 dia do webmaster, sem depender de dados da Jardmolas), **médio** (alguns dias, ou depende de informação da Jardmolas), **alto** (semanas, ou depende de levantamento interno grande).

| Ordem | Correção | Esforço | Detalhe |
|---|---|---|---|
| 1 | **Consertar o WhatsApp e o telefone, e abrir o WhatsApp direto.** Corrigir o link `55016991760936` para `5516991760936`. Separar os quatro números em links `tel:` próprios (`tel:+5516991760936`, `tel:+551636635901`...). Fazer o botão flutuante abrir `https://wa.me/5516991760936?text=` com mensagem pronta por página, sem formulário. O nome e a empresa a equipe pergunta na conversa. | Baixo | Afeta todas as páginas. É a correção com maior retorno por hora de trabalho. |
| 2 | **Publicar o Identificador de Molas em `/identificador-de-molas` e pôr o CTA em todas as páginas de produto**, acima da dobra e no fim do texto: "Tem a mola na mão? Meça com paquímetro e mande o orçamento pronto pelo WhatsApp". | Médio | Já está em construção. Medir "Identificador concluído" como conversão. |
| 3 | **Trocar o formulário genérico por um orçamento técnico por linha.** Campos opcionais: máquina (marca e modelo), código da peça antiga, medidas, quantidade, foto ou desenho (upload), CPF ou CNPJ. "Empresa" deixa de ser obrigatória. Trocar "Em breve retornaremos o contato" por "Respondemos em até [X] horas úteis pelo WhatsApp ou e-mail" [confirmar com a Jardmolas]. | Médio | Usar a tabela "o que mandar para orçar" de cada página da pasta `paginas/`. |
| 4 | **Reescrever as 8 páginas prioritárias** com compatibilidade ("compatível com [marca/modelo]"), como identificar, materiais, prazo, FAQ e JSON-LD. | Médio | Textos prontos em `paginas/`. Os dados marcados [confirmar com a Jardmolas] precisam ser preenchidos antes de publicar. |
| 5 | **Trocar a galeria "EXPANDIR" por uma tabela de referência**: foto, código Jardmolas, aplicação, "compatível com", arame (bitola e aço), medidas principais e "pedir este modelo" (abre o WhatsApp com o código). | Alto | Depende de a Jardmolas levantar os códigos dos modelos mais vendidos. Começar pelos 20 mais pedidos de dedo, feno e amendoim. |
| 6 | **Limpar o índice.** Excluir ou marcar `noindex` e tirar do sitemap: `/teste`, as três `/nova-linha-de-molas-oferece-maior-resistencia-no-campo*` e `/alta-procura-por-molas-duraveis-para-implementos-agricolas`. Redirecionar (301) para a página de categoria mais próxima, se alguma tiver link externo. | Baixo | |
| 7 | **H1 na home, títulos e descrições por página, JSON-LD.** Sugestão de H1 para a home: "Fábrica de molas agrícolas e industriais em Jardinópolis-SP". Bloco LocalBusiness em todas as páginas; Product ou Service e FAQPage nas de produto. Trocar o `og:image` placeholder por uma foto real. | Baixo a médio | Modelos de JSON-LD em cada arquivo de `paginas/`. |
| 8 | **Retirar ou comprovar as afirmações frágeis**: ISO 9001, "até 20% de produtividade", "entrega imediata", "550 °C", "líder", "mais bem avaliada". Unificar "desde 2008". Publicar garantia com prazo. | Baixo (texto), depende de informação | Itens 6.1 a 6.7. |
| 9 | **Levar a prova de campo para a página do produto.** Colocar os depoimentos com hectares (Sérgio Costa, Luís Gonçalves, Adriano Gomes) e o caso dos 200 hectares em `/dedo-enleirador-de-palha` e em `/dedo-desenleirador-de-palha`. Depois, redirecionar (301) a landing `/dedos-enleiradores-e-desenleiradores-de-palha-jardmolas` para `/dedo-enleirador-de-palha`. Se a landing for usada em anúncio, deixá-la com `noindex`. | Baixo | Pedir autorização por escrito aos clientes citados. |
| 10 | **Registrar as conversões no GTM e no GA4**: clique no WhatsApp (por página), clique no telefone, envio do formulário, Identificador concluído. Importar essas conversões no Google Ads. | Baixo | Sem isso, não dá para saber qual página gera orçamento. |
| 11 | **Perfil da Empresa no Google**: reivindicar ou verificar o perfil, padronizar nome, endereço e telefone, cadastrar produtos e pedir avaliações aos clientes que já elogiaram. | Baixo | Passo a passo em `google-perfil-e-ads.md`. |
| 12 | **Criar as páginas novas**: `/mola-para-enfardadeira-de-feno`, `/mola-para-recolhedor-de-amendoim`, `/molas-de-reposicao-para-usinas`, `/fabrica-de-molas-ribeirao-preto`. Ligar o post do amendoim à nova página de produto. | Médio | Textos prontos em `paginas/`. |
| 13 | **Fotos e vídeos reais**: mola com paquímetro mostrando a bitola, peça instalada na máquina, lote etiquetado com laudo, fábrica, ensaio. | Médio | Lista por página em `paginas/`. |
| 14 | **Dar conteúdo às páginas de categoria** (Mineração, Industriais, Implementos, Transporte Canavieiro) com 300 a 500 palavras: aplicações, máquinas e links para cada produto. Juntar `/mola-para-moto` com `/mola-para-descanso-de-moto` e `/molas-para-pneus` com `/molas-para-montadoras-de-pneu`, ou diferenciar o conteúdo. | Médio | |
| 15 | **Corrigir os erros de cópia** do cabeçalho ("Tela de Cobertura" no lugar errado) e do enleirador de capim ("Mola Prata Mil"). Revisar "WhastApp" e "sob-medida". | Baixo | [confirmar com a Jardmolas o produto "Prata Mil"] |
| 16 | **Blog com calendário fixo** (2 posts por mês), com data e autor visíveis e link para a página de produto. | Médio | Pautas em `blog-12-pautas.md`. |

### As 3 correções que mais vão gerar orçamento
1. **WhatsApp direto e telefone clicável** (itens 1 e 10). Hoje o principal canal de quem está no campo tem um formulário de 4 campos na frente, um link quebrado e um telefone que não liga.
2. **Identificador de Molas e formulário técnico com prazo de resposta** (itens 2 e 3). Quem não sabe o nome da peça passa a conseguir pedir orçamento, e a equipe recebe medida, foto e quantidade na primeira mensagem, sem vai e volta.
3. **Páginas de produto com "compatível com [marca/modelo]", medidas e tabela de referência** (itens 4 e 5), começando por dedo enleirador de palha, feno e amendoim. É exatamente o que as lojas que hoje ganham a busca mostram e a Jardmolas não mostra.

---

## 8. Dados que só a Jardmolas tem (preencher antes de publicar as páginas novas)

- Prazo de resposta do orçamento (horas úteis) e horário de atendimento do WhatsApp.
- Prazo de entrega: item de estoque, item sob medida (lote piloto e lote de produção), por região.
- Garantia: prazo, o que cobre, como acionar.
- Pedido mínimo, se vende peça avulsa, frete (CIF ou FOB), transportadoras e se entrega na usina.
- Quais modelos de dedo, dente e mola estão em linha, com código, e para quais máquinas são compatíveis.
- Faixa de fabricação: bitola mínima e máxima de arame, diâmetro externo máximo, comprimento máximo, tipos (compressão, tração, torção, dupla torção, forma de arame).
- Tratamentos que fazem: alívio de tensões, revenimento, jateamento com granalha (shot peening), pintura, zincagem, fosfatização.
- Ensaios que fazem: carga x deflexão, dureza, fadiga, e o que vai no laudo do lote.
- ISO 9001: existe certificado? Número e validade.
- Como funciona o programa de reciclagem de dedos usados.
- O que é a "Mola Prata Mil" e em qual máquina ela trabalha.
- Endereço oficial de atendimento (340 ou 450) e horário de funcionamento.
- Autorização dos clientes cujos depoimentos serão usados com nome, cidade e máquina.
