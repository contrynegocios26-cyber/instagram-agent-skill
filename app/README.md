# Atendimento para marinas

Aplicativo para o piloto com uma marina: um link de atendimento para os
clientes e um painel para a equipe, com um assistente de IA no meio.

- **Cliente da casa** abre o link pessoal no celular e pede a descida do
  barco, avisa que está voltando ou pede gelo e lavagem, a qualquer hora.
- **Visitante** abre o link público e pergunta de aluguel, vaga ou barco à
  venda.
- **Equipe** vê no painel a fila da rampa, aprova as respostas do
  assistente (modo sombra), recebe os chamados e assume a conversa quando
  quer.

O piloto roda por link, sem mexer no número de WhatsApp da marina. A
marina manda o link pessoal a cada cliente pelo próprio WhatsApp (há um
botão para isso no painel) e põe o link público na bio e na mensagem
automática.

Telas: [`docs/telas/`](docs/telas/).

## Ver funcionando em um minuto

Precisa do Node.js 22 ou mais novo.

```bash
cd app
npm install
npm run dev
```

Isso sobe a **Marina Remanso**, fictícia, com respostas de roteiro (sem
IA e sem custo). As senhas do painel aparecem no terminal na primeira vez.

- Cliente: `http://localhost:3000/` (link público)
- Painel: `http://localhost:3000/painel`
- Link pessoal de cada cliente: no painel, aba Clientes

## Como funciona por dentro

- **O que o assistente sabe** vem de dois textos: as regras de atendimento
  (`skills/marina-atendimento/SKILL.md`, a mesma skill validada na bancada)
  e a ficha da marina, editada no painel.
- **Quem confirma é o sistema, não a IA.** Horário da rampa, janela lotada,
  antecedência mínima e unidade de aluguel livre são conferidos por código
  (`lib/agenda.js`). O assistente só diz "confirmado" depois que o sistema
  aceita o registro.
- **Identidade pelo link.** O assistente não recebe a lista de clientes.
  Pedido de descida pelo link público, ou de cadastro com pendência, fica
  sempre "aguardando equipe", por mais que a pessoa insista.
- **Modo sombra.** O assistente escreve, a equipe aprova, edita ou
  descarta. Até aprovar, nada do que ele registrou vale.
- **Emergência não depende da IA.** Palavras como "à deriva", "afundando"
  e "socorro" disparam na hora o telefone da marina, Marinha 185 e
  Bombeiros 193, e um chamado vermelho no painel.
- **Falhou, chama gente.** Se a IA erra, recusa ou cai, o cliente é avisado
  e a conversa vai para a equipe com um chamado.
- **Ninguém fica esperando sem saber.** Se uma mensagem passa de 10 minutos
  sem resposta (aprovação parada no modo sombra, ou equipe na conversa sem
  responder), o cliente recebe um aviso e a equipe, um chamado.
- **Mensagem velha não é respondida sozinha.** O que ficou mais de 6 horas
  sem resposta vai para o assistente só como contexto, com a data em que
  foi escrito. Ele não marca descida por causa de um "amanhã" antigo.
- **A conversa volta para o assistente.** Depois de uma falha da IA, ele
  volta a responder em 15 minutos; se a equipe assumiu e ficou 12 horas
  sem escrever, também. O botão "Devolver ao assistente" faz isso na hora.
- **Link público com freio.** Pedido de descida vindo dele aparece no
  painel marcado "link público: confirme quem é" e não ocupa vaga até a
  equipe liberar. Ele tem cota própria de respostas da IA e limite de
  mensagens e fotos por aparelho, para um estranho não gastar o dia de
  atendimento dos clientes da casa.

## Os seis agentes

| Agente | O que faz | Quando |
|---|---|---|
| **Atendente** | Conversa com o cliente, agenda descida e subida, registra interessados e chama a equipe | Na hora, 24 horas |
| **Operação** | Resumo do dia para a equipe da rampa: descidas, serviços, aluguéis, pendências | Todo dia cedo |
| **Relacionamento** | Lembretes de vencimento, revisão e documento; mensagem de pós-passeio; cliente sumido | Todo dia |
| **Vendas** | Retorno para quem perguntou de aluguel, vaga ou barco à venda e não fechou | Todo dia |
| **Gerente** | Resumo da semana para o dono, com os números do atendimento e da rampa | Toda semana |
| **Conteúdo** | Três ideias de post para a semana | Toda semana |

Só o Atendente fala com o cliente por conta própria. Os outros cinco
preparam **sugestões** na aba Agentes: alguém da equipe confere, edita se
quiser e envia pelo WhatsApp da marina com um toque. Os fatos (datas,
nomes, números) são levantados por código; a IA só melhora a redação, e se
ela falhar ou tirar uma data do texto, vale o texto-modelo. Horários e
liga/desliga de cada agente ficam na aba Configuração.

## Instalar na Hostinger

Passos para uma VPS com Docker. Os nomes dos menus do painel da Hostinger
não foram conferidos; os comandos são os mesmos em qualquer VPS.

1. **Domínio.** Crie um subdomínio (ex.: `atendimento.suaagencia.com.br`)
   com um registro A apontando para o IP da VPS.
2. **Código.** No terminal da VPS (no painel da Hostinger há um terminal
   no navegador; não precisa de chave SSH):
   ```bash
   git clone -b claude/busy-shannon-35ewb5 https://github.com/contrynegocios26-cyber/instagram-agent-skill.git marina
   cd marina/app
   cp .env.example .env
   nano .env
   ```
   Se o comando `docker` não existir na VPS, instale antes com
   `curl -fsSL https://get.docker.com | sh`.
3. **Preencha o `.env`:** domínio, chave da API da Anthropic e as duas
   senhas do painel. A chave é criada por você em
   [platform.claude.com](https://platform.claude.com), em "API keys", depois
   de colocar crédito na conta (é pré-pago, em dólar). Ela aparece uma vez
   só: copie e cole direto no `.env`. Não mande a chave em conversa, e-mail
   ou GitHub. No `nano`, salve com Ctrl+O, Enter, e saia com Ctrl+X.
4. **Suba:**
   ```bash
   docker compose up -d --build
   ```
   O Caddy emite o certificado HTTPS sozinho. Em um ou dois minutos o
   endereço responde.
5. **Confira a IA antes de mostrar a alguém** (veja "Antes de ligar para
   clientes", abaixo).
6. **Atualizar depois:** `git pull && docker compose up -d --build`.

Os dados ficam no volume `dados`. Faça cópia dele, ou use "Baixar todos os
dados" na aba Configuração.

Se as senhas do painel ficarem em branco no `.env`, o aplicativo cria as
duas e mostra no log (`docker compose logs app`). Se o Docker Hub recusar
o download da imagem por limite de uso, tente de novo mais tarde.

## Preparar a marina

Entre no painel com a senha de administrador.

1. **Configuração:** nome, horários da rampa, tamanho e lotação das
   janelas, antecedência mínima, itens de aluguel com o número de unidades
   e o telefone de emergência.
2. **Ficha:** preços, políticas, chave Pix, equipe e quem responde por cada
   assunto, inclusive no fim de semana. Campo em branco significa "o
   assistente chama a equipe"; é melhor do que preencher no chute.
3. **Clientes:** cadastre cada um com a embarcação. Use "Enviar no
   WhatsApp" para mandar o link pessoal pelo WhatsApp da marina.
4. **Link público:** copie ou imprima o QR para a recepção.
5. **Aviso do dia:** na aba Rampa. É a única coisa que o assistente repete
   sobre rio, rampa e tempo.

## Antes de ligar para clientes

O que já foi testado, e como:

- **105 testes automáticos** das regras da rampa, do motor do atendente,
  das rotas, dos agentes e do formato dos pedidos à IA, com respostas de
  roteiro.
- **19 passos no navegador**, do pedido do cliente no celular até a rampa
  no painel, incluindo foto, link público, encaixe e emergência.
- **Dez situações de cliente respondidas por um modelo Claude de verdade**,
  com o prompt, as ferramentas e a validação do servidor reais, mas por uma
  ponte de arquivos (`scripts/ponte.mjs`), não pela API: 10 de 10, na
  rodada feita com o prompt atual
  (`validacao/aplicativo/ponte-rodada-2.txt`, que também lista pontos de
  redação a melhorar nas regras).
- **Revisão independente do código**, que apontou 15 defeitos (3 graves).
  Todos foram corrigidos e cada um ganhou um teste
  (`test/revisao.test.js`).

O que **não** foi testado: nenhuma chamada à API da Anthropic saiu do
ambiente de desenvolvimento, porque lá não havia chave. O formato dos
pedidos foi conferido contra a documentação, mas só a execução prova. Por
isso, com a chave no `.env`, rode estes dois comandos, nesta ordem, antes
de mostrar o aplicativo a qualquer marina:

```bash
docker compose exec app node scripts/sonda-custo.mjs    # a IA responde? o cache funciona? quanto custa?
docker compose exec app node scripts/bancada-real.mjs   # dez situações de cliente, com conferência automática
```

Fora do Docker, na pasta `app`, com a chave na variável
`ANTHROPIC_API_KEY`, os mesmos comandos funcionam sem o
`docker compose exec app`.

- A **sonda** faz três pedidos e gasta poucos centavos de dólar. Ela
  confere também a manutenção do cache (veja "Custo da IA").
- A **bancada** faz cerca de 30 pedidos. Ela usa a marina fictícia e não
  toca nos dados reais. Se alguma situação falhar, leia a conversa
  impressa: ela mostra o que o assistente disse e o que ficou registrado.
- Se a API recusar algum recurso opcional do pedido, o aplicativo desliga
  esse recurso sozinho e avisa no log (`docker compose logs app`).

Depois, com a ficha real da marina preenchida, rode a bancada de validação
da skill `marina-validacao`.

## Rodar o piloto

- **Comece em modo sombra.** Quem aprova precisa estar com o painel aberto;
  o cliente fica vendo "digitando" até a aprovação. Ative o som do painel.
- **Passe para automático** quando as aprovações estiverem saindo sem
  edição. A aba Relatório mostra quantas foram editadas.
- **Desligue na hora** pelo selo "Atendente" no topo do painel. As mensagens
  passam a ir para a equipe.
- **Relatório:** tempo de resposta, mensagens fora do horário, descidas
  agendadas pelo assistente e custo da IA. São os números para mostrar ao
  dono no fim dos 30 dias.

## Custo da IA

A cobrança é da Anthropic, por uso, na chave que estiver no `.env`. É
pré-paga: você põe crédito em dólar e o uso desconta dele. O painel mostra
o custo estimado por resposta na aba Relatório. Se o crédito acabar, o
painel mostra uma faixa avisando e as mensagens vão para a equipe até o
crédito voltar; vale ligar a recarga automática no console da Anthropic.

O prompt (regras, ficha e ferramentas, perto de 9 mil tokens) é igual para
todos os clientes da marina e fica em cache por 1 hora. Ler do cache custa
uns 2,5% do preço de gravar, então quase todo o custo de uma resposta é o
texto que o modelo escreve.

**Manutenção do cache.** Se passar mais de uma hora sem movimento, a
mensagem seguinte paga a gravação de novo (cerca de US$ 0,07 no Opus 5.5).
Para evitar isso, o servidor relê o cache a cada 50 minutos, enquanto houve
atendimento nas últimas 24 horas. Cada releitura custa uns US$ 0,002; o
dia inteiro custa menos que uma única gravação. Se a API não reaproveitar
o cache nesse pedido, o servidor percebe e desliga a manutenção sozinho.
`IA_MANTER_CACHE=off` desliga à mão.

**Estimativa por marina, por mês (não medida; preços de tabela de novembro
de 2026):**

| Respostas do assistente no mês | Opus 5.5 (padrão) | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|
| cerca de 300 (10 por dia) | US$ 8 a 15 | US$ 4 a 8 | menos de US$ 1 |
| cerca de 1.500 (50 por dia) | US$ 20 a 50 | US$ 10 a 25 | US$ 1 a 2 |
| cerca de 4.000 (130 por dia) | US$ 45 a 125 | US$ 25 a 65 | US$ 2 a 5 |

Os cinco agentes de retaguarda somam perto de US$ 2 por mês no Opus 5.5.
Sem a manutenção do cache, some de US$ 5 a 15 nas linhas de baixo
movimento. A conta que vale é a da aba Relatório, que soma o custo de cada
chamada, e a fatura da Anthropic. Para medir uma resposta:

```bash
docker compose exec app node scripts/sonda-custo.mjs
```

O modelo padrão é o Claude Opus 5.5, com esforço `medium`. Trocar o modelo
(`IA_MODELO`) ou o esforço (`IA_ESFORCO`) muda custo e qualidade; rode a
bancada (`scripts/bancada-real.mjs`) antes e depois de trocar.

## Limites desta versão

- **Não é WhatsApp.** É um link que abre no navegador. O cliente só vê a
  resposta com a página aberta; não há notificação no celular. Para avisos
  importantes, a equipe usa o botão de WhatsApp do painel.
- **Sem áudio.** O cliente escreve ou dita pelo teclado.
- **Fotos não vão para a IA.** O cliente pode enviar; só a equipe vê. O
  assistente sabe apenas que chegou uma foto.
- **Uma marina por instalação.**
- **Aluguel por dia:** uma unidade reservada conta como ocupada o dia
  inteiro, mesmo em aluguel por hora.
- **Ainda não rodou com a API da Anthropic nem com clientes reais.** Veja
  "Antes de ligar para clientes".
- **Conta nova na Anthropic tem limite de uso por minuto mais baixo.** Se
  o limite for atingido, a conversa vai para a equipe e o assistente volta
  a responder em 15 minutos.
- **Com `IA_MODELO=claude-sonnet-5-5`,** se um filtro de segurança recusar
  um pedido, a troca automática de modelo vai para o Sonnet 5, que pode não
  aceitar o formato do contexto. Nesse caso a conversa vai para a equipe.
- **A imagem Docker não foi construída no ambiente de desenvolvimento**
  (o download da imagem base foi recusado lá). Os mesmos arquivos que vão
  na imagem foram executados fora do Docker, em uma pasta limpa.

## Segurança e dados

- Conversas, clientes e registros ficam em arquivos na pasta de dados da
  VPS. O único serviço de fora que recebe dados é a API da Anthropic, que
  gera as respostas. **O que vai para ela:**
  - a ficha da marina e as regras de atendimento;
  - o texto das mensagens da conversa;
  - de quem tem cadastro: nome, embarcação, pessoas autorizadas, se há
    pendência, a observação da marina e os agendamentos em aberto;
  - nos agentes de retaguarda: primeiro nome, embarcação, datas de
    vencimento, revisão e documento, o que o interessado disse e os números
    da semana.

  **O que não vai:** fotos, telefones do cadastro, links pessoais e senhas.
  Isso precisa constar no termo assinado com a marina e está no aviso de
  privacidade do chat.
- O link pessoal é a credencial do cliente: quem tem o link pede descida em
  nome dele. Se vazar, gere um link novo na aba Clientes. O link não aparece
  nas sugestões dos agentes nem em "Baixar todos os dados".
- A sessão do chat e o login do painel são assinados com chaves diferentes:
  a chave que o chat entrega a um visitante não abre o painel. Cada foto
  tem um endereço próprio, que vence em 12 horas.
- As fotos ocupam no máximo 1 GB no disco (`FOTOS_LIMITE_MB`). Cheio, o
  cliente é avisado e o resto do atendimento segue.
- Excluir um cliente apaga a conversa e as fotos dele.
- O painel tem duas senhas: equipe (rampa, aprovações, conversas) e
  administrador (clientes, ficha, configuração, relatório, modo automático).

## Testes

```bash
npm test                 # 105 testes: rampa, atendente, rotas, agentes, pedidos à IA
node test/e2e.mjs        # 19 passos no navegador: cliente e equipe, do pedido à rampa
```

Os dois usam o roteiro sem IA. `test/revisao.test.js` tem um teste para
cada defeito achado na revisão do código. Com o modelo de verdade, use a sonda e a
bancada da seção "Antes de ligar para clientes". Para experimentar uma
frase de cliente pela linha de comando, com a marina de exemplo:

```bash
ANTHROPIC_API_KEY=... node scripts/conversa.mjs --cliente Fernanda \
  --agora 2026-12-18T19:10 "desce a aquarela amanhã 10h" "com 2 sacos de gelo"
```

## Variáveis de ambiente

| Variável | Para quê |
|---|---|
| `DOMINIO`, `URL_PUBLICA` | Endereço do atendimento |
| `ANTHROPIC_API_KEY` | Chave da API da Anthropic |
| `PAINEL_SENHA`, `ADMIN_SENHA` | Senhas do painel |
| `IA_MODELO` | Modelo (padrão `claude-opus-5-5`) |
| `IA_ESFORCO` | Quanto o modelo raciocina: `low`, `medium` (padrão) ou `high`. Menos esforço custa menos e responde mais rápido |
| `IA_CACHE_TTL` | `1h` (padrão) ou `5m` |
| `IA_MANTER_CACHE` | `off` desliga a releitura do cache a cada 50 minutos |
| `IA_LIMITE_DIARIO` | Teto de chamadas ao modelo por dia (padrão 1500) |
| `IA_LIMITE_DIARIO_PUBLICO` | Parte desse teto que o link público pode usar (padrão 40%) |
| `FOTOS_LIMITE_MB` | Espaço máximo das fotos em disco (padrão 1000) |
| `AVISO_SEM_RESPOSTA_MIN` | Minutos sem resposta até avisar o cliente e a equipe (padrão 10) |
| `IA_FALLBACK` | `off` desliga a troca de modelo quando um filtro de segurança recusa o pedido |
| `SEMENTE` | `exemplo` começa com a marina fictícia |
| `IA_FAKE` | `1` roda sem IA, com roteiro |
| `DADOS_DIR`, `PORT` | Pasta de dados e porta |
