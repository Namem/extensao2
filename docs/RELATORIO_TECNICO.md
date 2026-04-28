# Relatório Técnico — Ceres Diagnóstico
**TCC Engenharia da Computação — IFMT Sorriso-MT**
**Autor:** Namem Rachid Jaudy Neto
**Orientador:** (a preencher)
**Última atualização:** 2026-04-28

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

#### PENDENTE — Upload Edge Impulse

- [ ] Criar conta/projeto no Edge Impulse
- [ ] Upload de `processed/train/` e `processed/val/`
- [ ] Configurar Impulse: MobileNetV2 96x96 RGB INT8
- [ ] Treinar e registrar acurácia aqui

### Frente A — Firmware ESP32 (PENDENTE)

- [ ] Instalar PlatformIO
- [ ] Criar `firmware/esp32_mqtt_sensor/`
- [ ] Implementar WiFi + MQTT + DHT22 + umidade solo
- [ ] Testar publicação em `ceres/sensor/001`

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
