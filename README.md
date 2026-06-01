# Ceres Diagnóstico

**Sistema embarcado de detecção precoce de doenças em folhas de tomateiro**

TCC — Engenharia da Computação · IFMT Cuiabá · 2026  
Autor: **Namem Rachid Jaudy Neto**

---

## Visão Geral

O Ceres Diagnóstico é um sistema completo de diagnóstico fitossanitário voltado a produtores de tomate do Cerrado (região de Sorriso-MT). Integra inteligência artificial embarcada, comunicação IoT e aplicativo mobile em uma única plataforma.

```
Folha de tomate
      │
      ▼
 [ESP32-S3]  ──TFLite Micro──▶  Classificação local (638 KB, < 300 ms)
      │
      │ MQTT (JSON)
      ▼
 [Django REST]  ──────────────▶  Persistência + inferência via API
      │
      │ HTTP / WebSocket
      ▼
 [Flutter App]  ──────────────▶  Diagnóstico · Mapa · Histórico IoT · Enciclopédia · Perfil
```

### 10 classes detectadas

| Código | Doença | Urgência |
|--------|--------|----------|
| D01 | Requeima (*Phytophthora infestans*) | 🔴 URGENTE |
| D06 | Vira-cabeça (TSWV) | 🔴 URGENTE |
| D06b | Mosaico (ToMV) | 🔴 URGENTE |
| D09 | Mancha Bacteriana (*Xanthomonas vesicatoria*) | 🔴 URGENTE |
| D02 | Septoriose (*Septoria lycopersici*) | 🟡 MODERADO |
| D03 | Pinta Preta (*Alternaria solani*) | 🟡 MODERADO |
| D03b | Mancha Alvo (*Corynespora cassiicola*) | 🟡 MODERADO |
| D05 | Mofo Foliar (*Passalora fulva*) | 🟡 MODERADO |
| D07 | Ácaro Bronzeamento (*Aculops lycopersici*) | 🟡 MODERADO |
| S00 | Saudável | 🟢 NORMAL |

---

## Resultados do Modelo (Experimento E — Modelo Final)

| Métrica | Valor |
|---------|-------|
| Acurácia lab (PlantVillage test) | **98,43%** |
| Macro F1-Score | **0,9791** |
| Acurácia campo (PlantDoc) | **~67%** |
| Tamanho do modelo INT8 | **638 KB** |
| Latência ESP32-S3 | **< 300 ms** |
| RAM livre (PSRAM) | **> 4 MB** |

Dataset: PlantVillage — 18.160 imagens · 10 classes · CC BY 4.0 (Hughes & Salathé, 2015)

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Hardware | ESP32-S3 N16R8 (16 MB Flash + 8 MB PSRAM) |
| Câmera | OV5640 5MP |
| IA Embarcada | TFLite Micro + MobileNetV2 96×96 INT8 |
| Backend | Django 5 + Django REST Framework + SimpleJWT |
| Banco de Dados | PostgreSQL 18 (porta 5433) |
| IoT | MQTT (Mosquitto 2.x) |
| App Mobile | Flutter 3 + Dart |
| Cache Local | Drift (SQLite) |
| Mapa | OpenStreetMap via flutter_map |
| Treinamento | TensorFlow 2 + WSL2 + RTX 3060 Ti |

---

## Estrutura do Repositório

```
ceres-diagnostico/
├── app_ceres/              # Aplicativo Flutter
│   ├── lib/
│   │   ├── screens/        # 5 telas: Diagnóstico, Mapa, IoT, Enciclopédia, Perfil
│   │   ├── widgets/        # CeresAppBar, OfflineBanner, CeresSvgIcon
│   │   ├── services/       # ApiService, AuthStorage
│   │   ├── models/         # ResultadoInferencia, EventoMqtt
│   │   ├── data/           # DoencaInfo — dados das 10 classes (Embrapa)
│   │   ├── database/       # Drift — cache SQLite offline
│   │   └── theme/          # CeresColors — paleta Taxonomia Viva
│   └── android/            # Manifests + permissões
│
├── backend/                # API Django REST
│   ├── ceres_core/         # Settings, URLs raiz
│   ├── diagnostico/        # Models, Views, Serializers, MQTT consumer
│   ├── accounts/           # CustomUser, endpoint /api/auth/me/
│   └── datasets/
│       ├── scripts/        # prepare_plantvillage.py, train_local.py, export_tflite.py
│       └── modelo/         # ceres_expe_int8.tflite (modelo final, 638 KB)
│
├── firmware/
│   ├── esp32s3_ceres/      # TFLite Micro no ESP32-S3 (PlatformIO)
│   └── esp32_mqtt_sensor/  # Firmware MQTT com sensores DHT22
│
├── docs/
│   ├── core/               # TCC_CERES.md, RELATORIO_TECNICO.md, BACKLOG.md
│   └── resultados/         # Benchmarks, validação PlantDoc
│
├── verificar_ambiente.py   # Checklist de ambiente com apito sonoro
└── CLAUDE.md               # Contexto do projeto para Claude Code
```

---

## Como Executar

### Pré-requisitos

- Python 3.13
- Flutter 3.x + Dart
- PostgreSQL 18 (porta 5433)
- Mosquitto 2.x
- PlatformIO (para firmware)

### 1 — Backend Django

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-backend.txt

# Configurar banco
cp .env.example .env           # editar com suas credenciais
python manage.py migrate
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver 8000
```

### 2 — MQTT (Mosquitto)

```bash
# Windows — serviço sobe automaticamente
# Verificar: sc query mosquitto

# Linux/Mac
mosquitto -c mosquitto.conf
```

### 3 — App Flutter

```bash
cd app_ceres

# Desenvolvimento no PC (Windows)
flutter run -d windows

# Android (celular conectado via USB)
# Editar lib/config.dart: baseUrl → IP do servidor na rede local
flutter run -d android
```

### 4 — Firmware ESP32-S3 (PlatformIO)

```bash
cd firmware/esp32s3_ceres
pio run --target upload
pio device monitor --baud 115200
```

---

## Configuração de Rede (Notebook + Android + ESP32)

Editar `app_ceres/lib/config.dart`:

```dart
// Trocar localhost pelo IP do servidor na rede WiFi
static const String baseUrl = 'http://192.168.X.X:8000';
```

Descobrir o IP:
```bash
ipconfig   # Windows → "Endereço IPv4"
```

---

## API — Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/token/` | Login — retorna JWT |
| POST | `/api/auth/token/refresh/` | Renovar access token |
| GET | `/api/auth/me/` | Perfil + estatísticas do usuário |
| POST | `/api/diagnostico/inferir/` | Enviar imagem → classe + confiança |
| GET | `/api/diagnostico/historico/` | Eventos MQTT paginados |

---

## Verificação de Ambiente

```bash
python verificar_ambiente.py           # PC
python verificar_ambiente.py --notebook  # Notebook (foco em WiFi + ESP32)
python verificar_ambiente.py --wsl       # + GPU WSL2
```

Saída: 1 bipe = tudo OK · 2 bipes = avisos · 5 bipes = erro crítico

---

## Sprints Concluídas

| Sprint | Tema | Status |
|--------|------|--------|
| Sprint 0 | API Django + JWT + PostgreSQL | ✅ |
| Sprint 1 | MQTT + Dataset + 5 Experimentos IA | ✅ |
| Sprint 1b | Firmware ESP32-S3 WiFi + MQTT | ✅ |
| Sprint 2 | TFLite Micro no ESP32-S3 (sem câmera) | ✅ |
| Sprint 3 | Flutter + API Django + Cache Offline | ✅ |
| Sprint 3.5 | Design System Taxonomia Viva + 5 Telas | ✅ |
| Sprint 3.6 | Fidelidade pixel-perfect ao design HTML | ✅ |
| Sprint 4A | Back button + Persistência + Banner Offline | ✅ |
| Sprint 4B | Mapa OpenStreetMap + GPS | ✅ |
| Sprint 5 | Tela Perfil + `/api/auth/me/` | ✅ |
| Sprint 6 | TCC Final + Defesa | ⏳ |

---

## Licença

Projeto acadêmico — IFMT Cuiabá · 2026.  
Dataset PlantVillage: CC BY 4.0 (Hughes & Salathé, 2015).  
Fundamentação técnica: Embrapa Hortaliças — Manual de Pragas e Doenças do Tomateiro (2023).
