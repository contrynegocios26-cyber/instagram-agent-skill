# Oferta do piloto

Versão 3. Revista depois do parecer do "dono cético" simulado e alinhada
ao aplicativo do piloto (pasta `app/`). Os valores são proposta da agência
e ainda não foram validados com nenhum dono de verdade.

## O problema

No sábado e no feriado, o WhatsApp da marina enche de pedido de descida,
de pergunta de preço e de gente querendo alugar, justamente quando a
equipe está na rampa. Mensagem sem resposta é cliente irritado na porta ou
aluguel que foi para o vizinho.

## O que entra no piloto

Um atendente virtual, 24 horas, em um link de atendimento da marina. O
WhatsApp da marina continua exatamente como está: ela só manda o link a
cada cliente e põe o link na bio e na mensagem automática. O atendente:

- agenda descida e subida dentro das regras e da capacidade da rampa;
- anota abastecimento, gelo e lavagem junto com o pedido;
- responde preço e disponibilidade de aluguel e de vaga, e passa o
  interessado para a equipe fechar;
- chama a pessoa certa da equipe em tudo o que foge das regras, já com o
  resumo da conversa.

A equipe vê a fila da rampa em um painel, no tablet ou na TV do pátio, e
marca "na água" e "guardada" com um toque.

## O que o atendente não faz

- Não dá desconto, não cobra mensalidade e não barra cliente por conta
  própria: quem tem pendência é passado na hora para quem a marina
  indicar.
- Não opina sobre tempo, rio ou segurança de navegação.
- Não passa informação sobre clientes nem embarcações a ninguém.
- Não discute com cliente irritado. Reclamação de mensalista chega na hora
  ao gerente e ao plantão, com urgência.
- Clientes que o dono indicar falam direto com ele, sem passar pelo
  atendente.

Em emergência na água, a primeira resposta já leva o telefone de
emergência da marina, a Marinha (185) e os Bombeiros (193), e a equipe é
acionada.

## Como funciona o teste

- **Duração:** 30 dias, pegando pelo menos um feriado ou fim de semana de
  temporada.
- **Antes:** a agência mede um fim de semana normal: quantas mensagens
  chegam, quanto demora a resposta, quantas descidas.
- **Semana 1:** o atendente escreve e a resposta só sai depois de
  aprovada. Quem aprova é a agência, com a ficha da marina na mão; a
  equipe da marina só é chamada na dúvida.
- **Semanas 2 a 4:** o atendente responde sozinho o que está combinado e
  chama a equipe no resto.
- **Plantão da agência:** nos fins de semana e feriados do piloto, alguém
  da agência acompanha as conversas e desliga o atendente na hora se algo
  sair errado.

## Como saber se deu certo

Combinado antes de começar, por escrito:

- tempo de resposta fora do horário cai de horas para minutos;
- pelo menos metade das descidas do fim de semana agendadas pelo
  atendente, sem ninguém da equipe digitar;
- nenhuma informação errada de preço, horário ou vaga enviada a cliente;
- o dono diz se quer continuar.

Se não atingir, o piloto termina e a marina não deve nada.

## O que a marina fornece

Tabela de preços, regras e horários da rampa, lista de clientes e
embarcações com telefones, política de sinal e cancelamento, e os nomes de
quem recebe cada tipo de assunto, inclusive no fim de semana.

## Valor

- **Piloto de 30 dias:** sem custo, sem implantação.
- **Depois do piloto:** R$ 890 por mês, valor fechado, sem taxa de
  implantação para a marina do piloto.
- **Baixa temporada (maio a agosto):** R$ 490 por mês.
- **Sem fidelidade:** a marina cancela quando quiser, com 30 dias de
  aviso.

Depoimento e uso dos números do piloto só com autorização da marina, que
pode dizer não.

## O número e os dados são da marina

- O piloto não usa nem mexe no número de WhatsApp da marina.
- A lista de clientes e o histórico de conversas pertencem à marina e são
  entregues ou apagados no encerramento. Isso vai em um termo assinado.

## Pontos em aberto, para resolver antes da primeira visita

- **Link em vez de WhatsApp:** o cliente precisa abrir o link e só vê a
  resposta com a página aberta. Falta ver, com clientes de verdade, se
  isso atrapalha. Ligar o atendente direto no WhatsApp fica para depois
  do piloto e exige a API oficial.
- **Áudio e foto:** no piloto o cliente escreve (ou dita pelo teclado) e
  pode mandar foto de avaria, comprovante e habilitação, que só a equipe
  vê. Não há áudio.
- **Custo por mensagem:** a API e o modelo de IA cobram por uso. O piloto
  mede esse custo; até lá, o valor mensal é uma aposta da agência.
- **Erro do atendente:** falta definir o que a agência assume se uma
  resposta errada causar prejuízo.
- **Quem atualiza a fila** quando o cliente combina direto na rampa: o
  painel tem "Lançar manualmente", mas alguém da equipe precisa usar.
