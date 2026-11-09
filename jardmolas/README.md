# Kit comercial Jardmolas · 2026/27

Material para a Jardmolas (fábrica de molas agrícolas e industriais,
Jardinópolis-SP) vender mais na entressafra 2026/27 e no ano seguinte.
Preparado em 09/11/2026.

**Comece por aqui:** `apresentacao/plano-jardmolas.html` (a proposta em uma
página, com as duas ferramentas para testar) e
`00-diagnostico-e-plano/plano-90-dias.md`.

## A ideia

Quem tem o desenho da mola recebe o pedido. A usina hoje compra mola como peça
avulsa e urgente, sem código. A Jardmolas entra na entressafra, cataloga as
molas críticas de cada usina (Caderno de Molas), dá um código JM para cada uma
e passa a ser o lugar natural para repor. Em paralelo, deixa simples pedir
para quem tem uma mola quebrada na mão (Identificador de Molas) e mostra a
fábrica para quem compra.

## O que tem em cada pasta

| Pasta | Conteúdo | Para quem |
| --- | --- | --- |
| `apresentacao/` | A proposta em uma página (HTML) | Dono da Jardmolas |
| `00-diagnostico-e-plano/` | Diagnóstico, plano de 90 dias, perguntas para a Jardmolas | Dono e agência |
| `01-caderno-de-molas/` | **App de levantamento** (`caderno-de-molas.html`, funciona sem internet), oferta, roteiro da visita técnica, abordagem por cargo, objeções, Estoque Garantido, entrega e pós-venda, atendimento no WhatsApp, instalação do app | Comercial e técnico |
| `02-identificador/` | **Identificador de Molas** (`identificador-de-molas.html`) e instalação no site | Webmaster e comercial |
| `03-conteudo/` | Estratégia, perfil do Instagram, roteiros de Reels, carrosséis, stories e WhatsApp, LinkedIn, calendário de 30 dias, guia de gravação | Quem cuida das redes |
| `04-mercado-e-alvos/` | Usinas no raio de 200 km com grupo, distância e quem procurar; fabricantes, revendas e associações; feiras de 2027; concorrentes | Comercial |
| `05-seo-e-site/` | Diagnóstico do site, máquinas e palavras-chave, páginas prontas, pautas de blog, Perfil no Google e Google Ads | Webmaster e agência |
| `06-revenda-kits-feiras/` | Programa de revenda com expositor, kits pré-safra com troca de dedos, roteiro de feira | Comercial |
| `07-skills/` | Quatro skills para o Claude: `jm-orcamento-tecnico` (com `mola.py`), `jm-caderno-usina` (com `caderno.py`), `jm-prospeccao`, `jm-conteudo` | Equipe Jardmolas |

## As ferramentas

| Ferramenta | O que faz | Como testar |
| --- | --- | --- |
| `02-identificador/identificador-de-molas.html` | O cliente escolhe o tipo, mede seguindo o desenho cotado, vê constante, força e alertas, e manda o pedido pronto no WhatsApp. `?origem=` marca de onde veio o pedido. | Abrir o arquivo no navegador |
| `01-caderno-de-molas/caderno-de-molas.html` | Levantamento em campo: cadastro com fotos, código JM automático, criticidade e estoque mínimo, caderno em PDF A4, planilha CSV, backup. Sem internet quando hospedado em https. | Abrir o arquivo; já vem com uma usina de exemplo |
| `07-skills/jm-orcamento-tecnico/mola.py` | Calculadora de compressão, tração e torção, com alertas de engenharia | `python3 mola.py compressao --d 6 --De 45 --L0 110 --Nt 10` |
| `07-skills/jm-caderno-usina/caderno.py` | Lê o backup do app e escreve resumo, lista de troca e proposta de Estoque Garantido com valores | `python3 caderno.py exemplo-backup.json --precos precos-exemplo.csv` |

## Instalar as skills no Claude

```bash
cp -r jardmolas/07-skills/jm-* ~/.claude/skills/
```

Ou, num projeto, copie para `.claude/skills/`. A skill `jm-conteudo` usa as
skills de Instagram deste repositório (`skills/ig-*`); instale as duas juntas.

## Regras que valem para todo o kit

- Nada de prazo, garantia, preço ou capacidade sem a Jardmolas confirmar. Está
  marcado como `[confirmar com a Jardmolas]` onde aparece.
- Marca de terceiros só como "compatível com [marca e modelo]".
- Medida de campo é referência; a engenharia da Jardmolas confere antes de
  fabricar.
- Nenhuma visita a usina sem a documentação de segurança pronta, e nenhuma
  medição com equipamento em operação.
- Distâncias e listas de usinas são estimativas da pesquisa de 09/11/2026,
  com fonte em cada linha. Conferir antes de ligar.
