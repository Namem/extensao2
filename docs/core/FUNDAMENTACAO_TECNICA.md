# Fundamentação Técnica — Ceres Diagnóstico
**TCC Engenharia da Computação — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto
**Última atualização:** 2026-06-06

> Este documento registra a justificativa técnica e acadêmica de cada decisão
> arquitetural do projeto. Deve ser consultado na escrita do artigo e na defesa.

---

## 1. Arquitetura de IA — MobileNetV2 INT8 Quantizado

### Decisão
Utilizar **MobileNetV2** com **quantização INT8** como backbone do modelo de
classificação de doenças do tomateiro, treinado via **Edge Impulse** e
implantado como **TFLite Micro** no ESP32-S3.

### Por que MobileNetV2 e não outros?

| Modelo         | Parâmetros | Acurácia típica¹ | RAM necessária | Roda no ESP32-S3? |
|----------------|-----------|-----------------|----------------|-------------------|
| VGG16          | 138M      | ~98%            | > 500 MB       | NÃO               |
| ResNet-50      | 25M       | ~97%            | > 100 MB       | NÃO               |
| EfficientNet-B0| 5.3M      | ~97%            | ~20 MB         | NÃO (sem PSRAM)   |
| **MobileNetV2**| **3.4M**  | **93–97%**      | **< 4 MB**     | **SIM**           |
| MobileNetV1    | 4.2M      | ~90%            | ~3 MB          | Sim (inferior)    |

¹ Sobre PlantVillage (dataset de referência do projeto).

**MobileNetV2** foi projetado especificamente para dispositivos com restrição
de memória e energia (Howard et al., 2017 — Google). Sua arquitetura usa
**depthwise separable convolutions** e **inverted residuals com linear
bottlenecks**, reduzindo o número de operações (FLOPs) sem perda significativa
de acurácia em relação a redes maiores.

#### Evidências de uso em plantas / TinyML

- Coulibaly et al. (2019) — MobileNet atingiu **97,5% de acurácia** na
  detecção de doenças em folhas de arroz, superando variantes menores (FD-MobileNet: 90%).
- LeafSense (ACM, 2024) — primeiro dispositivo ESP32-CAM com TinyML para
  classificação de doenças em folhas de plantas ao vivo, acurácia de **92%**,
  latência de inferência **< 15 ms**.
- RTR_Lite_MobileNetV2 (ScienceDirect, 2025) — variante leve proposta
  especificamente para detecção de doenças em plantas em dispositivos de borda.
- Springer Nature Link (2025) — sistema automatizado para detecção de
  doenças em folhas de tomate com alerta via IoT usando TinyML.

### Por que quantização INT8?

A quantização converte os pesos do modelo de ponto flutuante (FP32) para
inteiro de 8 bits (INT8), reduzindo:
- **Tamanho do modelo**: ~4x menor (ex.: 6 MB → 1.5 MB)
- **Uso de RAM**: ~4x menor
- **Latência de inferência**: ~2–4x mais rápida em MCUs sem FPU
- **Consumo de energia**: redução significativa por operação

O ESP32-S3 possui aceleração para operações INT8 na extensão SIMD do Xtensa LX7,
tornando a quantização INT8 a escolha ideal para este hardware.
Perda de acurácia típica: **< 2%** em relação ao modelo FP32 original.

### Referências
- Howard, A. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861.
- Sandler, M. et al. (2018). *MobileNetV2: Inverted Residuals and Linear Bottlenecks*. CVPR 2018.
- [RTR_Lite_MobileNetV2 — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2214662825000271)
- [LeafSense — ACM Digital Library](https://dl.acm.org/doi/10.1145/3703412.3703438)
- [TinyML for Plant Disease Detection — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1877050925016515)
- [Automated tomato leaf disease detection — Springer](https://link.springer.com/article/10.1007/s43926-025-00257-8)

---

## 2. Dataset — PlantVillage (Hughes & Salathé, 2015)

### Decisão
Utilizar o **PlantVillage** como dataset primário de treinamento, com validação
final usando **PlantDoc** (~500 imagens de campo real).

### Por que PlantVillage?

O PlantVillage é o dataset de referência internacional para classificação de
doenças em folhas de plantas. Publicado por Hughes & Salathé (2015) na PLOS ONE,
contém **54.305 imagens** de folhas saudáveis e doentes de **14 espécies**,
incluindo **10 classes de tomate** com ~18.160 imagens — exatamente o escopo
do Ceres Diagnóstico.

**Características que justificam a escolha:**
- Licença **CC BY 4.0** — livre para uso acadêmico e comercial
- Maior dataset público disponível para folhas de tomate em laboratório
- Benchmark consolidado: utilizado em centenas de estudos desde 2015
- Disponível no Kaggle (`abdallahalidev/plantvillage-dataset`)
- Resolução padronizada e fundo neutro — ideal para treinamento inicial

**Limitação conhecida (documentada):**
Imagens coletadas em condição controlada (fundo cinza, iluminação uniforme),
o que pode reduzir a generalização em campo real. Por isso o projeto usa
**PlantDoc** (~500 imgs de campo) como conjunto de validação externa,
conforme recomendado por Thapa et al. (2020).

### Por que não usar o Roboflow "Tomato Fruit Disease Detection"?
Esse dataset é de **Object Detection em frutos** (5 classes, caixas delimitadoras),
incompatível com a tarefa do Ceres que é **classificação de folhas** em 10 classes.
Misturar os dois domínios introduziria ruído no treinamento.

### Referências
- [Hughes & Salathé (2015) — Semantic Scholar](https://www.semanticscholar.org/paper/An-open-access-repository-of-images-on-plant-health-Hughes-Salath%C3%A9/3e2da7c1c7dfc7960d1515b61f32fdc55359eea7)
- [Using Deep Learning for Image-Based Plant Disease Detection — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5032846/)
- [Plant disease recognition datasets in the age of deep learning — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11466843/)
- [Deep learning networks-based tomato disease detection — Frontiers](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2024.1493322/full)

---

## 3. Augmentation Offline e Split 70/15/15

### Decisão
Split **estratificado 70/15/15** (train/val/test) com **augmentation offline**
aplicada exclusivamente ao conjunto de treino (flip H/V, rotação ±15°, brilho ±20%).

### Por que split estratificado 70/15/15?

O split estratificado garante que a **proporção de cada classe** seja mantida
nos três conjuntos, evitando que classes minoritárias fiquem sub-representadas
na validação ou no teste — problema crítico em datasets desbalanceados como o
PlantVillage (algumas classes têm < 300 imagens).

A proporção **70/15/15** é amplamente adotada quando:
- O dataset tem tamanho moderado (10k–50k imagens)
- As classes de validação e teste precisam ter representatividade estatística igual
- Há necessidade de tuning de hiperparâmetros (val) e avaliação final independente (test)

Alternativas consideradas:
- **80/10/10**: val e test ficam pequenos demais para 10 classes (~180 imgs/classe no val)
- **60/20/20**: desperdiça dados de treino que são escassos em algumas classes
- **70/15/15**: equilíbrio ideal — ~270 imgs/classe no val, suficiente para métricas confiáveis

### Por que augmentation offline e não online?

**Augmentation online** (dentro do pipeline de treino, ex.: Keras ImageDataGenerator):
- Gera variações aleatórias a cada epoch
- Não duplica o dataset em disco
- Depende de frameworks pesados (TF/Keras)

**Augmentation offline** (pré-geração das imagens, abordagem do Ceres):
- As imagens já existem em disco ao fazer upload no Edge Impulse
- Compatível com qualquer ferramenta de treinamento (Edge Impulse Studio não
  suporta augmentation customizada no tier gratuito)
- Reproducibilidade total (seed fixo = resultados idênticos)
- Permite inspecionar visualmente as imagens geradas antes do treino

**Operações escolhidas e justificativa:**
| Operação      | Justificativa agrícola                                      |
|---------------|-------------------------------------------------------------|
| Flip H e V    | Folhas podem aparecer em qualquer orientação no campo       |
| Rotação ±15°  | Variação de ângulo ao capturar com câmera manual/drone      |
| Brilho ±20%   | Variação de iluminação solar ao longo do dia                |

Operações **não incluídas** (e por quê):
- Zoom/crop agressivo: pode remover regiões diagnósticas da folha
- Distorção de cor: pode mascarar sintomas com coloração específica (ex.: amarelamento do Vira-Cabeça)
- Ruído gaussiano: ESP32-S3 com OV5640 tem SNR alto — ruído não é realista

### Referências
- [A Survey on Image Data Augmentation for Deep Learning — Springer](https://link.springer.com/article/10.1186/s40537-019-0197-0)
- [Data Augmentation in Classification and Segmentation — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9966095/)
- [Train Test Validation Split: Best Practices — Lightly AI](https://www.lightly.ai/blog/train-test-validation-split)
- [Preventing Overfitting — Google ML Practicum](https://developers.google.com/machine-learning/practica/image-classification/preventing-overfitting)

---

## 4. TinyML — Inferência na Borda vs. Nuvem

### Decisão
Executar a inferência do modelo **diretamente no ESP32-S3** (edge), sem enviar
imagens para um servidor remoto.

### Comparativo Edge vs. Cloud

| Critério            | Cloud (servidor)          | Edge / TinyML (ESP32-S3)        |
|---------------------|---------------------------|---------------------------------|
| Latência            | 500ms–2s (depende de 4G)  | < 300ms (local, sem rede)       |
| Conectividade       | Obrigatória               | Opcional (envia apenas resultado)|
| Privacidade         | Imagens saem do dispositivo| Imagens nunca saem do hardware  |
| Custo operacional   | Servidor em nuvem (mensal)| Zero após implantação           |
| Funcionamento offline| NÃO                      | SIM                             |
| Energia consumida   | Alta (transmissão Wi-Fi)  | Baixa (só inferência local)     |

Em contexto rural brasileiro, a **conectividade é instável ou inexistente**
em lavouras remotas. Um sistema que dependa de nuvem para inferência se torna
inutilizável exatamente quando mais precisa funcionar (campo aberto, sem sinal).

O TinyML resolve isso ao mover a inteligência para o dispositivo:
"TinyML deployments do not rely on internet connectivity for inference,
with data being captured and processed on the device" (MDPI Sensors, 2025).

### Por que ESP32-S3 especificamente?

- **PSRAM de 8MB** — permite alocar buffers de imagem e o modelo TFLite
- **Xtensa LX7 dual-core @ 240MHz** — SIMD para operações INT8
- **Câmera OV5640 5MP** — resolução suficiente para diagnóstico foliar
- **Wi-Fi + BLE integrados** — publica resultado via MQTT sem hardware adicional
- **Custo**: ~R$ 60–80 (vs. Raspberry Pi 4: ~R$ 400+)
- **Suporte TFLite Micro**: biblioteca oficial do TensorFlow para microcontroladores

### Estratégia de treinamento — dois experimentos comparativos

O projeto adota dois experimentos paralelos de treinamento, cujos resultados
serão comparados no artigo:

**Experimento A — Edge Impulse (plataforma gerenciada):**
- Plataforma líder para TinyML com exportação direta para Arduino Library
- Quantização INT8 integrada e suporte oficial ao ESP32-S3
- Dataset: 18.160 imagens originais + augmentation online da plataforma
- Limitação: 60 min/job no plano gratuito

**Experimento B — TensorFlow 2.18 local (WSL2 + RTX 3060 Ti):**
- Hardware disponível: RTX 3060 Ti (8GB VRAM), CUDA 13.2, 48GB RAM
- TensorFlow via WSL2 Ubuntu (Python 3.12) com `tensorflow[and-cuda]`
- Dataset: 88.949 imagens com augmentation offline (prepare_plantvillage.py)
- Sem limite de tempo, controle total do pipeline
- Exportação manual para TFLite INT8 via `TFLiteConverter`

**Por que comparar os dois?**
A comparação gera dados originais para o artigo: qual pipeline
(gerenciado vs manual) produz melhor modelo para TinyML em termos de
acurácia, tamanho e latência no ESP32-S3?

| Criterio | Edge Impulse | TF Local |
|----------|-------------|----------|
| Facilidade | Alta | Media |
| Controle do pipeline | Baixo | Total |
| Dataset utilizado | 18k imgs | 88k imgs |
| Reproducibilidade | Media | Alta (seed fixo) |
| Custo | Gratuito (limitado) | Gratuito (sem limite) |

### Referências
- [Tiny Machine Learning and On-Device Inference — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12115890/)
- [TinyML for Ultra-Low Power AI — MDPI Future Internet](https://www.mdpi.com/1999-5903/14/12/363)
- [Federated learning and TinyML on IoT edge devices — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2405959525000839)
- [Novel Edge Device System for Plant Disease Detection — IJISAE](https://ijisae.org/index.php/IJISAE/article/download/5292/4018/10353)
- [TinyML Classification for Agriculture Objects with ESP32 — MDPI](https://www.mdpi.com/2673-6470/5/4/48)

---

## 5. Protocolo de Comunicação — MQTT

### Decisão
Usar **MQTT (Message Queuing Telemetry Transport)** com broker **Mosquitto local**
para comunicação entre o ESP32 e o servidor Django.

### Por que MQTT e não HTTP REST / WebSocket / AMQP?

| Protocolo   | Overhead (header) | QoS garantido | Ideal para MCU | Publish/Subscribe |
|-------------|-------------------|---------------|----------------|-------------------|
| HTTP REST   | ~800 bytes        | NÃO           | NÃO (pesado)   | NÃO               |
| WebSocket   | ~2–14 bytes       | NÃO           | Parcial        | NÃO               |
| **MQTT**    | **~2 bytes**      | **SIM (0/1/2)**| **SIM**       | **SIM**           |
| AMQP        | ~8 bytes          | SIM           | NÃO (pesado)   | SIM               |
| CoAP        | ~4 bytes          | Parcial       | SIM            | NÃO               |

O MQTT foi projetado especificamente para dispositivos com **recursos limitados**
e **redes instáveis** — exatamente o cenário do Ceres em campo.

**Vantagens decisivas para o projeto:**
- **Overhead mínimo**: header de apenas 2 bytes vs. 800+ do HTTP
- **QoS configurável**: garante entrega do evento de diagnóstico mesmo com queda momentânea de Wi-Fi
- **Publish/Subscribe**: o ESP32 publica em `ceres/sensor/001` e múltiplos clientes podem subscrever (Django, dashboard, app Flutter futuramente)
- **Broker local (Mosquitto)**: sem dependência de serviços de nuvem pagos, funciona em rede local

### Evidências acadêmicas
Estudo publicado no MDPI Sensors (2024) avaliou compressão de dados e
segurança em sistemas agrícolas IoT baseados em MQTT, confirmando sua
adequação para monitoramento de umidade do solo e saúde de culturas mesmo
em redes instáveis. O protocolo é adotado em sistemas de irrigação inteligente,
monitoramento de plantações e detecção de incêndios agrícolas.

### Referências
- [Efficient Data Management in Agricultural IoT with MQTT — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11174974/)
- [MQTT-Based System for Smart Livestock Housing — MDPI Sensors](https://www.mdpi.com/1424-8220/25/23/7186)
- [Precision Agriculture with MQTT — ResearchGate](https://www.researchgate.net/publication/329470076_The_Precision_Agriculture_Based_on_Wireless_Sensor_Network_with_MQTT_Protocol)
- [Smart farming for sustainable future — Springer](https://link.springer.com/article/10.1186/s42269-025-01366-8)

### 5.1 MQTT over WebSocket + TLS (HiveMQ Cloud)

#### Decisão
Migrar do Mosquitto local para **HiveMQ Cloud** como broker MQTT de produção,
utilizando **MQTT over WebSocket** (porta 8884) com **TLS** para comunicação
entre o ESP32 e o backend Django hospedado no Railway.

#### Por que HiveMQ Cloud e não Mosquitto self-hosted?

| Critério | Mosquitto local | HiveMQ Cloud |
|---|---|---|
| Infraestrutura | Requer servidor próprio 24/7 | Gerenciado, SLA 99,95% |
| TLS | Configuração manual de certificados | Certificados automáticos |
| Custo | Custo do servidor | Gratuito até 100 conexões |
| Manutenção | Atualizações, backups, firewall | Zero manutenção |
| Acessibilidade | Apenas na rede local | Acessível de qualquer lugar (ESP32 em campo) |

Para um TCC com dispositivo ESP32 em campo e backend em PaaS (Railway),
o broker precisa ser acessível publicamente com TLS. Mosquitto exigiria
um VPS dedicado — custo e complexidade injustificáveis para o escopo.

#### Por que WebSocket (porta 8884) além de TCP (porta 8883)?

Plataformas PaaS como Railway podem bloquear portas TCP arbitrárias ou
impor proxies HTTP que interferem no protocolo MQTT nativo. O MQTT over
WebSocket encapsula o protocolo MQTT dentro de uma conexão HTTP/WebSocket
padrão (RFC 6455), compatível com qualquer proxy HTTP.

O ESP32 continua usando MQTT TCP nativo (porta 8883) — a latência é menor
e não há proxy no caminho. Apenas o backend Railway usa WebSocket.

#### Segurança — TLS no ESP32

O ESP32 utiliza `WiFiClientSecure` com `setInsecure()` (aceita qualquer
certificado). Essa abordagem é aceitável para o escopo do TCC porque:
1. A comunicação é criptografada (TLS) — proteção contra sniffing
2. O risco de MITM em rede WiFi doméstica é baixo
3. Validação de CA no ESP32 requer flash de certificado raiz (~1.5KB) e
   atualização manual quando o certificado do broker expira

Para produção, recomenda-se usar `setCACert()` com o certificado raiz
do HiveMQ (ISRG Root X1 — Let's Encrypt).

#### Referências
- HiveMQ. *MQTT over WebSockets*. Disponível em: https://www.hivemq.com/blog/mqtt-essentials-special-mqtt-over-websockets/
- OASIS. *MQTT Version 5.0 — Transport*. Seção 4.2. 2019. DOI: 10.17487/RFC9431
- Espressif. *ESP-TLS — TLS Connection for ESP-IDF*. Disponível em: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/protocols/esp_tls.html

---

## 6. Backend — Django REST Framework

### Decisão
Usar **Django REST Framework (DRF)** com **PostgreSQL 15** e autenticação **SimpleJWT**.

### Justificativa
- Django é o framework Python mais maduro para APIs REST, com ORM robusto,
  sistema de migrações e ecossistema de bibliotecas para IoT (paho-mqtt)
- DRF oferece serialização automática, autenticação plugável e paginação nativa —
  funcionalidades críticas para o endpoint de histórico de diagnósticos
- SimpleJWT implementa o padrão RFC 7519 (JSON Web Tokens), sem estado no servidor,
  compatível com autenticação mobile (Flutter)
- PostgreSQL 15 oferece tipos JSON nativos, suporte a multi-tenant e performance
  superior ao SQLite para dados de séries temporais de sensores

---

## 7. App Mobile — Flutter

### Decisão
Usar **Flutter (Dart)** com **Drift** para cache SQLite local.

### Justificativa
- Flutter permite geração de APK Android e iOS a partir de um único codebase,
  reduzindo o esforço de desenvolvimento para um projeto de TCC individual
- Dart é compilado para código nativo (ARM), sem bridge JS como React Native —
  performance superior para renderização de listas de histórico e câmera
- **Drift** (antes Moor) é o ORM SQLite mais maduro para Flutter, permitindo
  que o app funcione **offline** e sincronize ao reconectar — requisito do
  Ceres para uso em áreas rurais sem conectividade constante

### 7.1 Design System — Taxonomia Viva (Sprint 3.5)

#### Material 3

O Ceres utiliza **Flutter Material 3** como sistema de componentes base.
A escolha de M3 sobre M2 se justifica pela:
- Suporte nativo a `NavigationBar`, `ColorScheme` semântico e `DynamicColor`
- API de temas unificada (`ThemeData`) com `useMaterial3: true`
- Compatibilidade com `NavigationBar` customizada (linha indicadora no topo
  em vez do indicador pill padrão do M3 — mais próximo da linguagem visual do projeto)

#### Paleta Cerrado (OKLCH → sRGB)

As cores foram derivadas do cerrado mato-grossense usando o espaço de cor
**OKLCH** (perceptualmente uniforme) e convertidas para hex sRGB para uso no Flutter.
A escolha de OKLCH garante que incrementos idênticos em luminância (`L`) produzam
diferenças perceptuais iguais — relevante para os tokens de urgência
(blight/dryGrass/leafLive) usados como indicadores clínicos de severidade.

Referência: BJÖRN Ottosson, "A perceptually uniform color space for image processing",
2020. Disponível em: https://bottosson.github.io/posts/oklab/

#### Tipografia

| Família | Uso no app | Justificativa |
|---|---|---|
| **Newsreader** (Google Fonts) | Nomes de doenças, valores sensor, títulos | Serifa de texto com boa legibilidade em telas pequenas; remete ao caderno botânico |
| **IBM Plex Sans** | Corpo de texto, botões, rótulos | Família técnica humanista, legível em tamanhos pequenos (8-13px) |
| **IBM Plex Mono** | Timestamps, porcentagens, dados técnicos | Alinhamento tabular de dados numéricos sem font-feature-settings manual |

A combinação Newsreader + IBM Plex é documentada na literatura de design editorial
como eficaz para interfaces que combinam conteúdo científico e leitura rápida
(LUPTON, Ellen. *Thinking with Type*. 2ª ed. Princeton Architectural Press, 2010).

#### Bibliotecas de UI adicionadas

| Pacote | Versão | Justificativa |
|---|---|---|
| `google_fonts` | ^6.2.1 | Acesso às fontes Newsreader e IBM Plex via CDN/cache local. Alternativa (bundled fonts) descartada por tamanho do APK |
| `flutter_native_splash` | ^2.4.6 | Gera splash screen nativo Android/iOS a partir de um PNG, evitando flash branco no carregamento. Padrão recomendado pela documentação Flutter |
| `flutter_launcher_icons` | ^0.14.3 | Gera todos os tamanhos de ícone Android/iOS a partir de um único PNG 1024×1024 |
| `flutter_svg` | ^2.0.10 | Renderização nativa de SVG no Flutter — necessário para fidelidade pixel-perfect com os ícones thin-stroke do design HTML (stroke-width 1.6). A alternativa (Material Icons) usa iconografia preenchida/arredondada incompatível com o design system Taxonomia Viva. `SvgTheme.currentColor` permite colorização dinâmica sem manipulação de string |

---

## 8. Gap Laboratorio-Campo e Background Augmentation

### Contexto

A avaliacao do modelo `ceres_mobilenetv2_int8.tflite` no PlantDoc
(campo real) em 2026-05-08 resultou em **20,77% de acuracia** contra
**98,13%** no test set PlantVillage (condicoes controladas).

Esse fenomeno e conhecido como **lab-to-field gap** e esta amplamente
documentado na literatura de visao computacional agricola.

### Evidencias na Literatura

| Paper | Resultado |
|---|---|
| Mohanty et al. (2016) | CNN PlantVillage: 99,35% lab → ~31% campo |
| Singh et al. (2020) — PlantDoc | VGG16 sem adaptacao: 29,73% campo |
| Salman et al. (2025) — ViT-MoE | Transferencia PV→PlantDoc: 68% |
| Xu et al. (2024) | 99,72% PV → 41,81% campo (fundos complexos) |
| Xiang et al. (2026) | ResNet-50: queda de 67,7 pp entre lab e campo |

O resultado do Ceres (20,77%) e compativel com a faixa reportada para
transferencia cross-domain sem adaptacao de dominio (20–56%).

### Causa Principal Identificada

O PlantVillage foi fotografado com **folhas isoladas sobre fundo cinza
ou preto uniforme**. O modelo aprendeu o fundo como feature
discriminativa. Evidencia: classe `saudavel` obteve apenas 1,8% no
PlantDoc — folhas saudaveis em campo tem fundo verde natural, nao cinza.

### Solucao Adotada — Background Augmentation

**Decisao:** implementar `background_augment.py` que:
1. Remove o fundo das imagens PlantVillage com **rembg** (U2-Net)
2. Recompoe a folha segmentada sobre fundos naturais do PlantDoc
3. Gera dataset em `datasets/processed_field/train`

**Justificativa direta:** Singh et al. (2020), paper original do PlantDoc,
mostrou que apenas **recortar a folha do fundo** aumentou a acuracia de
29,73% para **70,53% (+40,8 pp)** sem mudar a arquitetura.

A estrategia inversa — inserir fundos naturais no treino — deve produzir
efeito equivalente, ensinando o modelo a focar na textura da folha,
nao no fundo.

**Alternativas consideradas e descartadas:**

| Alternativa | Razao do descarte |
|---|---|
| Mudar arquitetura (ResNet, ViT) | Incompativel com TinyML — modelos > 1MB |
| Domain Adversarial Training | Requer dados rotulados de campo real |
| Few-shot fine-tuning | Requer coleta de campo — Sprint 3 |
| GAN-based augmentation | Complexidade alta, artefatos frequentes |

**Background augmentation** e a unica tecnica que:
- Nao muda o tamanho do modelo final (ainda 639 KB INT8)
- Nao requer dados rotulados de campo
- Tem evidencia direta no paper do PlantDoc (+40,8 pp)
- E implementavel no hardware disponivel (RTX 3060 Ti, WSL2)

### Ferramenta — rembg (U2-Net)

`rembg` e uma biblioteca Python que implementa o modelo **U2-Net**
(Qin et al., 2020) para segmentacao de saliencia, especializado em
remocao de fundo. Retorna imagem RGBA com canal alpha como mascara
da regiao segmentada.

**Por que U2-Net e nao GrabCut (OpenCV)?**
- GrabCut: algoritmo classico, requer seed manual ou caixa delimitadora
- U2-Net: rede neural treinada para remocao automatica sem seed
- Qualidade da mascara U2-Net significativamente superior para objetos organicos
- rembg oferece multiplos modelos (u2net, isnet-general-use, silueta)

### Resultado Esperado

Retreinar MobileNetV2 com `processed_field` (PlantVillage + fundos naturais)
deve elevar a acuracia no PlantDoc de **20,77% para 50–65%** (estimativa
baseada em resultados de tecnicas similares na literatura).

Meta definida: atingir **> 70%** no PlantDoc apos retreino (compativel
com estado da arte para modelos de porte similar).

### Referencias

- SINGH, D. et al. **PlantDoc: A Dataset for Visual Plant Disease Detection**.
  *ACM CoDS-COMAD*, 2020. DOI: 10.1145/3371158.3371196

- MOHANTY, S. P.; HUGHES, D. P.; SALATHE, M. **Using deep learning for image-based
  plant disease detection**. *Frontiers in Plant Science*, v. 7, p. 1419, 2016.
  DOI: 10.3389/fpls.2016.01419

- QIN, X. et al. **U2-Net: Going deeper with nested U-structure for salient object detection**.
  *Pattern Recognition*, v. 106, p. 107404, 2020.
  DOI: 10.1016/j.patcog.2020.107404

- SALMAN, Z. et al. **Plant disease classification in the wild using vision
  transformers and mixture of experts**. *Frontiers in Plant Science*, 16, 2025.
  DOI: 10.3389/fpls.2025.1522985

- XU, M. et al. **Plant disease recognition datasets in the age of deep learning:
  challenges and opportunities**. *Frontiers in Plant Science*, 15, 2024.
  DOI: 10.3389/fpls.2024.1452551

- YANG, S. et al. **From laboratory to field: cross-domain few-shot learning
  for crop disease identification**. *Frontiers in Plant Science*, 15, 2024.
  DOI: 10.3389/fpls.2024.1434222

- WU, X. et al. **From Laboratory to Field: Unsupervised Domain Adaptation
  for Plant Disease Recognition in the Wild**. *Plant Phenomics*, 2023.
  DOI: 10.34133/plantphenomics.0038

---

## Resumo das Decisões

| Componente        | Escolha                  | Principal alternativa descartada | Razão |
|-------------------|--------------------------|----------------------------------|-------|
| Modelo IA         | MobileNetV2 INT8         | ResNet-50                        | RAM: 100MB vs < 4MB no MCU |
| Dataset           | PlantVillage CC BY 4.0   | Roboflow Tomato Fruit            | Domínio errado (fruto vs folha) |
| Augmentation      | Offline (Pillow)         | Online (Keras)                   | Compatibilidade Edge Impulse |
| Split             | 70/15/15 estratificado   | 80/20                            | Val e test equilibrados |
| Inferência        | TinyML edge (ESP32-S3)   | API de visão em nuvem            | Offline, latência, custo |
| Protocolo IoT     | MQTT (Mosquitto)         | HTTP REST                        | Overhead 400x menor |
| Plataforma ML     | Edge Impulse             | TF/Keras manual                  | Export TFLite integrado |
| Backend           | Django REST + PostgreSQL | FastAPI + SQLite                 | ORM, migrações, paho-mqtt |
| App               | Flutter + Drift          | React Native                     | Performance nativa + offline |
| Gap lab-campo     | Background Augmentation (rembg) | Domain adversarial training | Nao requer dados campo; nao altera tamanho final do modelo |
| Broker MQTT cloud | HiveMQ Cloud (TLS 8883 + WS 8884) | Mosquitto self-hosted | Gratuito até 100 conexões, TLS nativo, WS para PaaS, sem infra própria |
| Deploy backend    | Railway (Docker + SQLite) | AWS EC2 / Heroku | Deploy automático via GitHub, $5 crédito gratuito |
| Inferência mobile | tflite_flutter 0.12.1 (on-device) | API cloud-only | Funciona offline, latência < 1s, sem custo por requisição |
