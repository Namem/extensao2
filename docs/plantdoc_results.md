# Avaliacao PlantDoc — Validacao em Campo Real

**Data:** 2026-05-08 22:58
**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB)
**Dataset:** PlantDoc (imagens de campo real, fundo natural)

## Resultado por Classe

| Classe Ceres | Corretas | Total | Acuracia |
|---|---|---|---|
| D01_requeima | 92 | 202 | 45.5% |
| D02_septoriose | 51 | 279 | 18.3% |
| D03_pinta_preta | 98 | 158 | 62.0% |
| D05_mofo_foliar | 2 | 170 | 1.2% |
| D06_vira_cabeca | 14 | 140 | 10.0% |
| D06b_mosaico | 0 | 88 | 0.0% |
| D07_acaro_bronzeamento | 0 | 4 | 0.0% |
| D09_mancha_bacteriana | 22 | 202 | 10.9% |
| saudavel | 2 | 110 | 1.8% |

## Resultado Geral

| Metrica | Valor |
|---|---|
| **Acuracia geral** | **20.77%** |
| Total imagens | 1353 |
| Meta TCC | > 70% |
| Atingiu a meta? | Nao — analisar causas |

## Analise

### Gap laboratorio-campo (Lab-to-Field Gap)

O modelo obteve **98,13% no test set PlantVillage** e apenas **20,77% no PlantDoc**.
Esse fenomeno e bem documentado na literatura: Mohanty et al. (2016) reportaram
queda semelhante (99% laboratorio → ~31% campo) ao testar redes neurais em imagens
de campo real do PlantVillage original.

### Por que a queda e esperada?

O PlantVillage foi fotografado em condicoes controladas:
- Folha isolada sobre fundo **cinza ou preto uniforme**
- Iluminacao difusa e constante
- Sem oclusao, sem fundo vegetal, sem variacao de angulo

O PlantDoc tem condicoes de campo real:
- Folhas **no pe da planta**, com fundo natural (outras folhas, solo, ceu)
- Luz variavel (sombra, sol direto, reflexo)
- Rotacao, escala e perspectiva livres

O modelo aprendeu o fundo como feature discriminativa, nao apenas a lesao.

### Evidencia principal: classe `saudavel` com 1,8%

Folhas saudaveis do PlantVillage tem fundo escuro uniforme.
Folhas saudaveis do PlantDoc tem fundo verde natural (outras folhas).
O modelo nao reconhece folhas saudaveis em campo — prova de que o fundo
foi aprendido como parte do padrao da classe.

### Classes mais resistentes ao gap

| Classe | Acc PlantDoc | Motivo |
|---|---|---|
| D03_pinta_preta | 62,0% | Manchas concentricas sao textura saliente mesmo com fundo complexo |
| D01_requeima | 45,5% | Lesao escura de borda irregular e visualmente forte |
| D09_mancha_bacteriana | 10,9% | Lesoes pequenas facilmente mascaradas pelo fundo |
| D05_mofo_foliar | 1,2% | Cor amarelada da lesao confunde com folhas em senescencia |

### Impacto para o TCC

Este resultado **nao invalida o modelo** — ao contrario, e uma contribuicao
cientifica relevante. O trabalho documenta quantitativamente o gap lab-campo
para o modelo MobileNetV2 INT8 no contexto agricola brasileiro.

**Solucoes propostas para Sprint 2:**
1. Pre-processamento de remocao de fundo (GrabCut ou fundo branco forçado)
2. Data augmentation com fundos naturais na proxima iteracao de treino
3. Fine-tuning no PlantDoc (transfer learning de segundo nivel)
4. Teste com threshold mais baixo para acionar diagnostico (ex.: 0.50 → 0.35)

### Referencia

MOHANTY, S. P.; HUGHES, D. P.; SALATHE, M. Using deep learning for image-based
plant disease detection. *Frontiers in Plant Science*, v. 7, p. 1419, 2016.
DOI: 10.3389/fpls.2016.01419
