# Funil de vendas automático — MP Marcenaria

O objetivo é que **cliente da região chegue sozinho no WhatsApp da MP** e que a **primeira resposta seja automática**, na hora, a qualquer hora. Você só entra quando o lead já está qualificado.

```
  ATRAIR (automático)           RESPONDER (automático)          FECHAR (você)
  ─────────────────────         ──────────────────────         ──────────────────
  Anúncio "Enviar mensagem"  ┐
  num raio de 60 km          │
  Instagram: "comente        │   WhatsApp da MP:               Você recebe o resumo
  PROJETO"                   ├─► boas-vindas + perguntas  ──►  e chama em até 1 h.
  Google: botão WhatsApp     │   do orçamento + temperatura    Orçamento → follow-up
  Placa de obra com QR code  │   do lead                       → fechamento
  Display nas lojas parceiras┘
                                         ▲
  REATIVAR (semiautomático): modelos aprovados para clientes antigos e orçamentos parados
```

---

## Uma regra antes de tudo: o que NÃO automatizar

**Não dispare mensagem automática para quem nunca falou com a MP** (a lista de 422 empresas, listas compradas ou contatos tirados da internet).
- O WhatsApp **bane o número** quando muita gente bloqueia ou denuncia. Perder o número da MP é perder todos os clientes que estão nele.
- A Meta proíbe mensagem de marketing sem permissão da pessoa, e a LGPD também exige uma base legal para isso.

Para a lista fria, o caminho certo é o que já está na planilha: **botão "Abrir conversa" com a mensagem pronta e envio um a um, personalizado**. Leva uns 20 segundos por contato.

A automação abaixo é toda para **quem chama a MP** e para **quem já é cliente**. Isso funciona, é permitido e não queima o número.

---

## Fase 1 — Hoje, sem gastar nada: WhatsApp Business no celular da MP (15 minutos)

No app **WhatsApp Business** do número da MP: ⋮ → **Ferramentas comerciais**.

### 1. Mensagem de saudação (a primeira mensagem automática)
Ferramentas comerciais → Mensagem de saudação → Ativar → Enviar para: **Todos** (ou "quem não está nos contatos").

```
Oi! 😊 Aqui é da MP Marcenaria, de Alto Paraná. Obrigado por chamar!

Para eu já adiantar seu atendimento, me responde 3 coisas:
1️⃣ Qual ambiente você quer fazer? (cozinha, quarto, closet, porta, painel, área externa…)
2️⃣ Em que cidade é a obra?
3️⃣ A obra está em que fase? (construindo, reboco, pronta ou reforma)

Se tiver fotos do espaço ou medidas, pode mandar também. Já te respondo! 
```

*O app manda essa saudação para quem chama pela 1ª vez ou depois de 14 dias sem conversa.*

### 2. Mensagem de ausência
Ferramentas comerciais → Mensagem de ausência → **Fora do horário comercial**.

```
Oi! Aqui é da MP Marcenaria. Agora estamos fora do horário (seg. a sex. 8h–18h, sáb. 8h–12h), mas sua mensagem já chegou.

Me conta qual ambiente você quer fazer e em que cidade é a obra, que no primeiro horário eu te respondo com tudo. 😊
```

### 3. Horário comercial e perfil
Perfil comercial → Horário: seg. a sex. 8h–18h, sáb. 8h–12h. Descrição: copie a do Google em `04-conteudo-que-gera-orcamento.md`. Endereço e site/Instagram preenchidos.

### 4. Etiquetas (o seu funil dentro do app)
Crie e use em toda conversa:
`🟢 Novo lead` · `📏 Medição agendada` · `📄 Orçamento enviado` · `🔁 Follow-up` · `✅ Fechado` · `🏛 Arquiteto` · `🤝 Parceiro (loja/corretor)` · `❄️ Frio`

Toda manhã abra a etiqueta **Follow-up** e **Orçamento enviado** e siga a tabela de follow-up de `05-mensagens-de-conexao.md`.

### 5. Respostas rápidas
Cadastre as 8 de `05-mensagens-de-conexao.md`, seção 13 (`/oi`, `/medida`, `/fase`, `/orc`, `/follow`, `/arquivo`, `/google`, `/indica`).

### 6. Catálogo
Ferramentas comerciais → Catálogo. Crie itens **sem preço** (é sob medida), um por tipo de serviço: Cozinha planejada, Dormitório e closet, Porta pivotante, Esquadrias, Painel ripado, Banheiro, Deck e área externa. Coloque 3 a 5 fotos reais em cada um e, na descrição: "Sob medida. Medição sem custo se fechar o serviço. Peça seu orçamento."

**Resultado da Fase 1:** quem chama a MP recebe resposta na hora, já respondendo as perguntas do orçamento. Você economiza a primeira rodada de conversa.

---

## Fase 2 — Robô completo com botões (API oficial do WhatsApp)

Está pronto em `automacao/whatsapp-bot/`. Ele faz o que a saudação simples não faz:
- Conversa com **botões e lista** (o cliente toca em vez de digitar).
- Pergunta **uma coisa de cada vez**: ambiente, cidade, fase da obra, prazo e fotos.
- Separa **cliente, arquiteto e outros assuntos**. Para arquiteto, já apresenta a parceria de 4%.
- Calcula a **temperatura** (Quente, Morno, Frio) e **te manda o resumo** no seu WhatsApp.
- Salva todos os leads numa planilha (`leads.csv`).
- Fica quieto depois que você assume a conversa.

Para colocar no ar, siga `automacao/whatsapp-bot/README.md`. Você vai precisar de conta no Meta Business e de um serviço para deixar o robô ligado (R$ 0 a R$ 40 por mês). Se travar em algum passo, me chama com o print da tela.

---

## Fase 3 — Atrair clientes por perto, no automático

### A. Anúncio "Enviar mensagem" no Instagram e Facebook (o que mais traz lead local)
O anúncio aparece só para quem mora perto, e o botão abre direto o WhatsApp da MP, onde a saudação ou o robô já respondem.

**Configuração sugerida (Gerenciador de Anúncios da Meta):**
- **Objetivo:** Engajamento → Mensagens → **WhatsApp**.
- **Local:** raio de **40 km de Alto Paraná** (pega Paranavaí, Loanda, Nova Esperança, Santa Isabel do Ivaí e Terra Rica). Depois teste um conjunto separado com **20 km de Maringá**.
- **Idade:** 27 a 60 anos. **Público:** aberto (sem interesses) ou com interesses em "Construção", "Design de interiores" e "Casa própria". Teste os dois.
- **Orçamento para começar:** R$ 20 a R$ 30 por dia, por 14 dias. Avalie pelo **custo por conversa iniciada**. No interior do PR, de R$ 3 a R$ 10 por conversa é bom.
- **Criativos (em ordem de prioridade):**
  1. O Reel campeão da **medição na obra** (já provou que funciona, 15× a média da conta).
  2. Um **antes e depois** de ambiente completo.
  3. Um vídeo de **porta pivotante abrindo**.
- **Texto principal:**
  > Vai construir ou reformar em Alto Paraná, Paranavaí ou região? A MP fabrica seus móveis planejados, portas e painéis de madeira aqui do lado, sob medida para a sua parede. A gente mede na obra, você vê o projeto em 3D antes de fabricar, e a instalação é com equipe própria. Toque em "Enviar mensagem" e peça seu orçamento.
- **Título:** `Planejados sob medida no noroeste do PR`
- **Mensagem pré-preenchida do cliente:** `Oi! Vi o anúncio e quero um orçamento.`

*Hoje o Windsor.ai desta conta só tem o Instagram conectado. Se você conectar o **Meta Ads** lá, eu consigo criar a campanha (pausada, para você revisar) e acompanhar o custo por conversa toda semana.*

### B. Instagram: "Comente PROJETO"
Em todo Reel, a legenda termina com: **"Comente PROJETO que eu te mando os detalhes no direct."**
Quem comenta recebe resposta no comentário ("Te chamei no direct! 😊") e uma mensagem no direct com o link do WhatsApp:
> Oi, [nome]! Vi seu comentário. Me chama no WhatsApp que eu te passo tudo e já começo seu orçamento: [link wa.me da MP]

A conexão do Windsor.ai com o Instagram da MP já permite **responder comentários**. Posso deixar uma rotina diária que encontra comentários novos e prepara as respostas para você aprovar.

### C. Google (Perfil da Empresa)
- Ative o **botão de WhatsApp/chat** no perfil.
- Peça avaliação a **todo cliente** que recebeu a obra (resposta rápida `/google`). No interior, 20 avaliações com nota 5 colocam a MP no topo do "marcenaria perto de mim".

### D. Placa de obra com QR code (o mais barato e mais local de todos)
Em **toda obra em instalação**, uma placa de 60 × 40 cm na frente: "Móveis e portas desta obra: **MP Marcenaria** · Orçamento pelo WhatsApp" + **QR code** que abre o WhatsApp com a mensagem "Oi! Vi a placa na obra da rua [ ] e quero um orçamento."
Vizinho de obra é o melhor lead que existe: ele vê o trabalho ao vivo e mora na mesma faixa de renda.

### E. Display nas lojas parceiras
O mesmo QR code num display de balcão nas lojas de material e vidraçarias da planilha (script 4). Mensagem pré-preenchida: "Oi! Vim pela indicação da [nome da loja]." Assim você sabe de onde veio o lead e paga os 4% certos.

**Gerador de links com mensagem pronta:**
`https://wa.me/55DDDNUMERO?text=` + a mensagem com espaços trocados por `%20`.
QR code grátis: qualquer gerador de QR code (cole o link).

---

## Fase 4 — Reativar quem já conhece a MP (semiautomático)

Com a lista de clientes antigos e de orçamentos parados (peça para a MP):
- **Com o robô no ar:** use os modelos aprovados de `automacao/whatsapp-bot/templates.md` (`retomar_orcamento`, `pos_venda`, `pedido_indicacao`), no máximo 30 por dia no começo.
- **Sem o robô:** use **Listas de transmissão** do WhatsApp Business (só chega para quem salvou o número da MP) com a mensagem de pós-venda de `05-mensagens-de-conexao.md`, em grupos de 30.

---

## Números para acompanhar toda semana

| Métrica | Onde ver | Meta inicial |
| --- | --- | --- |
| Conversas novas no WhatsApp | Etiqueta "Novo lead" / `leads.csv` | 15 por semana |
| Custo por conversa (anúncio) | Gerenciador de Anúncios | até R$ 10 |
| % de leads quentes | `leads.csv` | 30% |
| Tempo até a 1ª resposta humana | Você | até 1 hora |
| Orçamentos enviados | Etiqueta "Orçamento enviado" | 5 por semana |
| Fechamentos | Etiqueta "Fechado" | 1 por semana |

## Ordem de execução

1. **Hoje:** Fase 1 (15 min no celular da MP) e link wa.me com mensagem pronta na bio do Instagram.
2. **Esta semana:** placa de obra com QR code e "Comente PROJETO" em todo Reel.
3. **Semana que vem:** anúncio "Enviar mensagem" com R$ 20 a R$ 30 por dia, por 14 dias.
4. **Quando tiver o Meta Business pronto:** robô da Fase 2.
5. **Assim que a MP passar a lista:** Fase 4 com clientes antigos.
