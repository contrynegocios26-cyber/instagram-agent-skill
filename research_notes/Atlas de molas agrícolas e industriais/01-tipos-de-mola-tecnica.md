# Taxonomia técnica de molas e formas de arame: tipos, materiais, normas, processos e falhas (referência para a Jardmolas)

> Nota de método (09/11/2026): 26 buscas na web. Não consegui buscar páginas inteiras: `belgo.com.br`, `lesjofors.com` e `jardmolas.com.br` não resolvem neste ambiente. A cota de buscas da sessão acabou antes de cobrir quatro temas: as composições SAE (1070, 1095, 5160, 6150, 9254, 9260), as máquinas (CNC, 4-slide, torção), os dedos de cana e as molas de peneira vibratória. Muitos achados vêm de resumos dos resultados de busca, não da página inteira. Por isso há catálogos de fornecedor citados como fonte primária em temas de norma. Tudo marcado **[confirmar]** é conhecimento geral de engenharia sem fonte nesta sessão. Os termos em português (BR) aparecem ao lado do termo em inglês.

---

## 1. Molas helicoidais: compressão, tração (extensão) e torção

### Takeaway
As três famílias helicoidais são a maior parte do que uma fábrica de molas por arame produz: compressão (*compression*), tração (*extension/tension*) e torção (*torsion*). O que as diferencia é o sentido da carga: a de compressão é empurrada, a de tração é puxada e a de torção recebe um momento de giro. A ponta e o gancho definem boa parte do custo, da estabilidade e da resistência à fadiga. Na mola de tração, a **tensão inicial** (pré-carga entre espiras) é um parâmetro próprio.

### Cited Findings

**1.1 Mola helicoidal de compressão (*helical compression spring*)**
- No Brasil, a norma usa o nome "mola helicoidal de compressão", por exemplo na ABNT NBR 12794 (veículo ferroviário) — [normas.com.br NBR 12794](https://normas.com.br/visualizar/abnt-nbr-nm/309/abnt-nbr12794-mola-helicoidal-de-compressao-para-veiculo-ferroviario).
- A EN 15800 trata as molas cilíndricas helicoidais de arame redondo usadas em compressão: requisitos de qualidade, propriedades características e bases de cálculo. Seu escopo cobre, entre outros limites, arame de 0,07 mm a 16 mm — [Standards.ie – DIN EN 15800:2009-03](https://shop.standards.ie/en-ie/standards/din-en-15800-2009-03-450835_saig_din_din_892001); [BSI – EN 15800](https://knowledge.bsigroup.com/products/cylindrical-helical-springs-made-of-round-wire-quality-specifications-for-cold-coiled-compression-springs).
- **Tipos de ponta (*end types*):**
  - **Ponta aberta (*open ends*):** é a opção menos comum. Sem um pino por dentro, a mola em geral não fica em pé sozinha — [Century Spring – spring end types](https://centuryspring.com/resources/spring-end-types); [Acxess Spring – compression end types](https://acxesspring.com/compression-spring-end-types.html).
  - **Ponta fechada, ou fechada e assentada (*closed / squared*):** é o tipo mais comum — mesmas fontes acima.
  - **Ponta fechada e esmerilhada/retificada (*closed and ground*):** a última espira é retificada até ficar plana, e não apenas "assentada" com espira parcial. A retífica ajuda a mola a ficar em pé e reduz a flambagem — [Century Spring](https://centuryspring.com/resources/spring-end-types); [Lee Spring – Compression Spring Basic Features (PDF)](https://www.leespring.com/sites/default/files/pdf/Lee%20Spring%20-%20WhitePaper%20-%20Compression%20Spring%20Basic%20Features_US.pdf).
  - **Ponta dupla fechada (*double closed*):** dá estabilidade a molas esbeltas e sai mais barata que a fechada e esmerilhada — [Acxess Spring](https://acxesspring.com/compression-spring-end-types.html); [Tevema – multiple ends](https://webshop.tevema.com/gb/blog/multiple-ends-compression-springs).
- **Variantes de forma:** cilíndrica, cônica (*conical*), barril (*barrel/convex*), ampulheta (*hourglass/concave*) e passo variável (*variable pitch*). Não encontrei fonte lida com a definição de cada uma. A Essentra tem um artigo sobre "tipos de mola de compressão" que apareceu nos resultados, mas não foi lido — [Essentra](https://www.essentracomponents.com/en-gb/news/solutions/pcb-electronics/different-types-of-compression-springs). As descrições abaixo são **[confirmar]**:
  - A cônica pode encaixar as espiras umas dentro das outras ao comprimir, o que reduz a altura sólida e dá uma curva de carga progressiva.
  - A barril e a ampulheta mudam a estabilidade lateral e a ressonância.
  - O passo variável dá uma constante progressiva e ajuda a controlar a vibração (*surge*) em molas de válvula.
- **Termo de projeto citado:** índice de mola (*spring index*) = diâmetro médio ÷ diâmetro do arame — [Acxess Spring – extension spring design](https://acxesspring.com/extension-spring-design.html).

**1.2 Mola helicoidal de tração / extensão (*extension spring*)**
- **Tensão inicial (*initial tension*):** é a força interna que mantém fechadas as espiras de uma mola de tração enrolada encostada (*close-wound*). Em geral é definida como a força mínima para separar espiras adjacentes — [GlobalSpec – Extension springs](https://www.globalspec.com/learnmore/mechanical_components/springs/helical_extension_springs); [datasheet Lee Spring via GlobalSpec](https://datasheets.globalspec.com/ds/lee-spring/ei-011b-05-m/1bc738de-083f-498f-b04f-08edb4e2081b).
- A tensão inicial nasce no enrolamento: o arame é girado "para trás" enquanto a mola é enrolada. A Century diz que esse valor é bem mais difícil de controlar e o informa só como referência — [Century Spring – extension springs](https://www.centuryspring.com/extension-springs).
- Força total = tensão inicial + constante × deflexão. A tensão inicial entra uma vez só e não se acumula como a constante. Molas com índice alto exigem menos tensão inicial — [Acxess Spring – close wound](https://acxesspring.com/close-wound-coil-springs.html); [Acxess – extension design](https://acxesspring.com/extension-spring-design.html).
- **Ganchos e olhais (*hooks and loops*):**
  - **Famílias:** o gancho (*hook*) tem abertura; o olhal (*loop*) é fechado por completo.
  - **Mais comuns:** o olhal de máquina (*machine loop*, olhal dobrado da última espira) e o olhal cruzado (*crossover loop*, cruzando o centro). O olhal cruzado costuma ir em molas pequenas e o de máquina em molas maiores. O gancho de máquina resiste mais que o gancho cruzado central porque o raio de dobra é menos fechado.
  - **Gancho lateral (*side hook*):** usado quando o corpo da mola precisa desviar de outros componentes.
  - **Gancho estendido (*extended hook*):** é o tipo de gancho mais caro.
  - Quanto menor o espaço do olhal de máquina, mais fechado fica o raio de transição e maior a concentração de tensão.
  - Fontes: [Acxess Spring – hook types](https://www.acxesspring.com/tension-extension-spring-hook-types.html); [Lee Spring – extension](https://www.leespring.com/int_learn_extension.asp); [Industrial Technology – back to basics](https://www.industrialtechnology.co.uk/back-to-basics-on-extension-springs).
  - Meia volta (*half loop*), volta inteira (*full loop*) e inserto/tampão rosqueado (*threaded insert*) aparecem citados nas mesmas fontes, mas não li os detalhes **[confirmar]**.
- A EN 13906-2:2013 é a norma europeia de cálculo de molas de tração. Ela substitui a DIN 2089-2 — [Standards.ie – DIN EN 13906-2](https://shop.standards.ie/en-ie/standards/din-en-13906-2-2013-09-420805_saig_din_din_864969).

**1.3 Mola de torção (*torsion spring*; "mola de perna" na terminologia DIN, *Schenkelfeder*)**
- A EN 13906-3:2014 é a norma de cálculo das molas de torção helicoidais. Uma listagem diz que ela substitui a DIN 2088 (07/2002); outra página DIN diz que substitui a DIN EN 13906-3:2002. **As fontes divergem** — [Standards.ie – DIN EN 13906-3](https://shop.standards.ie/en-ie/standards/din-en-13906-3-2014-06-420813_saig_din_din_951678); [DIN – EN 13906-3](https://www.din.de/en/wdc-beuth:din21:198895053).
- **Mola de torção dupla (*double torsion*):** fabricantes chineses e indianos anunciam molas de torção dupla para ancinhos, enfardadoras, colhedoras e ancinhos acionados pela TDP. A forma típica é o "dedo" agrícola — [HB Custom Spring (Alibaba)](https://hbcustomspring.en.alibaba.com); [Trutech Springs (Aajjo)](https://www.aajjo.com/product/harvester-hey-tines-spring-in-meerut-trutech-springs). Mais detalhes na seção 2.
- **Como funciona [confirmar]:** a carga é um momento aplicado nas pernas. A mola trabalha de preferência no sentido de fechar as espiras, e o arame trabalha principalmente em flexão.

### Inferences
- Inferência: para a equipe de vendas, a primeira pergunta de classificação é "a mola é empurrada, puxada ou girada?". A segunda é o tipo de ponta ou gancho, porque muda custo, ferramental e fadiga.
- Inferência: o gancho estendido e o inserto rosqueado são os mais caros. Em orçamento de mola de tração, vale perguntar se o cliente aceita um olhal de máquina padrão.

### Gaps
- Não encontrei fonte lida com a definição formal de mola cônica, barril, ampulheta e passo variável, nem com a geometria de meia volta, volta inteira e inserto rosqueado.
- Não encontrei a norma ISO de vocabulário de molas (ISO 26909, *Springs — Vocabulary*) **[confirmar existência e edição]**.

---

## 2. Formas de arame e molas agrícolas: dedos, dentes, grampos, ganchos, pinos e anéis de arame

### Takeaway
"Forma de arame" (*wire form*) é qualquer peça de arame dobrada em 2D ou 3D que não é uma hélice simples. O dedo de enleirador ou ancinho é, tecnicamente, uma **mola de torção dupla com pernas longas** em aço-mola, e as fontes mostram jateamento (*shot peening*) e pintura nos produtos de ponta. Não há fonte pública sobre o dedo de palha de cana brasileiro em si.

### Cited Findings
- **Dedos de ancinho e espalhador (*tedder/rake tines*):** são feitos de aço-mola. Os dedos Sitrex são vendidos com o argumento de menos quebra em condições severas. Os dedos duplos montam nos braços do rotor do espalhador — [Ford Distributing – tedder tine](https://forddistributing.com/tedder-tine.html); [Reliable Aftermarket Parts – double tedder tines](https://www.reliableaftermarketparts.com/en-au/products/6-of-kt-1-double-teeth-tedder-tines-15-375-tines-x-3-50-gap-x-2-75-coil).
- **Montagem:** a Ford Distributing recomenda trocar um dedo de cada vez e manter a mesma orientação. Um dedo montado ao contrário ainda funciona, mas quebra mais — [Ford Distributing](https://forddistributing.com/tedder-tine.html).
- **Dente de ancinho de rodas Herschel:** aço-mola tratado termicamente, com pintura contra ferrugem — [Farm & Fleet – Herschel OT1A](https://www.farmandfleet.com/products/333249-herschel-wheel-rake-tooth-ot1a.html).
- **Pöttinger:** dedos duplos em aço-mola "Super C", descrito como aço-mola "com carbono reduzido" (*carbon-depleted*) e mais elástico — [Pöttinger tines](https://www.poettinger.at/en_in/produkte/detailtexthl/HIVA/th/2/poettinger-tines). O termo "carbon-depleted" é do fabricante; o significado metalúrgico não está claro **[confirmar]**.
- **Kverneland:** dedos "Super-C" de espalhador com arame de aço-mola de **10 mm**, jateado (*shot-peened*), e diâmetro de espira de **80 mm** — [Kverneland 8000 tedders (flippingbook)](https://flippingbook.kverneland.com/view/323669715/8/).
- **Patente de dedo de recolhedor de enfardadora (*pick-up tine*):** um único fio contínuo de material resiliente, com uma base de várias espiras helicoidais lado a lado e uma perna alongada — [Justia – Rake teeth patents, classe 56/400](https://patents.justia.com/patents-by-us-classification/56/400).
- **Dente-mola John Deere (*spring tooth*):** aparece como peça de reposição — [RDO Equipment – JD E56470](https://checkout.rdoequipment.com/john-deere-spring-tooth-e56470/).
- **Anéis de arame redondo (*round wire snap rings*):** a referência para anéis de arame redondo e para as ranhuras de eixo e furo é a DIN 7993. A Fasten.it lista em português "anéis elásticos de arame redondo para eixos e furos" — [Fasten.it (PT)](https://www.fasten.it/pt/search/suppliers/287).

### Inferences
- Inferência: os "dedos" da Jardmolas para enleirador e desenleirador de palha de cana têm muito provavelmente a mesma arquitetura dos dedos de ancinho e espalhador de feno: torção dupla com duas pernas, ou torção simples com perna longa, presos ao rotor. O diâmetro do arame tende a ser da ordem dos 10 mm da Kverneland **[confirmar com desenhos da Jardmolas]**.
- Inferência: pelos produtos de ponta citados, três coisas diferenciam um dedo bom: jateamento, material de alta fadiga e pintura. São argumentos de venda legítimos contra o dedo barato, desde que a Jardmolas de fato faça essas etapas **[confirmar]**.
- Inferência: subtipos de forma de arame para o catálogo: dedos e dentes (*tines*); grampos e presilhas (*clips*); ganchos (*hooks*); pinos-trava e contrapinos de arame, como o pino "R" e o grampo-trava **[confirmar terminologia]**; anéis de arame; alças, suportes e hastes dobradas.

### Gaps
- Não encontrei fonte sobre dedos de enleirador e desenleirador de palha de cana (diâmetro, aço, número de espiras), nem sobre os fabricantes OEM brasileiros desses implementos. A cota de buscas acabou antes.
- Não confirmei o aço usado nos dedos de feno (por exemplo, SAE 5160 ou 9260). As fontes dizem apenas "aço-mola".
- Não encontrei fonte sobre molas de recolhedor de amendoim (*peanut pick-up*). Por analogia com a patente de recolhedor de enfardadora, devem ser dedos de torção **[confirmar]**.

---

## 3. Molas planas e especiais: feixe de molas, parabólica, prato (Belleville), ondulada, espiral, força constante e barra de torção

### Takeaway
Estas molas usam sobretudo **chapa, fita ou barra**, não arame redondo enrolado. Exigem prensas, conformação de fita ou forjamento e tratamento térmico de têmpera e revenido. São quase sempre outra cadeia de fabricação, diferente da de molas helicoidais de arame.

### Cited Findings
- **Feixe de molas (*leaf spring*) e mola parabólica:**
  - Uma dissertação da UFMG comparou o feixe convencional de aço com um feixe parabólico (lâminas de espessura variável) e com um conjunto híbrido aço-fibra. Na análise por elementos finitos, o híbrido reduziu a massa em cerca de 42%, com penalidade de 20,91% em tensão e 23,93% em deflexão. A monolâmina híbrida de espessura variável chegou a 61,47% de redução de massa — [UFMG – Dissertação L. L. Dias (PDF)](https://repositorio.ufmg.br/bitstream/1843/51810/3/DISSERTA%C3%87%C3%83O_LEONARDOLELISDIAS_FINAL.pdf); [registro UFMG](https://repositorio.ufmg.br/handle/1843/51810?locale=en).
  - A parabólica é descrita como lâmina única, com seção variável em dois planos: mais larga nas pontas em planta e mais grossa no centro em vista lateral — [Autoentusiastas](https://autoentusiastas.com.br/2025/11/suspensao-independente-com-uma-mola-apenas/) **[confirmar página exata; o trecho apareceu num resumo de busca]**.
  - Na Fenatran 2026, a thyssenkrupp afirmou que os feixes continuam relevantes onde se exige alta capacidade de carga e resistência a condições severas — [Mecânica Online, 11/2026](https://mecanicaonline.com.br/2026/11/suspensao-mais-leve-para-caminhoes-eletricos-thyssenkrupp-apresenta-tecnologia-na-fenatran-2026/).
  - A ABNT NBR 8567 (cálculo e projeto de feixe de molas para veículos rodoviários) está **cancelada sem substituição desde 09/2012** — [Target – NBR 8567](https://www.target.com.br/produtos/normas-tecnicas/31660/nbr8567-calculo-e-projeto-de-feixe-de-molas-para-veiculos-rodoviarios).
  - O aço 52CrMoV4 (EN 10089) é usado em feixes de mola e em outras molas veiculares — [Ovako Steel Navigator](https://steelnavigator.ovako.com/steel-grades/52crmo4/).
- **Mola prato / arruela Belleville (*disc spring*):**
  - A DIN 2093:2013-12 virou a **DIN EN 16983:2017** (qualidade e dimensões) com conteúdo técnico idêntico. A DIN 2092 (cálculo) virou a **DIN EN 16984** — [SPIROL – DIN EN 16983](https://SPIROL.com/product/disc-springs/disc-springs-per-din-en-16983-formerly-din-2093/); [SPIROL – design guide (PDF)](https://uk.spirol.com/assets/files/dsc-disc-spring-design-guide-uk.pdf).
  - Grupo 1 = espessura < 1,25 mm; Grupo 2 = 1,25 a 6 mm (tabela da SPIROL). O Grupo 3 (> 6 mm) não aparece na fonte **[confirmar]**.
  - Séries A, B e C, com De/t ≈ 18, 28 e 48 e ho/t ≈ 0,4, 0,75 e 1,3. A forma da curva carga × deflexão depende de ho/t — [SPIROL](https://shop.spirol.com/category/disc-springs).
  - Os tamanhos padrão da SPIROL vão de Ø8 a Ø200 mm. Eles atendem a DIN EN 16983 em material, tolerância e qualidade, mas parte das combinações de diâmetro e espessura não está na tabela da norma — [SPIROL – DIN EN 16983](https://SPIROL.com/product/disc-springs/disc-springs-per-din-en-16983-formerly-din-2093/).
- **Mola ondulada (*wave spring*):**
  - A Smalley tem as molas "Crest-to-Crest", multivoltas de fio chato, empilhadas em série. A constante cai na proporção do número de voltas. Ocupam **até 50% menos espaço axial** que uma mola helicoidal de força equivalente (número de catálogo, máximo). Servem para constante baixa ou média, deflexão grande e força baixa ou média. Há versões aninhadas (*nested*, mais força), entrelaçadas e com ponta de calço (*shim-end*, 360° de apoio) — [Smalley – Crest-to-Crest](https://www.smalley.com/wave-springs/crest-crest); [Smalley node 4417](https://www.smalley.com/node/4417); [Smalley – Nestawave](https://smalley.com/nestawave); [datasheet Smalley C200-M1](https://datasheets.globalspec.com/ds/smalley/c200-m1/a4e4279a-0015-4f5d-8f10-c0454c861a49).
  - A Smalley tem um catálogo em português (PDF), não lido — [Smalley SM4PPPTBR](https://www.smalley.com/sites/default/files/pdfs/SM4PPPTBR-A4%20%28updated%20021717%29.pdf).
- **Mola de força constante (*constant force spring*):** rolo de fita pré-tensionada que resiste a desenrolar com força quase constante, em movimento linear. É usada em contrapesos e mecanismos retráteis — [Fastener Engineering – constant force springs](https://fastenerengineering.com/what-are-constant-force-springs/); [MW Components – constant force](https://www.mwcomponents.com/constant-force-springs).
- **Mola espiral / de potência / de relógio (*spiral power spring, clock spring, mainspring*):** fita enrolada em espiral plana que fornece torque rotativo. O torque **não** é constante e varia com o giro. A terminologia se sobrepõe à da mola de força constante, porque "*power spring*" é usado para as duas — [Fastener Engineering](https://fastenerengineering.com/what-are-constant-force-springs/); [USPTO 5054162 – constant force compensation for power spring](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5054162).
- **Barra de torção (*torsion bar*):** está no escopo de normas brasileiras de aço para molas. A ABNT NBR 16804 (11/2019, confirmada em 07/2024) cobre barras laminadas a quente e fio-máquina de qualidade especial para molas helicoidais, **barras de torção e barras estabilizadoras**, voltada à indústria automobilística — [normas.com.br – NBR 16804](https://www.normas.com.br/visualizar/abnt-nbr-nm/11536/abnt-nbr16804-barras-laminadas-a-quente-e-fios-maquina-de-aco-redondos-de-qualidade-especial-para-molas-helicoidais-barras-de-torcao-e-barras-estabilizadoras-requisitos). A NM 175 trata o mesmo tema para barras com acabamento de superfície — [normas.com.br – NM 175](https://www.normas.com.br/visualizar/abnt-nbr-nm/20287/abnt-nm175-barras-de-aco-com-acabamento-de-superficie-redondas-de-qualidade-especial-para-molas-helicoidais-barras-de-torcao-e-barras-estabilizadoras).

### Inferences
- Inferência: feixe de molas, mola prato, mola ondulada, mola espiral e mola de força constante pedem fita ou chapa (laminada a frio ou a quente), prensas, conformação e têmpera em forno. Não fazem parte do perfil "arame + enroladeira" declarado pela Jardmolas. Quando um cliente pedir, o normal é encaminhar ou revender **[confirmar com a Jardmolas]**.
- Inferência: a barra de torção é uma barra redonda temperada que trabalha em torção pura. É rara no agro, mas existe em suspensões e em alguns implementos.

### Gaps
- Não achei fonte sobre fabricantes brasileiros de mola prato, mola ondulada e mola de força constante, nem sobre o uso de feixe de molas em implementos agrícolas e carretas brasileiras.

---

## 4. Elementos elásticos padronizados: pino elástico, anel elástico, mola garter, mola para matriz (ISO 10243) e mola a gás

### Takeaway
São itens de catálogo normalizado (DIN e ISO), em geral feitos por especialistas de alto volume. Para uma fábrica de molas sob encomenda, entram mais como **revenda ou indicação** do que como produção, com exceção da mola garter de arame. A mola a gás **não é mola de arame**.

### Cited Findings
- **Pino elástico (*spring pin, roll pin*):**
  - **Fendido ou partido (*slotted*):** normalmente fornecido na forma pesada da ISO 8752. Há versão leve pela ISO 13337. Também são citadas DIN 1481, DIN 7346 e BS 7060 — [Torqbolt](https://torqbolt.com/slotted-pin-manufacturers-suppliers-india).
  - A SPIROL afirma que a DIN 1481 é intercambiável com a ISO 8752 (EN 28752), exceto pela tolerância de comprimento. A empresa recomenda pinos ASME B18.8.4M para projetos novos — [SPIROL – Slotted Spring Pins (PDF)](https://cdn.shopify.com/s/files/1/0492/3631/2223/files/SPIROL-Slotted-Spring-Pins-us.pdf).
  - **Espiral (*coiled*):** ligado à DIN 7343 e à ISO 8750, muitas vezes junto da ASME B18.8.3M. É indicado para vibração e choque. O pino de aço-mola é mais resistente que o inox, mas enferruja em ambiente úmido — [McMaster-Carr](https://www.mcmaster.com/products/springs/length~12-mm).
- **Anel elástico / anel de retenção (*retaining ring*, "anel Seeger"):**
  - DIN 471 = anel externo para **eixo**, tipo normal e pesado. DIN 472 = anel interno para **furo**. Os dois prendem componentes como rolamentos e transmitem força axial — [Seeger-Orbis – DIN 471/472](https://www.seeger-orbis.com/products/retaining-rings/seeger-rings-to-din-471-472); [McMaster – DIN 471](https://www.mcmaster.com/products/din-471-retaining-rings/); [McMaster – DIN 472](https://www.mcmaster.com/products/din-472-retaining-rings/).
  - O catálogo DIN lista novas edições da DIN 471 e da DIN 472 previstas para 2026-05 — [DIN – rings, bushes (ICS 21.060.60)](https://6sku3uaup9f9.din.de/en/mechanical-engineering/BVFR020/21.060.60/rings-bushes-sleeves-collars/all) **[confirmar se já publicadas em 11/2026]**.
  - A DIN 6799 é a arruela de retenção para eixo (estampada, não de arame). A edição de 06/2017 substitui a de 04/2011 — [Fabory](https://fabory.com/en_GB/c/011008).
  - A DIN 7993 é o anel de arame redondo — [Fasten.it](https://www.fasten.it/pt/search/suppliers/287).
- **Mola garter / mola de retentor (*garter spring*):**
  - É uma mola helicoidal com as pontas unidas em anel, usada em retentores de óleo, vedações de eixo e dispositivos com correia — [Wikipedia – Garter spring](https://en.wikipedia.org/wiki/Garter_spring).
  - A Katy Spring a descreve como "uma mola de tração com as pontas unidas em círculo" — [Katy Spring (Steel Technology)](https://www.steel-technology.com/products/katy-spring-manufacturing-inc/garter-springs).
  - Existem versões de tração (puxam para o centro) e de compressão (empurram para fora) — [Wikipedia](https://en.wikipedia.org/wiki/Garter_spring).
  - **Emenda:** conector com gancho e olhal, ponta de diâmetro reduzido (*nib*) encaixada na outra ponta, ou olhais entrelaçados. A emenda por ponta reduzida é descrita como a mais comum, mas essa fonte é um espelho de enciclopédia de qualidade incerta — [Cavac](https://cavac.at/cavacopedia/Garter%20spring).
  - No glossário de vedações, a garter é a mola dentro do lábio do retentor — [Glossário (Scribd)](https://www.scribd.com/document/47005790/Glossary).
- **Mola para matriz (*die spring*, mola de seção retangular para ferramentas de prensa):**
  - A ISO 10243:2019 define dimensões de alojamento e código de cores para molas de compressão de seção retangular. São quatro níveis: **verde = leve, azul = média, vermelha = forte, amarela = extraforte** — [ISO 10243:2019 (iTeh)](https://standards.iteh.ai/catalog/standards/iso/ad42212b-9235-4d46-a9a7-1ed4d29d8b01/iso-10243-2019); [Springmasters – ISO 10243](https://www.springmasters.com/?p=11443).
  - **Conflito:** páginas de produto da Lesjöfors listam amarelo = leve e verde = extrapesado, o inverso da norma. Trate como exceção ou série própria e confira antes de pedir — [Lesjöfors shop](https://shop.lesjofors.com/fi/en-US/all-products/compression-springs/1-10025-5092/).
  - A Tevema mostra níveis extras (ultraleve verde-claro, branco) — [Tevema – technical data die springs](https://webshop.tevema.com/gb/blog/technical-data-die-springs).
- **Mola a gás (*gas spring*, amortecedor a gás de tampa):** não encontrei fonte nesta sessão. **[confirmar]** É um cilindro com gás (nitrogênio) pressurizado e haste, não uma mola de arame metálico. Pertence a outra cadeia de fabricação, a de componentes hidropneumáticos.

### Inferences
- Inferência: o pino elástico, o anel DIN 471/472/6799 e a mola de matriz ISO 10243 são commodities feitas por especialistas (estampagem de fita, arame de seção retangular). A Jardmolas pode ganhar margem como **revenda ou kit**, mas dificilmente fabrica com custo competitivo.
- Inferência: a mola garter de arame fino e o anel de arame redondo (DIN 7993) são viáveis com enroladeira CNC e uma operação de emenda ou dobra.

### Gaps
- Não confirmei qual norma ISO cobre o pino espiral pesado e o leve (ISO 8748 e ISO 8749?) **[confirmar]**.
- Não confirmei a norma de anel de arame redondo além da DIN 7993.
- Não achei fonte técnica sobre mola a gás.

---

## 5. Materiais e normas de arame e barra (EN 10270-1/-2/-3, EN 10089, SAE/AISI, ASTM, ABNT/NM, Belgo)

### Takeaway
Para mola enrolada a frio, o arame vem pronto em resistência: **patenteado trefilado** (EN 10270-1: SL, SM, SH, DM, DH), **temperado em óleo** (EN 10270-2: FD, TD, VD × C, CrV, SiCr) ou **inox** (EN 10270-3: 1.4310, 1.4401, 1.4568). Para mola a quente, a barra é um **aço-mola laminado a quente** temperado depois (EN 10089: 51CrV4, 54SiCr6, 52CrMoV4…). Os aços SAE 5160, 6150, 9254 e 9260 são os equivalentes americanos dessa família **[confirmar equivalências]**. A Belgo Bekaert é, segundo o próprio material, a líder nacional em arame para molas, com linha EN 10270-1.

### Cited Findings

**5.1 EN 10270-1: arame de aço não ligado, patenteado e trefilado a frio**
- A edição vigente é a **EN 10270-1:2024** (publicada em 02/2024). Ela substitui a EN 10270-1:2011+A1:2017 — [iTeh – EN 10270-1:2024](https://standards.iteh.ai/catalog/standards/cen/bb953ab0-de83-4cae-be61-564db52cb8f8/en-10270-1-2024); [iTeh – EN 10270-1:2011](https://standards.iteh.ai/catalog/standards/cen/69043a85-5585-404a-b6bc-923206695a0c/en-10270-1-2001).
- **Classes:**
  - **SL, SM, SH** = carga **estática** (*static*), com resistência baixa, média e alta.
  - **DM, DH** = carga **dinâmica** (*dynamic*), com resistência média e alta.
  - Para uso dinâmico, prefere-se microestrutura mais uniforme e patenteamento contínuo.
  - Composição (catálogo secundário): SL/SM/SH com C 0,35–1,00%, P e S ≤ 0,035%, Cu ≤ 0,20%. DM/DH com C 0,45–1,00%, P ≤ 0,020%, S ≤ 0,025%, Cu ≤ 0,12%. A microliga pode ser acordada entre as partes.
  - Fontes: [mfgrobots – EN 10270-1](https://www.mfgrobots.com/Article/material/metal/38019.html); [mfgrobots 38020](https://www.mfgrobots.com/Article/material/metal/38020.html). São páginas de catálogo, não a norma. Use a norma para compra e projeto.
- **DH:** arame não ligado de alta resistência para molas de tração, compressão ou torção sob alta carga estática ou carga dinâmica moderada — [mfgrobots](https://www.mfgrobots.com/Article/material/metal/38019.html).
- **SH vs DH:** a SH serve à carga estática alta e a DH à carga dinâmica alta. A DH exige limites mais estreitos de defeito superficial e de descarbonetação — [ficha Vinco (Scribd)](https://www.scribd.com/document/657272212/Hard-Drawn-Steel-Wire) (fonte de terceiros).
- O arame fosfatizado patenteado SM, DM, SH e DH existe no mercado, por exemplo na Sapa Acciai — [Expometals – Sapa Acciai](https://www.expometals.net/en-gb/product-detail-sapa-acciai-srl/carbon-steel-wire-for-spring-production).
- **DIN 17223-1 → EN 10270-1 [confirmar]:** a DIN 17223-1 (classes A, B, C, D) foi substituída pela EN 10270-1 (2001), com correspondência aproximada A→SL, B→SM/DM, C→SH, D→DH. Não há fonte nesta sessão. A Jardmolas ainda declara "DIN 17223", que é **nomenclatura antiga**.

**5.2 EN 10270-2: arame temperado em óleo (*oil hardened and tempered*)**
- Cobre arame temperado em óleo de aço não ligado ou ligado. Grades: **FDC, TDC, VDC** (carbono), **FDCrV, TDCrV, VDCrV** (Cr-V) e **FDSiCr, TDSiCr, VDSiCr** (Si-Cr) — [iTeh – EN 10270-2:2011](https://standards.iteh.ai/catalog/standards/cen/7bd7b3f5-b1be-43d4-a6ec-5fd6ba6efdb3/en-10270-2-2011).
- **Faixas de diâmetro (extração parcialmente ilegível):** cerca de 0,50 a 17,00 mm para FDC e 0,50 a 10,00 mm para as séries TD e VD — mesma fonte **[confirmar]**.
- **Composição extraída (aproximada):**
  - VDC: C 0,60–0,75%.
  - VDCrV: C 0,62–0,72%, Cr 0,40–0,60%, V 0,15–0,25%.
  - VDSiCr: C 0,50–0,60%, Si 1,20–1,60%, Cr 0,50–0,80%.
  - Fonte: [iTeh – EN 10270-2:2011](https://standards.iteh.ai/catalog/standards/cen/7bd7b3f5-b1be-43d4-a6ec-5fd6ba6efdb3/en-10270-2-2011) **[confirmar na tabela completa]**.
- **Significado das letras [confirmar]:** FD = carga estática, TD = dinâmica média, VD = dinâmica alta (*Ventilfeder*, mola de válvula).
- Páginas da steelestores.com sobre EN 10270-2 e EN 10089 têm valores absurdos (temperaturas de milhares de °C). **Não usar** — [steelestores – FDC](https://www.steelestores.com/grade/din-fdc-din-en-10270-2.html).

**5.3 EN 10270-3: arame inox para molas**
- Edição **EN 10270-3:2011**, que substitui a de 2001. Aços: **1.4310** (X10CrNi18-8, ~AISI 301/302), **1.4401** (X5CrNiMo17-12-2, AISI 316) e **1.4568** (X7CrNiAl17-7, ~17-7PH). Classes de resistência **NS** (normal) e **HS** (alta).
- Uma nota da norma permite o 1.4436 para mais resistência à corrosão que o 1.4401. No 1.4568, o Ni máximo pode subir até 8,30% para melhorar a conformação a frio.
- Fonte: [iTeh – EN 10270-3:2011](https://standards.iteh.ai/catalog/standards/cen/d2acca79-33ca-469a-aef3-7163ae76c3cc/en-10270-3-2011); [DIN – DIN EN 10270-3](https://www.din.de/en/getting-involved/standards-committees/fes/publications/wdc-beuth:din21:141687268).
- **1.4310 (excerto de fornecedor):** até 0,20 mm, mínimos de 2200 MPa (NS) e 2350 MPa (HS). Depois de endireitado, o arame pode perder cerca de 10% de resistência **[confirmar a fonte exata; possível Zapp]** — [Zapp – Data sheet spring wire (PDF)](https://www.zapp.com/fileadmin/_documents/Downloads/PW/informationsdatenblaetter/Data_sheet_Spring_wire.pdf).
- A Knörzer anuncia uma variante própria do 1.4568 "20% mais resistente que o 1.4310" (afirmação de marketing) — [Knörzer – 1.4568RS](https://knoerzer.eu/en/production/new-material-14568rs.html).
- **ABNT NBR 13366 (arame redondo de aço inoxidável para molas):** arame trefilado até **10,00 mm**, para molas de compressão, tração e torção, com resistência à corrosão e uso até 350 °C conforme a liga. A edição é de 05/1995, confirmada em 08/2023 — [normas.com.br – NBR 13366](https://www.normas.com.br/visualizar/abnt-nbr-nm/1929/abnt-nbr13366-arame-redondo-de-aco-inoxidavel-para-molas-especificacao); [Target – NBR 13366](https://www.target.com.br/produtos/normas-tecnicas/31864/nbr13366-arame-redondo-de-aco-inoxidavel-para-molas-especificacao).

**5.4 EN 10089: aços laminados a quente para molas temperadas e revenidas (barra e fio-máquina para mola a quente)**
- A BS EN 10089:2002 aparece como vigente na BSI, com o título "*Hot rolled steels for quenched and tempered springs – Technical delivery conditions*" — [BSI – EN 10089](https://knowledge.bsigroup.com/products/hot-rolled-steels-for-quenched-and-tempered-springs-technical-delivery-conditions).
- **51CrV4 (1.8159):** aço de alta resistência para têmpera e revenido, adequado a molas temperadas. Tratamento de referência pela EN 10089:2002: **têmpera a 850 °C e revenido a 450 °C** — [Ovako – 51CrV4](https://steelnavigator.ovako.com/steel-grades/51crv4-en100892002).
- **52CrMoV4:** usado em feixes e em molas veiculares. Também em molas formadas a quente, como molas de torção de alta solicitação, molas helicoidais e molas de tração e compressão de veículos — [Ovako](https://steelnavigator.ovako.com/steel-grades/52crmo4/); [mfgrobots – 52CrMoV4](https://www.mfgrobots.com/Article/material/metal/39012.html).
- **54SiCr6:** C 0,51–0,59%, Cr 0,50–0,80%. Temperatura do ensaio Jominy de 850 ± 5 °C — [Total Materia – 54SiCr6](https://www.totalmateria.com/en-us/material/1051805).
- **60SiCr7:** não encontrei ficha confiável. Os resultados traziam 61SiCr7 e 60SiCrV7, que são outros graus **[confirmar se 60SiCr7 consta da EN 10089 vigente]**.
- **ABNT NBR 16804 (2019):** barras laminadas a quente e fio-máquina de qualidade especial para molas helicoidais, barras de torção e estabilizadoras — [normas.com.br – NBR 16804](https://www.normas.com.br/visualizar/abnt-nbr-nm/11536/abnt-nbr16804-barras-laminadas-a-quente-e-fios-maquina-de-aco-redondos-de-qualidade-especial-para-molas-helicoidais-barras-de-torcao-e-barras-estabilizadoras-requisitos).
- **ABNT NBR 9162** (barras e fio-máquina para molas helicoidais): aparece como substituída, sem sucessora clara na listagem — [normas.com.br – CB-028 "mola"](https://www.normas.com.br/produto/normas-brasileiras-e-mercosul/pesquisar/cb-028/siderurgia/palavra/1522/1).
- **Normas Mercosul:** NM 194-2 (arame redondo de aço-carbono para molas, usos especiais) e NM 138 (barras e fio-máquina de qualidade especial para molas helicoidais) — [normas.com.br – AMN "mola"](https://www.normas.com.br/produto/normas-brasileiras-e-mercosul/pesquisar/amn/associacao-mercosul-de-normalizacao/palavra/1522/1).

**5.5 SAE/AISI: 1070, 1095, 5160, 6150, 9254, 9260**
- Não consegui buscar as composições SAE (a cota acabou). O que segue é **[confirmar]**, sem fonte nesta sessão:
  - No sistema SAE/AISI de quatro dígitos, "10xx" = aço-carbono comum e os dois últimos dígitos ≈ % de C em centésimos. Assim, **1070** ≈ 0,70% C e **1095** ≈ 0,95% C, usados em arame e fita de mola e em peças temperadas.
  - **5160** = aço ao **cromo** (não cromo-silício), típico de feixe de molas e de barras. Equivalente aproximado: 55Cr3/60Cr3.
  - **6150** = **cromo-vanádio**, ≈ 51CrV4 (1.8159).
  - **9254** = **cromo-silício**, ≈ 54SiCr6 (1.7102). É a base química usual do arame CrSi (ASTM A401).
  - **9260** = **silício-manganês**, ≈ 60Si7/61SiCr7.
- **Contradição a registrar:** um resumo de busca chamou o SAE 5160 de "cromo-silício". Pelo conhecimento geral, o 5160 é aço ao cromo **[confirmar na SAE J404]**.

**5.6 ASTM (arame americano)**
- **A228** = corda de piano (*music wire*), aço alto carbono. É o material de mola mais usado em molas pequenas.
- **A227** = trefilado duro (*hard drawn*), o mais barato, para casos em que vida, precisão e deflexão importam menos.
- **A229** = temperado em óleo (*oil tempered*), usado onde a corda de piano é cara demais ou em bitolas maiores.
- **A230** = temperado em óleo, carbono, **qualidade válvula**.
- **A231** = **Cr-V**, para tensões maiores que as dos aços alto carbono, até cerca de 220 °C.
- **A232** = Cr-V qualidade válvula.
- **A401** = **Cr-Si**, para molas muito solicitadas, de vida longa e com choque. Não resiste à corrosão nem a temperaturas acima de cerca de 248 °C (475 °F).
- **A313** = inox para mola, até cerca de 550 °F nos graus comuns.
- Fontes: [Acxess – popular spring materials](https://www.acxesspring.com/popular-materials-used-for-springs.html); [Amesweb – spring steels](https://amesweb.info/MechanicalSprings/Tables/Spring-Steels.aspx); [Lee Spring – materials](https://leespring.com/spring-materials).
- **Níveis de qualidade:** a ASTM descreve a A229 como de qualidade inferior à A1000 (*specialty spring quality*) e à A230 (válvula). A A1000 fica entre os graus comerciais (A401, A231, A229) e os de válvula (A230, A232, A877). A A877 é o Cr-Si de qualidade válvula, contraparte da A401 — [ANSI – ASTM A229-18](https://webstore.ansi.org/standards/astm/astma229a229m18); [ASTM – A1000](https://store.astm.org/a1000_a1000m-17r23.html).
- **Aviso:** os limites de temperatura variam entre fontes. Confira as revisões vigentes das normas ASTM — [Total Materia – ASTM list](https://www.totalmateria.com/articles/art26.htm).

**5.7 Belgo Bekaert Arames (ArcelorMittal + Bekaert): o que oferece para molas**
- **Folder "Mola Mecânica":**
  - Arames **"Alto Carbono Claro para mola mecânica"**, de aço conforme a **EN 10270-1**, com tabelas de resistência à tração por diâmetro para **SL, SM, SH, DM e DH**.
  - A linha mira aplicações exigentes: **automotiva, implementos agrícolas e linha branca**.
  - O folder diz que a Belgo Bekaert Arames é **líder na produção de arames para molas no país** e cita assistência técnica.
  - Fonte: [Belgo – Folder Mola Mecânica (PDF)](https://www.belgo.com.br/wp-content/uploads/2019/02/BB-015-16-FOLDER-MOLA-MECANICA-28x21cm-v6-low.pdf).
- **Arame para mola de colchão (ensacada/pocket):** bitolas de 1,30 mm (ASTM A407 "Spider"), 1,37 mm e 1,60 mm, em embalagens de 500 a 1.000 kg — [Belgo – catálogo molas de colchão](https://www.belgo.com.br/produtos/arames-e-molas-para-mola-de-colchao/catalogo_arames-para-molas-colchao/).
- **Bezinal®:** revestimento zinco-alumínio (95% Zn, 5% Al) com camada trimetálica FeZnAl. Protege os pontos terminais da mola e tem menos atrito que o galvanizado comum, o que permite enrolar mais rápido — [Belgo – Catálogo Bezinal 2025 (PDF)](https://www.belgo.com.br/wp-content/uploads/2026/01/Catalogo-Bezinal_2025.pdf).
- **Concorrente nacional:** a Gerdau publica um "Catálogo Arames Industriais". O conteúdo para molas não foi lido — [Gerdau – Catálogo Arames Industriais (PDF)](https://gsn.gerdau.com/sites/gsn_gerdau/files/downloadable_files/Catalogo-Arames-Industriais.pdf) **[confirmar]**.

### Inferences
- Inferência: a lista de aços da Jardmolas (DIN 17223 + SAE 1070, 5160, 6150, 9254) mistura duas cadeias:
  - **Arame para mola a frio:** DIN 17223 (= EN 10270-1) e 1070.
  - **Aços-liga para alta solicitação:** 5160, 6150 e 9254. Podem vir como **arame temperado em óleo** (CrV ≈ 6150 / A231; CrSi ≈ 9254 / A401) para mola a frio de alta fadiga, como dedos, molas de peneira e de válvula. Ou como **barra laminada a quente** (EN 10089 / NBR 16804) para mola a quente.
  - Isso **não prova** que a Jardmolas faz enrolamento a quente **[confirmar com a fábrica]**.
- Inferência: na comunicação comercial, atualizar "DIN 17223" para "EN 10270-1 (antiga DIN 17223-1)" passa uma imagem técnica mais atual.
- Inferência: o Bezinal da Belgo é argumento para dedos e molas agrícolas expostos à palha úmida e à vinhaça, mas há que testar a resistência do revestimento à flexão repetida **[confirmar]**.

### Gaps
- As composições SAE e as normas SAE J404/J1268 não foram confirmadas nesta sessão.
- Os nomes comerciais de todos os arames Belgo para mola (temperado em óleo? CrSi?) e as faixas de diâmetro não foram confirmados, porque o site da Belgo não abriu.
- Não confirmei a correspondência oficial DIN 17223 → EN 10270.

---

## 6. Enrolamento a frio vs a quente e máquinas

### Takeaway
O limite prático entre frio e quente fica na casa dos **~16 mm de arame**: é o teto do escopo da EN 15800 para molas de compressão enroladas a frio e o limite de capacidade citado para uma enroladeira. Acima disso entra o enrolamento a quente, com barras de ~8 a 60–65 mm, aquecimento, enrolamento e têmpera e revenido. Mesmo assim, há fornecedores que enrolam a frio até ~19 mm.

### Cited Findings
- A Lesjöfors diz que o frio limita o diâmetro máximo de arame e os índices pequenos, e que o quente é usado nos tamanhos maiores. A escolha entre frio e quente depende sobretudo do diâmetro do arame. No quente, a Lesjöfors enrola **até 65 mm** de diâmetro — [Lesjöfors – cold vs hot coiling](https://www.lesjofors.com/en/technology/insights/cold-coiling-vs-hot-coiling/) (só o trecho de busca; página bloqueada aqui).
- Uma especificação técnica de molas de compressão formadas a quente (BSI) cobre arame de **8 a 60 mm** e exclui molas especiais, como as de suspensão ferroviária e automotiva — [BSI – hot formed helical compression springs](https://knowledge.bsigroup.com/products/hot-formed-helical-compression-springs-technical-specifications). A norma pode ser a ISO 11891 **[confirmar a designação]**.
- O catálogo Fortuna (via SlideShare) mostra uma enroladeira (*spring lathe coiler*) para arame **até 16 mm em EN 10270-1 DH**. Acima de 16 mm, o arame é enrolado com apanhador manual. É um limite de **máquina**, não de norma — [Fortuna catalog (SlideShare)](https://fr.slideshare.net/SergiiPivnov/pdf-ff-catalog-2016-new-test1print).
- O escopo da EN 15800 (molas de compressão **enroladas a frio**) vai de 0,07 a 16 mm de arame — [Standards.ie – DIN EN 15800](https://shop.standards.ie/en-ie/standards/din-en-15800-2009-03-450835_saig_din_din_892001).
- A MW Components enrola a frio até 0,75" (~19 mm) — [MW Components – cold wound](https://www.mwcomponents.com/cold-wound-springs).
- O 51CrV4 tem tratamento de referência de têmpera a 850 °C e revenido a 450 °C — [Ovako](https://steelnavigator.ovako.com/steel-grades/51crv4-en100892002). É o ciclo típico da barra formada a quente, depois temperada.

### Inferences
- Inferência: no **frio**, o arame já vem com resistência (patenteado/trefilado ou temperado em óleo). A mola é enrolada e depois só passa por **alívio de tensões** (ver seção 8). No **quente** **[confirmar]**, a barra de aço-mola recozida ou laminada é aquecida até a austenitização, enrolada num mandril ainda quente, temperada em óleo e revenida. Depois vêm jateamento e pintura.
- Inferência, máquinas por tipo **[confirmar modelos]**:
  - Compressão a frio: **enroladeira CNC** (*CNC coiler*) com 2 a 12 eixos; a retífica de pontas é feita em **retificadora de pontas** de dois discos.
  - Tração: enroladeira com ferramenta de olhal ou **máquina de olhais**.
  - Torção e dedos: **máquina de torção CNC** (*torsion spring machine*) ou **conformadora de arame CNC** 3D (*CNC wire bender / wire former*).
  - Grampos e clipes pequenos: **4-slide / multislide**.
  - A quente: **forno de indução ou de gás + enroladeira a quente + tanque de têmpera + forno de revenido**.
  - Feixe de molas: tesoura, laminadora de pontas (*taper rolling*), prensa de olhal, forno, prensa de têmpera (*cambering*).
- Inferência: se o arame da Jardmolas passar de ~16 mm (molas de peneira vibratória e de cabeçalho de carreta pesadas), ela precisa de capacidade a quente ou de um parceiro **[confirmar]**.

### Gaps
- Não encontrei fonte sobre máquinas específicas (Wafios, Simplex Rapid, Itaya, Numalliance, fabricantes chineses), nem sobre os limites de diâmetro de cada tipo de máquina. A cota acabou.
- Não confirmei se a Jardmolas faz enrolamento a quente nem qual é sua faixa de diâmetro de arame.

---

## 7. Normas de projeto e tolerância (EN 13906, EN 15800, DIN, SAE/SMI, ABNT)

### Takeaway
A família europeia vigente é: **EN 13906-1/-2/-3** (cálculo de molas de compressão, tração e torção, que substituíram as DIN 2089 e afins) e **EN 15800** (tolerâncias de molas de compressão a frio, que substituiu a DIN 2095). No Brasil, as normas ABNT de molas são sobretudo de **aço e barra** e dos setores **automotivo e ferroviário**. Não encontrei uma norma brasileira geral de cálculo ou tolerância de molas helicoidais.

### Cited Findings
- **DIN EN 13906-1:2013-11** (compressão) substitui a DIN 2089-1. A DIN 2089-1 consta como retirada e "*replaced by DIN EN 13906-1:2013-11*" — [Standards.ie – DIN EN 13906-1](https://shop.standards.ie/en-ie/standards/din-en-13906-1-2013-11-420801_saig_din_din_951648); [DIN Media – DIN 2089-1](https://www.dinmedia.de/en/standard/din-2089-1/1163570).
- **DIN EN 13906-2:2013-09** (tração) substitui a DIN 2089-2 — [Standards.ie](https://shop.standards.ie/en-ie/standards/din-en-13906-2-2013-09-420805_saig_din_din_864969).
- **DIN EN 13906-3:2014-06** (torção): há conflito sobre o que substituiu (DIN 2088 ou EN 13906-3:2002) — [Standards.ie](https://shop.standards.ie/en-ie/standards/din-en-13906-3-2014-06-420813_saig_din_din_951678); [DIN](https://www.din.de/en/wdc-beuth:din21:198895053).
- **DIN 2095 (05/1973)** foi retirada e substituída pela **DIN EN 15800:2009-03** (versão alemã da EN 15800:2008) — [DIN Media – DIN 2095](https://dinmedia.de/en/standard/din-2095/681255).
- **EN 15800 (sumário):** graus de qualidade com variações admissíveis de diâmetro do arame, diâmetro da espira, comprimento livre e força a um dado comprimento, mais uma "margem de produção" — [Standards.ie – DIN EN 15800](https://shop.standards.ie/en-ie/standards/din-en-15800-2009-03-450835_saig_din_din_892001); [AFNOR – DIN EN 15800](https://www.boutique.afnor.org/en-gb/standard/din-en-15800/cylindrical-helical-springs-made-of-round-wire-quality-specifications-for-c/eu056286/159799).
- A Tevema descreve classes de tolerância da DIN 2095, por exemplo a Classe 1 com ±2% e mínimo de ±1 mm no comprimento. É material de fornecedor, não verificado contra a norma — [Tevema – DIN 2095](https://www.tevema.com/?p=44545).
- **Mola prato:** DIN EN 16983 (qualidade e dimensões, ex-DIN 2093) e DIN EN 16984 (cálculo, ex-DIN 2092) — [SPIROL](https://SPIROL.com/product/disc-springs/disc-springs-per-din-en-16983-formerly-din-2093/).
- **Mola de matriz:** ISO 10243:2019 — [iTeh](https://standards.iteh.ai/catalog/standards/iso/ad42212b-9235-4d46-a9a7-1ed4d29d8b01/iso-10243-2019).
- **Normas ABNT/NM ligadas a molas:**
  - NBR 13366 (arame inox para molas, até 10 mm).
  - NBR 16804 (barras e fio-máquina para molas helicoidais e barras de torção, 2019).
  - NBR 15989 (molas helicoidais de suspensão automotiva: métodos de ensaio e requisitos mínimos para certificação, confirmada em 03/2024).
  - NBR 15663 (mola helicoidal para suspensão de truque de vagão ferroviário, 01/2023).
  - NBR 12794 (mola helicoidal de compressão para veículo ferroviário).
  - NBR 12792 (dimensões dessas molas, **cancelada**).
  - NBR 8567 (feixe de molas rodoviário, **cancelada** em 2012).
  - NM 194-2, NM 138, NM 175.
  - Fontes: [NBR 15989](https://www.normas.com.br/visualizar/abnt-nbr-nm/31153/abnt-nbr15989-veiculos-rodoviarios-automotores-molas-helicoidais-para-suspensao-automotivas-metodos-de-ensaio-e-requisitos-minimos-de-qualidade); [NBR 15663](https://www.normas.com.br/visualizar/abnt-nbr-nm/28049/abnt-nbr15663-vagao-ferroviario-mola-helicoidal-para-suspensao-de-truque-requisitos); [NBR 12792](https://normas.com.br/visualizar/abnt-nbr-nm/2546/abnt-nbr12792-mola-helicoidal-de-compressao-para-veiculo-ferroviario-determinacao-dos-caracteristicos-dimensionais); demais links na seção 5. O status vem de sites revendedores de normas e deve ser conferido no ABNT Catálogo.

### Inferences
- Inferência: para cotação de mola de compressão a frio, a equipe pode pedir ao cliente o **grau de qualidade EN 15800** (1, 2 ou 3) em vez de tolerância "livre" **[confirmar os números de grau]**. Isso padroniza a conversa com OEMs europeus (Pöttinger, Kuhn, Kverneland) e as multinacionais instaladas no Brasil.
- Inferência: em mola de tração e de torção, as tolerâncias DIN antigas (DIN 2097 para tração, DIN 2194 para torção) ainda aparecem em desenhos **[confirmar designações e status]**.

### Gaps
- Não confirmei o status atual nem o conteúdo das DIN 2096 (molas de compressão a quente), DIN 2097 (tolerâncias de mola de tração) e DIN 2194 (torção) **[confirmar]**.
- Não encontrei fonte sobre o SAE HS-795 (*SAE Spring Design Manual*) nem sobre o *Handbook of Spring Design* do SMI (Spring Manufacturers Institute) **[confirmar edição vigente]**.
- Não encontrei norma ABNT geral de cálculo ou tolerância de molas helicoidais de arame (equivalente à EN 13906 ou EN 15800). Pelo que apareceu, ela não existe, mas isso precisa ser confirmado no ABNT Catálogo.

---

## 8. Etapas de processo e ensaios de qualidade

### Takeaway
O fluxo típico de mola a frio é:

**enrolar ou conformar → aliviar tensões → retificar pontas (compressão) → jatear com granalha → 2º alívio → pré-assentar (*presetting*) → proteção superficial → ensaio.**

As temperaturas de alívio dependem do arame. Para o CrSi, a referência de fornecedor é ~400 °C por 30 min depois de enrolar e ~250 °C por 30 min depois do jateamento. Mola de alta resistência **zincada eletroliticamente precisa de desidrogenação** em poucas horas.

### Cited Findings
- **Alívio de tensões (*stress relief*)**, arame CrSi temperado em óleo (Gibbs): **~400 °C (750 °F) por 30 min** logo depois de enrolar. Depois do jateamento, segundo ciclo a **~250 °C (480 °F) por 30 min**. A Gibbs indica esse arame para molas sob choque forte e calor, e diz que o CrSi aguenta ~50 °F a mais que o CrV. Faixa de bitolas na ficha antiga: 0,018" a 0,625" — [Gibbs – chrome silicon commercial wire (PDF)](https://www.gibbswire.com/pdf/chrome-silicon-comm-wire.pdf); [Gibbs – Oil Temp Commercial datasheet (PDF)](https://www.gibbswire.com/wp-content/uploads/2025/08/Gibbs-Datasheet-Wire-7-Oil-Temp-Commercial.pdf).
- **Jateamento (*shot peening*):** os dedos Super-C da Kverneland são jateados — [Kverneland](https://flippingbook.kverneland.com/view/323669715/8/). Numa análise de falha prematura, a origem da trinca estava num ponto onde a camada jateada tinha se desgastado (o material estava livre de inclusões). Isso mostra a função protetora do jateamento contra a fadiga — resumo de busca sobre estudos de falha ([Scribd – Failure analysis spring](https://www.scribd.com/document/553313493/Failure-analysis-spring); [KTU](https://epubl.ktu.edu/object/elaba:19497848/19497848.pdf)) **[confirmar a qual das fontes pertence o caso]**.
- **Retífica de pontas:** a ponta fechada e esmerilhada faz a mola ficar em pé com menos flambagem — [Century Spring](https://centuryspring.com/resources/spring-end-types).
- **Revestimentos:**
  - Arame **fosfatizado** (Sapa Acciai) — [Expometals](https://www.expometals.net/en-gb/product-detail-sapa-acciai-srl/carbon-steel-wire-for-spring-production).
  - Arame com **Bezinal ZnAl**: menos atrito no enrolamento e proteção das pontas — [Belgo – Bezinal](https://www.belgo.com.br/wp-content/uploads/2026/01/Catalogo-Bezinal_2025.pdf).
  - **Pintura** de dentes de ancinho contra ferrugem — [Farm & Fleet](https://www.farmandfleet.com/products/333249-herschel-wheel-rake-tooth-ot1a.html).
- **Fragilização por hidrogênio (*hydrogen embrittlement*) e desidrogenação (*baking*):**
  - **ASTM B850:** o tratamento deve começar o quanto antes, **de preferência em até 1 h e no máximo 3 h** depois da eletrodeposição, e antes de qualquer retífica. O bake **reduz**, mas não elimina, o risco — [ASTM B850 (Scribd)](https://www.scribd.com/document/447067734/ASTM-B850); [finishing.com](https://www.finishing.com/12/16p3.shtml).
  - **ASTM B633** (zinco eletrolítico), citada no finishing.com: peças com **≥ 1200 MPa** devem ser assadas a **190 °C por ≥ 3 h, em até 4 h** depois da deposição. A prática comum é "375 ± 25 °F por 3 h mínimo em até 4 h", e molas costumam ser assadas por mais tempo — [finishing.com](https://www.finishing.com/12/16p3.shtml); [Products Finishing – Hydrogen Embrittlement Again](https://pfonline.com/articles/hydrogen-embrittlement-again).
  - Dado anedótico (finishing.com, resumo de artigo): o bake em até 30 min sempre preveniu a fragilização, e depois de 24 h "não adiantava". É de segunda mão e não verificado.
- **Ensaios previstos em norma:**
  - A EN 15800 fixa tolerâncias de força a um comprimento dado, de comprimento livre, de diâmetro do arame e de diâmetro da espira. Isso implica **ensaio carga × comprimento** e **dimensional** — [Standards.ie – EN 15800](https://shop.standards.ie/en-ie/standards/din-en-15800-2009-03-450835_saig_din_din_892001).
  - A NBR 15989 define métodos de ensaio e requisitos mínimos de molas de suspensão automotiva — [normas.com.br](https://www.normas.com.br/visualizar/abnt-nbr-nm/31153/abnt-nbr15989-veiculos-rodoviarios-automotores-molas-helicoidais-para-suspensao-automotivas-metodos-de-ensaio-e-requisitos-minimos-de-qualidade).

### Inferences
- Inferência, finalidade de cada etapa **[confirmar valores]**:
  - **Alívio de tensões:** remove as tensões residuais do enrolamento e estabiliza as dimensões. Em arame patenteado, também eleva o limite elástico.
  - **Têmpera e revenido:** só na mola a quente ou em fita e barra. Dá a dureza e a tenacidade finais.
  - **Jateamento:** cria tensão residual de compressão na superfície e retarda a nucleação de trinca por fadiga.
  - **Pré-assentamento (*presetting/setting*):** comprimir a mola até o bloco, ou além da carga de trabalho, para provocar a deformação permanente na fábrica. Assim a mola não "senta" em serviço e pode trabalhar com tensão maior.
  - **Retífica de pontas:** dá perpendicularidade e apoio.
  - **Fosfato + óleo:** proteção temporária e base para pintura.
  - **Pintura epóxi a pó:** proteção de campo, bom para o agro.
  - **Zinco eletrolítico:** proteção com risco de H₂, que obriga a assar.
- Inferência: como a maioria dos arames de mola passa de 1200 MPa de resistência (o 1.4310 fino chega a 2200 MPa, seção 5.3), a regra de desidrogenação da B633 vale para quase toda mola zincada. A Jardmolas deve exigir isso por escrito do galvanizador terceiro **[confirmar]**.
- Inferência, ensaios típicos de uma fábrica média **[confirmar]**:
  - **Internos:** carga × deflexão em máquina de ensaio de molas; dimensional (paquímetro, projetor, gabarito); dureza (Rockwell/Vickers); perpendicularidade.
  - **Terceirizados ou ocasionais:** fadiga em pulsador; névoa salina (ISO 9227 / ASTM B117); análise química e metalografia (descarbonetação, inclusões).

### Gaps
- Não encontrei fonte sobre temperaturas de alívio de tensões para corda de piano, EN 10270-1 e inox, nem sobre parâmetros de pré-assentamento.
- Não confirmei a janela de desidrogenação da ISO 4042.
- Não encontrei normas de névoa salina e de intensidade de jateamento (Almen) nesta sessão **[confirmar ISO 9227, ASTM B117, SAE J442/J443]**.

---

## 9. Modos de falha e diagnóstico

### Takeaway
A maioria das quebras de mola é **fadiga**, com origem na superfície ou logo abaixo dela. Os iniciadores típicos são inclusão não metálica, camada descarbonetada, pite de corrosão, risco ou marca de ferramenta, perda da camada jateada e raio apertado de gancho ou dobra. "Sentar" (perda de altura) indica sobretensão ou alívio e pré-assentamento ruins.

### Cited Findings
- **Inclusões:** num caso do IST (Institute of Spring Technology), uma mola falhou por fadiga a partir de uma inclusão logo abaixo da superfície. O IST observa que é impossível remover todas as inclusões, por melhor que seja o arame — [IST – case study](https://ist.org.uk/?p=2145). Outro estudo atribui a falha precoce de uma mola helicoidal a inclusões não metálicas que concentram tensão — resumo de busca ([Endurance – QFR 1088 (PDF)](https://vcportal.endurancegroup.com/data/qfrdoc/1088_Outflow_After.pdf); [Springer](https://springerlink.bibliotecabuap.elogim.com/10.1007/978-981-19-6945-4_79)) **[confirmar a fonte exata]**.
- **Descarbonetação:**
  - Está entre as causas reconhecidas de fadiga em molas de suspensão, ao lado de defeito de matéria-prima, imperfeição superficial, tratamento térmico inadequado e corrosão.
  - Num laudo ferroviário, a camada descarbonetada nas espiras tinha **0,114 a 0,158 mm**.
  - Fonte: [IRIMEE – Rolling stock failure analysis (PDF)](https://rskr.irimee.in/sites/default/files/Rolling%20stock%20FAILURE%20ANALYSIS-case%20study%20of%20material%20failure.pdf).
  - A classe DH da EN 10270-1 tem limites mais estreitos de descarbonetação e de defeito superficial que a SH — [Vinco (Scribd)](https://www.scribd.com/document/657272212/Hard-Drawn-Steel-Wire).
- **Corrosão e fadiga por corrosão:** numa mola helicoidal com revestimento danificado, os **pites de corrosão** foram os pontos de início da trinca. O laudo ferroviário também trata pites como concentradores de tensão e núcleos de fadiga — [IRIMEE](https://rskr.irimee.in/sites/default/files/Rolling%20stock%20FAILURE%20ANALYSIS-case%20study%20of%20material%20failure.pdf).
- **Danos superficiais e marcas:** mossas, entalhes e riscos são fatores que limitam a vida — [IRIMEE](https://rskr.irimee.in/sites/default/files/Rolling%20stock%20FAILURE%20ANALYSIS-case%20study%20of%20material%20failure.pdf). Nenhuma fonte tratou "marca de ferramenta" (*tool mark*) com esse nome.
- **Perda da camada jateada:** caso de falha prematura com origem no ponto onde o jateamento tinha se desgastado (ver seção 8).
- **Concentração de tensão em gancho e dobra:** quanto menor o olhal de máquina, mais fechado o raio de transição e maior a concentração de tensão. O gancho de máquina resiste mais que o gancho cruzado central por ter raio menos severo — [Acxess Spring – hook types](https://www.acxesspring.com/tension-extension-spring-hook-types.html).
- **Fragilização por hidrogênio:** o risco existe em molas de alta resistência eletrodepositadas. O bake reduz, mas não elimina — [ASTM B850 (Scribd)](https://www.scribd.com/document/447067734/ASTM-B850); [finishing.com](https://www.finishing.com/12/16p3.shtml).
- **Dedo montado ao contrário:** aumenta a quebra no espalhador — [Ford Distributing](https://forddistributing.com/tedder-tine.html). É uma falha de **aplicação**, não de fabricação.

### Inferences
- Inferência, roteiro de diagnóstico para pós-venda e engenharia **[confirmar com metalurgista]**:
  1. **Onde quebrou?** No gancho ou na dobra → concentração de tensão (raio, marca de ferramenta). No meio da espira → material, superfície ou sobretensão. Na transição da ponta → espira morta e de apoio.
  2. **Como é a fratura?** Fadiga mostra uma origem pontual, marcas de praia (*beach marks*) e uma zona final pequena. A sobrecarga mostra fratura áspera, eventualmente com estricção. A fragilização por hidrogênio costuma aparecer pouco depois da zincagem, sem carga cíclica e com fratura intergranular, o que exige MEV **[confirmar]**.
  3. **O que há na origem?** Pite (corrosão), inclusão (metalografia), camada clara sem carbono (descarbonetação), risco ou mossa (manuseio e ferramenta).
  4. **"Sentou" sem quebrar?** Tensão de trabalho acima do limite, falta de pré-assentamento ou temperatura alta demais para o aço (ver os limites ASTM da seção 5.6).
  5. **No campo agro:** montagem invertida, impacto com pedra ou toco, corrosão por umidade, vinhaça e fertilizante.
- Inferência: para os dedos de palha de cana, os riscos mais prováveis são fadiga na transição espira–perna, corrosão sob pintura lascada e impacto. O jateamento, a pintura e o raio generoso na transição são as defesas.

### Gaps
- Não encontrei fonte sobre falhas específicas de dedos de enleirador de cana, nem estatísticas de modos de falha em molas agrícolas.
- Não consegui ler a página do IST com detalhe, nem guias completos de análise de falha do SMI.

---

## 10. Inferência: o que uma fábrica pequena ou média como a Jardmolas costuma fazer internamente e o que terceiriza

### Takeaway
**Inferência (toda esta seção):** pelo perfil declarado (arame Belgo, DIN 17223/EN 10270-1, SAE 1070, 5160, 6150, 9254; compressão, tração, torção, formas de arame e dedos), o núcleo interno provável é **enrolamento e conformação a frio de arame + alívio de tensões + acabamento simples + ensaio de carga**. Galvanoplastia, molas de fita e chapa e itens padronizados costumam ficar com terceiros ou na revenda.

### Cited Findings
- A Belgo vende arame EN 10270-1 (SL a DH) para implementos agrícolas, o que confirma a cadeia "arame pronto → mola a frio" — [Belgo – Folder Mola Mecânica](https://www.belgo.com.br/wp-content/uploads/2019/02/BB-015-16-FOLDER-MOLA-MECANICA-28x21cm-v6-low.pdf).
- A Darvig Molas é um fabricante nacional de molas e peças de arame para vários segmentos industriais, ativa desde 1984. Serve de referência de par brasileiro, com conteúdo não detalhado — [Catálogo Darvig (PDF)](https://mfygixyrefykhfafisif.supabase.co/storage/v1/object/public/catalogo/catalogo-darvig.pdf).
- O enrolamento a frio cobre na prática até ~16 a 19 mm de arame, e o a quente vai de 8 a 65 mm (seção 6) — [Fortuna (SlideShare)](https://fr.slideshare.net/SergiiPivnov/pdf-ff-catalog-2016-new-test1print); [MW Components](https://www.mwcomponents.com/cold-wound-springs); [Lesjöfors](https://www.lesjofors.com/en/technology/insights/cold-coiling-vs-hot-coiling/).
- Não consegui acessar o site da Jardmolas (`jardmolas.com.br` não resolve neste ambiente) e a busca não trouxe nenhum resultado sobre a empresa.

### Inferences
- **Provavelmente interno:**
  - Molas de compressão, tração e torção a frio, de arame fino a médio (faixa a confirmar, talvez até ~12–16 mm).
  - Dedos e dentes de torção dupla.
  - Formas de arame (ganchos, grampos, pinos-trava, alças).
  - Mola garter e anéis de arame.
  - Alívio de tensões em forno.
  - Retífica de pontas.
  - Pintura (talvez a pó).
  - Ensaio de carga e dimensional.
- **Possivelmente interno, a confirmar:**
  - Jateamento (essencial para dedo de alta fadiga; uma cabine de granalha é investimento acessível).
  - Enrolamento a quente para molas de peneira e de cabeçalho pesadas. Os aços 5160, 6150 e 9254 declarados permitem, mas não provam, essa capacidade.
- **Provavelmente terceirizado:**
  - Zincagem e galvanoplastia, com desidrogenação. É um processo químico regulado ambientalmente.
  - Fosfatização em linha.
  - Névoa salina e fadiga certificada em laboratório.
  - Metalografia e análise química.
  - Feixe de molas.
  - Molas de fita (força constante, espiral de potência).
- **Provavelmente revenda (se oferecer):** molas de matriz ISO 10243, mola prato DIN EN 16983, mola ondulada, pino elástico ISO 8752/8750, anel elástico DIN 471/472/6799, mola a gás.

### Gaps
- Faltam a faixa real de diâmetro de arame, o parque de máquinas, a existência de forno de têmpera, de enrolamento a quente e de jateamento, e a lista de OEMs atendidos pela Jardmolas. Só a fábrica pode confirmar.

---

## 11. Tabela-síntese: como classificar qualquer mola pedida

### Takeaway
A tabela abaixo deixa a equipe de vendas e engenharia enquadrar o pedido em uma das 17 famílias. A coluna "Fonte" aponta a referência principal. Os dados das colunas "agro" e "indústria" vêm em parte do briefing do cliente e em parte das fontes. O que é inferência está marcado (Inf.).

### Cited Findings

| Tipo de mola (PT / EN) | Variantes | Como funciona | Materiais típicos | Processo (frio/quente) | Aplicações agro | Aplicações indústria | Fonte |
|---|---|---|---|---|---|---|---|
| Mola helicoidal de compressão / *compression spring* | Cilíndrica, cônica, barril, ampulheta, passo variável [confirmar defs]; pontas abertas, fechadas, fechadas e esmerilhadas, duplo fechamento | Resiste a ser comprimida; força ≈ constante × deflexão até o bloco | EN 10270-1 (SL a DH), EN 10270-2 (FD, TD, VD), inox EN 10270-3; a quente: EN 10089 (51CrV4, 54SiCr6) | Frio até ~16 mm (EN 15800); quente ~8 a 65 mm | Peneira vibratória, cabeçalho e engate de carreta, implementos (briefing) | Válvulas, máquinas, prensas, ferroviário (NBR 12794), automotivo (NBR 15989) | [Century](https://centuryspring.com/resources/spring-end-types); [EN 15800](https://shop.standards.ie/en-ie/standards/din-en-15800-2009-03-450835_saig_din_din_892001); [Lesjöfors](https://www.lesjofors.com/en/technology/insights/cold-coiling-vs-hot-coiling/) |
| Mola de tração (extensão) / *extension spring* | Olhal de máquina, olhal cruzado, gancho lateral, gancho estendido, meia volta, volta inteira, inserto rosqueado [confirmar] | Resiste a ser puxada; F = tensão inicial + constante × deflexão | EN 10270-1, ASTM A228/A229, inox | Frio | Enfardadora, ancinho, pedais e alavancas de implemento (briefing; Inf.) | Portas, balanças, eletrodomésticos (Inf.) | [Acxess hooks](https://www.acxesspring.com/tension-extension-spring-hook-types.html); [Century](https://www.centuryspring.com/extension-springs); [EN 13906-2](https://shop.standards.ie/en-ie/standards/din-en-13906-2-2013-09-420805_saig_din_din_864969) |
| Mola de torção / *torsion spring* | Simples, dupla; perna reta, curva, em gancho (Inf.) | Momento aplicado nas pernas; o arame trabalha em flexão [confirmar] | EN 10270-1, EN 10270-2 (CrV, CrSi), inox | Frio (máquina de torção CNC) | Ancinho, recolhedores, tampas (Inf.) | Dobradiças, prendedores, mecanismos de retorno (Inf.) | [EN 13906-3](https://shop.standards.ie/en-ie/standards/din-en-13906-3-2014-06-420813_saig_din_din_951678) |
| Dedo / dente de mola / *spring tine* (forma de arame de torção) | Torção dupla com duas pernas, torção simples com perna longa, dente-mola de cultivador | Espiras armazenam energia; a perna flexiona ao tocar palha ou feno e volta | Aço-mola jateado (Kverneland: 10 mm, espira de 80 mm); "Super C" (Pöttinger); CrSi/CrV (Inf.) | Frio + alívio + jateamento + pintura | **Enleirador e desenleirador de palha de cana**, ancinho e espalhador de feno, recolhedor de enfardadora e de amendoim (briefing) | — | [Kverneland](https://flippingbook.kverneland.com/view/323669715/8/); [Pöttinger](https://www.poettinger.at/en_in/produkte/detailtexthl/HIVA/th/2/poettinger-tines); [Justia 56/400](https://patents.justia.com/patents-by-us-classification/56/400) |
| Forma de arame / *wire form* | Grampos, clipes, ganchos, pinos-trava, alças, suportes, anéis de arame (DIN 7993) | Peça dobrada em 2D ou 3D que trabalha por flexão ou fixação | EN 10270-1, aço baixo carbono (peças não-mola), inox | Frio (conformadora CNC, 4-slide) | Travas de implemento, suportes de mangueira (Inf.) | Fixação, eletrodomésticos, automotivo (Inf.) | [Fasten.it DIN 7993](https://www.fasten.it/pt/search/suppliers/287) |
| Mola para matriz / *die spring* | ISO 10243: verde (leve), azul (média), vermelha (forte), amarela (extraforte) | Compressão de seção retangular, alta carga em espaço pequeno | Aço-liga temperado [confirmar] | Frio (arame retangular) + revenido [confirmar] | — | Ferramentas de estampar e prensas | [ISO 10243](https://standards.iteh.ai/catalog/standards/iso/ad42212b-9235-4d46-a9a7-1ed4d29d8b01/iso-10243-2019); [Springmasters](https://www.springmasters.com/?p=11443) |
| Mola de válvula / *valve spring* | Cilíndrica, passo variável [confirmar] | Compressão de altíssima fadiga | ASTM A230, A232, A877; EN 10270-2 grau VD | Frio + jateamento + pré-assentamento (Inf.) | Motores de trator e de bomba (Inf.) | Motores e compressores | [ANSI A229](https://webstore.ansi.org/standards/astm/astma229a229m18); [EN 10270-2](https://standards.iteh.ai/catalog/standards/cen/7bd7b3f5-b1be-43d4-a6ec-5fd6ba6efdb3/en-10270-2-2011) |
| Mola garter / mola de retentor / *garter spring* | Tração (fecha) ou compressão (abre); emenda por ponta reduzida, gancho e olhal, olhais | Helicoidal fechada em anel que aperta ou expande radialmente | Arame fino EN 10270-1, inox | Frio + emenda | Retentores de redutores e eixos (Inf.) | Vedações de óleo, eixos | [Wikipedia](https://en.wikipedia.org/wiki/Garter_spring); [Katy](https://www.steel-technology.com/products/katy-spring-manufacturing-inc/garter-springs) |
| Feixe de molas / mola parabólica / *leaf spring* | Convencional multilâmina, parabólica de espessura variável, híbrida aço-fibra | Lâminas em flexão como viga | 52CrMoV4, SAE 5160 [confirmar], EN 10089 | Quente (corte, conformação, têmpera, revenido) | Carretas e reboques agrícolas (Inf.) | Caminhões e implementos rodoviários | [UFMG](https://repositorio.ufmg.br/bitstream/1843/51810/3/DISSERTA%C3%87%C3%83O_LEONARDOLELISDIAS_FINAL.pdf); [Ovako](https://steelnavigator.ovako.com/steel-grades/52crmo4/) |
| Mola prato / Belleville / *disc spring* | Séries A, B, C (ho/t ≈ 0,4, 0,75, 1,3); Grupos 1 e 2 por espessura; empilhamento | Cone de chapa que achata; curva dependente de ho/t | Aço-mola em chapa [confirmar grau] | Estampagem + têmpera | Embreagens e freios de máquinas (Inf.) | Pré-carga de parafusos, válvulas, ferramentas | [SPIROL](https://SPIROL.com/product/disc-springs/disc-springs-per-din-en-16983-formerly-din-2093/) |
| Mola ondulada / *wave spring* | Uma volta, multivoltas *crest-to-crest*, aninhada, entrelaçada, com ponta de calço | Fio chato ondulado; até 50% menos espaço axial | Aço carbono ou inox em fio chato [confirmar] | Frio (enrolamento de fio chato) | Rolamentos de implementos (Inf.) | Pré-carga de rolamentos, vedações | [Smalley](https://www.smalley.com/wave-springs/crest-crest) |
| Mola espiral / de potência / de relógio / *power spring* | Com ou sem caixa; braço em gancho | Fita em espiral plana que dá torque rotativo variável | Fita de aço carbono ou inox [confirmar] | Frio (fita) | Enroladores de mangueira e cabo (Inf.) | Retratores, relógios, mecanismos | [Fastener Engineering](https://fastenerengineering.com/what-are-constant-force-springs/) |
| Mola de força constante / *constant force spring* | Linear (*Neg'ator*), de torque constante | Fita pré-tensionada que desenrola com força quase constante | Fita de aço inox ou carbono [confirmar] | Frio (fita pré-tensionada) | — | Contrapesos, retráteis, cortinas | [MW Components](https://www.mwcomponents.com/constant-force-springs) |
| Barra de torção / *torsion bar* | Reta com cabeças estriadas ou sextavadas (Inf.) | Barra que trabalha em torção pura | NBR 16804 / NM 175; 52CrMoV4 | Quente + têmpera | Suspensões de máquinas (Inf.) | Automotivo (estabilizadora) | [NBR 16804](https://www.normas.com.br/visualizar/abnt-nbr-nm/11536/abnt-nbr16804-barras-laminadas-a-quente-e-fios-maquina-de-aco-redondos-de-qualidade-especial-para-molas-helicoidais-barras-de-torcao-e-barras-estabilizadoras-requisitos) |
| Pino elástico / *spring pin* | Fendido (ISO 8752 pesado, ISO 13337 leve, DIN 1481); espiral (ISO 8750, DIN 7343) | Tubo de aço-mola que comprime radialmente ao entrar no furo | Aço-mola (enferruja no úmido) ou inox | Frio (enrolamento e corte de fita) + têmpera [confirmar] | Fixação de pinos, eixos e articulações de implemento (Inf.) | Montagem geral | [SPIROL](https://cdn.shopify.com/s/files/1/0492/3631/2223/files/SPIROL-Slotted-Spring-Pins-us.pdf); [Torqbolt](https://torqbolt.com/slotted-pin-manufacturers-suppliers-india) |
| Anel elástico / *retaining ring* (Seeger) | DIN 471 (eixo), DIN 472 (furo), DIN 6799 (arruela-trava), DIN 7993 (arame redondo) | Anel que trava axialmente em ranhura | Aço-mola (estampado), arame de mola | Estampagem + têmpera, ou arame a frio | Rolamentos e eixos de implementos (Inf.) | Universal | [Seeger-Orbis](https://www.seeger-orbis.com/products/retaining-rings/seeger-rings-to-din-471-472); [Fabory](https://fabory.com/en_GB/c/011008) |
| Mola a gás / *gas spring* | Pistão-haste, travável [confirmar] | Gás pressurizado num cilindro; **não é mola de arame** | — | Não se aplica (componente hidropneumático) | Tampas de cabine e capôs (Inf.) | Tampas, móveis | Sem fonte nesta sessão **[confirmar]** |

### Inferences
- Inferência, checklist de classificação para a equipe (perguntas ao cliente, nesta ordem):
  1. Sentido da carga: empurra, puxa ou gira.
  2. Seção: arame redondo, arame retangular, fita ou chapa.
  3. Diâmetro do arame ou da barra. Acima de ~16 mm, provável mola a quente.
  4. Ponta ou gancho.
  5. Carga estática ou dinâmica e número de ciclos. Isso define a classe SH vs DH, ou carbono vs CrSi.
  6. Ambiente: umidade, vinhaça, temperatura. Isso define inox, pintura ou zinco com desidrogenação.
  7. Norma de tolerância (EN 15800, grau) e desenho ou amostra.
- Inferência: pedidos de mola de matriz, mola prato, mola ondulada, pino elástico, anel elástico e mola a gás devem ser marcados como **"fora do núcleo"** no CRM, para decidir entre revenda e indicação.

### Gaps
- Não confirmei, para a Jardmolas, as linhas da tabela que entram de fato no portfólio, nem os diâmetros máximos.
- Não confirmei as aplicações agro marcadas "Inf.". Sairiam de catálogos de OEMs brasileiros (Baldan, Jumil, Tatu Marchesan, KLR/DMB e outros fabricantes de enleiradores de cana) **[confirmar]**, que não foram pesquisados por falta de cota.
