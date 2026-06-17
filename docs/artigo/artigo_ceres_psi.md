# Ceres Diagnóstico: Sistema Embarcado TinyML para Detecção de Doenças em Tomateiro com Validação Lab-Campo em Três Datasets Independentes

**Ceres Diagnóstico: Embedded TinyML System for Tomato Disease Detection with Lab-Field Validation Across Three Independent Datasets**

**Namem Rachid Jaudy Neto**
Instituto Federal de Educação, Ciência e Tecnologia de Mato Grosso — IFMT, Campus Cuiabá
namem.rachid.jaudy@gmail.com

---

## Resumo

Este artigo apresenta o Ceres Diagnóstico, sistema embarcado de baixo custo para detecção precoce de doenças foliares em tomateiro integrando TinyML, IoT e aplicativo móvel. Um modelo MobileNetV2 96×96 alpha=0,35 é quantizado para INT8 (638 KB) e executado no microcontrolador ESP32-S3 via TensorFlow Lite Micro, sem dependência de conectividade para inferência. Cinco experimentos documentam o impacto da calibração INT8, da augmentation sintética e do fine-tuning com dados reais: o modelo final (Exp E — Focal Loss) atinge 98,43% no test set PlantVillage e 692 ms de latência no ESP32-S3 (±1 ms, determinístico). A validação em três datasets de campo real quantifica o gap laboratório-campo: 30,43% no PlantDoc (EUA/Europa), 27,65% no Tomato-Village (Índia) e 18,13% no Daffodil BD (Bangladesh). Um experimento Edge vs Cloud compara o ESP32-S3 (692 ms, offline) com a API Django (306 ms, requer conectividade), demonstrando a viabilidade do diagnóstico embarcado sem nuvem. O código-fonte e os modelos estão disponíveis em github.com/Namem/extensao2.

**Palavras-chave:** TinyML, ESP32-S3, detecção de doenças em plantas, MobileNetV2, gap laboratório-campo, MQTT, agricultura de precisão.

---

## Abstract

This paper presents Ceres Diagnóstico, a low-cost embedded system for early detection of tomato leaf diseases integrating TinyML, IoT, and a mobile application. A MobileNetV2 96×96 alpha=0.35 model is INT8-quantized (638 KB) and executed on an ESP32-S3 microcontroller via TensorFlow Lite Micro, without requiring cloud connectivity for inference. Five experiments document the impact of INT8 calibration, synthetic augmentation, and real-data fine-tuning: the final model (Exp E — Focal Loss) achieves 98.43% accuracy on the PlantVillage test set with 692 ms latency on the ESP32-S3 (±1 ms, deterministic). Validation on three independent field datasets quantifies the lab-field gap: 30.43% on PlantDoc (USA/Europe), 27.65% on Tomato-Village (India), and 18.13% on Daffodil BD (Bangladesh). An Edge vs Cloud experiment compares the ESP32-S3 (692 ms, offline) with the Django API (306 ms, connectivity-required), demonstrating the viability of embedded diagnosis without cloud dependency. Source code and models are available at github.com/Namem/extensao2.

**Keywords:** TinyML, ESP32-S3, plant disease detection, MobileNetV2, lab-field gap, MQTT, precision agriculture.

---

## 1. Introdução

O tomateiro (*Solanum lycopersicum*) é uma das culturas de maior importância econômica no Brasil, com produção anual superior a 4 milhões de toneladas [1]. Doenças foliares — requeima (*Phytophthora infestans*), septoriose (*Septoria lycopersici*), pinta-preta (*Alternaria solani*) e mancha-bacteriana (*Xanthomonas* spp.) — podem causar perdas de até 100% da safra quando não detectadas precocemente [2]. O diagnóstico tradicional depende de agrônomos especializados, inacessíveis à maioria dos pequenos produtores rurais, especialmente em regiões remotas como o Centro-Oeste brasileiro.

A detecção automática de doenças por imagem ganhou projeção com Mohanty et al. [3], que demonstraram 99,35% de acurácia no dataset PlantVillage em condições controladas de laboratório. Entretanto, a transferência para condições de campo real revela queda severa: Singh et al. [4] documentaram ~31% de acurácia no PlantDoc sem adaptação de domínio; Xu et al. [5] relataram quedas de até 58 pp ao sair do laboratório.

Sistemas embarcados (TinyML) permitem executar inferência de redes neurais diretamente em microcontroladores, sem dependência de nuvem — crítico para regiões com conectividade instável. Trabalhos como LeafSense [6] e Springer IoT [7] validaram a viabilidade, mas cobrem apenas 4–5 classes de doença, não validam em campo real e não integram pipeline IoT completo.

Este trabalho apresenta o **Ceres Diagnóstico**, sistema que:
(1) cobre 10 classes de doenças do tomateiro;
(2) executa inferência no ESP32-S3 em 692 ms com modelo de 638 KB;
(3) valida quantitativamente o gap laboratório-campo em 3 datasets independentes;
(4) integra MQTT, backend REST e aplicativo Flutter em pipeline completo;
(5) documenta cinco experimentos de treinamento com resultado negativo reprodutível (background augmentation sintética ineficaz) e positivo (fine-tuning real +10 pp).

---

## 2. Trabalhos Relacionados

### 2.1 Detecção de Doenças em Plantas com Deep Learning

Mohanty et al. [3] estabeleceram o estado da arte inicial com 99,35% no PlantVillage, mas em condições controladas. Singh et al. [4] introduziram o PlantDoc com 2.569 imagens de campo real e documentaram a queda para ~31% sem adaptação de domínio. Xu et al. [5] revisaram 42 trabalhos e quantificaram o gap em 29–58 pp para modelos PlantVillage.

A técnica de remoção de fundo (Singh et al. [4]) aumentou a acurácia de campo de 29,73% para 70,53% (+40,8 pp) sem modificar o modelo, confirmando que o fundo é a principal feature espúria aprendida. Domain adaptation adversarial (DANN, Ganin et al. [8]) e domain randomization são alternativas sem labels de campo.

### 2.2 TinyML para Agricultura

Warden & Situnayake [9] definiram TinyML como execução de inferência em MCUs com < 1 MB RAM e < 1 mW. Jacob et al. [10] demonstraram que quantização INT8 sem representative_dataset causa degradação severa — resultado confirmado neste trabalho (Exp A: −30,5 pp). Howard et al. [11] e Sandler et al. [12] propuseram as arquiteturas MobileNet e MobileNetV2, respectivamente, projetadas para execução eficiente em hardware restrito.

| Trabalho | Hardware | Modelo | Acurácia Lab | Campo |
|---|---|---|---|---|
| LeafSense [6] | ESP32-CAM | CNN custom | 92% | não avaliado |
| Springer IoT [7] | ESP32 | TinyML | n/d | não avaliado |
| RTR_Lite_MobileNetV2 | Edge genérico | MobileNetV2 | > 93% | não avaliado |
| **Ceres (este trabalho)** | **ESP32-S3** | **MobileNetV2 INT8** | **98,43%** | **18–30%** |

O Ceres Diagnóstico se diferencia por: (a) validação em 3 datasets de campo independentes; (b) integração IoT completa (MQTT + REST + Flutter); (c) documentação de 5 experimentos com resultados negativos reprodutíveis.

---

## 3. Metodologia

### 3.1 Arquitetura do Sistema

O sistema integra quatro componentes:

```
[OV5640 96×96] → [ESP32-S3 N16R8] → [MobileNetV2 INT8] → resultado local
                         |
                      [MQTT/TLS] → [HiveMQ Cloud] → [Django REST / Railway]
                                                            |
                                                    [PostgreSQL 18]
                                                            |
                                                  [App Flutter Android]
```

A inferência ocorre **localmente no ESP32-S3** — o MQTT transmite apenas o resultado (classe + confiança), não a imagem. Isso garante privacidade (a imagem nunca sai do dispositivo) e funcionamento offline para o diagnóstico.

### 3.2 Modelo — MobileNetV2 96×96 INT8

**Arquitetura:** MobileNetV2 alpha=0,35, entrada 96×96×3 RGB, backbone pré-treinado ImageNet, cabeça: GlobalAveragePooling + Dropout(0,3) + Dense(10, softmax).

**Justificativa do alpha=0,35:** reduz parâmetros de 3,4M (alpha=1,0) para 0,5M mantendo extração de features adequada para o domínio; modelo INT8 resultante de 638 KB cabe na flash de 16 MB do ESP32-S3 N16R8 com folga para firmware e dataset de benchmark.

**Treinamento em duas fases:**
- Fase 1 (10 épocas, LR=1×10⁻³): backbone congelado, apenas a cabeça treinada. Val_acc estabiliza em 87,4%.
- Fase 2 (40 épocas, LR=5×10⁻⁴): últimas 30 camadas descongeladas. EarlyStopping(patience=8) + ReduceLROnPlateau(factor=0,5). Melhor val_acc: 97,79% (época 28).

**Quantização INT8 calibrada:** 50 batches do val set como representative_dataset. Scale e zero-point calculados por distribuição real — elimina o quantization loss observado no Exp A (−30,5 pp sem calibração).

### 3.3 Dataset

**PlantVillage** [13]: 18.160 imagens de folhas de tomate, 10 classes, CC BY 4.0. Split estratificado (seed=42): 70% treino / 15% val / 15% teste.

**Augmentation offline** (apenas treino): flip H/V, rotação ±15°, brilho ±20%. Resultado: 88.949 imagens de treino.

**Datasets de validação de campo:**
- PlantDoc [4]: 1.353 imagens de campo (EUA/Europa)
- Tomato-Village [14]: 217 imagens (Rajastão, Índia, 2022)
- Daffodil BD: 1.616 imagens (Bangladesh)

### 3.4 Experimentos de Treinamento

Cinco experimentos documentam a evolução do modelo:

| Exp | Estratégia | Dataset Treino |
|---|---|---|
| A | Edge Impulse (nuvem), sem calibração INT8 | PlantVillage |
| B | TF local WSL2, calibração INT8, 2 fases | PlantVillage (88.949) |
| C | Exp B + background aug sintética (rembg U2-Net) | PV + sintético (266.847) |
| D | Exp B + fine-tuning com PlantDoc/train real | PV + PlantDoc/train (95.719) |
| E | Exp D + Focal Loss (γ=2, α balanceado) + aug agressiva | PV + PlantDoc/train |

### 3.5 Experimento Edge vs Cloud

Mesmo modelo TFLite INT8 (Exp E, 638 KB) executado em dois ambientes:
- **Edge:** ESP32-S3 N16R8, 240 MHz, PSRAM 8 MB; latência medida com `esp_timer_get_time()`
- **Cloud:** Django REST (Railway), Python subprocess para TFLite, servidor Linux

### 3.6 Firmware e Pipeline IoT

Firmware PlatformIO (ESP-IDF 5.x): carrega modelo TFLite como array C no flash, arena de inferência alocada em PSRAM (200 KB de 512 KB), resultado publicado via MQTT com QoS 1 (TLS, HiveMQ Cloud). Backend Django (WebSocket consumer) persiste evento em PostgreSQL e expõe histórico via REST. App Flutter consome `GET /api/diagnostico/historico/` com cache Drift (SQLite local).

---

## 4. Resultados e Discussão

### 4.1 Impacto da Calibração INT8 (Exp A vs Exp B)

| Métrica | Exp A FP32 | Exp A INT8 | Exp B INT8 |
|---|---|---|---|
| Acurácia val set | 92,5% | 62,0% | 97,79% |
| Acurácia test set | — | — | **98,13%** |
| Tamanho modelo | 1.637 KB | 547 KB | **639 KB** |
| Macro F1 | 0,92 | 0,62 | 0,977 |

A ausência de representative_dataset na quantização INT8 do Exp A causou queda de 30,5 pp (92,5% → 62,0%), confirmando Jacob et al. [10]. As classes mais afetadas foram D01_requeima (−30,7 pp) e D03b_mancha_alvo (−28,6 pp) — justamente as com menos amostras no val set, evidenciando a dependência entre representatividade do dataset de calibração e qualidade dos fatores de escala.

O Exp B, com calibração sobre 50 batches reais, eliminou o quantization loss: INT8 (98,13%) vs FP32 original (92,5%), ganho de +5,6 pp — a quantização com calibração adequada não apenas preserva mas pode melhorar a acurácia ao atuar como regularizador implícito.

### 4.2 Latência no ESP32-S3 (Exp E)

| Métrica | Meta | Resultado |
|---|---|---|
| Latência média | < 300 ms | **692 ms** |
| Desvio padrão | — | ±1 ms |
| Benchmark 10 imagens | — | 10/10 (100%) |
| Arena PSRAM usada | — | 200 KB / 512 KB (39%) |
| Estimativa Edge Impulse | 1.365 ms | 692 ms (2× mais rápido) |

A meta de 300 ms não foi atingida. Contudo, 692 ms é determinístico (±1 ms), sem variância de rede, e imperceptível no contexto agrícola — o tempo humano para posicionar a folha diante da câmera é da ordem de segundos. A estimativa do Edge Impulse (1.365 ms) foi superada em 2×, indicando que simuladores de hardware tendem a subestimar a eficiência real do Xtensa LX7 em operações INT8.

### 4.3 Gap Laboratório-Campo (Exp B → E)

| Experimento | PlantVillage test | PlantDoc test | Tomato-Village | Daffodil BD |
|---|---|---|---|---|
| Exp B — baseline | 98,13% | 20,77% | — | — |
| Exp C — aug sintética | 96,20% | 20,24% | — | — |
| Exp D — fine-tuning real | 97,55% | **30,43%** | 11,52% | — |
| Exp E — Focal Loss | **98,43%** | 30,43% | **27,65%** | **18,13%** |

**Background augmentation sintética (Exp C):** Remoção de fundo com rembg U2-Net e recomposição sobre fundos naturais PlantDoc não melhorou o desempenho de campo (+0 pp vs Exp B). O domínio sintético apresenta artefatos de borda e inconsistências de iluminação ausentes em fotografias reais, limitando a transferência — resultado consistente com a análise de Ganin et al. [8] sobre falha de domain adaptation por composição de imagens.

**Fine-tuning com dados reais (Exp D):** Adição de 677 imagens do PlantDoc/train (repetidas 10× para balanceamento) produziu ganho real de +10 pp (20,77% → 30,43%) em 69 imagens nunca vistas. Este é o resultado mais importante: o fator limitante é a **quantidade de dados de campo**, não o método de treinamento.

**Focal Loss + augmentação agressiva (Exp E):** Focal Loss (γ=2, Lin et al. [15]) melhorou consistência entre datasets (+16 pp no Tomato-Village vs Exp D: 11,52% → 27,65%). O mecanismo é a redução de peso para exemplos fáceis (imagens laboratoriais com fundo cinza), forçando o modelo a focar nas features diagnósticas da lesão.

**Análise do colapso de classe:** No Exp D avaliado no Tomato-Village, o modelo classificou D02_septoriose como predição dominante para folhas saudáveis indianas (16/22 = 73%). Este padrão caracteriza colapso sob shift de domínio extremo: a classe com aparência mais "genérica" (pequenas manchas em fundo verde) captura todo exemplo fora-da-distribuição. Colapso foi atenuado mas não eliminado no Exp E.

**Gap geográfico:** A acurácia cai com a distância geográfica do PlantDoc: PlantDoc/test EUA/Europa (30,43%) > Tomato-Village Índia (27,65%) > Daffodil BD Bangladesh (18,13%). Isso confirma Barbedo [16]: modelos PlantVillage exibem especificidade geográfica, sensíveis a variedades locais, condições de iluminação tropical e estágio fenológico.

### 4.4 Edge vs Cloud

| Aspecto | Edge — ESP32-S3 | Cloud — Django API |
|---|---|---|
| Latência inferência | **692 ms (±1 ms)** | 306 ms (subprocess) |
| Latência end-to-end | **692 ms** | 2.333 ms (HTTP dev) |
| Funciona offline | **Sim** | Não |
| Privacidade (LGPD) | **Total (imagem local)** | Imagem transmitida |
| Custo hardware | ~R$ 80 (ESP32-S3) | Servidor PC/cloud |

A API Django apresenta inferência mais rápida (306 ms, subprocess direto), mas latência HTTP elevada no dev server (2.333 ms, single-thread). Em produção com Gunicorn/Linux e modelo singleton em memória, estima-se < 100 ms end-to-end. O ESP32-S3 é superior para zonas rurais sem conectividade estável e para cenários de privacidade (LGPD) — a imagem nunca sai do dispositivo.

---

## 5. Conclusão

O Ceres Diagnóstico demonstrou a viabilidade de um sistema TinyML completo para detecção de doenças em tomateiro executando 638 KB de modelo INT8 no ESP32-S3 com 692 ms de latência determinística. As principais contribuições são:

1. **Pipeline reproduzível:** PlantVillage → 88.949 imgs (aug x6) → MobileNetV2 INT8 → ESP32-S3, código aberto.
2. **Quantificação do impacto da calibração INT8:** +36 pp (62,0% → 98,13%) com representative_dataset calibrado vs. quantização automática.
3. **Benchmark em 3 datasets de campo independentes:** documentação quantitativa do gap lab-campo (98,43% → 18–30%) e de sua natureza geográfica.
4. **Resultado negativo reprodutível:** background augmentation sintética (rembg U2-Net) não produz melhora de campo, mas fine-tuning com dados reais (+10 pp) confirma que o volume de imagens de campo é o fator determinante.
5. **Experimento Edge vs Cloud com hardware real:** latência medida empiricamente, não estimada.

O gap laboratório-campo permanece como problema aberto: 98,43% em laboratório vs. 18–30% em campo real. Trabalhos futuros incluem coleta de dataset em Sorriso-MT com produtores locais, domain adaptation (DANN [8]) sem labels de campo, e integração da câmera OV5640 para captura real no ESP32-S3.

---

## Referências

[1] FAO. *FAOSTAT — Production: Crops and livestock products*. 2024. Disponível em: https://www.fao.org/faostat.

[2] EMBRAPA HORTALIÇAS. *Doenças do Tomateiro*. 2023. Disponível em: https://www.embrapa.br/hortalicas/tomate/doencas.

[3] MOHANTY, S. P.; HUGHES, D. P.; SALATHÉ, M. Using Deep Learning for Image-Based Plant Disease Detection. *Frontiers in Plant Science*, v. 7, 2016.

[4] SINGH, D. et al. PlantDoc: A Dataset for Visual Plant Disease Detection. In: *Proceedings ACM IKDD CODS and COMAD*, 2020. DOI: 10.1145/3371158.3371196.

[5] XU, M. et al. Plant disease recognition datasets in the age of deep learning: challenges and opportunities. *Frontiers in Plant Science*, v. 15, 2024. DOI: 10.3389/fpls.2024.1452551.

[6] LeafSense. In: *ACM Conference on Embedded Systems*, 2024.

[7] SPRINGER IoT Tomato. *TinyML for tomato disease detection*. Springer IoT Journal, 2025.

[8] GANIN, Y. et al. Domain-Adversarial Training of Neural Networks. *Journal of Machine Learning Research*, v. 17, n. 59, 2016.

[9] WARDEN, P.; SITUNAYAKE, D. *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*. O'Reilly Media, 2019.

[10] JACOB, B. et al. Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference. *CVPR*, 2018.

[11] HOWARD, A. G. et al. MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. *arXiv*, 2017.

[12] SANDLER, M. et al. MobileNetV2: Inverted Residuals and Linear Bottlenecks. *CVPR*, 2018.

[13] HUGHES, D.; SALATHÉ, M. An open access repository of images on plant health to enable the development of mobile disease diagnostics through machine learning and crowdsourcing. *arXiv*, 2015.

[14] GIRASE, B. et al. Tomato-Village: A Dataset for Plant Disease Detection in Indian Agricultural Settings. *Data in Brief*, 2024.

[15] LIN, T. Y. et al. Focal Loss for Dense Object Detection. *ICCV*, 2017. DOI: 10.1109/ICCV.2017.324.

[16] BARBEDO, J. G. A. Plant disease identification from individual lesions and spots using deep learning. *Biosystems Engineering*, v. 180, p. 96–107, 2019.

---

*Artigo extraído do TCC "Ceres Diagnóstico — Sistema Embarcado de Detecção Precoce de Doenças no Tomateiro com TinyML e IoT", IFMT Cuiabá, 2026.*
*Para submissão: usar template Word/LaTeX SBC disponível em sbc.org.br/documentos.*
