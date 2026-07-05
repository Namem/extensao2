# Ceres Diagnóstico

**Sistema embarcado TinyML para detecção precoce de doenças no tomateiro**

Engenharia da Computação · IFMT Cuiabá · 2026
Autor: **Namem Rachid Jaudy Neto**

---

## Visão Geral

O Ceres Diagnóstico classifica 10 categorias foliares do tomateiro (9 doenças + saudável) usando um modelo MobileNetV2 INT8 de 638 KB que roda diretamente no microcontrolador ESP32-S3 — sem internet, sem servidor. O mesmo modelo também executa no Android (offline) e via API Django (online).

```
Folha de tomate
      │
      ├──────────────────────────────────────────────────────┐
      ▼                          ▼                           ▼
 ① Edge — ESP32-S3        ② Mobile — Android         ③ Cloud — Django
  TFLite Micro              tflite_flutter              API Railway
  692 ms · offline          ~60 ms · offline            ~300 ms · HTTPS
  MQTT/TLS → HiveMQ         sem servidor                PostgreSQL
      │                                                      │
      └──────────────────────────┬───────────────────────────┘
                                 ▼
                     MobileNetV2 INT8 · 638 KB
                     96×96 · 10 classes · T=0,25
```

---

## Resultados

### Modelo (Experimento E — Focal Loss γ=2)

| Métrica | Valor |
|---|---|
| Acurácia lab (float) — PlantVillage test set (2.734 imgs) | **98,43%** |
| Acurácia lab (INT8 embarcado) | **95,76%** |
| Acurácia campo real (PlantDoc / documentada) | **20–30%** |
| Macro F1-Score | **0,9791** |
| Tamanho do modelo INT8 | **638 KB** |
| Latência ESP32-S3 (Xtensa LX7, 240 MHz) | **692 ms ±1 ms** |
| Latência on-device (Android) | **~60 ms** |
| Arena PSRAM usada | **200 KB / 512 KB (39%)** |

### 5 Experimentos de Treinamento

| Exp | Estratégia | PlantVillage | PlantDoc |
|---|---|---|---|
| A | Edge Impulse, sem calibração INT8 | 62,0% INT8 | — |
| B | TF local + calibração INT8 (50 batches) | 98,13% / 95,76% INT8 | 20,77% |
| C | Exp B + aug. sintética rembg U2-Net | 96,20% | 20,24% ❌ |
| D | Exp B + fine-tuning PlantDoc real | 97,55% | 30,43% ✅ |
| **E** ★ | **Exp D + Focal Loss γ=2** | **98,43%** | **30,43%** ✅ |

> **Lição principal:** a augmentation sintética foi ineficaz (Exp C). Fine-tuning com imagens reais de campo (+10 pp) superou 177 mil composições sintéticas. O gap laboratório-campo (98% → 20–30%) é um fenômeno estrutural documentado na literatura.

---

## As 10 Classes

| Código | Doença | Urgência |
|---|---|---|
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

Dataset: **PlantVillage** (Hughes & Salathé 2015) — 18.160 imagens · CC BY 4.0
Split estratificado seed=42 · augmentation offline x6 → 88.949 imagens de treino

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Hardware embarcado | ESP32-S3 N16R8 · 240 MHz · 16 MB Flash · 8 MB PSRAM |
| IA embarcada | TFLite Micro + MobileNetV2 alpha=0,35 · 96×96 · INT8 calibrado |
| Firmware | PlatformIO + framework Arduino |
| IoT / Mensageria | MQTT · HiveMQ Cloud (TLS 8883 / WebSocket 8884) · QoS 1 |
| Backend | Django + Django REST Framework + SimpleJWT |
| Banco de dados | PostgreSQL 18 (porta 5433) |
| Deploy | Railway (auto-deploy via GitHub push) |
| App mobile | Flutter + Dart · tflite_flutter |
| Cache offline | Drift (SQLite) + SyncService |
| Mapa | OpenStreetMap via flutter_map + geolocator |
| Treinamento | TensorFlow 2 + Python 3.12 + WSL2 + RTX 3060 Ti (8 GB) |

---

## Estrutura do Repositório

```
ceres-diagnostico/
├── app_ceres/               # Aplicativo Flutter
│   └── lib/
│       ├── screens/         # Diagnóstico · Mapa · IoT · Enciclopédia · Perfil
│       ├── widgets/         # CeresAppBar · OfflineBanner · CeresSvgIcon
│       ├── services/        # ApiService · AuthStorage · InferenceLocalService
│       ├── models/          # ResultadoInferencia · EventoMqtt
│       ├── data/            # DoencaInfo — dados das 10 classes (Embrapa)
│       ├── database/        # Drift — cache SQLite + SyncService offline-first
│       └── theme/           # CeresColors — paleta Taxonomia Viva
│
├── backend/                 # API Django REST
│   ├── ceres_core/          # Settings · URLs · settings_railway.py
│   ├── diagnostico/         # Models · Views · Serializers · mqtt_listener
│   ├── accounts/            # CustomUser · /api/auth/me/ · /api/auth/register/
│   ├── inferir_worker.py    # Worker TFLite (subprocess)
│   ├── scripts/testes/      # Smoke tests do motor de inferência
│   └── datasets/
│       ├── scripts/         # prepare_plantvillage.py · train_local.py · export_tflite.py
│       └── modelo/          # ceres_expe_int8.tflite (638 KB — modelo final Exp E)
│
├── firmware/
│   ├── esp32s3_ceres/       # TFLite Micro no ESP32-S3 (PlatformIO)
│   └── esp32_mqtt_sensor/   # Firmware MQTT + DHT22 + sensor de solo
│
├── docs/
│   ├── extensao/            # Relatório Final da Extensão (PDF/DOCX) + anexos
│   ├── core/                # BACKLOG.md · RELATORIO_TECNICO.md · FUNDAMENTACAO_TECNICA.md
│   └── resultados/          # Benchmarks · matriz de confusão · validações de campo
│
├── verificar_ambiente.py    # Checklist de ambiente com apito sonoro
└── .env.example             # Variáveis de ambiente necessárias
```

---

## Como Executar

### Pré-requisitos
- Python 3.13 (Windows) + Python 3.12 (WSL2 para treinamento)
- Flutter 3.x + Dart
- PostgreSQL 18 (porta 5433) — opcional (há modo SQLite)
- PlatformIO (para firmware ESP32)

### 1 — Backend Django
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-backend.txt

cp .env.example .env           # editar com suas credenciais
python manage.py migrate
python manage.py runserver 8000
# Em outra janela — listener MQTT:
python manage.py mqtt_listener
```

### 2 — App Flutter
```bash
cd app_ceres
flutter run -d windows          # desktop
# Android — editar lib/config.dart com o IP do servidor na rede local:
# static const String baseUrl = 'http://192.168.X.X:8000';
flutter run -d android
```

### 3 — Firmware ESP32-S3 (PlatformIO)
```bash
cd firmware/esp32s3_ceres
# Copiar include/config.h.example -> include/config.h e ajustar SSID, senha WiFi e broker MQTT
pio run --target upload
pio device monitor --baud 115200
```

### 4 — Verificação de Ambiente
```bash
python verificar_ambiente.py             # PC desktop
python verificar_ambiente.py --notebook  # Notebook (foco em WiFi + ESP32)
```
1 bipe = tudo OK · 2 bipes = avisos · 5 bipes = erro crítico

---

## API — Principais Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/api/auth/token/` | Login — retorna access + refresh JWT |
| POST | `/api/auth/token/refresh/` | Renovar access token |
| GET | `/api/auth/me/` | Perfil + estatísticas do usuário |
| POST | `/api/auth/register/` | Criar conta (Produtor ou Agrônomo) |
| POST | `/api/diagnostico/inferir/` | Imagem → classe + confiança (+ GPS) |
| GET | `/api/diagnostico/historico/` | Eventos paginados (app + IoT) |
| GET | `/api/diagnostico/sensor/` | Última leitura de sensor do ESP32 |

**Deploy de produção:** `https://ceres.up.railway.app`

---

## Sprints Concluídas

| Sprint | Tema | Status |
|---|---|---|
| Sprint 0 | API Django + JWT + PostgreSQL | ✅ |
| Sprint 1 | MQTT + Dataset + 5 Experimentos IA (Exp A→E) | ✅ |
| Sprint 1b | Firmware ESP32-S3 WiFi + MQTT | ✅ |
| Sprint 2 | TFLite Micro no ESP32-S3 · 692 ms · 638 KB | ✅ |
| Sprint 3 | Flutter + API Django + Cache Offline Drift | ✅ |
| Sprint 3.5 | Design System Taxonomia Viva + telas completas | ✅ |
| Sprint 3.6 | Fidelidade pixel-perfect ao design | ✅ |
| Sprint 3.7 | Design Refresh + MQTT Cloud (HiveMQ) + Deploy | ✅ |
| Sprint 4A | Back button + Persistência JWT + Banner Offline | ✅ |
| Sprint 4B | Mapa OpenStreetMap + GPS | ✅ |
| Sprint 5 | Tela Perfil + `/api/auth/me/` + cadastro | ✅ |
| Sprint 5B | Robustez backend + Sync Offline + PostgreSQL Railway | ✅ |

---

## Licença

Projeto acadêmico — IFMT Cuiabá · 2026.
Dataset PlantVillage: CC BY 4.0 (Hughes & Salathé, 2015).
Código: uso acadêmico e de pesquisa.
