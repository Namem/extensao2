# Backlog do Produto — Ceres Diagnóstico
**TCC Engenharia da Computação — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto
**Última atualização:** 2026-05-08

> Backlog exclusivo do produto (software + firmware + hardware).
> Para escrita do TCC e artigo científico, veja [BACKLOG_ESCRITA.md](BACKLOG_ESCRITA.md).

---

## Sprint 0 — Motor de Diagnóstico ✅ CONCLUÍDA

**Critério de aceite:** API Django funcional com motor de inferência por árvore de decisão, autenticação JWT e testes passando.

- [x] Mapeamento técnico das 10 doenças do tomateiro (base Embrapa)
- [x] Models `Pergunta`, `Opcao`, `Diagnostico` criados e migrados
- [x] Endpoints `GET /api/diagnostico/iniciar/` e `POST /api/diagnostico/responder/`
- [x] Autenticação JWT configurada (SimpleJWT)
- [x] 3 testes automatizados passando
- [x] PostgreSQL 18.3.3 instalado direto na porta 5433 (sem Docker)
- [x] Multi-tenant (`Tenant`, `CustomUser`) estruturado
- [x] `.env` criado e `settings.py` lendo variáveis de ambiente

---

## Sprint 1 — MQTT + Dataset + Treino ✅ CONCLUÍDA (exceto firmware)

**Critério de aceite:** Django persistindo eventos MQTT com endpoint paginado,
dataset PlantVillage preparado, modelos treinados e validados.

> ⚠️ Firmware ESP32 movido para Sprint 1b — precisa de notebook (mesma rede WiFi)

### Backend Django MQTT ✅ CONCLUÍDO (2026-04-29)
- [x] `paho-mqtt` adicionado ao `requirements.txt`
- [x] Model `DiagnosticoEvento` + migration (device_id, classe_detectada, confianca, temperatura, umidade_ar, umidade_solo, timestamp, FK Diagnostico)
- [x] Command `mqtt_listener` com retry exponencial e shutdown limpo
- [x] Endpoint `GET /api/diagnostico/historico/` paginado (page_size=10)
- [x] 5/5 testes passando (inclui MQTT e historico)
- [x] Mosquitto 2.1.2 instalado e testado (localhost:1883)

### Dataset & IA ✅ CONCLUÍDO (2026-04-29)
- [x] Baixar PlantVillage do Kaggle — 18.160 imgs
- [x] `prepare_plantvillage.py` — split 70/15/15, 6 augmentations → 88.949 imgs treino
- [x] `datasets/dataset_stats.md` gerado
- [x] **Experimento A (Edge Impulse):** MobileNetV2 96×96 0.35, 40 cycles — FP32 92,5% / INT8 62,0%
- [x] **Experimento B (TF local WSL2):** MobileNetV2 96×96 0.35, 2 fases — **INT8 98,13% test acc, 639 KB** ← modelo escolhido
- [x] `train_local.py` + `export_tflite.py` — scripts de treino e exportação INT8 calibrada
- [x] `datasets/modelo/ceres_mobilenetv2_int8.tflite` — modelo para ESP32-S3
- [x] Análise comparativa documentada (Exp A vs B, quantization loss -30pp)

### Validação de Campo ✅ CONCLUÍDO (2026-05-08)
- [x] PlantDoc copiado para `datasets/raw/plantdoc/` — 1.353 imgs campo real
- [x] `avaliar_plantdoc.py` executado — **20,77% acurácia** em campo real
- [x] Gap lab-campo documentado em `docs/plantdoc_results.md` e TCC seção 5.4
- [x] Análise científica: consistente com literatura (Mohanty 2016, Singh 2020)

### Background Augmentation ✅ CONCLUÍDA (2026-05-09)
- [x] `background_augment.py` criado — rembg U2-Net + recomposição sobre fundos PlantDoc
- [x] `FUNDAMENTACAO_TECNICA.md` atualizado com embasamento científico (seção 8)
- [x] `plotar_historico.py` — curvas de treino geradas em `docs/historico_treino.png`
- [x] `demo_inferencia.py` — demo visual de inferência com barra de confiança
- [x] `sprint_review_roteiro.md` — roteiro completo slide a slide para apresentação
- [x] TCC seção 5.2 — análise das curvas + acurácia por classe com valores reais
- [x] TCC seção 6 — conclusão parcial Sprint 1 com tabela e contribuições
- [x] TCC referências — Singh 2020, Wu 2023, Qin 2020, Yang 2024, Xu 2024 adicionadas
- [x] `.env.example` atualizado — MQTT, ALLOWED_HOSTS, EDGE_IMPULSE_API_KEY
- [x] `requirements_minimal.txt` criado — dependências mínimas para o notebook
- [x] TCC seção 2.2 — Transfer Learning, Quantização INT8, gap lab-campo com refs reais
- [x] TCC seção 2.5 — tabela trabalhos relacionados atualizada com resultados reais
- [x] TCC seção 3.2 — dataset e pré-processamento revisado
- [x] `RELATORIO_TECNICO.md` — log 2026-05-09 registrado
- [x] `docs/resumo_executivo.md` — resumo em linguagem simples (banca/orientador/produtores)
- [x] `verificar_ambiente.py` — instruções de correção salvas no check_report.txt
- [x] Processamento completo concluído — 177.698 composições, 0 erros, 650min (2026-05-09)
- [x] Retreinar MobileNetV2 no WSL2 com `processed_field` — **Exp C: 96,20% lab / 20,24% campo** (2026-05-09)
- [x] Rodar `avaliar_plantdoc.py` pós-retreino — resultado: **20,24%** (meta não atingida; resultado negativo documentado)
- [x] `avaliar_plantdoc.py` corrigido — avalia train+test splits (746 imgs); análise por classe registrada
- [x] `export_tflite.py` corrigido — `class_names` capturado antes de `map/prefetch`
- [x] **Exp D — Fine-tuning PlantDoc real:** `preparar_mixed.py` + retreino com 95.719 imgs (2026-05-09)
  - Lab (PlantVillage test): **97,55%** | Campo geral (746 imgs): **88,47%** | Campo justo (69 imgs): **30,43%**
  - Melhora real em campo não visto: ~20% → 30,43% (+10pp)
- [x] **Validação independente Tomato-Village** (2026-05-09)
  - `avaliar_tomatovillage.py` — 217 imgs campo real, Rajasthan, Índia — 4 classes com mapeamento Ceres
  - Resultado Exp D: **11,52%** — gap geográfico maior que o do PlantDoc
  - Achado: colapso para D02_septoriose sob shift de domínio extremo; saudavel=0%
  - Achado: mapeamento D06 biologicamente incorreto (TSWV ≠ TYLCV)
  - Documentado em `docs/resultados/tomatovillage_results.md`
- [x] **Validação independente Daffodil BD** (2026-05-11)
  - `avaliar_daffodil.py` — 1.616 imgs campo real, Bangladesh — 7 classes com mapeamento Ceres
  - Resultado Exp D: **9,59%** | Resultado Exp E: **18,13%** (+8,54pp)
  - Achado: D05_mofo_foliar 77,3% (Exp D) — hipótese de distinção visual Passalora fulva
  - Documentado em `docs/resultados/daffodil_results.md`
- [x] **Experimento E — Focal Loss + Augmentação Agressiva** (2026-05-12)
  - `train_expe.py` — Focal Loss (γ=2, label_smoothing=0.1) + aug cor + backbone completo LR=1e-5
  - Lab: **98,43%** test acc | Macro F1: **0,9791** | Tamanho: **638 KB**
  - Tomato-Village Exp E: **27,65%** (+16,13pp sobre Exp D)
  - Daffodil BD Exp E: **18,13%** (+8,54pp sobre Exp D)
  - Atrator mudou: D02_septoriose → D01_requeima/D09 (features mais discriminativas)
  - **Modelo final atualizado: `ceres_expe_int8.tflite` 638 KB** ← substitui Exp D

### Firmware ESP32-S3 — Sprint 1b ✅ CONCLUÍDA (2026-05-11)
- [x] **Pré-requisito:** feito no notebook (mesma rede WiFi que o ESP32)
- [x] Criar `firmware/esp32_mqtt_sensor/` com PlatformIO (`esp32-s3-devkitc-1`)
- [x] Conectar WiFi e broker Mosquitto (192.168.15.22:1883)
- [x] Publicar JSON simulado em `ceres/sensor/001` a cada 30s (sem sensores em mãos)
- [x] Reconexão automática WiFi e MQTT
- [x] Testado com `mosquitto_sub -t ceres/sensor/+` — 74 eventos persistidos no Django
- [x] Pilha completa validada: ESP32-S3 → WiFi → Mosquitto → mqtt_listener → PostgreSQL → API REST

**Hardware utilizado:** ESP32-S3-WROOM-1-N16R8 (16MB Flash + 8MB PSRAM) — mesmo chip do Sprint 2
**Nota:** valores simulados — substituir por DHT22 + ADC quando sensores chegarem

---

## Sprint 2 — ESP32-S3 + TFLite Micro ✅ CONCLUÍDA (2026-05-27)

> **Escopo revisado:** OV5640 removido (deadline). Câmera substituída por imagens embutidas como arrays C.

**Resultado real:** `ceres_mobilenetv2_int8.tflite` (Exp B, 639KB) rodando no ESP32-S3,
latência **692ms**, 10/10 correto, MQTT validado. Ver `docs/resultados/benchmark_esp32s3.md`.

### Firmware TFLite Micro
- [x] Criar `firmware/esp32s3_ceres/` com PlatformIO (Flash 16MB, PSRAM habilitada)
- [x] Integrar modelo como array C (`model_data.h`) via `gerar_arrays_c.py`
- [x] Implementar `inference.h` / `inference.cpp` — 512KB PSRAM, softmax INT8→float
- [x] Normalização INT8: `uint8 - 128` (scale=0.0078125, zero_point=0)
- [x] Latência medida: **692ms** média (esp_timer_get_time)
- [x] Arena PSRAM usada: 200KB / 512KB (39%)

### Imagens de Teste Embutidas
- [x] `gerar_arrays_c.py` — 10 imgs (1/classe) × 96×96×3 int8 → `test_images.h`
- [x] Inferência em loop sobre os 10 arrays

### Firmware Integrado
- [x] Serial: classe esperada + predição + confiança + latência + RAM
- [x] MQTT: 10/10 JSONs publicados em `ceres/sensor/001` ✓
- [x] LED RGB: verde/vermelho/amarelo por resultado
- [x] WiFi: VIVOFIBRA-WIFI6-0F20 → IP 192.168.15.94 ✓

### Benchmark
- [x] 10/10 imagens corretas (100% acurácia)
- [x] Latência: 692ms média / 692ms mín / 695ms máx
- [x] `docs/resultados/benchmark_esp32s3.md` completo
- [x] Lib usada: `spaziochirale/Chirale_TensorFLowLite@2.0.0`

---

## Fase Futura — Raspberry Pi 3B+ + EfficientNet (Exp F)

> Fora do escopo do artigo/TCC atual. Registrado para próxima fase de pesquisa.

- [ ] EfficientNet-B0 224×224 treinado no PC (RTX 3060 Ti)
- [ ] tflite-runtime no RPi3B+ — estimativa campo: 45-55%
- [ ] Câmera USB + DHT22 + sensor solo via GPIO Python
- [ ] Comparativo: ESP32-S3 (TinyML 638KB) vs RPi3B+ (edge 5MB)

---

## Sprint 3 — Flutter + Docker + Experimentos 🔄 EM ANDAMENTO (2026-05-27)

**Critério de aceite:** App Flutter consumindo API, histórico paginado,
Django containerizado; experimento edge vs cloud documentado.

### Flutter — Estrutura base ✅ CONCLUÍDA (2026-05-27)
- [x] `app_ceres/` criado com `flutter create --org br.edu.ifmt --platforms android,windows`
- [x] `pubspec.yaml` — dependências: drift, http, image_picker, intl, path_provider
- [x] `lib/config.dart` — BASE_URL configurável (10.0.2.2:8080 emulador / IP real celular)
- [x] `lib/models/resultado_inferencia.dart` — parse do POST /inferir/ com rotulo legível
- [x] `lib/models/evento_mqtt.dart` — parse do GET /historico/
- [x] `lib/services/api_service.dart` — HTTP multipart POST + GET paginado
- [x] `lib/screens/camera_screen.dart` — câmera/galeria + POST inferir/ + barras de score
- [x] `lib/screens/historico_screen.dart` — lista paginada eventos ESP32 + pull-to-refresh
- [x] `lib/main.dart` — NavigationBar (Diagnóstico / Histórico)
- [x] `flutter analyze` — zero issues
- [x] APK debug buildado com sucesso
- [x] Android permissions: INTERNET, CAMERA, READ_MEDIA_IMAGES
- [x] `HistoricoEventosView.permission_classes` → AllowAny (Flutter sem JWT)

### Django containerizado ✅ CONCLUÍDO (2026-05-27)
- [x] `backend/requirements-backend.txt` — dependências mínimas do backend
- [x] `backend/Dockerfile` — Python 3.12-slim + ai-edge-litert + migrate automático
- [x] `docker-compose.yml` atualizado — serviço `django` porta 8080, volume modelo TFLite
- [x] `.vscode/tasks.json` + `launch.json` — `Ctrl+Shift+B` sobe Django + Flutter
- [x] `iniciar.ps1` — script automação: emulador + fotos teste + Docker Django + Flutter

### Testes realizados no notebook
- [x] Emulador Android API 34 criado e testado (Pixel8 AVD)
- [x] App abre no emulador com telas Diagnóstico e Histórico funcionando
- [x] POST /api/diagnostico/inferir/ validado (Django Test Client: D01_requeima, 23,1%)
- [x] Fotos de teste: 10 classes enviadas ao emulador via adb (pasta Ceres na galeria)

### Configuração PC desktop (sem Docker) ✅ CONCLUÍDA (2026-05-27)
- [x] `ai-edge-litert==2.1.5` + `django-cors-headers` instalados no venv Python 3.13
- [x] `settings_notebook.py` → `ceres_expe_int8.tflite` (modelo Exp E, final)
- [x] `config.dart` → `localhost:8080` (Windows desktop)
- [x] `views.py` → latência real via subprocess (279ms medido)
- [x] `camera_screen.dart` → botão câmera desabilitado no Windows (`Platform.isWindows`)
- [x] `iniciar.ps1` reescrito para PC sem Docker (Django via venv + Flutter `-d windows`)
- [x] Visual Studio Build Tools + workload C++ instalados
- [x] `flutter analyze` → zero issues

### Validação end-to-end PC desktop ✅ CONCLUÍDA (2026-05-27)
- [x] Galeria → POST multipart → TFLite → resultado na tela (Windows desktop)
- [x] Latência API real: ~279ms (subprocess Python no PC)
- [x] Testado: Septoriose (14,3%) e Mosaico (12,6%) — confiança baixa esperada para campo real
- [N/A] `docker compose up` — Docker não disponível no PC desktop; Django roda via venv

### Experimento Edge vs Cloud ✅ CONCLUÍDO (2026-05-28)
- [x] `benchmark_api.py` — 10 classes × 5 repetições, latência + acurácia
- [x] Warm-up automático (evita outlier de primeira carga)
- [x] `docs/resultados/experimento_edge_vs_cloud.md` — análise completa
- [x] `docs/resultados/benchmark_api.json` — dados brutos salvos
- **Resultado:** 9/10 (90%) | 306ms subprocess | 2333ms HTTP (dev server)
- **Comparativo:** ESP32 692ms offline vs Cloud 306ms (infra necessária)

### Drift — Persistência offline ✅ CONCLUÍDA (2026-05-28)
- [x] `lib/database/database.dart` — tabela `DiagnosticosLocais` + AppDatabase singleton
- [x] `database.g.dart` gerado via build_runner (Drift code gen)
- [x] `camera_screen.dart` — salva automaticamente após cada inferência bem-sucedida
- [x] Badge "✅ Salvo localmente" exibido na tela de diagnóstico
- [x] `lib/screens/historico_local_screen.dart` — lista expansível com scores, timestamp e latência
- [x] `main.dart` — 3º tab "Salvo" adicionado à NavigationBar
- [x] `ResultadoInferencia.rotuloDeClasse()` — método estático compartilhado com o banco
- [x] `flutter analyze` → zero issues
- [x] `pubspec.yaml` — `path: ^1.9.1` adicionado

### Pendente ⏳
- [ ] Layout final (Claude Design)

---

## Resumo

| Sprint | Tema | Status | Progresso |
|--------|------|--------|-----------|
| Sprint 0 | Motor de Diagnóstico | ✅ Concluída | 8/8 |
| Sprint 1 | MQTT + Dataset + Treino (Exp A→E) | ✅ Concluída | 24/24 |
| Sprint 1b | Firmware ESP32-S3 MQTT | ✅ Concluída | 7/7 |
| Sprint 2 | TFLite Micro ESP32-S3 (sem câmera) | ✅ Concluída | 11/11 |
| Sprint 3 | Flutter + Django PC + API | ✅ Concluída | 19/19 |
| Fase Futura | RPi3B+ + EfficientNet (Exp F) | 📋 Registrado | — |
