# templates/gp: os arquivos de operação do Growth Partner IA

| Arquivo | O que é | Quem usa |
| --- | --- | --- |
| `oferta.md` | Promessa, planos, preços, regras, a conta na frente do cliente | todas as `gp-*` |
| `prospects.csv` | A lista diária de prospects com os sinais coletados | `gp-prospect` (`score.py`) |
| `pipeline.csv` | Cada prospect e em que estágio está | `gp-daily` (`daily.py`) |
| `clientes.csv` | Cada cliente, mensalidade, datas, retorno das últimas semanas | `gp-daily` (`daily.py`) |
| `metricas.csv` | Uma linha por dia por cliente (copie um por cliente) | `gp-report` (`report.py`) |
| `roteiro-auditoria.md` | O vídeo de 3 a 5 minutos que abre a porta | `gp-prospect` |
| `roteiro-reuniao.md` | Os 20 minutos de fechamento, com as objeções | você |
| `proposta-modelo.md` | A proposta de uma página mandada no WhatsApp | você |
| `contrato-modelo.md` | Estrutura do contrato (passe por advogado antes do 1º pagante) | você |
| `onboarding-reuniao.md` | Os 60 minutos que alimentam a base de conhecimento | `gp-onboard` |
| `kb-template.md` | As 12 seções da base de conhecimento do agente | `gp-onboard` |
| `agent-prompt.md` | O prompt do agente de WhatsApp, com as regras de segurança | `gp-onboard` |

Copie a pasta inteira para `~/.claude/instagram/gp/` e trabalhe lá. Os CSVs
têm só o cabeçalho; os scripts leem qualquer arquivo com essas colunas.
