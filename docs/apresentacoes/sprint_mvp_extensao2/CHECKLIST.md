# Checklist de Assets — Sprint MVP Extensão II

## Estrutura de pastas
```
sprint_mvp_extensao2/
  assets/
    screenshots/     ← capturas de tela do app no celular
    fotos_hardware/  ← fotos do ESP32, protoboard, sensores
    slides/          ← arquivo final do Gamma (.pdf ou imagens)
    video/           ← screenrecord do app (opcional)
  CHECKLIST.md       ← este arquivo
```

---

## FASE 1 — Hardware ✅ CONCLUÍDA

### Fotos reais (salvar manualmente da galeria do celular)
- [ ] `fotos_hardware/setup_completo.jpg`   ← foto carretel + planta + esp32 + sensores
- [ ] `fotos_hardware/sensor_solo_terra.jpg` ← sensor solo sendo inserido na planta
- [ ] `fotos_hardware/esp32_closeup.jpg`     ← ESP32-S3 close-up na protoboard
- [ ] `fotos_hardware/serial_monitor.jpg`    ← screenshot do VS Code com dados reais

### Imagens de componentes (baixadas da internet ✅)
- [x] `fotos_hardware/dht22_componente.jpg`       ← DHT22 fundo branco (components101)
- [x] `fotos_hardware/esp32s3_devkit.png`          ← ESP32-S3-DevKitC oficial Espressif (468KB)
- [x] `fotos_hardware/sensor_solo_componente.jpg`  ← Sensor capacitivo v1.2 (makerselectronics)

---

## FASE 2 — App no celular (screenshots)

### Salvar manualmente da galeria/screenshots do celular
- [ ] `screenshots/iot_sensor_card.jpg`     ← aba IoT com Temp 29.5°C / Umid 49% / Solo 34% ONLINE
- [ ] `screenshots/iot_historico.jpg`       ← lista de eventos MQTT (184 registros)
- [ ] `screenshots/diagnostico_resultado.jpg` ← resultado de diagnóstico com barra de confiança
- [ ] `screenshots/diagnostico_top3.jpg`    ← top-3 predições
- [ ] `screenshots/mapa.jpg`                ← marcadores no mapa
- [ ] `screenshots/enciclopedia.jpg`        ← uma doença aberta
- [ ] `screenshots/perfil.jpg`              ← estatísticas do perfil

> **NOTA:** Screenshot da aba IoT com dados reais já foi tirada (07/06/2026 17:28)
> Mostra: ESP32-S3 · ONLINE · 29.5°C · 49% · 34% · 184 eventos

---

## FASE 3 — Slides (Gamma)
- [ ] Gerar slides com prompt no gamma.app
- [ ] Inserir screenshots nas telas corretas
- [ ] Inserir fotos do hardware
- [ ] Exportar PDF → `slides/sprint_mvp_extensao2.pdf`

---

## FASE 4 — Screenrecord

### Pré-requisitos antes de gravar
- [ ] Deixar na galeria do celular: 1 foto de **requeima** + 1 foto de **folha saudável**
- [ ] App logado como test@test.com
- [ ] Mapa com pins de Cuiabá e Sorriso visíveis
- [ ] ESP32 publicando (IoT mostrando ONLINE)

### Roteiro v2 — Diagnóstico + Offline + Mapa (~2min)

| Cena | Ação | Tempo | Mostra |
|------|------|-------|--------|
| 1 | Abre app na **Diagnóstico** (modo Cloud) | 0–8s | UI inicial limpa |
| 2 | Galeria → escolhe **folha doente (Requeima)** → resultado online | 8–25s | "Requeima · 94%" + barra confiança · latência ~2s |
| 3 | Top-3 predições da mesma imagem | 25–35s | 3 doenças com % |
| 4 | Toca em "Saiba mais" → Enciclopédia da doença | 35–50s | Sintomas + tratamento |
| 5 | Vai para Perfil → seção "Modo de inferência" → toca em Local | 50–65s | Toggle Cloud → Local visível |
| 6 | LIGA MODO AVIÃO (puxa barra de notificações, ativa avião) | 65–75s | Sem WiFi/4G na status bar |
| 7 | Volta para Diagnóstico → escolhe **folha SAUDÁVEL** da galeria → resultado local | 75–95s | "Saudável" · latência <1s · sem rede |
| 8 | Aba Mapa → pins espalhados em Cuiabá-MT + Sorriso-MT | 95–110s | 30+ marcadores |
| 9 | Toca em 1 pin → mostra doença + data | 110–120s | Card com info do evento |
| 10 | (Opcional) Aba IoT → "Isso é um plus" | 120–130s | Sensor card 29.5°C |

- [ ] Duração: ~2 minutos
- [ ] Salvar em `video/demo_ceres.mp4`

---

## Status geral
| Fase | Status | Items |
|------|--------|-------|
| Hardware — componentes web | ✅ Concluído | 3/3 |
| Hardware — fotos reais | ✅ Concluído | 6/6 (setup_v1, setup_v2, sensor_solo, esp32_closeup, esp32_pinos, serial_monitor) |
| App screenshots | 🔄 Parcial | 1/7 (iot_sensor_card.jpg salvo) |
| Screenrecord | 🔄 EM ANDAMENTO | 0/1 |
| Slides Gamma | ⏳ Pendente | 0/4 |

## Slides Gamma — estrutura aprovada (voltar depois do vídeo)
1. Capa — Ceres Diagnóstico · IFMT · Namem Rachid
2. Problema — perdas no campo, diagnóstico precoce
3. Solução — arquitetura ESP32 → MQTT → Django → Flutter
4. Hardware IoT — setup_completo_v1.jpg + componentes + serial_monitor.png
5. App funcionando — iot_sensor_card.jpg + tela diagnóstico
6. Resultados — 98,43% · 692ms · 184 eventos · próximos passos
