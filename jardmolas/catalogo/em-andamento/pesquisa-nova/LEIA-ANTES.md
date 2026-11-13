# Instruções comuns — pesquisa de referências de molas (leia tudo antes de começar)

## Para que serve
Uma fábrica de molas brasileira (molas helicoidais de fio redondo: compressão, tração, torção, e dedos/garfos de
arame) está montando um catálogo para clientes: "Molas para implementos agrícolas", organizado por setor e por
marca de máquina. Para cada mola de máquina agrícola precisamos da **referência de mercado**: marca e modelo da
máquina, nome da peça, **código original do fabricante**, medidas publicadas e a **fonte**.
O dono exige **zero erro**. Uma linha errada no catálogo é pior que uma linha a menos. Nada é inventado, nada é
deduzido: só entra o que você leu numa página.

## Ferramentas e limites deste ambiente
- **WebFetch não funciona aqui. Não use.**
- **WebSearch**: orçamento apertado e compartilhado. Use no máximo o número de buscas dito na sua tarefa. Faça
  buscas específicas (marca + "mola" + máquina + código).
- **Bash com curl** é o caminho principal para LER PÁGINAS: `curl -sS -m 25 -L "URL"`. Regras:
  - NÃO defina User-Agent de navegador (nada de `-A "Mozilla..."`); use o curl como está.
  - NÃO desligue verificação TLS, não mexa em proxy.
  - Se vier `CONNECT tunnel failed, response 403`, o site não está liberado na rede: não insista nele agora.
    (A liberação de alguns sites foi pedida e pode chegar durante o seu trabalho: teste de novo uma vez mais
    tarde.) Se vier 403/503 do próprio site (bloqueio de robô), desista desse site; não tente contornar.
  - Sites pedidos para liberação (teste antes de usar): thorcomponentes.com.br, www.agridisco.com,
    catalogo.marchesan.com.br, www.revenda.jumil.com.br, revenda.jumil.com.br, loja.jumil.com.br, ingapecas.com,
    www.commersul.com.br, loja.agritork.com.br, www.jbagricola.com.br, www.lojanogueira.com.br, hh.net.br,
    partao.com, gb.sparex.com, shop.bigdutchman.com, www.agrotrator.com.br, unifort.com.br,
    www.plantiodistribuidora.com.br, plantforte.com.br, www.acamargo.com. Já liberado: www.kramp.com.
  - Para ler HTML: `curl ... | python3 -c "import sys,re,html; t=sys.stdin.read(); t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t); print(re.sub(r'\s+',' ',html.unescape(t))[:6000])"`.
    Para achar links: `grep -o 'href="[^"]*"'`. PDFs: baixe para o scratchpad e use `pdftotext -layout`.
  - Grave arquivos só dentro de `/tmp/claude-0/-home-user-instagram-agent-skill/a44018b1-0e82-5173-b144-b41abd2c67b9/scratchpad/`.
    Não altere nada em `/home/user/instagram-agent-skill` (só leitura).
- Não crie subagentes. Trabalhe direto.

## A base atual (só leitura)
`/home/user/instagram-agent-skill/jardmolas/catalogo/referencias-agro.csv` (separador `;`, UTF-8 com BOM).
Colunas: setor; maquina; marca; modelos; peca; tipo; codigo_original; ref_reposicao; arame_mm; comprimento_mm;
diametro_mm; diametro_ref; largura_mm; medida_publicada; nota; situacao; conferido; obs_pesquisa; fonte; id.
`situacao` = `catalogo` (está no catálogo) ou `fora: motivo`. Leia as linhas do seu setor (inclusive as `fora`,
para não repetir pesquisa já descartada).

## Seu trabalho tem duas partes
1. **Conferir** as linhas da base do seu setor cuja fonte você consegue abrir com curl: abra a página, confirme
   código, nome da peça, marca, modelos e medidas. Registre `acao`: `confirma`, `corrige` (preencha os campos
   certos e diga em `obs` o que mudou) ou `descarta` (diga por quê). Use `id_base` = coluna `id` da base.
2. **Achar referências novas** (`acao`: `nova`), de preferência lidas na página (catálogo de peças do fabricante,
   loja oficial, revenda). Linha vinda só de resumo de busca vale menos: marque `verificado`: `busca`.

## O que entra e o que NÃO entra
Entra: mola de fio redondo — compressão, tração, torção — e dedos/garfos/dentes de arame com espira.
NÃO entra (não registre): feixe de molas, mola plana/lâmina, mola prato (Belleville), mola a gás, amortecedor,
mola espiral de partida (fita), rosca sem-fim/helicoide de adubo, dedo retrátil de caracol (é pino), peça
fundida, haste "S" chata, conjunto montado (vareta + mola, braço + mola, kit com outras peças), peça de plástico.
Também não registre: código interno de loja (SKU) como se fosse código original; marca deduzida pelo prefixo do
código; medida sem rótulo "adivinhada" (se a fonte dá "12 x 50 x 85" sem dizer o que é cada número, copie
assim em `medida_publicada` e deixe os campos numéricos vazios).
Se a peça não tem função nem tipo identificado (só "MOLA" e um código), registre mesmo assim com
`peca_pt`: "Mola" e diga em `obs`: "função não identificada" — eu decido depois.

## Formato de saída
Grave um JSON (lista de objetos) no arquivo indicado na sua tarefa. Todos os valores são texto; vazio = não
informado. Grave o arquivo logo que tiver as primeiras linhas e vá regravando (se você for interrompido, o
que está no arquivo se aproveita).

```json
{
 "acao": "nova | confirma | corrige | descarta",
 "id_base": "id da linha da base, quando confirma/corrige/descarta",
 "setor": "nome do setor (use o da sua tarefa)",
 "maquina": "tipo de máquina e, se souber, o conjunto: ex. 'Plantadeira — linha de adubo'",
 "marca": "marca da MÁQUINA (ex.: Tatu Marchesan)",
 "modelos": "modelos em que a peça é usada, como a fonte lista (sem comentário)",
 "peca_pt": "nome da peça como o mercado brasileiro chama",
 "peca_original": "nome exatamente como está na fonte",
 "codigo_original": "código do fabricante da máquina; vários separados por ';'",
 "ref_aftermarket": "número em catálogo de reposição, com o nome do catálogo: 'Sparex S.78950; Thor TH28180008'",
 "arame_mm": "", "comprimento_mm": "", "espira_mm": "", "espira_ref": "interno | externo | (vazio)",
 "medida_publicada": "medidas como a fonte publica, quando não dá para rotular",
 "obs": "o que o catálogo NÃO deve mostrar: dúvidas, divergências entre fontes, quantidade por máquina etc.",
 "fonte": "URL da página onde está o código (a mais direta)",
 "verificado": "pagina (li a página com curl e o código e o nome estão nela) | busca (só resumo de busca)",
 "trecho": "até 200 caracteres copiados da página que mostram código + nome (obrigatório se verificado = pagina)"
}
```

## Relatório final (curto)
Quantas linhas por ação e por marca; quantas `verificado: pagina`; o que procurou e não achou; sites que não
abriram. Sem floreio: é para outro agente ler.
