# Fórmulas e critérios usados em `mola.py`

Notação: d fio, De diâmetro externo, D = De − d diâmetro médio, C = D/d índice,
Na espiras ativas, Nt espiras totais, G módulo de cisalhamento, E módulo de
elasticidade, Rm limite de resistência à tração do arame, F carga, M momento.

## Compressão (EN 13906-1 / SMI)

- Constante: k = G·d⁴ / (8·D³·Na)
- Tensão de cisalhamento sem correção: τ = 8·F·D / (π·d³)
- Fator de Wahl (curvatura + cisalhamento direto): Kw1 = (4C − 1)/(4C − 4) + 0,615/C
- Após presetting a distribuição muda e usa-se Kw2 = 1 + 0,5/C
- Critério estático SMI: Kw1·τ no sólido ≤ fração "sem preset" × Rm; se não
  passar, Kw2·τ ≤ fração "com preset" × Rm e o processo precisa incluir
  presetting.
- Extremidades (espiras totais e comprimento sólido):

| Extremidade | Nt | Ls | Passo |
|---|---|---|---|
| Fechada e retificada | Na + 2 | Nt·d | (L0 − 2d)/Na |
| Fechada | Na + 2 | (Nt + 1)·d | (L0 − 3d)/Na |
| Aberta e retificada | Na + 1 | Nt·d | L0/(Na + 1) |
| Aberta | Na | (Nt + 1)·d | (L0 − d)/Na |

- Folga mínima entre espiras na carga máxima: Sa = (0,0015·D²/d + 0,1·d)·Na;
  comprimento mínimo de trabalho = Ls + Sa. Para carga dinâmica multiplique Sa
  por 1,5.
- Flambagem: sK = L0 · 0,5/(1 − G/E) · [1 − √(1 − (1 − G/E)/(0,5 + G/E) · (π·D/(ν·L0))²)].
  Se o termo dentro da raiz for negativo, a mola não flamba. ν: 0,5 pratos
  paralelos guiados; 0,7 um lado articulado; 1 dois articulados; 2 um lado livre.
- Aumento do diâmetro externo no sólido: ΔDe = 0,1·(p² − 0,8·p·d − 0,2·d²)/D.
- Frequência natural (extremos fixos): f = d/(2π·Na·D²) · √(G/(2ρ)).
- Fadiga (somente aço carbono e baixa liga, d < 10 mm): dados de Zimmerli para
  vida infinita — sem shot peening Ssa = 241 MPa, Ssm = 379 MPa; com shot
  peening Ssa = 398 MPa, Ssm = 534 MPa; Ssu = 0,67·Rm; reta de Goodman.

## Tração (EN 13906-2 / Shigley)

- Espiras ativas: Na = Nb + G/E (os ganchos contribuem).
- k como na compressão; F = Fi + k·(L − L0).
- Comprimento livre com ganchos inteiros sobre o centro: L0 = (Nb + 1)·d + 2·(D − d).
- Tensão inicial fabricável: τi = 231/e^(0,105·C) ± 6,9·(4 − (C − 3)/6,5) MPa
  para aço; escalada por G/79 300 para outros materiais.
- Flexão no gancho: σ = F·[K·16·D/(π·d³) + 4/(π·d²)], K = (4C1² − C1 − 1)/(4C1·(C1 − 1)),
  C1 = 2·r1/d (r1 = raio médio do gancho).

## Torção (EN 13906-3 / SMI)

- Espiras ativas equivalentes: Na = Nb + (L1 + L2)/(3π·D).
- Constante: M/θ = E·d⁴/(10,8·D·Na) N·mm por volta (10,8 em vez do teórico
  10,2 cobre o atrito entre espiras e no pino).
- Flexão na fibra interna: σ = Ki·32·M/(π·d³), Ki = (4C² − C − 1)/(4C·(C − 1)).
- Diâmetro médio com θ voltas de deflexão: D' = D·Nb/(Nb + θ).
- Comprimento do corpo: (Nb + 1 + θ)·d para espiras encostadas.

## Portinhola (válvula de retenção dupla portinhola, API 594)

Cada portinhola é um meio-disco de raio R articulado no pino central.

- Área: A = π·R²/2. Centroide a 4R/(3π) da aresta reta.
- Momento da pressão diferencial: M = Δp·A·(4R/(3π) + e), com e a distância da
  aresta ao centro do pino. Para e = 0, M = 2·Δp·R³/3.
- Pressão de início de abertura: Δp = n·M_mola(pré-ângulo) / (A·braço).
- Montagem **independente** (uma perna na portinhola, outra no batente): a mola
  deflete o curso da portinhola. Montagem **entre portinholas** (uma perna em
  cada): a mola deflete o dobro do curso — é o caso que mais sobretensiona.
- O peso da portinhola e a orientação da linha somam ou subtraem torque; o
  cálculo da mola isola só a contribuição dela.

## Frações admissíveis de Rm (carga estática)

| Família | Compressão sem / com preset | Tração corpo / gancho flexão | Torção aliviada / residual favorável |
|---|---|---|---|
| Carbono patenteado e trefilado | 45% / 60% | 45% / 75% | 80% / 100% |
| Temperado, Cr-V, Cr-Si | 50% / 65% | 45% / 75% | 85% / 100% |
| Inox austenítico e ligas não ferrosas (níquel, cobalto) | 35% / 55% | 35% / 55% | 60% / 80% |

Fonte: SMI Handbook of Spring Design e Shigley, tabelas de tensões admissíveis
para aplicações estáticas. Usou-se o limite inferior das faixas publicadas.
Para temperatura elevada, a tensão admissível real é ditada pela relaxação
(ver `jm-inconel-x750`).

## Tensão de projeto a quente (relaxação)

Para Inconel X-750 o banco de materiais traz a tabela de tensões de projeto
do boletim do fabricante da liga (Special Metals, Tabela 30): tensão máxima
que produz 5% de relaxação em 7 dias, por faixa de temperatura. Com `--temp`,
a calculadora compara:

- molas helicoidais de compressão: tensão de cisalhamento corrigida (Wahl) na
  carga máxima contra `tau_relax`;
- molas de torção e de portinhola: tensão de flexão no ângulo máximo contra
  `sigma_relax` (valores de molas planas da mesma tabela, que trabalham em
  flexão como a mola de torção de fio redondo).

Onde a tabela dá faixa (por exemplo 414–483 MPa), o valor menor é para
relaxação mínima e o maior para quando alguma relaxação inicial é tolerável.
Fora da faixa de temperatura tabelada para a condição, a calculadora avisa
que não há tensão de projeto publicada (há folga de 2 °C para o
arredondamento de °F para °C: 371, 538 e 649 °C são 700, 1000 e 1200 °F). O
veredito estático usa o módulo a 20 °C; cargas e relaxação usam o módulo na
temperatura informada. Na mola de tração confere-se o corpo. Para os demais materiais vale apenas
o limite de temperatura (`temp_max`).
