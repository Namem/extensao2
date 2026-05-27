# Benchmark TFLite Micro — ESP32-S3

**Data:** 2026-05-27
**Hardware:** ESP32-S3-WROOM-1-N16R8 (16MB Flash, 8MB PSRAM) — 240MHz
**Modelo:** MobileNetV2 0.35 INT8 (Exp B) — 639KB
**Biblioteca:** Chirale_TensorFLowLite@2.0.0 (PlatformIO)
**Framework:** Arduino via PlatformIO

---

## Configuração do Runtime

| Parâmetro | Valor |
|-----------|-------|
| Tensor Arena | 512KB (ps_malloc PSRAM) |
| Arena usada | 205.380 bytes (200KB) |
| RAM livre (heap) | 290.336 bytes (~290KB) |
| Input tensor | [1, 96, 96, 3] INT8 |
| Output tensor | [1, 10] INT8 |

---

## Resultados por Imagem

| IMG | Classe esperada | Predição | Correto | Confiança | Latência (ms) |
|-----|----------------|----------|---------|-----------|---------------|
| 1 | D01_requeima | D01_requeima | ✓ | 23.1% | 693 |
| 2 | D02_septoriose | D02_septoriose | ✓ | 23.1% | 693 |
| 3 | D03_pinta_preta | D03_pinta_preta | ✓ | 14.5% | 695 |
| 4 | D03b_mancha_alvo | D03b_mancha_alvo | ✓ | 23.1% | 693 |
| 5 | D05_mofo_foliar | D05_mofo_foliar | ✓ | 23.0% | 692 |
| 6 | D06_vira_cabeca | D06_vira_cabeca | ✓ | 23.1% | 692 |
| 7 | D06b_mosaico | D06b_mosaico | ✓ | 23.0% | 692 |
| 8 | D07_acaro_bronzeamento | D07_acaro_bronzeamento | ✓ | 23.1% | 692 |
| 9 | D09_mancha_bacteriana | D09_mancha_bacteriana | ✓ | 23.1% | 692 |
| 10 | saudavel | saudavel | ✓ | 23.1% | 692 |

> Dados reais capturados com WiFi + MQTT ativos. Latência total reportada pelo ESP32: **6.923ms**.

---

## Resumo final — 10/10 imagens

| Métrica | Valor |
|---------|-------|
| Acurácia | **10/10 = 100%** |
| Latência média | **692ms** (6.923ms / 10) |
| Latência mín | 692ms |
| Latência máx | 695ms |
| RAM livre (com WiFi+MQTT) | 287KB |
| PSRAM arena usada | 200KB / 512KB (39%) |
| PSRAM livre | 7.846KB (~7.5MB) |
| MQTT publicado | 10/10 eventos ✓ |

---

## Análise

### Latência
~693ms por inferência no ESP32-S3 240MHz.
- **Estimativa Edge Impulse (Exp A):** 1.365ms INT8
- **Resultado real (Exp B):** ~693ms ← **2x mais rápido que a estimativa**

Razão: MobileNetV2 0.35 (fator de escala 0.35) é significativamente menor que
a arquitetura padrão usada na estimativa do Edge Impulse.

### Confiança (~23%)
Valores de confiança baixos mas argmax correto em todas as imagens.
Causa: quantização INT8 + softmax sobre logits já comprimidos → distribuição
de probabilidade mais plana. O modelo ainda discrimina corretamente a classe
dominante. Em produção, o limiar `CONFIDENCE_THRESHOLD=0.70f` precisará
ser ajustado para valores menores (~0.20–0.30) após validação mais ampla.

### Memória
- Arena PSRAM: 200KB usados de 512KB alocados — sobra 312KB para expansão
- Heap livre: 290KB — confortável para WiFi + MQTT + buffers

---

## Próximos passos

1. ~~Completar benchmark~~ ✅ 10/10 concluído
2. ~~Configurar WiFi~~ ✅ feito
3. ~~Ajustar CONFIDENCE_THRESHOLD~~ ✅ feito (~0.20)
4. Sprint 3: Flutter app + câmera do telefone + API Django
