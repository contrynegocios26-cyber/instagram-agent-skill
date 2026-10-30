# MP Marcenaria App — visão de produto

## Tese

Em marcenaria de alto padrão o cliente paga caro, espera de 60 a 120 dias e, na
maior parte desse tempo, não vê nada. A ansiedade vira mensagem no WhatsApp, a
mensagem vira interrupção na oficina, e a interrupção vira atraso. O app ataca
exatamente isso: dá ao cliente visibilidade e controle (3D, etapa, previsão,
pagamentos, aprovação) e devolve ao marceneiro tempo de produção.

O mesmo app serve dois momentos comerciais que hoje a MP resolve na mão:

1. **Antes da venda**: o simulador de orçamento qualifica o lead (ambientes,
   metragem, padrão, prazo, fotos) e entrega o pedido formatado. A MP responde
   com data de medição em vez de fazer dez perguntas.
2. **Depois da entrega**: garantia, cuidados, assistência e indicação ficam no
   bolso do cliente. Indicação é a principal fonte de novos projetos em
   marcenaria; o app transforma isso em código rastreável.

## O que está pronto (v1, este repositório)

- PWA instalável e offline, sem backend, dados em localStorage.
- Orçamento em 4 passos com faixa de referência configurável e envio por WhatsApp.
- Acompanhamento com 9 etapas reais da MP, progresso, previsão e feed da oficina.
- 3D volumétrico montado por peças a partir do mesmo formato do `projeto.json`
  usado no fluxo de orçamento da MP (módulos em mm, materiais por código).
- Aprovação com checklist e assinatura digital, registrada no histórico.
- Pagamentos com Pix, comprovante e status.
- Inspirações com elevações desenhadas e catálogo de acabamentos.
- Pós-venda: garantia, cuidados, assistência, indicação.
- Área do marceneiro por PIN para atualizar o cliente sem sair do app.
- Tema claro e escuro, tipografia e cores da identidade MP (grafite + madeira).

## Roadmap para a versão vendável

### v1.1 — a MP usando com clientes reais (2 a 3 semanas)
- Backend leve (Supabase ou Firebase): clientes, projetos, etapas, pagamentos, atualizações, aprovações com assinatura e carimbo de data/hora.
- Login do cliente por link mágico no WhatsApp ou e-mail (sem senha).
- Upload de fotos da oficina direto do celular do marceneiro.
- `projeto.json` gerado no orçamento vira o 3D do app sem retrabalho.
- Notificações push (Web Push) para "entrou em produção", "parcela vence em 3 dias", "nova foto".

### v1.2 — fechar mais e mais rápido
- Proposta em PDF assinável dentro do app, com aceite e entrada por Pix (API do PSP, confirmação automática).
- Agenda de medição e instalação com confirmação do cliente.
- Pesquisa de satisfação na entrega; nota alta pede avaliação no Google.
- Painel do arquiteto: pranchas, revisões e aprovação técnica em um link.

### v2 — plataforma para outras marcenarias (SaaS)
- Multi-empresa: cada marcenaria com sua marca, cores, WhatsApp, etapas e faixas.
- Onboarding em 15 minutos a partir do `config.js` atual.
- Planos por número de projetos ativos.

## Modelo de negócio e a meta de US$ 1 milhão

Um app vale pelo que gera ou economiza, não pelo código. A meta de valor de
US$ 1 milhão é uma meta de negócio, com premissas que precisam ser confirmadas
no uso real. O caminho mais curto tem duas camadas:

**Camada 1 — valor direto para a MP.** Premissas conservadoras a validar:
menos 30 % de mensagens operacionais, 1 orçamento a mais fechado por mês
pela qualificação do lead e pela aprovação sem atrito, e 1 indicação
rastreada a cada 5 projetos entregues. Com ticket médio de alto padrão, isso
paga o app muitas vezes no primeiro ano.

**Camada 2 — SaaS para marcenarias de planejados.** O Brasil tem dezenas de
milhares de marcenarias e fábricas de planejados; a maioria opera com
WhatsApp e planilha. Referência de valuation para SaaS pequeno em estágio
inicial: 3 a 6 vezes a receita anual recorrente.

| Cenário | Marcenarias pagantes | Plano médio/mês | Receita anual | Faixa de valuation (3–6×) |
| --- | ---: | ---: | ---: | ---: |
| Validação | 50 | R$ 297 | R$ 178 mil | R$ 0,5–1,1 mi |
| Tração | 300 | R$ 347 | R$ 1,25 mi | R$ 3,7–7,5 mi |
| Meta US$ 1 mi (≈ R$ 5,5 mi) | ~250 | R$ 347 | ≈ R$ 1,0 mi | ≈ R$ 3–6 mi |

Leitura: cerca de 250 marcenarias pagantes colocam a plataforma na faixa da
meta. Isso é alcançável em 18 a 24 meses se a MP for o caso de uso de
referência (vídeos da própria obra, antes/depois, depoimento de cliente) e a
distribuição vier pelo mesmo Instagram que já traz os clientes da MP.

Receitas adicionais que a plataforma habilita: taxa sobre pagamentos via Pix
integrado, catálogo de fornecedores (MDF, ferragens, LED) com comissão, e
plano para arquitetos.

## Arquitetura sugerida para a v1.1

```
Cliente (PWA, este repo)  ──HTTPS──▶  Supabase
  - auth por link mágico              - Postgres: empresas, clientes, projetos,
  - Realtime para etapa/fotos           etapas, pagamentos, atualizacoes,
  - Web Push                            aprovacoes (assinatura PNG + hash)
                                      - Storage: fotos da oficina, PDFs
Marceneiro (mesmo app, modo oficina)  - Edge Functions: webhook do PSP (Pix),
  - publica foto/etapa                  envio de push, geração do link mágico
  - marca pagamento
```

Regras que não mudam: o cliente nunca vê custo, margem, RT ou plano de corte;
nada vai para produção sem remedição técnica; o valor de um projeto sai do
projeto executivo, nunca do simulador.

## Métricas para acompanhar desde o primeiro cliente

- Tempo entre primeiro contato e aprovação assinada.
- Mensagens no WhatsApp por projeto (antes e depois do app).
- Taxa de aprovação de propostas enviadas pelo app.
- Parcelas pagas no vencimento.
- Indicações com código usadas.
- Projetos abertos no app por semana (engajamento do cliente).
