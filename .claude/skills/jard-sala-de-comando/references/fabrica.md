# Fábrica: processo, qualidade, PCP, compras, logística e segurança

Vale para Engenharia e Qualidade, Engenheiro de Aplicação, PCP e Produção, Compras e Estoque, Logística e Expedição, Pessoas e Segurança. Os números da Jardmolas (máquinas, capacidade, custos) estão em [confirmar] até o dono responder às Perguntas de abertura de `empresa.md`. Este arquivo traz o método; o número vem da fábrica.

## 1. Como uma mola nasce (e onde ela morre)

**Mola helicoidal e forma de arame, enrolada a frio** (a maior parte do que a Jardmolas faz):
1. **Recebimento do arame**: conferir bitola, certificado do lote (resistência à tração Rm, composição), oxidação, embalagem. Guardar o certificado amarrado ao lote: é a rastreabilidade que o comprador de usina e de OEM pede.
2. **Endireitamento e enrolamento/conformação** em enroladeira ou formadora CNC: diâmetro, passo, número de espiras, sentido, hastes, olhais e dobras.
3. **Alívio de tensões (revenimento)** logo depois de enrolar: tira a tensão residual do enrolamento. Pular ou encurtar essa etapa é uma das maiores causas de quebra precoce.
4. **Esmerilhamento de pontas** (molas de compressão que pedem apoio plano).
5. **Jateamento com granalha (shot peening)**: cria tensão de compressão na superfície e aumenta muito a vida em fadiga. É o diferencial técnico que mais faz sentido para dedo de enleirador, que trabalha em fadiga e impacto o dia inteiro. [confirmar se a Jardmolas jateia e em quais códigos]
6. **Pré-setagem (presetting)**: comprimir ou torcer além da carga de trabalho para a mola não "assentar" (perder altura ou abrir) no campo.
7. **Teste de carga e dimensional**: carga em um comprimento de trabalho, ou torque em um ângulo, mais medidas críticas.
8. **Acabamento**: pintura a pó, óleo protetivo, fosfato ou zinco. Atenção: **zincagem eletrolítica em mola de alta resistência exige desidrogenação** (forno logo depois), senão a mola quebra frágil por hidrogênio dias depois.
9. **Inspeção final, embalagem e etiqueta** (código, quantidade, lote, cliente).

**Mola enrolada a quente** (barras grossas, aços SAE 5160 e 9254): aquecer, enrolar, temperar e revenir. [confirmar se a Jardmolas faz ou terceiriza]

**Dedo de enleirador ou desenleirador** é uma forma de arame que trabalha como mola de torção: espiras que acumulam energia, haste que bate na palha e no solo, olhal ou dobra de fixação. Os pontos que decidem a vida do dedo são o **raio de dobra no olhal e na transição espira-haste**, a **ausência de marca de ferramenta**, o **tratamento térmico** e o **jateamento**.

## 2. Matéria-prima (o que dizer e o que conferir)

| Material | O que é | Onde usar |
|---|---|---|
| **EN 10270-1** (substituiu a DIN 17223-1; classes antigas A–D, hoje SL, SM, SH, DM, DH) | Arame de aço carbono patenteado e trefilado. S = uso estático, D = dinâmico | Molas e formas de arame em geral; para fadiga (dedos), classes D |
| **EN 10270-2** (temperado em óleo) | Arame temperado e revenido, inclusive ligas cromo-silício | Molas de válvula e serviço severo |
| **SAE 1070** | Aço alto carbono | Molas e formas de arame em geral |
| **SAE 5160** | Aço liga cromo | Molas grandes, suspensão, alta carga |
| **SAE 6150** | Aço liga cromo-vanádio | Fadiga e temperatura; válvulas |
| **SAE 9254** | Aço liga cromo-silício | Alta tensão e fadiga; válvulas; temperatura |

Regra comercial: falar "arame Belgo certificado" só mostrando o certificado do lote quando pedirem. Falar a norma certa (EN 10270-1 classe DH, por exemplo) impressiona engenheiro de OEM; "DIN 17223" ainda é entendido, mas é nome antigo.

## 3. Plano de controle mínimo

| Etapa | Característica | Método | Frequência | Registro |
|---|---|---|---|---|
| Recebimento | Bitola, Rm, composição | Micrômetro + certificado do fornecedor | Todo lote | Certificado arquivado por lote |
| Primeira peça | Todas as cotas do desenho | Paquímetro, gabarito, projetor/calibrador | Todo setup | Ficha de primeira peça assinada |
| Processo | Diâmetro, comprimento livre, ângulo das hastes | Gabarito passa/não passa | A cada {{n}} peças | Folha de verificação |
| Tratamento térmico | Temperatura e tempo | Registro do forno | Toda carga | Registro do forno |
| Final | Carga x deflexão (ou torque x ângulo) | Máquina de teste de carga | Amostragem por lote ({{n}} peças) ou 100% em item crítico | Relatório do lote |
| Final | Dureza (quando especificada) | Durômetro | Amostra por lote | Relatório |
| Validação de produto novo | Fadiga | Ciclos em bancada ou teste de campo acompanhado | Por código novo | Relatório de validação |

Cada código de catálogo tem uma **ficha técnica** (`modelos.md`). Código sem ficha não entra em catálogo nem em proposta para OEM.

## 4. Quebra em campo: como ler e o que fazer

Peça sempre: foto da fratura de perto, foto da peça inteira com trena, código, máquina e regulagem, hectares até a quebra, tipo de solo, quantas quebraram no conjunto.

| O que se vê | Causa provável | Como confirmar | Ação |
|---|---|---|---|
| Quebra no olhal ou na dobra, superfície com "marcas de praia" | Fadiga com concentração de tensão: raio de dobra pequeno, marca de ferramenta, sem alívio de tensões | Lupa na origem da trinca; conferir ferramenta e raio | Aumentar raio, revisar ferramenta, garantir alívio e jateamento |
| Quebra no meio da haste depois de muitos hectares | Fadiga normal ou sobrecarga por regulagem (dedo raspando o solo, velocidade alta, pedra e toco) | Hectares rodados; regulagem de altura; comparar com o resto do conjunto | Orientar regulagem (conteúdo e pós-venda); avaliar material/diâmetro |
| Quebra frágil logo no começo, fratura reta e brilhante | Dureza alta, tratamento térmico errado, fragilização por hidrogênio (zincagem sem desidrogenação), defeito do arame | Dureza, registro do forno, processo de acabamento, certificado | Segregar o lote, corrigir processo, repor ao cliente |
| Dedo "abriu" ou mola "assentou" (perdeu altura) | Tensão acima do limite, dureza baixa, sem pré-setagem | Carga medida contra a ficha | Pré-setagem, material ou diâmetro maior |
| Corrosão com pite onde a trinca começou | Acabamento inadequado, armazenagem úmida | Inspeção visual | Pintura/óleo; orientar armazenagem |
| Ponta gasta, sem quebra | Abrasão (solo arenoso), uso normal | Comparar com hectares | Normal; registrar vida em hectares (é argumento de venda) |

Toda quebra vira registro de análise de falha (`modelos.md`). Três quebras parecidas no mesmo código param a produção do código até a Engenharia liberar.

## 5. PCP: prometer o que dá para cumprir

- **Carteira única**: todos os pedidos com data prometida, máquina, arame, quantidade e status. O comercial consulta antes de prometer prazo.
- **Sequenciamento por arame e bitola** para reduzir setup; agrupar pedidos do mesmo arame na mesma janela.
- **Prazo prometível**: capacidade livre por máquina na semana menos o que já está na carteira. Item de estoque: prazo de expedição. Sob medida: prazo de amostra e de lote, separados.
- **Estoque de giro dos dedos e molas mais vendidos** (curva A): estoque de segurança = consumo médio semanal × semanas de cobertura. Na entressafra, produzir para chegar em abril com cobertura alta; durante a safra, reposição rápida é o argumento comercial.
- **OEE simples** por máquina = disponibilidade × desempenho × qualidade. Começar medindo paradas e refugo.
- **Quadro do dia** (15 min): o que entra, o que sai, o que está atrasado e por quê.

## 6. Compras e estoque

- **Curva ABC** dos arames por R$ consumido em 12 meses.
- **Estoque mínimo** = consumo diário × prazo do fornecedor (dias) + estoque de segurança. **Máximo** = mínimo + lote de compra.
- Registrar, por bitola: fornecedor, prazo de entrega, preço por kg, data do último reajuste. A variação do preço do arame alimenta a cláusula de reajuste do Financeiro.
- Insumos que param a fábrica se faltarem: granalha, tinta, embalagem, gás/energia do forno, ferramentas e peças de reposição das máquinas críticas.
- Compra antecipada de arame para o estoque de giro pré-safra consome caixa: decidir com o Financeiro.

## 7. Logística e expedição

- **Embalagem**: dedos amarrados por quantidade padrão em caixa ou saco resistente; etiqueta com código, quantidade, lote, cliente e número do pedido.
- **Checklist de expedição**: conferência de código e quantidade, foto antes de fechar, NF-e com **número do pedido de compra** do cliente (usina recusa nota sem ele), agendamento de recebimento quando a usina exige, rastreio enviado ao cliente no mesmo dia.
- **Frete**: tabela por região canavieira (transportadoras regionais), Correios ou similar para volumes pequenos, retirada na fábrica para clientes da região de Ribeirão Preto.
- **Indicadores**: OTIF (no prazo e completo), custo de frete em % do faturamento, avarias.

## 8. Pessoas e segurança

- **NR-12** (máquinas e equipamentos): proteções fixas e móveis com intertravamento, parada de emergência, manual e procedimento por máquina, capacitação registrada. [validar com técnico de segurança do trabalho]
- **NR-6** (EPI): luva anticorte, óculos (mola salta e corta), protetor auricular, calçado.
- **Risco específico de mola**: energia armazenada. Teste de carga, pré-setagem e desmontagem de dispositivo sempre com proteção e procedimento.
- **Matriz de habilidades**: quem opera cada máquina, quem faz setup, quem inspeciona. Ninguém sozinho em máquina crítica sem substituto treinado.
- **Vendedor técnico**: todo comercial passa um dia na fábrica e aprende a medir uma mola, ler uma ficha e reconhecer uma fratura por fadiga.
