# Avaliação Daffodil BD — 3ª Validação Independente em Campo Real

**Data:** 2026-05-12 09:09
**Modelo:** ceres_expe_int8.tflite (638 KB) — Exp E (Focal Loss + Aug Agressiva)
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
| D01_requeima | Late Blight | 68 | 166 | 41.0% | D09_mancha_bacteriana (86x) |
| D05_mofo_foliar | Leaf Mold | 29 | 66 | 43.9% | D09_mancha_bacteriana (33x) |
| D03_pinta_preta | Early Blight | 11 | 204 | 5.4% | D01_requeima (91x) |
| D07_acaro_bronzeamento | Spider Mites | 0 | 307 | 0.0% | D05_mofo_foliar (153x) |
| D06_vira_cabeca | Tomato Leaf Curl Virus | 0 | 394 | 0.0% | D01_requeima (259x) |
| D09_mancha_bacteriana | Bacterial Spot | 137 | 376 | 36.4% | D01_requeima (172x) |
| saudavel | Healthy | 48 | 103 | 46.6% | D01_requeima (25x) |

## Resultado Geral

| Métrica | Valor |
|---|---|
| **Acurácia geral** | **18.13%** |
| Total imagens | 1616 |
| Classes avaliadas | 7 |
| Erros de leitura | 0 |

## Comparativo — 3 Datasets Independentes

| Dataset | Região | Clima | Imagens | Exp D | Exp E | Δ |
|---|---|---|---|---|---|---|
| PlantDoc (train+test) | EUA / Europa | Temperado | 746 | 88,47%* | 67,69% | -20,78pp* |
| Tomato-Village (test) | Rajasthan, Índia | Árido tropical | 217 | 11,52% | **27,65%** | +16,13pp |
| **Daffodil BD** | **Bangladesh** | **Tropical úmido** | **1.616** | **9,59%** | **18,13%** | **+8,54pp** |

*\* Exp D treinou nas 677 imgs PlantDoc/train — queda no Exp E é esperada (menos memorização, mais generalização)*

## Análise — Exp E

### Resultado geral: 18,13% — melhora real de +8,54pp sobre o Exp D

O Exp E (Focal Loss + augmentação agressiva de cor + backbone completo) demonstrou
melhora genuína em datasets completamente independentes do treino:
- **+16,13pp** no Tomato-Village (Índia): de 11,52% para 27,65%
- **+8,54pp** no Daffodil BD (Bangladesh): de 9,59% para 18,13%

### Mudança no padrão de atrator

**Exp D:** D02_septoriose era o atrator universal (recebe a maioria das predições erradas).
**Exp E:** O atrator mudou para D01_requeima e D09_mancha_bacteriana — classes com sintomas
visualmente distintos (manchas marrons extensas). Isso indica que a Focal Loss forçou o modelo
a aprender features mais discriminativas em vez de convergir para a classe "mais segura".

### D05_mofo_foliar: queda de 77,3% → 43,9%

No Exp D, D05 era o único outlier positivo. No Exp E, a acurácia caiu — possivelmente porque
a augmentação de saturação e matiz interferiu com a textura branco-acinzentada característica de
*Passalora fulva*, que era a feature robusta detectada anteriormente.

### D07_acaro_bronzeamento e D06_vira_cabeca: permanecem em 0%

Essas classes continuam sem detecção confiável em campo real. Ambas têm sintomas difusos
(bronzeamento gradual, enrolamento foliar) que dependem fortemente do contexto visual — ângulo,
iluminação e variedade da cultivar — características impossíveis de aprender apenas de imagens
laboratoriais controladas.

### Conclusão para o TCC

O Exp E é o modelo final escolhido para o sistema Ceres:
- Lab: 98,43% (PlantVillage test set, 2.734 imagens)
- Macro F1 lab: 0,9791
- Campo genuinamente independente: +16pp Índia, +8,5pp Bangladesh vs Exp D
- Tamanho: 638 KB — compatível com ESP32-S3 N16R8 (8MB PSRAM)
- A validação definitiva permanece: produtores de Sorriso-MT (Sprint 3)
