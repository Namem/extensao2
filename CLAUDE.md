# Ceres Diagnóstico — Contexto para Claude Code

## Projeto
TCC de Engenharia da Computação — IFMT (Sorriso-MT).
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

## Experimentos de treinamento (Sprint 1)
Dois experimentos paralelos para comparação no artigo:

Exp A — Edge Impulse (nuvem):
  Projeto: ceres-diagnostico (Developer gratuito, privado)
  API Key: em backend/.env (EDGE_IMPULSE_API_KEY) — nunca commitar
  Dataset: 88.949 imgs (train) + 2.719 (val) via upload_edge_impulse.py
  Modelo: MobileNetV2 96x96 0.35 INT8
  Limite: 60 min/job

Exp B — TensorFlow local (WSL2):
  Ambiente: WSL2 Ubuntu, Python 3.12, ~/venv_ceres/
  GPU: RTX 3060 Ti via tensorflow[and-cuda]
  Dataset: 88.949 imgs augmentadas
  Script: backend/datasets/scripts/train_local.py (a criar)

## Estado atual das sprints
Sprint 0: CONCLUIDA — API Django + Motor IA + JWT (5/5 testes)
Sprint 1: EM ANDAMENTO — MQTT + dataset + treino
  - [x] Dataset PlantVillage baixado e processado (88.949 imgs)
  - [x] Upload Edge Impulse iniciado (Exp A)
  - [x] WSL2 + TF local sendo configurado (Exp B)
  - [ ] Treinamento Exp A concluido
  - [ ] Treinamento Exp B concluido
  - [ ] Firmware ESP32 MQTT
Sprint 2: PENDENTE — deploy TFLite no ESP32-S3
Sprint 3: PENDENTE — integração MQTT-Ceres completa
Sprint 4: PENDENTE — Flutter + experimentos
Sprint 5: PENDENTE — artigo + defesa

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
