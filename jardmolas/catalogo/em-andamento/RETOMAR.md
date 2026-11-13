# Catálogo de molas agro — ponto de retomada (13/11/2026)

O que está pronto e publicado no branch: `catalogo/catalogo-jardmolas-molas-agro.pdf`
(56 páginas, 20 setores, 283 códigos), a base `catalogo/referencias-agro.csv` e o gerador
`skills/jm-catalogo/scripts/referencias.py`.

## Pedido em andamento (ainda NÃO aplicado ao PDF)

1. Separar as molas por categorias, começando por "implementos agrícolas para cultivos".
2. Tratores: tirar tudo. A Jardmolas só fabrica as molas do banco do trator.
3. Tirar as fotos do site (fica só a logo) e usar fotos da internet de molas em implementos
   agrícolas no Brasil, que possam ser usadas no catálogo.
4. Voltar com os agentes de pesquisa e pôr mais. Sem erros.

## Estrutura de categorias proposta

- A. Implementos para cultivos: preparo de solo; plantio; pulverização e distribuição;
  colheita de grãos; cana-de-açúcar; café; algodão; amendoim; feijão, mandioca e
  hortaliças; fruticultura e citros.
- B. Fenação, forragem e pastagem: fenação; ensilagem; roçadeiras e trituradores.
- C. Pecuária e granjas: pecuária, ordenha e cercas; avicultura e suinocultura.
- D. Irrigação.
- E. Pós-colheita e transporte: armazenagem; carretas agrícolas.
- F. Componentes e portáteis: eixo cardan de implementos; banco de trator; florestal e
  máquinas portáteis.

## O que há nesta pasta

- `pesquisa-bruta/`: os JSON da primeira pesquisa (466 linhas), de onde saiu a base.
- `pesquisa-nova/`: instruções dos agentes (`LEIA-ANTES.md`) e os JSON da segunda pesquisa,
  que confere os códigos nas páginas e amplia. Cada linha traz `acao` (nova, confirma,
  corrige, descarta), `id_base`, `verificado` (pagina ou busca) e `trecho`.
- `fotos-internet/`: fotos de licença livre escolhidas, com `manifesto.json` (autor,
  licença, página de origem), quando os agentes de fotos terminarem.
- `curar.py`: script que transformou a pesquisa bruta na base (regras editoriais e ajustes
  linha a linha). Os caminhos apontam para a pasta temporária da sessão: ajustar ao rodar.

## Próximos passos, na ordem

1. Juntar a pesquisa nova à base: aplicar `confirma` (marcar `conferido`), `corrige` e
   `descarta`; incluir as `nova` pelas mesmas regras editoriais (ver SKILL.md do
   `jm-catalogo`). Linha `verificado: pagina` vale mais que `busca`.
2. Lançar a segunda leva de agentes: fenação, ensilagem e roçadeiras; pecuária, avicultura
   e irrigação; armazenagem, carretas e florestal.
3. `mapa-agro.json`: acrescentar a categoria de cada setor; trocar o setor "Tratores,
   cardans e engates" por "Banco de trator" e "Eixo cardan de implementos"; na base, pôr
   as linhas de trator como `fora: trator (só fabricamos molas de banco)`.
4. Modelo e gerador: abertura de categoria, sumário por categoria, sem as fotos do site
   (capa, página da empresa, galeria, faixas de setor, cartões "o que fabricamos"), fotos
   da internet com página de créditos (autor e licença de cada foto).
5. Gerar, conferir página por página, copiar o PDF para `catalogo/`, empacotar a skill,
   commit e push.

## Limites de rede já conhecidos

- Abrem com curl: thorcomponentes.com.br, www.agridisco.com, ingapecas.com,
  www.agrotrator.com.br, www.jbagricola.com.br, hh.net.br, www.commersul.com.br,
  unifort.com.br, plantforte.com.br, www.plantiodistribuidora.com.br, www.acamargo.com,
  loja.agritork.com.br, shop.bigdutchman.com, commons.wikimedia.org, api.openverse.org.
- Não abrem: catalogo.marchesan.com.br (só HTTP), lojas da Jumil (certificado inválido).
- Bloqueiam robô (não contornar): gb.sparex.com, partao.com, www.lojanogueira.com.br.

## Decisões que dependem do dono

- Rosca sem-fim do adubo: a Jardmolas fabrica? (10 códigos guardados, fora do catálogo.)
- Manter ou tirar as referências de catálogos de reposição (Thor, Unifort, Sparex)?
- Molas de embreagem de cardan: manter (o cardan é do implemento) ou tirar junto com trator?
- Versão com sangria para gráfica?
