# Modelos de mensagem para aprovar na Meta

Na API oficial, a empresa **só pode iniciar uma conversa** (ou falar depois de 24 h sem resposta do cliente) usando um **modelo aprovado**. Cadastre estes no Gerenciador do WhatsApp (Meta Business Suite → WhatsApp → Modelos de mensagem). A aprovação costuma sair em minutos ou horas.

Use só com quem **já tem relação com a MP** (clientes, quem pediu orçamento, quem chamou a MP antes) ou **deu permissão** para receber mensagens. Disparar para lista fria de empresas tira a nota de qualidade do número e pode bloqueá-lo. Para os 422 leads da planilha, use os botões "Abrir conversa" (envio manual, um a um).

`{{1}}`, `{{2}}`... são as variáveis preenchidas na hora do envio.

---

### 1. `retomar_orcamento` — Marketing
Para quem pediu orçamento e não fechou.

> Oi, {{1}}! Aqui é da MP Marcenaria. Em {{2}} você pediu um orçamento de {{3}} com a gente. Ainda está nos seus planos? Se quiser, revisamos o projeto com você e montamos opções para caber no que você pensou.

Botões de resposta rápida: `Quero revisar` · `Já resolvi` · `Não quero receber`

### 2. `pos_venda` — Utilidade
Para quem comprou de 1 a 36 meses atrás.

> Oi, {{1}}! Aqui é da MP Marcenaria. Passando para saber como está {{2}} que fizemos para você. Está tudo funcionando certinho? Se alguma porta ou gaveta precisar de ajuste, é só responder aqui.

Botões: `Está tudo ótimo` · `Preciso de ajuste`

### 3. `pedido_indicacao` — Marketing
Enviar uns 7 dias depois de o cliente responder "Está tudo ótimo".

> {{1}}, que bom que você gostou! ❤️ Se souber de alguém construindo ou reformando, pode indicar a MP? Para cada indicação que fechar, você ganha 4% do valor do serviço. É só mandar o contato da pessoa aqui.

Botões: `Vou indicar` · `Não quero receber`

### 4. `retorno_lead_incompleto` — Utilidade
Para quem começou o atendimento no robô e parou no meio (entre 2 e 24 h depois).

> Oi, {{1}}! Vi que você começou a pedir um orçamento com a MP Marcenaria e não conseguimos terminar. Quer continuar? Leva 1 minuto.

Botões: `Continuar` · `Agora não`

### 5. `aviso_novo_lead` — Utilidade (para o vendedor)
Usado pelo robô para te avisar quando você não falou com o número da MP nas últimas 24 h.

> Novo lead no WhatsApp da MP: {{1}}, {{2}}, quer {{3}}. Temperatura: {{4}}. Chame o cliente em até 1 hora.

---

**Regras que mantêm o número saudável:**
- Sempre um botão `Não quero receber`. O robô já entende "parar" e "sair" e marca o contato como descadastrado.
- No máximo 1 mensagem de marketing por contato a cada 15 dias.
- Se muita gente bloquear ou denunciar, a Meta reduz o limite de envios do número. Envie para poucos, bem escolhidos.
