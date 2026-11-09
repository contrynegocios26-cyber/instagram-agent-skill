---
name: jm-orcamento-tecnico
description: >-
  Transforma um pedido de mola da Jardmolas (mensagem de WhatsApp, saída do
  Identificador de Molas, foto com medidas, desenho ou amostra descrita) em
  ficha técnica conferida e resposta de orçamento pronta para enviar. Use
  sempre que alguém colar medidas de mola, pedir para "conferir essa mola",
  "calcular a constante", "responder esse orçamento", "o que falta perguntar
  ao cliente", ou mandar um pedido que começa com "Pedido de orçamento:
  Identificador de Molas".
---

# jm-orcamento-tecnico

Recebe o pedido como ele chega e devolve três coisas: a ficha técnica
calculada, o que falta perguntar ao cliente e a mensagem de resposta. Quem
decide preço e prazo é a Jardmolas. Esta skill nunca inventa os dois.

## Ferramenta

```bash
python3 mola.py compressao --d 6 --De 45 --L0 110 --Nt 10 [--pontas abertas] [--curso 30] [--Rm 1600] [--inox]
python3 mola.py tracao --d 3 --De 24 --Nb 35 --Li 150 [--F0 20] [--alongamento 40]
python3 mola.py torcao --d 4 --De 32 --Nb 6 --L1 60 --L2 40 [--giro 45]
python3 mola.py ... --json
```

Rode sempre. Não calcule de cabeça. O script avisa sobre índice fora da faixa,
mola que fecha antes do curso, tensão alta, flambagem e eixo apertado na
torção.

## Passo a passo

1. **Leia o pedido inteiro** e separe: tipo de mola, onde trabalha (máquina,
   marca, modelo), medidas, material/acabamento, quantidade, prazo, quem pede.
   Mensagem do Identificador já vem com tudo marcado com `•`.
2. **Confira se as medidas fecham.** Rode o `mola.py`. Se der erro ou alerta,
   isso vira pergunta ao cliente, não correção silenciosa.
3. **Liste o que falta**, só o que muda o projeto ou o preço:
   - compressão: pontas (fechadas/lixadas), curso de trabalho ou carga de trabalho, se tem guia;
   - tração: tipo e posição dos ganchos, tensão inicial (ou amostra);
   - torção e dedo: sentido do enrolamento, ângulo livre das pernas, forma das pontas;
   - todas: material ou acabamento se trabalha no tempo, no calor ou em contato com caldo;
   - mola de válvula de segurança: pressão de ajuste e se precisa de laudo do lote.
4. **Escreva a ficha** (modelo abaixo).
5. **Escreva a resposta ao cliente** no tom da Jardmolas: direto, sem
   "prezado", sem "soluções". Se faltar dado, a mensagem faz no máximo 3
   perguntas, numeradas, e diz que a amostra resolve tudo.
6. **Preço e prazo:** deixe `[preço: comercial]` e `[prazo: produção]`. Se a
   equipe já passou a tabela ou a regra de preço desta mola, use e diga de onde
   veio.

## Modelo da ficha

```
FICHA TÉCNICA · [tipo] · [cliente] · [data]
Aplicação: [máquina / equipamento / TAG]
Medidas: d __ mm · De __ mm · L0 __ mm · Nt __ · pontas __
Material: __ (Belgo, classe __)   Acabamento: __
Calculado: k __ N/mm (__ kgf/mm) · fechada __ mm · força fechada __ N
Alertas: [saída do mola.py]
Falta confirmar: [lista]
Quantidade: __   Urgência: __
Código JM: [se já existir no Caderno de Molas do cliente]
```

## Modelo de resposta (WhatsApp)

```
[Nome], recebi as medidas da mola do [máquina].
Pelo que você mandou, é uma mola de [tipo] com arame de [d] mm, [De] mm por fora e [Nt] voltas.
[Se faltar algo:] Para fechar o orçamento preciso de 2 coisas:
1. [pergunta]
2. [pergunta]
Se for mais fácil, manda uma foto de lado em cima de uma régua.
[Se completo:] Orçamento: [preço: comercial] por peça, [quantidade] peças, prazo [prazo: produção].
```

## Regras

- Medida aproximada do cliente é ponto de partida. Nunca diga que a mola
  "vai servir" sem amostra ou confirmação da engenharia.
- Mola de válvula de segurança e de vaso de pressão: sempre pedir a pressão de
  ajuste e oferecer laudo do lote. Não sugerir alteração de carga.
- Compatibilidade com marca de máquina: escreva "compatível com [marca e
  modelo]". Nunca "original [marca]".
- Se o pedido for de usina e a mola não tiver código JM, sugira o Caderno de
  Molas da Usina (ver `../jm-caderno-usina/SKILL.md`).
- Sem travessão (—) nas mensagens. Sem "estamos à disposição". Termine com a
  próxima ação.
