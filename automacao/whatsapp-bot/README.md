# Robô de atendimento WhatsApp — MP Marcenaria

Responde **na hora, 24 h por dia**, toda pessoa que chama o WhatsApp da MP. Faz as perguntas do orçamento (ambiente, cidade, fase da obra, prazo, fotos e medidas), classifica o lead como quente, morno ou frio, salva em `dados/leads.csv` e **te manda o resumo no seu WhatsApp** para você assumir a conversa.

Usa a **API oficial do WhatsApp (Cloud API da Meta)**. Não usa programas "piratas" que conectam pelo WhatsApp Web, porque esses derrubam o número.

## Como o funil funciona

```
Cliente chama no WhatsApp (anúncio, Instagram, Google, cartão, QR code)
        │
        ▼
Boas-vindas automática  ──►  [Quero um orçamento] [Sou arquiteto(a)] [Outro assunto]
        │                         │                       │
        ▼                         ▼                       ▼
Ambiente → Cidade → Fase      Escritório + cidade      Conta o que precisa
→ Prazo → Fotos/medidas       → Tem projeto agora?
        │                         │                       │
        └───────────────┬─────────┴───────────────────────┘
                        ▼
      Lead salvo + resumo no WhatsApp do vendedor
      (temperatura: Quente / Morno / Frio)
                        ▼
      Vendedor assume a conversa (o robô para de responder)
```

- Fora do horário (seg. a sex. 8h às 18h, sáb. 8h às 12h), avisa que o retorno é no primeiro horário.
- Quem digita em vez de tocar no botão também é entendido ("quanto custa um guarda-roupa?" já vai para orçamento).
- "Parar" ou "sair" descadastra; "menu" recomeça.
- Depois que o lead é passado para você, o robô **fica quieto** naquela conversa.

## O que você precisa (uma vez só)

1. **Conta no Meta Business** (business.facebook.com) com a MP verificada.
2. **Número no WhatsApp Cloud API.** Dá para usar o mesmo número da MP: a Meta permite usar o app WhatsApp Business e a API juntos (recurso de "coexistência", ao conectar pelo cadastro incorporado). Se aparecer a opção de migrar e perder o app, **pare e use um número novo** para o robô.
3. **Um lugar para rodar o robô**, 24 h ligado: Render, Railway ou Google Cloud Run. Custa de R$ 0 a R$ 40 por mês.
4. **Custos da Meta:** responder clientes que chamaram é gratuito. Mensagens de marketing iniciadas pela MP (modelos) são pagas por mensagem, alguns centavos cada.

## Instalação (passo a passo)

1. No painel do app da Meta (developers.facebook.com → seu app → WhatsApp → Configuração da API), copie o **ID do número de telefone** e gere um **token permanente** (Configurações do negócio → Usuários do sistema → Gerar token, com as permissões `whatsapp_business_messaging` e `whatsapp_business_management`).
2. Suba esta pasta no Render ou Railway como serviço web Python:
   - Comando de build: `pip install -r requirements.txt`
   - Comando de início: `gunicorn -w 1 -b 0.0.0.0:$PORT app:app`
   - Variáveis: preencha as de `.env.example`.
   - Ligue um **disco persistente** em `dados/`, senão as conversas somem a cada reinício.
3. No painel da Meta → WhatsApp → Configuração → Webhook:
   - URL de retorno: `https://SEU-ENDERECO/webhook`
   - Token de verificação: o mesmo `WA_VERIFY_TOKEN`
   - Assine o campo **messages**.
4. Mande "oi" de outro celular para o número da MP. O robô deve responder em segundos.
5. Todo dia, mande "bom dia" do **seu** celular para o número da MP. Isso abre a janela de 24 h para o robô te avisar dos leads de graça. (Ou cadastre o modelo `aviso_novo_lead` de `templates.md`.)

## Testar sem conta na Meta

```bash
python3 test_funil.py     # simula conversas completas
```
Sem `WA_TOKEN`, o `app.py` roda em modo simulação e só imprime o que enviaria.

## Arquivos

| Arquivo | O que é |
| --- | --- |
| `funil.py` | As perguntas e a lógica do funil. **Para mudar textos, mexa aqui.** |
| `app.py` | Servidor que recebe e envia mensagens pela API. |
| `test_funil.py` | Simulação de conversas. |
| `templates.md` | Modelos para aprovar na Meta (retomar orçamento, pós-venda, indicação, lead incompleto). |
| `.env.example` | Variáveis de configuração. |
