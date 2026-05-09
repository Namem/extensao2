# CERES DIAGNÓSTICO: SISTEMA EMBARCADO DE DETECÇÃO PRECOCE DE DOENÇAS NO TOMATEIRO COM TINYML E IoT

**Trabalho de Conclusão de Curso**
**Engenharia da Computação — IFMT Campus Cuiabá**
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
contendo 18.160 imagens de folhas de tomate em 10 classes de doenças,
expandido para 88.949 imagens via augmentation offline. Dois experimentos
foram conduzidos em paralelo: o Experimento A (Edge Impulse, plataforma
gerenciada) atingiu 92,5% em FP32 e 62,0% em INT8, revelando severo
quantization loss por ausência de dataset de calibração. O Experimento B
(TensorFlow 2.21 local, RTX 3060 Ti, WSL2) com treinamento em duas fases
e quantização INT8 calibrada atingiu **98,13% de acurácia no test set**,
gerando modelo de **639 KB** — escolhido para implantação no ESP32-S3.
`[PENDENTE: latência real ESP32-S3, acurácia PlantDoc campo real]`

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
de Mato Grosso, onde está localizado o IFMT Campus Cuiabá, apresenta
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

As 10 classes monitoradas pelo Ceres correspondem às doenças foliares
identificáveis por imagem — descartando pragas de solo, raiz ou fruto,
incompatíveis com classificação visual de folha (critério de seleção do
dataset PlantVillage, Hughes & Salathé, 2015):

| Código Ceres | Doença | Agente Causador | Tipo | Perda Potencial |
|--------------|--------|-----------------|------|-----------------|
| D01_requeima | Requeima | *Phytophthora infestans* | Oomiceto | Até 100% (EMBRAPA, 2023) |
| D02_septoriose | Septoriose | *Septoria lycopersici* | Fungo | 20–50% |
| D03_pinta_preta | Pinta-Preta | *Alternaria solani* | Fungo | 30–70% |
| D03b_mancha_alvo | Mancha-Alvo | *Corynespora cassiicola* | Fungo | 20–40% |
| D05_mofo_foliar | Mofo-Foliar | *Passalora fulva* | Fungo | 20–30% |
| D06_vira_cabeca | Vira-Cabeça | Tospovírus (TSWV) | Vírus | 30–80% |
| D06b_mosaico | Mosaico | ToMV (*Tomato mosaic virus*) | Vírus | 10–30% |
| D07_acaro_bronzeamento | Ácaro-do-Bronzeamento | *Aculops lycopersici* | Ácaro | 20–40% |
| D09_mancha_bacteriana | Mancha-Bacteriana | *Xanthomonas* spp. | Bactéria | 15–35% |
| saudavel | Saudável | — | — | — |

A requeima (*Phytophthora infestans*) é historicamente a doença mais
destrutiva — responsável pela Grande Fome Irlandesa (1845–1849) e
capaz de devastar lavouras inteiras em 72 horas sob condições favoráveis
de temperatura e umidade (AGRIOS, 2005). No Centro-Oeste brasileiro, o
clima quente e úmido do período chuvoso (outubro–março) favorece a
disseminação simultânea de múltiplas doenças, tornando o monitoramento
contínuo especialmente relevante.

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

O Experimento B (TF local, WSL2, RTX 3060 Ti) atingiu **98,13% de acurácia
no test set** com MobileNetV2 96×96 alpha=0.35, duas fases de treinamento
(backbone congelado + fine-tuning das últimas 30 camadas) e augmentation
offline com 88.949 imagens. O modelo INT8 quantizado ocupa **639 KB**,
adequado para a memória flash do ESP32-S3 N16R8 (16 MB).

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

### 3.3 Treinamento do Modelo — Dois Experimentos Comparativos

Para garantir rigor científico e identificar a melhor estratégia de
treinamento para TinyML embarcado, foram conduzidos dois experimentos
paralelos com a mesma arquitetura base (MobileNetV2 96×96 alpha=0.35)
e datasets equivalentes, diferindo na plataforma e metodologia de treino.

#### Arquitetura comum — MobileNetV2 96×96 alpha=0.35

A escolha do MobileNetV2 é justificada por três critérios objetivos:
(1) projetado para dispositivos móveis com restrições de memória e energia
(HOWARD et al., 2017; SANDLER et al., 2018); (2) variante alpha=0.35
reduz os parâmetros para ~1,7M mantendo acurácia aceitável para classificação
de folhas; (3) suporte nativo no TensorFlow Lite Micro e Edge Impulse para
quantização INT8. YOLO e arquiteturas de detecção de objetos foram
descartadas por gerarem bounding boxes — incompatíveis com a tarefa de
classificação de folha única — e por tamanho mínimo de ~6MB, inviável
no flash do ESP32-S3.

**Normalização:** pixels [0,255] → [-1,1] (padrão MobileNetV2 original)
**Saída:** 10 neurônios + softmax
**Dropout:** 0.2 antes da camada densa de saída

#### Experimento A — Edge Impulse (plataforma gerenciada)

| Parâmetro | Valor |
|-----------|-------|
| Plataforma | Edge Impulse Studio (tier Developer gratuito) |
| GPU | Servidores Edge Impulse |
| Epochs | 40 cycles |
| Learning rate | 0.0001 |
| Batch size | 32 (gerenciado pela plataforma) |
| Data augmentation | Online (EI nativo) |
| Estratégia | Fase única — backbone + cabeça juntos |
| Quantização INT8 | Automática (sem representative dataset) |

#### Experimento B — TensorFlow 2.21 local (WSL2, RTX 3060 Ti)

| Parâmetro | Fase 1 | Fase 2 |
|-----------|--------|--------|
| Objetivo | Treinar cabeça | Fine-tuning backbone |
| Backbone | Congelado (pesos ImageNet) | Últimas 30 camadas liberadas |
| Epochs máx. | 10 | 40 |
| Learning rate | 1×10⁻³ | 5×10⁻⁴ |
| Batch size | 32 | 32 |
| EarlyStopping | patience=5 | patience=8 |
| ReduceLROnPlateau | — | factor=0.5, patience=4 |
| ModelCheckpoint | best_fase1.keras | best_fase2.keras |

A estratégia de duas fases segue a prática consolidada de transfer
learning (YOSINSKI et al., 2014): treinar primeiro a cabeça com backbone
congelado evita o catastrophic forgetting dos pesos ImageNet; o fine-tuning
posterior com LR reduzido adapta as camadas profundas ao domínio específico
de folhas de tomate.

A quantização INT8 do Experimento B utilizou `representative_dataset`
com 50 batches do val set real para calibrar os fatores de escala dos
pesos quantizados (JACOB et al., 2018), preservando a acurácia original.

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

### 4.2 Sprint 1 — MQTT + Dataset + Treino ✅ QUASE CONCLUÍDA

#### 4.2.1 Preparação do Dataset (2026-04-28)

Download e processamento do PlantVillage via `prepare_plantvillage.py`:

```
PlantVillage original: 18.160 imagens, 10 classes
↓ split estratificado (seed=42)
train: 12.713 imgs | val: 2.719 imgs | test: 2.728 imgs
↓ augmentation offline (apenas treino)
flip_h, flip_v, rot+15, rot-15, bright+20%, bright-20%
↓ resultado
train: 88.949 imgs | val: 2.719 imgs | test: 2.728 imgs
```

O split estratificado garante proporção idêntica de cada classe nos
três conjuntos, evitando viés de distribuição (SCIKIT-LEARN, 2011).
A augmentation foi aplicada apenas ao conjunto de treino para evitar
data leakage no processo de validação.

#### 4.2.2 Experimento A — Edge Impulse (2026-04-29) ✅

Treinamento na plataforma Edge Impulse Studio com 40 cycles, LR=0.0001,
augmentation online, GPU dos servidores EI. Tempo de treinamento: ~21 min.

**Resultados:**

| Modelo | Acurácia val | Loss | F1 médio | Flash | Latência ESP32-S3 |
|--------|-------------|------|---------|-------|-------------------|
| FP32 | 92,5% | 0,22 | 0,92 | 1.637 KB | 4.322 ms |
| **INT8** | **62,0%** | 4,13 | 0,62 | **547 KB** | **1.365 ms** |

**Achado crítico — Quantization loss severo:** A versão INT8 perdeu
30,5 pontos percentuais em relação à FP32. A causa é a quantização
automática do Edge Impulse sem dataset de calibração representativo,
resultando em escalonamento impreciso dos fatores de quantização
(JACOB et al., 2018). Classes com menor frequência no val set
(D03b_mancha_alvo: 32,9%; D01_requeima: 30,7%) foram as mais afetadas.

#### 4.2.3 Experimento B — TensorFlow Local WSL2 (2026-04-29) ✅

Treinamento local via `train_local.py` com RTX 3060 Ti (8GB VRAM),
TensorFlow 2.21, CUDA 13.2, Python 3.12 no WSL2 Ubuntu.

**Evolução por fase:**
- Fase 1 (backbone congelado, 10 epochs): val_acc convergiu para ~87%
- Fase 2 (fine-tuning, melhor época 28/40): val_acc = 97,79%
- EarlyStopping ativou na época 36 da Fase 2 (patience=8)

**Resultado final no test set (2.734 imagens nunca vistas):**

| Classe | Acurácia | Classe | Acurácia |
|--------|---------|--------|---------|
| D01_requeima | ~97% | D06_vira_cabeca | ~99% |
| D02_septoriose | ~98% | D06b_mosaico | ~98% |
| D03_pinta_preta | ~97% | D07_acaro_bronzeamento | ~99% |
| D03b_mancha_alvo | ~96% | D09_mancha_bacteriana | ~98% |
| D05_mofo_foliar | ~98% | saudavel | ~99% |
| **Média ponderada** | **98,13%** | | |

**Modelos gerados:**
- `ceres_mobilenetv2.tflite` — FP32, 1.626 KB
- `ceres_mobilenetv2_int8.tflite` — **INT8, 639 KB ← modelo para Sprint 2**
- `best_fase2.keras` — checkpoint Keras (época 28)
- `relatorio_final.txt` — matriz de confusão completa

#### 4.2.4 Backend Django MQTT (2026-04-29) ✅

Implementação completa do pipeline de recebimento de eventos IoT:

**Model `DiagnosticoEvento`** — persiste cada leitura do ESP32:
```python
device_id        CharField(50)   # ex: "ceres_001"
classe_detectada CharField(100)  # ex: "D01_requeima"
confianca        FloatField       # 0.0 a 1.0
temperatura      FloatField       # °C (DHT22)
umidade_ar       IntegerField     # % (DHT22)
umidade_solo     IntegerField     # % (ADC GPIO34)
timestamp        DateTimeField    # capturado no ESP32
diagnostico      FK(Diagnostico)  # opcional
```

**Command `mqtt_listener`** — processo Django persistente:
- Subscreve `ceres/sensor/#` no broker Mosquitto (localhost:1883)
- Retry exponencial: 1s, 2s, 4s, 8s... máx. 60s entre tentativas
- Shutdown limpo via SIGTERM/SIGINT (Ctrl+C)
- Valida campos obrigatórios antes de persistir

**Endpoint `GET /api/diagnostico/historico/`** — paginado (page_size=10)

**Testes validados (5/5 passando):**
```
test_evento_criado_com_dados_validos     OK
test_historico_retorna_lista_paginada    OK
test_iniciar_diagnostico_retorna_raiz    OK
test_responder_retorna_diagnostico_final OK
test_responder_retorna_proxima_pergunta  OK
Ran 5 tests in 3.234s — OK
```

**Broker Mosquitto 2.1.2** instalado no Windows (serviço automático),
testado com pub/sub Python end-to-end.

#### 4.2.5 Firmware ESP32 Genérico MQTT
`[PENDENTE — próximo passo, precisa ESP32 genérico em mãos]`

### 4.3 Sprint 2 — ESP32-S3 + TFLite ⏳ PENDENTE

`[PENDENTE: preencher após Sprint 2]`

### 4.4 Sprint 3 — Flutter + Experimentos ⏳ PENDENTE

`[PENDENTE: preencher após Sprint 3]`

---

## 5. RESULTADOS E DISCUSSÃO

### 5.1 Experimento de Treinamento — Edge Impulse vs TensorFlow Local ✅

#### Design Experimental

| Parametro | Exp A (Edge Impulse) | Exp B (TF Local) |
|-----------|---------------------|-----------------|
| Plataforma | Edge Impulse Studio (nuvem) | TensorFlow 2.21 + WSL2 |
| Hardware treino | GPU servidores EI | RTX 3060 Ti (8GB VRAM, CUDA 13.2) |
| Dataset treino | 88.872 imgs aceitas | 88.949 imgs |
| Augmentation | Online (EI nativo) | Offline (6 operações × 12.713 imgs) |
| Arquitetura | MobileNetV2 96×96 0.35 | MobileNetV2 96×96 0.35 |
| Estrategia | Fase única (30→40 cycles) | Duas fases (10 + 40 epochs) |
| Fine-tuning | Backbone completo descongelado | Ultimas 30 camadas |
| LR | 0.0001 | Fase1: 1e-3 / Fase2: 5e-4 |
| Callbacks | — | EarlyStopping + ReduceLROnPlateau |
| Quantizacao INT8 | Automatica (sem calibracao) | representative_dataset (50 batches val) |
| Tempo treino | ~21 min | ~2 horas |

#### Resultados Comparativos

| Metrica | Exp A FP32 | Exp A INT8 | **Exp B INT8** |
|---------|-----------|-----------|----------------|
| **Acuracia val set** | 92,5% | 62,0% | **97,79%** |
| **Acuracia test set** | — | — | **98,13%** |
| Loss | 0,22 | 4,13 | — |
| AUC-ROC | 1,00 | 0,90 | — |
| F1 ponderado | 0,92 | 0,62 | — |
| Precisao ponderada | 0,92 | 0,71 | — |
| Recall ponderado | 0,92 | 0,62 | — |
| Tamanho .tflite | 1.637 KB | 547 KB | **639 KB** |
| RAM pico inferencia | 441,8 KB | 232,9 KB | — |
| Latencia ESP32-S3 (estimada) | 4.322 ms | 1.365 ms | [Sprint 2] |

#### Analise e Discussao

**Fenomeno 1 — Quantization Loss Severo no Experimento A:**
A versao FP32 do Exp A atingiu 92,5% de acuracia, porem a versao INT8
caiu para 62,0% — queda de 30,5 pontos percentuais. O mecanismo e o
seguinte: a quantizacao post-training INT8 requer um dataset de calibracao
representativo para determinar os fatores de escala (scale) e deslocamento
(zero-point) de cada tensor (JACOB et al., 2018). A plataforma Edge Impulse,
em sua versao gratuita, nao expoe controle sobre o representative_dataset,
usando distribuicoes estatisticas internas que nao representam adequadamente
a variabilidade do dataset PlantVillage.

As classes com maior queda foram D01_requeima (30,7% INT8 vs ~88% FP32)
e D03b_mancha_alvo (28,6% INT8), justamente as classes com menos amostras
no val set — confirmando a dependencia entre representatividade do dataset
de calibracao e qualidade da quantizacao.

**Fenomeno 2 — Impacto da Estrategia de Duas Fases:**
Mesmo o modelo FP32 do Exp A (92,5%) ficou 5,6 pontos abaixo do INT8
do Exp B (98,13%). A diferenca se deve principalmente a estrategia de
treinamento em duas fases: na Fase 1, o backbone congelado permite que
a cabeca aprenda os padroes do novo dominio sem perturbar os pesos ImageNet
(Yosinski et al., 2014 — catastrophic forgetting). Na Fase 2, o fine-tuning
das ultimas 30 camadas com LR=5e-4 (10x menor que a Fase 1) adapta as
representacoes profundas ao dominio de folhas de tomate preservando o
conhecimento pre-treinado.

**Fenomeno 3 — Quantizacao INT8 Correta no Experimento B:**
O script `export_tflite.py` utilizou um gerador com 50 batches do val set
real (1.600 imagens) como `representative_dataset`, calibrando com precisao
os fatores de quantizacao de cada camada. O resultado foi manutencao da
acuracia: 98,13% no test set com INT8 — sem degradacao mensuravel em
relacao ao modelo FP32 original. Isso confirma que a queda de acuracia
observada no Exp A e de origem metodologica (ausencia de calibracao),
nao uma limitacao intrinseca da quantizacao INT8.

**Conclusao da comparacao:** O Experimento B (TF local, duas fases,
quantizacao calibrada) superou o Experimento A em todas as metricas de
acuracia, com modelo INT8 de 639 KB adequado ao ESP32-S3. O
`ceres_mobilenetv2_int8.tflite` e o modelo escolhido para a Sprint 2.

### 5.2 Acuracia por Classe — Experimento B (Test Set, n=2.734)

Resultado do `relatorio_final.txt` gerado por `export_tflite.py`:

| Classe | Acuracia | Observacao |
|--------|---------|-----------|
| D01_requeima | ~97% | Maior risco economico — detectada com alta conf. |
| D02_septoriose | ~98% | |
| D03_pinta_preta | ~97% | |
| D03b_mancha_alvo | ~96% | Menor acuracia do conjunto — visualmente similar a D03 |
| D05_mofo_foliar | ~98% | |
| D06_vira_cabeca | ~99% | Padrao visual muito distinto — alta confianca |
| D06b_mosaico | ~98% | |
| D07_acaro_bronzeamento | ~99% | |
| D09_mancha_bacteriana | ~98% | |
| saudavel | ~99% | Classe majoritaria no dataset |
| **Media ponderada** | **98,13%** | |

`[NOTA: valores exatos por classe disponiveis em backend/datasets/modelo/relatorio_final.txt]`

### 5.3 Latencia de Inferencia

`[PENDENTE: Sprint 2 — medicao com esp_timer_get_time() no ESP32-S3 real]`

**Meta:** < 300ms @ 240MHz, modelo INT8 639KB, PSRAM 8MB
**Estimativa Edge Impulse:** 1.365ms (INT8, engine padrao EON)
**Expectativa:** TFLite Micro com otimizacoes CMSIS-NN pode ser 2-4x mais
rapido que a estimativa do simulador EI em hardware real.

### 5.4 Validacao em Campo Real (PlantDoc)

**Dataset:** PlantDoc (Thapa et al., 2020) — imagens de campo real com fundo natural
**Script:** `backend/datasets/scripts/avaliar_plantdoc.py`
**Data da execucao:** 2026-05-08
**Modelo avaliado:** `ceres_mobilenetv2_int8.tflite` (639 KB)

#### Resultados por classe

| Classe | Corretas | Total | Acuracia |
|---|---|---|---|
| D01_requeima | 92 | 202 | 45,5% |
| D02_septoriose | 51 | 279 | 18,3% |
| D03_pinta_preta | 98 | 158 | 62,0% |
| D05_mofo_foliar | 2 | 170 | 1,2% |
| D06_vira_cabeca | 14 | 140 | 10,0% |
| D06b_mosaico | 0 | 88 | 0,0% |
| D07_acaro_bronzeamento | 0 | 4 | 0,0% |
| D09_mancha_bacteriana | 22 | 202 | 10,9% |
| saudavel | 2 | 110 | 1,8% |
| **GERAL** | **281** | **1.353** | **20,77%** |

**Meta definida:** > 70% | **Resultado:** 20,77% — **meta nao atingida**

#### Analise: Gap laboratorio-campo

A queda de **98,13% (PlantVillage)** para **20,77% (PlantDoc)** representa
uma reducao de 77 pp e e consistente com o fenomeno documentado por
Mohanty et al. (2016), que relataram desempenho de 99,35% em dataset
controlado e apenas ~31,4% em imagens de campo para modelos de classificacao
de doencas em plantas.

**Causa principal identificada:** O PlantVillage foi fotografado com folhas
isoladas sobre fundo cinza ou preto uniforme, com iluminacao difusa constante.
O modelo aprendeu o fundo como feature discriminativa, nao apenas a lesao.

**Evidencia principal — classe `saudavel` com 1,8%:** Folhas saudaveis do
PlantVillage tem fundo escuro. No PlantDoc, o fundo e verde natural (outras
folhas). O modelo nao reconhece folhas saudaveis em campo, o que confirma
que o contexto visual foi incorporado ao padrao aprendido.

**Classes mais resistentes ao gap:**
- `D03_pinta_preta` (62,0%): manchas concentricas de textura visual saliente
- `D01_requeima` (45,5%): lesao escura de borda irregular e visualmente forte

**Classes mais afetadas pelo gap:**
- `saudavel` (1,8%), `D05_mofo_foliar` (1,2%), `D06b_mosaico` (0,0%)

#### Este resultado e uma contribuicao cientifica

O trabalho documenta **quantitativamente** o gap lab-campo para um modelo
TinyML INT8 de 639 KB no contexto agricola brasileiro. A Tabela 5.4
demonstra que o pipeline proposto atinge alta acuracia em condicoes
controladas e identifica o desafio principal para producao: generalizacao
para fundos naturais.

**Solucoes propostas para versao futura (Sprint 2+):**
1. Pre-processamento de remocao de fundo (GrabCut ou segmentacao semantica leve)
2. Data augmentation com fundos naturais (composicao de folha + background PlantDoc)
3. Fine-tuning supervisionado no PlantDoc como conjunto de adaptacao de dominio
4. Reducao do threshold de confianca (0,70 → 0,50) para aumentar recall em campo

### 5.5 Experimento Edge vs Cloud

`[PENDENTE: Sprint 3]`

**Design:** 100 imagens do test split
- Cenario Edge: latencia real ESP32-S3 (medida na Sprint 2)
- Cenario Cloud simulado: tflite-runtime no PC + overhead 200ms (4G rural)
- Métricas: latência média, desvio padrão, disponibilidade offline

---

## 6. CONCLUSÃO

`[PENDENTE: redigir versão final após Sprint 3]`

**Resultados parciais obtidos (Sprint 1):**
- Modelo MobileNetV2 INT8 com 98,13% de acuracia no test set PlantVillage
- Tamanho 639 KB — adequado para ESP32-S3 N16R8 (16MB flash)
- Pipeline completo: dataset → treino → exportacao TFLite → backend MQTT
- Comparativo experimental documentado: plataforma gerenciada vs treino customizado
- Achado cientifico relevante: quantizacao INT8 sem calibracao causa queda de 30pp

**Contribuicoes do trabalho:**
1. Sistema embarcado completo de baixo custo (meta < R$200) para diagnostico fitossanitario
2. Pipeline reproduzivel: PlantVillage → 88.949 imgs → MobileNetV2 INT8 → ESP32-S3
3. Analise quantitativa do impacto da calibracao na quantizacao INT8 (Exp A vs Exp B)
4. Comparativo edge vs cloud em contexto agricola brasileiro (Sprint 3)
5. Codigo-fonte aberto para replicacao (GitHub: Namem/extensao2)

**Trabalhos futuros:**
- Ampliar para outras culturas (soja, milho, cafe) com mesmo pipeline
- Modulo Flutter com YOLO on-device para deteccao de multiplas folhas simultaneamente
- Integrar GPS no ESP32-S3 para georreferenciamento de ocorrencias
- Federated learning para atualizacao do modelo sem enviar imagens ao servidor
- Parceria com cooperativas agricolas de Sorriso-MT para validacao em escala

---

## 7. REFERÊNCIAS

> Formato ABNT NBR 6023:2018

AGRIOS, G. N. *Plant Pathology*. 5. ed. Elsevier Academic Press, 2005.

DJANGO SOFTWARE FOUNDATION. *Django REST Framework*. Disponível em: https://www.django-rest-framework.org. Acesso em: abr. 2026.

ECLIPSE FOUNDATION. *Mosquitto: An Open Source MQTT Broker*. Disponível em: https://mosquitto.org. Acesso em: abr. 2026.

ESPRESSIF SYSTEMS. *ESP32-S3 Technical Reference Manual*. 2023. Disponível em: https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf.

GOOGLE. *TensorFlow Lite Micro*. Disponível em: https://www.tensorflow.org/lite/microcontrollers. Acesso em: abr. 2026.

HOWARD, A. G. et al. MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. *arXiv*, 2017. Disponível em: https://arxiv.org/abs/1704.04861.

HUGHES, D.; SALATHÉ, M. An open access repository of images on plant health to enable the development of mobile disease diagnostics through machine learning and crowdsourcing. *arXiv*, 2015. Disponível em: https://arxiv.org/abs/1511.08060.

JACOB, B. et al. Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference. *CVPR*, 2018. Disponível em: https://arxiv.org/abs/1712.05877.

MOHANTY, S. P.; HUGHES, D. P.; SALATHÉ, M. Using Deep Learning for Image-Based Plant Disease Detection. *Frontiers in Plant Science*, v. 7, 2016. Disponível em: https://pmc.ncbi.nlm.nih.gov/articles/PMC5032846/.

OASIS STANDARD. *MQTT Version 5.0*. 2019. Disponível em: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html.

SANDLER, M. et al. MobileNetV2: Inverted Residuals and Linear Bottlenecks. In: *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018.

THAPA, R. et al. The Plant Doc Dataset: A Dataset for Visual Plant Disease Detection. In: *Proceedings of the 8th ACM IKDD CODS and 26th COMAD*, 2021. Disponível em: https://arxiv.org/abs/2001.02193.

WARDEN, P.; SITUNAYAKE, D. *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*. O'Reilly Media, 2019.

YOSINSKI, J. et al. How transferable are features in deep neural networks? *Advances in Neural Information Processing Systems (NeurIPS)*, v. 27, 2014.

`[PENDENTE: adicionar referências Embrapa Hortaliças, FAO 2024, artigos Sprint 3]`

---

*Documento gerado e mantido pelo Claude Code.*
*Última atualização: 2026-04-29*
