# Avaliação Tomato-Village — Validação Independente em Campo Real

**Data:** 2026-05-12 09:05
**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB) — Exp D
**Dataset:** Tomato-Village (Rajasthan, Índia, 2022 — Girase et al., 2024)
**Splits avaliados:** test

## Mapeamento de Classes

| Classe Tomato-Village | Classe Ceres |
|---|---|
| Late_blight | D01_requeima |
| Early_blight | D03_pinta_preta |
| Spotted Wilt Virus | D06_vira_cabeca |
| Healthy | saudavel |

*Nota: 4 das 8 classes do dataset não têm correspondência direta no Ceres e foram ignoradas.*

## Resultado por Classe

| Classe Ceres | Pasta TV | Corretas | Total | Acurácia | Top predição errada |
|---|---|---|---|---|---|
| D01_requeima | Late_blight | 52 | 92 | 56.5% | D09_mancha_bacteriana (19x) |
| D03_pinta_preta | Early_blight | 4 | 50 | 8.0% | D01_requeima (27x) |
| D06_vira_cabeca | Spotted Wilt Virus | 3 | 53 | 5.7% | D01_requeima (29x) |
| saudavel | Healthy | 1 | 22 | 4.5% | D01_requeima (12x) |

## Resultado Geral

| Métrica | Valor |
|---|---|
| **Acurácia geral** | **27.65%** |
| Total imagens | 217 |
| Erros de leitura | 0 |
| Splits | test |

## Comparativo com PlantDoc

| Dataset | Imgs | Modelo | Acurácia | Nota |
|---|---|---|---|---|
| PlantDoc (train+test) | 746 | Exp B | 20,24% | Linha base |
| PlantDoc (test only) | 69 | Exp D | 30,43% | Após fine-tuning |
| **Tomato-Village (test)** | **217** | **Exp D** | **27.65%** | **Validação independente** |

## Análise

`[Preencher após ver os resultados]`
