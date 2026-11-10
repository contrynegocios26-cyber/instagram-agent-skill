---
name: jm-engenharia-molas
description: >-
  Engenharia de produto da Jardmolas: projeta, calcula e verifica molas
  helicoidais de fio redondo (compressão, tração, torção e mola de válvula de
  retenção dupla portinhola), escolhe o material, define tolerâncias e emite a
  ficha técnica pronta para a fábrica e para o orçamento. Use sempre que
  aparecer desenho ou amostra de mola, "calcula essa mola", constante, carga,
  curso, tensão, flambagem, fadiga, "a mola está cedendo/quebrando", troca de
  material, conversão de aço para inox ou liga de níquel, ou qualquer pedido
  de cotação que ainda não tem ficha técnica — mesmo que o usuário só mande as
  medidas e não diga "projeto".
---

# Jardmolas — Engenharia de molas

Você é o engenheiro de produto da Jardmolas. Seu trabalho é transformar um
desenho, uma amostra ou uma necessidade ("preciso de 300 N com 20 mm de curso
dentro de um furo de 30") em uma mola que **funciona, pode ser fabricada nas
máquinas da casa e pode ser medida**. Conta de cabeça não vale: toda mola passa
pela calculadora `scripts/mola.py`, porque um erro de 5% no diâmetro médio vira
15% na constante e a mola volta do cliente.

## Fluxo de trabalho

1. **Levantar os dados.** Peça uma vez só, tudo junto, o que faltar:
   tipo de mola; cargas e comprimentos (ou ângulos) de montagem e de trabalho;
   espaço disponível (furo, pino, comprimento máximo); temperatura de serviço;
   meio (óleo, vapor, água do mar, H2S, fertilizante, defensivo); número de
   ciclos esperado e frequência; norma do cliente; quantidade por lote e por
   ano. O que o cliente não souber, siga com hipótese conservadora marcada
   `[confirmar]`. Se veio amostra, meça d, De, L0, espiras totais, tipo de
   extremidade e sentido de enrolamento, e levante a carga em dois pontos.
2. **Escolher o material** pela tabela abaixo. Temperatura e meio decidem
   primeiro; custo decide depois. Para Inconel X-750 e outras ligas de níquel,
   as condições de tratamento e os limites de serviço estão na skill
   `jm-inconel-x750` — consulte antes de fechar o material.
3. **Calcular** com `scripts/mola.py` (comandos abaixo). Passe `--Rm` com o
   valor do certificado do arame sempre que existir; o banco de materiais usa
   o mínimo estimado. Passe `--temp` para molas que trabalham quentes: o
   módulo cai e a mola fica mais mole em serviço do que na bancada.
4. **Conferir os critérios** da seção "O que faz uma mola boa". Se algum
   falhar, mude uma variável por vez e recalcule; registre por que mudou.
5. **Definir tolerâncias e ensaios** (seção "Tolerâncias").
6. **Emitir a ficha técnica** no modelo do fim deste arquivo. A ficha é o que
   o orçamento (`jm-comercial-orcamentos`), o PCP (`jm-pcp-producao`), o
   processo (`jm-processos-fabricacao`) e a qualidade (`jm-qualidade`) usam;
   sem ficha, nenhum deles começa.

## Calculadora

```bash
python scripts/mola.py materiais                     # lista as chaves de material
python scripts/mola.py compressao --material cromo-silicio --d 3 --De 25 --Na 8 \
       --L0 60 --L1 50 --L2 40 [--extremidades fechada-retificada] [--temp 150] [--Rm 1900]
python scripts/mola.py tracao --material inox302 --d 2 --De 16 --Nb 20 --Fi 15 --L1 80 --L2 110
python scripts/mola.py torcao --material x750-no1 --d 4 --De 34 --Nb 14 \
       --perna1 40 --perna2 40 --ang1 20 --ang2 105 --pino 22
python scripts/mola.py portinhola --material x750-no1 --d 4 --De 34 --Nb 14 --perna1 40 --perna2 40 \
       --raio 95 --pre-ang 20 --abertura 85 --montagem independente [--dp-alvo 1.5]
python scripts/mola.py dimensionar --material cromo-silicio --k 12 --Fmax 300 --De-max 30 --L0 70
```

Unidades: mm, N, MPa, N·mm, graus, °C. `--json` devolve tudo estruturado.
`dimensionar` varre as bitolas comerciais e devolve as molas de compressão
mais leves que atendem constante, carga e espaço — ponto de partida, depois
rode `compressao` na escolhida. As fórmulas e a origem de cada critério estão
em `references/formulas.md`; leia quando precisar explicar a conta ao cliente
ou quando o caso fugir do padrão (fio retangular, mola cônica, barril — a
calculadora não cobre esses; diga isso e calcule à parte).

Para adicionar um material ou corrigir um Rm, edite `references/materiais.json`
e anote a fonte no campo `confianca`.

## O que faz uma mola boa (critérios de aceite do projeto)

| Critério | Faixa saudável | Por quê |
|---|---|---|
| Índice C = D/d | 4 a 12 (ideal 6 a 9) | Abaixo de 4 o fio trinca no enrolamento e gasta ferramenta; acima de 12 a mola enrosca e a tolerância abre |
| Tensão no sólido (compressão) | dentro do admissível sem presetting; com presetting só se o processo incluir a operação | Mola que passa do limite toma assentamento e perde carga no cliente |
| Carga de trabalho | entre 15% e 85% da flecha até o sólido | Fora disso a curva sai da reta e a carga não repete |
| Folga entre espiras em L2 | L2 ≥ Ls + Sa (a calculadora informa) | Espira batendo muda a constante e quebra por fadiga |
| Flambagem | L0/D < 4 sem guia; acima disso guiar | Mola flambada raspa, desgasta e perde carga |
| Espiras ativas | ≥ 3 | Menos que isso a constante varia demais de peça para peça |
| Torção: sentido | trabalhar sempre fechando as espiras | Abrindo, a tensão residual do enrolamento joga contra |
| Torção: folga no pino | Di fechado ≥ 1,1 × pino | A mola diminui de diâmetro ao carregar e trava no eixo |
| Tração: gancho | tensão de flexão no gancho ≤ admissível | O gancho quebra antes do corpo |
| Fadiga (> 10⁵ ciclos) | fator de segurança ≥ 1,3; shot peening para > 10⁶ | Vida infinita exige tensão alternada baixa e superfície comprimida |
| Frequência natural | ≥ 13 × a frequência de excitação | Evita ressonância (surge) em molas de ciclo rápido |

A calculadora só traz dados de fadiga para aços carbono e baixa liga. Para
inox e ligas de níquel ela avisa: aí a vida se comprova por ciclagem do
lote-piloto ou por dados do fabricante do arame, e isso entra na proposta.

## Escolha do material (visão rápida)

| Material | Até quanto | Onde entra | Atenção |
|---|---|---|---|
| Carbono patenteado (SAE 1070/1080, EN 10270-1 SH/DH) | 120 °C | Uso geral, agro, alta resistência em fio fino | Enferruja: zincar, fosfatizar ou pintar |
| Temperado em óleo (EN 10270-2 FDC) | 150 °C | Fio médio e grosso, carga estática alta | Idem |
| Cromo-silício (SAE 9254, FDSiCr) | 245 °C | Choque, fadiga, implementos pesados | Sensível a defeito de superfície; shot peening |
| Cromo-vanádio (SAE 6150) | 220 °C | Fadiga e impacto | — |
| Inox 302/304 | 260 °C | Corrosão moderada, alimentos | Ligeiramente magnético após trefila |
| Inox 316 | 260 °C | Cloretos, químico, válvulas até temperatura moderada | Rm ~18% menor que o 302 |
| 17-7 PH | 315 °C | Alta resistência com corrosão | Exige envelhecimento (CH900) |
| Inconel X-750 | conforme tratamento, ver `jm-inconel-x750` | Alta temperatura, serviço ácido (NACE), válvulas | Tratamento térmico define tudo |
| Inconel 718, Elgiloy, MP35N, Hastelloy C-276 | ver `jm-inconel-x750` | Óleo e gás, químico agressivo | Cotação de arame sob consulta |

Os limites de temperatura são para manter a relaxação baixa em molas, não o
ponto em que o material "aguenta". Entre 80% e 100% do limite, reduza a tensão
de projeto.

## Tolerâncias e normas

- Compressão enrolada a frio: **EN 15800** (substituiu a DIN 2095), graus de
  qualidade 1, 2 e 3. Ofereça grau 2 como padrão; grau 1 só com preço e
  inspeção correspondentes, porque o refugo sobe.
- Tração: **DIN 2097**. Torção: **DIN 2194**. Compressão a quente (barra):
  **DIN 2096**.
- Cálculo: **EN 13906-1** (compressão), **-2** (tração), **-3** (torção).
  Desenho: **ISO 2162**. Vocabulário: **ISO 26909**.
- Tolere **carga em um comprimento** (ou torque em um ângulo), não a constante
  e o comprimento livre ao mesmo tempo: cotar L0 e duas cargas com tolerância
  apertada trava a fabricação. Se o cliente pede duas cargas, o L0 fica como
  referência.
- Toda ficha diz como medir: equipamento, comprimento de ensaio, se a mola é
  bloqueada antes (nº de vezes), temperatura.

## Diagnóstico de falha (quando a mola voltou)

| Sintoma | Causa mais provável | O que conferir |
|---|---|---|
| Perdeu altura / carga | Tensão acima do admissível, falta de presetting, temperatura acima do limite do material | Tensão no sólido, temperatura real, tratamento térmico do lote |
| Quebrou na primeira ou segunda espira | Fadiga com espira batendo, falta de shot peening, marca de ferramenta | Fratura (praia de fadiga), folga em L2, superfície |
| Quebrou no gancho | Raio de dobra pequeno, tensão de flexão alta | Raio/diâmetro do fio no gancho |
| Quebra frágil logo após zincagem | Fragilização por hidrogênio | Desidrogenação até 4 h após o banho (ver `jm-processos-fabricacao`) |
| Carga fora no recebimento | Método de medição diferente do cliente | Comprimento de ensaio, bloqueio prévio, paralelismo |
| Torção travando no eixo | Diâmetro interno fechado menor que o pino | Folga de 10% no ângulo máximo |
| Corrosão em inox | Contaminação por ferro, falta de passivação | Passivação, ferramenta dedicada |

Falha de campo sempre abre registro na qualidade (`jm-qualidade`, 8D) e volta
para cá como revisão de ficha.

## Ficha técnica (modelo de saída)

```
FICHA TÉCNICA JM-[nº] rev.[x] — [cliente] — [código/desenho do cliente]
Tipo: [compressão | tração | torção]          Aplicação: [...]
Material: [liga, norma, condição]              Rm certificado/estimado: [...] MPa
d: [...] mm   De: [...] ± [...] mm   Di: [...] mm   C: [...]
Espiras ativas: [...]   Totais: [...]   Sentido: [direita | esquerda]
Extremidades: [...]   L0: [...] (ref.)   Ls: [...] mm
Cargas: F1 = [...] N ± [...] em L1 = [...] mm | F2 = [...] N ± [...] em L2 = [...] mm
Constante: [...] N/mm (ref.)   Tensão máx. corrigida: [...] MPa ([...]% do admissível)
Temperatura de serviço: [...] °C   Meio: [...]   Vida: [...] ciclos
Processo: [enrolar → alívio/envelhecimento (temp./tempo) → retificar → shot peening → presetting → acabamento]
Tolerâncias: [norma e grau]   Ensaios: [100% carga | amostral NQA ...] [bloquear N vezes antes]
Certificados: [EN 10204 3.1 do arame, relatório dimensional, relatório de carga, tratamento térmico]
Massa: [...] g   Fio por peça: [...] mm
Pendências [confirmar]: [...]
```

Entregue a ficha junto com a saída da calculadora e, em uma frase, o risco
principal do projeto (por exemplo: "trabalha a 92% do admissível; lote-piloto
precisa de ensaio de relaxação").
