# CERES DIAGNÓSTICO: SISTEMA EMBARCADO DE DETECÇÃO PRECOCE DE DOENÇAS NO TOMATEIRO COM TINYML E IoT

**Trabalho de Conclusão de Curso**
**Engenharia da Computação — IFMT Campus Sorriso-MT**
**Autor:** Namem Rachid Jaudy Neto
**Orientador:** (a preencher)
**Ano:** 2026

---

> **INSTRUÇÃO DE USO DESTE ARQUIVO**
> Este documento é o rascunho vivo do TCC. Ao final de cada implementação,
> o Claude Code atualiza as seções correspondentes com o que foi feito,
> resultados obtidos e referências. Ao final do projeto, este arquivo
> serve de base para o documento final em Word/LaTeX (ABNT).
> Seções marcadas com `[PENDENTE]` serão preenchidas nas sprints futuras.

---

## RESUMO

O tomateiro (*Solanum lycopersicum*) é uma das culturas de maior importância
econômica no Brasil, com produção anual superior a 4 milhões de toneladas.
Doenças foliares como requeima (*Phytophthora infestans*), septoriose
(*Septoria lycopersici*) e mancha-bacteriana (*Xanthomonas* spp.) podem causar
perdas de até 100% da safra quando não detectadas precocemente. O diagnóstico
tradicional depende de agrônomos especializados, inacessíveis à maioria dos
pequenos produtores rurais brasileiros.

Este trabalho propõe o **Ceres Diagnóstico**, um sistema embarcado de baixo
custo para detecção precoce de doenças em folhas de tomateiro. O sistema
integra um microcontrolador ESP32-S3 com câmera OV5640, executando um modelo
de visão computacional MobileNetV2 quantizado (INT8) via TensorFlow Lite Micro
diretamente no dispositivo (*TinyML*), sem necessidade de conexão com servidor
de nuvem para inferência. Os resultados são transmitidos via protocolo MQTT
para um backend Django REST, acessível por aplicativo Flutter para Android/iOS.

O modelo foi treinado com o dataset PlantVillage (Hughes & Salathé, 2015),
contendo 18.160 imagens de folhas de tomate em 10 classes de doenças.
`[PENDENTE: acurácia final, latência medida, resultados do experimento edge vs cloud]`

**Palavras-chave:** TinyML, ESP32-S3, detecção de doenças em plantas,
MobileNetV2, MQTT, Django REST, Flutter, agricultura de precisão.

---

## ABSTRACT

`[PENDENTE: tradução do resumo após versão final]`

---

## LISTA DE FIGURAS

`[PENDENTE: gerada ao final do projeto]`

---

## LISTA DE TABELAS

`[PENDENTE: gerada ao final do projeto]`

---

## LISTA DE ABREVIATURAS

| Sigla | Significado |
|-------|-------------|
| API | Application Programming Interface |
| CNN | Convolutional Neural Network |
| DRF | Django REST Framework |
| ESP32-S3 | Espressif Systems ESP32-S3 Microcontroller |
| FP32 | Floating Point 32-bit |
| INT8 | Integer 8-bit (quantização) |
| IoT | Internet of Things |
| JWT | JSON Web Token |
| MCU | Microcontroller Unit |
| MQTT | Message Queuing Telemetry Transport |
| PSRAM | Pseudo-Static Random Access Memory |
| QoS | Quality of Service |
| REST | Representational State Transfer |
| SQLite | Serverless SQL Database Engine |
| TCC | Trabalho de Conclusão de Curso |
| TFLite | TensorFlow Lite |
| TinyML | Tiny Machine Learning |

---

## SUMÁRIO

1. Introdução
2. Referencial Teórico
   2.1 Doenças do Tomateiro e Impacto Econômico
   2.2 Visão Computacional para Diagnóstico Fitossanitário
   2.3 TinyML e Inferência na Borda
   2.4 Protocolos IoT para Agricultura de Precisão
   2.5 Trabalhos Relacionados
3. Metodologia
   3.1 Arquitetura Geral do Sistema
   3.2 Dataset e Pré-processamento
   3.3 Treinamento do Modelo
   3.4 Firmware ESP32-S3
   3.5 Backend Django REST
   3.6 Aplicativo Flutter
4. Desenvolvimento e Implementação
   4.1 Sprint 0 — Motor de Diagnóstico
   4.2 Sprint 1 — MQTT + Dataset + Treino
   4.3 Sprint 2 — Deploy TFLite no ESP32-S3
   4.4 Sprint 3 — Flutter + Experimentos
5. Resultados e Discussão
   5.1 Acurácia do Modelo
   5.2 Latência de Inferência
   5.3 Experimento Edge vs Cloud
   5.4 Avaliação em Campo (PlantDoc)
6. Conclusão
7. Referências

---

## 1. INTRODUÇÃO

### 1.1 Contextualização

O Brasil é o nono maior produtor mundial de tomate, com produção de
aproximadamente 4,4 milhões de toneladas em 2023 (FAO, 2024). O estado
de Mato Grosso, onde está localizado o IFMT Campus Sorriso, apresenta
expansão crescente da tomaticultura, impulsionada pela fronteira agrícola
do Cerrado. Contudo, o manejo fitossanitário ainda é majoritariamente
reativo: o produtor detecta a doença visualmente após o aparecimento de
sintomas severos, quando a perda já é significativa.

A detecção precoce de doenças foliares é fundamental para reduzir o uso
de agrotóxicos, diminuir perdas e aumentar a rentabilidade da cultura.
Sistemas automatizados de diagnóstico, baseados em visão computacional,
têm demonstrado resultados promissores na literatura científica, com
acurácias superiores a 90% em datasets controlados (MOHANTY et al., 2016).

O desafio para o pequeno produtor rural brasileiro não é apenas técnico,
mas também econômico e de conectividade: soluções baseadas em nuvem
requerem internet estável (indisponível em lavouras remotas) e custos
recorrentes de servidor. O paradigma **TinyML** — execução de modelos de
aprendizado de máquina diretamente em microcontroladores de baixo custo —
surge como alternativa viável para este contexto.

### 1.2 Problema

Como detectar precocemente doenças foliares no tomateiro de forma
automatizada, de baixo custo e funcionando offline, acessível ao pequeno
produtor rural do Centro-Oeste brasileiro?

### 1.3 Hipótese

Um sistema embarcado baseado em ESP32-S3 com modelo MobileNetV2 quantizado
(TinyML) é capaz de classificar doenças foliares do tomateiro com acurácia
superior a 85%, latência inferior a 300ms e custo de hardware inferior a
R$ 200,00, viabilizando o diagnóstico em tempo real sem conectividade.

### 1.4 Objetivos

**Objetivo Geral:**
Desenvolver e validar um sistema embarcado de detecção precoce de doenças
em folhas de tomateiro integrando TinyML, IoT e aplicativo mobile.

**Objetivos Específicos:**
1. Preparar e aumentar o dataset PlantVillage com 10 classes de doenças do tomateiro
2. Treinar modelo MobileNetV2 INT8 via Edge Impulse com acurácia > 85%
3. Implantar o modelo no ESP32-S3 com latência < 300ms e RAM livre > 4MB
4. Desenvolver backend Django REST com persistência de eventos via MQTT
5. Desenvolver aplicativo Flutter com funcionamento offline e histórico paginado
6. Comparar experimentalmente inferência edge vs cloud em latência e disponibilidade

### 1.5 Justificativa

O projeto endereça três lacunas simultâneas:
- **Tecnológica:** integração de TinyML + IoT + mobile em sistema único de baixo custo
- **Agrícola:** cobertura das 10 principais doenças do tomateiro mapeadas pela Embrapa
- **Social:** ferramenta acessível ao pequeno produtor, sem dependência de internet

### 1.6 Estrutura do Trabalho

Este trabalho está organizado em 6 capítulos. O Capítulo 2 apresenta o
referencial teórico. O Capítulo 3 descreve a metodologia. O Capítulo 4
detalha o desenvolvimento por sprint. O Capítulo 5 apresenta e discute
os resultados. O Capítulo 6 conclui e aponta trabalhos futuros.

---

## 2. REFERENCIAL TEÓRICO

### 2.1 Doenças do Tomateiro e Impacto Econômico

O tomateiro é acometido por diversas doenças foliares de origem fúngica,
bacteriana e viral. As 10 principais doenças monitoradas pelo Ceres,
com base no mapeamento da Embrapa Hortaliças, são:

| Código | Doença | Agente Causador | Tipo |
|--------|--------|-----------------|------|
| D1 | Requeima | *Phytophthora infestans* | Oomiceto |
| D2 | Septoriose | *Septoria lycopersici* | Fungo |
| D3 | Pinta-Preta | *Alternaria solani* | Fungo |
| D4 | Traça-do-Tomateiro | *Tuta absoluta* | Inseto |
| D5 | Mosca-Branca | *Bemisia tabaci* | Inseto |
| D6 | Tripes/Vira-Cabeça | *Frankliniella* + Tospovírus | Inseto + Vírus |
| D7 | Ácaro-do-Bronzeamento | *Aculops lycopersici* | Ácaro |
| D8 | Murcha-Bacteriana | *Ralstonia solanacearum* | Bactéria |
| D9 | Mancha-Bacteriana | *Xanthomonas* spp. | Bactéria |
| D10 | Broca-Pequena | *Neoleucinodes elegantalis* | Inseto |

`[PENDENTE: dados de perda econômica por doença — pesquisar IBGE/Embrapa]`

### 2.2 Visão Computacional para Diagnóstico Fitossanitário

O uso de redes neurais convolucionais (CNNs) para classificação de doenças
em plantas foi popularizado por Mohanty et al. (2016), que demonstraram
acurácia de 99,35% usando AlexNet e GoogLeNet sobre o PlantVillage em
condições laboratoriais. Entretanto, estudos subsequentes com imagens de
campo real (Thapa et al., 2020 — PlantDoc) mostraram queda significativa
na acurácia, evidenciando o gap laboratório-campo.

Arquiteturas leves como MobileNet foram propostas por Howard et al. (2017)
para execução em dispositivos móveis, com redução de parâmetros de 138M
(VGG16) para 4.2M sem perda crítica de acurácia. A versão MobileNetV2
(Sandler et al., 2018) introduziu os blocos *inverted residual* com
*linear bottleneck*, melhorando a eficiência computacional.

`[PENDENTE: adicionar resultados próprios após treinamento]`

### 2.3 TinyML e Inferência na Borda

TinyML refere-se à execução de modelos de machine learning em
microcontroladores com restrições severas de memória (< 1MB RAM) e
energia (< 1mW). Warden & Situnayake (2019) definiram o campo como
a intersecção entre embedded systems e machine learning.

A **quantização INT8** é a técnica central que viabiliza TinyML: converte
pesos de FP32 (4 bytes/peso) para INT8 (1 byte/peso), reduzindo o tamanho
do modelo em ~4x e a latência em ~2-4x em MCUs com suporte SIMD, como o
ESP32-S3 (Xtensa LX7).

O **TensorFlow Lite Micro** (Google, 2019) é o runtime de inferência para
microcontroladores, sem dependência de sistema operacional, heap dinâmico
ou bibliotecas padrão completas.

**Edge Impulse** (2019) é a plataforma líder para desenvolvimento de
modelos TinyML com exportação direta para firmware Arduino/PlatformIO,
quantização INT8 integrada e suporte oficial ao ESP32-S3.

Referências: ver `docs/FUNDAMENTACAO_TECNICA.md` seções 1 e 4.

### 2.4 Protocolos IoT para Agricultura de Precisão

O protocolo **MQTT** (*Message Queuing Telemetry Transport*, OASIS 2019)
foi projetado para redes instáveis e dispositivos com recursos limitados.
Com header mínimo de 2 bytes (vs. ~800 bytes do HTTP), suporte a
Quality of Service (QoS 0/1/2) e modelo publish/subscribe, é o protocolo
dominante em sistemas IoT agrícolas (ver `docs/FUNDAMENTACAO_TECNICA.md` seção 5).

O broker **Mosquitto** (Eclipse Foundation) é a implementação open-source
de referência, disponível para Windows/Linux/Docker, utilizado no Ceres
para comunicação local entre ESP32 e backend Django.

### 2.5 Trabalhos Relacionados

| Trabalho | Hardware | Modelo | Acurácia | Dataset |
|----------|----------|--------|----------|---------|
| LeafSense (ACM, 2024) | ESP32-CAM | TinyML CNN | 92% | PlantVillage |
| Springer IoT Tomato (2025) | ESP32 + câmera | TinyML | n/d | PlantVillage |
| RTR_Lite_MobileNetV2 (2025) | Edge genérico | MobileNetV2 leve | > 93% | PlantVillage |
| **Ceres Diagnóstico** | **ESP32-S3 N16R8** | **MobileNetV2 INT8** | **[PENDENTE]** | **PlantVillage + PlantDoc** |

**Diferencial do Ceres em relação aos trabalhos relacionados:**
- Cobre 10 classes de doenças (maioria dos trabalhos usa 4–5 classes)
- Integra MQTT + backend REST + app mobile em sistema completo
- Valida em campo real (PlantDoc) além do laboratório (PlantVillage)
- Hardware ESP32-S3 com PSRAM 8MB para modelos maiores

---

## 3. METODOLOGIA

### 3.1 Arquitetura Geral do Sistema

```
[Câmera OV5640]
      |
[ESP32-S3 N16R8]  <-- TFLite Micro (MobileNetV2 INT8)
      |
   [MQTT]  ---> [Broker Mosquitto] ---> [Django REST API]
                                              |
                                        [PostgreSQL 18]
                                              |
                                       [App Flutter]
                                    (Android / iOS)
```

O ciclo de operação completo:
1. ESP32-S3 captura imagem com OV5640 (96x96 RGB)
2. Executa inferência local: MobileNetV2 INT8 retorna classe + confiança
3. Se confiança > 0.70: publica JSON em `ceres/sensor/<device_id>` via MQTT
4. Django MQTT listener persiste evento no PostgreSQL
5. App Flutter consulta `GET /api/diagnostico/historico/` e exibe resultado

### 3.2 Dataset e Pré-processamento

**Dataset primário:** PlantVillage (Hughes & Salathé, 2015)
- 18.160 imagens de folhas de tomate, 10 classes
- Licença CC BY 4.0
- Fonte: Kaggle `abdallahalidev/plantvillage-dataset`

**Pré-processamento (execute `datasets/scripts/prepare_plantvillage.py`):**

| Etapa | Descrição | Parâmetro |
|-------|-----------|-----------|
| Split | Estratificado por classe | 70% train / 15% val / 15% test |
| Seed | Reprodutibilidade | 42 |
| Augmentation | Offline, apenas treino | 6 operações × 12.707 imgs |
| Resultado | Imagens de treino totais | 88.949 |

**Augmentations aplicadas:**
- Flip horizontal e vertical (variações de orientação de campo)
- Rotação ±15° (variação de ângulo de captura)
- Brilho ±20% (variação de iluminação solar)

**Validação em campo real:** PlantDoc (~500 imgs) — aplicado após treino
para medir generalização fora do laboratório.

### 3.3 Treinamento do Modelo

**Plataforma:** Edge Impulse Studio (tier gratuito)
**Arquitetura:** MobileNetV2 96×96 0.35 (variante leve)
**Quantização:** INT8 pós-treinamento
**Hiperparâmetros:**

| Parâmetro | Valor |
|-----------|-------|
| Epochs | 50 |
| Learning rate | 0.0005 |
| Batch size | 32 |
| Data augmentation | Desligada (feita offline) |
| Input size | 96×96 RGB |

`[PENDENTE: acurácia treino, val, test após execução no Edge Impulse]`

### 3.4 Firmware ESP32-S3

**Plataforma:** PlatformIO + Arduino framework
**Localização:** `firmware/esp32s3_ceres/`

Ciclo de execução:
```
loop() {
  1. Captura frame OV5640 (96x96 RGB)
  2. Normaliza pixels [-1, 1]
  3. run_inference() -> classe, confianca
  4. Se confianca > THRESHOLD (0.70):
       Lê DHT22 (temperatura, umidade_ar)
       Lê GPIO34 ADC (umidade_solo)
       Publica JSON via MQTT
  5. Aguarda 30s
}
```

`[PENDENTE: Sprint 2]`

### 3.5 Backend Django REST

**Framework:** Django 6.0.4 + DRF 3.17.1
**Banco:** PostgreSQL 18 (porta 5433)
**Autenticação:** SimpleJWT (RFC 7519)

**Endpoints implementados:**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/diagnostico/iniciar/ | Retorna primeira pergunta da árvore |
| POST | /api/diagnostico/responder/ | Avança na árvore, retorna diagnóstico |
| GET | /api/diagnostico/historico/ | Lista eventos paginados (page_size=10) |

**Models principais:**
- `Pergunta`, `Opcao`, `Diagnostico` — motor de diagnóstico por árvore
- `DiagnosticoEvento` — evento IoT: device_id, classe, confiança, sensores, timestamp
- `Tenant`, `CustomUser` — multi-tenant para cooperativas

### 3.6 Aplicativo Flutter

`[PENDENTE: Sprint 3]`

**Stack:** Flutter (Dart) + Drift (cache SQLite)

**Telas planejadas:**
- `DiagnosticoResultadoScreen` — nome da doença, confiança, sensores, recomendação Embrapa
- `HistoricoScreen` — paginação infinita + pull-to-refresh
- `SensorStatusScreen` — polling 10s, status online/offline

---

## 4. DESENVOLVIMENTO E IMPLEMENTAÇÃO

### 4.1 Sprint 0 — Motor de Diagnóstico ✅ CONCLUÍDA

**Critério de aceite atingido:** 5/5 testes passando, API funcional.

**Principais decisões técnicas:**
- Árvore de decisão como motor inicial (antes do TFLite estar disponível)
- Multi-tenant estruturado desde o início para escabilidade futura
- JWT sem estado no servidor (stateless) para compatibilidade com mobile

**Testes validados (2026-04-28, PostgreSQL 18, Python 3.13):**
```
test_evento_criado_com_dados_validos        OK
test_historico_retorna_lista_paginada       OK
test_iniciar_diagnostico_retorna_raiz       OK
test_responder_retorna_diagnostico_final    OK
test_responder_retorna_proxima_pergunta     OK
Ran 5 tests in 5.025s — OK
```

### 4.2 Sprint 1 — MQTT + Dataset + Treino 🔄 EM ANDAMENTO

#### 4.2.1 Preparação do Dataset (2026-04-28)

Download e processamento do PlantVillage:
- 18.160 imagens → split estratificado 70/15/15
- 88.949 imagens de treino após 6 augmentations offline
- Scripts: `backend/datasets/scripts/prepare_plantvillage.py`
- Saídas: `backend/datasets/processed/train|val|test`

#### 4.2.2 Treinamento Edge Impulse
`[PENDENTE]`

#### 4.2.3 Firmware ESP32 MQTT
`[PENDENTE]`

#### 4.2.4 Backend MQTT Listener
`[PENDENTE — já modelado no DiagnosticoEvento, falta o command mqtt_listener]`

### 4.3 Sprint 2 — ESP32-S3 + TFLite ⏳ PENDENTE

`[PENDENTE: preencher após Sprint 2]`

### 4.4 Sprint 3 — Flutter + Experimentos ⏳ PENDENTE

`[PENDENTE: preencher após Sprint 3]`

---

## 5. RESULTADOS E DISCUSSÃO

### 5.1 Experimento de Treinamento — Edge Impulse vs TensorFlow Local

O projeto realizou dois experimentos de treinamento para comparação:

**Design experimental:**

| Parametro | Experimento A (Edge Impulse) | Experimento B (TF Local) |
|-----------|------------------------------|--------------------------|
| Plataforma | Edge Impulse Studio (nuvem) | TensorFlow 2.18 + WSL2 |
| Hardware treino | GPU Edge Impulse | RTX 3060 Ti (8GB VRAM) |
| Dataset | 18.160 imgs originais | 88.949 imgs com aug offline |
| Augmentation | Online (Edge Impulse) | Offline (prepare_plantvillage.py) |
| Arquitetura | MobileNetV2 96x96 0.35 | MobileNetV2 96x96 0.35 |
| Quantizacao | INT8 automatica (EI) | INT8 pos-treinamento (TFLite) |
| Epochs | 50 (max 60min) | 50 |

**Resultados:**

`[PENDENTE: preencher apos conclusao dos dois treinamentos]`

| Metrica | Exp A (Edge Impulse) | Exp B (TF Local) |
|---------|---------------------|------------------|
| Acuracia val set | - | - |
| Acuracia test set | - | - |
| Tamanho modelo (.tflite) | - | - |
| Latencia ESP32-S3 | - | - |

### 5.2 Acurácia do Modelo

`[PENDENTE: preencher após treinamentos]`

Métricas esperadas (baseline literatura):
- Acurácia top-1 no val set: > 85%
- Acurácia top-1 no test set PlantVillage: > 85%
- Acurácia no PlantDoc (campo real): > 70%

### 5.3 Latência de Inferência

`[PENDENTE: preencher após Sprint 2 — medição com esp_timer_get_time()]`

Meta: < 300ms no ESP32-S3 @ 240MHz com modelo INT8.

### 5.4 Experimento Edge vs Cloud

`[PENDENTE: preencher após Sprint 3 — script experiment_edge_vs_cloud.py]`

**Design do experimento:**
- 100 imagens do test split
- Cenário Edge: latência real no ESP32-S3
- Cenário Cloud simulado: tflite-runtime no PC + overhead 200ms (4G)
- Métricas: latência média, desvio padrão, disponibilidade offline

### 5.4 Avaliação em Campo (PlantDoc)

`[PENDENTE: preencher após Sprint 2]`

---

## 6. CONCLUSÃO

`[PENDENTE: preencher após Sprint 3]`

**Contribuições esperadas:**
1. Sistema embarcado completo de baixo custo (< R$200) para diagnóstico fitossanitário
2. Dataset PlantVillage processado e aumentado para 88.949 imagens (público no GitHub)
3. Script reproduzível de preparação de dataset com split estratificado
4. Comparativo quantitativo edge vs cloud em contexto agrícola brasileiro
5. Código-fonte aberto para replicação por pesquisadores e produtores

**Trabalhos futuros:**
- Ampliar para outras culturas (soja, milho, café)
- Integrar georreferenciamento via GPS no ESP32-S3
- Federated learning para atualização do modelo sem enviar dados ao servidor
- Parceria com cooperativas agrícolas de Sorriso-MT para validação em escala

---

## 7. REFERÊNCIAS

> Formato ABNT NBR 6023:2018

GOOGLE. *TensorFlow Lite Micro*. Disponível em: https://www.tensorflow.org/lite/microcontrollers. Acesso em: abr. 2026.

HOWARD, A. G. et al. MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. *arXiv*, 2017. Disponível em: https://arxiv.org/abs/1704.04861.

HUGHES, D.; SALATHÉ, M. An open access repository of images on plant health to enable the development of mobile disease diagnostics through machine learning and crowdsourcing. *arXiv*, 2015. Disponível em: https://arxiv.org/abs/1511.08060.

MOHANTY, S. P.; HUGHES, D. P.; SALATHÉ, M. Using Deep Learning for Image-Based Plant Disease Detection. *Frontiers in Plant Science*, v. 7, 2016. Disponível em: https://pmc.ncbi.nlm.nih.gov/articles/PMC5032846/.

SANDLER, M. et al. MobileNetV2: Inverted Residuals and Linear Bottlenecks. *CVPR*, 2018.

THAPA, R. et al. The Plant Doc Dataset. *arXiv*, 2020. (PlantDoc — validação em campo real)

WARDEN, P.; SITUNAYAKE, D. *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*. O'Reilly, 2019.

`[PENDENTE: adicionar referências completas de MQTT, Edge Impulse, Flutter, Django conforme uso no texto]`

---

*Documento gerado e mantido automaticamente pelo Claude Code.*
*Última atualização: 2026-04-28*
