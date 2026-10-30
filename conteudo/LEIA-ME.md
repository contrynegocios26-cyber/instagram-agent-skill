# Conteúdo da MP Marcenaria (@mp.marcenariaa)

Tudo o que já foi feito para o Instagram, uma pasta por post. A lista
completa, com data, status e link, está em [CATALOGO.md](CATALOGO.md). A mesma
lista, para abrir no Excel, está em `catalogo.csv`.

## Como está organizado

| pasta | o que tem | hoje |
| --- | --- | --- |
| `0-material-bruto` | fotos e vídeos que chegaram e ainda não viraram post | vazia aqui (o bruto está no PC, ver abaixo) |
| `1-postados` | já está no Instagram, com link, plays e curtidas | 12 reels, todos de 29/10/2026 |
| `2-prontos-para-postar` | legenda e mídia prontas, falta publicar | 57 do calendário (03/11/2026 a 09/02/2027) + 5 sem data |
| `3-em-producao` | falta terminar | 5 vídeos 3D sendo feitos no PC |
| `4-ideias` | ainda não foi gravado | 10 ideias de reels + 20 roteiros "o que gravar" |

Cada post tem uma pasta com nome `AAAA-MM-DD_tipo_tema`. A data é a do dia
em que foi postado ou em que está marcado para sair. O que não tem data
começa com `sem-data_`. Dentro da pasta fica o `info.md`, com a legenda
completa, os avisos e o campo `arquivos_pc`, que diz onde estão os
arquivos no PC.

**O status de um post é a pasta onde ele está.** Quando publicar, arraste a
pasta de `2-prontos-para-postar` para `1-postados` e cole o link no
`info.md`. Ou use o comando, que faz as duas coisas:

    python catalogo.py postar 2026-11-03_carrossel_familia-valerio --link https://www.instagram.com/p/XXXX/

Depois de mexer em qualquer coisa, rode `python catalogo.py` para atualizar
o catálogo.

## A pasta no PC

Os vídeos e as fotos de verdade estão no seu PC, em
`D:\Usuario\Downloads\projetos.arquitetos\conteudo_redes_sociais\`. Esse
comando cria a pasta organizada ao lado e copia cada arquivo para a pasta do
seu post. Ele não move nem apaga nada:

    python catalogo.py montar --origem "D:\Usuario\Downloads\projetos.arquitetos\conteudo_redes_sociais" --destino "D:\Usuario\Downloads\projetos.arquitetos\MP_CONTEUDO"

Os 12 reels postados ficam só com a capa, porque os vídeos originais não
estão nessa pasta. O material bruto (fotos de obra do WhatsApp, simulações
do ChatGPT, PDFs dos arquitetos) continua em
`projetos.arquitetos\projetos_organizados\`.

## Conteúdo novo

1. Coloque a foto ou o vídeo em `0-material-bruto`.
2. Crie a pasta do post. O arquivo sai do bruto e vai para a pasta nova:

       python catalogo.py novo reel "cozinha verde" --status producao --midia VID_20261030.mp4

3. Escreva a legenda no `info.md` e, quando estiver pronto, mova para
   `2-prontos-para-postar`.

## Antes de postar, resolva

- **Dois números de WhatsApp.** Os reels postados usam (44) 99884-6314. Todo o
  conteúdo novo e o link da bio usam (44) 99833-5946. Confirme qual é o certo
  antes do primeiro post de novembro.
- **Hashtags demais.** Quase todas as legendas prontas têm de 6 a 10 hashtags,
  e o Instagram aceita no máximo 5 por post desde dezembro de 2025. O
  `info.md` de cada post diz quantas tirar.
- **Três reels postados com texto de modelo na legenda.** O deck de piscina, a
  sala de TV e a parede de cabeceira ainda mostram "📍 [cidade]" ou
  "[alto- Paraná]". A parede de cabeceira também repete "Veios marcados". Dá
  para editar a legenda no Instagram.
- **Possíveis repetidos.** O ripado com LED, os dois posts de pergolado e o La
  Reserva parecem com reels que já saíram em 29/10. O `info.md` de cada um
  diz com qual reel comparar.
- **Créditos.** Falta confirmar o nome do escritório "LC" (Casa NG) e de quem
  são o Quarto com Mezanino e o Gourmet em Dois Tons.
- **Apartamento em Maringá 3D.** Decida se ele entra no lugar do "Do zero: La
  Reserva" de 18/01/2027.
- **Um post por dia.** Os 12 reels saíram todos em 29/10, entre 7h e 17h33, e
  disputaram alcance entre si. O calendário novo já está espaçado.

## De onde veio cada coisa

- **Postados:** o perfil público @mp.marcenariaa, lido em 30/10/2026 às 14:39.
  Os números são do primeiro dia e ainda vão mudar. A ferramenta devolve só o
  começo de cada legenda.
- **Prontos, em produção e roteiros:** a conversa do Claude que roda no seu
  PC ("Análise e conteúdo para redes sociais"), que montou a
  [Central de Postagens](https://claude.ai/artifact/S7jor9cAAfnP3pBFNqLAEV).
- **Pixel art da oficina:** a conversa "Pixel agents", de 29/10.
- **10 ideias de reels:** os Pacotes da manhã de 29 e 30/10, no Google Drive.
