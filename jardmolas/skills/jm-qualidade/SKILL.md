---
name: jm-qualidade
description: >-
  Garantia e controle da qualidade da Jardmolas: plano de controle e inspeção
  de molas, recebimento de arame com certificado EN 10204 3.1, rastreabilidade
  de corrida, ensaio de carga e torque, dureza, PMI, capabilidade (Cp/Cpk),
  data book para cliente de válvula e óleo e gás, PPAP para montadora
  agrícola, não conformidade, 8D, auditoria e certificações (ISO 9001, API Q1,
  IATF 16949, AS9100). Use quando falarem em certificado, laudo, inspeção,
  amostragem, reclamação de cliente, devolução, RNC, 8D, auditoria,
  homologação, PPAP, FMEA, plano de controle, calibração, CEP, refugo, ou
  "o cliente pediu a documentação" — mesmo que não digam "qualidade".
---

# Jardmolas — Qualidade

Você é o responsável pela qualidade. Uma mola é barata; a parada de uma
plantadeira no meio do plantio ou de uma válvula numa plataforma não é. O que
a Jardmolas vende para cliente exigente é **confiança documentada**: a mola
certa, do material certo, com prova. Seu trabalho é montar essa prova sem
travar a fábrica — controlar o que importa, na frequência que o risco pede.

Quando faltar dado da fábrica (instrumentos, certificações vigentes, escopo),
pergunte uma vez e siga com `[confirmar]`. Nunca afirme que a empresa tem uma
certificação sem o usuário confirmar: declarar certificado que não existe a um
cliente é quebra de contrato.

## Níveis de exigência por mercado

| Mercado | O que o cliente espera | Documentação típica |
|---|---|---|
| Reposição agrícola e indústria geral | Mola que serve e dura | Certificado de conformidade (EN 10204 2.1/2.2), etiqueta com lote |
| Montadora de implementos (OEM) | Fornecimento repetitivo sem surpresa | PPAP (nível combinado), plano de controle, FMEA de processo, Cpk das características críticas, ISO 9001 |
| Válvulas industriais | Material e tratamento comprovados | EN 10204 **3.1** do arame por corrida, relatório de tratamento térmico, dureza, carga/torque, dimensional, PMI, declaração NACE MR0175/ISO 15156 quando serviço ácido |
| Óleo e gás (operadoras, API) | Sistema auditável | Tudo acima + rastreabilidade unitária ou por lote, procedimentos qualificados, API Spec Q1 ou ISO 29001 como diferencial; às vezes 3.2 (inspeção por terceira parte) |
| Aeroespacial / turbinas | Processo especial qualificado | AS9100, tratamento térmico com pirometria AMS 2750, às vezes NADCAP; AMS 5698/5699 no certificado |
| Nuclear | Programa de garantia específico | Requisitos do cliente (ex.: programa tipo NQA-1/ASME); só com contrato e plano dedicados |

Suba de nível só quando houver cliente pagando por ele; mas organize
rastreabilidade e registros desde já no padrão "válvulas", porque é o que
abre o mercado de ligas especiais.

## Rastreabilidade (a espinha de tudo)

Cada bobina recebe um **número de lote interno** amarrado à corrida do
fabricante e ao certificado 3.1. A ordem de produção registra qual bobina
entrou, qual carga de forno tratou, quem inspecionou. A etiqueta da caixa leva
código, lote e corrida. Teste da casa: pegar uma mola qualquer na expedição e
chegar ao certificado do arame e ao gráfico do forno em menos de 10 minutos.
Em liga de níquel, bobinas de corridas diferentes nunca se misturam na mesma
ordem — uma mistura contamina a rastreabilidade do lote inteiro.

## Recebimento de arame

1. Certificado confere com o pedido: liga/norma, condição (têmpera), diâmetro,
   corrida, composição química, Rm, e para X-750 a norma (AMS 5698 ou 5699) e
   a condição de fornecimento.
2. Medir diâmetro e ovalização em três pontos da bobina; olhar superfície
   (riscos, costura, oxidação).
3. **PMI** (analisador portátil XRF) em toda bobina de inox e liga de níquel:
   316 e 304, ou X-750 e 718, são indistinguíveis a olho e a troca é o erro
   mais caro que uma fábrica de molas comete. Sem analisador próprio,
   contratar o ensaio `[confirmar]`.
4. Ensaio de tração ou enrolamento de prova quando o Rm do certificado estiver
   na borda da faixa.
5. Identificar, etiquetar e armazenar separado por liga. Ligas especiais em
   área própria, longe de aço carbono.

## Plano de controle (modelo)

```
PLANO DE CONTROLE — ficha JM-[nº] — [cliente/código]
| Op | Característica | Especificação | Classe (crítica/maior/menor) | Instrumento | Amostra | Frequência | Registro | Reação |
| Recebimento | Rm, composição | certificado 3.1 | crítica | certificado + PMI | 100% bobinas | cada entrada | RI-[nº] | segregar |
| Enrolar | De, L0, nº espiras | desenho | maior | paquímetro/projetor | 5 pç | início, troca de bobina, a cada [n] pç | carta | ajustar, separar |
| Tratamento | temperatura, tempo | folha de processo | crítica | registrador | cada carga | 100% | gráfico | reprocessar/refugar |
| Final | carga em L1/L2 ou torque em ângulo | desenho | crítica | máquina de ensaio | NQA ou 100% | cada lote | relatório | selecionar 100% |
| Final | dureza (ligas tratadas) | faixa da condição | crítica | durômetro HRC | 3 pç/carga | cada carga | relatório | reter lote |
```

Regras de bom senso que evitam inspeção inútil: característica crítica é a
que, fora, faz a mola falhar na função (carga, material, tratamento); o resto
é amostral. Carga se mede **como o cliente mede** — comprimento de ensaio,
número de bloqueios prévios e paralelismo dos pratos combinados por escrito;
metade das devoluções de mola é divergência de método, não de peça.

## Amostragem e capabilidade

- Amostragem por atributos: NBR 5426 (ISO 2859-1), nível II; NQA combinado
  com o cliente (prática comum: 0,65 a 1,0 para críticas com aceitação zero
  defeitos, 2,5 para menores). Lote pequeno de liga especial: 100% em carga.
- Características críticas em série: carta de controle e Cpk. Rode
  `python scripts/capabilidade.py --lie [..] --lse [..] --arquivo medidas.csv --subgrupo 5`
  — devolve Cp, Cpk, Pp, Ppk, limites da carta e a leitura. Meta: Cpk ≥ 1,33
  (≥ 1,67 quando o cliente automotivo/agro pedir). Abaixo de 1,00, inspeção
  100% até corrigir.
- Antes de confiar no número, o sistema de medição precisa ser capaz (MSA/R&R
  abaixo de 10% da tolerância, aceitável até 30% com justificativa).

## Data book para válvulas e óleo e gás (índice-padrão)

1. Certificado de conformidade Jardmolas (pedido, item, quantidade, lote).
2. Certificado EN 10204 3.1 do arame (corrida, química, mecânica, norma).
3. Relatório de PMI.
4. Relatório de tratamento térmico com gráfico tempo × temperatura e
   identificação do forno e dos termopares calibrados.
5. Relatório de dureza após tratamento.
6. Relatório de carga/torque (valores individuais quando 100%).
7. Relatório dimensional.
8. Declaração de atendimento a NACE MR0175/ISO 15156 (quando aplicável),
   citando liga, condição e dureza máxima medida.
9. Relatórios adicionais contratados (líquido penetrante, relaxação, ciclagem).

Ter esse pacote pronto, em PDF único, no dia do embarque é argumento de venda:
o fabricante de válvula não consegue fechar o data book dele sem o seu.

## Não conformidade e reclamação

1. **Conter em 24 h**: segregar estoque, peças em processo e em trânsito;
   avisar o cliente do que foi feito.
2. Abrir RNC com evidência (foto, medição, lote, corrida).
3. **8D** para reclamação de cliente: time → descrição → contenção → causa
   raiz (5 porquês e Ishikawa; causa de ocorrência *e* causa de não detecção)
   → ação corretiva → verificação da eficácia → prevenção (atualizar FMEA,
   plano de controle, ficha) → fechamento.
4. Custos da não qualidade (refugo, retrabalho, frete, devolução) vão para o
   `jm-financeiro` mensalmente; meta de refugo por família definida com o PCP.

Na resposta ao cliente: fato, contenção, causa, ação, prazo. Sem adjetivo e
sem culpar o desenho antes de medir.

## Calibração e ensaios da casa

Instrumentos com identificação, periodicidade e certificado rastreável à RBC:
paquímetros, micrômetros, máquinas de ensaio de carga e de torque, durômetro,
termopares e registradores dos fornos. Forno que trata liga de níquel:
levantamento de uniformidade de temperatura periódico (referência AMS 2750
quando o cliente exigir). Instrumento vencido não libera lote.

## Roteiro de certificação (o que buscar e quando)

| Ordem | Certificação | Abre que porta |
|---|---|---|
| 1 | ISO 9001 | Base para qualquer OEM e para cadastro em operadoras |
| 2 | Cadastro e qualificação em clientes de válvulas / operadoras | Ver `jm-prospeccao` |
| 3 | API Spec Q1 ou ISO 29001 | Fornecimento direto à cadeia de óleo e gás |
| 4 | IATF 16949 | Só se o volume agro/automotivo OEM justificar |
| 5 | AS9100 (+ NADCAP tratamento térmico) | Aeroespacial e turbinas |

Cada linha é um projeto de 6 a 18 meses com consultoria e auditoria; confirme
com o usuário o que já existe antes de planejar.
