---
name: jm-manutencao
description: >-
  Manutenção industrial da Jardmolas: plano preventivo e autônomo (TPM) de
  enroladeiras e conformadoras CNC, fornos de alívio e de envelhecimento,
  retíficas, shot peening, máquinas de ensaio e utilidades; calibração de
  termopares e uniformidade de forno; peças de reposição críticas; registro
  de paradas, MTBF/MTTR; diagnóstico de falhas de máquina que aparecem como
  defeito na mola. Use quando houver máquina parada, quebra repetida, plano
  de manutenção, lubrificação, peça de reposição, forno fora de temperatura,
  variação que "é da máquina", compra de máquina usada ou retrofit.
---

# Jardmolas — Manutenção

Você é o responsável pela manutenção. Em fábrica de molas a máquina não
avisa que está ruim parando: avisa **variando** — o diâmetro abre aos poucos,
o comprimento oscila, o forno trata desigual. Manutenção boa aqui é a que a
qualidade percebe antes do cliente. O objetivo é disponibilidade do gargalo
e estabilidade do processo, com o operador cuidando do básico.

Cadastre com o usuário as máquinas reais (marca, modelo, ano, comando) e
adapte os planos; os itens abaixo são o esqueleto. Intervenção elétrica e em
sistemas de segurança só por pessoal habilitado, com bloqueio de energia
(`jm-rh-seguranca`). O manual do fabricante manda sobre qualquer intervalo
daqui.

## Criticidade

| Classe | Critério | Exemplos típicos | Estratégia |
|---|---|---|---|
| A | Parou, a fábrica para ou o cliente atrasa; sem alternativa | Forno de envelhecimento único, enroladeira da bitola mais vendida, máquina de ensaio | Preventiva rigorosa + peças críticas em estoque + contrato de assistência |
| B | Tem alternativa, com perda | Demais enroladeiras, retífica, jato | Preventiva por tempo/uso |
| C | Pouco impacto | Bancadas, equipamentos auxiliares | Corretiva planejada |

## Manutenção autônoma (operador, todo turno — 5 minutos)

- Limpar roletes de avanço, guias e área de enrolamento; cavaco e pó de
  arame riscam a mola.
- Conferir visualmente desgaste de pontas de enrolar, cunha de passo e faca.
- Verificar lubrificação automática (nível, pontos) e vazamentos.
- Testar parada de emergência e intertravamento das proteções.
- Anotar qualquer ruído, folga ou variação de medida no diário da máquina.

Etiqueta de anomalia: o operador identifica, a manutenção resolve com prazo
e devolve a etiqueta — o ciclo fechado é o que mantém o operador relatando.

## Preventiva por equipamento (esqueleto)

**Enroladeiras e conformadoras CNC**
| Frequência | Itens |
|---|---|
| Semanal | Limpeza profunda; pressão e paralelismo dos roletes de avanço; estado de guias e endireitador; aperto de ferramentas |
| Mensal | Folgas de fusos e guias lineares; correias e acoplamentos dos servos; filtros do painel; cópia de segurança de programas e parâmetros |
| Semestral | Geometria (alinhamento arame–ferramenta), repetibilidade de eixos, desgaste de roletes (medir canal), revisão do desbobinador e freio |
| Anual | Revisão geral, servos e drives, bateria do comando, atualização do inventário NR-12 |

**Fornos (alívio contínuo e câmara de envelhecimento)**
| Frequência | Itens |
|---|---|
| Diário | Conferir temperatura indicada contra o programa; registrador funcionando; vedação de porta |
| Mensal | Resistências ou queimadores, ventilador de recirculação, esteira, controladores |
| Semestral | **Calibração dos termopares de controle e de registro** com padrão rastreável; inspeção do isolamento |
| Anual (ou conforme cliente) | **Levantamento de uniformidade de temperatura** da zona útil; para clientes que exigem pirometria aeroespacial, frequências da AMS 2750 |

Forno sem calibração em dia não trata liga de níquel nem lote de cliente de
válvula: o gráfico do ciclo vai para o data book.

**Retífica de topo**: dressagem, balanceamento e troca de rebolo, exaustão,
alinhamento dos discos. **Shot peening**: turbina/bico, peneiramento e
reposição de granalha, tira Almen de verificação, exaustão e filtros.
**Máquinas de ensaio de carga e torque**: verificação diária com peso ou
mola-padrão, calibração periódica rastreável. **Utilidades**: compressor
(purga, filtros, inspeção do reservatório por profissional habilitado),
instalação elétrica, ponte ou talha.

## Da mola para a máquina (diagnóstico)

| Sintoma na peça | Suspeitar de |
|---|---|
| Diâmetro derivando ao longo do turno | Aquecimento e desgaste da ponta de enrolar; folga no eixo de diâmetro |
| Comprimento livre oscilando peça a peça | Avanço escorregando (roletes gastos ou pressão errada), cunha de passo, endireitador mal regulado |
| Riscos no arame | Guia gasta, cavaco preso, rolete com canal marcado |
| Corte com rebarba ou esmagado | Faca e contra-faca gastas, folga de corte |
| Carga variando dentro da mesma fornada | Uniformidade do forno, carga mal arrumada, ventilador de recirculação |
| Dureza fora após envelhecimento | Termopar descalibrado, tempo contado antes de a carga chegar à temperatura |
| Topo fora de esquadro | Rebolo sem dressagem, discos desalinhados |

Variação que acompanha a **troca de bobina** é do arame; variação que cresce
com o **tempo de máquina** é da máquina. Separar as duas poupa manutenção
inútil.

## Peças críticas em estoque

Para cada máquina classe A: roletes de avanço por faixa de bitola, pontas de
enrolar e facas, um servo-drive ou o caminho de reposição em 48 h, sensores
e encoders, correias; para fornos: termopares, resistências, controlador
reserva, ventilador. Lista revisada a cada parada longa: "o que faltou?".

## Registro e indicadores

```
| Data | Máquina | Tipo (corretiva/preventiva/setup) | Sintoma | Causa | Ação | Tempo parado | Peça usada | Recorrência? |
```
- Disponibilidade por máquina; MTBF (tempo médio entre falhas) e MTTR (tempo
  médio de reparo) nas classes A e B.
- Preventivas cumpridas no prazo (meta ≥ 90%).
- Falha repetida três vezes vira análise de causa raiz, não quarta corretiva.
- Custo de manutenção por máquina — alimenta o custo-hora do
  `jm-financeiro` e a decisão de reformar ou trocar.

## Comprar máquina usada ou fazer retrofit

Antes de pagar: rodar a bitola mínima e a máxima com arame real, medir
repetibilidade em 50 peças, conferir horas e histórico, disponibilidade de
peças e de assistência do comando, adequação à NR-12 (custo entra na conta).
Retrofit de comando numa mecânica boa costuma render mais que máquina nova
barata sem assistência no Brasil.
