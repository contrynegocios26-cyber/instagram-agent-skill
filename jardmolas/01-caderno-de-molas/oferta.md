# Caderno de Molas da Usina: a oferta

> Documento interno da equipe comercial Jardmolas. Versão 1, 09/11/2026.
> Tudo que está entre [colchetes] precisa ser confirmado ou decidido pela Jardmolas antes de ir para o cliente.

## Em uma frase

Na entressafra, a Jardmolas vai até a usina sem custo, levanta cada mola crítica com a máquina parada e liberada pela equipe da usina, e entrega um caderno com foto, local/TAG, medidas, material e um código Jardmolas para cada mola. A partir daí, o comprador pede pelo código e a manutenção para de procurar medida no meio da parada.

## O problema que a gente resolve

Todo gerente de manutenção conhece a cena:

- A válvula de retenção abre na parada e a mola está quebrada. Ninguém sabe a medida. A peça que estava no almoxarifado está cadastrada como "MOLA COMPRESSAO DIVERSAS".
- A mola original vem junto com o reparo do fabricante da válvula, com o prazo dele.
- O mecânico leva a mola quebrada até alguém que "faz igual", sem desenho, sem material definido, sem laudo.
- Na safra seguinte a mesma mola quebra de novo e a busca recomeça.

O caderno acaba com isso: cada mola que importa ganha um registro único, com medida e material, e um código que o almoxarifado e o comprador conseguem usar.

## Para quem

**Cliente principal:** usinas de açúcar e etanol e destilarias da região de Ribeirão Preto e entorno (lista de alvos: ver `04-mercado-e-alvos/`).

**Quem patrocina dentro da usina:**

| Cargo | Por que interessa a ele |
|---|---|
| Gerente de manutenção industrial | Menos equipamento parado esperando mola na parada e na safra |
| PCM (planejamento e controle da manutenção) | Lista de sobressalentes com código, medida e tempo de reposição |
| Suprimentos / compras | Cadastro de material limpo, cotação comparável, laudo por lote |
| Gerente agrícola / oficina agrícola | Enleiradores de palha, carretas canavieiras, implementos com mola identificada |

**Também serve para:** grandes fornecedores de cana e prestadores de serviço com frota própria de enleiradores, carretas e implementos (versão reduzida do caderno, só área agrícola).

## O que o cliente recebe

1. **Visita técnica de levantamento**, agendada com a manutenção, feita só com equipamento parado, bloqueado e liberado pela usina (ver `roteiro-visita-tecnica.md`).
2. **Caderno de Molas em PDF**, organizado por área da usina. Para cada mola:
   - foto da mola (com escala) e foto do local de montagem;
   - área, equipamento, local/TAG da usina;
   - código Jardmolas;
   - tipo (compressão, tração, torção, dedo, especial);
   - medidas principais: diâmetro do arame, diâmetro externo, comprimento livre, número de espiras, tipo de ponta, sentido de enrolamento (e, conforme o tipo, ganchos, pernas e ângulo);
   - material (identificado ou proposto pela Jardmolas);
   - quantidade instalada e consumo informado pelo mecânico;
   - criticidade A, B ou C (definição abaixo);
   - se existe sobressalente no almoxarifado hoje.
3. **Planilha de cadastro** (Excel/CSV) com as mesmas informações, numa coluna de "descrição padronizada" pronta para o cadastro de material do ERP da usina.
4. **Etiquetas de código** para as caixas ou gavetas do almoxarifado: código Jardmolas, descrição curta, TAG do equipamento e QR code que abre o Identificador de Molas [confirmar o destino do QR com `02-identificador/`].
5. **Reunião de entrega** com manutenção, PCM, almoxarifado e compras, com a lista de reposição de entressafra já montada (ver `entrega-do-caderno-e-pos-venda.md`).

## Quanto custa

**Nada.** Sem pedido mínimo, sem contrato, sem exclusividade. A usina fica com o caderno e a planilha mesmo que não compre nada.

Isso precisa ser dito assim, sem asterisco. O que a Jardmolas espera em troca é a chance de cotar as molas do caderno, e isso também precisa ser dito com clareza na primeira conversa.

## O que a Jardmolas ganha

- **O desenho.** Quem tem a medida e o material de cada mola cota primeiro, cota certo e entrega rápido. Quem não tem precisa pedir amostra.
- **O código dentro do almoxarifado.** Quando o código Jardmolas entra no cadastro de material da usina, o pedido de compra já sai com ele.
- **O pedido de entressafra.** O levantamento mostra o que está quebrado, cansado ou sem sobressalente. Isso vira orçamento na hora.
- **A porta para o Estoque Garantido** (ver `estoque-garantido.md`): com o caderno na mão, dá para propor estoque das molas A com preço travado por 12 meses.
- **Base de dados para o estoque estratégico.** A mesma mola aparece em várias usinas (mesma válvula, mesma peneira, mesmo atuador). Saber isso define o que vale ter pronto na prateleira.
- **Referência.** Uma usina com caderno é o melhor argumento para a próxima.

## Regra do código Jardmolas

**Como o app de levantamento gera hoje:** um código por usina, com a sigla dela e um número sequencial (`JM-SIGLA-001`, por exemplo `JM-SMA-001`). A mesma mola em vários lugares da mesma usina fica com o mesmo código; muda só a TAG (ver `instalacao-do-app.md`). É esse código que vai para o caderno, para as etiquetas e para o cadastro da usina.

**O que falta decidir:** a mesma mola (mesma geometria e material) pode aparecer em várias usinas, cada uma com o seu código `JM-SIGLA-...`. Para o estoque estratégico e para o Estoque Garantido, a Jardmolas precisa saber que `JM-SMA-001` e, digamos, `JM-USB-014` são a mesma mola. Duas saídas:

- **Opção 1 (recomendada):** manter o código por usina para o cliente e ter, na Jardmolas, um código interno de produção por mola (ex.: `C-00142`), ligado a todos os códigos de usina que usam essa mola. O cliente não vê o interno.
- **Opção 2:** um código único por mola para todas as usinas. Mais simples para a produção, mas o cliente perde a leitura "esta é a mola 001 da minha usina".

Por que importa: mola que serve a várias usinas pode ficar pronta na prateleira com pouco risco; mola que só uma usina usa precisa da regra de saldo do Estoque Garantido (`estoque-garantido.md`, item 8). [Decidir com quem está construindo o app e o gerador do caderno antes da primeira visita.]

## Criticidade (usada no caderno, na visita e no Estoque Garantido)

| Nível | Critério | Exemplo típico |
|---|---|---|
| **A** | Se a mola falha, para equipamento sem reserva ou para a moagem, ou é item de segurança | Mola de válvula de segurança, de atuador de válvula sem by-pass, de alimentação de bagaço da caldeira |
| **B** | Se falha, perde capacidade ou para equipamento que tem reserva | Mola de peneira vibratória com peneira reserva, válvula de retenção de bomba com bomba reserva |
| **C** | Se falha, não afeta produção no curto prazo | Molas de proteção, tampas, acessórios |

A classificação é feita **com o mecânico da usina**, não pela Jardmolas sozinha. Quem conhece a planta é ele.

## Regras da oferta

### Capacidade

- Visitas por mês que a equipe aguenta: **[confirmar com a Jardmolas]**.
- Para calcular, considerar por visita: [confirmar] pessoas em campo, 1 dia de usina (mais deslocamento), [confirmar] dias de escritório para montar o caderno, medição em bancada das amostras trazidas.
- Regra prática: não vender mais visitas do que dá para entregar no prazo. Caderno atrasado mata a oferta.

### Raio de atendimento

- Raio a partir de Jardinópolis: **[confirmar com a Jardmolas]**. Sugestão para discutir: começar só com usinas a até um dia de viagem ida e volta, para que a equipe durma em casa.
- Fora do raio: só se a usina já for cliente com volume relevante ou se houver duas ou mais usinas próximas para visitar na mesma viagem.

### Critério para aceitar uma usina

Pontue cada item com 0 ou 1. Aceitar com 5 pontos ou mais; com 3 ou 4, aceitar se houver vaga na agenda; abaixo de 3, oferecer só o atendimento normal pelo WhatsApp.

| # | Critério | 0 / 1 |
|---|---|---|
| 1 | Está dentro do raio definido | |
| 2 | Temos um patrocinador com nome: gerente de manutenção ou PCM que pediu a visita | |
| 3 | A usina aceita marcar data dentro da entressafra (dez a mar) | |
| 4 | A usina autoriza foto das molas e dos locais (por escrito ou no e-mail de agendamento) | |
| 5 | Temos o contato de compras/suprimentos para a reunião de entrega | |
| 6 | A usina compra molas hoje (de qualquer fornecedor) e sabe dizer quais deram problema | |
| 7 | Cadastro de fornecedor possível: a Jardmolas consegue ser cadastrada (ou já é) | |
| 8 | Situação financeira sem alerta (consulta de crédito padrão da Jardmolas) [confirmar procedimento] | |

### Quando visitar

- A melhor janela é **logo no começo da parada**: equipamentos abertos, mecânicos disponíveis para conversar, compras ainda montando o pacote de entressafra.
- Calendário da temporada 2026/27 (proposta):

| Período | O que acontece |
|---|---|
| 10/11 a 30/11/2026 | Prospecção, onda 1 (`abordagem-usinas.md`), usinas que já pararam ou param no início de dezembro |
| 01/12 a 19/12/2026 | Visitas da onda 1 |
| 20/12/2026 a [confirmar] | Recesso de fim de ano da Jardmolas e das usinas [confirmar] |
| Janeiro a fevereiro de 2027 | Visitas da onda 2, entrega dos cadernos da onda 1, pedidos de entressafra |
| Março de 2027 | Fechamento de contratos de Estoque Garantido antes da partida da safra 2027/28 |

## O que entregar e em que prazo

| Entregável | Formato | Prazo |
|---|---|---|
| Resumo do dia (quantas molas, quantas A, quantas sem sobressalente) | Mensagem para o gerente no fim da visita | No mesmo dia |
| Caderno de Molas | PDF gerado pelo app (aba Caderno) | **[confirmar com a Jardmolas]**. Sugestão: reunião de entrega em até 7 dias após a visita, como propõe o roteiro do script `07-skills/jm-caderno-usina/`. Se houver muitas amostras para a bancada, até 10 dias úteis |
| Planilha de cadastro | CSV gerado pelo app (abre no Excel) | Junto com o caderno |
| Orçamento das molas para troca imediata | PDF ou WhatsApp, por código Jardmolas | Junto com o caderno, ou antes se houver urgência |
| Etiquetas de código | Impressas, entregues na reunião | Na reunião de entrega |
| Proposta de Estoque Garantido | PDF (`estoque-garantido.md`) | Na reunião de entrega ou até [confirmar] dias depois |

**O que faz o prazo variar:** número de molas, quantas amostras precisam ir para a bancada, e se a usina libera as fotos no dia.

## Decisões que a Jardmolas precisa tomar antes de lançar

1. **O caderno traz a ficha técnica completa ou só as medidas principais?**
   - Opção A: ficha completa (tolerâncias, material, carga). Mais confiança, compras aceita melhor. A concorrência também pode cotar com ela.
   - Opção B: medidas principais no caderno; ficha completa fica com a Jardmolas e acompanha cada fornecimento com o laudo.
   - Recomendação comercial: **opção A**. O dado foi levantado dentro da usina e ela vai considerar que é dela. A vantagem da Jardmolas vem do código já cadastrado, do estoque e do prazo, não de esconder medida. Esconder vira objeção de compras.
2. **O que o laudo por lote traz** (composição do arame, dureza, carga x deflexão, dimensional?). [confirmar] Isso aparece em toda conversa com usina.
3. **Prazo de garantia por escrito.** O site fala em "garantia superior ao mercado", sem prazo. Usina vai pedir o número. [confirmar]
4. **Capacidade mensal de visitas, raio e prazo do caderno** (acima).
5. **Quem vai a campo** e se essa pessoa tem (ou vai fazer) os treinamentos que as usinas costumam pedir (ver `roteiro-visita-tecnica.md`).
6. **Custo de uma visita** (horas, deslocamento, etiquetas, bancada) para saber quantos pedidos pagam um caderno. Conta sugerida:

| Item | Valor |
|---|---|
| Horas de campo x custo/hora da equipe | [confirmar] |
| Horas de escritório para montar o caderno | [confirmar] |
| Deslocamento (km x custo/km) e alimentação | [confirmar] |
| Etiquetas e impressão | [confirmar] |
| **Custo total da visita (CV)** | soma |
| Margem bruta média por pedido de usina (MP) | [confirmar] |
| **Pedidos para pagar a visita** | CV / MP |

## O que o caderno NÃO é (dizer isso na primeira conversa)

- Não é inspeção de segurança, nem laudo de válvula de segurança, nem substitui o profissional habilitado da usina. Mola de válvula de segurança de caldeira ou vaso de pressão continua sob a responsabilidade da usina e do seu profissional habilitado (NR-13: https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/arquivos/normas-regulamentadoras/nr-13.pdf). A Jardmolas registra a mola e fornece com laudo; quem aprova a troca e a calibração é a usina.
- Não envolve desmontar nada. A Jardmolas mede o que está acessível com a máquina parada, o sobressalente do almoxarifado e a mola quebrada que a manutenção guardou.
- Não cria obrigação de compra.

## Metas da primeira temporada

[confirmar com a Jardmolas] Sugestão de indicadores (detalhe em `entrega-do-caderno-e-pos-venda.md`):

- usinas com caderno entregue até 31/03/2027: [meta];
- molas cadastradas (total): [meta];
- usinas com pedido por código até 31/03/2027: [meta];
- contratos de Estoque Garantido assinados antes da safra 2027/28: [meta].
