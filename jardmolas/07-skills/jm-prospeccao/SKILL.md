---
name: jm-prospeccao
description: >-
  Roda a prospecção diária da Jardmolas: escolhe os alvos do dia (usinas,
  fabricantes de válvulas e peneiras, revendas e cooperativas), escreve as
  mensagens personalizadas por cargo e canal, registra no funil e lembra os
  follow-ups. Use quando alguém pedir "quem eu chamo hoje", "escreve a
  mensagem para o gerente da usina X", "prospecção", "follow-up", "funil",
  "lista de usinas", ou colar um perfil de LinkedIn de um comprador.
---

# jm-prospeccao

## Fontes que esta skill usa

- Alvos: `../../04-mercado-e-alvos/usinas-alvo.md` e
  `../../04-mercado-e-alvos/oem-revendas-e-associacoes.md`.
- Mensagens base e sequência de 21 dias: `../../01-caderno-de-molas/abordagem-usinas.md`.
- Objeções: `../../01-caderno-de-molas/objecoes.md`.
- Funil: `funil.csv` nesta pasta (crie se não existir) com o cabeçalho
  `alvo;grupo;cidade;prioridade;contato;cargo;canal;etapa;ultimo_toque;proximo_toque;observacao`.

## Etapas do funil

`mapeado` → `contato_feito` → `respondeu` → `visita_marcada` → `caderno_entregue`
→ `pedido_entressafra` → `estoque_garantido`. Perdido vira `nao_agora` com a
data para voltar.

## Rotina do dia (15 minutos)

1. Leia `funil.csv`. Liste quem tem `proximo_toque` hoje ou atrasado.
2. Complete até 10 toques por dia com novos alvos de prioridade A (até 60 km),
   depois B. Um grupo com várias usinas vale mais que uma usina sozinha:
   comece pela unidade mais perto e cite as outras no segundo contato.
3. Para cada toque, escreva a mensagem pelo cargo:
   - **gerente de manutenção industrial / PCM:** a mola que para a máquina,
     a entressafra, o caderno com código;
   - **suprimentos / compras:** pedir pelo código, menos cotação, preço
     travado no Estoque Garantido;
   - **gerente agrícola / oficina:** dedos de enleirador, cabeçalho de
     carreta, tela de cobertura, kit pré-safra;
   - **engenheiro de fabricante (OEM):** mola em série com laudo por lote,
     desenho, protótipo.
4. Atualize `funil.csv` com a etapa e o próximo toque.
5. No fim da semana, mostre: toques feitos, respostas, visitas marcadas,
   cadernos entregues, pedidos.

## Regras das mensagens

- Até 5 linhas no LinkedIn e no WhatsApp. Um motivo concreto, uma pergunta.
- Cite algo verdadeiro da usina (unidade, cidade, grupo), nunca dado que você
  não confirmou.
- Sem "parceria", "soluções", "excelência", "espero que esteja bem", travessão.
- Uma ligação vale mais que três mensagens: depois de dois toques sem
  resposta, sugira ligar e use o roteiro de `abordagem-usinas.md`.
- Não envie nada sozinho. Esta skill escreve; a pessoa da Jardmolas envia.
