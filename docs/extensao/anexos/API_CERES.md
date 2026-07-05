# Documentação da API — Ceres Diagnóstico

**Atividade de Extensão II — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto

API REST do sistema Ceres Diagnóstico, construída em **Django REST Framework**.
Fornece autenticação JWT, motor de diagnóstico por árvore de decisão, inferência
de imagem por IA (TFLite) e histórico de eventos IoT (ESP32 via MQTT).

---

## 1. Informações gerais

| Item | Valor |
|---|---|
| Base URL (produção) | `https://ceres.up.railway.app/api/` |
| Base URL (local) | `http://localhost:8000/api/` |
| Formato | JSON (exceto `/inferir/`, que usa `multipart/form-data`) |
| Autenticação | JWT (Bearer Token) via SimpleJWT |
| Encoding | UTF-8 |
| Conta de teste | `test@test.com` / `test123` |

### Autenticação

A maioria dos endpoints é **pública** (`AllowAny`) — decisão de projeto para que o
produtor no campo use o diagnóstico sem barreira de login. Endpoints que dependem
do usuário (`/auth/me/`) exigem o header:

```
Authorization: Bearer <access_token>
```

O token `access` expira e é renovado com o `refresh` em `/auth/token/refresh/`.

---

## 2. Endpoints de Autenticação (`/api/auth/`)

### 2.1 Obter token — `POST /api/auth/token/`

Autentica o usuário e retorna o par de tokens JWT.

**Request (JSON):**
```json
{ "username": "test@test.com", "password": "test123" }
```

**Response 200:**
```json
{
  "access":  "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Erros:** `401` credenciais inválidas.

---

### 2.2 Renovar token — `POST /api/auth/token/refresh/`

**Request:** `{ "refresh": "<refresh_token>" }`
**Response 200:** `{ "access": "<novo_access_token>" }`

---

### 2.3 Cadastro — `POST /api/auth/register/`

Cria um novo usuário (produtor ou agrônomo).

**Request (JSON):**

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `nome` | string | sim | Nome completo |
| `email` | string | sim | Usado como `username` |
| `senha` | string | sim | Mínimo 6 caracteres |
| `tipo` | string | não | `produtor` (padrão) ou `agronomo` |
| `crea` | string | condicional | Obrigatório se `tipo = agronomo` |

**Response 201:** `{ "mensagem": "Conta criada com sucesso.", "tipo": "produtor" }`

**Erros:** `400` campos faltando, e-mail inválido, senha curta, CREA ausente para
agrônomo, ou e-mail já cadastrado.

---

### 2.4 Redefinir senha — `POST /api/auth/reset-password/`

Troca a senha diretamente (sem e-mail de confirmação — limitação documentada:
Railway bloqueia portas SMTP).

**Request:** `{ "email": "user@x.com", "nova_senha": "novaSenha123" }`
**Response 200:** `{ "mensagem": "Senha alterada com sucesso." }`
**Erros:** `400` campos faltando / senha curta · `404` e-mail não cadastrado.

---

### 2.5 Perfil do usuário — `GET /api/auth/me/`  🔒

Retorna dados e estatísticas do usuário autenticado. **Requer JWT.**

**Response 200:**
```json
{
  "nome": "Namem Rachid",
  "email": "test@test.com",
  "username": "test@test.com",
  "total_diagnosticos": 42,
  "total_doencas": 30,
  "total_saudavel": 12,
  "membro_desde": "06/2026",
  "ultimo_acesso": "04/07/2026 14:22"
}
```

**Erros:** `401` sem token / token inválido.

---

## 3. Endpoints de Diagnóstico (`/api/diagnostico/`)

### 3.1 Iniciar triagem — `GET /api/diagnostico/iniciar/`

Retorna a **pergunta raiz** da árvore de decisão (motor por sintomas).

**Response 200:**
```json
{
  "tipo": "pergunta",
  "dados": {
    "id": 1,
    "texto": "Em qual parte da planta está o problema?",
    "opcoes": [
      { "id": 1, "texto": "Na folha" },
      { "id": 2, "texto": "No caule" }
    ]
  }
}
```

**Erros:** `404` árvore vazia (sem perguntas cadastradas).

---

### 3.2 Responder — `POST /api/diagnostico/responder/`

Avança na árvore. Retorna a **próxima pergunta** ou o **diagnóstico final**.

**Request:** `{ "opcao_id": 1 }`

**Response 200 (próxima pergunta):**
```json
{ "tipo": "pergunta", "dados": { "id": 5, "texto": "...", "opcoes": [...] } }
```

**Response 200 (diagnóstico final):**
```json
{
  "tipo": "diagnostico",
  "dados": {
    "id": 3,
    "nome": "Requeima",
    "descricao": "Doença causada por Phytophthora infestans...",
    "recomendacao_manejo": "Aplicar fungicida cúprico; eliminar folhas..."
  }
}
```

**Erros:** `400` `opcao_id` ausente · `404` opção inexistente.

---

### 3.3 Inferência por imagem — `POST /api/diagnostico/inferir/`

Recebe a foto de uma folha e retorna a classificação da IA (modelo TFLite INT8).
Persiste o resultado como `DiagnosticoEvento` (alimenta o mapa de ocorrências).

**Request (`multipart/form-data`):**

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `imagem` | arquivo (JPEG/PNG) | sim | Foto da folha |
| `latitude` | float | não | GPS enviado pelo app |
| `longitude` | float | não | GPS enviado pelo app |

**Response 200:**
```json
{
  "classe": "D01_requeima",
  "class_index": 0,
  "confianca": 0.857,
  "latencia_ms": 279,
  "scores": {
    "D01_requeima": 0.857,
    "D02_septoriose": 0.032,
    "D09_mancha_bacteriana": 0.081,
    "saudavel": 0.004
  }
}
```
> `scores` traz a probabilidade das **10 classes** (softmax com temperature scaling T=0.25).

**Erros:** `400` imagem ausente · `503` modelo não encontrado ·
`504` timeout (>30s) · `500` falha na inferência.

> As 10 classes possíveis: `D01_requeima`, `D02_septoriose`, `D03_pinta_preta`,
> `D03b_mancha_alvo`, `D05_mofo_foliar`, `D06_vira_cabeca`, `D06b_mosaico`,
> `D07_acaro_bronzeamento`, `D09_mancha_bacteriana`, `saudavel`.

---

### 3.4 Histórico de eventos — `GET /api/diagnostico/historico/`

Lista paginada de eventos (diagnósticos do app + leituras IoT do ESP32).
Se autenticado, retorna os diagnósticos do próprio usuário + eventos IoT.
Se anônimo, retorna apenas os eventos IoT.

**Query params:** `?page=2` · `?page_size=20` (máx. 20; padrão 10).

**Response 200:**
```json
{
  "count": 128,
  "next": "https://ceres.up.railway.app/api/diagnostico/historico/?page=2",
  "previous": null,
  "results": [
    {
      "id": 127,
      "device_id": "app_flutter",
      "classe_detectada": "D06_vira_cabeca",
      "confianca": 0.8564,
      "temperatura": null,
      "umidade_ar": null,
      "umidade_solo": null,
      "latitude": -15.6014,
      "longitude": -56.0979,
      "timestamp": "2026-07-04T14:22:31Z",
      "usuario_email": "test@test.com",
      "diagnostico": null,
      "criado_em": "2026-07-04T14:22:31Z"
    }
  ]
}
```

---

### 3.5 Última leitura de sensor — `GET /api/diagnostico/sensor/`

Retorna a leitura de sensor mais recente do ESP32 (card "Status do Sensor" na tela IoT).

**Response 200 (com dados):**
```json
{
  "status": "ok",
  "sensor": {
    "id": 340, "device_id": "ceres-esp32-01",
    "temperatura": 32.7, "umidade_ar": 41.8, "umidade_solo": 34.0,
    "timestamp": "2026-07-04T14:20:00Z", "criado_em": "2026-07-04T14:20:01Z"
  }
}
```

**Response 200 (sem dados):**
```json
{ "status": "aguardando", "mensagem": "Nenhuma leitura de sensor disponível." }
```

---

## 4. Modelo de dados — `DiagnosticoEvento`

Entidade central que registra tanto diagnósticos do app quanto leituras IoT.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | bigint (PK) | Identificador |
| `device_id` | varchar(50) | `app_flutter`, `app_<user>` ou `ceres-esp32-01` |
| `classe_detectada` | varchar | Classe da doença (nullable para leitura pura de sensor) |
| `confianca` | float | Probabilidade 0.0–1.0 |
| `temperatura` | float | °C (DHT22) — null se não houver sensor |
| `umidade_ar` | float | % (DHT22) |
| `umidade_solo` | float | % (sensor capacitivo) |
| `latitude` / `longitude` | float | GPS do celular no diagnóstico |
| `timestamp` | datetime | Momento da captura |
| `usuario` | FK → CustomUser | Autor (null para evento MQTT do ESP32) |
| `diagnostico` | FK → Diagnostico | Diagnóstico associado (opcional) |
| `criado_em` | datetime | Recebido em (servidor) |

---

## 5. Códigos de status HTTP

| Código | Significado no Ceres |
|---|---|
| `200 OK` | Sucesso |
| `201 Created` | Usuário criado (`/register/`) |
| `400 Bad Request` | Parâmetro ausente/inválido |
| `401 Unauthorized` | JWT ausente ou inválido |
| `404 Not Found` | Recurso inexistente (opção, e-mail, árvore vazia) |
| `500 Internal Server Error` | Falha na inferência |
| `503 Service Unavailable` | Modelo TFLite indisponível |
| `504 Gateway Timeout` | Inferência excedeu 30s |

---

## 6. Exemplos com `curl`

```bash
# Login
curl -X POST https://ceres.up.railway.app/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test@test.com","password":"test123"}'

# Iniciar triagem por sintomas
curl https://ceres.up.railway.app/api/diagnostico/iniciar/

# Inferência por imagem (com GPS)
curl -X POST https://ceres.up.railway.app/api/diagnostico/inferir/ \
  -F "imagem=@folha.jpg" -F "latitude=-15.60" -F "longitude=-56.09"

# Histórico (autenticado)
curl https://ceres.up.railway.app/api/diagnostico/historico/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 7. Comunicação IoT (fora do REST)

O ESP32-S3 **não** usa a API REST — publica via **MQTT** no broker HiveMQ Cloud,
e o `mqtt_listener` (comando de gerenciamento Django) consome e persiste no banco.

| Item | Valor |
|---|---|
| Broker | HiveMQ Cloud (TLS 8883 / WebSocket 8884) |
| Tópico | `ceres/sensor/#` |
| Payload | `{"device_id":"ceres-esp32-01","temperatura":32.7,"umidade_ar":41.8,"umidade_solo":0}` |

Fluxo completo: **ESP32 → HiveMQ → mqtt_listener → PostgreSQL → GET /historico/ → App**.
