# Relatório Final — Atividade de Extensão II

**Ceres Diagnóstico — Sistema embarcado de detecção precoce de doenças no tomateiro**

---

## 1. Identificação do Projeto

### 1.1 Título
**Ceres Diagnóstico** — Sistema embarcado de detecção precoce de doenças no tomateiro,
integrando visão computacional (TinyML) no ESP32-S3, backend em nuvem e aplicativo móvel.

### 1.2 Curso / Disciplina / Professor
- **Curso:** Engenharia da Computação — IFMT Cuiabá (Campus Cel. Octayde Jorge da Silva)
- **Disciplina:** Extensão II — 2026/1
- **Professor:** Tiago Lacerda

### 1.3 Integrantes
Projeto desenvolvido **individualmente**:

| Nome | Funções desempenhadas |
|---|---|
| **Namem Rachid Jaudy Neto** | Product Owner, Scrum Master, Desenvolvedor Back-end (Django/API), Desenvolvedor Front-end/Mobile (Flutter), Engenheiro de IA (treino/quantização), Desenvolvedor de Firmware (ESP32-S3), Banco de Dados, UX/UI e QA |

### 1.4 Local e Ano
Cuiabá — MT, IFMT, 2026.

---

## 2. Resumo Executivo

**Problema.** Pequenos produtores de tomate têm dificuldade de acesso a diagnóstico
agronômico rápido. Doenças como a requeima podem destruir uma lavoura inteira antes
de o produtor identificar o problema, e a conectividade no campo é limitada.

**Público-alvo.** Pequenos horticultores de Sorriso-MT e região, produtores de tomate
que trabalham diretamente no campo.

**Produto.** Um sistema em três camadas: (1) **aplicativo móvel** que diagnostica
doenças da folha por foto, com IA rodando **no próprio celular** (offline) ou na nuvem;
(2) **nó IoT ESP32-S3** que monitora temperatura e umidade e roda o modelo embarcado;
(3) **backend em nuvem** (Django REST no Railway) com histórico, mapa de ocorrências e
enciclopédia das doenças.

**Tecnologias.** Django REST Framework, PostgreSQL, Flutter/Dart, TensorFlow/TFLite
(MobileNetV2 INT8), ESP32-S3 (PlatformIO/Arduino), MQTT (Mosquitto/HiveMQ), Railway, GitHub.

**Principais resultados.** Modelo de **638 KB** classificando **10 categorias** (9 doenças
+ saudável); acurácia de **95,76%** (INT8, laboratório); latência de **692 ms** no ESP32-S3
e **~60 ms** on-device no celular; aplicativo completo com 5 telas publicado e API em
produção. O projeto documentou honestamente o **gap laboratório-campo** (queda para
20–30% em imagens de campo real), fenômeno reconhecido na literatura.

---

## 3. Visão do Projeto

**Problema identificado.** Um tomateiro doente não “grita”: murcha em silêncio enquanto
a doença avança. O diagnóstico depende de um agrônomo, inacessível ao pequeno produtor,
e existem cerca de 10 doenças difíceis de distinguir a olho nu. A internet que permitiria
o diagnóstico digital muitas vezes não chega à lavoura.

**Público-alvo e comunidade beneficiada.** Pequenos horticultores de Sorriso-MT e região
— produtores que trabalham diretamente no campo, com pouco tempo ou dificuldade para
digitar textos técnicos no celular.

**Justificativa.** Diferente de grupos de WhatsApp, buscas no Google ou chatbots agrícolas
genéricos, o Ceres transforma recomendações de manejo (base Embrapa) em diagnósticos
rápidos e acessíveis diretamente na lavoura, ajudando o produtor a tomar decisões técnicas
mais seguras e reduzir perdas.

**Objetivos.**
- Treinar um modelo de IA leve o suficiente para rodar em microcontrolador e celular;
- Disponibilizar diagnóstico por foto **funcionando offline**;
- Monitorar variáveis ambientais da lavoura via sensores IoT;
- Entregar um aplicativo completo, publicado e utilizável em condições reais.

**Benefícios esperados.** Triagem agronômica imediata e de baixo custo (~R$80 por nó de
hardware), redução de perdas por diagnóstico tardio e democratização do acesso à
informação técnica no campo.

---

## 4. Roadmap do Produto

O desenvolvimento foi organizado em **3 sprints de ~1 mês**, além de uma fase futura
registrada. O backlog completo (com épicos, prioridades e status) está no anexo
`BACKLOG_PRODUTO` (Markdown e Excel).

**Figura 1 —** Linha do tempo do produto (`diagramas/roadmap.png`).

| Sprint | Tema | Duração | Tarefas | Status |
|---|---|---|---|---|
| 1 | Núcleo Inteligente (Backend + IA) | ≈ 1 mês | 18 | ✅ |
| 2 | Borda Embarcada (Firmware + IoT) | ≈ 1 mês | 8 | ✅ |
| 3 | Aplicativo e Integração (App + UX + Deploy) | ≈ 1 mês | 29 | ✅ |
| — | Fase Futura (câmera OV5640, RPi3B+) | — | — | 📋 |

**Alterações de escopo (repriorizações justificadas):**
- **Câmera OV5640** removida da entrega e mantida como prova de conceito — o custo/prazo
  inviabilizaram a integração; o app móvel assumiu o papel de produto principal.
- **Experimentos de IA (A→E):** a augmentation sintética (Exp C) foi descartada por piorar
  o resultado; adotou-se fine-tuning com dados reais (Exp D) e Focal Loss (Exp E, modelo final).

---

## 5. Gestão e Tecnologias

### 5.1 Gestão do Projeto
- **Metodologia:** Scrum adaptado ao contexto individual — sprints de ~1 mês com revisão
  (Sprint Review) e ajuste de backlog ao final de cada ciclo.
- **Sprints realizadas:** 3 (+ fase futura registrada).
- **Ferramenta de gestão e versionamento:** **GitHub** (`github.com/Namem/extensao2`) —
  histórico de commits (Conventional Commits) como registro de progresso; backlog mantido
  em Markdown/Excel.
- **Organização das tarefas:** backlog priorizado por criticidade (Crítica → Baixa),
  agrupado por épico e camada (Backend, IA, Firmware, App, Infra, QA).
- **Adaptação:** por ser projeto individual, os papéis de PO, Scrum Master e time foram
  acumulados pelo autor; a “comunicação” se deu via documentação viva no repositório.

### 5.2 Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Django REST Framework | Backend / API REST |
| PostgreSQL | Banco de dados (produção) |
| SimpleJWT | Autenticação por token JWT |
| Flutter / Dart | Aplicativo móvel e desktop |
| Drift (SQLite) | Persistência offline no app |
| flutter_map + OpenStreetMap | Mapa de ocorrências |
| geolocator | Captura de GPS |
| TensorFlow / Keras | Treinamento do modelo de IA |
| TensorFlow Lite / tflite_flutter | Inferência embarcada (celular e ESP32) |
| MobileNetV2 (INT8) | Arquitetura do classificador |
| rembg (U2-Net) / Pillow | Pré-processamento de imagens no treino |
| ESP32-S3 (PlatformIO / Arduino) | Firmware do nó IoT |
| DHT22 + sensor capacitivo | Sensores de temperatura, umidade do ar e do solo |
| MQTT (Mosquitto / HiveMQ Cloud) | Comunicação IoT (TLS / WebSocket) |
| Railway | Hospedagem do backend e do PostgreSQL |
| GitHub | Versionamento e gestão do backlog |

**Figura 2 —** Arquitetura do sistema (`diagramas/arquitetura.png`).

---

## 6. Descrição do Desenvolvimento

### Sprint 1 — Núcleo Inteligente (Backend + IA)
- **Objetivo:** API Django, motor de diagnóstico e modelo de IA treinado/validado.
- **Planejado:** models e endpoints, JWT, dataset, treino do modelo, pipeline MQTT.
- **Concluído:** motor por árvore de decisão (`/iniciar/`, `/responder/`), JWT, multi-tenant,
  PostgreSQL; dataset PlantVillage (18.160 → 88.949 imgs); **5 experimentos de treino
  (A→E)**, chegando ao modelo final de 638 KB; backend MQTT (`mqtt_listener`, `/historico/`).
- **Dificuldades:** TensorFlow não suporta Python 3.13 (uso do WSL2 + Python 3.12);
  detecção da GPU no WSL2 (ajuste de `LD_LIBRARY_PATH`); bug de pré-processamento INT8 na
  validação.
- **Decisões:** treinar localmente (Exp B) por permitir quantização INT8 calibrada;
  descartar a augmentation sintética (Exp C) por não melhorar o campo.
- **Entrega:** API funcional (5/5 testes) + modelo TFLite validado.

### Sprint 2 — Borda Embarcada (Firmware + IoT)
- **Objetivo:** IA e sensores rodando no hardware real ESP32-S3.
- **Planejado:** firmware WiFi/MQTT, leitura de sensores, TFLite Micro embarcado.
- **Concluído:** nó de sensores publicando via MQTT; **TFLite Micro** com o modelo embarcado
  como array C; benchmark de **692 ms** e **10/10** classificações corretas; pilha IoT
  ponta a ponta (ESP32 → broker → Django → PostgreSQL).
- **Dificuldades:** bibliotecas TFLite para ESP32 descontinuadas (solução:
  `Chirale_TensorFLowLite`); boot loop por flags de PSRAM; broker só escutando em localhost.
- **Decisões:** remover a câmera OV5640 do escopo (prazo/custo) e usar imagens embutidas
  para validar a inferência.
- **Entrega:** modelo rodando em hardware real com latência medida.

### Sprint 3 — Aplicativo e Integração (App + UX + Deploy)
- **Objetivo:** aplicativo Flutter completo, publicado e resiliente.
- **Planejado:** telas de diagnóstico/histórico, design system, deploy, offline, mapa, perfil.
- **Concluído:** app com **5 telas** (Diagnóstico, Mapa, IoT, Enciclopédia, Perfil);
  inferência **on-device (~60 ms)** e na nuvem; **deploy no Railway** com PostgreSQL
  persistente; **MQTT Cloud (HiveMQ)**; GPS + mapa; sincronização offline→online; calibração
  de confiança (temperature scaling).
- **Dificuldades:** confiança “achatada” do INT8 (resolvida com temperature scaling T=0.25);
  race condition no GPS; Railway bloqueando portas MQTT (uso de WebSocket + renome de env vars);
  perda de dados por SQLite efêmero (migração para PostgreSQL persistente).
- **Decisões:** app como produto principal; design fiel a um mockup de referência.
- **Entrega:** aplicativo publicado + API em produção (`ceres.up.railway.app`).

---

## 7. Resultados Obtidos

### Produto final e funcionalidades
Sistema completo e funcional composto por app móvel, nó IoT e backend em nuvem:
- Diagnóstico de **10 categorias** (9 doenças + saudável) por foto, **cloud ou offline**;
- Histórico de diagnósticos e leituras IoT em tempo real (temperatura, umidade do ar/solo);
- Mapa georreferenciado de ocorrências; enciclopédia das doenças; perfil com exportação CSV;
- Sincronização automática dos diagnósticos feitos offline ao voltar a conexão.

**Figura 3 —** Casos de uso (`diagramas/casos_de_uso.png`).

### Métricas
| Métrica | Valor |
|---|---|
| Acurácia (float, laboratório) | 98,13% |
| Acurácia (INT8 embarcado, laboratório) | **95,76%** |
| Acurácia em campo real (documentada) | 20–30% |
| Tamanho do modelo (INT8) | 638 KB |
| Latência — ESP32-S3 | 692 ms |
| Latência — on-device (celular) | ~60 ms |
| Latência — nuvem | ~280–330 ms |
| Custo do nó de hardware | ~R$80 |

### Testes e validações
- **5/5 testes automatizados** no backend (motor de diagnóstico, MQTT, histórico);
- Validação **end-to-end** (galeria → inferência → resultado) no app;
- **Matriz de confusão INT8** em 2.734 imagens (95,76%);
- Benchmark do ESP32-S3 (10/10 corretos) e experimento Edge vs Cloud.

### Benefícios proporcionados
Triagem agronômica imediata, de baixo custo e funcionando sem internet — colocando na mão
do pequeno produtor uma ferramenta de apoio à decisão que antes dependia de especialista.

### Limitações identificadas
- **Gap laboratório-campo:** o modelo, treinado com imagens de fundo controlado
  (PlantVillage), cai para 20–30% em fotos de campo real — fenômeno documentado na
  literatura (Mohanty 2016; Singh 2020). É a principal limitação e o foco dos próximos passos.
- **Câmera embarcada (OV5640):** não integrada ao ESP32-S3 na entrega (prova de conceito).
- **Validação com usuários reais:** ainda não realizada com produtores em campo — planejada
  como etapa futura.

### Reflexão
- **Aprendizados:** transfer learning e quantização INT8 calibrada; comunicação IoT segura
  (MQTT/TLS); arquitetura offline-first; deploy em nuvem; a importância de **documentar
  resultados negativos** (o gap de campo não é fracasso — é achado).
- **Dificuldades enfrentadas:** compatibilidade de ambientes (GPU/WSL2), bibliotecas de
  TinyML descontinuadas, restrições de rede em PaaS.
- **Melhorias futuras:** dataset brasileiro de tomateiro (condições de MT), retreino com
  dados locais, câmera embarcada e validação com produtores.
- **Continuidade:** o projeto tem sequência natural como TinyML agrícola — “o gargalo é o
  dado, não o hardware”.

---

## 8. Anexos

### 8.1 Repositório GitHub
`https://github.com/Namem/extensao2` — código-fonte (backend, app, firmware), histórico de
commits, README e documentação em `docs/`.

### 8.2 Slides das Sprint Reviews
`docs/extensao/slides/` — apresentação Sprint MVP (`Ceres Diagnostico - Sprint MVP_ATT.pptx`)
e roteiro (`roteiro_ceres_sprint_mvp.pdf`).

### 8.3 Prints e fotos do projeto
- Fotos do hardware: `docs/extensao/assets/fotos_hardware/` (ESP32-S3, DHT22, sensor de solo, setup);
- Screenshots do app: `docs/extensao/assets/screenshots/`.

### 8.4 Documentação Técnica
Toda em `docs/extensao/`:
- **Diagrama de Casos de Uso** — `diagramas/casos_de_uso.png`
- **Diagrama de Classes** — `diagramas/diagrama_classes.png`
- **Modelo Entidade-Relacionamento (MER)** — `diagramas/mer.png`
- **Arquitetura do Sistema** — `diagramas/arquitetura.png`
- **Roadmap (linha do tempo)** — `diagramas/roadmap.png`
- **Documentação da API** — `API_CERES.md` / `documentacao_api_ceres.pdf`
- **Manual de Instalação** — `MANUAL_INSTALACAO.md` / `manual_instalacao_ceres.pdf`
- **Manual do Usuário** — `MANUAL_USUARIO.md` / `manual_usuario_ceres.pdf`
- **Backlog do Produto** — `BACKLOG_PRODUTO.md` / `backlog_produto_ceres.xlsx`
