# Jardmolas — skills da fábrica

Dezesseis skills para o Claude operar, setor por setor, uma fábrica de molas
para implementos agrícolas e indústria, com especialidade em molas de fio
redondo de Inconel X-750. Feitas para a Jardmolas (Jardinópolis-SP).

Cada skill é o manual de um setor. A `jm-time-ia` é a porta de entrada: ela
coordena as outras como um time de agentes e sabe a ordem em que o trabalho
passa de um setor ao outro.

## As skills

| Skill | Setor | O que entrega | Ferramenta |
|---|---|---|---|
| `jm-time-ia` | Direção / time de IA | Coordena 15 agentes, fluxos entre setores, rotinas diária, semanal e mensal | perfil da empresa |
| `jm-estrategia-100m` | Estratégia | Plano por etapas até US$ 100 milhões, desenho da fábrica, portões de decisão, painel do dono | `plano.py` |
| `jm-engenharia-molas` | Engenharia de produto | Projeto e verificação de molas, ficha técnica, diagnóstico de falha | `mola.py` + banco de materiais |
| `jm-inconel-x750` | Ligas especiais | Têmpera, tratamento térmico por temperatura de serviço, NACE, compra do arame, fabricação | dados com fonte e grau de confiança |
| `jm-molas-valvulas` | Aplicação em válvulas | Dupla portinhola, esfera trunnion, segurança, retenções, compressores | usa `mola.py portinhola` |
| `jm-molas-agro` | Linha agrícola | Dedos, garfos, molas por máquina, catálogo de reposição, calendário de safra, canais | — |
| `jm-processos-fabricacao` | Engenharia de processo | Roteiros, alívio e envelhecimento, retífica, shot peening, acabamento, hidrogênio | — |
| `jm-pcp-producao` | PCP | Prazo, sequenciamento, capacidade, arame, indicadores | — |
| `jm-qualidade` | Qualidade | Plano de controle, rastreabilidade, data book, 8D, certificações | `capabilidade.py` |
| `jm-compras-suprimentos` | Compras e comércio exterior | Especificação de arame, cotação, importação, drawback, estoque, terceiros | — |
| `jm-comercial-orcamentos` | Comercial | Custo e preço por faixa, proposta, negociação, pós-venda | `custo.py` |
| `jm-prospeccao` | Novos negócios | Quem compra molas de X-750, segmentos, abordagem, funil, feiras | lista de compradores pesquisada |
| `jm-marketing-industrial` | Marketing | Site e SEO por aplicação, conteúdo técnico, catálogo, feiras | lista de verificação técnica |
| `jm-financeiro` | Financeiro | Custo-hora, margem, caixa, DRE, câmbio e níquel, investimento | — |
| `jm-rh-seguranca` | Pessoas e segurança | Cargos, formação de preparador, polivalência, riscos de arame e mola, NRs | — |
| `jm-manutencao` | Manutenção | Preventiva de enroladeiras e fornos, calibração, diagnóstico pela peça | — |

## As calculadoras

Todas em Python puro, sem dependências.

```bash
# mola: compressão, tração, torção, dupla portinhola, dimensionamento
python skills/jm-engenharia-molas/scripts/mola.py materiais
python skills/jm-engenharia-molas/scripts/mola.py portinhola --material x750-no1 --d 4 --De 34 \
   --Nb 14 --perna1 40 --perna2 40 --raio 95 --pre-ang 20 --abertura 85 --pino 22 --dp-alvo 1.5

# custo e preço por faixa de quantidade (arame em R$ ou em US$)
python skills/jm-comercial-orcamentos/scripts/custo.py --help

# capabilidade de processo (Cp, Cpk, carta de controle)
python skills/jm-qualidade/scripts/capabilidade.py --help

# modelo de crescimento até a meta
python skills/jm-estrategia-100m/scripts/plano.py --receita-atual 6 --cambio 5.40 --anos 12
```

## Como instalar

**Claude Code** — neste repositório:
```
/plugin marketplace add contrynegocios26-cyber/instagram-agent-skill
/plugin install jardmolas
```

**Claude (aplicativo e web)** — cada skill está empacotada em `dist/` como
arquivo `.skill`; envie o arquivo numa conversa e use "Salvar skill", ou
adicione em Configurações → Capacidades → Skills.

## Como usar

Fale com o time como falaria com a equipe:

- "Chegou este desenho para cotar" → projeto, liga, processo, prazo e preço.
- "Quem compra mola de Inconel X-750? Monta a lista da semana."
- "O cliente reclamou que a mola relaxou a 400 °C."
- "Dá para entregar 500 peças até o dia 20?"
- "Vale comprar um forno com registrador?"
- "O que temos para hoje?"

## O que você precisa preencher

As skills não inventam dado de fábrica. O arquivo
`skills/jm-time-ia/references/perfil-jardmolas.md` lista o que falta
confirmar: faixa de bitola, máquinas e fornos, certificações, condição de
X-750 fabricada hoje, custo-hora, regime tributário, faturamento por
mercado. Quanto mais disso estiver preenchido, menos `[confirmar]` aparece
nas entregas.

## Limites — leia antes de confiar

- **Pesquisa**: o levantamento de mercado e de dados do Inconel X-750 foi
  feito em 10/11/2026 só por busca na web; os sites e PDFs originais
  estavam bloqueados na sessão. Cada número de liga traz a etiqueta de
  confiança em `jm-inconel-x750/references/dados-x750.md`, e cada empresa da
  lista de compradores traz o tipo de evidência. Confira no boletim do
  fabricante da liga, nas normas compradas e no catálogo do cliente antes de
  usar em certificado ou proposta.
- **Cálculo**: a calculadora verifica o projeto; quem libera a mola é o
  ensaio do lote-piloto. O Rm do certificado do arame vence o Rm estimado.
- **Impostos e leis**: alíquotas, classificação fiscal, reforma tributária e
  normas de segurança mudam; as skills dão o roteiro e as perguntas, quem
  confirma é o contador e o profissional de segurança.
- **Leads**: a lista de compradores é de empresas a qualificar, não de
  clientes garantidos.
- **Meta de US$ 100 milhões**: as skills dão o método e a conta; o
  faturamento vem de execução, capital e tempo.
