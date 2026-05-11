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
  - Modelo final escolhido: `ceres_mobilenetv2_int8.tflite` 639 KB (Exp D)
- [x] **Validação independente Tomato-Village** (2026-05-09)
  - `avaliar_tomatovillage.py` — 217 imgs campo real, Rajasthan, Índia — 4 classes com mapeamento Ceres
  - Resultado Exp D: **11,52%** — gap geográfico maior que o do PlantDoc (30,43%)
  - Achado: colapso para D02_septoriose sob shift de domínio extremo; saudavel=0%
  - Achado: mapeamento D06 biologicamente incorreto (TSWV ≠ TYLCV)
  - Conclusão: fine-tuning com PlantDoc não generaliza para regiões geográficas muito distintas
  - Documentado em `docs/tomatovillage_results.md` e TCC seção 5.4.5

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

## Sprint 2 — ESP32-S3 + TFLite + Integração Completa ⏳ PENDENTE

**Pré-requisito:** ESP32-S3 N16R8 + OV5640 5MP (a comprar) + sensor solo resistivo
**Critério de aceite:** Modelo TFLite rodando no ESP32-S3 com latência < 300ms;
loop completo câmera → MQTT → Django → endpoint em menos de 5 segundos.

### Hardware
- [ ] Comprar ESP32-S3 N16R8 + OV5640 + sensor solo resistivo
- [ ] Criar `firmware/esp32s3_ceres/` com PlatformIO (Flash 16MB, PSRAM habilitada)
- [ ] Sketch de teste câmera OV5640 com pinout correto para N16R8

### TFLite Micro no ESP32-S3
- [ ] Integrar `ceres_mobilenetv2_int8.tflite` via TFLite Micro
- [ ] Implementar `inference.h` / `inference.cpp` com alocação na PSRAM
- [ ] Normalizar pixels [-1, 1] e medir latência com `esp_timer_get_time()`
- [ ] Validar: latência < 300ms, RAM livre > 4MB

### Firmware Integrado
- [ ] Ciclo: captura OV5640 → `run_inference()` → DHT22 + solo → MQTT
- [ ] Threshold configurável (default 0.70) em `include/config.h`
- [ ] LED vermelho 3x (anomalia) / verde 1x (saudável)
- [ ] Watchdog 60s + reconexão automática WiFi/MQTT

### Benchmark
- [ ] `benchmark_esp32s3.py` — 50 imagens, latência + acurácia
- [ ] `docs/benchmark_results.md` + `benchmark_raw.csv`
- [ ] Teste end-to-end T0→T4 para 5 eventos, meta < 5s

---

## Sprint 3 — Flutter + Resiliência + Experimentos ⏳ PENDENTE

**Critério de aceite:** App Flutter consumindo API, histórico paginado,
funcionamento offline; experimento edge vs cloud documentado.

### Flutter — Telas
- [ ] Design System Agrícola (Mobile First)
- [ ] `DiagnosticoResultadoScreen` (doença, confiança, sensores, recomendação Embrapa)
- [ ] `HistoricoScreen` paginação infinita + pull-to-refresh
- [ ] `SensorStatusScreen` polling 10s
- [ ] `DiagnosticoEventoModel` + `DiagnosticoService` em Dart
- [ ] `flutter analyze` sem warnings críticos

### Resiliência
- [ ] Persistência offline com Drift
- [ ] Sincronização ao reconectar
- [ ] Geração de relatórios PDF/CSV para agrônomos

### Experimento Edge vs Cloud
- [ ] `experiment_edge_vs_cloud.py` (100 imgs test split)
- [ ] Cenário Edge: latência real ESP32-S3
- [ ] Cenário Cloud simulado: tflite-runtime PC + overhead 200ms (4G)
- [ ] `docs/experiment_a_results.md` com tabela comparativa

---

## Resumo

| Sprint | Tema | Status | Progresso |
|--------|------|--------|-----------|
| Sprint 0 | Motor de Diagnóstico | ✅ Concluída | 8/8 |
| Sprint 1 | MQTT + Dataset + Treino | ✅ Concluída | 24/24 |
| Sprint 1b | Firmware ESP32-S3 MQTT | ✅ Concluída | 7/7 |
| Sprint 2 | ESP32-S3 + TFLite + Integração | ⏳ Pendente — aguardando hardware | 0/15 |
| Sprint 3 | Flutter + Resiliência + Experimentos | ⏳ Pendente | 0/14 |
