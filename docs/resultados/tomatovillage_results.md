# Avaliação Tomato-Village — Validação Independente em Campo Real

**Data:** 2026-05-09 21:38
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
| D01_requeima | Late_blight | 19 | 92 | 20.7% | D02_septoriose (31x) |
| D03_pinta_preta | Early_blight | 6 | 50 | 12.0% | D05_mofo_foliar (20x) |
| D06_vira_cabeca | Spotted Wilt Virus | 0 | 53 | 0.0% | D02_septoriose (26x) |
| saudavel | Healthy | 0 | 22 | 0.0% | D02_septoriose (16x) |

## Resultado Geral

| Métrica | Valor |
|---|---|
| **Acurácia geral** | **11.52%** |
| Total imagens | 217 |
| Erros de leitura | 0 |
| Splits | test |

## Comparativo com PlantDoc

| Dataset | Imgs | Modelo | Acurácia | Nota |
|---|---|---|---|---|
| PlantDoc (train+test) | 746 | Exp B | 20,24% | Linha base |
| PlantDoc (test only) | 69 | Exp D | 30,43% | Após fine-tuning |
| **Tomato-Village (test)** | **217** | **Exp D** | **11.52%** | **Validação independente** |

## Análise

### Padrão dominante: colapso para D02_septoriose

O modelo previu `D02_septoriose` como classe mais frequente em 3 das 4 classes avaliadas,
incluindo folhas **saudáveis** (16/22 = 73% rotuladas como septoriose).
Isso caracteriza **colapso de classe sob shift de domínio**: sob entradas
fora-de-distribuição, o modelo converge para a classe visualmente mais "genérica"
— septoriose exibe pequenas manchas escuras em fundo verde, padrão que se sobrepõe
a imperfeições naturais, poeira e textura de campo.

### Análise por classe

| Classe real | Top-2 predições erradas | Interpretação |
|---|---|---|
| D01_requeima (92 imgs) | septoriose (31), mofo (26) | Manchas escuras úmidas de requeima confundem com septoriose/mofo |
| D03_pinta_preta (50 imgs) | mofo (20), septoriose (17) | Lesões concêntricas de pinta preta absorvidas pelas mesmas classes |
| D06_vira_cabeca (53 imgs) | septoriose (26), mofo (16) | **Mapeamento incorreto**: TSWV (manchas necróticas+bronzeamento) ≠ TYLCV (folha enrolada+amarelada) |
| saudavel (22 imgs) | septoriose (16), requeima (2) | Folhas sãs indianas com iluminação de campo e variedades locais não reconhecidas como saudáveis |

### Mapeamento D06 biologicamente incorreto

O Ceres D06_vira_cabeca corresponde ao **TYLCV** (Tomato Yellow Leaf Curl Virus),
cujos sintomas são folhas enroladas para cima e amarelamento das margens.
O Tomato-Village "Spotted Wilt Virus" é o **TSWV** (Tomato Spotted Wilt Virus),
cujos sintomas são manchas necróticas anulares e bronzeamento.
São vírus diferentes, vetores diferentes (mosca-branca vs. tripes) e aparência visual
completamente distinta. O 0% nesta classe não indica falha do modelo nesta doença —
indica que o mapeamento de classes é inválido para este dataset.

### Gap geográfico vs. gap de fundo

A comparação com o PlantDoc revela dois componentes separados do gap lab-campo:

| Fator | PlantDoc | Tomato-Village |
|---|---|---|
| País/região | EUA, Europa (similar ao PV) | Rajasthan, Índia |
| Condições de campo | Moderadas | Forte sol tropical, variedades locais |
| Resultado Exp D | 30,43% | 11,52% |

O fine-tuning com PlantDoc (Exp D) melhorou o desempenho em PlantDoc (+10pp),
mas **não generalizou** para um dataset geográfico mais distante.
Isso é consistente com Barbedo (2019), que demonstra forte especificidade geográfica
em modelos treinados com PlantVillage.

### Implicações para o TCC

1. **Gap lab-campo é multifatorial**: fundo, iluminação, variedade geográfica, câmera.
   Resolver apenas o fundo (Exp C/D) é insuficiente para generalização global.
2. **Validação em condições brasileiras é essencial**: o resultado de Sprint 3
   com produtores de Sorriso-MT é a métrica mais relevante para este projeto,
   pois o sistema será operado no Centro-Oeste brasileiro.
3. **Resultado negativo tem valor científico**: confirma a literatura e delimita
   o escopo de aplicação do modelo atual (tomaticultura brasileira, não global).
4. **D06_vira_cabeca no campo**: classe nunca corretamente detectada em campo real
   em nenhum dos experimentos — requer investigação separada (TYLCV vs TSWV,
   mais dados de campo brasileiros com TYLCV confirmado).
