# Presente de fim de ano 2026 para empresas

Tábuas de churrasco em madeira maciça, feitas com o retalho da fábrica e com a marca da empresa compradora gravada. A MP vende para a empresa, e a empresa dá de presente para os clientes dela.

**Por que vale a pena agora:** as empresas do noroeste do Paraná fecham o presente de fim de ano entre meados de novembro e o começo de dezembro. Um único pedido pode ter de 50 a 300 peças. Quem recebe o presente é fazendeiro, empresário e gerente, ou seja, o mesmo cliente da porta pivotante e da cozinha planejada. Cada caixa leva um cartão com um QR para o WhatsApp da MP, então quem paga para a marca da MP chegar na mão desse cliente é a empresa que comprou o presente.

Criado em 09/11/2026. Tudo marcado com **[confirmar]** é estimativa até a MP passar o número real.

## O que tem nesta pasta

| Arquivo | Para quê |
|---|---|
| `precificacao-presentes-2026.xlsx` | Custo de cada kit, tabela de preço por quantidade e controle de pedidos com a capacidade da fábrica. As células amarelas são as premissas a confirmar. |
| `catalogo-presentes-2026.png` | Catálogo de 1 página para mandar no WhatsApp (a imagem abre na hora, sem baixar). |
| `catalogo-presentes-2026.pdf` | O mesmo catálogo em A4, para e-mail ou impressão. |
| `cartao-presente-2026.pdf` / `.png` | O cartão que vai dentro de cada caixa, em 9 × 5 cm, frente e verso. |
| `empresas-alvo.md` | Empresas reais da região para abordar, com fonte, e os preços de mercado pesquisados. |
| `gerador/` | O programa que monta o catálogo e o cartão (`gerar.py`). Também faz a **proposta personalizada** com o logo do cliente gravado na tábua. O `planilha.py` recria a planilha do zero; não rode depois de lançar pedidos, porque ele apaga a aba Pedidos. |

## Esta semana, antes de mandar o primeiro catálogo

1. **Responder 5 perguntas e corrigir a aba Premissas** (10 minutos):
   - Quanto custa a hora de fábrica, com encargos? (hoje está R$ 40)
   - Que madeiras sobram em retalho, e quanto por semana? Precisa ser maciça densa e **sem tratamento químico**: nunca pinus ou eucalipto autoclavado, nunca MDF.
   - Como gravar: a MP tem CNC? Conhece alguém com laser em Paranavaí ou Maringá? Ou prefere o ferro de marcar a fogo?
   - Qual a alíquota efetiva do Simples (pergunta para o contador)? Hoje está 8%.
   - Quantas horas por dia dá para tirar da produção para isso sem atrasar os planejados? Hoje está 8 h por dia, por exemplo 2 pessoas por 4 h.
2. **Fazer 1 protótipo de cada kit até quinta (12/11)** e cronometrar. O tempo real substitui as horas da aba Custos, e a tabela de preço se ajusta sozinha.
3. **Fotografar o protótipo do kit Churrasco** em três fotos: de cima, sobre fundo escuro; na mão de alguém, para dar a escala; e a gravação de perto. Depois rodar `python3 gerar.py --foto foto.jpg` para o catálogo sair com a foto real no lugar da ilustração.
4. **Cotar** faca e garfo inox no atacado, caixa kraft, saco de algodão cru e a impressão do cartão (couché 300 g, 9 × 5 cm, frente e verso).
5. **Perguntar ao contador** como sai a NF-e de venda de produto para empresa.

## Os três kits

| Kit | O que vai | Medidas | Mão de obra estimada |
|---|---|---|---|
| Essencial | Tábua de servir gravada, em saco de algodão cru, com cartão | 35 × 22 × 2,5 cm | 0,35 h [cronometrar] |
| **Churrasco** (o recomendado) | Tábua com canaleta para o caldo e alça de couro, gravada, em caixa kraft com cartão | 45 × 30 × 3 cm | 0,6 h [cronometrar] |
| Premium | Estojo de madeira com tampa gravada, tábua do Churrasco, faca e garfo trinchante inox | estojo sob medida | 1 h [cronometrar] |

Ficha técnica completa (madeira, acabamento, canaleta, gravação, embalagem) na aba **Custos** da planilha. Três regras não mudam:
- Só madeira maciça sem tratamento químico, com umidade até 12%.
- Acabamento atóxico: óleo mineral e cera de abelha, curado por 24 a 48 h antes de embalar. Verniz comum não pode, porque a peça encosta em comida.
- Tiras coladas com cola PVA D4 própria para contato indireto com alimento [confirmar a marca].

## Preço

A planilha calcula: **preço = custo direto ÷ (1 − imposto − comissão − margem)**, arredondado para cima com final ,90. A margem cai conforme a quantidade sobe, mas nunca fica abaixo de 25%.

Tabela atual, com os custos de referência e gravação a laser terceirizada a R$ 6 a peça (muda sozinha quando a MP preencher as premissas):

| Kit | 20 a 49 | 50 a 99 | 100 a 199 | 200 ou mais |
|---|---|---|---|---|
| Essencial | R$ 64,90 | R$ 59,90 | R$ 54,90 | R$ 49,90 |
| Churrasco | R$ 104,90 | R$ 94,90 | R$ 84,90 | R$ 79,90 |
| Premium | R$ 259,90 | R$ 234,90 | R$ 214,90 | R$ 199,90 |

Mais a **taxa de personalização de R$ 290 por pedido abaixo de 100 peças**, isenta a partir de 100. Ela cobre a arte e o ajuste da gravação e serve de argumento para o cliente subir de faixa.

**A faixa conta o total de peças do cliente.** Quem compra 20 Premium para os maiores clientes e 100 Churrasco para o resto paga o preço da faixa de 100 a 199 nos dois kits, sem taxa. A aba Pedidos já faz essa conta: lance cada kit numa linha com o mesmo nome de cliente. Ofereça essa combinação. É o jeito mais fácil de vender o Premium.

### Comparação com o mercado (pesquisa de 09/11/2026, fontes em `empresas-alvo.md`)

| O que o mercado vende | Preço por peça | Onde a MP fica |
|---|---|---|
| Tábua simples ou de bambu gravada, no atacado | R$ 22 a R$ 43 | A MP não compete aqui. O Essencial é maior e maciço, e o argumento é "não vai para a gaveta". |
| Tábua de 40 × 30 cm gravada | a partir de R$ 81 | **Churrasco: R$ 79,90 a R$ 104,90.** No preço do mercado, mas com madeira maciça, canaleta e alça. É o kit para empurrar. |
| Tábua, faca e garfo em estojo (10 a 200 peças) | R$ 89 a R$ 134 | **Premium: R$ 199,90 a R$ 259,90.** Custa o dobro porque o estojo também é de madeira maciça e leva duas gravações. É o kit VIP: poucas unidades, para os maiores clientes. |
| Caixa completa com 7 a 17 itens | R$ 80 a R$ 205 | Não fazemos. |

Quase todo kit do mercado usa tábua de bambu ou pinus. "Madeira maciça de verdade, feita por marcenaria" é o diferencial, e precisa aparecer em toda conversa.

**Gravação:** o laser terceirizado custa de R$ 2 a R$ 10 por peça em lote. O ferro de marcar personalizado custa de R$ 190 a R$ 850 e demora uns 20 dias para chegar. Por isso a planilha usa laser como padrão: com o ferro, um pedido fechado hoje só começaria a ser gravado em dezembro.

## Capacidade e prazos

Com 8 h por dia de 16/11 a 18/12, são **200 h de fábrica**, o que dá uns 330 kits Churrasco. A aba **Pedidos** soma as horas de cada pedido fechado e fica vermelha quando passa de 80%. Nesse ponto, ou a MP para de aceitar pedido grande ou aumenta as horas.

**Produzir as tábuas sem gravação desde já.** A gravação é a última etapa. Se a MP começar agora a cortar, colar, lixar e passar óleo num lote de tábuas lisas (por exemplo 50 do kit Churrasco), cada pedido que fechar só precisa de gravação e embalagem. Isso dá para aceitar pedido até 05/12 sem apertar a fábrica. O risco é baixo: tábua lisa que sobrar vende no Dia dos Pais, no TikTok Shop ou como produto da loja.

| Data | O quê |
|---|---|
| Seg 09 a qua 11/11 | Premissas confirmadas, protótipos, cotações |
| Qui 12/11 | Fotos dos protótipos, catálogo com foto, mensagem para a lista quente |
| Sex 13 a sex 28/11 | Abordagem: 10 empresas por dia, com os follow-ups abaixo |
| A partir de 16/11 | Lote de tábuas sem gravação; gravação e embalagem conforme os pedidos fecham |
| **28/11** | Último dia para pedidos de 100 peças ou mais |
| **05/12** | Último dia para qualquer pedido |
| **18/12** | Última entrega |

## Quem abordar, nesta ordem

1. **Lista quente, hoje.** Quem já conhece a MP fecha mais rápido.
   - Clientes antigos que têm empresa ou são gerentes.
   - Arquitetos e designers parceiros: muitos dão presente aos clientes na entrega da obra ou no fim do ano.
   - Construtoras, imobiliárias e lojas de material que já indicaram a MP.
   - Clientes da madeireira que são empresa.
2. **Associações comerciais da região.** Uma divulgação no grupo ou no informativo da ACI alcança centenas de empresas de uma vez.
3. **Lista fria:** `empresas-alvo.md`, começando pela prioridade A. São 36 empresas: 14 de prioridade A, 18 de prioridade B e 4 de prioridade C, das quais 5 são associações e sindicatos que servem de canal. As 10 melhores:
   - Cocamar e Cocamar Máquinas (John Deere), em Paranavaí
   - Usina Santa Terezinha (unidades de Paranacity e Terra Rica)
   - Sicredi Dexis e Cresol Pioneira, em Paranavaí
   - Sicredi Rio Paraná, com sede em Nova Londrina
   - Equagril (New Holland) e Prat's, em Paranavaí
   - Coopcana, em Paraíso do Norte
   - Podium Alimentos, em Tamboara

   A pesquisa não conseguiu abrir os sites oficiais, então confirme telefone e endereço antes de ligar. Em Alto Paraná não apareceu nenhuma empresa grande na internet: vale um levantamento presencial.

Lance cada contato na aba **Pedidos** como "Proposta enviada", mesmo antes de fechar, para ver as horas que estão em jogo.

## Mensagens prontas (WhatsApp)

Troque o que está entre colchetes. Mande o catálogo em PNG no WhatsApp e o PDF por e-mail.

**Primeira mensagem para empresa (dono, RH ou marketing)**
> Bom dia, [nome]! Aqui é o [seu nome], da MP Marcenaria, de Alto Paraná. A gente faz portas e móveis sob medida, e este ano abriu uma produção pequena de presente de fim de ano para empresas: tábua de churrasco em madeira maciça com a marca de vocês gravada.
> Posso te mandar o catálogo com os preços? É uma página só.

**Quando responder que sim**
> [catálogo em PNG]
> Para [quantidade] peças, o kit Churrasco sai a [preço] cada, já com a gravação, a caixa e um cartão com a mensagem da [empresa]. Se você me mandar o logo, hoje mesmo te devolvo a prévia de como fica na tábua.

A prévia é a proposta personalizada: `python3 gerar.py --empresa "[empresa]" --logo logo.png`. Ela sai com o logo gravado nas tábuas do catálogo e com o cartão assinado pela empresa.

**Follow-up 1, dois dias úteis depois, se não houver resposta.** Mande a proposta personalizada com o nome da empresa gravado, mesmo sem o logo.
> [nome], fiz uma prévia de como fica a tábua com a marca da [empresa], vai aqui. Os pedidos fecham dia 05/12 porque a gente produz aqui na fábrica, uma por uma.

**Follow-up 2, cinco dias úteis depois do primeiro contato.** É a última mensagem.
> Oi [nome], última mensagem sobre isso para não te encher. Se o presente deste ano já está resolvido, tudo certo. Se não, me fala a quantidade que eu seguro a vaga na produção até sexta.

**Cliente antigo que tem empresa**
> Oi [nome], tudo bem? Aqui é o [seu nome], da MP. Como está a [cozinha/porta] que a gente fez aí? Te chamei porque este ano estamos fazendo presente de fim de ano para empresas, tábua de churrasco com a marca gravada, e lembrei da [empresa]. Quer que eu te mande o catálogo?

**Arquiteto parceiro.** Sugestão: não cobrar a taxa de personalização de escritório parceiro. Ela custa pouco e abre a conversa do Clube do Arquiteto.
> Oi [nome]! Este ano a MP está fazendo tábua de churrasco em madeira maciça com a marca gravada. Muito escritório usa como presente de entrega de obra ou de fim de ano para os clientes. Se quiser, gravo o logo do escritório e te mando a prévia. Para escritório parceiro, a personalização sai sem custo.

**Ligação, em 30 segundos**
> Oi, [nome]? Aqui é o [seu nome], da MP Marcenaria, de Alto Paraná. Rapidinho: vocês já escolheram o presente de fim de ano para os clientes? A gente faz tábua de churrasco em madeira maciça com a marca da empresa gravada, a partir de [preço] a peça. Posso te mandar o catálogo no WhatsApp? É uma página.

**Quando disserem que está caro**
> Entendo. Tábua de MDF com adesivo sai mais barata, mas vai para a gaveta. Para caber no orçamento, tenho duas saídas: o kit Essencial, com a mesma madeira e a mesma gravação, a [preço]; ou, se a quantidade passar de 100, a taxa de personalização sai e o preço da peça cai para [preço].

**"Manda por e-mail"**: mande o PDF e avise no WhatsApp que mandou.

**"Quero ver pessoalmente"**
> Levo uma tábua até vocês em [cidade] esta semana. Que dia fica bom?

## A amostra que fecha pedido grande

Para as 10 empresas com maior potencial (as de prioridade A), vale levar **uma tábua de verdade com o logo delas já gravado**. Custa uns R$ 50 de peça (com a gravação avulsa a laser, de R$ 10 a R$ 50), mais o deslocamento, e é muito difícil recusar o próprio logo queimado na madeira. Só compensa com laser ou CNC: com ferro de marcar, cada amostra pediria um ferro novo.

## O cartão e o QR

O verso do cartão traz "Feita à mão em madeira maciça pela MP Marcenaria", os cuidados com a tábua e um QR que abre o WhatsApp da MP com uma mensagem pronta e um **código da empresa compradora** (por exemplo, N26-COOPX). Quando chegar uma mensagem com esse código, a MP sabe de qual presente veio o contato. Vale anotar isso num caderno ou numa aba nova da planilha.

Avise o comprador que o verso leva a assinatura da MP. É uma linha discreta, e os cuidados com a madeira justificam o cartão. Se ele pedir para tirar, tire.

Para gerar o cartão de cada cliente: `python3 gerar.py --empresa "[empresa]" --codigo N26-[SIGLA] --mensagem "[mensagem da empresa]"`.

## No Instagram, ao mesmo tempo

- **Reel do processo**: tiras sendo coladas, plaina, canaleta, óleo entrando na madeira, e no fim a gravação. O primeiro segundo é a gravação acontecendo, que é a imagem mais forte. Texto na tela: "Presente de empresa que não vai para a gaveta". CTA: "Comente PRESENTE que te mando o catálogo". Para o roteiro completo, use a skill `/ig-reel`.
- **Stories por 3 dias**: enquete "Sua empresa já escolheu o presente de fim de ano?" e, em seguida, o catálogo com o link do WhatsApp.

## Condições comerciais

- Pedido mínimo de 20 peças.
- Sinal de 50% para entrar na fila de produção; o restante na entrega, com NF-e.
- A arte é aprovada por escrito no WhatsApp antes de gravar.
- Entrega pela MP no noroeste do Paraná [confirmar o raio sem frete]. Outras cidades com frete à parte.
- Cada peça tem veio e tom diferentes. Isso está no catálogo e precisa estar na proposta.

## Depois do Natal

A mesma tábua é o presente mais óbvio do **Dia dos Pais (agosto de 2027)** e do churrasco de fim de semana o ano inteiro. O que sobrar de estoque, as fotos e os vídeos desta campanha viram a primeira linha da loja de decoração (skill `mp-tiktok-shop`).

## Pendências [confirmar]

- [ ] Custo da hora de fábrica
- [ ] Madeiras disponíveis em retalho e volume por semana
- [ ] Método de gravação e custo real
- [ ] Alíquota do Simples e emissão de NF-e
- [ ] Horas por dia para a campanha
- [ ] Tempo cronometrado de cada protótipo
- [ ] Cotação de faca e garfo, embalagem e cartão
- [ ] Raio de entrega sem frete
- [ ] Quem da MP faz a abordagem e responde o WhatsApp
