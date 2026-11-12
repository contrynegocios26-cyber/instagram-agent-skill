# Ferramentas, custos, requisitos de loja e lançamento de um app de IA de função única no Brasil (notas de 12/11/2026)

> Aviso de método: nesta sessão o acesso direto (fetch) às páginas oficiais de Apple, Google, OpenAI, Google AI, RevenueCat, Tecnoblog e outras estava bloqueado pela rede. A única página oficial lida na íntegra foi a de preços da Anthropic. Todo o resto vem de resultados de busca (trechos de páginas oficiais e de terceiros). Onde o número vem de blog de fornecedor/agregador, isso está indicado. Preços devem ser reconferidos na página oficial antes de virar "fato" no relatório.

## 1. Stack de construção em 2026 (ferramentas, preços, quem publica nas lojas)

### Takeaway
O caminho barato e realista para quem programa pouco é: um construtor "prompt para app mobile" (Rork ou a0.dev, ~US$20-25/mês) ou Claude Code/Cursor (~US$20/mês) gerando React Native/Expo, com Supabase (grátis), RevenueCat (grátis até US$2.500/mês de receita) e PostHog (grátis até 1M eventos). Lovable e Bolt geram web apps (bons para PWA/web-to-app), não apps nativos de loja.

### Cited Findings
**Construtores "prompt to app"**
- Rork, Bolt e Lovable começam todos em torno de US$20-25/mês; a0.dev começa em US$20; Rork e a0.dev usam créditos e "o modelo de créditos é a reclamação mais comum" (gerações falhas queimam a cota) — fontes de terceiros, não páginas oficiais — [vp0 – AI app builder pricing compared 2026](https://vp0.com/blogs/ai-app-builder-pricing-compared-2026/); [vp0 – a0.dev vs Rork](https://vp0.com/blogs/a0-dev-vs-rork)
- Rork é o único dos quatro (Rork, a0, Lovable, Bolt) construído para mobile nativo; Bolt e Lovable constroem web apps; "mobile" em demos do Bolt é web responsivo — [vp0 – Rork vs Bolt](https://vp0.com/blogs/rork-vs-bolt); [playcode – Best mobile app builders 2026](https://playcode.io/blog/best-ai-mobile-app-builders-2026)
- Rork publica na App Store e gera iOS/Android/web; fontes divergem sobre a arquitetura: uma diz que Rork migrou para Swift nativo compilado na nuvem, outra ainda descreve React Native (Expo). Reviews no Trustpilot citam falhas de publicação — [playcode](https://playcode.io/blog/best-ai-mobile-app-builders-2026); [nocode.mba – Rork review 2026](https://www.nocode.mba/articles/rork-ai-review-2026)
- a0.dev (YC) gera apps React Native/Expo a partir de texto; uma fonte diz "publicação em um clique" na App Store e Google Play, outra diz que só documenta a rota App Store (conflito não resolvido) — [vp0 – a0.dev vs Rork](https://vp0.com/blogs/a0-dev-vs-rork); [appypie – AI mobile app builders compared](https://www.appypie.com/blog/ai-mobile-app-builders-compared)
- Lovable: Free; Pro US$25/mês; sem suporte mobile nativo (precisa de wrapper). Bolt: Free; Pro US$20-25/mês; faz Expo. Replit: Free; Core US$20-25/mês (fontes divergem) — [vibecodingacademy – Lovable vs Bolt vs Replit 2026](https://www.vibecodingacademy.ai/blog/lovable-vs-bolt-vs-replit-comparison-2026); [dupple – best vibe coding tools](https://dupple.com/learn/best-vibe-coding-tools)

**Assistentes de código**
- Claude Code está incluído no plano Claude Pro a partir de US$20/mês, com limites maiores nos planos Max — [automationatlas – custo de assistentes de código 2026](https://automationatlas.io/answers/how-much-do-ai-coding-assistants-cost-2026/)
- Cursor: segundo leitura da página de preços em 02/11/2026, os planos pagos custam US$30, US$100 ou US$200/mês; o antigo Pro de US$20 virou plano legado. Combinação comum citada: Cursor + Claude Code ≈ US$40/mês — [morphllm – best vibe coding tools](https://morphllm.com/best-vibe-coding-tools); [founderstoolkit](https://founderstoolkit.pages.dev/blog/best-ai-coding-tools-solo-founders-2026)

**Build/Deploy (Expo EAS)**
- Expo EAS Free: US$0 com 15 builds Android + 15 builds iOS por mês; Starter US$19/mês + uso; Production US$199/mês + uso (leitura de outubro/2026) — [Expo pricing](https://expo.dev/pricing.md); [docs.expo.dev – plans](https://docs.expo.dev/billing/plans/)

**Backend**
- Supabase: Free US$0; Pro US$25/mês; Team US$599/mês — [schematichq – Supabase pricing 2026](https://schematichq.com/blog/supabase-pricing); [costbench – Supabase](https://costbench.com/software/developer-tools/supabase-dev/)

**Assinaturas e paywalls**
- RevenueCat: grátis até US$2.500 de receita mensal rastreada (MTR), depois 1% da receita rastreada; a taxa incide sobre a receita bruta (antes do corte da Apple/Google) — [costbench – RevenueCat](https://costbench.com/software/subscription-billing/revenuecat/); [pricepush – MTR](https://pricepush.app/glossary/monthly-tracked-revenue)
- Superwall: mudou de preço por conversão para % da receita atribuída (MAR); abaixo de US$10 mil de MAR é grátis — [Superwall docs – pricing FAQ](https://superwall.com/docs/support/faq/2801653905-how-does-superwalls-pricing-work); [Superwall pricing](https://superwall.com/pricing.md)
- Adapty: desde fevereiro/2026, grátis para apps com menos de US$5.000/mês de receita; acima disso 1% — [Adapty blog – new pricing 2026](https://adapty.io/blog/adapty-new-pricing-2026/)

**Analytics**
- PostHog: plano grátis com até 1 milhão de eventos/mês — [costbench – PostHog free plan](https://costbench.com/software/product-analytics/posthog/free-plan/)
- Mixpanel: fontes divergem (1M eventos/mês grátis vs. 100 mil MTUs grátis) — [costbench – PostHog vs Mixpanel](https://costbench.com/compare/posthog-vs-mixpanel/)

### Inferences
- "Lista de compras" mínima de software para um app nativo: construtor/assistente de IA (US$20-25/mês) + Expo EAS (US$0) + Supabase (US$0) + RevenueCat (US$0) + PostHog (US$0) = ~US$20-25/mês antes das taxas de loja.
- Para quem não programa, o risco dos construtores não é o preço de tabela, e sim o consumo de créditos em iterações/bugs e a etapa de publicação (certificados, builds, rejeições), que continua exigindo conta própria de desenvolvedor Apple/Google.
- MMPs de atribuição (AppsFlyer, Adjust) são dispensáveis no MVP; RevenueCat + PostHog + os painéis das próprias plataformas de anúncio bastam para as primeiras semanas.

### Gaps
- Não foi possível ler as páginas oficiais de preços de Rork, a0.dev, Lovable, Bolt, Replit, Cursor, Firebase, AppsFlyer e Adjust; os valores acima são de comparativos de terceiros. Preços de AppsFlyer/Adjust e limites do Firebase Spark/Blaze e do Supabase Free não foram levantados.
- Arquitetura atual do Rork (Swift nativo vs. Expo) e rota do a0.dev para Google Play: fontes em conflito.
- Flutter e SwiftUI não foram pesquisados em detalhe (sem achados citáveis).

## 2. Custo dos modelos de IA (visão) e bases brasileiras de alimentos

### Takeaway
O custo de IA por foto é irrelevante frente ao preço da assinatura: com modelos pequenos fica na ordem de frações de centavo de dólar por foto. A TACO (Unicamp) permite reprodução com citação da fonte; os termos da TBCA (USP) não foram confirmados.

### Cited Findings
**Anthropic (página oficial lida em 12/11/2026, US$ por milhão de tokens, entrada/saída)**
- Claude Haiku 5.5: US$0,10 / US$0,50 (prompts até 100 mil tokens); Claude Haiku 4.5: US$1 / US$5; Claude Sonnet 5 e Sonnet 5.5: US$2 / US$10; Claude Opus 5.5: US$4 / US$20; Claude Opus 5: US$5 / US$25 — [Anthropic – Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Modelos Claude 4.7 em diante usam tokenizador novo que gera ~30% mais tokens para o mesmo texto — [Anthropic – Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Batch API da Anthropic custa 50% do preço (ex.: Sonnet 5 a US$1 / US$5) — [Anthropic – Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**Google Gemini (via busca; não foi possível abrir a página oficial)**
- Gemini 3.6 Flash: preço introdutório de US$0,75 / US$3,75 por 1M tokens até 31/12/2026; preço padrão de US$1,50 / US$7,50 a partir de 01/01/2027 — [Google Cloud – Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- Gemini 3.5 Flash-Lite: US$0,30 entrada (texto, imagem, vídeo, áudio) / US$2,50 saída; Gemini 3.1 Flash-Lite: US$0,25 / US$1,50 (arquivo de julho/2026 de terceiro) — [usagepricing – Gemini](https://www.usagepricing.com/blueprint/activity/google-gemini-2026-07-28-gemini-36-flash-ai-plus)
- Desde abril/2026 os modelos Pro saíram do nível gratuito da API; Flash e Flash-Lite continuam com nível gratuito, com cotas diárias menores; dados do nível gratuito podem ser usados para melhorar produtos do Google — [findskill – Gemini API pricing guide](https://www.findskill.ai/blog/gemini-api-pricing-guide/)

**OpenAI (via agregadores; não confirmado na página oficial)**
- GPT-5.4-mini: US$0,75 / US$4,50; GPT-5.4-nano: US$0,20 / US$1,25; GPT-5.5: US$5 / US$30; entrada em cache ~90% mais barata; Batch API com 50% de desconto — [morphllm – OpenAI API pricing](https://morphllm.com/openai-api-pricing); [costbench – OpenAI API](https://costbench.com/software/llm-api-providers/openai-api/)
- Agregadores divergem sobre modelos mais novos (ex.: "Luna" a US$0,10/US$0,50 em uma fonte e US$1/US$6 em outra) — [costbench – OpenAI API](https://costbench.com/software/llm-api-providers/openai-api/)

**Bases de composição de alimentos**
- TACO, 4ª edição revisada e ampliada (2011, NEPA/Unicamp, 161 páginas): a publicação traz o aviso de que a reprodução total ou parcial é permitida desde que citada a fonte; não há nome de licença formal (tipo Creative Commons) — [BVS – TACO](https://search.bvsalud.org/gim/resource/en/lil-643323); [cópia da 4ª ed. em disciplina da USP](https://edisciplinas.usp.br/mod/resource/view.php?id=2301180)
- TBCA é mantida pelo Food Research Center (FoRC/USP); a citação sugerida indica versão 7.3 (2025) — [TBCA](https://tbca.net.br/indexen.html); [CFN – nova versão da TBCA](https://cfn.org.br/ja-esta-no-ar-a-nova-versao-da-tabela-brasileira-de-composicao-de-alimentos-tbca/)

### Inferences
- Estimativa própria (premissa: ~1.500 tokens de entrada por foto + prompt e ~300 tokens de saída em JSON; a contagem real de tokens por imagem varia por modelo e resolução): Haiku 5.5 ≈ US$0,0003/foto; GPT-5.4-nano ≈ US$0,0007; Gemini 3.1 Flash-Lite ≈ US$0,0008; Gemini 3.6 Flash ≈ US$0,0023; GPT-5.4-mini ≈ US$0,0025; Haiku 4.5 ≈ US$0,003; Sonnet 5 ≈ US$0,006.
- Usuário ativo com 3 fotos/dia (90 fotos/mês): de ~US$0,03 (Haiku 5.5) a ~US$0,55 (Sonnet 5) por mês. Mesmo o cenário caro é menos de R$4/mês por usuário pagante; o custo de IA não é o gargalo do modelo de negócio.
- O aviso "permitida a reprodução desde que citada a fonte" da TACO não é uma licença comercial explícita para redistribuir a base dentro de um app; o prudente é citar a fonte e pedir confirmação por escrito (taco@unicamp.br).

### Gaps
- Preços oficiais de OpenAI e Gemini AI Studio não puderam ser lidos; tokens por imagem de cada modelo não confirmados.
- Termos de uso/licença da TBCA para uso comercial não encontrados.
- Preços de modelos abertos via provedores (Together, Groq, OpenRouter etc.) não pesquisados.
- Não foram buscados testes independentes de precisão de calorias por foto.

## 3. Requisitos das lojas para desenvolvedor brasileiro

### Takeaway
Apple: US$99/ano, pessoa física (CPF) ou MEI se inscrevem como "individual" sem D-U-N-S; revisão típica de 1-2 dias. Google Play: conta pessoal nova precisa de teste fechado com 12 testadores por 14 dias contínuos antes de produção, o que faz a primeira publicação Android levar ~3 semanas. Desenvolvimento de software não é atividade permitida ao MEI.

### Cited Findings
**Apple Developer Program**
- Anuidade de US$99 tanto para pessoa física quanto organização; preços são exibidos em moeda local na inscrição — [Apple – inscrição](https://developer.apple.com/br/support/enrollment/); [TabNews – o que a Apple realmente exige](https://www.tabnews.com.br/adevelop/inscricao-no-apple-developer-program-o-que-a-apple-realmente-exige-e-onde-as-pessoas-travam)
- Empresário individual/sociedade unipessoal deve se inscrever como pessoa física e o nome civil aparece como vendedor na App Store; pessoa física não precisa de D-U-N-S; organização precisa de D-U-N-S (e CNPJ) — [Apple – D-U-N-S](https://developer.apple.com/br/help/account/membership/D-U-N-S/); [Apple – inscrição no programa](https://developer.apple.com/br/help/account/membership/program-enrollment/)
- Relato de terceiro: tentar inscrição de organização com MEI tende a ser reprovado — [TabNews](https://www.tabnews.com.br/adevelop/inscricao-no-apple-developer-program-o-que-a-apple-realmente-exige-e-onde-as-pessoas-travam)
- Há relato em fórum da Apple (2026) de inscrições no Brasil travadas em "purchase your membership" com cobrança que não é efetivada — [Apple Developer Forums](https://developer.apple.com/forums/thread/838891)
- Relato não confirmado oficialmente: a Apple estaria pedindo CNPJ no lugar de CPF para continuar pagando desenvolvedores, ligado a um "CNPJ para pessoa física" da reforma tributária com obrigatoriedade em 01/01/2027 — [TabNews](https://www.tabnews.com.br/marcelxsilva/a-apple-esta-pedindo-cnpj-no-lugar-do-cpf-para-continuar-pagando-voce-mas-calma)

**Google Play Console**
- Contas pessoais criadas após 13/11/2023 precisam rodar teste fechado com pelo menos 12 testadores inscritos continuamente por 14 dias antes de pedir acesso à produção; contas de organização e contas pessoais antigas são isentas; o requisito caiu de 20 para 12 testadores em dezembro/2024 — [Google Play Console Help](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en-GB); [testerscommunity – 12 testers policy 2026](https://www.testerscommunity.com/guides/how-many-testers-do-you-need-google-play)
- Uma fonte afirma que em 2026 passaram a ocorrer rejeições por "engajamento insuficiente" dos testadores (fonte única, comercial) — [testerscommunity](https://www.testerscommunity.com/blog/google-play-closed-testing-requirements-2026)

**Tempos de revisão**
- Apple declara que ~90% das submissões são revisadas em menos de 24 horas (leitura de terceiro); blogs indicam 24-72h, com picos de 5-7 dias; há tópicos no fórum da Apple sobre atrasos em outubro/2026 — [Adalo – App Store review time 2026](https://studio.adalo.com/blog/how-long-does-app-store-review-take); [Apple Developer Forums – atrasos out/2026](https://developer.apple.com/forums/thread/852614)
- Google Play: de horas a alguns dias, podendo chegar a 7 dias ou mais; para conta pessoal nova, um dado isolado fala em ~5 dias na App Store vs. ~3 semanas no Google Play — [choicely – how long does app review take](https://www.choicely.com/tutorials/how-long-does-app-review-take); [ptkd – Google Play review time](https://ptkd.com/journal/google-play-review-time)

**Comissões (ver também seção 4)**
- No Brasil, após o acordo com o CADE, a Apple anunciou comissão reduzida de 10% para a maioria dos desenvolvedores (inclui Small Business Program), mais taxa de 5% de processamento quando se usa o In-App Purchase da Apple — [Apple Newsroom, junho/2026](https://www.apple.com/br/newsroom/2026/06/apple-announces-changes-to-ios-in-brazil/); [Appcharge – Apple Brazil framework](https://appcharge.com/blog/apple-brazil-framework-is-now-live-what-publishers-need-to-know)

**Regras de IA e saúde**
- Em 13/11/2025 a Apple revisou a diretriz 5.1.2(i): apps devem divulgar claramente e obter permissão explícita do usuário antes de compartilhar dados pessoais com IA de terceiros — [TechCrunch](https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai)
- Interpretação de blogs (não texto da Apple): linha na política de privacidade não basta; precisa de tela de consentimento no app nomeando o provedor de IA. Há relatos de rejeição por 5.1.2(i) no fórum da Apple — [dev.to – guideline 5.1.2(i)](https://dev.to/arshtechpro/apples-guideline-512i-the-ai-data-sharing-rule-that-will-impact-every-ios-developer-1b0p); [Apple Developer Forums – app rejeitado](https://developer.apple.com/forums/thread/816140)
- Exemplo de aviso usado por app brasileiro de calorias por foto: "não substitui a orientação de nutricionistas ou profissionais de saúde" — [App Store – Olho no Prato](https://apps.apple.com/br/app/id6757802677)

**Tributação no Brasil**
- Desenvolvedor de software/aplicativos não pode ser MEI (atividade intelectual, vedada); o caminho é ME no Simples Nacional; CNAE mais citado 6201-5/01 — [contabilidade.com – desenvolvedor pode ser MEI em 2026?](https://contabilidade.com/blog/desenvolvedor-pode-ser-mei-em-2026-veja-como-abrir-cnpj-escolher-o-cnae-ideal-e-pagar-menos-impostos/); [Agilize – CNAE para desenvolvedor](https://agilize.com.br/artigos/qual-cnae-para-programador)
- Simples Nacional: alíquota inicial de 6% no Anexo III ou 15,5% no Anexo V; o Fator R (folha/receita dos últimos 12 meses ≥ 28%) decide o Anexo III — [Agilize – impostos no Simples para desenvolvedor](https://agilize.com.br/artigos/?p=4996)
- Fontes divergem sobre exportação de serviços no Simples (uma diz que se desconsideram PIS/Cofins/ISS; outra diz tributação integral). A Solução de Consulta Cosit nº 185/2025 (sobre anúncios na internet) concluiu que não é receita de exportação de serviços no Simples mesmo com pagamento intermediado por plataforma no exterior — [SC Cosit 185/2025](https://rota.apet.org.br/wp-content/uploads/2025/09/SC-Cosit-no-185-2025.pdf); [contabilidade.com – serviço para o exterior](https://contabilidade.com/blog/prestacao-de-servico-para-o-exterior-paga-imposto/)

### Inferences
- Rota mais rápida de loja: Apple primeiro (pessoa física com CPF, sem D-U-N-S, revisão em dias). Para Android, abrir a conta e iniciar o teste fechado de 14 dias no dia 1, em paralelo.
- Como o app vende a consumidores brasileiros, é arriscado presumir tratamento de "exportação de serviços" para a receita das lojas; a SC Cosit 185/2025 aponta no sentido contrário para caso análogo. Precisa de contador.
- Um app de calorias por foto que envia a imagem a OpenAI/Google/Anthropic cai diretamente na 5.1.2(i): planejar tela de consentimento antes da primeira foto.

### Gaps
- Taxa de US$25 do Google Play e verificação de identidade: não confirmadas em fonte nesta sessão (página oficial bloqueada).
- Formulários fiscais exigidos pela Apple/Google de brasileiros (W-8BEN etc.), retenções e emissão de nota fiscal para receita de loja: sem fonte confiável.
- Regras de divulgação de assinatura (Apple 3.1.2 / política de assinaturas do Google) e regras de alegações de saúde das lojas: não levantadas em fonte primária.
- Texto oficial atual da diretriz 5.1.2(i) não pôde ser lido.

## 4. Como cobrar no Brasil (lojas, Pix, links externos, checkouts)

### Takeaway
Desde 18/06/2026 a Apple permite no Brasil meios de pagamento alternativos e links externos em apps (acordo com o CADE), mas com comissão: cerca de 15% no link externo. A Apple não aceita Pix na App Store; o Google Play aceita Pix apenas para compras avulsas (não confirmada a aceitação em assinaturas). O funil web com Pix (Asaas, Mercado Pago, Stripe) custa de R$0,99-1,99 fixos a ~1% por transação.

### Cited Findings
**Apple / CADE**
- As mudanças do acordo Apple-CADE entraram em vigor em 18/06/2026: desenvolvedores podem oferecer meios de pagamento próprios dentro do app e links para sites externos, exibidos lado a lado com o pagamento da App Store; lojas de apps alternativas passam a ser permitidas (uma fonte, TNH1, cita 18 de outubro, aparentemente erro) — [Olhar Digital](https://olhardigital.com.br/2026/06/18/pro/apple-agora-o-ios-e-aberto-no-brasil/); [TecMundo](https://www.tecmundo.com.br/mercado/413975-apple-oficializa-lojas-externas-no-brasil-e-outros-meios-de-pagamento-na-app-store.htm)
- Faixas de comissão reportadas: 15% a 26% usando integralmente o sistema da Apple; 10% a 21% com pagamento alternativo dentro do app; 10% a 15% para pagamentos concluídos fora do app (link); 5% para lojas alternativas — [Letsmoney](https://www.letsmoney.com.br/noticias/apple-cade-iphone-brasil-lojas-pagamentos-alternativos/); [Convergência Digital](https://convergenciadigital.com.br/mercado/apple-abre-iphones-para-lojas-de-terceiros-mas-ainda-fecha-porta-para-o-pix-por-aproximacao/)
- Conflito: reportagens pré-lançamento baseadas em documentos do CADE citavam comissão padrão de 25% (em vez de 21%) e 15% para direcionamento externo — [MacMagazine, 23/12/2025](https://macmagazine.com.br/post/2025/12/23/apple-permitira-compras-externas-e-lojas-alternativas-a-app-store-no-brasil/); [MacRumors](https://www.macrumors.com/2025/12/24/new-app-store-fee-structure-in-brazil/)
- Apps usados por menores de 18 anos não podem incluir links externos de compra; em compras por meios alternativos a Apple não processa reembolsos — [Tribuna do Sertão](https://www.tribunadosertao.com.br/mundo-tech/2026/06/19/924661-apple-abre-iphone-para-outras-lojas-de-aplicativos-e-carteiras-virtuais)
- Apple afirma que 86% dos desenvolvedores no Brasil são isentos de taxas — [Tribuna do Sertão](https://www.tribunadosertao.com.br/mundo-tech/2026/06/19/924661-apple-abre-iphone-para-outras-lojas-de-aplicativos-e-carteiras-virtuais)
- A Apple continua resistindo a abrir sua plataforma ao Pix (o acordo não cobre Pix por aproximação); nenhuma fonte encontrada indica Pix como forma de pagamento da App Store — [Convergência Digital](https://convergenciadigital.com.br/mercado/apple-abre-iphones-para-lojas-de-terceiros-mas-ainda-fecha-porta-para-o-pix-por-aproximacao/); [Correio](https://www.correio24horas.com.br/economia/fim-de-teto-do-pix-por-aproximacao-de-r500-esbarra-em-disputa-com-a-apple-e-deixa-iphone-de-fora-0626)

**Google Play**
- Google Play aceita Pix desde 06/03/2024, somente para compras avulsas; não vale para assinaturas com renovação automática — [Blog do Google Brasil](https://blog.google/intl/pt-br/produtos/android-chrome-play/google-play-pix-chega-a-loja-de-apps-e-amplia-opcoes-de-pagamento/); [Tecnoblog](https://tecnoblog.net/noticias/google-play-agora-aceita-pix-para-pagar-apps-e-games/)
- Um guia de 2026 (sem fonte oficial) diz que Pix pode renovar "certas assinaturas" — não confirmado — [GameOverDrive](https://gameoverdrive.com.br/como-comprar-jogos-itens-android-sem-cartao-credito/)
- Mobile Time (04/03/2026) noticiou que desenvolvedores Android poderão usar pagamento próprio ou links externos; não ficou claro se vale para o Brasil; outra fonte diz que a política vale só para usuários nos EUA — [Mobile Time](https://www.mobiletime.com.br/noticias/04/03/2026/google-play-fim-monopoli/); [games.gg](https://games.gg/pt-BR/news/google-atualiza-politicas-da-play-store/)

**Checkouts e gateways (web-to-app)**
- Asaas (tabela padrão, out/2026): R$1,99 por Pix ou boleto recebido; cartão à vista 2,99% + R$0,49; sem mensalidade; promoção de 3 meses para novos clientes: R$0,99 por Pix/boleto e 1,99% + R$0,49 no cartão — [Asaas – preços e taxas](https://www.asaas.com/precos-e-taxas); [Quasa](https://quasa.io/pt/media/asaas-ou-iugu-tarifa-publicada-vence-ate-o-volume-pedir-proposta)
- Asaas: Pix Automático sem custo adicional, segue a tarifa do Pix comum — [Blog Asaas – Pix Automático](https://blog.asaas.com/release/pix-automatico/amp/)
- Stripe Brasil: cartão nacional 3,99% + R$0,39; Pix 1,19% (comparativos de terceiros) — [paritydeals – gateways Brasil 2026](https://www.paritydeals.com/blog/best-payment-gateways-brazil-2026/); [ecomcalctools – Stripe vs PayPal Brasil](https://ecomcalctools.com/pt-br/blog/stripe-vs-paypal-brasil/)
- Stripe Brasil aceita conta de pessoa física (CNPJ opcional; representante precisa de CPF) — [Stripe Support – Brasil](https://support.stripe.com/questions/brazil-specific-information-to-open-a-stripe-account?locale=pt-BR)
- Mercado Pago (checkout online): Pix 0,99%; crédito à vista 4,98% com recebimento na hora (comparador de terceiros) — [idinheiro – melhores gateways](https://www.idinheiro.com.br/negocios/melhores-gateways-de-pagamento/)
- Pagar.me: Pix 1,19%; cartão varia muito entre fontes (3,99% + R$0,40 a 5,59%) — [Nuvemshop – gateways 2026](https://www.nuvemshop.com.br/blog/gateway-de-pagamento-mais-barato/); [Shopify – serviços de pagamento](https://www.shopify.com/br/blog/servicos-de-pagamento-para-empresas)
- Hotmart: 9,9% + R$2,49 por venda desde 21/09/2026 (antes 9,9% + R$1,00). Kiwify: 8,99% + R$2,49 por venda aprovada; Pix liberado em 2 dias, cartão em 15 dias (blogs/comparativos) — [HeroSpark – taxas das plataformas 2026](https://herospark.com/guias/taxas-e-margem); [Contabilidade Zen – tabela de taxas 2026](https://www.contabilidadezen.com.br/blog/tabela-taxas-plataformas-digitais-2026/)
- O Banco Central permite que instituições cobrem das empresas pelo Pix Automático; é gratuito para pessoas físicas — [Jornal Contábil](https://www.jornalcontabil.com.br/noticia/quais-sao-os-beneficios-do-pix-para-quem-e-microempreendedor-individual/)

**Preços praticados no Brasil por apps de calorias com IA**
- Olho no Prato (iPhone): R$9,90/mês e R$49,90/ano — [App Store](https://apps.apple.com/br/app/id6757802677)
- Pratoly AI (web): 3 análises grátis; Pro R$19,90/mês com 80 análises por ciclo — [TabNews](https://www.tabnews.com.br/RafaSS/pitch-criei-o-pratoly-ai-estime-as-calorias-do-seu-prato-usando-apenas-uma-foto)
- Cal AI: sem tabela pública; relatos de ~US$2,99/semana a US$49,99/ano, variando por região e teste A/B; MyFitnessPal anunciou a aquisição do Cal AI em 2026 — [eesel – preços Cal AI 2026](https://www.eesel.ai/pt/blog/cal-ai-pricing)

### Inferences
- Numa assinatura de R$14,99: Asaas via Pix fica com R$1,99 (13%) na tabela padrão; Mercado Pago ~R$0,15 (0,99%); Stripe ~R$0,18 (1,19%); Kiwify ~R$3,84 (25,6%); Apple IAP no Small Business ~15% (R$2,25). Para tíquete baixo, taxa fixa pesa muito; percentuais (Mercado Pago/Stripe) ou plano anual são mais eficientes.
- Link externo dentro do app iOS no Brasil não é "taxa zero": ~10-15% à Apple mais a taxa do gateway. A economia real vem de vender na web antes do app (funil web-to-app), onde a comissão da loja não incide.
- Como nem Apple nem Google cobram assinatura por Pix (até onde foi possível confirmar), oferecer Pix/Pix Automático no checkout web é o diferencial para o público sem cartão.

### Gaps
- Faixas de preço regionais em R$ da App Store/Google Play e lista oficial de meios de pagamento aceitos pela Apple no Brasil: não levantadas.
- Taxas oficiais de Pix Automático de Mercado Pago, Pagar.me e Stripe: não encontradas.
- Existência de programa de faturamento alternativo/links externos do Google Play específico para o Brasil e sua taxa: não confirmada.
- Percentuais exatos da Apple no Brasil (21% vs. 25% padrão): reportagens em conflito; o comunicado oficial não pôde ser aberto.

## 5. Vender no mesmo dia: PWA/web app ou bot de WhatsApp

### Takeaway
Já existe uma categoria de "nutricionista de IA no WhatsApp" no Brasil cobrando ~R$10-15/mês via checkout web. Porém, desde 01/10/2026 a Meta cobra mensagens de serviço na API oficial (R$0,035 por mensagem após 1.000 grátis/mês por número), o que cria um custo variável relevante para um bot de alto volume.

### Cited Findings
**Exemplos brasileiros**
- FoodSnap ("Nutricionista e Personal Trainer com IA no WhatsApp"): R$5 no primeiro mês, depois R$14,99/mês — [FoodSnap](https://www.foodsnap.com.br/)
- Miafit ("assistente nutricional no WhatsApp"): oferta "por menos de 10 reais por mês" — [Miafit](https://miafit.app/oferta/)
- NutriYuu: alega ~90% de precisão na identificação de alimentos e porções (alegação do fornecedor, sem verificação) — [NutriYuu](https://nutriyuu.com/)
- Outros no mesmo formato: Lucy Fit, Wellmi, Zuppy, Dieta.AI ("conte calorias por foto com IA no WhatsApp"; Instagram com 78 mil seguidores) — [Lucy Fit](https://lucyfit.com.br/); [Wellmi](https://wellmi.com.br/); [Dieta.AI](https://dieta.ai/en); [Instagram @dieta.ai](https://www.instagram.com/dieta.ai/)
- Mannah/DHM: serviço de emagrecimento por WhatsApp com versões grátis e paga — [CNN Brasil](https://www.cnnbrasil.com.br/tecnologia/plataforma-usa-ia-e-desafios-em-rede-social-para-emagrecimento/)

**Custos e regras do WhatsApp Business Platform**
- Desde 01/10/2026 a Meta cobra por mensagem de serviço enviada pela API oficial, inclusive respostas livres dentro da janela de 24h; no Brasil, R$0,0350 por mensagem; cada número tem 1.000 mensagens de serviço grátis por mês (não cumulativas, sem desconto por volume); respostas de chatbots/IA de terceiros contam como mensagens de serviço — fontes são blogs de provedores — [Letalk](https://letalk.com.br/blog/cobranca-mensagens-de-servico-whatsapp/); [Opa Suite](https://www.opasuite.com.br/blog/cobranca-mensagens-servico-whatsapp-2026); [E-Commerce Brasil](https://www.ecommercebrasil.com.br/artigos/novo-custo-do-whatsapp-o-que-muda-a-partir-de-outubro-e-como-reduzir-o-impacto)
- Tarifas Brasil (tabela de 01/10/2026, via provedor): marketing ~R$0,3217 por mensagem; utilidade/autenticação/serviço ~R$0,035; desconto por volume só para utilidade e autenticação — [chatmaxima – preço da API no Brasil](https://chatmaxima.com/pt-br/whatsapp-api-pricing/brazil/)
- O app WhatsApp Business gratuito (respostas manuais) continua sem cobrança — [eazybe – preços da API](https://eazybe.com/br/blog/preco-api-whatsapp-business)
- Twilio cobra US$0,005 por mensagem (entrada ou saída) além das tarifas da Meta — [Twilio – WhatsApp pricing](https://www.twilio.com/en-us/whatsapp/pricing)
- Em outubro/2025 a Meta proibiu chatbots de IA de uso geral na API; a regra não afeta empresas que usam IA para atender os próprios clientes — [Olhar Digital](https://olhardigital.com.br/2025/10/18/pro/whatsapp-business-vai-proibir-chatbots-de-ia-entenda/)
- O CADE mandou a Meta suspender a regra; a Meta abriu exceção para números brasileiros (jan/2026) — [Startups.com.br](https://startups.com.br/negocios/cade-manda-meta-suspender-regra-que-barra-chatbots-de-ia-no-whatsapp/); [MacMagazine](https://macmagazine.com.br/post/2026/01/15/meta-abre-excecao-e-libera-chatbots-de-ia-para-o-whatsapp-no-brasil/)
- Em março/2026 a Meta anunciou cobrança de provedores de chatbots de IA no Brasil, cerca de R$0,33 por mensagem não padronizada; Zapia e Luzia disseram que isso inviabiliza seus serviços — [Tecnoblog](https://tecnoblog.net/noticias/meta-vai-cobrar-chatbots-de-ia-por-uso-do-whatsapp/); [Olhar Digital](https://olhardigital.com.br/2026/03/09/pro/meta-vai-cobrar-por-mensagens-enviadas-para-ias-no-whatsapp-entenda/)

### Inferences
- Custo de mensagens num bot de calorias: um assinante com 3 fotos/dia gera ~90-180 respostas/mês. Acima da franquia de 1.000 mensagens por número, isso é ~R$3-6/mês por usuário a R$0,035, ou 20-40% de uma assinatura de R$14,99. A franquia cobre só ~6-11 usuários ativos. Consolidar a resposta em uma única mensagem por foto é decisivo.
- Risco regulatório/comercial: não está claro se um "nutricionista de IA" vendido como produto é tratado pela Meta como empresa atendendo seus clientes (R$0,035) ou como "provedor de IA" (R$0,33 por mensagem). A R$0,33 o modelo de R$10-15/mês não fecha.
- PWA/web app com checkout Pix evita tanto a cobrança por mensagem quanto a espera das lojas, e ainda serve de funil web-to-app depois. O WhatsApp serve melhor como canal de aquisição/retensão do que como produto principal.
- Os concorrentes de WhatsApp ancoram o preço em R$10-15/mês, abaixo dos apps de loja internacionais.

### Gaps
- Preços e risco de banimento de APIs não oficiais (Z-API, Evolution API): nenhuma fonte encontrada.
- Tabela oficial da Meta para o Brasil e definição oficial de "AI provider": não lidas (apenas blogs de provedores e imprensa).
- Números de assinantes/receita dos bots brasileiros citados: não encontrados.
- Preço do Dieta.AI: não encontrado.

## 6. Go-to-market no Brasil (creators, anúncios, CONAR, LGPD)

### Takeaway
Mídia no Brasil é barata frente aos EUA (CPM do Meta estimado em ~US$3,5 vs. ~US$20 global em um benchmark automatizado), mas não há tabela confiável de preço de microcreators em R$: as faixas publicadas vão de ~R$100 por vídeo UGC em marketplace a R$600+ por Reels com direitos de uso. O novo Guia do CONAR (em vigor desde 01/06/2026) trata cupons e links de afiliado como publicidade.

### Cited Findings
**Creators e UGC**
- Exemplo de blog: creator com 15 mil seguidores e 8% de engajamento pode cobrar R$600 por um Reels com direitos de uso por 3 meses (exemplo ilustrativo, não pesquisa) — [agenciagram](https://agenciagram.com.br/blog/como-ser-micro-influenciador-instagram-2026)
- Produção de vídeo/Reels (sem publicação): R$300 a R$2.500 por vídeo — [FreelaSemCrise](https://www.freelasemcrise.com.br/quanto-cobrar/producao-reels)
- Noovid (marketplace UGC com creators do Brasil): marca paga ~€75 (15s) a €149 (60s) por vídeo com direitos vitalícios; a tabela de remuneração ao creator indica R$101 (15s) e R$131 (30s) — [Influee – Noovid](https://influee.co/br/blog/noovid-alternatives); [Quasa – plataformas UGC no Brasil](https://quasa.io/pt/media/qual-plataforma-ugc-paga-melhor-no-brasil)
- Billo: a partir de US$99 por vídeo; freelancers (Fiverr/Upwork): média de US$185 por vídeo de 30s — [Influencer Hero](https://www.influencer-hero.com/br/blogs/top-ugc-platforms-for-ecommerce-brands); [voxbooster – UGC stats 2026](https://voxbooster.com/pt-BR/blog/ugc-creator-statistics-2026)
- Estimativa de outro blog: R$800 a R$2.500 por vídeo UGC com creators humanos vs. ~R$10 com IA — [nemovideo](https://www.nemovideo.com/pt-BR/blog/ai-ugc-vs-traditional-ugc)
- Exclusividade e direitos de uso para mídia paga multiplicam o valor — [empreender.com.br](https://empreender.com.br/quanto-custa-contratar-um-influenciador/)

**Anúncios**
- CPM Meta no Brasil (blog de agência, abril/2026): R$15-35 no Feed e R$8-20 em Stories/Reels — [Trafius](https://trafius.com.br/blog/cpm-medio-facebook-ads-brasil-2026)
- Benchmark automatizado (nov/2025 a out/2026): CPM do Brasil ~US$3,46 vs. ~US$20,59 de média global (~83% abaixo) — [Superads](https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/brazil)
- CPC médio do Facebook no Brasil: US$0,25 a US$1,20 em 2026 — [NovoAds](https://novoads.ai/pt-br/resources/quanto-custa-publicidade-no-meta)
- CPI global (Singular, Q2 2026): iOS US$3,03; Android US$0,76; em saúde e fitness (Q4 2025), instalações 50/50 entre iOS e Android, mas iOS gerou 94% da receita — [Singular Q2 2026](https://www.singular.net/pt/quarterly-report-2026-q2/); [Singular Q4 2025](https://www.singular.net/pt/quarterly-report-2025-q4/)
- Apple Search Ads está disponível no Brasil desde 23/04/2024 — [9to5Mac](https://9to5mac.com/2024/02/22/apple-search-ads-expands-to-brazil-and-eight-more-countries/); [MacMagazine](https://macmagazine.com.br/post/2024/04/24/apple-search-ads-no-brasil-e-no-mundo-como-lancar-e-escalar/)
- Brasil liderou em 2025 a taxa de conversão do Apple Search Ads (72,51%); CPT mediano global ~US$0,92 e EUA US$1,91 — [MobileAction – region analysis](https://www.mobileaction.co/report/apple-search-ads-2025-benchmark-report/region-analysis/); [AppTweak – Apple Ads benchmarks](https://www.apptweak.com/en/aso-blog/apple-ads-benchmarks)

**CONAR**
- Nova edição do Guia de Publicidade por Influenciadores Digitais, vigente desde 01/06/2026, substitui a de 2020; recomenda priorizar as ferramentas de sinalização de conteúdo pago das próprias plataformas em vez de só "#publi"; links comissionados, cupons e programas de afiliados passam a ser considerados publicidade; amplia regras sobre crianças/adolescentes e uso de IA — [Migalhas](https://www.migalhas.com.br/depeso/456124/guia-conar-2026-o-que-todo-influenciador-precisa-saber-agora); [Meio & Mensagem](https://www.meioemensagem.com.br/midia/conar-atualiza-guia-para-influenciadores-digitais); [Contábeis](https://www.contabeis.com.br/artigos/77061/conar-novas-regras-para-influenciadores-e-ia-a-partir-de-1o-de-junho/)

**LGPD**
- Agentes de pequeno porte (Resolução CD/ANPD nº 2/2022) são dispensados de indicar encarregado (DPO), mas devem manter canal de comunicação com o titular; a dispensa não vale para quem faz tratamento de alto risco e não isenta das demais obrigações (bases legais, princípios) — [Machado Meyer](https://www.machadomeyer.com.br/pt/inteligencia-juridica/publicacoes-ij/direito-digital/empresas-de-pequeno-porte-podem-ser-dispensadas-de-ter-dpo); [Resolução CD/ANPD nº 2/2022](https://www.gov.br/palmares/pt-br/midias/arquivos-menu-acesso-a-informacao/legislacao/resolucao-cd-anpd-n2-2022.pdf)
- "Alto risco" exige pelo menos um critério geral e um específico da Resolução — [Confidata](https://confidata.com.br/blog/lgpd-pequenas-empresas-resolucao-pequeno-porte)

### Inferences
- Um pacote de 10 vídeos de microcreators/UGC no Brasil deve ficar na faixa de ~R$1.000 a R$6.000, conforme canal (marketplace vs. negociação direta) e direitos de uso — estimativa a partir de fontes heterogêneas e de baixa confiabilidade.
- Programa de afiliados/cupom para creators é o modelo de menor desembolso inicial, mas pelo CONAR 2026 continua sendo publicidade e precisa de sinalização.
- Dados de peso, dieta e fotos de refeição vinculados a objetivos de saúde tendem a ser tratados como dado sensível (saúde) pela LGPD; combinados a uso de IA/tecnologia emergente, podem configurar "alto risco" e derrubar a dispensa de DPO. Isso é interpretação, não achado.
- A receita de assinatura em saúde/fitness concentra-se em iOS (94% no dado global da Singular), o que reforça lançar primeiro no iPhone, embora o Brasil seja majoritariamente Android.

### Gaps
- Preços por vídeo em R$ de BrandLovrs, Squid, Inflr e Influency.me; modelo de CPM/pagamento por visualização com creators; preços no Kwai: não encontrados.
- CPM/CPI de TikTok Ads no Brasil e CPI de saúde/fitness específico do Brasil: não encontrados.
- Regras específicas do CONAR e do CDC sobre alegações de emagrecimento/saúde: não localizadas; o PDF oficial do Guia 2026 não foi lido.
- Texto dos critérios de alto risco (arts. 4º e 5º da Resolução nº 2/2022) e orientação da ANPD sobre apps de saúde: não lidos.

## 7. Cronograma e orçamento realistas do MVP (rota mais barata)

### Takeaway
A rota mais barata e rápida até a primeira venda é web app/PWA com checkout Pix (primeira venda possível em dias, com ~US$20-25 de ferramenta), seguido de iOS (US$99/ano, revisão de ~1-2 dias) e Android por último por causa do teste fechado de 14 dias.

### Cited Findings
- Custos fixos confirmados em fonte: Apple Developer US$99/ano — [Apple](https://developer.apple.com/br/support/enrollment/); construtores de IA ~US$20-25/mês — [vp0](https://vp0.com/blogs/ai-app-builder-pricing-compared-2026/); Expo EAS grátis com 15+15 builds/mês — [Expo](https://expo.dev/pricing.md); RevenueCat grátis até US$2.500 de MTR — [costbench](https://costbench.com/software/subscription-billing/revenuecat/); Asaas sem mensalidade, R$1,99 por Pix — [Asaas](https://www.asaas.com/precos-e-taxas)
- Prazos confirmados em fonte: revisão Apple ~24-72h; Google Play com conta pessoal nova exige 14 dias de teste fechado com 12 testadores antes da produção — [Adalo](https://studio.adalo.com/blog/how-long-does-app-store-review-take); [Google Play Console Help](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en-GB)

### Inferences
- Cronograma estimado (inferência): Dia 1-3: landing + web app/PWA com upload de foto, chamada de modelo de visão e checkout Pix (Asaas/Mercado Pago/Stripe); primeiras vendas via creators/afiliados. Semana 1-2: app Expo com RevenueCat, tela de consentimento de IA (5.1.2(i)), envio à App Store. Dia 1 em paralelo: abrir conta Google Play e iniciar teste fechado, produção Android na semana 3-4.
- Orçamento estimado do primeiro mês (inferência): ferramenta de IA US$20-25; Apple US$99; domínio e hospedagem próximos de zero em planos gratuitos; API de IA abaixo de US$10 para as primeiras centenas de usuários; total de ferramentas ~US$130-150 (~R$700-900, câmbio não verificado). Marketing é a maior variável: de R$0 (afiliados) a R$1.000-6.000 (10 vídeos de creators).
- Abrir uma ME no Simples (em vez de MEI, vedado) acrescenta custo de contador mensal, não levantado aqui.

### Gaps
- Nenhuma fonte com cronograma/orçamento real e auditável de um MVP brasileiro deste tipo foi encontrada; tudo nesta seção é estimativa derivada das seções anteriores.
- Câmbio US$/R$ de novembro/2026 e custo de abertura/manutenção de ME (contador): não pesquisados.
