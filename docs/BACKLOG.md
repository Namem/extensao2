# Backlog do Produto — Ceres Diagnóstico
**TCC Engenharia da Computação — IFMT Sorriso-MT**
**Autor:** Namem Rachid Jaudy Neto
**Última atualização:** 2026-04-23

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
- [x] Docker Compose com PostgreSQL 15 na porta 5433
- [x] Multi-tenant (`Tenant`, `CustomUser`) estruturado
- [x] `.env` criado e `settings.py` lendo variáveis de ambiente

---

## Sprint 1 — MQTT + Dataset + Treino 🔄 EM ANDAMENTO

**Critério de aceite:** ESP32 publicando JSON via MQTT, Django persistindo eventos com endpoint paginado, dataset PlantVillage preparado e upload iniciado no Edge Impulse.

### Firmware (ESP32 genérico disponível)
- [ ] Criar `firmware/esp32_mqtt_sensor/` com PlatformIO (`esp32dev`)
- [ ] Conectar WiFi e broker Mosquitto local (192.168.x.x:1883)
- [ ] Ler DHT22 no GPIO4 e sensor de umidade do solo no GPIO34 (ADC 12 bits)
- [ ] Publicar JSON em `ceres/sensor/001` a cada 30s
- [ ] Reconexão automática WiFi e MQTT
- [ ] Testar com `mosquitto_sub -t ceres/sensor/+`

### Backend Django
- [ ] Adicionar `paho-mqtt>=2.0.0` ao `requirements.txt`
- [ ] Model `DiagnosticoEvento` + migration (device_id, classe_detectada, confianca, temperatura, umidade_ar, umidade_solo, timestamp, FK Diagnostico)
- [ ] Command `mqtt_listener` com retry exponencial e shutdown limpo (SIGTERM)
- [ ] Endpoint `GET /api/diagnostico/historico/` paginado (page_size=10)
- [ ] Testes: `test_evento_criado_com_dados_validos` e `test_historico_retorna_lista_paginada`

### Dataset & IA
- [ ] Baixar PlantVillage do Kaggle (`abdallahalidev/plantvillage-dataset`)
- [ ] Criar `datasets/scripts/prepare_plantvillage.py` (filtro 10 classes tomate, split 70/15/15, augmentation)
- [ ] Gerar `datasets/dataset_stats.md` com contagem por classe (alerta se < 200 imgs)
- [ ] Gerar `datasets/edge_impulse_upload_guide.md` com instruções de upload
- [ ] Treinar MobileNetV2 INT8 no Edge Impulse

---

## Sprint 2 — ESP32-S3 + TFLite + Integração Completa ⏳ PENDENTE

**Critério de aceite:** Modelo TFLite rodando no ESP32-S3 com latência < 300ms e RAM > 4MB; loop completo câmera → MQTT → Django → endpoint em menos de 5 segundos.

### Hardware — ESP32-S3 N16R8 + OV5640
- [ ] Criar `firmware/esp32s3_ceres/` com PlatformIO (Flash 16MB, PSRAM habilitada)
- [ ] Sketch de teste câmera OV5640 com pinout correto para N16R8
- [ ] Documentar gravação via USB-C nativo

### TFLite Micro
- [ ] Exportar modelo Edge Impulse como Arduino Library
- [ ] Integrar biblioteca ao PlatformIO (`lib/ei_ceres/`)
- [ ] Implementar `inference.h` / `inference.cpp` com alocação na PSRAM
- [ ] Normalizar pixels para [-1, 1] e medir latência com `esp_timer_get_time()`
- [ ] Validar: latência < 300ms, RAM livre > 4MB

### Firmware Integrado
- [ ] Ciclo completo: captura OV5640 → `run_inference()` → leitura DHT22 + solo → publicação MQTT
- [ ] Threshold configurável (default 0.70) em `include/config.h`
- [ ] LED vermelho 3x (anomalia detectada) / LED verde 1x (sem anomalia)
- [ ] Armazenar último evento válido na NVS
- [ ] Watchdog timer de 60s (`esp_task_wdt`)
- [ ] Reconexão automática WiFi (5s) e MQTT (10s)

### Benchmark & Integração
- [ ] Criar `datasets/scripts/benchmark_esp32s3.py` (50 imagens, latência + acurácia)
- [ ] Gerar `docs/benchmark_results.md` e `docs/benchmark_raw.csv`
- [ ] Teste end-to-end: medir T0→T4 para 5 eventos, meta < 5s
- [ ] Documentar `docs/e2e_test_results.md`

---

## Sprint 3 — Flutter + Resiliência + Experimentos ⏳ PENDENTE

**Critério de aceite:** App Flutter consumindo API com histórico paginado, status do sensor e funcionamento offline; experimento edge vs cloud documentado com dados para o artigo.

### Flutter — Telas
- [ ] Design System Agrícola (Mobile First) — ícones e fotos, mínimo de digitação
- [ ] `DiagnosticoResultadoScreen` (nome da doença, confiança, sensores, recomendação Embrapa)
- [ ] `HistoricoScreen` com paginação infinita e pull-to-refresh
- [ ] `SensorStatusScreen` com polling a cada 10s (online/offline, última leitura)
- [ ] Integração com câmera para registro de foto da planta
- [ ] `DiagnosticoEventoModel` + `DiagnosticoService` em Dart
- [ ] `flutter analyze` sem warnings críticos

### Resiliência & Gestão
- [ ] Persistência offline com Drift (diagnóstico funciona sem internet)
- [ ] Módulo de sincronização inteligente (upload ao reconectar)
- [ ] Histórico de diagnósticos georreferenciados (mapa simples + lista)
- [ ] Módulo de recomendação de manejo automático pós-diagnóstico
- [ ] Sistema multi-tenant para associações/cooperativas
- [ ] CI/CD e monitoramento configurados
- [ ] Geração de relatórios técnicos (PDF/CSV) para agrônomos

### Experimento Edge vs Cloud
- [ ] Criar `datasets/scripts/experiment_edge_vs_cloud.py` (100 imagens test split)
- [ ] Cenário Edge: latência real no ESP32-S3
- [ ] Cenário Cloud simulado: tflite-runtime no PC + overhead 200ms (4G)
- [ ] Gerar `docs/experiment_a_results.md` (tabela comparativa + gráfico ASCII)

---

## Resumo

| Sprint | Tema | Status | Tarefas |
|--------|------|--------|---------|
| Sprint 0 | Motor de Diagnóstico | ✅ Concluída | 8/8 |
| Sprint 1 | MQTT + Dataset + Treino | 🔄 Em andamento | 0/16 |
| Sprint 2 | ESP32-S3 + TFLite + Integração | ⏳ Pendente | 0/16 |
| Sprint 3 | Flutter + Resiliência + Experimentos | ⏳ Pendente | 0/17 |
