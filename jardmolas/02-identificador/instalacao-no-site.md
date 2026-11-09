# Identificador de Molas: como colocar no site

Arquivo: `identificador-de-molas.html`. Uma página só, sem banco de dados e sem
servidor. Funciona em qualquer hospedagem que aceite um arquivo HTML.

## O que a página faz

1. O cliente escolhe o tipo de mola (compressão, tração, torção, dedo de
   enleirador ou "não sei").
2. Diz onde ela trabalha (enleirador, enfardadeira, válvula, peneira etc.).
3. Mede com paquímetro ou régua. Cada campo explica como medir e o desenho
   destaca a cota que ele está preenchendo.
4. A página calcula na hora: diâmetro médio, índice, constante (N/mm e kgf/mm),
   altura fechada, força com a mola fechada, peso por peça. E avisa quando a
   medida não fecha (externo menor que dois arames, comprimento menor que a
   mola fechada, mola comprida que precisa de guia).
5. O botão abre o WhatsApp da Jardmolas com o pedido pronto. O cliente anexa a
   foto na conversa.

Nada é guardado: o pedido só existe na mensagem do WhatsApp.

## Antes de publicar (5 minutos)

Abra o arquivo num editor de texto e procure o bloco `CONFIGURAÇÃO`:

```js
var CONFIG = {
  whatsapp: '5516991760936',          // DDI + DDD + número, só dígitos
  whatsappTexto: '(16) 99176-0936',
  modoProposta: true,                 // false para tirar a faixa amarela de protótipo
  origem: 'Identificador de Molas'
};
```

- Troque `modoProposta: true` por `modoProposta: false`. Isso tira a faixa
  amarela "Protótipo preparado para a Jardmolas".
- Confirme o número do WhatsApp que vai receber os orçamentos. Se for outro
  (um WhatsApp Business só do comercial, por exemplo), troque nos dois campos.

## Onde publicar

**Opção A (recomendada): página própria no domínio.**
Suba o arquivo como `jardmolas.com.br/identificador-de-molas/index.html`
(ou `identificador-de-molas.html` na raiz). Endereço final:
`https://jardmolas.com.br/identificador-de-molas`.

**Opção B: dentro de uma página do site atual.**
Se o painel do site não aceitar arquivo solto, suba o HTML em qualquer
hospedagem estática e coloque na página do site:

```html
<iframe src="https://ENDERECO/identificador-de-molas.html"
        style="width:100%;height:2400px;border:0" loading="lazy"
        title="Identificador de Molas"></iframe>
```

A opção A é melhor para o Google e para o celular.

## Onde colocar o link

- Menu principal: "Identificar minha mola".
- Toda página de produto, logo acima do formulário: "Não sabe as medidas? Use
  o Identificador".
- Bio do Instagram e botão do Perfil da Empresa no Google.
- Resposta automática do WhatsApp Business ("Para orçamento rápido, mande as
  medidas por aqui: ...").
- QR code no expositor de balcão das revendas e no estande das feiras.

## Saber de onde veio cada orçamento

Acrescente `?origem=` no link e a origem aparece na primeira linha da mensagem
que chega no WhatsApp. Exemplos:

| Onde está o link | Link |
| --- | --- |
| Bio do Instagram | `/identificador-de-molas?origem=instagram` |
| Expositor na Coopercitrus de Bebedouro | `/identificador-de-molas?origem=balcao-coopercitrus-bebedouro` |
| Estande da Fenasucro | `/identificador-de-molas?origem=fenasucro` |
| Campanha no Google | `/identificador-de-molas?utm_source=google&utm_medium=cpc` |

A mensagem chega assim: `*Pedido de orçamento: Identificador de Molas · instagram*`.

## Medir no Google Analytics (se o site tiver GA4 ou Tag Manager)

A página dispara dois eventos sozinha, sem configurar nada no código:

| Evento | Quando |
| --- | --- |
| `identificador_whatsapp` | O cliente tocou em Enviar pelo WhatsApp (com `tipo_mola`, `setor` e `urgencia`) |
| `identificador_copiar` | O cliente copiou o texto para mandar por e-mail |

No GA4, marque `identificador_whatsapp` como evento principal (conversão). Se
houver campanha no Google Ads, importe essa conversão.

## Testar depois de publicar

1. Abra no celular, escolha Compressão e preencha d 6, De 45, L0 110, Nt 10.
   A ficha deve mostrar constante perto de 27 N/mm.
2. Toque em Enviar pelo WhatsApp. Tem que abrir a conversa com a Jardmolas e o
   texto completo.
3. Teste com `?origem=teste` e confira a origem na primeira linha.

## Mudanças comuns

- **Incluir outra máquina na lista:** procure `var SETORES` e copie uma linha.
- **Mudar textos de ajuda:** procure `var CAMPOS`, campo `ajuda`.
- **Trocar cores:** bloco `:root` no começo do arquivo (verde `--brand`,
  amarelo `--accent`).
