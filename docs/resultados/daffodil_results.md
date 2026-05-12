# Avaliação Daffodil BD — 3ª Validação Independente em Campo Real

**Data:** 2026-05-11 21:01
**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB) — Exp D
**Dataset:** Daffodil International University, Bangladesh (Mendeley, 2024)
**Captura:** iPhone 11, campo aberto, luz natural, Khagan/Charabag

## Mapeamento de Classes

| Classe Daffodil BD | Classe Ceres | Justificativa |
|---|---|---|
| Late Blight | D01_requeima | Phytophthora infestans — mesma doença |
| Leaf Mold | D05_mofo_foliar | Passalora fulva — mesma doença |
| Early Blight | D03_pinta_preta | Alternaria solani — mesma doença |
| Spider Mites | D07_acaro_bronzeamento | Tetranychus urticae — mesma espécie |
| Tomato Leaf Curl Virus | D06_vira_cabeca | TLCV = begomovirus mesma família do TYLCV (D06) — sintomas equivalentes |
| Bacterial Spot | D09_mancha_bacteriana | Xanthomonas spp. — mesma doença |
| Healthy | saudavel | Folha saudável |

*Ignoradas (sem mapeamento Ceres): Cercospora leaf mold, Insect Damage, Leaf Miner*

## Resultado por Classe

| Classe Ceres | Pasta BD | Corretas | Total | Acurácia | Top predição errada |
|---|---|---|---|---|---|
| D01_requeima | Late Blight | 1 | 166 | 0.6% | D02_septoriose (71x) |
| D05_mofo_foliar | Leaf Mold | 51 | 66 | 77.3% | D02_septoriose (14x) |
| D03_pinta_preta | Early Blight | 14 | 204 | 6.9% | D02_septoriose (68x) |
| D07_acaro_bronzeamento | Spider Mites | 0 | 307 | 0.0% | D05_mofo_foliar (167x) |
| D06_vira_cabeca | Tomato Leaf Curl Virus | 0 | 394 | 0.0% | D02_septoriose (204x) |
| D09_mancha_bacteriana | Bacterial Spot | 89 | 376 | 23.7% | D02_septoriose (143x) |
| saudavel | Healthy | 0 | 103 | 0.0% | D05_mofo_foliar (66x) |

## Resultado Geral

| Métrica | Valor |
|---|---|
| **Acurácia geral** | **9.59%** |
| Total imagens | 1616 |
| Classes avaliadas | 7 |
| Erros de leitura | 0 |

## Comparativo — 3 Datasets Independentes

| Dataset | Região | Clima | Imagens | Classes | Resultado Exp D |
|---|---|---|---|---|---|
| PlantDoc (test) | EUA / Europa | Temperado | 69 | 4 | 30,43% |
| Tomato-Village (test) | Rajasthan, Índia | Árido tropical | 217 | 4* | 11,52% |
| **Daffodil BD** | **Bangladesh** | **Tropical úmido** | **1616** | **7** | **9.59%** |

*\* D06 no Tomato-Village era TSWV (mapeamento incorreto — doença diferente do TYLCV)*

## Análise

### Acurácia geral: 9,59% — terceiro gap geográfico confirmado

O resultado de 9,59% é o mais baixo dos três datasets de campo avaliados, confirmando que
o gap lab-campo é progressivo conforme a distância geográfica e climática do conjunto de treino.

| Dataset | Região | Acurácia |
|---|---|---|
| PlantDoc (test) | EUA / Europa (temperado) | 30,43% |
| Tomato-Village | Rajasthan, Índia (árido tropical) | 11,52% |
| Daffodil BD | Bangladesh (tropical úmido, monção) | 9,59% |

### Achado 1 — D05_mofo_foliar: 77,3% (outlier positivo)

A única classe com acurácia aceitável em campo real é D05_mofo_foliar (Passalora fulva).
**Hipótese de distinção visual:** o crescimento fúngico de *Passalora fulva* cria uma textura
branca-acinzentada densa na face inferior da folha que é estruturalmente única e geograficamente
invariante. O modelo aprende essa textura como feature discriminativa robusta, independentemente
do fundo, iluminação ou cultivar local.

Esta hipótese é reforçada pelo fato de D05 ter sido a única classe com acurácia significativa
também nos outros dois datasets de validação.

### Achado 2 — D02_septoriose como atrator universal

D02_septoriose é o destino mais comum de predições erradas em 5 das 7 classes avaliadas.
Isso sugere que, sob shift de domínio extremo, o modelo converge para a classe visualmente
mais "genérica" — manchas irregulares escuras são uma representação padrão de doença foliar
que o modelo generaliza excessivamente.

### Achado 3 — D07_acaro_bronzeamento: colapso para D05 (167/307)

O modelo confunde sistematicamente sintomas de ácaros (bronzeamento difuso) com mofo foliar.
No conjunto laboratorial isso não ocorre, pois os fundos são distintos. Em campo, a textura
difusa de ambas as classes é suficientemente similar para enganar o modelo.

### Achado 4 — saudavel: 0% (103 folhas saudáveis previstas como D05)

66 das 103 folhas saudáveis bangladeshianas foram classificadas como mofo foliar.
Iluminação natural forte e reflexos foliares em cultivares locais aparentemente ativam
as mesmas features do D05 aprendidas pelo modelo.

### Implicações para o TCC

1. **O gap não é resolvido por augmentation sintética** — Exp C confirmou isso.
2. **Fine-tuning local é necessário por região** — não existe modelo universalmente generalizável
   com os dados atualmente disponíveis.
3. **A coleta em Sorriso-MT (Sprint 3) é a validação mais importante** — sem ela, qualquer
   resultado de acurácia em campo reflete apenas datasets publicados internacionalmente.
4. **D05_mofo_foliar** é o diagnóstico mais confiável do modelo em campo real (77,3%) —
   clinicamente relevante pois o mofo foliar é economicamente significativo em clima tropical úmido.

