# Sprint Review — Ceres Diagnóstico
**Roteiro de apresentação — Sprint 1**
**Extensão 2 — IFMT Cuiabá**

---

## Slide 1 — Capa
**Título:** Ceres Diagnóstico — Sprint Review 1
**Subtítulo:** Sistema TinyML de Diagnóstico de Doenças no Tomateiro
**Autor:** Namem Rachid Jaudy Neto
**Data:** Maio/2026

---

## Slide 2 — O Problema
**Título:** Por que isso importa?

- Tomateiro é a 2ª hortaliça mais consumida no Brasil
- Doenças foliares podem destruir até 100% da colheita
- Produtor pequeno não tem acesso a diagnóstico rápido e barato
- Diagnóstico errado → defensivo errado → prejuízo e contaminação

**Visual sugerido:** foto de lavoura de tomate doente

---

## Slide 3 — A Solução Proposta
**Título:** Ceres Diagnóstico

```
[ESP32-S3]          [Backend]         [App]
Câmera OV5640  →   Django REST   →   Flutter
TFLite INT8        PostgreSQL        Histórico
MobileNetV2        MQTT              Recomendação
639 KB             JWT               Offline
```

- Funciona **sem internet** (inferência na borda)
- Custo alvo: **< R$ 200** (hardware)
- 10 doenças do tomateiro detectadas

---

## Slide 4 — O que foi planejado para a Sprint 1
**Título:** Sprint 1 — O que foi planejado

| Frente | Planejado |
|---|---|
| Dataset & IA | Preparar PlantVillage, treinar modelo TFLite |
| Backend | MQTT + persistência + endpoint histórico |
| Firmware | ESP32 publicando sensores via MQTT |
| Validação | Testar modelo em imagens de campo real |

---

## Slide 5 — O que foi entregue
**Título:** Sprint 1 — O que foi entregue ✅

| Frente | Status | Resultado |
|---|---|---|
| Dataset | ✅ | 18.160 → 88.949 imgs (augmentation x6) |
| Exp A — Edge Impulse | ✅ | FP32 92,5% / INT8 **62,0%** |
| Exp B — TF Local | ✅ | INT8 **98,13%** / 639 KB ← **escolhido** |
| Backend MQTT | ✅ | 5/5 testes passando |
| Validação campo | ✅ | PlantDoc 20,77% — gap documentado |
| Firmware | ⏳ | Aguarda notebook + WiFi |

---

## Slide 6 — Destaque: os dois experimentos
**Título:** Exp A vs Exp B — Por que treinamos duas vezes?

| | Exp A (Edge Impulse) | Exp B (TF Local) |
|---|---|---|
| Plataforma | Nuvem (gerenciada) | WSL2 + RTX 3060 Ti |
| Fases | 1 fase | **2 fases** |
| INT8 calibrado | ❌ | ✅ |
| Acurácia INT8 | 62,0% | **98,13%** |
| Tamanho | 624 KB | 639 KB |

**Achado científico:** calibração INT8 evitou queda de 30 pp

**Visual:** gráfico lado a lado dos dois resultados

---

## Slide 7 — Curvas de treinamento
**Título:** Como o modelo aprendeu

**Visual:** `docs/historico_treino.png` (inserir o PNG gerado)

Pontos a destacar na fala:
- Linha cinza: separação Fase 1 (backbone congelado) e Fase 2 (fine-tuning)
- Salto de ~87% → ~95% no início da Fase 2: efeito do descongelamento
- Melhor época: 28 (val acc 97,79%) — salvo automaticamente pelo ModelCheckpoint
- Train e val acc próximas: sem overfitting significativo

---

## Slide 8 — Acurácia por classe
**Título:** Resultado por classe — Test Set (2.734 imagens)

| Classe | Acurácia |
|---|---|
| Mosaico / Saudável | 100% |
| Vira-Cabeça | 99,5% |
| Mancha Bacteriana | 99,1% |
| Septoriose / Ácaro | 98,5% / 98,4% |
| Requeima | 97,6% |
| Mofo Foliar | 97,2% |
| Mancha Alvo | 95,3% |
| Pinta Preta | 90,0% ← mais difícil |
| **Geral** | **98,13%** |

---

## Slide 9 — Validação em campo real (PlantDoc)
**Título:** E no mundo real?

- Dataset PlantDoc: **1.353 fotos** tiradas em lavouras reais
- Resultado: **20,77%** (vs 98,13% em laboratório)
- **Isso é esperado** — documentado em 5 artigos científicos
- Causa identificada: modelo aprendeu o fundo cinza do PlantVillage

```
Classe saudável no PlantVillage → fundo cinza → 100%
Classe saudável no PlantDoc    → fundo verde  → 1,8%
```

**Solução em andamento:** Background Augmentation (rembg + fundos naturais)
Meta: superar **70%** no PlantDoc após retreino

---

## Slide 10 — Backend MQTT
**Título:** Pipeline IoT funcionando

```
ESP32          Mosquitto       Django         PostgreSQL
[sensor] →→→ [broker]  →→→  [listener] →→→  [DB]
ceres/sensor/001             mqtt_listener    DiagnosticoEvento
```

- 5/5 testes automatizados passando
- Endpoint `GET /api/diagnostico/historico/` paginado
- Retry exponencial automático em caso de queda do broker

**Demo ao vivo (opcional):** rodar `mosquitto_pub` e mostrar evento no DB

---

## Slide 11 — Próximos passos
**Título:** O que vem a seguir

| Sprint | O que fazer | Precisa |
|---|---|---|
| Sprint 1b | Firmware ESP32 MQTT | Notebook + WiFi |
| Sprint 1b | Retreino Exp C (background aug) | PC (rodando agora) |
| Sprint 2 | TFLite no ESP32-S3 | ESP32-S3 N16R8 + OV5640 |
| Sprint 2 | Latência real < 300ms | Hardware em mãos |
| Sprint 3 | App Flutter | Qualquer máquina |

---

## Slide 12 — Encerramento
**Título:** Resumo Sprint 1

✅ Modelo treinado: **98,13%** (639 KB, pronto para ESP32-S3)
✅ Backend IoT: **5/5 testes** passando
✅ Gap lab-campo documentado: contribuição científica
🔄 Background augmentation: em andamento para superar 70% no campo

**Repositório:** github.com/Namem/extensao2

---

*Dicas de apresentação:*
- *Slides 6 e 7 são os mais técnicos — ensaiar a explicação*
- *Slide 9 (PlantDoc) é importante: deixar claro que 20,77% não é falha*
- *Demo ao vivo no Slide 10 impressiona — ter mosquitto aberto antes*
