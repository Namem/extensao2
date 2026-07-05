# Backlog do Produto — Ceres Diagnóstico

**Atividade de Extensão II — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto

> Backlog **exclusivo do produto** (software, firmware e hardware) para o Relatório
> Final da disciplina. Não inclui tarefas de escrita de TCC ou artigo científico.

**Metodologia:** Scrum adaptado — **3 sprints de ~1 mês** cada, com revisão ao final.
**Gerenciamento e versionamento:** GitHub (`github.com/Namem/extensao2`).
**Prioridades:** 🔴 Crítica · 🟠 Alta · 🔵 Média · ⚪ Baixa.

---

## Roadmap — visão geral

| Sprint | Tema | Duração | Camada | Status | Tarefas |
|---|---|---|---|---|---|
| **1** | Núcleo Inteligente (Backend + IA) | ≈ 1 mês | Backend / IA | ✅ Concluída | 18/18 |
| **2** | Borda Embarcada (Firmware + IoT) | ≈ 1 mês | Firmware / IoT | ✅ Concluída | 8/8 |
| **3** | Aplicativo e Integração (App + UX + Deploy) | ≈ 1 mês | App / Infra | ✅ Concluída | 29/29 |
| — | Próximos passos (Fase Futura) | — | IA / Firmware | 📋 Registrada | — |

**Total: 55/55 tarefas de produto · ~3 meses de desenvolvimento.**

---

## Sprint 1 — Núcleo Inteligente (Backend + IA) · ≈ 1 mês (4 semanas) · ✅ 18/18

**Objetivo:** construir a API Django, o motor de diagnóstico e o modelo de IA treinado e validado.

### Épico A — Motor de Diagnóstico e API *(ex-Sprint 0)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| Mapeamento das 10 doenças do tomateiro (Embrapa) | Backend | 🔴 Crítica | ✅ |
| Models Pergunta/Opcao/Diagnostico + migrations | Backend | 🔴 Crítica | ✅ |
| Endpoints `/iniciar/` e `/responder/` | Backend | 🟠 Alta | ✅ |
| Autenticação JWT (SimpleJWT) | Backend | 🟠 Alta | ✅ |
| Multi-tenant (Tenant + CustomUser) | Backend | 🔵 Média | ✅ |
| PostgreSQL 18 (porta 5433) | Infra | 🟠 Alta | ✅ |
| 5 testes automatizados passando | QA | 🟠 Alta | ✅ |

### Épico B — Dataset, Modelo de IA e MQTT *(ex-Sprint 1)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| PlantVillage (18.160 imgs) + augmentation → 88.949 | IA | 🔴 Crítica | ✅ |
| Exp A — Edge Impulse (FP32 92,5% / INT8 62%) | IA | 🔵 Média | ✅ |
| Exp B — TF local (float 98,13% / INT8 95,76%, 639 KB) | IA | 🔴 Crítica | ✅ |
| Exp C — Background augmentation sintética (20,24% campo) | IA | ⚪ Baixa | ✅ |
| Exp D — Fine-tuning PlantDoc real (30,43% campo) | IA | 🔵 Média | ✅ |
| Exp E — Focal Loss + aug agressiva (**final, 638 KB**) | IA | 🔴 Crítica | ✅ |
| `export_tflite.py` — INT8 calibrado | IA | 🟠 Alta | ✅ |
| Validação PlantDoc — gap lab-campo documentado | IA | 🟠 Alta | ✅ |
| Backend MQTT (DiagnosticoEvento + `mqtt_listener` + `/historico/`) | Backend | 🟠 Alta | ✅ |
| Mosquitto 2.1 instalado e testado | Infra | 🔵 Média | ✅ |
| Matriz de confusão + acurácia por classe | QA | 🔵 Média | ✅ |

---

## Sprint 2 — Borda Embarcada (Firmware + IoT) · ≈ 1 mês (4 semanas) · ✅ 8/8

**Objetivo:** rodar a IA e os sensores no hardware real ESP32-S3.

### Épico A — Nó de sensores MQTT *(ex-Sprint 1b)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| Projeto PlatformIO `esp32_mqtt_sensor` | Firmware | 🟠 Alta | ✅ |
| WiFi + MQTT + reconexão automática | Firmware | 🟠 Alta | ✅ |
| Publicação de JSON em `ceres/sensor/` | Firmware | 🟠 Alta | ✅ |
| Pilha ESP32 → Mosquitto → Django → PostgreSQL | Integração | 🟠 Alta | ✅ |

### Épico B — TFLite Micro no ESP32-S3 *(ex-Sprint 2)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| `esp32s3_ceres` — TFLite Micro (arena PSRAM 200 KB) | Firmware | 🔴 Crítica | ✅ |
| `gerar_arrays_c.py` — modelo + 10 imgs como arrays C | IA | 🟠 Alta | ✅ |
| Benchmark embarcado — **692 ms, 10/10 correto** | Firmware | 🔴 Crítica | ✅ |
| `benchmark_esp32s3.md` documentado | QA | 🔵 Média | ✅ |

---

## Sprint 3 — Aplicativo e Integração (App + UX + Deploy) · ≈ 1 mês (4 semanas) · ✅ 29/29

**Objetivo:** entregar o aplicativo Flutter completo, publicado e resiliente.

### Épico A — App base + inferência *(ex-Sprint 3)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| App Flutter (Diagnóstico + Histórico) | App | 🔴 Crítica | ✅ |
| `api_service` — multipart POST + GET paginado | App | 🟠 Alta | ✅ |
| View `/inferir/` via subprocess TFLite | Backend | 🔴 Crítica | ✅ |
| Validação end-to-end (galeria → TFLite → resultado) | QA | 🟠 Alta | ✅ |
| Experimento Edge vs Cloud | IA | 🔵 Média | ✅ |
| Drift (SQLite) — persistência local | App | 🟠 Alta | ✅ |

### Épico B — Design System e UI *(ex-Sprint 3.5 + 3.6)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| CeresTheme (paleta cerrado, Material 3) | App | 🟠 Alta | ✅ |
| 6 telas redesenhadas (Splash/Login/Diagnóstico/IoT/Salvos/Enciclopédia) | App | 🟠 Alta | ✅ |
| `doencas_data.dart` — 10 doenças centralizadas | App | 🔵 Média | ✅ |
| `flutter_svg` + ícones thin-stroke | App | ⚪ Baixa | ✅ |
| Tab bar + appbar fiéis ao mockup | App | ⚪ Baixa | ✅ |

### Épico C — Deploy, nuvem e novas telas *(ex-Sprint 3.7)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| 12 telas migradas + 4 novas (Alertas/Parceiro/Cadastro/Agrônomos) | App | 🟠 Alta | ✅ |
| Registro de usuário `/register/` | Backend | 🟠 Alta | ✅ |
| Deploy Railway — `ceres.up.railway.app` | Infra | 🔴 Crítica | ✅ |
| TFLite on-device Android (~60 ms) | App | 🔴 Crítica | ✅ |
| MQTT Cloud HiveMQ (TLS 8883 / WS 8884) | IoT | 🟠 Alta | ✅ |

### Épico D — UX: navegação, mapa e perfil *(ex-Sprint 4A + 4B + 5)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| Back button no `CeresAppBar` | App | ⚪ Baixa | ✅ |
| Persistência de sessão (shared_preferences) + auto-refresh JWT | App | 🔵 Média | ✅ |
| Banner offline (`connectivity_plus`) | App | 🔵 Média | ✅ |
| `latitude`/`longitude` em DiagnosticoEvento | Backend | 🔵 Média | ✅ |
| `MapaScreen` (flutter_map + OSM, marcadores por urgência) | App | 🟠 Alta | ✅ |
| Captura de GPS no diagnóstico | App | 🔵 Média | ✅ |
| `GET /api/auth/me/` (estatísticas do usuário) | Backend | 🔵 Média | ✅ |
| `PerfilScreen` (stats, exportar CSV, logout) | App | 🔵 Média | ✅ |

### Épico E — Robustez e sincronização offline *(ex-Sprint 5B)*
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| Railway PostgreSQL persistente entre deploys | Infra | 🔴 Crítica | ✅ |
| Per-user diagnostics (FK `usuario`) | Backend | 🟠 Alta | ✅ |
| Temperature scaling INT8 (T=0.25) | Backend/App | 🟠 Alta | ✅ |
| Fila de sincronização offline → online (`SyncService`) | App | 🟠 Alta | ✅ |
| Matriz de confusão INT8 (95,76%, 2.734 imgs) | QA | 🔵 Média | ✅ |

---

## Próximos passos — Fase Futura (registrada) 📋
| Tarefa | Camada | Prioridade | Status |
|---|---|---|---|
| EfficientNet-B0 no Raspberry Pi 3B+ | IA | 🔵 Média | 📋 |
| Câmera OV5640 no ESP32-S3 (diagnóstico autônomo) | Firmware | 🟠 Alta | 📋 |
