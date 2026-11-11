# Taxonomia, códigos e padrões do catálogo

## Árvore por aplicação (navegação principal)

A árvore abaixo parte das linhas que a Jardmolas divulga. Equipamentos sem
itens cadastrados ficam fora da página até terem pelo menos uma família.

```
Implementos agrícolas
├── Palha de cana ........ enleirador · desenleirador
├── Fenação .............. enleirador rotativo · espalhador · ancinho · enfardadeira
├── Amendoim ............. arrancador · recolhedor
├── Sementes de capim .... colhedora
├── Plantio .............. plantadeira/semeadora (linha, disco de corte, compactador, limitador)
├── Preparo de solo ...... subsolador · arado · grade · escarificador · cultivador
├── Colheita de grãos .... plataforma (molinete, caracol) · plataforma de milho
├── Pulverização ......... barra · bicos
├── Roçada e transmissão . roçadeira · tensionadores · embreagens
└── Atuadores de implementos
Sucroenergético e usinas
├── Válvulas ............. retenção dupla portinhola · segurança e alívio
├── Atuadores
├── Peneiras e transportadores
└── Transporte canavieiro  tela de cobertura · cabeçalho de carreta
Indústria e válvulas
├── Retenção ............. dupla portinhola · axial · pistão
├── Esfera trunnion ...... mola de sede · antiestática
├── Segurança e alívio
├── Atuadores
└── Compressão, tração e torção sob desenho
Mineração ................ peneira vibratória
Transporte ............... rodoviário · carretas
Motocicletas ............. descanso
Pneus e borracharia ...... montadora de pneu
```

Para cada equipamento, a aplicação desce até **marca → modelo → posição na
máquina**. A posição ("pressão da linha", "rotor, braço externo") é o que
desempata duas molas da mesma máquina.

## Árvore por forma (navegação secundária)

| Tipo | Como reconhecer | Medidas que identificam |
|---|---|---|
| Compressão | Espiras afastadas; trabalha apertada | Fio, De, L0, espiras, pontas |
| Tração | Espiras encostadas, com ganchos ou olhais | Fio, De, corpo, comprimento entre ganchos, tipo de gancho |
| Torção | Corpo com duas pernas; trabalha girando | Fio, Di, espiras, pernas, ângulo, sentido |
| Torção dupla | Dois corpos enrolados em sentidos opostos unidos por um arco | As de torção + largura entre corpos |
| Dedo | Uma haste longa saindo de espiras de torção, com fixação | Arame, comprimento total, espiras, fixação |
| Garfo / dente | Dois dedos numa peça só, ou dente de ancinho/enfardadeira | Arame, comprimento, distância entre dentes, espiras, fixação |
| Haste flexível | Barra chata ou redonda curvada (tipo "S") | Seção, altura, furo |
| Cônica | Diâmetro varia ao longo do comprimento | Fio, diâmetros maior e menor, L0 |
| Prato | Arruela cônica | De, Di, espessura, altura |
| Arame conformado | Clipes, travas, grampos | Desenho |

## Código do item

Formato recomendado: **`JM-` + 2 letras de tipo + 5 dígitos sequenciais**
(ex.: `JM-CO-00123`, `JM-TO-00045`, `JM-DE-00007`, `JM-GA-00012`). Letras:
CO compressão, TR tração, TO torção, TD torção dupla, DE dedo, GA garfo, HA
haste, CN cônica, PR prato, AC arame conformado, OU outros.

- O código **não carrega medida nem máquina**: medidas mudam em revisão e a
  mesma peça serve em várias máquinas.
- Nunca reaproveitar código de item descontinuado.
- Se a empresa já usa uma numeração, mantenha a existente e registre a
  regra aqui — trocar código de item em linha confunde revenda e estoque.
- Famílias provisórias usam `JM-FAM-…` até os itens serem cadastrados.

## Descrição (padrão de escrita)

`[Tipo ou nome de uso] + [função ou máquina] + [— medida que distingue]`

| Em vez de | Escreva |
|---|---|
| Mola premium de alta resistência | Mola de compressão da linha de plantio — fio 6,0 × De 45 × 180 mm |
| Dedo original marca X | Dedo enleirador de palha — arame 8 mm, 520 mm (para uso em enleirador X modelo Y) |
| Mola Inconel para alta temperatura | Mola de torção dupla portinhola DN 200 — Inconel X-750, têmpera No. 1 |

## Aplicação e código original

- `equipamento` usa sempre o mesmo nome para a mesma máquina (lista
  controlada: copie de um registro existente antes de criar um novo).
- `marca` e `modelo` exatamente como o fabricante escreve; a busca ignora
  espaço e maiúsculas.
- `codigo_original` é o número de peça do fabricante da máquina. Só entra
  quando conferido no manual de peças ou gravado na peça — referência
  cruzada errada é devolução certa.
- Compatibilidade declarada sem conferência da peça recebe a observação
  "a confirmar" e não vai para material impresso.

## Fotos

Uma foto principal por item: fundo claro liso, peça inteira, de lado, com
escala (régua) na borda; uma segunda de detalhe da fixação ou da ponta
quando isso distingue a peça. Nome do arquivo = código do item
(`JM-DE-00007.jpg`). Sem foto de catálogo de terceiros.

## O que cada público procura

| Público | Como busca | O que precisa ver primeiro |
|---|---|---|
| Produtor e mecânico | Máquina e modelo; foto no WhatsApp | Se serve, quantas vão por máquina, se tem em estoque |
| Balconista de revenda | Código original; marca e modelo | Código Jardmolas, embalagem, equivalência |
| Comprador de montadora | Desenho e código próprio | Capacidade, material, norma |
| Engenheiro de válvulas | Tipo, liga, DN e classe | Condição do material, temperatura, documentos |
| Manutenção industrial | Medidas da peça na mão | Item mais próximo ou caminho para sob medida |

## Referências de como os bons catálogos funcionam

- Catálogos de molas de estoque oferecem busca por diâmetro externo,
  comprimento livre e constante, com busca avançada por carga, deflexão,
  espiras, altura sólida, diâmetro interno e fio, e devolvem resultados
  dentro de uma faixa de ±10% do valor pedido; mola de torção se busca pelo
  eixo em que ela trabalha; itens de estoque e sob medida aparecem
  separados.
- Catálogos de peças agrícolas listam dentes e dedos com comprimento total,
  diâmetro do arame e diâmetro interno da espira, a marca a que servem e a
  referência original.
- Guias de medição pedem fio com paquímetro, diâmetro externo medido nas
  espiras centrais, pernas medidas a partir do centro da mola, contagem de
  espiras e sentido de enrolamento.

O catálogo da Jardmolas junta as três coisas: aplicação, medidas e guia de
medição na mesma página.
