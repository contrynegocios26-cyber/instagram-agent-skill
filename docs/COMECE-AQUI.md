# Comece aqui: Growth Partner IA na prática

O plano completo está em [`PROJETO-IA-MARKETING-DIGITAL.md`](PROJETO-IA-MARKETING-DIGITAL.md).
Este arquivo é só o que fazer, na ordem, a partir de hoje. Cada passo aponta
para a skill ou o arquivo que faz o trabalho.

## O que está pronto neste repositório

| Peça | Onde | Faz |
| --- | --- | --- |
| Fábrica de conteúdo | `skills/ig-*` (13 skills) | Reels, carrosséis, legendas, stories, perfil, plano, humanizador |
| Prospecção | `skills/gp-prospect` + `score.py` | Lista pontuada, mensagem em 3 partes, vídeo de auditoria |
| Implantação | `skills/gp-onboard` | voice.md, base de conhecimento, prompt do agente, testes, checklist |
| Relatório | `skills/gp-report` + `report.py` | A conta do dinheiro, funil, gargalo, alertas |
| Gerente | `skills/gp-daily` + `daily.py` | As 5 ações de hoje |
| Operação | `templates/gp/` | Oferta, preços, contrato, proposta, roteiros, planilhas |

## Dia 1: instalar e apontar para o seu negócio

```bash
git clone https://github.com/contrynegocios26-cyber/instagram-agent-skill.git
cp -r instagram-agent-skill/skills/ig-* instagram-agent-skill/skills/gp-* ~/.claude/skills/
mkdir -p ~/.claude/instagram/gp
cp instagram-agent-skill/templates/voice.md ~/.claude/instagram/voice.md
cp -r instagram-agent-skill/templates/gp/* ~/.claude/instagram/gp/
```

1. Preencher `~/.claude/instagram/voice.md` com a **sua** voz (quem prospecta).
   Ou mandar 3 áudios/mensagens suas para o Claude e pedir "escreve meu
   voice.md".
2. Abrir `~/.claude/instagram/gp/oferta.md`. Confirmar nicho, região e
   preços. Não mude os preços para baixo.
3. Abrir CNPJ, se ainda não tem (MEI até R$ 81 mil/ano).

## Dia 2 a 4: o sistema rodando no seu próprio negócio (caso número 1)

1. `/ig-profile` no Instagram da MP Marcenaria. Aplicar as correções.
2. Fazer com você mesmo a reunião de `templates/gp/onboarding-reuniao.md`
   (grave um áudio de 30 minutos respondendo as perguntas).
3. `/gp-onboard` com essa transcrição. Sai a base de conhecimento, o prompt
   do agente e os 30 testes.
4. Escolher a plataforma de agente de WhatsApp (API oficial da Meta, com
   fallback humano). Colar o prompt. Rodar os 30 testes. Zero falha em
   preço e reclamação antes de ligar.
5. `/ig-plan` e as primeiras 6 peças com `/ig-reel` e `/ig-carousel`,
   todas pelo `/ig-human`. Postar.
6. Criar `~/.claude/instagram/gp/metricas-mp.csv` a partir de `metricas.csv`
   e preencher todo dia, 2 minutos.

## Dia 5 em diante: 30 contatos por dia

Rotina fixa, todo dia útil:

| Hora | O quê | Ferramenta |
| --- | --- | --- |
| 8h00 | As 5 ações de hoje | `python3 ~/.claude/skills/gp-daily/daily.py` |
| 8h15 | Testar o WhatsApp de 10 prospects novos (mensagem como cliente) e anotar | `prospects.csv` |
| 9h00 | Pontuar e escrever as mensagens | `/gp-prospect` → `score.py` |
| 9h30 | Mandar 30 mensagens e os follow-ups do dia | você, no WhatsApp/Direct |
| 11h00 | Gravar os vídeos de auditoria para quem respondeu ontem | `roteiro-auditoria.md` |
| 12h00 | Registrar o pipeline | `pipeline.csv` |
| 14h00 | Entrega: conteúdo e ajustes de agente dos clientes | `ig-*` |
| 17h30 | Métricas do dia de cada cliente | `metricas-*.csv` |

Toda segunda, antes das 10h: `report.py` de cada cliente, cinco linhas,
enviar. Toda reunião de fechamento: `roteiro-reuniao.md` aberto, planilha da
conta aberta.

## Metas das primeiras 12 semanas

| Semana | Meta |
| --- | --- |
| 1 | Sistema no ar no seu negócio. voice.md, oferta, CNPJ. |
| 2 a 4 | 600 contatos. 3 pilotos fechados (R$ 1.297/mês, 3 meses, depoimento). |
| 5 a 8 | 3 pilotos implantados e com relatório semanal. Primeiro depoimento no dia 45. |
| 9 a 12 | 5 clientes no preço cheio. R$ 10 a 15 mil de MRR. |

Se na semana 4 a taxa de resposta à primeira mensagem estiver abaixo de 12%,
o problema é a mensagem (falta o achado específico ou o teste do WhatsApp),
não o nicho. Se na semana 8 a conversão reunião para fechamento estiver
abaixo de 30%, falta a conta na frente dele ou falta o caso número 1
funcionando.

## O que ainda depende de você e não está no repositório

- Escolher e contratar a plataforma de agente de WhatsApp (API oficial).
- Passar o `contrato-modelo.md` por um advogado antes do primeiro pagante.
- Gravar. O dono aparecendo ainda ganha de qualquer avatar.
- Mandar as 30 mensagens. Nenhuma skill manda por você, e isso é
  proposital.
