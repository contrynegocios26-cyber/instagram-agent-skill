# Revisão técnica do site jardmolas.com.br

Data: 10/11/2026. Foram lidas as 34 páginas do site (menu, produtos, matéria-prima, projetos, empresa). Abaixo, o que está tecnicamente errado ou arriscado, por ordem de gravidade, com o texto corrigido pronto para substituir. As correções de liga usam o boletim técnico do fabricante do Inconel X-750 (Special Metals), lido no original.

Nada foi alterado no site — este documento é a lista de trabalho para quem administra as páginas.

## 1. Erros técnicos (corrigir primeiro)

### 1.1 Temperatura máxima das molas de válvula — página "Molas para Válvulas de Retenção Dupla Portinhola"

**Como está:** tabela com "Temperatura máxima: Aço Inox 302/304 — 550 °C; Inconel — 980 °C".

**Problema:** esses não são limites de trabalho de mola. Mola perde carga (relaxa) muito antes de o material oxidar. Os 980 °C correspondem à resistência à oxidação do Inconel X-750 (1800 °F no boletim do fabricante); como mola, o mesmo boletim limita a liga a 371, 538 ou 649 °C conforme o arame e o tratamento térmico. Inox austenítico em mola trabalha até cerca de 250 °C. Um engenheiro de válvulas percebe o erro na hora, e é exatamente o cliente que a página quer atrair.

**Texto corrigido:**

| Característica | Inox 302/304 | Inox 316 | Inconel X-750 |
|---|---|---|---|
| Temperatura de trabalho da mola | até cerca de 250 °C | até cerca de 250 °C | até 370 °C, 540 °C ou 650 °C, conforme a têmpera do arame e o tratamento térmico |
| Resistência à corrosão | boa em ambientes úmidos | melhor em presença de cloretos | alta; aceito para molas em serviço ácido (NACE MR0175) com dureza controlada |
| Magnetismo | levemente magnético depois de trefilado | praticamente não magnético | não magnético |

> "Informe a temperatura de serviço: no Inconel X-750 ela define a têmpera do arame e o tratamento térmico da mola."

### 1.2 "Inconel" sem dizer qual — várias páginas

**Como está:** "aço inoxidável 302, 304 e Inconel".

**Problema:** Inconel é uma família (600, 625, 718, X-750…) com propriedades muito diferentes. Para mola de válvula, a liga é o X-750.

**Texto corrigido:** "aço inoxidável 302, 304 e 316 e Inconel X-750 (UNS N07750)".

### 1.3 "Não magnético (304)" — mesma página

**Problema:** o arame de inox 302/304 para mola fica levemente magnético por causa do trabalho a frio da trefila. Cliente que testar com ímã vai achar que recebeu material errado.

**Texto corrigido:** "Inox 302/304: levemente magnético depois de trefilado (característica normal do arame para molas). Inconel X-750: não magnético."

### 1.4 "Garantir o fechamento hermético das válvulas" — mesma página

**Problema:** a mola não veda. Ela fecha as portinholas rapidamente antes de o fluxo inverter, o que evita o golpe de aríete; a vedação é feita pela sede da válvula.

**Texto corrigido:** "A mola de torção fecha as portinholas assim que o fluxo diminui, antes da inversão — é o que evita o golpe de aríete e protege bombas e tubulação."

### 1.5 Classificação dos aços — página "Matéria Prima"

| Como está | Problema | Texto corrigido |
|---|---|---|
| "SAE 9254 (Aço C/Camada de Cromo Silício)" | Não existe "camada": cromo e silício são elementos da liga | "SAE 9254 — aço-liga ao cromo-silício" |
| SAE 9254: "resistência à fadiga e à deformação em altas temperaturas" | Exagero: é aço para temperatura moderada | "Excelente resistência à fadiga e ao choque; mantém a carga até cerca de 250 °C" |
| SAE 5160: "Aço liga de médio carbono e cromo" | O 5160 tem 0,56–0,64% de carbono: é alto carbono | "SAE 5160 — aço-liga ao cromo, alto carbono" |
| SAE 6150: "Aço liga de alto carbono com cromo e vanádio" | O 6150 tem cerca de 0,50% de carbono: é médio carbono | "SAE 6150 — aço-liga cromo-vanádio, médio carbono" |
| "DIN 17223 – Classe A, B, C, D" | Norma antiga, substituída pela EN 10270-1; o certificado do arame vem pela norma nova | "Arame patenteado EN 10270-1, classes SL, SM, SH (estáticas) e DM, DH (dinâmicas) — equivalente à antiga DIN 17223" |

### 1.6 "Fabricação conforme ISO 9001" — páginas "Molas para Atuadores" (agrícola e industrial)

**Como está:** "Fabricação conforme ISO 9001" e "Processos de fabricação certificados ISO 9001".

**Problema:** só pode ficar se a Jardmolas tiver certificado ISO 9001 vigente em seu nome. Se não tiver, é afirmação falsa em material de venda — o tipo de coisa que derruba uma homologação em cliente industrial e gera problema com cliente e com órgão de defesa do consumidor. **Confirmar hoje.**

**Se houver certificado:** "Sistema de gestão certificado ISO 9001:2015 (certificado nº …, válido até …)". **Se não houver:** retirar as duas frases.

### 1.7 "Certificado Belgo Arames" como certificação da Jardmolas — "Matéria Prima" e home

**Como está:** "Orgulhamo-nos de possuir o certificado Belgo Arames, um selo de qualidade reconhecido internacionalmente."

**Problema:** o certificado é do fornecedor do arame; ele atesta a matéria-prima, não o sistema da Jardmolas.

**Texto corrigido:** "Trabalhamos com arame da Belgo Arames, fornecido com certificado de qualidade por lote — composição química e propriedades mecânicas rastreáveis até a corrida do aço."

### 1.8 "Nanotecnologia" e "novos metais e compósitos" — páginas de molas de compressão

**Como está:** "O uso de ligas especiais, nanotecnologia e simulação computacional…"; "Incorporando nanoestruturas para melhorar a resistência e elasticidade"; "Ligação de novos metais e compósitos".

**Problema:** não são processos de uma fábrica de molas; texto genérico que tira a credibilidade do restante. Na página agrícola, a frase "utilizadas em suspensões de veículos, válvulas, brinquedos, dispositivos médicos" também não tem relação com implemento.

**Texto corrigido:** "Cada mola é calculada para a carga e o curso da aplicação, enrolada em máquina CNC, tratada termicamente e ensaiada em carga. Materiais: aço carbono patenteado, cromo-silício, cromo-vanádio e inox."

### 1.9 Válvula de segurança — página "Molas para Válvula de Segurança Industriais"

| Como está | Problema | Texto corrigido |
|---|---|---|
| "Ajustadas para uma pressão específica de abertura" | Quem é ajustada é a válvula; cada mola cobre uma faixa de pressão de ajuste | "Fabricadas com constante e alturas dentro da tolerância do fabricante da válvula, para a faixa de pressão de ajuste especificada" |
| "Todas as molas são testadas individualmente e certificadas" | Só manter se o ensaio de carga for mesmo em 100% das peças; dizer qual certificado | "Ensaio de carga em [100% das peças / por amostragem] com relatório por lote e certificado do arame" |
| "Aço Carbono, Aço Inoxidável, Inconel e Aço 5160" | Mistura famílias com uma liga específica e não diz qual Inconel | "Aço carbono e aço-liga (SAE 5160, 6150, 9254), inox e Inconel X-750 para alta temperatura" |

Acrescentar: "A mola é fornecida conforme desenho ou amostra; a calibração e a certificação da válvula são feitas pelo fabricante ou pela oficina credenciada."

### 1.10 Garfos "soldados" — página "Molas para Enleiradores e Enfardadeiras de Feno"

**Como está:** "Soldados: Maior resistência, mas manutenção mais complexa."

**Problema:** soldar arame de aço mola cria uma região frágil ao lado da solda, onde o garfo tende a quebrar. Apresentar solda como "maior resistência" induz a erro. Confirmar se a Jardmolas fornece mesmo garfo soldado.

**Texto corrigido:** "Fixação parafusada: troca rápida no campo, sem afetar o aço da mola."

### 1.11 "Molas do Enleirador de capim" — nome e texto não batem

O título fala em enleirador; o texto descreve a "Mola Prata Mil" para **ceifadeiras de colheita de sementes de capim**. Alinhar título, endereço da página e texto com a máquina certa, e citar a máquina só como indicação de uso ("para uso em …").

## 2. Afirmações que precisam de prova (ou sair)

| Onde | Como está | O que fazer |
|---|---|---|
| Home, Empresa | "Líder em Molas Agrícolas e Industriais no Brasil"; "a melhor fabricante de molas agrícolas do Brasil"; "a fabricante de molas agrícolas mais bem avaliada do mercado" | Liderança e "melhor" exigem comprovação. Trocar por fatos: "Desde 2008 em Jardinópolis-SP. Mais de 2.000 itens de reposição. Nota 5,0 em [n] avaliações no Google." |
| Válvula de segurança, compressão industrial | "Entrega mais rápida do mercado" | "Itens de linha em estoque; prazo informado na cotação" |
| Dedos, tração | "Garantia superior ao mercado"; "garantia estendida" | Dizer o prazo e a condição da garantia, ou retirar |
| Dedo enleirador | "Programa de reciclagem de dedos usados"; "Processos produtivos eco-friendly" | Manter só se o programa existir; descrever como funciona |
| Descanso de moto | "produtos certificados conforme normas do setor" | Dizer qual norma e qual certificado, ou retirar |
| Peneira vibratória | "Testes rigorosos de fadiga"; "Laudos detalhados para cada lote" | Manter só o que é entregue de fato; dizer o que vem no laudo |
| Projetos | "softwares avançados de modelagem e simulação"; "protótipos virtuais" | Dizer o que é feito: cálculo de mola, protótipo físico, ensaio de carga |

## 3. Inconsistências

- **Endereço:** rodapé e contato dizem Rua Artur Costacurta, **340**; a política de privacidade diz **450**. Padronizar.
- **Tempo de empresa:** o site diz "17 anos" e fundação em 2008; em 2026 já são 18. Usar "desde 2008", que não envelhece.
- **Parceiros:** os 12 logotipos da home misturam fornecedor (Belgo) e, aparentemente, clientes. Separar "fornecedores" de "clientes" e publicar logotipo de cliente só com autorização.

## 4. O que falta no site (e o catálogo resolve)

1. Nenhuma página de produto traz bitola, medidas ou código. Quem tem a peça na mão não consegue saber se a Jardmolas fabrica. → catálogo com busca por máquina, tipo e medidas (skill `jm-catalogo`; a base inicial com as 19 famílias e as 20 compatibilidades de fenação já está em `jardmolas/catalogo/`).
2. Não há guia de "como medir sua mola". → já incluído na página do catálogo.
3. Não há página própria para Inconel X-750, que é o diferencial industrial. → conteúdo sugerido na skill `jm-marketing-industrial` (condição × temperatura, NACE, documentos).
4. A compatibilidade de garfos (New Holland Pro Ted e Pro Rotor; Kuhn GA, VB, VBP, Haybob) está em lista corrida, sem dizer qual garfo serve em qual modelo. → cadastrar item a item no catálogo, com código e foto.

## 5. Ordem sugerida de correção

1. Tabela de temperaturas e "Inconel X-750" (1.1 a 1.3) — é o erro que mais custa cliente industrial.
2. ISO 9001 (1.6) — confirmar e corrigir no mesmo dia.
3. Matéria-prima (1.5 e 1.7).
4. Textos genéricos e superlativos (1.8 e seção 2).
5. Catálogo e guia de medição (seção 4).

## Fontes

- Special Metals, boletim técnico "INCONEL alloy X-750" (limites de serviço de molas por têmpera e tratamento; resistência à oxidação até 1800 °F; permeabilidade magnética).
- Composição do SAE 5160 (C 0,56–0,64%) conforme tabela de distribuidor de aços especiais; SAE 6150 conforme faixa usual da norma SAE (conferir no certificado do fornecedor).
- EN 10270-1 como norma vigente de arame patenteado para molas (folheto técnico do fornecedor do arame).
- Limite de cerca de 250 °C para molas de inox austenítico: prática de manuais de molas e de fabricantes de válvulas de segurança, que retiram o 316 por volta de 230 °C.
