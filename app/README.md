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

## Instalar na Hostinger

Passos para uma VPS com Docker. Os nomes dos menus do painel da Hostinger
não foram conferidos; os comandos são os mesmos em qualquer VPS.

1. **Domínio.** Crie um subdomínio (ex.: `atendimento.suaagencia.com.br`)
   com um registro A apontando para o IP da VPS.
2. **Código.** No terminal da VPS:
   ```bash
   git clone <endereço do repositório> marina
   cd marina/app
   cp .env.example .env
   nano .env
   ```
3. **Preencha o `.env`:** domínio, chave da API da Anthropic e as duas
   senhas do painel.
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

A parte que conversa com a IA de verdade ainda não foi executada: o
ambiente de desenvolvimento não tinha chave da API. Tudo em volta dela foi
testado com respostas de roteiro. Por isso, com a chave no `.env`, rode
estes dois comandos, nesta ordem, antes de mostrar o aplicativo a qualquer
marina:

```bash
docker compose exec app node scripts/sonda-custo.mjs    # a IA responde? o cache funciona? quanto custa?
docker compose exec app node scripts/bancada-real.mjs   # dez situações de cliente, com conferência automática
```

Fora do Docker, na pasta `app`, com a chave na variável
`ANTHROPIC_API_KEY`, os mesmos comandos funcionam sem o
`docker compose exec app`.

- A **sonda** faz dois pedidos e gasta poucos centavos de dólar.
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

A cobrança é da Anthropic, por uso, na chave que estiver no `.env`. O
painel mostra o custo estimado por resposta na aba Relatório.

O prompt (regras, ficha e ferramentas) é igual para todos os clientes da
marina e fica em cache, o que reduz bastante o custo de entrada. Para
conferir o cache e medir o custo de uma resposta:

```bash
ANTHROPIC_API_KEY=... node scripts/sonda-custo.mjs
```

O modelo padrão é o Claude Opus 5.5. Trocar o modelo (`IA_MODELO`) ou o
esforço (`IA_ESFORCO`) reduz o custo e pode reduzir a qualidade; meça com
a bancada de cenários antes de trocar.

## Limites desta versão

- **Não é WhatsApp.** É um link que abre no navegador. O cliente só vê a
  resposta com a página aberta; não há notificação no celular. Para avisos
  importantes, a equipe usa o botão de WhatsApp do painel.
- **Sem áudio.** O cliente escreve ou dita pelo teclado.
- **Fotos não vão para a IA.** O cliente pode enviar; só a equipe vê.
- **Uma marina por instalação.**
- **Aluguel por dia:** uma unidade reservada conta como ocupada o dia
  inteiro, mesmo em aluguel por hora.
- **Ainda não rodou com a IA de verdade nem com clientes reais.** Veja
  "Antes de ligar para clientes".
- **A imagem Docker não foi construída no ambiente de desenvolvimento**
  (o download da imagem base foi recusado lá). Os mesmos arquivos que vão
  na imagem foram executados fora do Docker, em uma pasta limpa.

## Segurança e dados

- Conversas, clientes e registros ficam em arquivos na pasta de dados da
  VPS. Nada vai para outro serviço, exceto o texto das mensagens e a ficha,
  que são enviados à API da Anthropic para gerar as respostas. Isso precisa
  constar no termo assinado com a marina.
- O link pessoal é a credencial do cliente: quem tem o link pede descida em
  nome dele. Se vazar, gere um link novo na aba Clientes.
- Excluir um cliente apaga a conversa e as fotos dele.
- O painel tem duas senhas: equipe (rampa, aprovações, conversas) e
  administrador (clientes, ficha, configuração, relatório, modo automático).

## Testes

```bash
npm test                 # regras da rampa, motor do atendente e rotas
node test/e2e.mjs        # navegador: cliente e equipe, do pedido à rampa
```

Os dois usam o roteiro sem IA. Com o modelo de verdade, use a sonda e a
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
| `IA_ESFORCO` | `low`, `medium` ou `high`; em branco usa o padrão do modelo |
| `IA_CACHE_TTL` | `1h` (padrão) ou `5m` |
| `IA_LIMITE_DIARIO` | Teto de chamadas ao modelo por dia (padrão 1500) |
| `AVISO_SEM_RESPOSTA_MIN` | Minutos sem resposta até avisar o cliente e a equipe (padrão 10) |
| `IA_FALLBACK` | `off` desliga a troca de modelo quando um filtro de segurança recusa o pedido |
| `SEMENTE` | `exemplo` começa com a marina fictícia |
| `IA_FAKE` | `1` roda sem IA, com roteiro |
| `DADOS_DIR`, `PORT` | Pasta de dados e porta |
