# Manual de Instalação — Ceres Diagnóstico

**Atividade de Extensão II — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto
**Repositório:** https://github.com/Namem/extensao2

Guia para instalar e executar o sistema completo: **Backend Django**, **App Flutter**
e **Firmware ESP32-S3**. Testado em Windows 11.

---

## 1. Pré-requisitos

| Software | Versão | Usado para |
|---|---|---|
| Git | qualquer | Clonar o repositório |
| Python | 3.13 (Windows) / 3.12 (WSL2) | Backend Django + treino |
| PostgreSQL | 18 (porta 5433) — *opcional* | Banco de produção local (ou SQLite) |
| Flutter SDK | 3.44+ | App mobile/desktop |
| Visual Studio Build Tools | 2022+ (workload "Desktop C++") | Build do Flutter no Windows |
| PlatformIO | 6.1+ (extensão VS Code) | Firmware ESP32 |
| Mosquitto | 2.1+ — *opcional* | Broker MQTT local |

> Para treinar o modelo (opcional) é necessário WSL2 + GPU NVIDIA com CUDA.

---

## 2. Clonar o projeto

```bash
git clone https://github.com/Namem/extensao2 ceres-diagnostico
cd ceres-diagnostico
```

---

## 3. Backend — Django REST API

### 3.1 Ambiente virtual e dependências

```powershell
cd backend
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Banco de dados

**Opção A — SQLite (mais simples, recomendado para testes):**
usa `settings_notebook.py`, sem configuração extra.

**Opção B — PostgreSQL 18 (porta 5433):**
```powershell
$env:PGPASSWORD = "<senha-postgres>"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 -c "CREATE USER ceres_user WITH PASSWORD 'ceres_senha_local';"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 -c "CREATE DATABASE ceres_db OWNER ceres_user;"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 -c "ALTER USER ceres_user CREATEDB;"
```

### 3.3 Variáveis de ambiente

Copie `backend/.env.example` para `backend/.env` e ajuste (SECRET_KEY, banco,
MQTT_BROKER, ALLOWED_HOSTS). **Nunca commitar o `.env`.**

### 3.4 Migrations, testes e execução

```powershell
python manage.py migrate --settings=ceres_core.settings_notebook
python manage.py test diagnostico --verbosity=2
python manage.py runserver 0.0.0.0:8080 --settings=ceres_core.settings_notebook
```

A API sobe em **http://localhost:8080/api/**.

> **Atalho:** o script `iniciar.ps1` na raiz sobe Django + Flutter juntos.

### 3.5 Listener MQTT (opcional — dados IoT)

```powershell
python manage.py mqtt_listener --settings=ceres_core.settings_notebook
```

---

## 4. App — Flutter

```powershell
cd ..\app_ceres
flutter pub get
```

Ajuste o servidor em `lib/config.dart` (`baseUrl`):
- **Produção:** `https://ceres.up.railway.app`
- **Local (desktop):** `http://localhost:8080`
- **Emulador Android:** `http://10.0.2.2:8080`
- **Celular na mesma WiFi:** `http://192.168.X.X:8080`

Executar / gerar APK:
```powershell
flutter run -d windows        # desktop Windows
flutter build apk --release   # APK para celular
```

O APK sai em `build\app\outputs\flutter-apk\app-release.apk`.

---

## 5. Firmware — ESP32-S3 (sensores + MQTT)

```
firmware/esp32_mqtt_sensor/   → nó de sensores (DHT22 + solo) via MQTT
firmware/esp32s3_ceres/       → benchmark TFLite Micro (inferência embarcada)
```

### 5.1 Configuração

Copie `include/config.h.example` para `include/config.h` e ajuste:
```cpp
#define WIFI_SSID     "SuaRede"
#define WIFI_PASSWORD "SuaSenha"
#define MQTT_BROKER   "ee2c89bab...s1.eu.hivemq.cloud"   // HiveMQ Cloud
#define MQTT_PORT     8883
```
O `config.h` é ignorado pelo Git (contém segredos).

### 5.2 Gravar (PlatformIO)

```bash
cd firmware/esp32_mqtt_sensor
pio run --target upload --upload-port COM5
pio device monitor           # acompanhar a saída serial
```

> Placa: `esp32-s3-devkitc-1` · Flash 16MB · framework Arduino.
> Fazer no **notebook** (mesma rede WiFi do ESP32).

---

## 6. MQTT — Broker

| Cenário | Broker | Portas |
|---|---|---|
| Local (dev) | Mosquitto 2.1 | 1883 (TCP) |
| Nuvem (prod) | HiveMQ Cloud | 8883 (TLS) / 8884 (WebSocket) |

Mosquitto local: configurar `listener 1883` + `allow_anonymous true`.

---

## 7. Deploy (produção — Railway)

- Deploy automático via `git push` na branch `main`.
- `DJANGO_SETTINGS_MODULE=ceres_core.settings_railway` (PostgreSQL via `DATABASE_URL`).
- Variáveis MQTT: `CERES_BROKER`, `CERES_TLS`, `MQTT_PORT=8884`, `MQTT_USER`, `MQTT_PASSWORD`, `MQTT_WEBSOCKET=true`.
- URL: **https://ceres.up.railway.app** · Conta de teste: `test@test.com` / `test123`.

---

## 8. Modelos de IA (TFLite)

| Arquivo | Exp | Tamanho | Onde roda |
|---|---|---|---|
| `backend/datasets/modelo/ceres_expe_int8.tflite` | Exp E | 638 KB | Backend + App (on-device) |
| `backend/datasets/modelo/ceres_mobilenetv2_int8.tflite` | Exp B | 639 KB | ESP32-S3 (TFLite Micro) |

O caminho do modelo do backend é definido por `TFLITE_MODEL_PATH` em `settings*.py`.

---

## 9. Verificação do ambiente

```bash
python verificar_ambiente.py --notebook   # checklist + apito sonoro
python verificar_ambiente.py --fix        # tenta corrigir automaticamente
```
