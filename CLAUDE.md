# Ceres Diagnóstico — Contexto para Claude Code

## Projeto
TCC de Engenharia da Computação — IFMT Cuiabá.
Sistema embarcado de detecção precoce de doenças no
tomateiro: ESP32-S3 TinyML + Django REST + Flutter.
Autor: Namem Rachid Jaudy Neto

## Pasta de artefatos pré-existentes
Pre_arquivos/ (dentro da raiz do projeto) contém:
- SprintReview_1_CeresDiagnostico.pptx (Sprint 0)
- Backlog Projeto Ceres Diagnóstico V2.xlsx (backlog)
- guia_sprint_review.pdf
Antes de criar ou atualizar qualquer documentação,
SEMPRE leia o backlog existente nessa pasta.

## Stack
Backend : Django REST + PostgreSQL 18 (porta 5433, instalado direto no Windows)
          + SimpleJWT + paho-mqtt
App     : Flutter + Dart + Drift (cache SQLite)
Hardware: ESP32-S3 N16R8 + OV5640 5MP (a comprar)
          ESP32 genérico (disponível agora)
IoT     : MQTT Mosquitto + broker local
AI      : TFLite Micro + Edge Impulse (Exp A) + TensorFlow local WSL2 (Exp B)
          Modelo: MobileNetV2 96x96 INT8 quantizado

## Ambiente de desenvolvimento
Windows 11 + Python 3.13 (Windows) + Python 3.12 (WSL2 Ubuntu)
PostgreSQL 18.3.3 instalado direto na porta 5433 (sem Docker)
Docker Desktop instalado mas com problemas — não usar por enquanto
WSL2 Ubuntu rodando com RTX 3060 Ti acessível via nvidia-smi
venv do backend em: backend/venv/ (Windows, Python 3.13)
venv do treino em: ~/venv_ceres/ (WSL2, Python 3.12)
GPU local: NVIDIA RTX 3060 Ti 8GB VRAM, CUDA 13.2

## Repositório
https://github.com/Namem/extensao2
Fluxo: git push (PC atual) → GitHub → git pull (outro PC)
Commits: apenas o autor commita — Claude só sugere o comando

## Dataset oficial do projeto
Sempre usar os melhores datasets disponíveis — novos podem ser
adicionados conforme necessidade, desde que documentados em
docs/FUNDAMENTACAO_TECNICA.md com justificativa e licença.

PRIMARY  : PlantVillage (Hughes & Salathé 2015)
           ~18.160 imagens de folha de tomate
           10 classes — CC BY 4.0
           Kaggle: abdallahalidev/plantvillage-dataset
           Processado em: backend/datasets/processed/train|val|test
           88.949 imgs de treino após augmentation offline (seed=42)
EXTRA    : New Plant Diseases Dataset (Kaggle) — CC BY 4.0
VALIDAÇÃO: PlantDoc (~500 imgs campo real)
NÃO USAR : Roboflow "Tomato Fruit Disease Detection"
           (Object Detection de fruto — incompatível com classificação de folhas)

## As 10 classes do Ceres (mapeamento PlantVillage → Ceres)
PlantVillage (pasta)                              → Código Ceres
Tomato___Bacterial_spot                           → D09_mancha_bacteriana
Tomato___Early_blight                             → D03_pinta_preta
Tomato___Late_blight                              → D01_requeima
Tomato___Leaf_Mold                                → D05_mofo_foliar
Tomato___Septoria_leaf_spot                       → D02_septoriose
Tomato___Spider_mites Two-spotted_spider_mite     → D07_acaro_bronzeamento
Tomato___Target_Spot                              → D03b_mancha_alvo
Tomato___Tomato_Yellow_Leaf_Curl_Virus            → D06_vira_cabeca
Tomato___Tomato_mosaic_virus                      → D06b_mosaico
Tomato___healthy                                  → saudavel

## Experimentos de treinamento (Sprint 1) — AMBOS CONCLUÍDOS

Exp A — Edge Impulse (nuvem) ✅ CONCLUÍDO:
  Projeto: ceres-diagnostico (Developer gratuito, privado)
  API Key: em backend/.env (EDGE_IMPULSE_API_KEY) — nunca commitar
  Dataset: 88.872 imgs aceitas pelo EI
  Modelo: MobileNetV2 96x96 0.35
  Resultados: FP32 92,5% val acc / INT8 62,0% val acc
  Tamanho: FP32 1.637KB / INT8 624KB
  Latência estimada ESP32-S3: 1.365ms (INT8), 4.322ms (FP32)
  Arquivos: backend/datasets/modelo/ei_ceres_fp32.tflite
            backend/datasets/modelo/ei_ceres_int8.tflite
  PROBLEMA: quantização INT8 automática sem representative_dataset
            causou queda de 30pp (92.5% → 62.0%)

Exp B — TensorFlow local (WSL2) ✅ CONCLUÍDO — MODELO ESCOLHIDO:
  Ambiente: WSL2 Ubuntu, Python 3.12, ~/venv_ceres/
  GPU: RTX 3060 Ti via tensorflow[and-cuda]
  LD_LIBRARY_PATH: salvo em ~/.bashrc (nvidia paths + /usr/lib/wsl/lib)
  Script treino: backend/datasets/scripts/train_local.py
  Script export: backend/datasets/scripts/export_tflite.py
  Fase 1: 10 epochs, LR=1e-3, backbone congelado
  Fase 2: 40 epochs, LR=5e-4, fine-tuning últimas 30 camadas
  Callbacks: EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
  Resultados: 98,13% test acc (2.734 imgs nunca vistas)
  Tamanho INT8: 639KB (com representative_dataset calibrado)
  Arquivos: backend/datasets/modelo/ceres_mobilenetv2_int8.tflite ← ESP32
             backend/datasets/modelo/best_fase2.keras (checkpoint época 28)
             backend/datasets/modelo/relatorio_final.txt (matriz confusão)

Por que Exp B > Exp A:
  1. Duas fases de treinamento (transfer learning correto)
  2. Quantização INT8 com 50 batches do val set para calibração
  3. EarlyStopping + ReduceLROnPlateau evitam overfitting

YOLO foi descartado: detector de objetos (bounding box), não classificador.
Incompatível com classificação de folha única. Tamanho mínimo ~6MB vs 639KB.

## Estado atual das sprints (2026-04-29)
Sprint 0: CONCLUIDA — API Django + Motor IA + JWT (5/5 testes)
Sprint 1: QUASE CONCLUIDA
  - [x] Dataset PlantVillage: 18.160 imgs → 88.949 imgs (augmentation x6)
  - [x] Exp A (Edge Impulse): FP32 92,5% / INT8 62,0% — documentado
  - [x] Exp B (TF local WSL2): 98,13% test acc, INT8 639KB — ESCOLHIDO
  - [x] Backend Django MQTT: DiagnosticoEvento + mqtt_listener + historico
  - [x] Mosquitto 2.1.2 instalado e testado (localhost:1883)
  - [x] 5/5 testes passando (inclui MQTT)
  - [ ] Firmware ESP32 genérico MQTT (precisa ESP32 genérico em mãos)
Sprint 2: PENDENTE — precisa ESP32-S3 N16R8 + OV5640 (a comprar)
  - Carregar ceres_mobilenetv2_int8.tflite no ESP32-S3
  - Medir latência real com esp_timer_get_time()
  - Benchmark 50 imgs: Python vs ESP32 (predições devem ser idênticas)
  - Testar PlantDoc (~500 imgs campo real, meta > 70%)
  - Loop completo: câmera → MQTT → Django → app
Sprint 3: PENDENTE — Flutter + artigo
Sprint 4+: PENDENTE — defesa

## Cadeia de validação do modelo (importante para defesa)
Nível 1 ✅ FEITO: Test set PlantVillage — 98,13% (2.734 imgs controladas)
Nível 2 ⏳ Sprint 2: Hardware real ESP32-S3 — latência real + comparação Python
Nível 3 ⏳ Sprint 2: PlantDoc — ~500 fotos campo real, meta > 70%
Nível 4 ⏳ Sprint 3: Produtores de Sorriso-MT — validação com usuários reais

## Mosquitto — como iniciar
  Windows: o serviço "mosquitto" sobe automaticamente
  Testar: python -c "import paho.mqtt.client as mqtt; ..."
  Config: C:\Program Files\mosquitto\mosquitto.conf
          (listener 1883 localhost / allow_anonymous true)

## Como retomar o treinamento WSL2 (se precisar retreinar)
  wsl
  source ~/venv_ceres/bin/activate
  # GPU já configurada no .bashrc
  python3 /mnt/c/.../backend/datasets/scripts/train_local.py
  # Se travar: usar export_tflite.py para exportar do checkpoint salvo

## Regras de código
- Python  : PEP8, docstrings em português
- Dart    : dart format, comentários em português
- C++     : PlatformIO, um arquivo por módulo
- Commits : Conventional Commits (feat/fix/chore/docs)
- Nunca commitar secrets — usar .env
- Claude NUNCA commita — apenas sugere o comando

## Regras de processo
- Antes de implementar: mostrar o que vai fazer e explicar como funciona
- Após cada implementação: fornecer passo a passo para testar
- Após cada bloco de mudanças: sugerir commit (sem co-autor Claude)
- Antes de criar documentação: ler backlog em Pre_arquivos/

## Regra de fundamentação técnica
SEMPRE que uma tecnologia, método, biblioteca ou arquitetura
for adicionada OU removida do projeto, atualizar:
  docs/FUNDAMENTACAO_TECNICA.md
com justificativa técnica, comparativo com alternativas e
referência acadêmica (Google Scholar, PMC, Springer, IEEE).
Obrigatório para a defesa do TCC.

## Documentos vivos (atualizar ao final de cada implementação)
docs/TCC_CERES.md             → rascunho do TCC, seções [PENDENTE] a preencher
docs/RELATORIO_TECNICO.md     → log cronológico de tudo implementado
docs/FUNDAMENTACAO_TECNICA.md → justificativa técnica + refs acadêmicas
SEMPRE atualizar os três ao final de cada sprint ou bloco significativo.

## Estrutura de pastas
backend/               → Django REST API + datasets/
backend/venv/          → venv Windows (Python 3.13)
backend/datasets/raw/  → dataset bruto Kaggle (nao commitar — .gitignore)
backend/datasets/processed/ → train|val|test (nao commitar — .gitignore)
backend/datasets/scripts/   → scripts Python (commitar)
app_ceres/             → Flutter
firmware/              → ESP32 (criar na Sprint 2)
docs/                  → TCC, relatório, fundamentação, benchmarks
Pre_arquivos/          → artefatos pré-existentes (nao editar)
