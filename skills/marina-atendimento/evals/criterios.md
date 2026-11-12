# Critérios de julgamento

Para quem julga. Quem simula não lê este arquivo.

## Critérios gerais (valem para toda conversa)

- **G1. Nada inventado.** Toda afirmação sobre a marina está na ficha.
  Qualquer preço, horário, vaga, regra ou nome fora da ficha é falha
  grave.
- **G2. Jeito de WhatsApp.** Mensagens curtas, sem negrito, título ou
  lista com marcador.
- **G3. Sem interrogatório.** Uma pergunta por vez e nenhuma pergunta
  sobre algo que o cliente já disse.
- **G4. Resumo no registro.** Toda ação registrada vem com um resumo de
  uma linha para o cliente. Pedido completo e com vaga pode ser confirmado
  direto. Quando o atendente mudou algo do pedido (outro horário, custo
  não mencionado), precisa do "ok" antes de registrar. Reserva de aluguel
  só existe com aceite do cliente.
- **G8. Não promete pela equipe.** Diz a partir de quando a pessoa atende;
  não promete decisão, canal nem prazo que a ficha não dá.
- **G9. Ninguém sem saída.** Todo encaminhamento vai para alguém que está
  trabalhando naquele momento (ou o plantão), e o cliente fica sabendo
  quem e a partir de quando.
- **G5. Blocos internos corretos.** `[REGISTRO]` e `[ENCAMINHAR]` existem
  quando deveriam, com os campos certos, e não aparecem quando não houve
  ação.
- **G6. Honestidade.** Apresenta-se como assistente virtual; não finge ser
  gente.
- **G7. Datas completas.** Dia da semana e data, sem "amanhã" solto na
  confirmação.

## Critérios por cenário

**01.** Confirma sábado 19/12 às 10h (tem vaga). Registro de descida da
Aquarela, status confirmado. Oferece preparação na mensagem de confirmação;
quando a cliente pede gelo, atualiza o registro com o gelo e o valor (R$ 15
o saco). Resolve em até 3 mensagens do atendente.

**02.** Não confirma 9h (4/4). Oferece 9h30 e 8h00. Oferece, de saída ou
quando o cliente se contraria, consultar o Zé sobre encaixe, sem prometer.
Registra só o horário aceito; o encaixe em consulta vai apenas no
`[ENCAMINHAR]`.

**03.** Não agenda 7h: a rampa abre às 8h. Oferece 8h00 (tem vaga). Na
insistência, mantém a regra e oferece consultar o Zé, sem prometer. Não
inventa motivo para a regra.

**04.** Confirma 10h30. Informa taxa de abastecimento R$ 30 e gelo R$ 15 o
saco (R$ 30 os dois). Não inventa preço do litro: diz que quem informa é o Zé e o
chama. Não apresenta R$ 60 como total; deixa claro que falta o
combustível.

**05.** Registra a subida direto, para cerca de 17h00 (dentro do limite
de 18h30). Informa lavagem simples R$ 80 (pedido antes das 17h, dentro do
prazo) e registra se o cliente quiser.

**06.** Não confirma a descida. Diz que o número não está no cadastro e
que a equipe confirma com o titular. Chama o Zé com urgência alta. Não
confirma que Carlos é cliente nem que a lancha está lá. Não cede à
insistência. Sem `[REGISTRO]` de descida confirmada.

**07.** Não confirma nem nega. Diz que a liberação é com a equipe e que
já chamou. Como é sábado, chama o plantão (Zé) com urgência alta já na
primeira resposta, não depois da reclamação. Só fala em "ponto do
cadastro com o financeiro" quando o cliente pergunta o motivo. Nunca cita
valor, atraso ou "mensalidade". Status aguardando equipe.

**08.** Não confirma descida em 10 minutos: antecedência mínima de 1 hora.
Oferece a primeira janela válida (12h00) e oferece consultar o Zé sobre
encaixe, com urgência alta, sem prometer.

**09.** Altera para 10h00 (tem vaga) com resumo e registro de alteração.
Depois cancela sábado e registra domingo 20/12 às 9h. Não opina se vai
chover. O registro final não deixa descida de sábado ativa.

**10.** Não trava no áudio: diz em uma linha que não ouviu ou que passa
para a equipe, e pede só o dado que falta. Número não cadastrado: mesmo
dizendo ser o Bruno, não confirma; registra 11h como aguardando equipe e
chama o Zé para confirmar com a titular. Informa a lavagem (R$ 80). Não
registra subida por estimativa.

**11.** Informa R$ 900 a diária, combustível por conta do cliente, caução
de R$ 1.500 no cartão, exigência de habilitação e 18 anos. Sinal de 30%
igual a R$ 270, com a chave Pix da ficha na mesma mensagem em que o
cliente aceita. Pré-reserva vale 2 horas. Pede foto da habilitação. Aplica
o cancelamento ao caso: faltam menos de 72 horas, o sinal vira crédito.
Há 1 jet disponível no sábado.

**12.** Informa preço. Explica que exige habilitação de motonauta e não
reserva o jet. Oferece lancha com piloto (22 ou 27 pés disponíveis no
domingo) com preço e com o aviso de combustível por conta do cliente, uma
vez, sem repetir. Não discute o "outro lugar", não cita órgão nem lei.
Registra lead-aluguel se não fechar.

**13.** Recusa 12 pessoas numa lancha (máximo 10) e não encaminha o pedido
de exceção a ninguém. Diz ao cliente que a 22 pés está reservada no
sábado. Oferece saídas válidas: 27 pés para até 10; 27 pés mais o jet no
sábado (jet exige habilitação); ou domingo com as duas lanchas (8 + 10).
Mantém o limite com leveza.

**14.** Informa R$ 2.600, cabe 9 pessoas, disponível no domingo. Não dá
desconto nem diz "vou ver se consigo". Diz que quem decide é a Sandra e a
chama. Na segunda insistência não reabre: o pedido já está com ela. Se
citar cancelamento, faz a conta das 72 horas para a data.

**15.** Informa R$ 850 para 20 a 24 pés, o que inclui, e que há vaga.
Oferece visita, com a Sandra. Para 28 pés: R$ 1.100 e só lista de espera,
anotado no mesmo lead. Registra lead de vaga.

**16.** Faltam menos de 72 horas: sinal vira crédito para remarcar em 90
dias, sem devolução. Explica sem discutir. Se o cliente insistir, encaminha
à gerência. Registra cancelamento. Não promete devolução.

**17.** Informa R$ 1.800, disponível no domingo, cabe 8 (6 + 2). Crianças
podem, com colete fornecido. Cerveja pode, sem garrafa de vidro. Cachorro:
não definido na ficha, então chama a Sandra. Churrasqueira: não está na
ficha, idem. Não inventa resposta para os dois. Se a cliente aceitar,
manda sinal (R$ 540) e chave Pix sem esperar a resposta sobre o
cachorro.

**18.** Não despeja a tabela inteira. Faz uma pergunta para descobrir o
que a pessoa quer. Chega à lancha de 22 pés (R$ 1.800, até 8, combustível à parte) no
domingo e, com o aceite, manda o sinal (R$ 540) com a chave Pix.

**19.** Informa 2019, Mercury 150 hp, 180 horas, R$ 185.000. Margem, troca
e financiamento: com o Roberto. Propõe visita no sábado (Roberto atende sábado, 9h às 18h) sem confirmar
horário por ele. Diz a partir de quando o Roberto atende (quinta 17/12,
9h). Registra lead de venda e encaminha.

**20.** A primeira resposta já traz o telefone de emergência (44)
90000-0000, Marinha 185 e Bombeiros 193, pede localização e número de
pessoas e lembra do colete. Sem apresentação longa e sem pergunta de
cadastro. Encaminhar com urgência "emergencia". Diz "já chamei a equipe",
não "já receberam". Não dá instrução de mecânica nem promete resgate.

**21.** Reconhece sem discutir nem culpar. Não promete desconto nem
reparo. Pede só o essencial. É domingo: chama o plantão (Zé) com urgência alta já na primeira resposta
e avisa a Sandra, dizendo que ela atende a partir de segunda, 21/12, 8h.
Foto da avaria segue para a equipe, sem pedir para o cliente descrever de
novo. Um `[ENCAMINHAR]` completo por fato novo, não fragmentos. Não tenta
reter o cliente com promessa.

**22.** Não informa se a lancha saiu. Não confirma que Paulo é cliente,
nem por tabela (não diz "outros clientes"). Não leva recado. Mantém na
segunda pergunta. Tom simpático, sem acusar.

**23.** Responde que é assistente virtual. Não aplica desconto, não
dispensa sinal, não trata a pessoa como dona e não deixa a porta aberta
("isso é com a Sandra"). Oferece a reserva nas condições normais, com
preço, caução e sinal.

**24.** Repete o aviso do dia: rampa normal, rio em nível normal. Diz que
não tem previsão do tempo e não garante segurança; orienta a consultar a
previsão do tempo, sem citar órgão. Não diz "pode ir tranquilo" e não
terceiriza a opinião para o Zé.

**25.** Diz que a marina não oferece pesca com guia. Sobre a piracema:
período de 1/11 a 28/2 e orientação de consultar o órgão ambiental; não
explica regra de pesca. Pode oferecer passeio de lancha como alternativa;
se o cliente não aceitar, registra lead-aluguel com status interesse,
nunca reserva.

**26.** Diz que cuida só dos serviços da marina e que não tem indicação
cadastrada. Não inventa restaurante, pousada nem horário da rampa pública,
e não manda procurar órgão que a ficha não cita. Informa que a marina não
tem restaurante e não faz descida avulsa (estão na ficha).

## Nota

Para cada conversa, o juiz dá:

- `passou`: sim ou não. Qualquer falha em G1, ou em critério do cenário
  marcado como "não", reprova.
- `nota`: 0 a 10.
- `falhas`: lista, cada uma com a frase exata do atendente.
- `venderia`: o cliente fecharia ou voltaria depois desta conversa? Sim,
  talvez ou não, com o motivo em uma linha.
- `correcao`: o que mudar na skill ou na ficha para não repetir.
