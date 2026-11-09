# Jardmolas — Sala de Comando

Um time de 21 agentes de IA para comandar a Jardmolas inteira, com força maior em vendas e prospecção. O Diretor-Geral coordena; cada agente tem missão, entregas, indicadores e regras.

- **Diagnóstico do Instagram e do site:** [`relatorios/diagnostico-jardmolas-2026-11-09.md`](../relatorios/diagnostico-jardmolas-2026-11-09.md)
- **Plano de 90 dias e tarefas da semana:** [`operacao/atas/2026-11-09-abertura.md`](operacao/atas/2026-11-09-abertura.md)
- **Atlas de molas agrícolas e industriais** (cada tipo de mola × implemento × setor do agro × indústria, com empresas compradoras e fontes): [`reports/Atlas de molas agrícolas e industriais.md`](../reports/Atlas%20de%20molas%20agr%C3%ADcolas%20e%20industriais.md)
- **159 contas para prospectar, com fonte:** [`operacao/contas-alvo.csv`](operacao/contas-alvo.csv)

## O time

| Mesa | Agente | Faz o quê |
|---|---|---|
| Diretoria | **Diretor-Geral** | Abre a reunião, aciona quem precisa, fecha com decisões, tarefas, donos e prazos |
| Diretoria | **Inteligência de Mercado** | Onde está o dinheiro: segmentos, regiões, concorrentes, sinais da safra |
| Vendas | **Caçador de Contas** | 30 contas novas e certas por semana, com fonte |
| Vendas | **Pré-vendas (SDR)** | Primeiro contato, cadências, roteiros, qualificação MÁQUINA |
| Vendas | **Grandes Contas (Usinas)** | Plano de conta, teste de campo, contrato anual |
| Vendas | **Canais e Representantes** | Revendas, cooperativas, representantes por região |
| Vendas | **OEM e Indústria** | Mola original para fabricantes, válvulas, mineração, carretas |
| Vendas | **Engenheiro de Aplicação e Orçamento** | Especificação e orçamento em até 2 h úteis, com a calculadora |
| Vendas | **Fechamento e Follow-up** | Nenhum orçamento morre sem resposta |
| Vendas | **Pós-venda e Recompra** | Hectares, garantia, depoimentos, recompra antes da safra |
| Marketing | **Conteúdo e Instagram** | Reels de prova de campo e fábrica por dentro |
| Marketing | **Site, Google e Anúncios** | Catálogo por máquina, SEO, Google, impulsionamento |
| Marketing | **Feiras e Eventos** | Fenasucro, Agrishow, Coopercitrus Expo, dias de campo |
| Fábrica | **Engenharia e Qualidade** | Fichas técnicas, plano de controle, análise de quebra |
| Fábrica | **PCP e Produção** | Prazo prometível, carteira, estoque de giro |
| Fábrica | **Compras e Estoque** | Arame, mínimos, reajustes |
| Fábrica | **Logística e Expedição** | Embalagem, NF-e, frete, OTIF |
| Gestão | **Financeiro, Custos e Preço** | Custo-padrão, preço por canal, margem, caixa |
| Gestão | **Administrativo, Fiscal e Contratos** | Cadastro em usina, contratos, fiscal, LGPD |
| Gestão | **Pessoas e Segurança** | Treinamento, contratação, NR-12 |
| Inteligência | **BI e CRM** | Painel semanal e três recomendações com número |

## Como usar

### No Claude Code (aqui no repositório)
A skill e os agentes já carregam sozinhos em qualquer sessão aberta neste repositório:
- Digite **`/jard-sala-de-comando`** ou só fale do assunto ("o que a gente faz hoje?", "orçamento para a usina X", "quero mais revendas").
- Os 20 especialistas são subagentes reais (`.claude/agents/jard-*.md`): o Diretor roda vários em paralelo.

### No claude.ai ou no app do celular
1. Baixe [`dist/jard-sala-de-comando.zip`](dist/jard-sala-de-comando.zip).
2. Em claude.ai: **Configurações → Capacidades → Skills → Enviar skill**, e escolha o zip.
3. Num chat novo, escreva "Sala de Comando da Jardmolas: o que a gente faz hoje?". Sem subagentes, o Diretor veste um chapéu de cada vez; o resultado é o mesmo.

### Frases que acionam o time
- "O que a gente faz hoje?" → lista do dia (follow-ups, orçamentos, expedição, prospecção)
- "Quero mais clientes" → Inteligência + Caçador + Pré-vendas
- "Orçamento: [foto/medidas/máquina]" → Engenheiro de Aplicação com a calculadora
- "Vamos atacar as usinas" → Grandes Contas + Admin (cadastro)
- "Quero revendedor em [região]" → Canais
- "Quebrou dedo no cliente X" → Pós-venda + Engenharia (análise de falha)
- "Posts da semana" → Conteúdo e Instagram
- "Painel da semana" → BI e CRM

## Arquivos

```
.claude/skills/jard-sala-de-comando/
  SKILL.md                      o Diretor-Geral: time, rotinas, fluxos, regras
  references/empresa.md         fatos da Jardmolas (com fonte) e Perguntas de abertura
  references/vendas-prospeccao.md  ICP, ofertas, cadências, roteiros, objeções, funil
  references/mercado-e-calendario.md  segmentos, calendário do campo, concorrência, feiras
  references/fabrica.md         processo, qualidade, falhas, PCP, compras, logística, NR-12
  references/financeiro-preco.md   custo-padrão, preço por canal, crédito, caixa
  references/marketing.md       Instagram, site, Google, anúncios, feiras
  references/modelos.md         ata, cotação, ficha técnica, proposta, teste de campo, 8D, painel
  references/atlas-resumo.md    tabelas do Atlas de molas (cópia fiel do relatório)
  references/agentes.md         ficha completa de cada agente
  scripts/calc_mola.py          rigidez, tensão, peso, custo e preço de mola
  scripts/funil.py              resumo do funil e follow-ups do dia
.claude/agents/jard-*.md        os 20 especialistas como subagentes
jardmolas/
  operacao/contas-alvo.csv      159 contas pesquisadas (usinas, cooperativas, revendas, OEMs, indústria)
  operacao/pipeline.csv         o CRM da sala (oportunidades em andamento)
  operacao/decisoes.md          decisões com motivo e resultado
  operacao/backlog-conteudo.md  vídeos a gravar, gravados e postados
  operacao/atas/                uma ata por reunião
  pesquisa/                     concorrentes, feiras 2027, listas brutas da pesquisa
  dist/jard-sala-de-comando.zip a skill pronta para enviar ao claude.ai
```

### As duas ferramentas que rodam

```bash
# mola de compressão: rigidez, carga, tensão x Rm do certificado, peso, custo e preço por lote
python3 .claude/skills/jard-sala-de-comando/scripts/calc_mola.py compressao \
  --d 6 --De 50 --nt 10 --L0 120 --Lt 90 --Rm 1600 \
  --arame-kg 12.5 --perda 5 --pecas-hora 120 --custo-hora 150 --setup-min 60 --lote 500 \
  --tratamento-kg 2 --acabamento 0.3 --embalagem 0.1 \
  --impostos 8 --comissao 5 --frete 3 --margem 25

# funil: etapas, valor, follow-ups vencidos e de hoje, perdas por motivo
python3 .claude/skills/jard-sala-de-comando/scripts/funil.py jardmolas/operacao/pipeline.csv
```
Os números do exemplo são ilustrativos. Use o preço real do arame, o custo-hora da fábrica e as alíquotas confirmadas pelo contador.

## Regras que nenhum agente quebra

1. Nada inventado: falta de dado vira `{{dado}}` [confirmar].
2. Agente prepara; pessoa aprova e envia. Nada de disparo em massa no WhatsApp.
3. Prospecção limpa (LGPD): dado corporativo, fonte registrada, opção de sair.
4. Orçamento em até 2 h úteis (catálogo) e 24 h (sob medida).
5. Preço sai da conta; prazo sai do PCP; prova vale mais que adjetivo.
