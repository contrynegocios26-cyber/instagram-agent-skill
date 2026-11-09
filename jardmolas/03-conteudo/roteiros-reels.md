# Roteiros de Reels Jardmolas (15)

Data: 09/11/2026. Base: skills/ig-reel/SKILL.md e hooks.json, skills/ig-caption/SKILL.md, skills/ig-human/SKILL.md, e as lições da auditoria da MP Marcenaria.

Todos foram pensados para gravar com celular, na fábrica em Jardinópolis-SP e no campo, por gente da própria Jardmolas. As regras de segurança e de câmera estão em `guia-de-gravacao.md` e valem para todos.

## Como as ferramentas foram usadas (e onde não funcionaram)

As ferramentas Python do repositório foram feitas para inglês. Testei cada uma numa amostra em português antes de usar:

| Ferramenta | Funciona em português? | Como foi usada aqui |
| --- | --- | --- |
| `hookscore.py` (nota do gancho) | **Não, do jeito que está.** As listas de tensão, de abertura fraca, de imperativo e de "você" são em inglês, e a regex corta palavra com acento. No teste, "Bom dia pessoal, hoje vou mostrar a nossa fábrica" tirou a mesma nota (30,0) que ganchos bons. | Apliquei as 5 regras do hookscore (tamanho de 5 a 12 palavras, algo concreto, algo em jogo, o principal no começo, falar com "você") com uma cópia temporária do script, fora do repositório, com as listas trocadas por palavras em português. O cálculo é o mesmo do original. Com ela, a saudação cai para 0 e os ganchos com número e "você" sobem, igual ao original em inglês. **As notas abaixo vêm dessa cópia e servem para comparar os 3 ganchos de cada Reel, não para prever visualização.** Onde o gancho tem um número entre colchetes, a nota supõe que o número real vai entrar ali. |
| `beats.py` (tempo da fala) | **Sim, para tempo.** Conta palavras e soma segundos. O acento quebra palavras e infla a conta em uns 8%, então rodei numa cópia sem acento, a 160 palavras por minuto. A checagem de "loop" pega palavra pequena do português ("de", "a"), então conferi o loop na mão. | Todas as falas abaixo passaram sem alerta de gancho acima de 3 s e sem frase acima de 4 s. O alerta "trecho sem número" ficou em alguns Reels de propósito: ali o número aparece na tela (visor do paquímetro, da máquina de teste). |
| `caption.py` (legenda) | **Em parte.** A janela de 125 caracteres, o limite de 2.200, a contagem de hashtags (máximo 5), links e emoji funcionam. Não reconhece CTA em português ("Comenta MOLA" deu "nenhuma CTA") e corta hashtag com acento (#manutenção vira #manuten). | Rodei todas as legendas. Hashtag sempre sem acento. A CTA única foi conferida na mão. |
| `humanize.py` | **Só a parte de tipografia.** Tira travessão, aspas curvas e reticências direito. A troca de palavras estraga o português: "É crucial" virou "É important". | Usei só para conferir tipografia. Os clichês proibidos foram checados com uma busca própria em português. |
| `detect.py` | **Em parte.** Variação do tamanho das frases e impressão tipográfica funcionam; as checagens de vocabulário e de "voz" são em inglês e não valem aqui. | Não usei a nota final dele. |

## Regras que valem para os 15

- **Quadro 1 com movimento e texto na tela.** Arame andando, mão pegando a mola, rotor girando. Nada de logo, nada de "bom dia".
- **Texto na tela com até 6 palavras por cartaz**, no meio da tela: nada acima de 230 px nem abaixo de 1440 px num quadro de 1080x1920, e os 230 px da direita livres (é onde ficam os botões). O gancho nunca embaixo, onde a legenda cobre.
- **Legenda queimada na fala.** A maioria assiste sem som primeiro.
- **Som do lugar.** Máquina, palha, trator. Música só se for baixinha, por baixo.
- **Uma CTA por Reel.**
- **Capa escolhida**, com até 4 palavras no centro.
- **Nenhum número inventado.** Onde está [N], entra o número real medido na hora da gravação. Se o número não aparecer de verdade, a frase sai.

**Palavras-chave das CTAs** (o fluxo de cada uma está em `stories-e-whatsapp.md`):

| Palavra | O que a pessoa recebe no direct |
| --- | --- |
| MOLA | O link do WhatsApp com mensagem pronta e as 3 fotos que fazem o orçamento sair |
| MEDIDA | O link do Identificador de Molas e o guia das medidas (compressão e tração) |
| DEDO | O checklist de entressafra do enleirador |
| CADERNO | Como funciona o Caderno de Molas da Usina e o link para agendar |

## Ordem sugerida de gravação

1. **Dia de fábrica 1 (12 ou 13/11):** R01, R02, R11, R12 e R13. Tudo na fábrica, sem cliente.
2. **Campo (17 a 19/11, antes de acabar a safra):** R07, R09, R10 e R08 se tiver enfardadeira perto. Precisa de fazenda de cliente que autorize [confirmar com a Jardmolas].
3. **Dia de fábrica 2 (24/11):** R03, R04, R05, R06 e R15.
4. **Primeira visita do Caderno (dezembro):** R14.

---

## R01: Do arame à mola em 15 segundos, ep. 1: mola de compressão

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Do arame à mola em 15 segundos | 1. A máquina trabalhando | Todos (é o primeiro contato) | 15 s | Fábrica, máquina de enrolar mola de compressão | Filmador da fábrica; operador trabalha normalmente, sem falar |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #18 Cold Open Demo | "Olha o que essa máquina faz com um rolo de arame Belgo." | OLHA ESSA MÁQUINA | 45,8 |
| 2 | #5 Time Collapse | "Em 15 segundos, do rolo de arame à mola da sua máquina." | ARAME À MOLA EM 15 s | 55,4 |
| 3 | #3 Nobody Tells You | "Você nunca viu como nasce a mola da sua máquina. São 15 segundos." | COMO NASCE A SUA MOLA | **81,6** |

**Escolhido: 3.** Fala com quem compra ("a mola da sua máquina"), promete uma coisa curta e entrega no próprio vídeo. A opção 2 parece dizer que a máquina faz a mola em 15 segundos, e isso a gente não sabe; os 15 segundos são do vídeo. A opção 1 não fala com ninguém.

**Fala:** nenhuma. Só o som da máquina. A linha do gancho vai no cartaz.

**Texto na tela**

```
0:00  COMO NASCE A SUA MOLA
0:02  ARAME BELGO
0:05  SOB MEDIDA OU REPOSIÇÃO
0:07  MEDIDA CONFERIDA
0:10  LAUDO POR LOTE
0:13  COMO NASCE A SUA MOLA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Arame entrando no alimentador da máquina | Lateral, close, celular preso num suporte fora da proteção | 2 |
| 2 | 0:02 | A ponta da máquina formando as espiras | De frente, através da proteção transparente ou pela janela de inspeção. Nunca abrir a proteção para filmar | 3 |
| 3 | 0:05 | Mola cortada caindo na bandeja | De cima, câmera parada | 2 |
| 4 | 0:07 | Mão do operador, com o EPI do posto, medindo a mola com paquímetro na bancada, longe da máquina | Close, de lado | 3 |
| 5 | 0:10 | Caixa do lote com a etiqueta, ou o laudo sendo separado | Plano médio | 3 |
| 6 | 0:13 | Arame entrando de novo, mesmo enquadramento do plano 1 | Lateral, close | 2 |

Se a mola passar por outra etapa antes de ficar pronta (forno de alívio de tensão, retífica das pontas, pintura) [confirmar com a Jardmolas], trocar o plano 3 por ela.

**Áudio:** som da máquina gravado no local. Sem música ou com música bem baixa por baixo.

**Capa:** COMO NASCE A SUA MOLA

**Legenda**

```legenda
Comenta MOLA que a gente te manda no direct o caminho pra cotar a sua, de reposição ou sob medida.

Isso é a fábrica da Jardmolas em Jardinópolis-SP, região de Ribeirão Preto. Arame Belgo entrando na máquina, mola saindo pronta e laudo por lote.

São 17 anos fazendo molas agrícolas e industriais, mais de 2.000 modelos: dedo de enleirador de palha de cana, mola de enfardadeira de feno, recolhedor de amendoim, mola de compressão, tração e torção para implemento e mola de válvula de usina.

#fabricademolas #molasagricolas #jardinopolis #ribeiraopreto
```

**CTA:** comentar MOLA.

**Confirmar com a Jardmolas:** etapas do processo depois de enrolar; se a medida é conferida na bancada em todo lote (se não, tirar o cartaz MEDIDA CONFERIDA).

---

## R02: Do arame à mola em 15 segundos, ep. 2: dedo de enleirador

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Do arame à mola em 15 segundos | 1. A máquina trabalhando | Agricultor e operador de enleirador de palha | 15 s | Fábrica, onde o dedo é feito | Filmador da fábrica |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #16 The Verbatim Question | "Vocês fazem dedo de enleirador de palha?" Olha aqui. | FAZ DEDO DE PALHA? | 50,0 |
| 2 | #24 The Reveal | "Esse é o dedo que puxa a palha de cana no seu enleirador." | O DEDO DO SEU ENLEIRADOR | 36,5 |
| 3 | #3 Nobody Tells You | "Você já trocou esse dedo. Nunca viu ele nascer." | VOCÊ NUNCA VIU ELE NASCER | **87,0** |

**Escolhido: 3.** O operador troca esse dedo e nunca viu de onde ele vem. Mantém o mesmo jeito do episódio 1, o que faz a série ser reconhecida. A opção 1 só vale se for pergunta que chega de verdade no WhatsApp [confirmar], com as palavras do cliente.

**Fala:** nenhuma. Som da máquina.

**Texto na tela**

```
0:00  VOCÊ NUNCA VIU ELE NASCER
0:02  ARAME BELGO
0:05  A PERNA NA MEDIDA
0:08  CONFERIDO NO GABARITO
0:11  PRA PALHA DE CANA
0:13  VOCÊ NUNCA VIU ELE NASCER
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Arame reto entrando na máquina de dedo | Lateral, close, celular no suporte | 2 |
| 2 | 0:02 | As espiras do dedo se formando | Close, através da proteção | 3 |
| 3 | 0:05 | A dobra das pernas | Close de cima | 3 |
| 4 | 0:08 | Dedo pronto encostado no gabarito de conferência | Close, mão entrando no quadro | 3 |
| 5 | 0:11 | Caixa ou pilha de dedos prontos | De cima, câmera descendo devagar | 2 |
| 6 | 0:13 | Arame reto entrando de novo | Igual ao plano 1 | 2 |

**Áudio:** som da máquina.

**Capa:** VOCÊ NUNCA VIU ELE NASCER

**Legenda**

```legenda
Manda esse vídeo pro operador do enleirador de palha. Ele já trocou esse dedo e nunca viu ele nascer.

Dedo enleirador e desenleirador de palha de cana feito aqui em Jardinópolis-SP, com arame Belgo e laudo por lote. Do arame reto ao dedo pronto pro rotor.

Se você trabalha com recolhimento de palha na região de Ribeirão Preto, a Jardmolas tem estoque estratégico de dedos e faz sob medida pra máquina que não tem mais peça.

#enleirador #palhadecana #dedoenleirador #jardinopolis
```

**CTA:** mandar para o operador (compartilhamento).

**Confirmar com a Jardmolas:** como o dedo é feito (máquina automática ou dobra manual); se existe gabarito de conferência (se não, trocar o plano 4 pelo paquímetro); quais modelos de dedo ficam no estoque estratégico.

---

## R03: Quanto peso essa mola aguenta, ep. 1: compressão no teste de carga

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Quanto peso essa mola aguenta | 5. A prova | Todos; é o candidato a post fixado de prova | cerca de 20 s (16,5 s de fala e 3 s de máquina) | Fábrica, equipamento de teste de carga | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #16 The Verbatim Question | "Quanto peso essa mola aguenta? Chuta antes de eu apertar." | QUANTO ELA AGUENTA? | **77,8** |
| 2 | #18 Cold Open Demo | "Olha o número que aparece no visor quando a mola fecha." | OLHA O VISOR | 36,6 |
| 3 | #10 If This, Then Watch | "Se você compra mola pelo olho, olha esse visor." | COMPRA MOLA PELO OLHO? | 37,8 |

**Escolhido: 1.** É o nome da série, puxa comentário (o chute) e o visor entrega a resposta. A opção 3 pode soar como cutucada no cliente.

**Fala** (técnico; 44 palavras, cerca de 16,5 s a 160 ppm no beats.py)

```
Quanto peso essa mola aguenta?
Chuta nos comentários antes de eu apertar.
É mola de compressão, arame Belgo de [N] mm.
Agora aperta.
[N] quilos pra chegar na altura de trabalho.
Esse número vai pro laudo do lote.
E aí, quanto peso você chutou?
```

**Texto na tela**

```
0:00  QUANTO ELA AGUENTA?
0:02  CHUTA AÍ
0:04  ARAME BELGO [N] mm
0:10  [N] kg
0:13  VAI PRO LAUDO
0:16  QUANTO VOCÊ CHUTOU?
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Mão do técnico colocando a mola na máquina de teste e saindo | Close lateral | 2 |
| 2 | 0:02 | Rosto do técnico falando "Chuta nos comentários" | Peito para cima, celular na altura do olho | 2 |
| 3 | 0:04 | Paquímetro no arame da mola, visor legível | Close | 3 |
| 4 | 0:07 | Máquina comprimindo a mola | Close lateral, câmera parada fora da área de risco | 3 |
| 5 | 0:10 | Visor da máquina com o número | Close, sem reflexo | 3 |
| 6 | 0:13 | Laudo do lote com o número anotado, dedo apontando | De cima | 3 |
| 7 | 0:16 | Técnico: "E aí, quanto peso você chutou?" | Rosto | 3 |

Se o visor mostrar em newton, colocar na tela também em quilos (newton dividido por 9,8).

**Áudio:** fala do técnico com o som da máquina por baixo.

**Capa:** QUANTO ELA AGUENTA?

**Legenda**

```legenda
Chuta aqui embaixo: quantos quilos essa mola de compressão aguenta até a altura de trabalho? A resposta tá no fim do vídeo.

O teste é feito aqui na fábrica em Jardinópolis-SP e o resultado vai pro laudo do lote. É assim que a mola sai daqui com a carga que o seu implemento ou a sua válvula pede.

Arame Belgo. Molas de compressão, tração e torção, de reposição ou sob medida.

#moladecompressao #fabricademolas #molasagricolas #ribeiraopreto
```

**CTA:** comentar o chute.

**Confirmar com a Jardmolas:** que equipamento de teste de carga eles têm e em que unidade mostra; se o teste é feito em todo lote; o que o laudo traz; a medida real da mola filmada.

---

## R04: Quanto peso essa mola aguenta, ep. 2: dedo novo contra dedo de uma safra

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Quanto peso essa mola aguenta | 5. A prova | Agricultor e operador de enleirador | cerca de 24 s (22 s de fala) | Fábrica, bancada | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #17 Head To Head | "Dedo novo contra dedo de uma safra inteira. Mesma medida." | NOVO x 1 SAFRA | **59,6** |
| 2 | #13 Before And After | "Esse dedo saiu daqui assim. Voltou da safra assim." | SAIU / VOLTOU | 39,2 |
| 3 | #3 Nobody Tells You | "Ninguém te fala que o dedo cansa antes de quebrar." | O DEDO CANSA ANTES | 55,8 |

**Escolhido: 1.** A comparação é o vídeo inteiro e o resultado aparece no visor, não é afirmação nossa. A opção 3 é boa como frase do meio, e entrou na fala ("ele não quebrou, ele cansou").

**Regra deste Reel:** só publica se a diferença aparecer de verdade no teste. Se der igual, o vídeo muda para "Dedo de uma safra ainda segura [N] kg" e a mensagem vira "confere o jogo, nem sempre precisa trocar". Os dois são úteis; inventar não é.

**Fala** (técnico; 59 palavras, cerca de 22 s)

```
Dedo novo contra dedo de uma safra inteira.
Mesma medida. Mesmo puxão na ponta.
O novo marcou [N] quilos.
O que trabalhou a safra marcou [N].
Ele não quebrou. Ele cansou.
Dedo cansado trabalha menos e você nem vê.
Na entressafra, confere o jogo inteiro, não só o quebrado.
Comenta DEDO que eu te mando o checklist do enleirador.
```

**Texto na tela**

```
0:00  NOVO x 1 SAFRA
0:05  NOVO: [N] kg
0:07  1 SAFRA: [N] kg
0:10  NÃO QUEBROU. CANSOU.
0:15  CONFERE O JOGO INTEIRO
0:18  COMENTA DEDO
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Os dois dedos lado a lado na bancada, mão pegando um em cada | De cima | 3 |
| 2 | 0:03 | Close das pernas dos dois, para ver a diferença de abertura (se houver) | Close de lado | 2 |
| 3 | 0:05 | Dedo novo preso na morsa, dinamômetro de gancho puxando a ponta até a marca de [N] cm numa régua | Lateral, visor do dinamômetro legível | 2 |
| 4 | 0:07 | O mesmo teste com o dedo usado, mesma marca | Mesmo ângulo | 3 |
| 5 | 0:10 | Técnico: "Ele não quebrou. Ele cansou." | Rosto | 2 |
| 6 | 0:12 | Jogo de dedos de um rotor na bancada | De cima | 6 |
| 7 | 0:18 | Técnico: "Comenta DEDO" | Rosto | 4 |

Segurança: morsa firme, óculos de proteção (dedo carregado pode escapar), rosto fora da linha da ponta.

**Áudio:** fala do técnico, som da bancada.

**Capa:** NOVO x 1 SAFRA

**Legenda**

```legenda
Comenta DEDO que eu te mando no direct o checklist do enleirador pra revisão de entressafra.

Dedo novo e dedo que trabalhou uma safra inteira na palha de cana, no mesmo teste: mesma marca na régua, mesmo puxão na ponta. O novo marcou [N] kg e o usado marcou [N] kg. Ele não quebrou, mas já não trabalha igual.

Na entressafra vale conferir o jogo inteiro do rotor, não só o dedo que quebrou. Dedos enleiradores e desenleiradores feitos em Jardinópolis-SP.

#enleirador #palhadecana #dedoenleirador #entressafra
```

**CTA:** comentar DEDO.

**Confirmar com a Jardmolas:** de onde vem o dedo usado (programa de reciclagem de dedos usados), quantas safras e em que máquina ele trabalhou; o resultado real do teste.

---

## R05: Chegou quebrada, saiu nova, ep. 1: a mola sem código

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Chegou quebrada, saiu nova | 3. Chegou quebrada, saiu nova | Mecânico, balconista, agricultor com máquina antiga | cerca de 20 s (18,4 s de fala) | Fábrica, bancada e máquina | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #13 Before And After | "Chegou assim, em dois pedaços e sem código. Saiu assim." | CHEGOU / SAIU | **62,6** |
| 2 | #21 Mid-Sentence Start | "...e o cliente falou: essa máquina não tem mais peça." | "NÃO TEM MAIS PEÇA" | 40,8 |
| 3 | #12 The Objection | "Essa mola não fabrica mais." Fabrica sim, olha. | "NÃO FABRICA MAIS" | 62,6 |

**Escolhido: 1.** É o nome da série e o corte entre a quebrada e a nova faz o trabalho. A opção 3 empata na nota, mas precisa ser frase que um cliente falou de verdade [confirmar]; se houver, usar no episódio seguinte.

Adaptar "em dois pedaços" ao caso real.

**Fala** (técnico; 49 palavras, cerca de 18,4 s)

```
Chegou assim, em [dois] pedaços e sem código.
Máquina antiga, peça que ninguém tinha.
Mas o que sobrou já conta muita coisa.
Grossura do arame. Diâmetro de fora. Passo das espiras.
Com isso a gente desenha a nova.
E saiu assim.
Tem mola sem código parada aí? Comenta MOLA.
```

**Texto na tela**

```
0:00  CHEGOU ASSIM
0:02  SEM CÓDIGO
0:05  ARAME: [N] mm
0:08  DIÂMETRO E PASSO
0:11  SOB MEDIDA
0:14  SAIU ASSIM
0:17  COMENTA MOLA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Pedaços da mola quebrada sendo colocados na bancada | De cima, close | 2 |
| 2 | 0:02 | Técnico juntando os pedaços | Plano médio | 3 |
| 3 | 0:05 | Paquímetro no arame, visor legível | Close | 3 |
| 4 | 0:08 | Paquímetro no diâmetro de fora; régua no passo | Close | 3 |
| 5 | 0:11 | Máquina enrolando a nova (do banco de imagens, da mesma mola) | Lateral | 3 |
| 6 | 0:14 | Quebrada e nova lado a lado, mão virando a nova | De cima | 3 |
| 7 | 0:17 | Técnico: "Comenta MOLA" | Rosto | 3 |

**Áudio:** fala com som da bancada e da máquina.

**Capa:** CHEGOU QUEBRADA, SAIU NOVA

**Legenda**

```legenda
Comenta MOLA se tem uma mola sem código parada aí, que a gente te chama no direct pra ver como fazer a sua.

Essa chegou em [N] pedaços, de uma [máquina, só se o cliente autorizar]. Sem código e sem desenho. Pelo que sobrou a gente tirou a grossura do arame, o diâmetro e o passo das espiras, e fez a nova sob medida aqui em Jardinópolis-SP.

Molas agrícolas e industriais, originais e de reposição. 17 anos de fábrica.

#molasobmedida #fabricademolas #pecasagricolas #ribeiraopreto
```

**CTA:** comentar MOLA.

**Confirmar com a Jardmolas:** um caso real recente, com autorização do cliente para mostrar a peça (e o nome da máquina, se ele deixar).

---

## R06: Chegou quebrada, saiu nova, ep. 2: a mola da válvula de retenção

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Chegou quebrada, saiu nova | 3. Chegou quebrada, saiu nova | Mecânico e encarregado de manutenção de usina | cerca de 26 s (25 s de fala) | Fábrica, com uma válvula ou portinhola de exemplo | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #10 If This, Then Watch | "Válvula de retenção batendo na sua usina? Olha a mola de torção." | VÁLVULA BATENDO? | **80,0** |
| 2 | #13 Before And After | "Essa mola de torção chegou rompida da usina. Saiu nova daqui." | CHEGOU / SAIU | 54,6 |
| 3 | #26 The Superlative | "A peça mais barata da válvula é a que para a linha." | A PEÇA MAIS BARATA | 37,2 |

**Escolhido: 1.** Separa logo quem tem o problema (válvula batendo) e dá a causa provável. A opção 3 é uma frase solta, sem prova.

**Fala** (técnico; 67 palavras, cerca de 25 s)

```
Válvula de retenção batendo na sua usina?
Olha a mola de torção.
É ela que fecha a portinhola antes do fluxo voltar.
Quando ela cansa ou rompe, a portinhola fecha atrasada.
E aí bate.
Essa aqui chegou rompida.
A gente mediu e fez nova, sob medida.
Com laudo do lote.
Entressafra é a hora de abrir e conferir.
Salva pra mostrar pro pessoal da manutenção da usina.
```

**Texto na tela**

```
0:00  VÁLVULA BATENDO?
0:03  OLHA A MOLA
0:05  ELA FECHA A PORTINHOLA
0:09  CANSOU OU ROMPEU: BATE
0:12  MEDIU, FEZ NOVA
0:16  COM LAUDO DO LOTE
0:19  ENTRESSAFRA: ABRE E CONFERE
0:23  SALVA E MOSTRA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Válvula dupla portinhola aberta na bancada, mão abrindo a portinhola | Plano médio, de frente | 3 |
| 2 | 0:03 | Mola de torção no pino | Close | 2 |
| 3 | 0:05 | Mão fechando a portinhola devagar, a mola trabalhando | Close lateral | 4 |
| 4 | 0:09 | Mola rompida na mão | Close | 3 |
| 5 | 0:12 | Técnico medindo a rompida: arame e ângulo das pernas | Close | 4 |
| 6 | 0:16 | Mola nova ao lado do laudo | De cima | 3 |
| 7 | 0:19 | Válvula montada com a nova | Plano médio | 4 |
| 8 | 0:23 | Técnico: "Salva pra mostrar pro pessoal da manutenção" | Rosto | 3 |

Se a cena for gravada dentro da usina: só com autorização da segurança do trabalho da usina, com o EPI dela, e sem logo nem nome da usina na imagem sem autorização por escrito.

**Áudio:** fala com som da bancada.

**Capa:** VÁLVULA BATENDO?

**Legenda**

```legenda
Salva esse vídeo e mostra pro pessoal da manutenção antes de abrir as válvulas na entressafra.

Na válvula de retenção dupla portinhola, quem fecha as portinholas antes do fluxo voltar é a mola de torção. Mola cansada ou rompida, a portinhola fecha atrasada e bate.

Essa chegou rompida e saiu nova, sob medida, com laudo do lote. A Jardmolas faz mola pra válvula de retenção, válvula de segurança e atuador, em Jardinópolis-SP, região de Ribeirão Preto.

#usinadeacucar #valvuladeretencao #manutencaoindustrial #entressafra
```

**CTA:** salvar.

**Confirmar com a Jardmolas:** caso real de mola de torção de válvula dupla portinhola; se eles têm uma válvula ou portinhola de exemplo para filmar.

---

## R07: Onde essa mola trabalha, ep. 1: o dedo na palha de cana

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Onde essa mola trabalha | 2. A mola no campo | Agricultor e operador de enleirador | 20 s | Fábrica (plano 2) e fazenda de cliente durante o recolhimento de palha | Filmador; operador do cliente trabalha normalmente |

**Precisa ser gravado até o fim de novembro**, enquanto ainda tem palha sendo recolhida. Depois da safra, só no ano que vem.

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #24 The Reveal | "Você só vê esse dedo quando ele quebra. Olha ele trabalhando." | VOCÊ SÓ VÊ QUANDO QUEBRA | **85,6** |
| 2 | #13 Before And After | "Esse dedo saiu da fábrica em Jardinópolis. Olha ele na palha." | DA FÁBRICA PRA PALHA | 40,8 |
| 3 | #14 The Callout | "Quem enleira palha de cana: olha o seu dedo trabalhando de perto." | QUEM ENLEIRA PALHA | 36,4 |

**Escolhido: 1.** É verdade para todo operador: o dedo só vira assunto quando quebra. A peça é o gancho e a frase dá o motivo para olhar. A opção 2 vira a legenda.

**Fala:** nenhuma. Som do trator e da palha. Se o operador falar alguma coisa natural durante a gravação, pode entrar com legenda.

**Texto na tela**

```
0:00  VOCÊ SÓ VÊ QUANDO QUEBRA
0:02  SAIU DE JARDINÓPOLIS
0:05  [CIDADE], PALHA DE CANA
0:09  OLHA ELE TRABALHANDO
0:12  LEIRA PRA ENFARDAR
0:16  AGORA VOCÊ VIU
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Rotor do enleirador girando na palha | Baixo, de lado, celular em tripé longe da linha da máquina; ninguém perto | 2 |
| 2 | 0:02 | Dedo novo na mão, na fábrica (do banco de imagens) | Close | 3 |
| 3 | 0:05 | Trator com enleirador passando, leira se formando | Aberto, tripé parado na lateral do talhão | 4 |
| 4 | 0:09 | Close dos dedos passando | Tripé baixo, zoom óptico se o celular tiver; nunca alguém segurando o celular perto | 3 |
| 5 | 0:12 | Leira pronta, câmera andando ao lado depois que a máquina já passou | Na altura do peito | 4 |
| 6 | 0:16 | Máquina parada, motor desligado, mão do operador no dedo | Close | 4 |

**Áudio:** som do campo.

**Capa:** VOCÊ SÓ VÊ QUANDO QUEBRA

**Legenda**

```legenda
Manda esse vídeo pra quem opera enleirador de palha de cana. É o dedo que ele só olha quando quebra.

Filmado em [fazenda e cidade, com autorização do cliente]. O dedo saiu da nossa fábrica em Jardinópolis-SP e tá aqui puxando a palha pra formar a leira que vai virar fardo.

Dedos enleiradores e desenleiradores de palha de cana, de reposição e sob medida, com arame Belgo.

#palhadecana #enleirador #dedoenleirador #ribeiraopreto
```

**CTA:** mandar para o operador.

**Confirmar com a Jardmolas:** cliente que deixa filmar a máquina trabalhando, com dedo Jardmolas; nome da fazenda e cidade só com autorização.

---

## R08: Onde essa mola trabalha, ep. 2: o pick-up da enfardadeira de feno

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Onde essa mola trabalha | 2. A mola no campo | Quem faz feno, operador de enfardadeira, mecânico de revenda | cerca de 24 s (23 s de fala) | Fazenda de cliente ou revenda, com a enfardadeira parada | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #10 If This, Then Watch | "Sua enfardadeira deixando feno no chão? Antes de mexer na regulagem, olha os dedos." | FENO FICANDO NO CHÃO? | **72,1** |
| 2 | #2 Negative Command | "Não deixa feno no chão por causa de um dedo quebrado." | NÃO DEIXA FENO NO CHÃO | 54,6 |
| 3 | #14 The Callout | "Quem faz feno: o dedo do pick-up quebra antes de você ver." | QUEM FAZ FENO | 48,6 |

**Escolhido: 1.** Começa por um sintoma que o operador já viu e manda olhar uma coisa barata antes de mexer na regulagem.

**Fala** (técnico; 62 palavras, cerca de 23 s)

```
Sua enfardadeira deixando feno no chão?
Antes de mexer na regulagem, olha os dedos.
Máquina desligada, tomada de força desligada.
Conta os dedos do pick-up.
Tem dedo faltando, torto ou com a ponta gasta?
Cada falha no pick-up é feno que fica pra trás.
Mede, manda a foto, a gente faz.
Comenta MEDIDA.
Eu te mando como medir o dedo da enfardadeira.
```

**Texto na tela**

```
0:00  FENO FICANDO NO CHÃO?
0:02  OLHA OS DEDOS
0:05  TOMADA DE FORÇA DESLIGADA
0:07  CONTA OS DEDOS
0:09  FALTANDO, TORTO, GASTO
0:13  FALHA = FENO NO CHÃO
0:16  MEDE E MANDA
0:19  COMENTA MEDIDA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Feno deixado no chão atrás da enfardadeira | Baixo, rente ao chão | 2 |
| 2 | 0:02 | Técnico na frente do pick-up, máquina parada | Plano médio | 3 |
| 3 | 0:05 | Chave fora da ignição e tomada de força desligada | Close | 2 |
| 4 | 0:07 | Mão passando pelos dedos do pick-up, contando | Close lateral | 2 |
| 5 | 0:09 | Dedo faltando, torto ou gasto | Close | 4 |
| 6 | 0:13 | Faixa de feno no chão | Aberto | 3 |
| 7 | 0:16 | Paquímetro no arame do dedo | Close | 3 |
| 8 | 0:19 | Técnico: "Comenta MEDIDA" | Rosto | 4 |

**Áudio:** fala com som do campo.

**Capa:** FENO FICANDO NO CHÃO?

**Legenda**

```legenda
Comenta MEDIDA que eu te mando no direct como medir o dedo do pick-up da sua enfardadeira.

Feno ficando no chão atrás da enfardadeira tem mais de uma causa, e uma delas é dedo do pick-up quebrado, torto ou faltando. Antes de mexer na regulagem, desliga a máquina, desliga a tomada de força e conta os dedos.

A Jardmolas faz molas e dedos pra enleirador e enfardadeira de feno, enleirador de capim e recolhedor de amendoim. Fábrica em Jardinópolis-SP.

#feno #enfardadeira #fenacao #pecasagricolas
```

**CTA:** comentar MEDIDA.

**Confirmar com a Jardmolas:** cliente ou revenda com enfardadeira para filmar; se a Jardmolas faz o dedo do pick-up das marcas mais comuns da região [confirmar quais].

---

## R09: Erro que quebra o dedo do enleirador, ep. 1: raspar o chão

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Erro que quebra o dedo do enleirador | 4. O técnico que resolve | Operador e mecânico de enleirador | cerca de 23 s | Fábrica (dedos) e campo (máquina parada) | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #2 Negative Command | "Para de raspar o chão com o enleirador. Quem paga é o dedo." | NÃO RASPA O CHÃO | **78,9** |
| 2 | #13 Before And After | "Dedo na altura certa contra dedo que raspou o chão. Olha a ponta." | CERTO / RASPANDO | 53,2 |
| 3 | #7 Wrong Way, Right Way | "Você tá quebrando dedo na regulagem, não no arame." | QUEBRA NA REGULAGEM | 48,6 |

**Escolhido: 1.** Manda parar um hábito que o operador reconhece e diz quem paga a conta. A comparação da opção 2 entrou como plano 3.

**Fala** (técnico; 61 palavras, cerca de 23 s)

```
Para de raspar o chão com o enleirador.
Quem paga é o dedo.
Olha a ponta desse aqui. Gastou e entortou.
Na palha de cana tem toco, tem pedra, tem terra.
Dedo raspando pega tudo isso de frente.
Regula a altura pelo manual da sua máquina.
E confere com ela parada, num chão plano.
Manda esse vídeo pro operador do enleirador.
```

**Texto na tela**

```
0:00  NÃO RASPA O CHÃO
0:02  QUEM PAGA É O DEDO
0:04  GASTOU E ENTORTOU
0:07  TOCO, PEDRA, TERRA
0:11  ALTURA PELO MANUAL
0:14  CONFERE COM ELA PARADA
0:18  MANDA PRO OPERADOR
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Dedo com a ponta gasta caindo na bancada | Close de cima | 2 |
| 2 | 0:02 | Técnico: "Quem paga é o dedo" | Rosto | 2 |
| 3 | 0:04 | Ponta gasta e torta ao lado de um dedo novo | Close | 3 |
| 4 | 0:07 | Chão do talhão com palha, toco, pedra | Baixo, rente | 4 |
| 5 | 0:11 | Mão na regulagem de altura do enleirador, máquina desligada | Close lateral | 3 |
| 6 | 0:14 | Trena entre a ponta do dedo e o chão, máquina parada em chão plano | Close | 4 |
| 7 | 0:18 | Técnico: "Manda pro operador" | Rosto | 4 |

**Áudio:** fala com som do lugar.

**Capa:** NÃO RASPA O CHÃO

**Legenda**

```legenda
Manda pro operador do enleirador antes da próxima safra. Esse dedo quebrou na regulagem, não no arame.

Enleirador regulado baixo demais faz o dedo raspar o chão. Na palha de cana tem toco, pedra e terra, e o dedo pega tudo de frente. A ponta gasta, entorta, e o dedo trabalha forçado.

Regula a altura pelo manual da sua máquina e confere com ela parada, em chão plano.

Dedos enleiradores e desenleiradores de palha de cana feitos em Jardinópolis-SP.

#enleirador #palhadecana #dedoenleirador #manutencaoagricola
```

**CTA:** mandar para o operador.

**Confirmar com a Jardmolas:** se raspar o chão é mesmo o erro que o técnico mais vê nos dedos que voltam; se ele tem uma referência prática de altura para falar no lugar de "pelo manual".

---

## R10: Erro que quebra o dedo do enleirador, ep. 2: o parafuso frouxo

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Erro que quebra o dedo do enleirador | 4. O técnico que resolve | Operador e mecânico de enleirador | cerca de 21 s (20 s de fala) | Campo ou oficina, máquina parada | Filmador; técnico fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #18 Cold Open Demo | "Olha esse dedo balançando no suporte com a máquina parada." | TÁ BALANÇANDO | 43,8 |
| 2 | #2 Negative Command | "Não sai pra safra sem apertar esse parafuso." | APERTA ANTES DA SAFRA | **54,6** |
| 3 | #1 Cost Confession | "Um parafuso frouxo custou [N] dedos numa semana de safra." | [N] DEDOS, 1 PARAFUSO | 63,2 |

**Escolhido: 2.** Não depende de caso. A opção 3 tem nota maior e é mais forte, mas só pode ser usada se o técnico tiver um caso real com o número [confirmar]. Se tiver, troca para ela.

**Fala** (técnico; 53 palavras, cerca de 20 s)

```
Não sai pra safra sem apertar esse parafuso.
Dedo frouxo balança a cada volta do rotor.
O esforço vai todo pra espira de baixo.
E é ali que ele quebra.
Máquina parada, chave na mão, confere um por um.
Arruela ou suporte gasto, troca junto.
Salva pra revisão da entressafra, antes da safra.
```

**Texto na tela**

```
0:00  APERTA ANTES DA SAFRA
0:02  BALANÇA A CADA VOLTA
0:05  QUEBRA AQUI
0:08  UM POR UM
0:11  GASTO? TROCA JUNTO
0:14  REVISÃO DE ENTRESSAFRA
0:18  SALVA PRA REVISÃO
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Mão balançando um dedo frouxo no suporte, máquina parada | Close | 2 |
| 2 | 0:02 | O dedo balançando, mais perto | Close lateral | 3 |
| 3 | 0:05 | Dedo quebrado na espira, com o dedo apontando onde rompeu | Close | 3 |
| 4 | 0:08 | Chave apertando o parafuso | Close | 3 |
| 5 | 0:11 | Arruela gasta ao lado de uma nova | De cima | 3 |
| 6 | 0:14 | Rotor inteiro, máquina parada | Aberto | 4 |
| 7 | 0:18 | Técnico: "Salva pra revisão" | Rosto | 3 |

**Áudio:** fala com som do lugar.

**Capa:** APERTA ANTES DA SAFRA

**Legenda**

```legenda
Salva pra revisão de entressafra do enleirador: parafuso do dedo apertado antes de ir pro campo.

Dedo frouxo no suporte balança a cada volta do rotor. O esforço vai pra espira de baixo e ali ele rompe. Confere um por um com a máquina parada e troca arruela ou suporte gasto junto com o dedo.

Dedos enleiradores e desenleiradores de palha de cana, feitos em Jardinópolis-SP.

#enleirador #palhadecana #entressafra #dedoenleirador
```

**CTA:** salvar.

**Confirmar com a Jardmolas:** se o dedo frouxo quebra mesmo na espira de baixo (ou em outro ponto; ajustar fala e plano 3); um caso real com número, para a opção 3.

---

## R11: Como medir sua mola em 30 segundos, ep. 1: compressão (puxa para o Identificador)

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Como medir sua mola em 30 segundos | 4. O técnico que resolve | Mecânico, balconista de revenda, agricultor | cerca de 29 s | Fábrica, bancada com fundo limpo | Filmador; técnico fala e mede |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #10 If This, Then Watch | "Sua mola não tem código? Mede essas 5 coisas." | MOLA SEM CÓDIGO? | **84,4** |
| 2 | #11 Numbered With A Favourite | "5 medidas pra cotar sua mola. A terceira quase todo mundo erra." | A 3ª TODO MUNDO ERRA | 80,0 |
| 3 | #16 The Verbatim Question | "Que medida vocês precisam pra fazer a mola?" São só 5. | SÃO SÓ 5 MEDIDAS | 65,2 |

**Escolhido: 1.** Separa quem tem o problema e promete uma lista curta. A opção 2 segura mais gente até o meio, mas só se o técnico confirmar qual medida o cliente mais erra [confirmar]; se confirmar, usar a 2 e trocar "a terceira" pela certa.

**Fala** (técnico; 77 palavras, cerca de 29 s)

```
Sua mola não tem código?
Mede essas 5 coisas.
1: a grossura do arame, no paquímetro.
2: o diâmetro de fora.
3: o comprimento, com ela solta.
4: quantas voltas ela tem, de ponta a ponta.
5: se enrola pra direita ou pra esquerda.
Tira uma foto com a trena do lado.
Coloca no Identificador de Molas, no nosso site.
O orçamento chega no seu WhatsApp.
Comenta MEDIDA.
Eu te mando o link pra cotar sua mola.
```

Enquanto o Identificador não estiver no ar, trocar as linhas 9 e 10 por "Manda essas medidas no nosso WhatsApp." e a última por "Eu te mando o guia pra medir sua mola."

**Texto na tela**

```
0:00  MOLA SEM CÓDIGO?
0:02  5 MEDIDAS
0:04  1 ARAME
0:07  2 DIÂMETRO DE FORA
0:09  3 COMPRIMENTO SOLTA
0:11  4 NÚMERO DE VOLTAS
0:14  5 DIREITA OU ESQUERDA
0:17  FOTO COM TRENA
0:20  IDENTIFICADOR DE MOLAS
0:25  COMENTA MEDIDA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Mola sem etiqueta caindo na bancada, mão com paquímetro entrando | De cima | 2 |
| 2 | 0:02 | Técnico: "Mede essas 5 coisas" | Rosto | 2 |
| 3 | 0:04 | Paquímetro no arame, visor legível | Close | 3 |
| 4 | 0:07 | Paquímetro no diâmetro de fora | Close | 2 |
| 5 | 0:09 | Mola em pé, régua no comprimento | Close lateral | 2 |
| 6 | 0:11 | Dedo contando as voltas, giz marcando a primeira | Close | 3 |
| 7 | 0:14 | Mola em pé girando devagar para mostrar o sentido | Close | 3 |
| 8 | 0:17 | Celular tirando foto da mola com a trena do lado | Por cima do ombro | 3 |
| 9 | 0:20 | Gravação da tela do celular preenchendo o Identificador | Gravação de tela | 5 |
| 10 | 0:25 | Técnico: "Comenta MEDIDA" | Rosto | 4 |

**Áudio:** fala do técnico, sala quieta (desligar compressor e rádio durante a fala).

**Capa:** MOLA SEM CÓDIGO? MEDE ASSIM

**Legenda**

```legenda
Comenta MEDIDA que eu te mando no direct o link do Identificador de Molas e a lista das 5 medidas.

Mola de compressão sem código? Mede a grossura do arame, o diâmetro de fora, o comprimento com ela solta, o número de voltas e o sentido do enrolamento. Tira foto com a trena do lado. No Identificador de Molas você coloca isso e o orçamento chega no seu WhatsApp.

Serve pra mecânico, balconista de revenda e pra quem tá com a máquina parada. Fábrica de molas em Jardinópolis-SP, região de Ribeirão Preto.

#moladecompressao #mecanicoagricola #pecasagricolas #fabricademolas
```

**CTA:** comentar MEDIDA.

**Confirmar com a Jardmolas:** se o Identificador já está no ar e o endereço final (o previsto em `02-identificador/instalacao-no-site.md` é jardmolas.com.br/identificador-de-molas). O protótipo pede também o tipo de ponta, escolhido na própria página; se quiserem, trocar a linha da foto por "Tira foto da ponta, com a trena do lado." Qual medida o cliente mais erra.

---

## R12: Como medir sua mola em 30 segundos, ep. 2: tração

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Como medir sua mola em 30 segundos | 4. O técnico que resolve | Mecânico, balconista de revenda | cerca de 22 s (20,6 s de fala) | Fábrica, bancada | Filmador; técnico fala e mede |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #2 Negative Command | "Não mede tração por fora do gancho. Mede assim." | POR FORA DO GANCHO, NÃO | **85,8** |
| 2 | #7 Wrong Way, Right Way | "Você tá medindo a mola de tração errado, e a culpa não é sua." | VOCÊ MEDE ERRADO | 44,5 |
| 3 | #10 If This, Then Watch | "Se a mola de tração da sua máquina quebrou, mede assim em 30 segundos." | MOLA DE TRAÇÃO QUEBROU? | 58,1 |

**Escolhido: 1.** Corrige um hábito numa frase e já mostra o certo. O protótipo do Identificador de Molas (`02-identificador/`) também pede o comprimento por dentro dos ganchos, então o Reel e a página falam a mesma coisa. Mesmo assim, confirmar com a Jardmolas antes de gravar: se eles usarem o comprimento total, inverter a frase.

**Fala** (técnico; 55 palavras, cerca de 20,6 s)

```
Não mede tração por fora do gancho.
Mede assim.
Por dentro dos ganchos, com a mola solta.
Depois a grossura do arame.
O diâmetro de fora do corpo.
E olha os ganchos: alinhados ou virados?
Foto de frente e de lado, com a trena.
Comenta MEDIDA.
Eu te mando o passo a passo do gancho.
```

**Texto na tela**

```
0:00  POR FORA DO GANCHO, NÃO
0:02  MEDE ASSIM
0:04  POR DENTRO DO GANCHO
0:07  ARAME
0:09  DIÂMETRO DE FORA
0:11  ALINHADO OU VIRADO?
0:14  2 FOTOS COM TRENA
0:17  COMENTA MEDIDA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Trena medindo a mola por fora dos ganchos (na edição, um X por cima) | Close de cima | 2 |
| 2 | 0:02 | Técnico: "Mede assim" | Rosto | 2 |
| 3 | 0:04 | Paquímetro por dentro dos ganchos | Close | 3 |
| 4 | 0:07 | Paquímetro no arame | Close | 2 |
| 5 | 0:09 | Paquímetro no diâmetro de fora do corpo | Close | 2 |
| 6 | 0:11 | Mola girando de ponta: ganchos alinhados e ganchos virados (duas molas) | Close de frente | 3 |
| 7 | 0:14 | Foto de frente e de lado com a trena | Por cima do ombro | 3 |
| 8 | 0:17 | Técnico: "Comenta MEDIDA" | Rosto | 4 |

**Áudio:** fala do técnico, sala quieta.

**Capa:** MOLA DE TRAÇÃO: MEDE ASSIM

**Legenda**

```legenda
Comenta MEDIDA que eu te mando no direct o passo a passo pra medir mola de tração.

O comprimento se mede por dentro dos ganchos, com a mola solta. Depois a grossura do arame, o diâmetro de fora do corpo e a posição dos ganchos: alinhados ou virados. Foto de frente e de lado, com a trena.

Mola de tração pra implemento, enfardadeira e máquina agrícola, sob medida ou de reposição. Jardinópolis-SP.

#moladetracao #mecanicoagricola #pecasagricolas #implementosagricolas
```

**CTA:** comentar MEDIDA.

**Confirmar com a Jardmolas:** como eles medem o comprimento da mola de tração; que outras medidas o Identificador pede para tração.

---

## R13: Entressafra e Caderno de Molas, ep. 1: o lançamento

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Caderno de Molas da Usina | Campanha de entressafra (pilar 4) | Mecânico, encarregado e gerente de manutenção de usina que estão no Instagram | cerca de 29 s | Fábrica, com molas de válvula, atuador e carreta na bancada | Filmador; dono ou gerente comercial fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #19 The Deadline | "Entressafra começa em dezembro. Cataloga as molas da usina antes." | ANTES DA SAFRA 2027 | 51,0 |
| 2 | #10 If This, Then Watch | "Se mola quebra na sua usina e ninguém acha o código, isso é pra você." | QUEBROU E NÃO ACHA O CÓDIGO? | 50,4 |
| 3 | #20 Permission | "Você não precisa parar a usina. Cataloga as molas na entressafra." | CATALOGA NA ENTRESSAFRA | **85,6** |

**Escolhido: 3.** Tira a objeção de cara (ninguém quer parar a usina para isso) e já põe a solução no lugar. O prazo da opção 1 é verdadeiro (dezembro a março) e aparece na fala.

**Fala** (dono ou gerente comercial; 77 palavras, cerca de 29 s)

```
Você não precisa parar a usina.
Cataloga as molas na entressafra.
De dezembro a março tá tudo aberto.
É a hora de olhar cada mola crítica.
Válvula, atuador, carreta.
A gente vai até a sua usina, de graça.
E cataloga uma por uma: onde trabalha, medida, quantidade.
Você recebe o Caderno de Molas da sua usina.
Quebrou na safra? Você manda o código, não a foto.
Comenta CADERNO.
Eu te explico como agenda a visita na usina.
```

**Texto na tela**

```
0:00  CATALOGA NA ENTRESSAFRA
0:04  DEZEMBRO A MARÇO
0:07  CADA MOLA CRÍTICA
0:10  VÁLVULA, ATUADOR, CARRETA
0:12  VISITA GRATUITA
0:15  ONDE, MEDIDA, QUANTIDADE
0:18  O CADERNO DA SUA USINA
0:21  MANDA O CÓDIGO
0:25  COMENTA CADERNO
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Dono ou gerente andando entre as prateleiras e falando | Celular andando de costas na frente dele, altura do peito | 4 |
| 2 | 0:04 | Mão preenchendo uma ficha do Caderno numa prancheta | Close de cima | 3 |
| 3 | 0:07 | Mola de válvula, de atuador e de carreta na bancada, mão passando por elas | Close, travelling lateral | 4 |
| 4 | 0:11 | Dono ou gerente: "A gente vai até a sua usina, de graça" | Rosto | 4 |
| 5 | 0:15 | Técnico medindo uma mola com paquímetro | Close | 3 |
| 6 | 0:18 | Ficha pronta, campos visíveis | De cima | 3 |
| 7 | 0:21 | Celular com uma mensagem de WhatsApp com o código da mola | Gravação de tela ou por cima do ombro | 4 |
| 8 | 0:25 | Dono ou gerente: "Comenta CADERNO" | Rosto | 4 |

**Áudio:** fala com som da fábrica por baixo.

**Capa:** CADERNO DE MOLAS DA USINA

**Legenda**

```legenda
Comenta CADERNO que eu te explico no direct como agendar a visita na sua usina.

O Caderno de Molas da Usina é uma visita técnica gratuita na entressafra, de dezembro a março. A gente vai até a usina e cataloga as molas críticas: válvula, atuador, carreta canavieira e o que mais pare a safra se quebrar. Cada mola fica registrada com onde trabalha, medida e quantidade instalada.

Na safra, quebrou, o pedido sai pelo código do Caderno. Jardmolas, fábrica de molas em Jardinópolis-SP há 17 anos.

#usinadeacucar #entressafra #manutencaoindustrial #canadeacucar
```

**CTA:** comentar CADERNO.

**Confirmar com a Jardmolas:** a aprovação da oferta do Caderno (proposta em `01-caderno-de-molas/oferta.md`: ficha por mola, PDF, planilha e código Jardmolas); até que distância eles vão; quantas visitas a equipe consegue fazer de dezembro a março. **Este Reel só sai depois da aprovação.**

---

## R14: Entressafra e Caderno de Molas, ep. 2: a primeira visita

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Caderno de Molas da Usina | Campanha de entressafra (pilar 5) | Manutenção e PCM de usina | cerca de 20 s (17,6 s de fala) | Dentro da primeira usina visitada, com autorização | Técnico que faz a visita, ou quem for junto; técnico fala |

**Só existe depois da primeira visita, com os números reais dela.** Se a visita não acontecer até 12/12, este Reel sai do calendário e entra um da reserva.

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #6 The Receipt | "Em [N] horas, [N] molas catalogadas numa usina. [N] sem código." | [N] MOLAS EM [N] HORAS | **62,6** (com números reais) |
| 2 | #18 Cold Open Demo | "Olha a gente medindo mola dentro de uma usina na entressafra." | DENTRO DA USINA | 35,2 |
| 3 | #21 Mid-Sentence Start | "...e essa mola não tinha código nenhum no almoxarifado." | SEM CÓDIGO NENHUM | 44,4 |

**Escolhido: 1.** Para o pessoal de manutenção, número de molas sem código é a prova que convence. A opção 3 serve se a visita tiver um achado assim, e aí pode ser o episódio 3.

**Fala** (técnico; 47 palavras, cerca de 17,6 s)

```
Em [N] horas, [N] molas catalogadas numa usina.
[N] sem código no almoxarifado.
Cada uma ganhou ficha.
Onde trabalha, medida, quantidade instalada.
Agora, se quebrar na safra, o pedido sai pelo código.
Ainda tem data na entressafra.
Comenta CADERNO.
A gente cataloga as molas da sua usina.
```

**Texto na tela**

```
0:00  [N] MOLAS EM [N] HORAS
0:03  [N] SEM CÓDIGO
0:06  CADA UMA COM FICHA
0:09  ONDE, MEDIDA, QUANTIDADE
0:12  NA SAFRA, PEDE PELO CÓDIGO
0:16  COMENTA CADERNO
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Técnico, com o EPI da usina, medindo uma mola de equipamento parado, bloqueado e liberado pela usina (ou um sobressalente do almoxarifado) | Close | 3 |
| 2 | 0:03 | Prateleira do almoxarifado com mola sem etiqueta | Plano médio | 3 |
| 3 | 0:06 | Foto sendo tirada e etiqueta sendo colocada | Close | 3 |
| 4 | 0:09 | Ficha preenchida | De cima | 3 |
| 5 | 0:12 | Técnico e o mecânico da usina conversando na frente do equipamento | Plano médio, sem logo da usina | 4 |
| 6 | 0:16 | Técnico: "Comenta CADERNO" | Rosto | 4 |

**Áudio:** fala com som do lugar.

**Capa:** [N] MOLAS SEM CÓDIGO

**Legenda**

```legenda
Comenta CADERNO que a gente te explica no direct como agendar a visita na sua usina.

Primeira visita do Caderno de Molas da Usina nesta entressafra: [N] horas, [N] molas catalogadas e [N] sem código no almoxarifado. Cada uma ganhou ficha com onde trabalha, medida e quantidade instalada.

A visita é gratuita, de dezembro a março. Ainda tem data: [datas livres].

#usinadeacucar #entressafra #manutencaoindustrial #canadeacucar
```

**CTA:** comentar CADERNO.

**Confirmar com a Jardmolas:** data da primeira visita; autorização da usina por escrito para filmar e para citar (ou não) o nome; os números reais; as datas que ainda estão livres.

---

## R15: O técnico que resolve: as 3 fotos do WhatsApp

| Série | Pilar | Para quem | Duração | Onde | Quem grava |
| --- | --- | --- | --- | --- | --- |
| Avulso (vira post fixado de "pessoa") | 4. O técnico que resolve | Todos que compram pelo WhatsApp | cerca de 26 s | Fábrica, mesa ou balcão de atendimento | Filmador; atendente do WhatsApp fala |

**Ganchos**

| # | Fórmula (hooks.json) | Linha | Na tela | Nota |
| --- | --- | --- | --- | --- |
| 1 | #24 The Reveal | "Essa é a cara de quem responde o seu WhatsApp aqui na Jardmolas." | QUEM TE RESPONDE | 44,2 |
| 2 | #9 The Steal | "Copia essas 3 fotos. Seu orçamento de mola não volta com pergunta." | COPIA ESSAS 3 FOTOS | **78,6** |
| 3 | #8 Insider Leak | "Faz [N] anos que eu respondo pedido de mola. Essa foto me salva." | [N] ANOS NO WHATSAPP | 54,4 |

**Escolhido: 2.** Dá uma coisa que a pessoa usa hoje, e quem fala é quem responde, então apresenta a pessoa sem precisar de "oi, eu sou". A opção 3 precisa do tempo real de casa do atendente [confirmar].

**Fala** (atendente; 70 palavras, cerca de 26 s)

```
Copia essas 3 fotos.
Seu orçamento de mola não volta com pergunta.
Eu sou [nome], eu respondo o WhatsApp da Jardmolas.
Foto 1: a mola inteira, com a trena do lado.
Foto 2: de perto, na ponta ou no gancho.
Foto 3: a placa da máquina, ou onde ela trabalha.
Com essas 3, quase sempre já dá pra cotar.
Salva pra próxima mola quebrada, e manda as 3 fotos.
```

**Texto na tela**

```
0:00  COPIA ESSAS 3 FOTOS
0:02  ORÇAMENTO SEM VAI E VOLTA
0:05  [NOME], DO WHATSAPP
0:08  1 INTEIRA, COM TRENA
0:12  2 PONTA OU GANCHO
0:15  3 PLACA DA MÁQUINA
0:19  (16) 99176-0936
0:22  SALVA PRA PRÓXIMA
```

**Planos**

| # | Tempo | O que filmar | Ângulo | Seg. |
| --- | --- | --- | --- | --- |
| 1 | 0:00 | Celular na mão do atendente recebendo foto de mola no WhatsApp | Por cima do ombro | 2 |
| 2 | 0:02 | Atendente falando | Rosto, prateleira de molas atrás | 3 |
| 3 | 0:05 | Atendente se apresentando | Plano médio no balcão | 3 |
| 4 | 0:08 | Foto 1 sendo tirada: mola inteira com trena | Por cima do ombro | 4 |
| 5 | 0:12 | Foto 2: close da ponta ou do gancho | Por cima do ombro | 3 |
| 6 | 0:15 | Foto 3: placa de uma máquina (de cliente que autorizou, sem número de série legível) | Close | 4 |
| 7 | 0:19 | Atendente: "Com essas 3, quase sempre já dá pra cotar" | Rosto | 3 |
| 8 | 0:22 | Atendente: "Salva pra próxima" | Rosto | 4 |

**Áudio:** fala do atendente, sala quieta.

**Capa:** COPIA ESSAS 3 FOTOS

**Legenda**

```legenda
Salva pra próxima mola quebrada: 3 fotos que deixam o orçamento pronto pra sair.

Foto 1: a mola inteira, com a trena do lado. Foto 2: de perto, na ponta ou no gancho. Foto 3: a placa da máquina ou o lugar onde a mola trabalha. Quem responde é o [nome], aqui na fábrica em Jardinópolis-SP.

WhatsApp (16) 99176-0936.

#pecasagricolas #mecanicoagricola #fabricademolas #ribeiraopreto
```

**CTA:** salvar.

**Confirmar com a Jardmolas:** nome de quem responde o WhatsApp e se a pessoa topa aparecer; se com essas 3 fotos dá mesmo para cotar na maioria das vezes (se precisar de mais alguma coisa, entra na fala).

---

## Receita das legendas (saída do caption.py, conferida na mão)

Todas as 15 legendas: primeira linha inteira dentro dos 125 caracteres que o feed mostra, uma CTA só (conferida na mão, porque o caption.py não lê CTA em português), 4 hashtags sem acento abaixo da dobra (o limite é 5; o humanize.py marca 5 ou mais como parede de hashtag, então fica uma de folga), nenhum link no corpo, nenhum emoji. A legenda do R15 tem o número do WhatsApp escrito, que não é link e serve para quem quer copiar.

Antes de publicar, trocar todo [N] e todo [confirmar] pelo dado real. Se o dado não existir, a frase sai.
