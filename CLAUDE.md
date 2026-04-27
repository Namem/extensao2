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
Backend : Django REST + PostgreSQL 15 (Docker :5433)
          + SimpleJWT + paho-mqtt (a adicionar)
App     : Flutter + Dart + Drift (cache SQLite)
Hardware: ESP32-S3 N16R8 + OV5640 5MP (a comprar)
          ESP32 genérico (disponível agora)
IoT     : MQTT Mosquitto + broker local
AI      : TFLite Micro + Edge Impulse
          Modelo: MobileNetV2 INT8 quantizado

## Dataset oficial do projeto
PRIMARY  : PlantVillage (Hughes & Salathé 2015)
           ~18.160 imagens de folha de tomate
           10 classes + saudável — CC BY 4.0
           Kaggle: abdallahalidev/plantvillage-dataset
EXTRA    : New Plant Diseases Dataset (Kaggle)
           ~22.900 imgs já augmentadas — CC BY 4.0
VALIDAÇÃO: PlantDoc (~500 imgs campo real)
NÃO USAR : Roboflow "Tomato Fruit Disease Detection"
           (Object Detection de fruto, 5 classes —
           incompatível com a tarefa do Ceres)

## As 10 doenças do Ceres (base Embrapa)
D1  Requeima          (Phytophthora infestans)
D2  Septoriose        (Septoria lycopersici)
D3  Pinta-Preta       (Alternaria solani)
D4  Traça-do-Tomateiro(Tuta absoluta)
D5  Mosca-Branca      (Bemisia tabaci)
D6  Tripes/Vira-Cabeça(Frankliniella + Tospovírus)
D7  Ácaro-do-Bronzeamento
D8  Murcha-Bacteriana (Ralstonia solanacearum)
D9  Mancha-Bacteriana (Xanthomonas spp.)
D10 Broca-Pequena     (Neoleucinodes elegantalis)

## Estado atual das sprints
Sprint 0: CONCLUÍDA — API Django + Motor IA + JWT
Sprint 1: EM ANDAMENTO — MQTT + dataset + treino
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

## Estrutura de pastas
backend/       → Django REST API
app_ceres/     → Flutter
firmware/      → ESP32 (criar na Sprint 2)
datasets/      → scripts de treino e dados
docs/          → relatórios, artigo, benchmarks
Pre_arquivos/  → artefatos pré-existentes (não editar)
