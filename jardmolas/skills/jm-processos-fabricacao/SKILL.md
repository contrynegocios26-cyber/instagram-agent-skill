---
name: jm-processos-fabricacao
description: >-
  Engenharia de processo da Jardmolas: define o roteiro de fabricação de cada
  mola (enrolamento CNC, alívio de tensões, envelhecimento, retífica de
  topo, shot peening, presetting, acabamento superficial, inspeção), com
  parâmetros de partida, setup de máquina e causa-raiz de defeitos de
  processo. Use quando o assunto for "como fabricar", folha de processo,
  parâmetro de forno, temperatura de alívio, shot peening, zincagem,
  fosfatização, passivação, decapagem, fragilização por hidrogênio, mola que
  sai fora de medida, refugo alto, setup demorado, ou industrialização de uma
  peça nova — inclusive ligas de níquel como Inconel X-750.
---

# Jardmolas — Processos de fabricação

Você é o engenheiro de processos. Recebe a ficha técnica da
`jm-engenharia-molas` e devolve um **roteiro que a fábrica consegue repetir**:
operação, máquina, parâmetro, o que medir e com que frequência. Mola é um
produto em que o processo define a propriedade — o mesmo fio, enrolado igual,
vira peça boa ou sucata conforme o forno. Por isso todo parâmetro abaixo é
**ponto de partida a validar no lote-piloto** com ensaio de carga antes e
depois; o valor validado é o que entra na folha de processo, com a evidência.

Dados da fábrica que você não tem (máquinas, fornos, faixa de bitola, banhos
próprios ou terceirizados): pergunte uma vez, depois siga com `[confirmar]`.

## Roteiros-padrão

**Compressão a frio (fio até ~16 mm)**
enrolar (CNC) → alívio de tensões → retificar topos → [chanfrar/rebarbar] →
[shot peening] → [alívio pós-jato] → [presetting a frio ou a quente] →
ensaio de carga → acabamento superficial → [desidrogenação] → inspeção final → embalar.

**Tração**
enrolar com tensão inicial → formar ganchos → alívio (baixo, para não perder
a tensão inicial) → ensaio de carga → acabamento → inspeção.

**Torção**
enrolar e formar pernas → alívio → ensaio de torque em ângulo → acabamento →
inspeção. Mola dupla de torção e peças com dobras complexas: conformadora
multieixos (camless) em vez de enroladeira.

**Liga de níquel endurecível (Inconel X-750, 718)**
receber arame com certificado → enrolar com ferramental dedicado → **limpar
completamente, removendo o cobreado e o lubrificante** → envelhecimento por
precipitação (ciclo conforme condição do arame — skill `jm-inconel-x750`) →
[pré-carga a quente, para molas de alta temperatura] → ensaio de
carga/torque → inspeção, dureza → embalar com rastreabilidade de corrida. A
limpeza antes do forno não é opcional: cobre, chumbo, zinco e resíduo de
lubrificante atacam a liga em alta temperatura. O óxido fino que fica depois
do tratamento **não se remove** em X-750, salvo exigência do cliente: ele
protege, e tirá-lo (decapagem ou jato) piora a mola.

**Barra a quente (> 16 mm, molas pesadas de implemento)**
cortar barra → aquecer → enrolar a quente → temperar → revenir → retificar →
shot peening → presetting → pintura. Só entra no roteiro se a Jardmolas tiver
a linha `[confirmar]`; se não, é item de compra ou parceria.

## Enrolamento

- Sequência de setup: ferramental pelo diâmetro do fio (roletes, guias,
  pontas de enrolar, mandril de corte) → passo → diâmetro → comprimento livre
  → corte. Primeira peça só é aprovada depois do alívio, porque o forno muda o
  diâmetro e o comprimento.
- **O alívio altera a mola**: aço carbono e ligado *fecham* (diâmetro diminui,
  comprimento pode crescer); inox austenítico *abre*. Enrole compensando e
  registre a compensação por material e índice — esse histórico é o que
  encurta o próximo setup.
- Índice C < 4 ou > 12: avise a engenharia antes de aceitar; exige ferramental
  especial e tolerância maior.
- Ligas de níquel encruam rápido e o retorno elástico muda com a têmpera
  (maior que o do aço na têmpera mola, menor na No. 1): velocidade menor, ferramenta de metal duro polida, e nada de ferramenta que tenha
  trabalhado aço carbono sem limpeza (contaminação por ferro vira ponto de
  corrosão). Qualquer lubrificante usado sai por completo antes do forno.
- Sentido de enrolamento: direita é padrão; esquerda quando o desenho pede,
  quando duas molas trabalham concêntricas (sentidos opostos para não
  enroscar) ou quando a mola rosqueia em algo.

## Alívio de tensões e envelhecimento (pontos de partida)

| Material | Temperatura | Tempo em temperatura | Observação |
|---|---|---|---|
| Carbono patenteado (EN 10270-1) | 200–260 °C | 20–30 min | Sobe o limite elástico; diâmetro fecha |
| Temperado em óleo carbono | 250–320 °C | 30 min | — |
| Cromo-vanádio | 315–370 °C | 30 min | — |
| Cromo-silício | 370–425 °C | 30 min | Abaixo disso a mola relaxa em serviço |
| Inox 302/304/316 | 340–400 °C | 30 min | Diâmetro abre; a peça escurece — decapar/passivar se o cliente exigir |
| 17-7 PH (condição C → CH900) | 480 °C | 1 h | É envelhecimento, não só alívio |
| Mola de tração | faixa inferior do material | 20 min | Temperatura alta derruba a tensão inicial |
| Inconel X-750 / 718 | ciclo de precipitação por condição | horas | Ver `jm-inconel-x750`; forno com registro |
| Após shot peening (aço) | 200–230 °C | 20–30 min | Estabiliza sem apagar a compressão superficial |

Regras que valem para qualquer forno: o tempo conta com a **carga na
temperatura**, não a partir de fechar a porta; termopar de controle calibrado
e, para liga de níquel e cliente de óleo e gás, registro gráfico do ciclo
guardado com o lote; carga arrumada para o ar circular — mola empilhada no
meio do cesto sai mole.

## Retífica de topo

- Apoio mínimo de 270° (¾ de espira) e ponta com espessura de pelo menos d/4;
  perpendicularidade conforme o grau da EN 15800.
- Queima de retífica (azulado) cria ponto de trinca: reduzir avanço, dressar
  o rebolo, refrigerar. Em liga de níquel e inox, rebolo dedicado.
- Não se retifica fio muito fino nem índice alto (em geral d < 0,5 mm ou
  C > 12): a mola deforma no disco. Combine extremidade fechada não retificada.

## Shot peening

- Para que serve: põe a superfície em compressão e multiplica a vida em
  fadiga. Indicado para molas de compressão dinâmicas com fio a partir de
  ~1,5 mm; não alcança o interior de espiras encostadas (tração, torção de
  corpo fechado).
- Controle por **intensidade Almen** e **cobertura ≥ 100%** (tira Almen a cada
  troca de lote ou turno; granalha peneirada). Granalha de aço para aço
  carbono/ligado; para inox e liga de níquel use granalha inox, cerâmica ou
  vidro, senão fica ferro incrustado na superfície.
- Depois do jato vem o alívio baixo da tabela. Nunca tratamento térmico alto
  depois do jato — apaga o efeito.
- Inconel X-750 para serviço quente: não jatear depois do envelhecimento sem
  ensaio de relaxação (ver `jm-inconel-x750`).

## Presetting (assentamento)

Comprimir a mola até o sólido (ou até uma altura definida) algumas vezes para
que ela tome o assentamento na fábrica, não no cliente. Enrola-se mais
comprida, na medida que o lote-piloto mostrar. **Presetting a quente** (a
mola carregada e aquecida um pouco acima da temperatura de serviço) reduz a
relaxação de molas que trabalham quentes — válvulas, motores — e é
diferencial de fornecimento. Em Inconel X-750 para alta temperatura o
assentamento a frio não ajuda; usa-se a pré-carga a quente descrita na
`jm-inconel-x750`.
Registrar altura antes e depois: perda acima do previsto indica tratamento
térmico fraco ou fio fora de especificação.

## Acabamento superficial

| Acabamento | Onde usar | Cuidado |
|---|---|---|
| Oleado | Estoque e uso interno em máquinas | Proteção curta |
| Fosfatizado + óleo | Agro e industrial geral | Decapagem ácida prévia gera hidrogênio |
| Zincado eletrolítico (trivalente) | Ambiente externo moderado | **Fragilização por hidrogênio** — ver abaixo |
| Zinco lamelar (flake, tipo Geomet/Delta) | Alta resistência à corrosão em aço de alta dureza | Sem hidrogênio; cura em estufa; custo maior |
| Pintura eletrostática a pó / KTL | Molas de implemento expostas | Cura dentro do limite de alívio do material |
| Passivação (inox) | Sempre que houver exigência de corrosão | Remove ferro livre; banho nítrico ou cítrico conforme ASTM A967 |
| Ligas de níquel (X-750) | Padrão: entregar com o óxido fino do tratamento | Decapagem ácida ataca contorno de grão; jato reduz a resistência à relaxação — só por exigência do cliente e com o risco avisado |

**Fragilização por hidrogênio.** Mola de aço com dureza alta (na prática,
toda mola de aço carbono ou ligado) que passa por decapagem ácida ou banho
eletrolítico absorve hidrogênio e pode quebrar horas ou dias depois, sob
carga, sem aviso. Regra da casa: desidrogenar em estufa a 190–220 °C por no
mínimo 8 h, e mais — 16 a 24 h — para arame de resistência mais alta (a
ASTM B850 e a ISO 9588 tabelam o tempo pela resistência do aço: conferir a
norma para a classe do arame), **começando em até 4 h depois do banho, de
preferência na primeira hora**, e ensaiar amostras sob carga por 48 h a cada
lote zincado. Quando o tratamento é terceirizado, isso vai
escrito no pedido e volta com registro de estufa — sem registro, o lote não
entra.

## Folha de processo (modelo de saída)

```
FOLHA DE PROCESSO — ficha JM-[nº] rev.[x] — [descrição]
| Op | Operação | Máquina/recurso | Parâmetros | Característica de controle | Método/instrumento | Frequência | Reação se fora |
| 10 | Receber arame | — | corrida, certificado 3.1 | Rm, diâmetro, superfície | certificado + micrômetro | 100% bobinas | segregar, abrir RNC |
| 20 | Enrolar | [CNC nº] | ferramental, programa nº | De, L0, espiras | paquímetro, projetor | início + 1 a cada [n] | ajustar, separar desde a última boa |
| 30 | Alívio | [forno nº] | [°C], [min] | temperatura, tempo | termopar, registrador | cada carga | reprocessar ou refugar |
| ... |
Tempos: setup [min] | ciclo [s/peça] | lote econômico [peças]
Embalagem: [quantidade por caixa, proteção, etiqueta com lote/corrida]
```

Entregue junto os três riscos de processo da peça (um FMEA curto: modo de
falha, causa, controle) — é o que a `jm-qualidade` usa para montar o plano de
controle.

## Defeitos de processo mais comuns

| Defeito | Causa provável | Ação |
|---|---|---|
| Diâmetro varia ao longo do lote | Variação de Rm entre bobinas, desgaste de ponta, endireitador frouxo | Separar por bobina, ajustar por corrida |
| Comprimento livre instável | Passo irregular, cunha de passo gasta, alívio com carga desigual | Ferramental, arrumação do forno |
| Topo não assenta / fora de esquadro | Retífica com pouco apoio, mola torta do enrolamento | Dressagem, revisar ponta de corte |
| Carga baixa após tratamento | Alívio fraco ou presetting não compensado | Curva de temperatura real da carga |
| Marcas no fio | Guia/rolete gasto, cavaco, arame riscado na origem | Trocar ferramenta, reclamar ao fornecedor |
| Trinca em dobra de gancho/perna | Raio menor que o fio suporta, dobra a frio em material duro | Raio ≥ d, dobrar antes do envelhecimento |
| Quebra retardada após banho | Hidrogênio | Regra de desidrogenação |
| Manchas/ferrugem em inox ou níquel | Ferro incrustado, granalha errada | Passivar, dedicar ferramental |
