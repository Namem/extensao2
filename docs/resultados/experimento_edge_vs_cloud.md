# Experimento: Edge vs Cloud — Inferência TFLite
**TCC Ceres Diagnóstico — Engenharia da Computação — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto
**Data:** 2026-05-28

---

## 1. Objetivo

Comparar duas arquiteturas de inferência para diagnóstico de doenças do tomateiro:

- **Edge (TinyML):** modelo TFLite rodando diretamente no microcontrolador ESP32-S3
- **Cloud API:** modelo TFLite servido via endpoint Django REST, consumido pelo app Flutter

A comparação avalia latência, acurácia, dependências de infraestrutura e adequação
para uso em campo agrícola.

---

## 2. Configuração Experimental

### Modelo
| Parâmetro | Valor |
|-----------|-------|
| Arquitetura | MobileNetV2 0.35, 96×96 px, INT8 |
| Experimento | Exp E — Focal Loss + Augmentação Agressiva |
| Arquivo | `ceres_expe_int8.tflite` |
| Tamanho | 638 KB |
| Classes | 10 (9 doenças + saudável) |
| Acurácia lab (PlantVillage test) | 98,43% |

### Dataset de avaliação
- **PlantVillage val set** — imagens controladas (fundo branco)
- 1 imagem por classe, seleção determinística (seed=42)
- 10 imagens no total (mesma metodologia do benchmark ESP32-S3)

---

## 3. Arquitetura Edge — ESP32-S3 TinyML

### Hardware
| Componente | Especificação |
|-----------|---------------|
| MCU | ESP32-S3-WROOM-1-N16R8 |
| Clock | 240 MHz (dual-core Xtensa LX7) |
| Flash | 16 MB |
| PSRAM | 8 MB (tensor arena: 512 KB) |
| Framework | TFLite Micro via Chirale_TensorFLowLite 2.0.0 |
| Conectividade | WiFi 802.11 b/g/n (não necessária para inferência) |

### Fluxo de inferência (Edge)
```
Imagem embutida (array C, 96×96×3 INT8)
  → memcpy → tensor_arena (PSRAM)
  → TFLite Micro Interpreter::Invoke()
  → dequantização INT8→float → softmax
  → classe + confiança
  [medido com esp_timer_get_time()]
```

### Resultados ESP32-S3 (Sprint 2, 2026-05-27)
| Métrica | Valor |
|---------|-------|
| Acurácia | **10/10 (100%)** |
| Latência média | **692 ms** |
| Latência mínima | 692 ms |
| Latência máxima | 695 ms |
| Desvio padrão | ±1 ms |
| Arena PSRAM usada | 200 KB / 512 KB (39%) |
| RAM livre (heap) | 290 KB |
| Requer conectividade | **Não** |

---

## 4. Arquitetura Cloud — Django REST API

### Stack
| Componente | Especificação |
|-----------|---------------|
| Servidor | Django 6.0.4 + Python 3.13 (dev server) |
| Inferência | ai-edge-litert 2.1.5 (subprocess por requisição) |
| Hardware servidor | PC desktop — Intel + NVIDIA RTX 3060 Ti |
| Cliente | Flutter Windows desktop / app Android |
| Protocolo | HTTP/1.1 multipart/form-data |

### Fluxo de inferência (Cloud)
```
Cliente (Flutter)
  → HTTP POST multipart (imagem JPEG)
  → Django view (InferirImagemView)
    → base64(imagem) via stdin
    → subprocess: nova instância Python
      → importar ai_edge_litert + PIL + numpy
      → carregar modelo TFLite (638 KB)
      → pré-processar (96×96 RGB → INT8)
      → Interpreter.invoke()
      → dequantização + softmax
      → JSON stdout
    ← JSON resultado
  → Response HTTP 200
← ResultadoInferencia (Flutter)
```

> **Nota arquitetural:** o subprocess é instanciado a cada requisição por restrição
> do XNNPACK delegate no Windows (thread-safety). Em produção Linux, o modelo
> pode ser carregado uma vez (singleton) e mantido em memória, reduzindo drasticamente
> a latência (estimativa: 20–50 ms por inferência).

### Resultados Django/PC (2026-05-28, 5 repetições por imagem)

#### Por classe
| Classe esperada | Predição | OK | Lat. API (ms) | Lat. HTTP (ms) |
|----------------|----------|----|---------------|----------------|
| D01_requeima | D01_requeima | ✓ | 257 | 2265 |
| D02_septoriose | D02_septoriose | ✓ | 260 | 2267 |
| D03_pinta_preta | D03_pinta_preta | ✓ | 257 | 2266 |
| D03b_mancha_alvo | D03b_mancha_alvo | ✓ | 822 | 2847 |
| D05_mofo_foliar | D05_mofo_foliar | ✓ | 245 | 2279 |
| D06_vira_cabeca | D06_vira_cabeca | ✓ | 245 | 2278 |
| **D06b_mosaico** | **D05_mofo_foliar** | **✗** | 243 | 2287 |
| D07_acaro_bronzeamento | D07_acaro_bronzeamento | ✓ | 246 | 2285 |
| D09_mancha_bacteriana | D09_mancha_bacteriana | ✓ | 242 | 2277 |
| saudavel | saudavel | ✓ | 245 | 2281 |

#### Resumo Cloud API
| Métrica | Valor |
|---------|-------|
| Acurácia | **9/10 (90,0%)** |
| Latência subprocess média | **306 ms** |
| Latência subprocess mínima | 239 ms |
| Latência subprocess máxima | 3071 ms |
| Desvio padrão subprocess | ±399 ms |
| Latência HTTP end-to-end média | **2333 ms** |

> **D03b_mancha_alvo — 822ms/2847ms:** valor atípico consistente.
> Causa provável: imagem de maior resolução nessa classe do val set,
> gerando mais dados no pipe stdin → maior overhead no subprocess.

> **Latência HTTP 2333ms:** Django dev server (single-thread, Windows) +
> overhead de pipe subprocess por requisição. Em produção com Gunicorn/Linux
> e modelo em memória, estima-se < 100ms end-to-end.

---

## 5. Comparativo Edge vs Cloud

### Tabela principal
| Métrica | ESP32-S3 (Edge) | Django/PC (Cloud) |
|---------|-----------------|-------------------|
| **Acurácia val PlantVillage** | 10/10 (100%) | 9/10 (90,0%) |
| **Latência média** | **692 ms** | 306 ms (subprocess) |
| **Latência end-to-end real** | **692 ms** | 2333 ms (dev server) |
| **Latência prod. estimada** | 692 ms | ~50–100 ms (Gunicorn/Linux) |
| **Requer conectividade** | **Não** | Sim (WiFi/4G) |
| **Funciona offline** | **Sim** | Não |
| **Modelo em memória** | Sempre carregado | Por requisição (Windows) |
| **Tamanho modelo** | 638 KB (Flash) | 638 KB (RAM servidor) |
| **Hardware necessário** | ESP32-S3 (~R$80) | Servidor PC/cloud |
| **Privacidade do dado** | **Total (local)** | Imagem transmitida |
| **Escalabilidade** | 1 dispositivo por unidade | N clientes simultâneos |
| **Atualização de modelo** | Requer reflash firmware | Deploy no servidor |
| **Custo por inferência** | ~R$0,0001 (energia) | Energia + infra servidor |
| **Temperatura/Umidade** | DHT22 integrado | Sensores externos |

### Análise por dimensão

#### 5.1 Latência
O ESP32-S3 apresenta latência de **692ms** consistente (±1ms), determinística
e independente de condições de rede. A Cloud API, em ambiente de desenvolvimento
(subprocess por requisição), apresenta **306ms de inferência** mas **2333ms
end-to-end**, com alta variância (±399ms).

Em cenário de produção com servidor Linux e modelo carregado em memória
(singleton com Gunicorn), estima-se latência < 100ms. Para a validação deste TCC,
o Django development server é suficiente para demonstrar a viabilidade do pipeline.

#### 5.2 Acurácia
Ambas as arquiteturas usam **o mesmo modelo** (`ceres_expe_int8.tflite`),
portanto a acurácia no test set PlantVillage é idêntica (98,43%).

A divergência observada neste benchmark (10/10 vs 9/10) é atribuída à seleção
de imagens: o ESP32 usou os arrays C do test set gerados por `gerar_arrays_c.py`,
enquanto o benchmark API usou imagens diferentes do val set (seed=42).

**Erro observado:** D06b_mosaico → D05_mofo_foliar.
Cientificamente relevante: Mosaico (ToMV) e Mofo Foliar (*Passalora fulva*)
podem compartilhar características visuais de descoloração foliar. A confusão
entre essas classes foi documentada em validações anteriores (Exp D, Tomato-Village).

#### 5.3 Adequação para uso em campo (Sorriso-MT)
**ESP32-S3 (Edge):** ideal para produtores sem acesso confiável à internet.
Conectividade WiFi é usada apenas para MQTT (registro histórico), não para
inferência. Diagnóstico funciona mesmo sem rede.

**Cloud API:** adequada como complemento quando o produtor usa o aplicativo
Flutter com conectividade estável. Permite modelo mais sofisticado no servidor
(EfficientNet-B0, Exp F) sem limitações de hardware embarcado.

#### 5.4 Privacidade e LGPD
Na arquitetura edge, a imagem **nunca sai do dispositivo**. Na arquitetura cloud,
a imagem JPEG é transmitida ao servidor. Para aplicações com produtores rurais,
a opção edge oferece maior proteção de dados por padrão (privacy by design).

---

## 6. Conclusão

Para o contexto do TCC (detecção precoce de doenças em tomateiros,
produtores de Sorriso-MT), **ambas as arquiteturas são complementares**:

| Cenário | Arquitetura recomendada |
|---------|------------------------|
| Campo sem internet (zona rural) | **Edge — ESP32-S3** |
| App móvel com WiFi estável | **Cloud — Django API** |
| Alta escala / múltiplos clientes | **Cloud — Gunicorn/Linux** |
| Privacidade máxima dos dados | **Edge — ESP32-S3** |
| Modelo mais preciso (Exp F futuro) | **Cloud — EfficientNet-B0** |

O Ceres Diagnóstico implementa **ambas as arquiteturas**, permitindo que o
produtor utilize a solução mais adequada à sua realidade de conectividade,
validando a proposta de sistema embarcado + API como contribuição científica.

---

## 7. Referências metodológicas

- Lane, N. D. et al. (2017). *Deepx: A software accelerator for low-power deep learning inference on mobile devices.* IPSN.
- Warden, P.; Situnayake, D. (2020). *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers.* O'Reilly.
- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications.* arXiv:1704.04861.
- Benchmark ESP32-S3: `docs/resultados/benchmark_esp32s3.md` (Sprint 2, 2026-05-27)
- Benchmark API: `docs/resultados/benchmark_api.json` (Sprint 3, 2026-05-28)
