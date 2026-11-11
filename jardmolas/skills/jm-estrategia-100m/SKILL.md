---
name: jm-estrategia-100m
description: >-
  Estratégia e direção da Jardmolas rumo a uma fábrica de US$ 100 milhões de
  faturamento: tese de crescimento, portfólio de mercados, etapas com portões
  de decisão, desenho da fábrica por células, organograma, investimentos,
  certificações, exportação, aquisições, riscos e painel do dono. Use quando
  o assunto for plano de negócios, plano de 5 ou 10 anos, meta de
  faturamento, onde investir, qual máquina comprar primeiro, ampliar a
  fábrica, novo mercado, comprar concorrente, buscar sócio ou financiamento,
  reunião de diretoria, ou "como chegar em 100 milhões" — e sempre que uma
  decisão grande precisar ser checada contra o plano.
---

# Jardmolas — Estratégia: a fábrica de US$ 100 milhões

Você é o conselheiro do dono. A meta é grande de propósito: uma fábrica de
molas com US$ 100 milhões de faturamento anual é uma empresa de centenas de
pessoas, várias plantas ou uma planta grande, clientes globais e sistema de
gestão auditado. Seu papel é manter a meta honesta — **mostrar a conta, a
ordem das apostas e o que precisa ser verdade em cada etapa** — e impedir
que o entusiasmo compre a máquina errada na hora errada.

Duas regras:
1. Nenhum número de mercado ou da empresa é inventado. O que não se sabe
   vira premissa explícita ou pergunta ao usuário.
2. Toda recomendação diz o que ela exige de caixa, de gente e de tempo.

## Primeiro, a conta

```bash
python scripts/plano.py --receita-atual [R$ mi/ano] --meta-usd 100 --cambio [R$/US$] --anos [n] \
   [--organico 0.30] [--receita-por-func 0.45] [--giro-ativo 2.0] [--capital-giro 0.25]
```

O script devolve a taxa de crescimento composta necessária, a trajetória ano
a ano, quanto o crescimento orgânico sozinho alcança e a lacuna, além de
ordens de grandeza de equipe, ativo fixo e capital de giro na meta. Os
parâmetros opcionais são **premissas do usuário**, não dados de mercado.

Leitura típica: uma empresa de pequeno porte que queira chegar a US$ 100
milhões em 10 a 15 anos precisa crescer na casa de 35% a 60% ao ano, todos
os anos. Crescimento orgânico sustentado nesse ritmo é raro em indústria;
por isso o plano tem três motores — orgânico, exportação e aquisições — e
portões que permitem parar numa empresa excelente de R$ 50, 100 ou 200
milhões se o seguinte não fizer sentido. Diga isso ao dono com clareza:
cada etapa já é um bom negócio.

## Tese: por onde a Jardmolas cresce

| Motor | Aposta | Por que a Jardmolas pode ganhar | O que precisa ser verdade |
|---|---|---|---|
| 1. **Reposição agrícola nacional** | De fornecedor regional a marca de reposição com catálogo por máquina em todo o país | Mais de 2.000 itens, polo canavieiro e Agrishow ao lado, carro-chefe em palha de cana | Distribuição (revendas, cooperativas), estoque pré-safra, catálogo digital |
| 2. **Molas de liga para válvulas (Brasil)** | De um nicho (dupla portinhola) a fornecedor de referência de molas em X-750, 718, C-276 para fabricantes de válvulas | Referência real em X-750; concorrentes locais sem certificação visível | Forno com registro, PMI, data book, ISO 9001, engenharia de aplicação |
| 3. **Montadoras agrícolas (OEM)** | Contratos de fornecimento seriado | Proximidade dos polos paulistas; engenharia de custo | PPAP, entrega confiável, preço com fórmula |
| 4. **Exportação de molas de liga** | México, EUA e Europa compram X-750 como padrão de catálogo | Câmbio, drawback, mesma peça já fabricada | Certificação, inglês técnico, logística, capital de giro |
| 5. **Óleo e gás e energia** | Subsea, cabeça de poço, compressores, nuclear, turbinas | Margem alta, poucos fornecedores locais | Sistema tipo API Q1/ISO 29001; depois AS9100; qualificações de 12–24 meses |
| 6. **Componentes elásticos vizinhos** | Molas prato, anéis, arames conformados, estampados, kits de reparo de válvula, molas a quente | Mesmo cliente, mesma engenharia | Investimento por linha; ou aquisição |
| 7. **Aquisições** | Comprar fabricantes regionais (Sul para OEM agro; São Paulo para industrial) | Setor pulverizado, sucessão familiar mal resolvida | Caixa, governança, capacidade de integrar |

Ordem: 1 e 2 pagam as contas e financiam o resto; 3 e 4 escalam; 5, 6 e 7
transformam a empresa. Não inverta.

## Etapas e portões

Os valores de faturamento são marcos de referência; ajuste com o resultado
do script e o ponto de partida real.

| Etapa | Marco | Foco | Investimentos típicos | Portão para avançar |
|---|---|---|---|---|
| **0. Arrumar a casa** | hoje | Custo-hora real, margem por cliente, ficha técnica para tudo, rastreabilidade, catálogo organizado, time de IA rodando as rotinas | Sistema de gestão simples, instrumentos, treinamento | DRE gerencial mensal confiável; entrega no prazo ≥ 90% |
| **1. Especialista regional** | ~R$ 15–30 mi | Reposição agro com distribuição; 5 a 10 clientes de válvulas; trunnion e PSV | ISO 9001; forno de câmara com registro; máquina de ensaio; analisador de liga; enroladeira de fio fino | Nenhum cliente acima de 20% da receita; margem de contribuição estável; caixa positivo com crescimento |
| **2. Referência nacional** | ~R$ 60–100 mi | OEM agro; primeiras exportações de liga; segunda linha de produto | Expansão de planta; ERP com chão de fábrica; laboratório (fadiga, relaxação, metalografia); certificação de óleo e gás | Exportação recorrente; gestão profissional nas áreas-chave; sistema auditado sem não conformidade maior |
| **3. Plataforma** | ~R$ 150–250 mi | Primeira aquisição integrada; linha a quente ou molas prato; contratos de longo prazo | Aquisição; segunda planta; automação de ensaio e inspeção | Integração concluída com ganho medido; conselho consultivo; auditoria contábil externa |
| **4. Empresa global** | ~R$ 500 mi+ (US$ 100 mi) | Multiplanta; presença nos EUA ou México; portfólio de componentes; aeroespacial ou nuclear | Capital de sócio ou dívida de longo prazo; novas aquisições | — |

Cada portão é uma pergunta de sim ou não. Se a resposta for não, a
prioridade é fechá-lo, não avançar.

## A fábrica (desenho-alvo por células)

| Célula | O que faz | Por que separada |
|---|---|---|
| **Agro alto volume** | Dedos, garfos, molas de linha em arame patenteado; conformadoras e enroladeiras de fio médio e grosso; forno contínuo; pintura | Fluxo contínuo, setup curto, estoque de produto acabado |
| **Fio fino de precisão** | Molas pequenas (sede de válvula, instrumentação) em alta cadência com ensaio de carga automático | Limpeza, metrologia fina, lotes de milheiro |
| **Ligas especiais** | Inox e níquel; ferramental dedicado; área limpa de contaminação por ferro; rastreabilidade por corrida | Evitar contaminação e mistura; é a célula de maior margem |
| **Tratamento térmico** | Forno contínuo de alívio; fornos de câmara com registro e uniformidade conhecida; no futuro, vácuo ou atmosfera controlada | Gargalo natural e processo especial auditado |
| **Acabamento** | Retífica, shot peening, presetting a frio e a quente; revestimentos próprios ou parceiros homologados | Define vida em fadiga |
| **Molas pesadas (futuro)** | Barra a quente, têmpera e revenimento | Só com carteira que justifique; alternativa: aquisição |
| **Laboratório** | Ensaio de carga e torque, dureza, PMI, metalografia, fadiga, relaxação a quente | Transforma a fábrica em fornecedora de engenharia |
| **Logística** | Almoxarifado de arame por liga e corrida; expedição com documentação | Rastreabilidade e prazo |

Princípios de layout: fluxo em linha do arame à expedição sem cruzamento;
ligas especiais fisicamente separadas; forno perto das enroladeiras que mais
o alimentam; espaço reservado para dobrar cada célula.

## Organização (evolução)

- **Etapa 0–1**: dono + líderes de produção, qualidade e comercial técnico;
  PCP e financeiro com apoio do time de IA (`jm-time-ia`); contador e
  segurança do trabalho externos.
- **Etapa 2**: gerências de operações, comercial, qualidade/engenharia e
  administrativo-financeiro; engenheiro de aplicação dedicado a válvulas;
  responsável por exportação.
- **Etapa 3–4**: diretoria profissional, controladoria, conselho, gestor de
  integração de aquisições, estrutura comercial por mercado.

A regra de contratação: cada função ganha uma pessoa dedicada quando o
gargalo passa a ser atenção humana, não ferramenta.

## Painel do dono (mensal, uma página)

| Indicador | Por quê |
|---|---|
| Receita por mercado e crescimento em 12 meses | Trajetória contra o plano |
| Margem de contribuição por mercado | Qualidade do crescimento |
| Concentração: maior cliente e três maiores, % da receita | Risco |
| Entrega no prazo e reclamações | Saúde operacional |
| Caixa, ciclo de caixa e dívida líquida ÷ EBITDA | Fôlego |
| Carteira de pedidos em meses de produção | Visibilidade |
| Funil de ligas especiais: leads A, amostras, homologações | Futuro |
| Pessoas em nível 3–4 nas operações críticas | Capacidade de crescer |

## Riscos que derrubam o plano

| Risco | Sinal de alerta | Defesa |
|---|---|---|
| Crescer sem caixa | Ciclo de caixa alongando, desconto de recebíveis subindo | Sinal em arame especial, linha de giro contratada antes, crescimento limitado pelo caixa |
| Dependência de um cliente ou de uma safra | Cliente > 20%; mercado > 50% | Motores 1 e 2 em paralelo; exportação |
| Falha de qualidade em liga especial | Reclamação com parada de cliente | Rastreabilidade, PMI, forno calibrado, 8D |
| Oscilação do níquel e do câmbio | Margem de Inconel variando | Validade curta, reajuste, travas |
| Perda de pessoas-chave | Turnover de preparador | Matriz de polivalência, carreira, biblioteca de setups |
| Investir antes da demanda | Máquina parada | Carteira ou carta de intenção como condição de compra |
| Aquisição mal integrada | Queda de entrega ou margem na adquirida | Começar pequeno, plano de 100 dias, gestor dedicado |
| Mudança tributária | Regime novo altera preço e crédito | Revisão anual com o contador; cláusula em contrato |

## Como responder

Para qualquer decisão: (1) em que etapa a empresa está e qual portão está
aberto; (2) a decisão aproxima ou distrai do portão; (3) conta de retorno
com premissas (`jm-financeiro`); (4) recomendação em uma frase e o que
precisa ser confirmado. Plano anual: três prioridades, cada uma com dono,
indicador e orçamento — mais que três é lista de desejos.
