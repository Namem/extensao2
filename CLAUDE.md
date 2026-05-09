# Ceres Diagnóstico — Contexto para Claude Code

## Como retomar o contexto em uma nova sessão
Leia ESTE arquivo (CLAUDE.md) — ele é suficiente para retomar qualquer sprint.
Se precisar de detalhes técnicos específicos, leia também:
  docs/RELATORIO_TECNICO.md  → log cronológico completo de tudo implementado
  docs/BACKLOG.md            → estado atual de cada tarefa
  docs/plantdoc_results.md   → resultado da validação campo real

## Projeto
TCC de Engenharia da Computação — IFMT Cuiabá.
Sistema embarcado de detecção precoce de doenças no
tomateiro: ESP32-S3 TinyML + Django REST + Flutter.
Autor: Namem Rachid Jaudy Neto

## Pasta de artefatos pré-existentes
Pre_arquivos/ (dentro da raiz do projeto) contém:
- SprintReview_1_CeresDiagnostico.pptx (Sprint 0)
- Backlog Projeto Ceres Diagnóstico V2.xlsx (backlog)
- guia_sprint_review.pdf
Antes de criar ou atualizar qualquer documentação,
SEMPRE leia o backlog existente nessa pasta.

## Stack
Backend : Django REST + PostgreSQL 18 (porta 5433, instalado direto no Windows)
          + SimpleJWT + paho-mqtt
App     : Flutter + Dart + Drift (cache SQLite)
Hardware: ESP32-S3 N16R8 + OV5640 5MP (a comprar)
          ESP32 genérico (disponível agora, usar no notebook com WiFi)
IoT     : MQTT Mosquitto + broker local
AI      : TFLite Micro + Edge Impulse (Exp A) + TensorFlow local WSL2 (Exp B)
          Modelo: MobileNetV2 96x96 INT8 quantizado

## Máquinas de desenvolvimento
PC DESKTOP (principal — treinamento pesado):
  Windows 11 + Python 3.13 + WSL2 Ubuntu
  GPU: NVIDIA RTX 3060 Ti 8GB VRAM, CUDA 13.2
  PostgreSQL 18.3.3 na porta 5433 (sem Docker)
  Mosquitto 2.1.2 em localhost:1883
  venv backend: backend/venv/ (Windows, Python 3.13)
  venv treino:  ~/venv_ceres/ (WSL2, Python 3.12)

NOTEBOOK (firmware + testes WiFi):
  Usar para: firmware ESP32 (precisa mesma rede WiFi que o ESP32)
  Usar para: testes de campo, Sprint 2 e 3
  NÃO usar para: treinamento pesado (sem GPU dedicada)

## Repositório
https://github.com/Namem/extensao2
Fluxo: git push (PC) → GitHub → git pull (notebook)
Commits: apenas o autor commita — Claude só sugere o comando

## Dataset oficial do projeto
PRIMARY  : PlantVillage (Hughes & Salathé 2015)
           ~18.160 imagens de folha de tomate, 10 classes — CC BY 4.0
           Processado em: backend/datasets/processed/train|val|test
           88.949 imgs de treino após augmentation offline (seed=42)
FIELD AUG: processed_field/ — PlantVillage com fundos naturais do PlantDoc
           Gerado por background_augment.py (rembg U2-Net)
           NÃO commitar — .gitignore
VALIDAÇÃO: PlantDoc (~1.353 imgs campo real)
           backend/datasets/raw/plantdoc/ — NÃO commitar
OUTROS   : Qualquer dataset pode ser usado se necessário (Roboflow, Kaggle,
           Hugging Face, etc.) — desde que documentado em
           docs/FUNDAMENTACAO_TECNICA.md com justificativa e licença
ATENÇÃO  : Roboflow "Tomato Fruit Disease Detection" é Object Detection
           de fruto (bounding box) — incompatível com classificação de
           folhas. Só usar se a tarefa mudar para detecção de objetos.

## As 10 classes do Ceres (mapeamento PlantVillage → Ceres)
PlantVillage (pasta)                              → Código Ceres
Tomato___Bacterial_spot                           → D09_mancha_bacteriana
Tomato___Early_blight                             → D03_pinta_preta
Tomato___Late_blight                              → D01_requeima
Tomato___Leaf_Mold                                → D05_mofo_foliar
Tomato___Septoria_leaf_spot                       → D02_septoriose
Tomato___Spider_mites Two-spotted_spider_mite     → D07_acaro_bronzeamento
Tomato___Target_Spot                              → D03b_mancha_alvo
Tomato___Tomato_Yellow_Leaf_Curl_Virus            → D06_vira_cabeca
Tomato___Tomato_mosaic_virus                      → D06b_mosaico
Tomato___healthy                                  → saudavel

## Experimentos de treinamento — AMBOS CONCLUÍDOS

Exp A — Edge Impulse (nuvem) ✅ CONCLUÍDO:
  Resultados: FP32 92,5% val acc / INT8 62,0% val acc
  Tamanho: FP32 1.637KB / INT8 624KB
  Latência estimada ESP32-S3: 1.365ms (INT8), 4.322ms (FP32)
  Arquivos: backend/datasets/modelo/ei_ceres_fp32.tflite
            backend/datasets/modelo/ei_ceres_int8.tflite
  PROBLEMA: quantização INT8 automática sem representative_dataset
            causou queda de 30pp (92.5% → 62.0%)

Exp B — TensorFlow local (WSL2) ✅ CONCLUÍDO — MODELO ESCOLHIDO:
  Ambiente: WSL2 Ubuntu, Python 3.12, ~/venv_ceres/
  GPU: RTX 3060 Ti via tensorflow[and-cuda]
  LD_LIBRARY_PATH: salvo em ~/.bashrc (nvidia paths + /usr/lib/wsl/lib)
  Fase 1: 10 epochs, LR=1e-3, backbone congelado
  Fase 2: 40 epochs, LR=5e-4, fine-tuning últimas 30 camadas
  Resultados: 98,13% test acc (2.734 imgs nunca vistas)
  Tamanho INT8: 639KB (com representative_dataset calibrado)
  Arquivo principal: backend/datasets/modelo/ceres_mobilenetv2_int8.tflite ← ESP32

Exp C — Background Augmentation + Retreino 🔄 EM ANDAMENTO (PC desktop):
  Objetivo: resolver gap lab-campo (98,13% PlantVillage → 20,77% PlantDoc)
  Causa do gap: modelo aprendeu fundo cinza do PlantVillage como feature
  Estratégia: rembg (U2-Net) remove fundo + recompõe sobre fundos naturais PlantDoc
  Base científica: Singh et al. 2020 — recorte de fundo: +40,8pp no PlantDoc
  Script: backend/datasets/scripts/background_augment.py
  Dataset gerado: backend/datasets/processed_field/train/ (NÃO commitar)
  Retreino: train_local.py --data-dir datasets/processed_field (WSL2)
  Meta: > 50% PlantDoc (conservador) / > 70% (meta TCC)
  FAZER NO PC ANTES DO NOTEBOOK (RTX 3060 Ti necessário)

Por que Exp B > Exp A:
  1. Duas fases de treinamento (transfer learning correto)
  2. Quantização INT8 com 50 batches do val set para calibração
  3. EarlyStopping + ReduceLROnPlateau evitam overfitting

YOLO foi descartado: detector de objetos (bounding box), não classificador.
Incompatível com classificação de folha única. Tamanho mínimo ~6MB vs 639KB.

## Estado atual das sprints (2026-05-08)

Sprint 0: ✅ CONCLUÍDA — API Django + Motor IA + JWT (5/5 testes, 8/8 tarefas)

Sprint 1: 🔄 QUASE CONCLUÍDA (17/24 tarefas)
  ✅ Dataset PlantVillage: 18.160 imgs → 88.949 imgs (augmentation x6)
  ✅ Exp A (Edge Impulse): FP32 92,5% / INT8 62,0% — documentado
  ✅ Exp B (TF local WSL2): 98,13% test acc, INT8 639KB — ESCOLHIDO
  ✅ Backend Django MQTT: DiagnosticoEvento + mqtt_listener + historico/
  ✅ Mosquitto 2.1.2 instalado e testado (localhost:1883)
  ✅ 5/5 testes passando (inclui MQTT)
  ✅ Validação PlantDoc: 20,77% em 1.353 imgs campo real — gap documentado
  ✅ background_augment.py criado — rodando no PC (processamento lento)
  ⏳ Retreino Exp C: aguarda background_augment.py terminar (WSL2, RTX 3060 Ti)
  ⏳ Firmware ESP32 genérico: FAZER NO NOTEBOOK (mesma rede WiFi que o ESP32)

Sprint 2: ⏳ PENDENTE — precisa ESP32-S3 N16R8 + OV5640 (a comprar)
  - Carregar ceres_mobilenetv2_int8.tflite no ESP32-S3
  - Medir latência real com esp_timer_get_time()
  - Benchmark 50 imgs: Python vs ESP32

Sprint 3: ⏳ PENDENTE — Flutter + experimento edge vs cloud + artigo
Sprint 4+: ⏳ PENDENTE — defesa TCC

## Cadeia de validação do modelo
Nível 1 ✅ FEITO:  Test set PlantVillage — 98,13% (2.734 imgs controladas)
Nível 2 ✅ FEITO:  PlantDoc campo real — 20,77% em 1.353 imgs (gap documentado)
         🔄 EM ANDAMENTO: Exp C retreino com fundos naturais — meta > 70%
Nível 3 ⏳ Sprint 2: Hardware real ESP32-S3 — latência real + comparação Python
Nível 4 ⏳ Sprint 3: Produtores de Sorriso-MT — validação com usuários reais

## O que fazer no PC antes de ir para o notebook
1. ⏳ Aguardar background_augment.py terminar (pode demorar horas — deixar rodando)
2. ⏳ Retreinar no WSL2:
     wsl && source ~/venv_ceres/bin/activate
     python3 .../train_local.py --data-dir datasets/processed_field
3. ⏳ Rodar avaliar_plantdoc.py e medir melhora
4. ✅ Commitar tudo e git push antes de ir para o notebook

## O que fazer no notebook
1. git pull
2. python verificar_ambiente.py --notebook  (apita se faltar algo)
3. Firmware ESP32 genérico MQTT:
   - Criar firmware/esp32_mqtt_sensor/ com PlatformIO
   - WiFi + MQTT + DHT22 + umidade solo
   - Testar com mosquitto_sub

## Verificação de ambiente
Script: verificar_ambiente.py (na raiz do projeto)
  python verificar_ambiente.py --notebook   # modo focado + apito se faltar algo
  python verificar_ambiente.py --fix        # tenta corrigir automaticamente
  python verificar_ambiente.py --wsl        # + verificações GPU WSL2
Apito: 5 bipes agudos = erro crítico | 2 bipes = avisos | 1 bipe = tudo OK

## Mosquitto — como iniciar
  Windows: serviço "mosquitto" sobe automaticamente
  Config: C:\Program Files\mosquitto\mosquitto.conf
          (listener 1883 localhost / allow_anonymous true)

## Como retomar o treinamento WSL2
  wsl
  source ~/venv_ceres/bin/activate
  # GPU já configurada no .bashrc (LD_LIBRARY_PATH com paths nvidia + /usr/lib/wsl/lib)
  python3 /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/scripts/train_local.py
  # Para Exp C (background augmentation):
  python3 .../train_local.py --data-dir datasets/processed_field
  # Se travar: usar export_tflite.py para exportar do checkpoint salvo

## Scripts principais
backend/datasets/scripts/
  prepare_plantvillage.py   → prepara dataset (split + augmentation offline)
  train_local.py            → treina MobileNetV2 WSL2 (aceita --data-dir)
  export_tflite.py          → exporta FP32 + INT8 calibrado
  avaliar_plantdoc.py       → avalia modelo no PlantDoc (campo real)
  background_augment.py     → remove fundo + recompõe sobre fundos naturais
verificar_ambiente.py       → checklist de ambiente com apito sonoro

## Regras Comportamentais (Token & Time Saving)
- NUNCA usar `read` em arquivos de log grandes. Usar `bash` com
  `tail -n 50` ou `grep` para extrair apenas a parte relevante
- Edição estrita: NUNCA reescrever arquivo inteiro. Usar sempre
  substituição pontual (search/replace) apenas nas funções afetadas
- NUNCA executar scripts bloqueantes via bash por conta própria:
  train_local.py, background_augment.py, qualquer treinamento ou
  processamento pesado. Fornecer apenas o comando para o usuário rodar
- Anti-Yapping: respostas puramente técnicas. Sem "Aqui está o código",
  "Entendi perfeitamente", "Espero que ajude". Apenas arquitetura e execução
- Fail Fast: se script falhar por dependência faltando, parar imediatamente,
  reportar o erro de forma concisa e aguardar instrução. Não tentar adivinhar

## Skills de Prompt
- Pensamento explícito: em tarefas complexas (integração MQTT, alocação
  ESP32, arquitetura nova), usar <thinking> para mapear a solução em
  bullet points ANTES de gerar código
- Validação de escopo: ao analisar bugs, limitar busca apenas às pastas
  relevantes informadas. Não vasculhar o repositório inteiro
- Dry Run Flutter (Sprint 3): para UI Flutter, gerar primeiro a árvore
  de widgets em texto simples. Só gerar código Dart após aprovação
- Git: ao sugerir commit, gerar APENAS um bloco bash com `git add`
  específico + `git commit -m "..."` em Conventional Commits. Não executar

## Regras de código
- Python  : PEP8, docstrings em português
- Dart    : dart format, comentários em português
- C++     : PlatformIO, um arquivo por módulo
- Commits : Conventional Commits (feat/fix/chore/docs)
- Nunca commitar secrets — usar .env
- Claude NUNCA commita — apenas sugere o comando

## Regras de processo
- Antes de implementar: mostrar o que vai fazer e explicar como funciona
- Após cada implementação: fornecer passo a passo para testar
- Após cada bloco de mudanças: sugerir commit (sem co-autor Claude)
- Antes de criar documentação: ler backlog em Pre_arquivos/
- Após qualquer implementação que der certa: SEMPRE atualizar
  TCC_CERES.md, RELATORIO_TECNICO.md e FUNDAMENTACAO_TECNICA.md
- Após qualquer implementação que der certa: SEMPRE atualizar
  docs/BACKLOG.md marcando o que foi concluído, OU perguntar ao
  usuário se pode atualizar antes de fazê-lo

## Regra de fundamentação técnica
SEMPRE que uma tecnologia, método, biblioteca ou arquitetura
for adicionada OU removida do projeto, atualizar:
  docs/FUNDAMENTACAO_TECNICA.md
com justificativa técnica, comparativo com alternativas e
referência acadêmica (Google Scholar, PMC, Springer, IEEE).
Obrigatório para a defesa do TCC.

## Documentos vivos (atualizar ao final de cada implementação)
docs/TCC_CERES.md             → rascunho do TCC, seções [PENDENTE] a preencher
docs/RELATORIO_TECNICO.md     → log cronológico de tudo implementado
docs/FUNDAMENTACAO_TECNICA.md → justificativa técnica + refs acadêmicas
SEMPRE atualizar os três ao final de cada sprint ou bloco significativo.

## Estrutura de pastas
backend/                    → Django REST API + datasets/
backend/venv/               → venv Windows (Python 3.13)
backend/datasets/raw/       → dataset bruto Kaggle (NÃO commitar)
backend/datasets/processed/ → train|val|test PlantVillage (NÃO commitar)
backend/datasets/processed_field/ → train com fundos naturais (NÃO commitar)
backend/datasets/modelo/    → modelos .tflite (commitar os < 2MB)
backend/datasets/scripts/   → scripts Python (commitar)
app_ceres/                  → Flutter
firmware/                   → ESP32 (criar na Sprint 1b/2)
docs/                       → TCC, relatório, fundamentação, benchmarks
Pre_arquivos/               → artefatos pré-existentes (não editar)
verificar_ambiente.py       → checklist de ambiente (raiz do projeto)
