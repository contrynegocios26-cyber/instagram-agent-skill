---
name: jm-conteudo
description: >-
  Produz o conteúdo semanal da Jardmolas para Instagram, LinkedIn, WhatsApp e
  blog a partir do que aconteceu na fábrica e no campo: Reels de máquina
  enrolando arame, teste de carga, "chegou quebrada, saiu nova", entrega para
  usina, e os posts técnicos para gerente de manutenção. Use quando alguém da
  Jardmolas mandar vídeo ou foto da fábrica, pedir "o que eu posto essa
  semana", "legenda", "roteiro", "post para o LinkedIn", ou "pauta do blog".
---

# jm-conteudo

Esta skill adapta para a Jardmolas as skills de Instagram deste repositório
(`/ig-reel`, `/ig-caption`, `/ig-carousel`, `/ig-story`, `/ig-plan`,
`/ig-human`). Use as ferramentas delas; esta aqui diz o que é verdade sobre a
Jardmolas e o que não pode sair.

## Antes de escrever

1. Leia `../../03-conteudo/estrategia.md` (pilares, para quem fala cada rede)
   e `../../03-conteudo/calendario-30-dias.md` (o que está programado).
2. Se a pessoa mandou material bruto (vídeo, foto), descreva o que tem nele
   antes de propor o post. O melhor Reel sai do que já foi filmado.
3. Para o blog e as páginas, leia `../../05-seo-e-site/blog-12-pautas.md`.

## Fatos que podem ser usados

- Fábrica em Jardinópolis-SP, 17 anos, mais de 2.000 modelos, arame Belgo
  Arames, laudo por lote, projeto sob medida, estoque estratégico, programa de
  reciclagem de dedos usados.
- Linhas: dedos de enleirador de palha de cana, feno, capim, recolhedor de
  amendoim, válvulas dupla portinhola e de segurança, atuadores, peneira
  vibratória, carretas canavieiras, moto, pneus.
- Avaliações nota 5 no site (pode citar a frase do cliente com o nome que está
  publicado).

Qualquer outro número (prazo, garantia, capacidade, quantidade de clientes)
só com confirmação da Jardmolas. Escreva `[confirmar]` no rascunho.

## Regras

- No máximo 1 post no feed por dia. Stories à vontade.
- Gancho nos 3 primeiros segundos mostrando a peça ou a máquina, não o logo.
- Gente de verdade e som ambiente funcionam melhor que locução com música
  genérica (lição da auditoria da MP Marcenaria, em
  `../../../relatorios/auditoria-instagram-2026-11-05.md`).
- Segurança aparece certa: EPI no quadro, ninguém perto de máquina sem
  proteção. Se o vídeo mostrar risco, não publique e avise.
- Até 5 hashtags. CTA único: comentar uma palavra (MOLA, CADERNO), chamar no
  WhatsApp ou usar o Identificador de Molas.
- Passe todo texto final por `python3 ../../../skills/ig-human/humanize.py
  arquivo.txt --report` para tirar caractere invisível e travessão.
- Sem "qualidade e excelência", "soluções", "transformar", "não é só X, é Y".
