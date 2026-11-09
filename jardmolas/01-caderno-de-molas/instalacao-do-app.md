# App Caderno de Molas: instalação e uso em campo

Arquivos desta pasta que formam o app:

| Arquivo | Para que serve |
| --- | --- |
| `caderno-de-molas.html` | O app inteiro: cadastro das molas, fotos, cálculo, caderno em PDF, planilha e backup |
| `sw.js` | Guarda o app no celular para abrir sem internet dentro da usina |
| `manifest.webmanifest` | Permite "instalar" o app na tela inicial com nome e ícone |
| `icone-192.png`, `icone-512.png` | Ícone do app |

## 1. Publicar (uma vez, pelo webmaster)

1. Abra `caderno-de-molas.html` num editor e, no bloco `CONFIG`, troque
   `modoProposta: true` por `false`. Se quiser começar sem a usina de exemplo,
   troque também `carregarExemplo: true` por `false`.
2. Suba os 5 arquivos juntos, na mesma pasta, num endereço com **https**. Por
   exemplo `https://jardmolas.com.br/caderno/`. Pode ser uma pasta sem link no
   menu: o app é de uso interno.
3. Abra `https://jardmolas.com.br/caderno/caderno-de-molas.html` e confira se
   carrega.

Sem https o app funciona, mas não abre sem internet.

## 2. Instalar no celular do técnico (2 minutos, com internet)

**Android (Chrome):** abra o endereço, toque nos três pontos e em
"Instalar app" ou "Adicionar à tela inicial".

**iPhone (Safari):** abra o endereço, toque em Compartilhar e em "Adicionar à
Tela de Início".

Depois de instalado, ative o modo avião e abra o app pelo ícone. Se abrir, está
pronto para a usina.

## 3. Na usina

1. **Nova usina**: preencha nome, unidade, cidade, contato e a **sigla** (3 ou
   4 letras, sem repetir outra usina). A sigla vira o código: `JM-SMA-001`.
2. Aba **Molas**, botão **+ Mola**. Para cada mola:
   - área, equipamento, TAG e função;
   - tipo e medidas (o cálculo aparece embaixo; se aparecer "confira as
     medidas", meça de novo);
   - peças instaladas, estado e criticidade (A para a produção, B tem reserva,
     C não para). O estoque mínimo é sugerido sozinho;
   - até 3 fotos: de lado com régua, de frente e no lugar onde trabalha;
   - o que o mecânico contou.
3. Mola igual em vários lugares: abra a primeira e toque em **Duplicar para
   outro local**. Só muda a TAG.
4. Só meça com o equipamento parado e bloqueado. Se não estiver liberado, anote
   na observação e volte depois.

## 4. No fim do dia (não pule)

1. Aba **Dados e backup**, **Baixar backup desta usina**.
2. Mande o arquivo `.json` para o escritório pelo WhatsApp ou e-mail.

Os dados ficam só no celular. Se o celular quebrar ou for formatado sem
backup, o levantamento se perde.

## 5. No escritório

1. Abra o mesmo endereço no computador, **Dados e backup**, **Importar backup**.
2. Aba **Caderno**: confira as fichas e use **Imprimir ou salvar PDF** (no
   Chrome, escolha "Salvar como PDF", papel A4, com "Gráficos de plano de
   fundo" marcado para a capa verde sair).
3. **Baixar planilha (CSV)** abre no Excel com uma linha por mola.
4. Para a proposta de Estoque Garantido com valores, rode o script da skill:
   `python3 ../07-skills/jm-caderno-usina/caderno.py backup.json --precos precos.csv`.

## Limites desta versão

- Não sincroniza sozinho entre celulares. Dois técnicos na mesma usina: cada
  um cria a sua parte com siglas diferentes (`SMA` e `SMB`) ou um importa o
  backup do outro no fim do dia.
- Fotos são reduzidas para cerca de 1.100 px para caber no celular. Se a
  engenharia precisar de detalhe, tire também a foto pela câmera normal.
- Se num aparelho aparecer o aviso amarelo "Este navegador não está guardando
  os dados", saia do modo anônimo.
