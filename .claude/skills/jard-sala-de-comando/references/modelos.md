# Modelos da sala

Copie, preencha e salve em `jardmolas/` quando houver sistema de arquivos. Campo sem dado fica `{{assim}}` e marcado [confirmar].

## 1. Ata de reunião (`jardmolas/operacao/atas/AAAA-MM-DD.md`)

```
# Reunião {{data}} — pauta: {{pauta}}
Presentes: {{pessoas}} · Agentes acionados: {{agentes}}

## Decisões
- {{decisão}} — por quê: {{dado}}

## Tarefas
| Tarefa | Dono | Prazo | Status |
|---|---|---|---|

## Pendências [confirmar]
-

## Próxima reunião: o que vamos olhar
-
```

## 2. Ficha de cotação (o que perguntar ao cliente, em uma mensagem só)

```
Para te passar o preço certo hoje, me manda:
1. Foto da peça ao lado de uma trena (de frente e de lado)
2. Marca e modelo da máquina (ou o código da peça original/Jardmolas, se tiver)
3. Quantidade (e se quer programar entregas)
4. Cidade de entrega e se tem preferência de transportadora
5. Prazo que você precisa
```
Para sob medida/OEM: desenho (PDF/DWG/STEP) ou amostra; carga de trabalho e comprimento de trabalho (ou torque e ângulo); ambiente (corrosão, temperatura); volume anual.

## 3. Ficha técnica de mola (uma por código)

```
Código: JM {{nnnn}}    Nome: {{dedo enleirador com olhal / mola de compressão...}}
Aplicação: {{máquina, marca, modelo, posição}}    Revisão: {{n}} de {{data}}
Tipo: compressão | tração | torção | forma de arame (dedo)
Arame: norma {{EN 10270-1 DH / SAE 9254...}}  d = {{mm}}  fornecedor {{Belgo}}
Geometria: Ø ext {{mm}} · Ø int {{mm}} · espiras totais {{n}} · ativas {{n}} · sentido {{direita/esquerda}}
           L0 {{mm}} · pontas {{fechadas e esmerilhadas}} · hastes/braços {{mm}} · olhal {{Ø, raio de dobra}}
Carga: {{N}} em {{mm}} (ou {{N.mm}} em {{°}}), tolerância ±{{%}}
Processo: enrolamento {{máquina}} · alívio de tensões {{°C / min}} · jateamento {{sim/não}} · pré-setagem {{sim/não}}
Acabamento: {{pintura pó cor / óleo / zinco + desidrogenação}}
Inspeção: {{características e frequência}}
Embalagem: {{n}} por {{caixa/amarrado}}, etiqueta com código, lote e cliente
Peso por peça: {{g}} (calc_mola.py)    Custo-padrão: R$ {{}} em {{data}}
```

## 4. Proposta comercial

```
Jardmolas Indústria e Comércio de Molas Ltda · CNPJ 09.394.583/0001-57
Rua Artur Costacurta, 340, Distrito Industrial I, Jardinópolis/SP · {{telefone}} · {{e-mail}}

Proposta {{nº}} · {{data}} · Válida até {{data}}
Para: {{empresa}} · {{cidade/UF}} · A/C {{cargo}}

| Código | Descrição técnica | Aplicação | Qtde | Preço unit. | Total |
|---|---|---|---|---|---|

Faixas de quantidade: {{tabela}}
Prazo de entrega: {{dias úteis}} após confirmação (confirmado pela produção em {{data}})
Frete: {{CIF/FOB}} · Pagamento: {{condição}} · Impostos: {{inclusos/destacados}}
Garantia: {{texto aprovado pelo dono}}
Documentos: certificado do arame do lote {{sim}} · relatório de carga {{sim/não}}

Por que a Jardmolas: {{uma prova: vídeo, número de campo, cliente de referência autorizado}}
{{assinatura}}
```

## 5. Plano de conta (usina ou grupo)

```
Conta: {{grupo / unidade}} · Cidade: {{}} · Moagem/área: {{com fonte}}
Implementos de palha: {{enleiradores, desenleiradores: marca, modelo, quantidade}} [confirmar]
Mapa de pessoas (cargo, papel na compra: usa / especifica / aprova / compra / paga):
  - {{cargo}} — {{papel}} — contato por {{canal}}
Processo de compra: portal {{nome}} · cadastro de fornecedor {{status}} · época do orçamento {{mês}}
Fornecedor atual e dor: {{}}
Estratégia: piloto em {{frente/máquina}} → relatório em {{data}} → proposta anual em {{data}}
Próximos 3 passos (com data e dono):
Risco e como contornar:
```

## 6. Relatório de teste de campo (o documento que fecha contrato)

```
Cliente: {{}} · Máquina: {{marca/modelo}} · Frente/talhão: {{}} · Período: {{datas}}
Dedos Jardmolas: código {{}} · quantidade {{}} · instalados em {{data}}
Comparação: {{dedo anterior / outra máquina na mesma frente}}
Resultado:
  Hectares trabalhados: {{}}
  Quebras Jardmolas: {{}} ({{por 100 ha}}) · Quebras referência: {{}}
  Horas paradas por troca: {{}}
  Custo por hectare (fórmula de vendas-prospeccao.md): Jardmolas {{}} · referência {{}}
Observações do operador/encarregado: {{}}
Fotos: {{}}
Conclusão e próxima etapa: {{}}
Assinado por: {{responsável do cliente}} e {{Jardmolas}}
```

## 7. Análise de falha (8D simplificado)

```
Nº {{}} · Data {{}} · Cliente {{}} · Código {{}} · Lote {{}}
1. Problema: {{o que, onde, quantas, com quantos hectares/horas}}
2. Evidência: fotos da fratura (origem da trinca), peça inteira com trena, regulagem da máquina
3. Contenção: {{troca ao cliente, segregação do lote, inspeção 100%}}
4. Causa provável (tabela de fabrica.md §4): {{fadiga no olhal / frágil / assentamento / aplicação}}
5. Causa confirmada como: {{dureza, ferramenta, forno, regulagem do cliente...}}
6. Ação corretiva: {{processo, ficha técnica, orientação ao cliente}}
7. Verificação: {{como e quando saberemos que resolveu}}
8. Fechamento e lição: {{o que muda no padrão}} · Decisão de garantia: {{}}
```

## 8. Painel semanal (BI e CRM)

```
Semana {{nº}} · {{datas}}
VENDAS: faturado {{R$}} · pedidos {{n}} · ticket médio {{R$}} · novos clientes {{n}}
FUNIL: contas novas {{n}} · tentativas {{n}} · conversas {{n}} · qualificados {{n}}
       orçamentos {{n}} ({{R$}}) · tempo médio de resposta {{h}} · conversão orçamento→pedido {{%}}
CANAIS: revendas ativas {{n}} · pedidos de revenda {{n}} · usinas em teste {{n}}
FÁBRICA: OTIF {{%}} · atrasos {{n}} · carga das máquinas {{%}} · refugo {{%}}
FINANCEIRO: margem de contribuição {{%}} · inadimplência {{%}} · caixa 13 semanas {{ok/alerta}}
MARKETING: Reels {{n}} · conversas vindas do Instagram {{n}} · cliques no WhatsApp do site {{n}}
DECISÕES DA SEMANA PASSADA: {{funcionou / não funcionou / sem dado}}
3 RECOMENDAÇÕES (com o número que sustenta cada uma):
1.
2.
3.
```

## 9. Kit de cadastro de fornecedor (usinas e OEMs pedem)

- Cartão CNPJ, contrato social e última alteração, inscrição estadual
- Certidões negativas (federal, estadual, municipal, FGTS, trabalhista) dentro da validade
- Alvará de funcionamento e licença ambiental/CETESB, se aplicável [confirmar]
- Dados bancários em papel timbrado
- Ficha cadastral do cliente preenchida
- Apresentação da empresa (1 página): o que fabrica, desde quando, onde, capacidade, clientes de referência autorizados
- Certificado de qualidade do arame (Belgo) e exemplo de relatório de inspeção
- Certificação ISO, se existir [confirmar]
- Política de segurança do trabalho/NRs, se a usina pedir

## 10. Autorização de uso de imagem (depoimento)

> "Eu, {{nome}}, autorizo a Jardmolas a usar o vídeo/foto gravado em {{data}}, com meu nome, cidade e falas, nas redes sociais, site, apresentações e feiras da empresa, sem prazo, podendo pedir a retirada a qualquer momento por mensagem."
> Pode ser enviada e respondida por WhatsApp ("Autorizo"). Guardar o print na pasta do cliente.
