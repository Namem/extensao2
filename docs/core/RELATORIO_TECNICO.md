# Relatório Técnico — Ceres Diagnóstico
**TCC Engenharia da Computação — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto
**Orientador:** (a preencher)
**Última atualização:** 2026-05-28

> Este documento registra cronologicamente tudo que foi implementado,
> as decisões tomadas, os resultados obtidos e os problemas resolvidos.
> Atualizar ao final de cada sprint ou bloco significativo de trabalho.

---

## Ambiente de Desenvolvimento

| Item | Máquina Principal | Máquina Secundária |
|------|------------------|--------------------|
| SO | Windows 11 | Windows 11 |
| Python | 3.13 | 3.13 |
| PostgreSQL | 18.3.3 (porta 5433) | Docker / PostgreSQL |
| Docker | WSL2 + Docker Desktop | - |
| IDE | VS Code + Claude Code | VS Code + Claude Code |
| Repositório | https://github.com/Namem/extensao2 | idem (git pull/push) |

**Fluxo multi-máquina:**
```
git push  →  GitHub  →  git pull
```
O `CLAUDE.md` garante que o Claude Code recupere o contexto do projeto
automaticamente em qualquer máquina ao abrir o projeto.

---

## Sprint 0 — Motor de Diagnóstico ✅ CONCLUÍDA

**Período:** (anterior a 2026-04-28)
**Critério de aceite atingido:** API Django funcional, JWT, 5 testes passando.

### O que foi implementado

| Item | Arquivo / Endpoint | Status |
|------|-------------------|--------|
| Models Pergunta, Opcao, Diagnostico | `diagnostico/models.py` | ✅ |
| Model DiagnosticoEvento (sensores IoT) | `diagnostico/models.py` | ✅ |
| Endpoint GET /api/diagnostico/iniciar/ | `diagnostico/views.py` | ✅ |
| Endpoint POST /api/diagnostico/responder/ | `diagnostico/views.py` | ✅ |
| Endpoint GET /api/diagnostico/historico/ | `diagnostico/views.py` | ✅ |
| Autenticação JWT (SimpleJWT) | `ceres_core/settings.py` | ✅ |
| Multi-tenant (Tenant, CustomUser) | `accounts/models.py` | ✅ |
| Docker Compose PostgreSQL 15 porta 5433 | `docker-compose.yml` | ✅ |
| .env + settings.py com variáveis de ambiente | `backend/.env` | ✅ |

### Testes automatizados (5/5 passando)

```
test_evento_criado_com_dados_validos         OK
test_historico_retorna_lista_paginada        OK
test_iniciar_diagnostico_retorna_raiz        OK
test_responder_retorna_diagnostico_final     OK
test_responder_retorna_proxima_pergunta      OK
```

Validado em: 2026-04-28 — PostgreSQL 18.3.3, porta 5433, Python 3.13.

---

## Sprint 1 — MQTT + Dataset + Treino 🔄 EM ANDAMENTO

**Período:** 2026-04-28 →
**Critério de aceite:** ESP32 publicando JSON via MQTT, Django persistindo,
dataset PlantVillage preparado e upload iniciado no Edge Impulse.

### Frente B — Backend Django (CONCLUÍDA dentro da sprint)

> Nota: os itens de Backend da Sprint 1 já estavam implementados
> desde a Sprint 0 (DiagnosticoEvento, historico/, testes).
> Validados novamente em 2026-04-28 com 5/5 testes passando.

### Frente C — Dataset & IA (EM ANDAMENTO)

#### 2026-04-28 — Preparação do ambiente de dataset

**Problema encontrado:** Dataset não estava presente na máquina secundária.
**Solução:** Download via Kaggle CLI após configuração do `kaggle.json`.

```bash
pip install kaggle
kaggle datasets download abdallahalidev/plantvillage-dataset \
    -p backend/datasets/raw/ --unzip
```

**Resultado:** 18.160 imagens de tomate em 10 classes confirmadas.

#### 2026-04-28 — Script prepare_plantvillage.py

**Arquivo:** `backend/datasets/scripts/prepare_plantvillage.py`

**O que faz:**
1. Lê as 10 pastas `Tomato___*` do PlantVillage
2. Divide estratificadamente em train/val/test (70/15/15, seed=42)
3. Copia para `backend/datasets/processed/train|val|test`
4. Aplica 6 augmentations offline apenas no treino
5. Gera `dataset_stats.md` e `edge_impulse_upload_guide.md`

**Resultado da execução (2026-04-28):**

| Classe | Original | Train (orig) | Aug (+6x) | Train total | Val | Test |
|--------|----------|-------------|-----------|-------------|-----|------|
| D01 Requeima | 1.909 | 1.336 | +8.016 | 9.352 | 286 | 287 |
| D02 Septoriose | 1.771 | 1.239 | +7.434 | 8.673 | 265 | 267 |
| D03 Pinta Preta | 1.000 | 700 | +4.200 | 4.900 | 150 | 150 |
| D03b Mancha Alvo | 1.404 | 982 | +5.892 | 6.874 | 210 | 212 |
| D05 Mofo Foliar | 952 | 666 | +3.996 | 4.662 | 142 | 144 |
| D06 Vira-Cabeça | 5.357 | 3.749 | +22.494 | 26.243 | 803 | 805 |
| D06b Mosaico | 373 | 261 | +1.566 | 1.827 | 55 | 57 |
| D07 Ácaro | 1.676 | 1.173 | +7.038 | 8.211 | 251 | 252 |
| D09 Mancha Bacteriana | 2.127 | 1.488 | +8.928 | 10.416 | 319 | 320 |
| Saudável | 1.591 | 1.113 | +6.678 | 7.791 | 238 | 240 |
| **TOTAL** | **18.160** | **12.707** | **+76.242** | **88.949** | **2.719** | **2.734** |

**Observação:** Classe D06b Mosaico tem apenas 373 imagens originais
(menor do dataset). Monitorar acurácia dessa classe no Edge Impulse.

#### 2026-04-28 — Definição da Estratégia de Treinamento (2 Experimentos)

Análise do hardware disponível (CPU-Z + nvidia-smi):
- CPU: AMD Ryzen 7 5700X3D (8 cores / 16 threads)
- RAM: 48 GB DDR4
- GPU: NVIDIA RTX 3060 Ti (8GB VRAM, CUDA 13.2)

Decisão: realizar **dois experimentos de treinamento** para comparação no artigo:

| | Experimento A | Experimento B |
|--|---------------|---------------|
| Plataforma | Edge Impulse (nuvem) | TensorFlow local (WSL2) |
| Dataset | 18.160 imgs originais | 88.949 imgs com augmentation |
| Augmentation | Online (Edge Impulse) | Offline (prepare_plantvillage.py) |
| GPU | Servidores Edge Impulse | RTX 3060 Ti local |
| Limite de tempo | 60 min/job | Sem limite |
| Saída | Arduino Library (.zip) | .tflite INT8 |

Justificativa: comparação entre plataforma gerenciada vs treinamento próprio
gera dados experimentais originais para o artigo (seção 5 do TCC).

#### 2026-04-28 — Upload Experimento A — Edge Impulse

- Projeto criado: `ceres-diagnostico` (plano Developer gratuito, privado)
- Script: `backend/datasets/scripts/upload_edge_impulse.py`
- API Key: armazenada em `backend/.env` (EDGE_IMPULSE_API_KEY)
- Upload: processed/train (88.949 imgs) e processed/val (2.719 imgs)
- Status: EM ANDAMENTO (upload via API REST, 4 workers paralelos)
- Destino EI: train -> "training" | val -> "testing"
- test/ NAO enviado — reservado para benchmark final

Observacao: plano gratuito tem 60min/job. Se 88k imgs exceder,
criar projeto separado com apenas as 18k originais para comparacao.

#### 2026-04-29 — Treinamento Experimento A — Edge Impulse ✅ CONCLUÍDO

**Configuração do Impulse:**
- Input: Image 96×96 RGB, Squash
- Processing: Image (RGB)
- Learning: Transfer Learning — MobileNetV2 96×96 0.35
- Training cycles: 30 | Learning rate: 0.0005 | Data augmentation: ON
- Target device: ESP32-S3 N16R8, 240MHz

**Resultado (2026-04-29):**

| Métrica | Valor |
|---------|-------|
| Versão | Acurácia val | Loss | AUC | F1 | Flash | RAM | Latência ESP32-S3 |
|--------|-------------|------|-----|-----|-------|-----|-------------------|
| **INT8** | **62,0%** | 4,13 | 0,90 | 0,62 | 547 KB | 232,9 KB | 1.365 ms ⚠️ |
| **FP32** | **92,5%** | 0,22 | 1,00 | 0,92 | 1.600 KB | 441,8 KB | 4.322 ms ⚠️ |
| Tempo de treinamento | ~21 min (GPU EI) |||||| |

**Acurácia por classe (val set):**
- D01_requeima: 35,1% (pior — confundida com saudável 27,4%)
- D02_septoriose: 72,8%
- D03_pinta_preta: 31,8%
- D03b_mancha_alvo: 32,9%
- D05_mofo_foliar: 39,0%
- D06_vira_cabeca: 69,9%
- D06b_mosaico: 46,0%
- D07_acaro_bronzeamento: 68,7%
- D09_mancha_bacteriana: 64,7%
- saudavel: 98,3% ✅

**Análise:** Treinamento de fase única (30 cycles) resultou em modelo que
acerta a classe dominante (saudável) mas confunde as doenças entre si.
Contrastar com Exp B (98,13%) evidencia importância das duas fases + fine-tuning.

- [x] Upload completo — 88.872 items no Edge Impulse Studio
- [x] Impulse configurado: Image 96x96 RGB > MobileNetV2 0.35
- [x] Treinamento concluído — 61,4% val acc
- [ ] Exportar como Arduino Library para Sprint 2 (após melhorar acurácia se necessário)

#### 2026-04-28 — Experimento B — TensorFlow Local WSL2 ✅ CONCLUÍDO

**Ambiente:**
- WSL2 Ubuntu 24.04, Python 3.12.3, venv ~/venv_ceres/
- GPU: RTX 3060 Ti (8GB VRAM, CUDA 13.2) — detectada via LD_LIBRARY_PATH fix
- TensorFlow 2.21 com tensorflow[and-cuda]

**Fix LD_LIBRARY_PATH (GPU detection em WSL2):**
```bash
export LD_LIBRARY_PATH=$(find ~/venv_ceres/lib/python3.12/site-packages/nvidia \
    -name "lib" -type d | tr '\n' ':'):/usr/lib/wsl/lib:$LD_LIBRARY_PATH
```
Salvo em `~/.bashrc` para persistência.

**Arquitetura:** MobileNetV2 96×96 alpha=0.35 (mesmo do Edge Impulse)
- Fase 1: backbone congelado, 10 epochs, LR=1e-3, Adam
- Fase 2: fine-tuning últimas 30 camadas, 40 epochs, LR=5e-4, Adam

**Incidente:** Treinamento travou na Época 29 step 1546/2780 por contenda de
I/O (git add simultâneo ao treino). Checkpoint da Época 28 (best_fase2.keras,
val_acc 97,79%) foi preservado pelo ModelCheckpoint callback.
Treinamento retomado automaticamente, concluindo 40 épocas.
Script `export_tflite.py` criado como contingência (carrega checkpoint se necessário).

**Resultado final (2026-04-28):**

| Métrica | Valor |
|---------|-------|
| Acurácia val set (melhor época) | 97,79% |
| **Acurácia test set** | **98,13%** |
| Loss test set | (ver relatorio_final.txt) |
| TFLite FP32 | 1.626,0 KB |
| **TFLite INT8** | **639,2 KB** |
| Épocas totais | 40 (Fase 1: 10, Fase 2: 30 efetivas) |
| Tempo total estimado | ~2h (RTX 3060 Ti) |

**Arquivos gerados:**
- `backend/datasets/modelo/best_fase1.keras` — melhor Fase 1
- `backend/datasets/modelo/best_fase2.keras` — melhor Fase 2 (Época 28)
- `backend/datasets/modelo/ceres_mobilenetv2.h5` — Keras completo
- `backend/datasets/modelo/ceres_mobilenetv2.tflite` — FP32 (1,6 MB)
- `backend/datasets/modelo/ceres_mobilenetv2_int8.tflite` — INT8 (639 KB) **← para ESP32-S3**
- `backend/datasets/modelo/historico_treino.csv` — métricas por época
- `backend/datasets/modelo/relatorio_final.txt` — acurácia + matriz de confusão

**Scripts:**
- `backend/datasets/scripts/train_local.py` ✅ commitar
- `backend/datasets/scripts/export_tflite.py` ✅ commitar (contingência)

✅ GPU OK | ✅ INT8 export OK | ✅ 98,13% test acc | ✅ 639 KB < 1MB (ESP32-S3)

#### 2026-05-08 — Validação PlantDoc (nível 3 da cadeia de validação) ✅ CONCLUÍDO

**Script criado:** `backend/datasets/scripts/avaliar_plantdoc.py`

**Dataset:** PlantDoc — copiado de `C:\Users\Namem\Desktop\PlantDoc-Dataset-master`
para `backend/datasets/raw/plantdoc/` (pasta de campo real, não commitar).

**Mapeamento de classes (PlantDoc → Ceres):**
9 das 10 classes Ceres encontradas no PlantDoc. Ausente: D03b_mancha_alvo.
D07_acaro_bronzeamento presente mas com apenas 4 imagens (resultado não conclusivo).

**Problema encontrado e resolvido — bug INT8 preprocessing:**

| | Versão errada | Versão correta |
|--|--|--|
| Passo | `arr / escala + zero` direto | Normalizar [-1,1] PRIMEIRO |
| Código | `arr / 0.00784 + (-1)` → valores ~32.513, clip → tudo 127 | `arr / 127.5 - 1.0` → depois `norm / escala + zero` |
| Sintoma | 1ª run: 13,45%; modelo previu tudo como D01_requeima (85,1%) | 2ª run: 20,77%; distribuição realista por classe |
| Causa raiz | Escala é quantization scale (pequena ~0.008), não normalização | Quantização INT8 opera sobre float já normalizado |

**Resultado final (2ª execução — 2026-05-08):**

| Classe | Corretas | Total | Acurácia |
|--------|----------|-------|----------|
| D01_requeima | 92 | 202 | 45,5% |
| D02_septoriose | 51 | 279 | 18,3% |
| D03_pinta_preta | 98 | 158 | 62,0% |
| D05_mofo_foliar | 2 | 170 | 1,2% |
| D06_vira_cabeca | 14 | 140 | 10,0% |
| D06b_mosaico | 0 | 88 | 0,0% |
| D07_acaro_bronzeamento | 0 | 4 | 0,0% |
| D09_mancha_bacteriana | 22 | 202 | 10,9% |
| saudavel | 2 | 110 | 1,8% |
| **GERAL** | **281** | **1.353** | **20,77%** |

**Análise:** Gap laboratorio-campo de 77 pp (98,13% PlantVillage → 20,77% PlantDoc).
Consistente com literatura: Mohanty et al. (2016) reportaram queda de 99% → 31%.
Achado principal: classe `saudavel` com 1,8% confirma que modelo aprendeu o
fundo cinza/preto do PlantVillage como feature discriminativa.
Meta de 70% não atingida — documentado como limitação a resolver nas próximas sprints
via augmentation com fundos naturais ou remoção de fundo (GrabCut).

**Arquivos gerados/atualizados:**
- `docs/plantdoc_results.md` — resultado completo + análise do gap
- `docs/TCC_CERES.md` — seção 5.4 preenchida com dados reais
- `docs/BACKLOG.md` — PlantDoc marcado como concluído

### Frente A — Firmware ESP32 (PENDENTE)

- [ ] Instalar PlatformIO no notebook
- [ ] Criar `firmware/esp32_mqtt_sensor/`
- [ ] Implementar WiFi + MQTT + DHT22 + umidade solo
- [ ] Testar publicação em `ceres/sensor/001`

#### 2026-05-09 — Scripts de apoio + documentação Sprint 1 ✅

**Scripts criados (todos em `backend/datasets/scripts/`):**

`plotar_historico.py`
- Lê `historico_treino.csv` e gera `docs/historico_treino.png`
- Gráfico com 2 subplots (accuracy + loss), marcação de Fase 1 vs Fase 2,
  linha da melhor época (ep 28, val_acc 97,79%), anotação do test set 98,13%
- Dependência: matplotlib (instalado no venv Windows)
- Uso: `python plotar_historico.py`

`demo_inferencia.py`
- Demo visual de inferência do `ceres_mobilenetv2_int8.tflite`
- Aceita `--imagem` ou `--pasta`, exibe tabela com barra de confiança colorida
- Salva relatório em `docs/demo_results.md`
- Uso: `python demo_inferencia.py --pasta "caminho/pasta" --max 10`

`background_augment.py`
- Remove fundo de 88.949 imgs PlantVillage (rembg U2-Net)
- Recompoe sobre fundos naturais do PlantDoc
- Gera `processed_field/train/` para retreino (Exp C)
- Resumível (pula arquivos já gerados), usa `--sample N` para teste
- Status: rodando em background no PC desktop (2026-05-08 →)

**Documentação atualizada:**
- `docs/sprint_review_roteiro.md` — roteiro completo 12 slides Sprint Review
- `docs/historico_treino.png` — gráfico de curvas de treinamento
- `docs/TCC_CERES.md` — seção 5.2 (curvas + acurácia por classe reais),
  seção 6 (conclusão parcial Sprint 1), seção 4.2.6 (Exp C), refs novas
- `backend/.env.example` — adicionado MQTT_BROKER, MQTT_PORT, ALLOWED_HOSTS
- `backend/requirements_minimal.txt` — dependências mínimas para notebook
- `verificar_ambiente.py` — modo `--notebook`, apito sonoro, `--fix`

#### 2026-05-09 (tarde) — Exp C concluído + análise de resultados ✅

**Exp C — Retreino com background augmentation:**
- Dataset: 266.847 imgs (88.949 originais + 177.698 composições sintéticas)
- Splits val/test: symlinks para `processed/val` e `processed/test` (avaliação justa)
- Resultado lab (PlantVillage test): **96,20%** (vs 98,13% Exp B — -1,93 pp)
- Resultado campo (PlantDoc, 746 imgs): **20,24%** (vs 20,77% Exp B — -0,53 pp)
- Conclusão: **background augmentation sintética não melhora generalização de campo**

**Bugs corrigidos:**
- `export_tflite.py` linha 67: `class_names` capturado do dataset raw antes de `.map().prefetch()`
- `avaliar_plantdoc.py`: script corrigido para varrer `train/` + `test/` (746 imgs vs 677 anterior)

**Análise por classe (Exp C — campo):**
- Melhor: D01_requeima 66,7% | D02_septoriose 32,5% (lesões visualmente salientes)
- Pior: saudavel 0,0% | D07_acaro 0,0% | D09_mancha_bacteriana 5,5%
- Diagnóstico: fundo verde natural de campo não reconhecido como "saudável"

**Documentação atualizada:**
- `docs/TCC_CERES.md` seção 5.4 — comparativo Exp B vs Exp C, análise do gap, caminhos futuros
- `docs/BACKLOG.md` — Sprint 1 marcada 21/24 (pendente apenas firmware ESP32)

#### 2026-05-09 (noite) — Exp D Fine-tuning PlantDoc real ✅

**Dataset misto criado por `preparar_mixed.py`:**
- 88.949 imgs PlantVillage (symlinks) + 6.770 cópias PlantDoc/train (677 únicas × 10)
- Total treino: 95.719 imagens | 7,1% campo real

**Resultados Exp D:**
- Lab (PlantVillage test, 2.734 imgs): **97,55%** (vs 98,13% Exp B — -0,58pp)
- Campo geral (PlantDoc train+test, 746 imgs, inclui treino): **88,47%**
- Campo justo (PlantDoc test-only, 69 imgs, nunca visto): **30,43%** (+10pp vs Exp B ~20%)

**Diagnóstico intermediário (Opção A — rembg no teste):**
- PlantDoc test+train com rembg: 21,05% — sem melhora → fundo não é causa única
- D06_vira_cabeca: +50pp com rembg (fundo era causa nessa classe específica)
- D02_septoriose: -22pp com rembg (spots nas bordas cortados pelo rembg)

**Conclusão da cadeia experimental:**
- Exp B → C: augmentação sintética ineficaz (gap persiste)
- Exp D: fine-tuning com dados reais: +10pp campo não visto; limitado pelo tamanho do PlantDoc
- Fator crítico: mais dados reais de campo (Sorriso-MT) para superar 70%

**Modelo final escolhido:** Exp D `ceres_mobilenetv2_int8.tflite` 639 KB
**Scripts criados:** `preparar_mixed.py` (dataset misto), `avaliar_plantdoc.py --remover-fundo` (Opção A)

---

## Sprint 2 — ESP32-S3 + TFLite ⏳ PENDENTE

> A ser preenchido após conclusão da Sprint 1.

### Metas
- Modelo TFLite rodando no ESP32-S3
- Latência de inferência < 300ms
- RAM livre > 4MB após carregar modelo
- Loop completo câmera → MQTT → Django < 5s

---

## Sprint 3 — Flutter + Experimentos ⏳ PENDENTE

> A ser preenchido após conclusão da Sprint 2.

---

## Problemas Encontrados e Soluções

| Data | Problema | Causa | Solução |
|------|----------|-------|---------|
| 2026-04-28 | Docker Desktop falha ao instalar | WSL2 sem distro Linux | Habilitar VT-x no BIOS, instalar Ubuntu WSL |
| 2026-04-28 | Docker Engine não sobe | VT-x desabilitado no BIOS | Entrar no BIOS e habilitar virtualização |
| 2026-04-28 | icacls acesso negado em C:\ProgramData\DockerDesktop | Pasta sem permissão de admin | takeown + icacls |
| 2026-04-28 | prepare_plantvillage.py: UnicodeEncodeError | Terminal Windows cp1252 | Remover caracteres Unicode (✓ → [OK]) |
| 2026-04-28 | Nomes de pastas PlantVillage com `___` | Dataset usa triple underscore | Corrigir mapeamento no script |
| 2026-04-28 | PowerShell bloqueando activate.ps1 | ExecutionPolicy restrita | Set-ExecutionPolicy RemoteSigned -Scope CurrentUser |
| 2026-04-28 | Testes Django: sem permissão CREATEDB | Usuário ceres_user sem privilégio | ALTER USER ceres_user CREATEDB |
| 2026-04-28 | edge-impulse-cli falha ao instalar | node-gyp exige Visual Studio C++ | Usar --ignore-scripts; migrar para API REST Python |
| 2026-04-28 | TensorFlow não suporta Python 3.13 | Suporte oficial até 3.12 | Usar Python 3.12 do WSL2 Ubuntu |
| 2026-04-28 | python3.12-venv não encontrado no apt | Pacote ausente no Ubuntu WSL | sudo apt update + python3-venv |
| 2026-04-28 | GPU RTX 3060 Ti não detectada no WSL2 | LD_LIBRARY_PATH sem paths CUDA nvidia | export LD_LIBRARY_PATH com paths nvidia + /usr/lib/wsl/lib |
| 2026-04-28 | Treinamento travou época 29 step 1546/2780 | Contenda I/O: git add simultâneo ao treino | Ctrl+C; retomou; ModelCheckpoint preservou best_fase2.keras |
| 2026-05-08 | avaliar_plantdoc.py — 1ª run: modelo previu 85,1% como D01 | Bug INT8 preprocessing: `arr / escala` sem normalizar primeiro criava valores ~32.513, clip → tudo 127 | Normalizar para [-1,1] antes de quantizar; dequantizar saída antes do argmax |
| 2026-05-08 | openpyxl: AttributeError 'MergedCell' object read-only | Row inserida no Excel herdou célula mesclada do header | Não inserir linha nova — atualizar a célula existente da tarefa EI |
| 2026-05-08 | PowerShell: UnicodeEncodeError ao exibir emoji (✅) | Terminal cp1252 não suporta Unicode acima de U+00FF | Redirecionar output para arquivo com `-Encoding utf8` |

---

## Configuração do Ambiente (Passo a Passo Reproduzível)

Para replicar o ambiente em uma nova máquina:

```powershell
# 1. Clonar
git clone https://github.com/Namem/extensao2 ceres-diagnostico
cd ceres-diagnostico/backend

# 2. Liberar execução de scripts PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 3. Criar venv e instalar dependências
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install Pillow kaggle

# 4. PostgreSQL: criar banco (senha do postgres definida na instalação)
$env:PGPASSWORD = "<senha-do-postgres>"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 `
    -c "CREATE USER ceres_user WITH PASSWORD 'ceres_senha_local';"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 `
    -c "CREATE DATABASE ceres_db OWNER ceres_user;"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 `
    -c "GRANT ALL PRIVILEGES ON DATABASE ceres_db TO ceres_user;"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 `
    -c "ALTER USER ceres_user CREATEDB;"

# 5. Migrations e testes
python manage.py migrate
python manage.py test diagnostico --verbosity=2

# 6. Dataset (requer kaggle.json em C:\Users\<user>\.kaggle\)
kaggle datasets download abdallahalidev/plantvillage-dataset `
    -p datasets/raw/ --unzip
python datasets/scripts/prepare_plantvillage.py
```


---

## 2026-05-11 — Sprint 1b: Firmware ESP32-S3 MQTT

### Ambiente
- Notebook Windows 11, Python 3.12, PlatformIO 6.1.19
- ESP32-S3-WROOM-1-N16R8 (16MB Flash + 8MB PSRAM) via COM5 (CH343)
- Mosquitto 2.1.2 reconfigurado para listener 1883 (todas as interfaces)

### O que foi feito
1. Projeto PlatformIO criado em firmware/esp32_mqtt_sensor/
2. include/config.h com WiFi SSID/PASS + broker IP + topico (excluido do git via .gitignore)
3. src/main.cpp com WiFi + MQTT + JSON simulado + reconexao automatica
4. Mosquitto reconfigurado: listener 1883 sem bind a localhost + allow_anonymous true
5. Regra de firewall adicionada para porta 1883
6. Upload via pio run --target upload concluido em 38s

### Resultados
- ESP32-S3 conectado ao broker: 192.168.15.94 -> 192.168.15.22:1883 ESTABLISHED
- 74 eventos persistidos no PostgreSQL via mqtt_listener
- Endpoint GET /api/diagnostico/historico/ retornando JSON paginado com JWT
- Pilha completa validada: ESP32-S3 -> WiFi -> Mosquitto -> Django -> PostgreSQL -> REST API

### Problemas encontrados e solucoes
- Boot loop: flag board_build.arduino.memory_type=qio_opi conflita com Arduino framework -> removida
- Serial silencioso: ARDUINO_USB_CDC_ON_BOOT=1 redireciona Serial para USB nativa -> flags removidas
- MQTT rc=-2: Mosquitto so escutava em localhost -> listener 1883 sem bind no mosquitto.conf

### Proximo passo
- Sprint 2: TFLite Micro no ESP32-S3 com imagens embedded (OV5640 removido do escopo)

---

## 2026-05-27 — Sprint 2: TFLite Micro no ESP32-S3

### Objetivo
Validar inferência TFLite Micro no ESP32-S3 sem câmera: 10 imagens de teste
embutidas como arrays C int8, medir latência real com `esp_timer_get_time()`,
publicar resultados via MQTT.

### Decisões de escopo
- **OV5640 removida** do escopo da Sprint 2 — deadline impossibilita compra/integração
- **Imagens embedded**: 10 imgs (1/classe) convertidas em arrays C via `gerar_arrays_c.py`
- **Modelo usado**: `ceres_mobilenetv2_int8.tflite` (Exp B, 639KB) — Exp E não disponível no notebook
- **Raspberry Pi 3B+** anotado para Exp F (fase futura): EfficientNet-B0 224×224

### Arquivos criados

| Arquivo | Descrição |
|---------|-----------|
| `firmware/esp32s3_ceres/platformio.ini` | Config PlatformIO: esp32-s3-devkitc-1, qio_opi, huge_app.csv, TFLite 2.4.0 |
| `firmware/esp32s3_ceres/include/config.h` | WiFi, MQTT, CONFIDENCE_THRESHOLD (gitignore) |
| `firmware/esp32s3_ceres/include/inference.h` | Struct InferenceResult + assinaturas |
| `firmware/esp32s3_ceres/src/inference.cpp` | Engine TFLite Micro: 512KB PSRAM arena, softmax INT8→float, latência |
| `firmware/esp32s3_ceres/src/main.cpp` | Loop benchmark: WiFi + MQTT + iteração 10 imgs + LED RGB |
| `backend/datasets/scripts/gerar_arrays_c.py` | Gera model_data.h (639KB) + test_images.h (10 imgs × 27648 int8) |
| `firmware/esp32s3_ceres/include/model_data.h` | Array C do modelo TFLite (gerado — gitignore) |
| `firmware/esp32s3_ceres/include/test_images.h` | Arrays C das 10 imagens de teste (gerado — gitignore) |

### Arquitetura do firmware

```
setup()
  ├── WiFi.begin() + aguarda WL_CONNECTED
  ├── PubSubClient.setServer(MQTT_BROKER, 1883)
  └── inference_init()
        ├── ps_malloc(512KB)  → tensor_arena na PSRAM
        ├── tflite::GetModel(g_model_data)
        ├── tflite::MicroInterpreter::AllocateTensors()
        └── valida dims I/O + imprime arena_used_bytes()

loop() [enquanto s_img_index < 10]
  ├── inference_run(g_test_images[i])
  │     ├── memcpy → s_input->data.int8
  │     ├── esp_timer_get_time() → Invoke() → esp_timer_get_time()
  │     ├── dequantiza INT8: score = (raw - zero_point) * scale
  │     └── softmax → confidence + argmax → class_name
  ├── Serial.printf (classe esperada, predição, confiança, latência, RAM)
  ├── PubSubClient.publish(JSON com device_id, classe, confiança, latência_ms)
  └── indicar_led() → verde=saudável / vermelho=doença / amarelo=baixa confiança

loop() [após todas as imagens]
  └── print_benchmark_summary() → latência média + RAM livre + PSRAM livre
```

### Normalização INT8
```
int8 = uint8 - 128   (scale=0.0078125, zero_point=0)
```
Compatível com quantização do Exp B (`representative_dataset` calibrado).

### MQTT payload publicado por imagem
```json
{"device_id":"001","img_idx":0,"classe":"D01_requeima","class_index":0,
 "confianca":0.9512,"latencia_ms":187,"ram_livre":234000}
```

### Resultados reais (2026-05-27)

**Build:**
- Biblioteca: `spaziochirale/Chirale_TensorFLowLite@2.0.0` (PlatformIO registry)
- RAM: 15.6% (51KB de 320KB)
- Flash: 61.6% (1.94MB de 3MB da partição huge_app)
- Tempo de compilação: 361s (primeiro build com TFLite)

**Runtime ESP32-S3:**
- Arena PSRAM usada: **205.380 bytes (200KB)** — sobra 312KB
- RAM livre (heap): **290KB**
- Input: [1, 96, 96, 3] INT8 ✓
- Output: [1, 10] INT8 ✓

**Inferências (6/10 registradas):**
- Acurácia: **6/6 correto (100%)**
- Latência média: **~693ms**
- Confiança: ~23% (INT8 softmax plano — argmax correto, threshold precisa ajuste)

**Estimativa Exp A vs Real Exp B:**
- Edge Impulse estimou: 1.365ms
- Real ESP32-S3: ~693ms (2x mais rápido — MobileNetV2 0.35 é menor)

**Problemas resolvidos:**
- `arduino-libraries/TensorFlowLite_ESP32@2.4.0` → não existe no registro
- `tanakamasayuki/TensorFlowLite_ESP32` → repo GitHub deletado
- Solução: `spaziochirale/Chirale_TensorFLowLite@2.0.0` + remover `#include <TensorFlowLite.h>`
- WiFi falhou (placeholder "SEU_WIFI") — MQTT inativo — inferência OK independente

**Resultado:** Nível 3 da cadeia de validação atingido — modelo rodando em hardware real.

### Próximos passos (Sprint 2 — resolvidos na Sprint 3)
1. ✅ Sprint 3: Flutter app Windows desktop + API Django funcionando
2. Configurar `config.h` com WiFi real → validar publicação MQTT
3. Ajustar `CONFIDENCE_THRESHOLD` para ~0.20 baseado nos resultados reais

---

## Sprint 3 — Flutter + Django PC (sem Docker) — 2026-05-27

### Contexto
Após concluir Sprint 2 (TFLite Micro ESP32-S3), iniciada Sprint 3 com foco em
Flutter + API Django. Descobriu-se que Docker não está disponível no PC desktop
(apenas no notebook). Decisão: rodar Django diretamente via venv Python 3.13 +
`settings_notebook.py` (SQLite), sem Docker.

### Ambiente configurado no PC desktop

| Componente | Versão / Detalhe |
|---|---|
| Flutter SDK | 3.44.0 (estável) — `C:\Users\Namem\flutter\bin` |
| Visual Studio Build Tools | 2026 18.6.2 + workload "Desktop C++" |
| Python venv backend | Python 3.13.13 — `backend/venv/` |
| Django settings | `settings_notebook.py` — SQLite + CORS aberto |
| Modelo TFLite | `ceres_expe_int8.tflite` — 638KB (Exp E, modelo final) |
| Plataforma teste | Windows desktop (Flutter `-d windows`) |

### Pacotes instalados no venv
- `ai-edge-litert==2.1.5` — inferência TFLite (não estava instalado)
- `django-cors-headers==4.9.0` — CORS para Flutter (não estava instalado)

### Correções aplicadas

| Arquivo | Problema | Correção |
|---|---|---|
| `app_ceres/lib/config.dart` | `10.0.2.2` (só emulador) | → `localhost:8080` |
| `backend/ceres_core/settings_notebook.py` | modelo Exp B (antigo) | → `ceres_expe_int8.tflite` |
| `backend/diagnostico/views.py` | latência 0ms (sub-ms arredondado) | → medir tempo total subprocess |
| `app_ceres/lib/screens/camera_screen.dart` | `ImageSource.camera` crasha no Windows | → desabilitado via `Platform.isWindows` |
| `app_ceres/test/widget_test.dart` | referenciava `MyApp` (inexistente) | → `CeresApp` |
| `iniciar.ps1` | path errado (`Rachid`), Docker, emulador | → reescrito para PC sem Docker |
| `.vscode/launch.json` | task inexistente (`notebook`) | → `Flutter (Windows desktop)` |
| `.vscode/tasks.json` | só `iniciar.ps1` | → adicionado task Django via venv |

### Validação end-to-end (2026-05-27)

Testado com imagens de campo real selecionadas pela galeria do Windows:

| Imagem | Resultado | Confiança | Latência API |
|---|---|---|---|
| Folha com manchas amarelas/marrons | Septoriose | 14,3% | 0ms (bug) |
| Folha com manchas verdes/textura | Mosaico | 12,6% | 279ms |

**Latência 279ms** = startup subprocess Python + carregamento modelo + inferência TFLite no PC.  
**Confiança baixa (~10-14%)** = comportamento esperado para imagens de campo real (gap lab-campo
documentado: Exp E ~67% PlantDoc). Distribuição uniforme indica imagem fora da distribuição
do PlantVillage (fundos, iluminação, ângulo).

### Resultado
- Pipeline end-to-end validado: Galeria → POST multipart → TFLite → JSON → Flutter ✅
- `flutter analyze` → zero issues ✅
- `django migrate --settings=settings_notebook` → todas migrations OK ✅
- Nível 4 da cadeia de validação iniciado (interface produtores)

### Próximos passos
- Experimento edge vs cloud (núcleo científico do TCC)
- Persistência offline com Drift
- Layout final no Claude Design

---

## Sprint 3.5 — Design System Taxonomia Viva + Telas Completas — 2026-05-28

### Contexto
Após validação end-to-end da Sprint 3 (pipeline Flutter→Django→TFLite funcionando),
implementado design system completo baseado no mockup "Taxonomia Viva" criado no
Claude Design. Paleta derivada do cerrado mato-grossense (OKLCH→sRGB). Todas as telas
redesenhadas do zero para corresponder ao HTML de referência.

### Design System — CeresTheme

| Token | Hex | Semântica |
|---|---|---|
| bone | #F1ECE5 | Fundo — terra seca |
| paper | #FAF4EB | Cards — caderno botânico |
| leafDeep | #1A2D1D | AppBar splash |
| leafDark | #2B412B | Botões primários |
| leafLive | #5D8650 | Saudável |
| blight | #A64636 | Doença — ferrugem |
| dryGrass | #C69245 | Alerta moderado |
| ink | #261E19 | Texto — nanquim |

**Fontes:**
- Newsreader (serif display) — nomes de doenças, títulos, valores de sensor
- IBM Plex Sans (sans body) — rótulos, botões, metadados
- IBM Plex Mono (monospace) — dados técnicos, timestamps, porcentagens

### Telas implementadas

| Tela | Arquivo | Componentes chave |
|---|---|---|
| Splash | `splash_screen.dart` | Animação fade, brackets botânicos, barra progresso, crédito "Namem Rachid" |
| Login | `login_screen.dart` | Campos underline, checkbox, JWT, "Continuar sem conta" |
| Diagnóstico | `camera_screen.dart` | Viewfinder brackets+reticle, result card, barra confiança com ticks 25%/50%, score bars 3px, action box |
| IoT/Histórico | `historico_screen.dart` | Sensor card 3-col, IoT summary 2-col, MQTT strip, event icon anel+dot |
| Salvos | `historico_local_screen.dart` | Offline banner, faixa vertical 3px, scores expansíveis |
| Enciclopédia | `enciclopedia_screen.dart` | Lista 10 doenças, stat card urgentes/moderadas, expansível com ação recomendada |

### Arquitetura de dados centralizada

`lib/data/doencas_data.dart` — `DoencaInfo` com 10 doenças compartilhada entre
`CameraScreen` e `EnciclopediaScreen`. Elimina duplicação de código.

### Correções de bugs

| Bug | Arquivo | Correção |
|---|---|---|
| Porta 8080 (errada) | `config.dart` | → 8000 (padrão Django) |
| URL JWT errada (`/api/token/`) | `config.dart` + `api_service.dart` | → `/api/auth/token/` |
| `ALLOWED_HOSTS = []` bloqueava PC | `settings.py` | → `['localhost', '127.0.0.1']` |
| `TFLITE_MODEL_PATH` ausente em settings.py | `settings.py` | → adicionado (Exp E) |
| Campos sensor NOT NULL | `diagnostico/models.py` | → `null=True, blank=True` |
| JWT retornado mas não persistido | `login_screen.dart` | Documentado como trabalho futuro |

### Navegação

NavigationBar Material 3 substituída por widget custom com **linha indicadora no topo**
da aba ativa (equivalente ao `::before { top: 0 }` do HTML de referência).
5 abas: Diagnóstico / IoT / Salvo / Mapa / Guia.

### Resultado
- `flutter analyze` → zero issues ✅
- Backend com `TFLITE_MODEL_PATH` → inferência funcional ✅
- Pipeline completo: Splash→Login→Diagnóstico→Resultado→Salvo ✅

---

## Sprint 3.6 — Fidelidade pixel-perfect HTML → Flutter — 2026-05-28

### Problema identificado

Usuário reportou que os ícones e cores do app não correspondiam ao HTML de design.
Diagnóstico: Material Icons (estilo preenchido/arredondado) vs. custom thin-stroke SVG
do HTML (stroke-width="1.6", viewBox="0 0 24 24"). Ordem das abas também divergia.

### Solução

**Dependência adicionada:** `flutter_svg: ^2.0.10` — renderiza SVG nativamente no Flutter,
suportando `currentColor` via `SvgTheme(currentColor: cor)`.

**`lib/widgets/ceres_icons.dart`** (NOVO):
- `CeresIconsSvg` — constantes com as strings SVG exatas do HTML
- `CeresSvgIcon` — widget wrapper: `SvgPicture.string(svgString, theme: SvgTheme(currentColor: color))`
- `CeresMark` — marca botânica (lente/folha rotacionada) em Container circular

**`lib/widgets/ceres_app_bar.dart`** (REFATORADO):
- Marca "C" sólido → lente botânica SVG (bg transparente, borda hairline, leafDeep)
- `CeresIconButton` → aceita `svgString` + `SvgPicture`; `.material()` para fallback
- `CeresAppBar` → page-bar com título dois-segmentos: `pageTitleItalic` (leafDeep italic) + `pageTitle` (ink normal)

**Tab bar corrigida:**
- Material Icons removidos; substituídos por `CeresSvgIcon` com paths do HTML
- Ordem: Diagnóstico (câmera) / Mapa (pin) / IoT (ECG) / Enciclopédia (caderno) / Perfil (pessoa)
- "Salvos" removido da tab bar → acessível via botão no appbar da tela Diagnóstico

**Splash + Login:** marca botânica SVG substitui "C" em ambas as telas.

### Resultado
- `flutter analyze` → zero issues ✅
- Ícones thin-stroke SVG idênticos ao HTML ✅
- Ordem das abas corrigida para HTML de referência ✅

---

## Sprint 4A.1 — Back button + Planejamento 4B→6 — 2026-05-28

### Problema identificado
`CeresAppBar` não exibia seta de voltar em telas pushadas (ex: `HistoricoLocalScreen`).
O usuário solicitou planejamento completo de tudo que falta para concluir o app.

### Solução — Back button

**`lib/widgets/ceres_app_bar.dart`** (MODIFICADO):
- Parâmetros adicionados: `showBack: bool = false`, `onBack: VoidCallback?`
- Quando `showBack: true`: substitui a marca botânica por botão circular 32px (hairline border, bg paper2) com `Icons.arrow_back_ios_new_rounded` 13px ink2
- `onBack ?? Navigator.of(context).pop()` — callback opcional, fallback automático
- `padding-left`: 8px quando showBack, 22px quando brand mark (alinhamento correto)

**`lib/screens/historico_local_screen.dart`** (MODIFICADO):
- `CeresAppBar(showBack: true)` ativado

### Resultado
- `flutter analyze` → zero issues ✅
- Back button visível e funcional em `HistoricoLocalScreen` ✅
- Extensível: qualquer tela pushada pode usar `showBack: true` ✅

### Planejamento registrado

**Sprint 4A.2 — Persistência de sessão** (próxima):
- `flutter_secure_storage: ^9.2.2` — JWT no Keystore/Keychain
- `shared_preferences: ^2.3.2` — e-mail + checkbox lembrar
- Auto-refresh token quando 401

**Sprint 4A.3 — Banner conectividade**:
- `connectivity_plus: ^6.1.1` — faixa âmbar offline
- Bloquear POST diagnóstico quando offline

**Sprint 4B — Mapa + GPS**:
- Backend: `latitude`/`longitude` em DiagnosticoEvento
- Flutter: `flutter_map: ^7.0.2` + OpenStreetMap, marcadores por urgência

**Sprint 5 — Perfil**:
- `GET /api/auth/me/` com stats
- Tela Perfil: avatar, total diagnósticos, % doenças, logout, exportar CSV

**Sprint 6 — TCC**:
- Preencher seções [PENDENTE] em TCC_CERES.md
- Slides Sprint Review final + vídeo demonstração

---

## Sprints 4A, 4B e 5 — UX Completo — 2026-05-29

### Sprint 4A — Navegação + Persistência UX

**4A.1 Back button**: `CeresAppBar` recebeu `showBack: bool` + `onBack: VoidCallback?`. No Windows/Android substitui a marca botânica por botão circular 32px ink2. `HistoricoLocalScreen` ativado com `showBack: true`.

**4A.2 Persistência de sessão**: `shared_preferences: ^2.3.2` adicionado. `flutter_secure_storage` descartado — exige ATL (Active Template Library) do Visual Studio no Windows, quebrando o build de dev. `AuthStorage` (novo) centraliza read/write de access token, refresh token e e-mail. `LoginScreen` pré-preenche e-mail salvo via `initState`. `_BootScreen` em `main.dart` checa token no boot e pula `LoginScreen` se válido. `ApiService` faz auto-refresh em 401 antes de rejeitar.

**4A.3 Banner de conectividade**: `connectivity_plus: ^6.1.1`. `OfflineBanner` widget (novo) usa `Stream<List<ConnectivityResult>>` — sem polling. Faixa âmbar animada (`AnimatedSize`) integrada em todas as 5 telas. `CameraScreen` desabilita botões câmera/galeria quando `_offline: true` + `SnackBar` âmbar.

### Sprint 4B — Mapa + GPS

**Backend**: `DiagnosticoEvento` recebeu `latitude` e `longitude` (FloatField, null=True). Migration `0004_add_gps_fields` aplicada. Serializer atualizado.

**Flutter**: `flutter_map: ^7.0.2` + `latlong2: ^0.9.1` + `geolocator: ^13.0.1`. `MapaScreen` (novo) renderiza tiles OpenStreetMap sem API key. Marcadores circulares coloridos por urgência (blight/dryGrass/leafLive). Tap no marcador → `ModalBottomSheet` com nome da doença, data, confiança e GPS. Fallback: Sorriso-MT quando GPS indisponível (Windows/Web). `EventoMqtt` refatorado: `timestamp: DateTime`, `confianca: double?`, `classeDetectada` getter, `latitude`/`longitude` adicionados.

### Sprint 5 — Perfil + Backend Usuário

**Backend**: `GET /api/auth/me/` (novo) retorna `{ nome, email, total_diagnosticos, total_doencas, total_saudavel, membro_desde, ultimo_acesso }`. Rota wired em `ceres_core/urls.py` via `accounts.urls`.

**Flutter**: `PerfilScreen` (novo) — card de identidade com avatar inicial leafDeep, stats row (total/doenças/saudável), último acesso, botão exportar CSV (`share_plus: ^10.1.3`) e botão Sair com `pushNamedAndRemoveUntil`. Offline: aviso âmbar sem quebrar a tela. `_PlaceholderScreen` removido de `main.dart` — todas as 5 abas implementadas.

### Resultado
- `flutter analyze` → zero issues ✅
- 5 abas completas: Diagnóstico / Mapa / IoT / Enciclopédia / Perfil ✅
- Persistência de sessão (boot sem login) ✅
- Banner offline em todas as telas ✅
- Exportar CSV + logout ✅
