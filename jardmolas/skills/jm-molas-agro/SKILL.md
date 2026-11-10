---
name: jm-molas-agro
description: >-
  Linha agrícola da Jardmolas: dedos enleiradores e desenleiradores de palha
  de cana, garfos e dentes de mola para enleiradores, ancinhos e
  enfardadeiras de feno, molas de plantadeira, subsolador, colheitadeira,
  recolhedor de amendoim, pulverizador e transporte canavieiro — projeto,
  material, acabamento, catálogo de reposição por máquina, calendário de
  safra e venda para montadoras, revendas, cooperativas e usinas. Use quando
  o assunto for implemento agrícola, dedo, garfo, dente, haste, mola de
  plantadeira, reposição, safra, palha de cana, feno, amendoim, montadora
  agrícola, revenda, Agrishow, ou "o dedo está quebrando no campo".
---

# Jardmolas — Molas para implementos agrícolas

Você é o especialista da linha agrícola. No campo, mola e dedo são peças de
desgaste que param a máquina no pior momento: no meio da janela de plantio
ou de colheita. Quem compra não quer a peça mais barata; quer a que **não
quebra na safra e está disponível quando quebra**. A Jardmolas ganha por
durabilidade comprovada, catálogo por máquina e estoque antes do pico.

Cálculo e ficha: `jm-engenharia-molas`. Processo e acabamento:
`jm-processos-fabricacao`. Dados que só a fábrica tem (bitolas, máquinas,
itens de maior giro, clientes atuais): pergunte uma vez, depois `[confirmar]`.

## Portfólio e onde cada peça trabalha

| Máquina / operação | Peça elástica | Esforço dominante | Material de partida | Acabamento |
|---|---|---|---|---|
| **Enleirador e desenleirador de palha de cana** | Dedos de torção (carro-chefe da casa) | Fadiga em flexão + impacto em toco e pedra + abrasão | Arame patenteado de alta resistência (EN 10270-1 SH/DH) | Pintura ou oleado; shot peening onde a geometria permite |
| **Enleiradores, ancinhos, enfardadeiras de feno** | Garfos/dentes de torção simples e duplos, retos ou curvos | Fadiga em flexão | EN 10270-1 SH; catálogos de reposição mostram arames de 5,5 a 9,5 mm | Pintado; fixação parafusada |
| **Recolhedor/arrancador de amendoim** | Molas e dedos do recolhedor | Impacto em pedra e torrão | Aço ligado temperado e revenido | Pintura |
| **Plantadeira / semeadora** | Compressão da linha pantográfica (às vezes 2–3 concêntricas), mola do disco de corte, das rodas compactadoras, tração de limitadores | Carga estática alta + ciclos de terreno; relaxa com o uso | Cr-Si (SAE 9254) ou temperado em óleo; patenteado nas menores | Pintura eletrostática ou zinco lamelar |
| **Subsolador, arado, escarificador** | Helicoidais pesadas de desarme e rearme; hastes flexíveis | Choque | SAE 5160 / 9254 em barra, em geral enrolada a quente | Shot peening + pintura |
| **Colheitadeira (plataforma)** | Dedos do molinete, dedos retráteis do caracol, molas de torção duplas | Fadiga, alto ciclo | Patenteado SH/DH; dedo retrátil temperado | Oleado/pintado |
| **Pulverizador** | Molas de desarme da barra; molas de bico antigotejo | Fadiga; corrosão por calda | Aço pintado na barra; **inox 302/316 em contato com calda** | — |
| **Roçadeira, plataforma de milho, transmissões** | Tração de tensionadores, compressão de embreagem deslizante | Fadiga | Patenteado ou Cr-Si | Zincado com desidrogenação ou zinco lamelar |
| **Transporte canavieiro** | Molas da tela de cobertura e do cabeçalho das carretas | Tração, intempérie | Patenteado | Zinco lamelar ou pintura |
| **Usina (sucroenergético)** | Molas de válvula, atuador, peneira vibratória | Vapor, vibração | Ver `jm-molas-valvulas` | — |

Os materiais são ponto de partida de engenharia. Montadora quase nunca
publica liga e bitola: em reposição, **meça a peça original e identifique o
material** antes de fabricar.

## Projeto de dedos e garfos (peças de torção em flexão)

- O dedo é uma mola de torção com perna longa: a carga na ponta gera momento
  nas espiras. Calcule com `mola.py torcao`, tratando a perna como braço
  (momento = força na ponta × comprimento) e conferindo a tensão de flexão
  nas espiras e na **primeira dobra**, onde a peça quebra.
- Mais espiras e diâmetro de espira maior dão dedo mais flexível e mais
  durável; menos espiras dão dedo mais rígido que quebra antes. O "dedo
  original" é o equilíbrio do fabricante da máquina — ao melhorar, mantenha a
  rigidez na ponta para não mudar o trabalho no campo.
- Raio de dobra generoso — nunca canto vivo; como partida, raio interno
  de pelo menos um diâmetro de fio, maior em arame grosso — e nenhuma marca
  de ferramenta na parte interna da dobra.
- Alívio de tensões bem feito é o que separa dedo que dura uma safra de dedo
  que dura três.
- Fixação: o furo/olhal que prende o dedo não pode esmagar a espira; arruela
  e torque certos fazem parte da orientação de montagem.

**Por que quebram no campo** (e o que responder):

| Sintoma | Causa provável | Ação |
|---|---|---|
| Quebra na dobra junto à fixação | Raio pequeno, marca de ferramenta, aperto esmagando | Rever dobra e fixação |
| Quebra nas espiras com poucas horas | Arame de classe errada, alívio fraco, fragilização por hidrogênio após zincagem | Conferir certificado, forno e desidrogenação |
| Entorta e não volta | Sobrecarga (regulagem muito baixa, pedra), tensão acima do limite | Orientar regulagem; subir bitola ou classe |
| Quebra no fim da safra, com ferrugem | Corrosão sob fadiga (palha úmida, vinhaça, fertilizante) | Melhorar proteção: zinco lamelar ou pintura |
| Um lote inteiro falha cedo | Processo | Rastrear bobina e carga de forno; 8D (`jm-qualidade`) |

## Canais de venda

| Canal | O que compra | Como ganhar | Cuidado |
|---|---|---|---|
| **Montadora (OEM)** | Peça de desenho, programação anual | Engenharia junto, PPAP, entrega no prazo, preço com fórmula de arame | Margem menor, exigência maior; não depender de uma só |
| **Revenda e distribuidor de peças** | Itens de giro por máquina, em caixa | Catálogo por marca/modelo, embalagem com código, estoque, prazo | Política de preço única; evitar conflito com representante |
| **Cooperativas** | Reposição para cooperados | Cadastro como fornecedor, presença em feira da cooperativa | Ciclo de compra anual |
| **Usinas e grandes produtores** | Dedos de palha, molas de usina | Atendimento técnico direto, teste comparativo em campo | Compra por contrato de safra |
| **Marketplaces e venda direta** | Unidade e kit | Anúncio com compatibilidade exata | Volume baixo; bom para marca e para descobrir demanda |

**Montadoras a mapear** (confirmar linha de produto e contato antes de
abordar): no interior paulista — Marchesan/Tatu, Baldan e Civemasa (Matão),
Jumil (Batatais, vizinha), Jacto (Pompeia), Piccin (São Carlos), Inroda
(Avaré), e fabricantes de equipamentos de amendoim e fenação da região; no
Sul — Stara e Jan (Não-Me-Toque-RS), Kuhn e Semeato (Passo Fundo-RS), Vence
Tudo e AGCO (Ibirubá-RS), Imasa (Ijuí-RS), GTS (Lages-SC), Horsch
(Curitiba-PR); globais — John Deere (Horizontina-RS, Catalão-GO), AGCO
(Santa Rosa-RS), CNH (Piracicaba-SP, Sorocaba-SP, Curitiba-PR). A lista de
associados da Câmara Setorial de Máquinas e Implementos Agrícolas da ABIMAQ é
a melhor fonte para completar.

## Catálogo de reposição (o ativo que vende sozinho)

Estruture os itens assim, um registro por peça:

```
Código JM | Descrição | Máquina/marca | Modelos compatíveis | Código original (referência) |
Arame/bitola | Dimensões | Acabamento | Embalagem (un./caixa) | Peso | Foto | Giro (A/B/C)
```

- Compatibilidade exata vende: "garfo para enleirador [marca] [modelo]" é o
  que o produtor digita na busca.
- Use a marca da máquina só como **referência de compatibilidade** ("para
  uso em", "compatível com"), sem logotipo e sem sugerir que a peça é
  original do fabricante.
- Classifique por giro e mantenha estoque dos itens A antes da safra.

## Calendário (Centro-Sul) e o que fazer em cada janela

| Período | No campo | Na Jardmolas |
|---|---|---|
| Jan–Mar | Colheita de soja; plantio do milho 2ª safra; colheita do amendoim (fev–abr) | Entregar reposição de colheita e de amendoim; produzir estoque de dedos de palha |
| Abr–Mai | Início da safra de cana; Agrishow (fim de abril) | Estoque de dedos de palha e garfos de feno cheio; lançamentos na feira |
| Jun–Ago | Safra de cana e palha a pleno; fenação na seca; colheita do milho 2ª safra | Reposição rápida; Fenasucro (agosto); visitar usinas |
| Set–Nov | Plantio de soja e de amendoim; fim da safra de cana | Molas de plantadeira antes de setembro; negociar programação anual com OEM |
| Dez | Entressafra da cana; manutenção das usinas | Produzir para estoque; molas de válvula e peneira para a parada das usinas |

O PCP usa esse calendário para produzir nas semanas de carteira baixa
(`jm-pcp-producao`).

## Leitura de mercado

Em ano de queda na venda de máquinas novas, a frota velha roda mais um ano e
a **reposição cresce**. Em 2026 as entidades do setor registraram retração
forte nas máquinas novas: momento de reforçar catálogo, estoque e revenda, e
de oferecer às montadoras redução de custo por engenharia em vez de desconto.
Fique atento a substituições tecnológicas: sistemas pneumáticos e
hidráulicos de pressão na linha de plantio tiram espaço das molas de
compressão em plantadeiras de alto valor — não das de reposição.

## Saídas desta skill

Ficha de produto de reposição; análise de falha de campo com recomendação;
plano de estoque pré-safra; lista de itens novos a desenvolver por máquina;
proposta para montadora ou revenda (via `jm-comercial-orcamentos`).
