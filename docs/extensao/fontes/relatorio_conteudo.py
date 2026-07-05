# -*- coding: utf-8 -*-
"""Conteudo estruturado do Relatorio Final de Extensao II (fonte unica).
Consumido por gen_relatorio_pdf.py e gen_relatorio_docx.py.
Toda a documentacao tecnica (diagramas, API, manuais, backlog) esta EMBUTIDA aqui —
o relatorio e autocontido, nao aponta para arquivos externos.

Blocos:
  ('h1'|'h2'|'h3', txt)      cabecalhos
  ('p', txt)                 paragrafo (marcacao **negrito**)
  ('bul', [itens])           lista com marcadores
  ('tab', [headers], [rows]) tabela
  ('code', txt)              bloco de codigo/JSON monoespacado
  ('fig', path, caption)     figura unica
  ('figrow', cols, [(path,cap)])  grade de figuras (cols por linha)
"""

BASE = "C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/extensao"
DIAG = BASE + "/anexos/diagramas"
SHOT = BASE + "/assets/screenshots"
HW   = BASE + "/assets/fotos_hardware"

TITULO = "Relatório Final — Atividade de Extensão II"
SUBTITULO = ("Ceres Diagnóstico — Sistema embarcado de detecção precoce de doenças no tomateiro  ·  "
             "IFMT Cuiabá  ·  Namem Rachid Jaudy Neto")

# ── Backlog por sprint (usado na Secao 6 — todas as tarefas) ──
SPRINT1 = [
    ("Épico A — Motor de Diagnóstico e API", [
        ("Mapeamento das 10 doenças do tomateiro (Embrapa)", "Backend", "Crítica"),
        ("Models Pergunta/Opcao/Diagnostico + migrations", "Backend", "Crítica"),
        ("Endpoints /iniciar/ e /responder/", "Backend", "Alta"),
        ("Autenticação JWT (SimpleJWT)", "Backend", "Alta"),
        ("Multi-tenant (Tenant + CustomUser)", "Backend", "Média"),
        ("PostgreSQL 18 (porta 5433)", "Infra", "Alta"),
        ("5 testes automatizados passando", "QA", "Alta"),
    ]),
    ("Épico B — Dataset, Modelo de IA e MQTT", [
        ("PlantVillage (18.160 imgs) + augmentation → 88.949", "IA", "Crítica"),
        ("Exp A — Edge Impulse (FP32 92,5% / INT8 62%)", "IA", "Média"),
        ("Exp B — TF local (float 98,13% / INT8 95,76%, 639 KB)", "IA", "Crítica"),
        ("Exp C — Background augmentation sintética (20,24% campo)", "IA", "Baixa"),
        ("Exp D — Fine-tuning PlantDoc real (30,43% campo)", "IA", "Média"),
        ("Exp E — Focal Loss + aug agressiva (final, 638 KB)", "IA", "Crítica"),
        ("export_tflite.py — INT8 calibrado", "IA", "Alta"),
        ("Validação PlantDoc — gap lab-campo documentado", "IA", "Alta"),
        ("Backend MQTT (DiagnosticoEvento + mqtt_listener + /historico/)", "Backend", "Alta"),
        ("Mosquitto 2.1 instalado e testado", "Infra", "Média"),
        ("Matriz de confusão + acurácia por classe", "QA", "Média"),
    ]),
]
SPRINT2 = [
    ("Épico A — Nó de sensores MQTT", [
        ("Projeto PlatformIO esp32_mqtt_sensor", "Firmware", "Alta"),
        ("WiFi + MQTT + reconexão automática", "Firmware", "Alta"),
        ("Publicação de JSON em ceres/sensor/", "Firmware", "Alta"),
        ("Pilha ESP32 → Mosquitto → Django → PostgreSQL", "Integração", "Alta"),
    ]),
    ("Épico B — TFLite Micro no ESP32-S3", [
        ("esp32s3_ceres — TFLite Micro (arena PSRAM 200 KB)", "Firmware", "Crítica"),
        ("gerar_arrays_c.py — modelo + 10 imgs como arrays C", "IA", "Alta"),
        ("Benchmark embarcado — 692 ms, 10/10 correto", "Firmware", "Crítica"),
        ("benchmark_esp32s3.md documentado", "QA", "Média"),
    ]),
]
SPRINT3 = [
    ("Épico A — App base + inferência", [
        ("App Flutter (Diagnóstico + Histórico)", "App", "Crítica"),
        ("api_service — multipart POST + GET paginado", "App", "Alta"),
        ("View /inferir/ via subprocess TFLite", "Backend", "Crítica"),
        ("Validação end-to-end (galeria → resultado)", "QA", "Alta"),
        ("Experimento Edge vs Cloud", "IA", "Média"),
        ("Drift (SQLite) — persistência local", "App", "Alta"),
    ]),
    ("Épico B — Design System e UI", [
        ("CeresTheme (paleta cerrado, Material 3)", "App", "Alta"),
        ("6 telas redesenhadas (Splash/Login/Diagnóstico/IoT/Salvos/Enciclopédia)", "App", "Alta"),
        ("doencas_data.dart — 10 doenças centralizadas", "App", "Média"),
        ("flutter_svg + ícones thin-stroke", "App", "Baixa"),
        ("Tab bar + appbar fiéis ao mockup", "App", "Baixa"),
    ]),
    ("Épico C — Deploy, nuvem e novas telas", [
        ("12 telas migradas + 4 novas (Alertas/Parceiro/Cadastro/Agrônomos)", "App", "Alta"),
        ("Registro de usuário /register/", "Backend", "Alta"),
        ("Deploy Railway — ceres.up.railway.app", "Infra", "Crítica"),
        ("TFLite on-device Android (~60 ms)", "App", "Crítica"),
        ("MQTT Cloud HiveMQ (TLS 8883 / WS 8884)", "IoT", "Alta"),
    ]),
    ("Épico D — UX: navegação, mapa e perfil", [
        ("Back button no CeresAppBar", "App", "Baixa"),
        ("Persistência de sessão + auto-refresh JWT", "App", "Média"),
        ("Banner offline (connectivity_plus)", "App", "Média"),
        ("latitude/longitude em DiagnosticoEvento", "Backend", "Média"),
        ("MapaScreen (flutter_map + OSM, marcadores)", "App", "Alta"),
        ("Captura de GPS no diagnóstico", "App", "Média"),
        ("GET /api/auth/me/ (estatísticas do usuário)", "Backend", "Média"),
        ("PerfilScreen (stats, exportar CSV, logout)", "App", "Média"),
    ]),
    ("Épico E — Robustez e sincronização offline", [
        ("Railway PostgreSQL persistente entre deploys", "Infra", "Crítica"),
        ("Per-user diagnostics (FK usuario)", "Backend", "Alta"),
        ("Temperature scaling INT8 (T=0.25)", "Backend/App", "Alta"),
        ("Fila de sincronização offline → online (SyncService)", "App", "Alta"),
        ("Matriz de confusão INT8 (95,76%, 2.734 imgs)", "QA", "Média"),
    ]),
]


def sprint_tables(epicos):
    blk = []
    for nome, tarefas in epicos:
        blk.append(("h3", nome))
        rows = [[t, c, p, "Concluído"] for (t, c, p) in tarefas]
        blk.append(("tab", ["Tarefa", "Camada", "Prioridade", "Status"], rows))
    return blk


BLOCKS = [
    # ───────────────────────── 1. IDENTIFICAÇÃO ─────────────────────────
    ("h1", "1. Identificação do Projeto"),
    ("h2", "1.1 Título"),
    ("p", "**Ceres Diagnóstico** — Sistema embarcado de detecção precoce de doenças no tomateiro, "
          "integrando visão computacional (TinyML) no ESP32-S3, backend em nuvem e aplicativo móvel."),
    ("h2", "1.2 Curso / Disciplina / Professor"),
    ("bul", ["**Curso:** Engenharia da Computação — IFMT Cuiabá (Campus Cel. Octayde Jorge da Silva)",
             "**Disciplina:** Extensão II — 2026/1",
             "**Professor:** Tiago Lacerda"]),
    ("h2", "1.3 Integrantes"),
    ("p", "Projeto desenvolvido individualmente:"),
    ("tab", ["Nome", "Funções desempenhadas"],
     [["Namem Rachid Jaudy Neto",
       "Product Owner, Scrum Master, Desenvolvedor Back-end (Django/API), Desenvolvedor "
       "Front-end/Mobile (Flutter), Engenheiro de IA (treino/quantização), Desenvolvedor de "
       "Firmware (ESP32-S3), Banco de Dados, UX/UI e QA"]]),
    ("h2", "1.4 Local e Ano"),
    ("p", "Cuiabá — MT, IFMT, 2026."),

    # ───────────────────────── 2. RESUMO EXECUTIVO ─────────────────────────
    ("h1", "2. Resumo Executivo"),
    ("p", "**Problema.** Pequenos produtores de tomate têm dificuldade de acesso a diagnóstico "
          "agronômico rápido. Doenças como a requeima podem destruir uma lavoura inteira antes de o "
          "produtor identificar o problema, e a conectividade no campo é limitada."),
    ("p", "**Público-alvo.** Pequenos horticultores de Sorriso-MT e região, produtores de tomate que "
          "trabalham diretamente no campo."),
    ("p", "**Produto.** Um sistema em três camadas: (1) aplicativo móvel que diagnostica doenças da "
          "folha por foto, com IA rodando no próprio celular (offline) ou na nuvem; (2) nó IoT "
          "ESP32-S3 que monitora temperatura e umidade e roda o modelo embarcado; (3) backend em "
          "nuvem (Django REST no Railway) com histórico, mapa de ocorrências e enciclopédia."),
    ("p", "**Tecnologias.** Django REST Framework, PostgreSQL, Flutter/Dart, TensorFlow/TFLite "
          "(MobileNetV2 INT8), ESP32-S3 (PlatformIO/Arduino), MQTT (Mosquitto/HiveMQ), Railway, GitHub."),
    ("p", "**Principais resultados.** Modelo de **638 KB** classificando **10 categorias** (9 doenças + "
          "saudável); acurácia de **95,76%** (INT8, laboratório); latência de **692 ms** no ESP32-S3 e "
          "**~60 ms** on-device no celular; aplicativo completo com 5 telas publicado e API em produção. "
          "O projeto documentou honestamente o gap laboratório-campo (queda para 20–30% em imagens de "
          "campo real), fenômeno reconhecido na literatura."),

    # ───────────────────────── 3. VISÃO DO PROJETO ─────────────────────────
    ("h1", "3. Visão do Projeto"),
    ("p", "**Problema identificado.** Um tomateiro doente não “grita”: murcha em silêncio enquanto a "
          "doença avança. O diagnóstico depende de um agrônomo, inacessível ao pequeno produtor, e "
          "existem cerca de 10 doenças difíceis de distinguir a olho nu. A internet que permitiria o "
          "diagnóstico digital muitas vezes não chega à lavoura."),
    ("p", "**Público-alvo e comunidade beneficiada.** Pequenos horticultores de Sorriso-MT e região — "
          "produtores que trabalham diretamente no campo, com pouco tempo ou dificuldade para digitar "
          "textos técnicos no celular."),
    ("p", "**Justificativa.** Diferente de grupos de WhatsApp, buscas no Google ou chatbots agrícolas "
          "genéricos, o Ceres transforma recomendações de manejo (base Embrapa) em diagnósticos rápidos "
          "e acessíveis diretamente na lavoura, ajudando o produtor a reduzir perdas."),
    ("p", "**Objetivos.**"),
    ("bul", ["Treinar um modelo de IA leve o suficiente para rodar em microcontrolador e celular;",
             "Disponibilizar diagnóstico por foto funcionando offline;",
             "Monitorar variáveis ambientais da lavoura via sensores IoT;",
             "Entregar um aplicativo completo, publicado e utilizável em condições reais."]),
    ("p", "**Benefícios esperados.** Triagem agronômica imediata e de baixo custo (~R$80 por nó de "
          "hardware), redução de perdas por diagnóstico tardio e democratização do acesso à informação "
          "técnica no campo."),

    # ───────────────────────── 4. ROADMAP ─────────────────────────
    ("h1", "4. Roadmap do Produto"),
    ("p", "O desenvolvimento foi organizado em **3 sprints de ~1 mês (4 semanas)**, além de uma fase "
          "futura registrada. A metodologia foi **Scrum adaptado** ao contexto individual, com "
          "revisão ao final de cada sprint e priorização por criticidade (Crítica → Baixa)."),
    ("fig", f"{DIAG}/roadmap.png", "Figura 1 — Linha do tempo do produto (roadmap das 3 sprints)."),
    ("tab", ["Sprint", "Tema", "Duração", "Tarefas", "Status"],
     [["1", "Núcleo Inteligente (Backend + IA)", "≈ 1 mês", "18", "Concluída"],
      ["2", "Borda Embarcada (Firmware + IoT)", "≈ 1 mês", "8", "Concluída"],
      ["3", "Aplicativo e Integração (App + UX + Deploy)", "≈ 1 mês", "29", "Concluída"],
      ["—", "Fase Futura (câmera OV5640, RPi3B+)", "—", "—", "Registrada"]]),
    ("p", "**Alterações de escopo (repriorizações justificadas):** a câmera OV5640 foi mantida como "
          "prova de conceito (custo/prazo), com o app móvel assumindo o papel de produto principal; "
          "entre os experimentos de IA, a augmentation sintética (Exp C) foi descartada por piorar o "
          "resultado, adotando-se fine-tuning com dados reais (Exp D) e Focal Loss (Exp E, modelo final)."),

    # ───────────────────────── 5. GESTÃO E TECNOLOGIAS ─────────────────────────
    ("h1", "5. Gestão e Tecnologias"),
    ("h2", "5.1 Gestão do Projeto"),
    ("bul", ["**Metodologia:** Scrum adaptado — sprints de ~1 mês com revisão e ajuste de backlog ao "
             "final de cada ciclo;",
             "**Sprints realizadas:** 3 (+ fase futura registrada);",
             "**Ferramenta de gestão e versionamento:** GitHub (github.com/Namem/extensao2) — histórico "
             "de commits (Conventional Commits) e backlog em Markdown/Excel;",
             "**Organização das tarefas:** backlog priorizado por criticidade, agrupado por épico e "
             "camada (Backend, IA, Firmware, App, Infra, QA);",
             "**Adaptação:** por ser projeto individual, os papéis de PO, Scrum Master e time foram "
             "acumulados pelo autor; a comunicação se deu via documentação viva no repositório."]),
    ("h2", "5.2 Tecnologias Utilizadas"),
    ("tab", ["Tecnologia", "Finalidade"],
     [["Django REST Framework", "Backend / API REST"],
      ["PostgreSQL", "Banco de dados (produção)"],
      ["SimpleJWT", "Autenticação por token JWT"],
      ["Flutter / Dart", "Aplicativo móvel e desktop"],
      ["Drift (SQLite)", "Persistência offline no app"],
      ["flutter_map + OpenStreetMap", "Mapa de ocorrências"],
      ["geolocator", "Captura de GPS"],
      ["TensorFlow / Keras", "Treinamento do modelo de IA"],
      ["TensorFlow Lite / tflite_flutter", "Inferência embarcada (celular e ESP32)"],
      ["MobileNetV2 (INT8)", "Arquitetura do classificador"],
      ["rembg (U2-Net) / Pillow", "Pré-processamento de imagens no treino"],
      ["ESP32-S3 (PlatformIO / Arduino)", "Firmware do nó IoT"],
      ["DHT22 + sensor capacitivo", "Sensores de temperatura, umidade do ar e do solo"],
      ["MQTT (Mosquitto / HiveMQ Cloud)", "Comunicação IoT (TLS / WebSocket)"],
      ["Railway", "Hospedagem do backend e do PostgreSQL"],
      ["GitHub", "Versionamento e gestão do backlog"]]),
    ("fig", f"{DIAG}/arquitetura.png", "Figura 2 — Arquitetura do sistema em três camadas."),

    # ───────────────────────── 6. DESENVOLVIMENTO (todas as tarefas) ─────────────────────────
    ("h1", "6. Descrição do Desenvolvimento"),
    ("p", "Esta seção detalha cada sprint com **todas as suas tarefas**, além de objetivo, "
          "dificuldades, decisões e entregas."),

    ("h2", "Sprint 1 — Núcleo Inteligente (Backend + IA) · ≈ 1 mês · 18 tarefas"),
    ("p", "**Objetivo:** construir a API Django, o motor de diagnóstico e o modelo de IA treinado e "
          "validado."),
] + sprint_tables(SPRINT1) + [
    ("p", "**Dificuldades:** TensorFlow sem suporte a Python 3.13 (uso de WSL2 + Python 3.12); "
          "detecção da GPU no WSL2; bug de pré-processamento INT8 na validação."),
    ("p", "**Decisões:** treinar localmente (Exp B) para quantização INT8 calibrada; descartar a "
          "augmentation sintética (Exp C). **Entrega:** API funcional (5/5 testes) + modelo TFLite validado."),

    ("h2", "Sprint 2 — Borda Embarcada (Firmware + IoT) · ≈ 1 mês · 8 tarefas"),
    ("p", "**Objetivo:** rodar a IA e os sensores no hardware real ESP32-S3."),
] + sprint_tables(SPRINT2) + [
    ("p", "**Dificuldades:** bibliotecas TFLite para ESP32 descontinuadas (solução: "
          "Chirale_TensorFLowLite); boot loop por flags de PSRAM; broker só escutando em localhost."),
    ("p", "**Decisões:** remover a câmera OV5640 do escopo e usar imagens embutidas para validar a "
          "inferência. **Entrega:** modelo rodando em hardware real com latência medida (692 ms)."),

    ("h2", "Sprint 3 — Aplicativo e Integração (App + UX + Deploy) · ≈ 1 mês · 29 tarefas"),
    ("p", "**Objetivo:** entregar o aplicativo Flutter completo, publicado e resiliente."),
] + sprint_tables(SPRINT3) + [
    ("p", "**Dificuldades:** confiança achatada do INT8 (temperature scaling T=0.25); race condition "
          "no GPS; Railway bloqueando portas MQTT (WebSocket + renome de env vars); SQLite efêmero "
          "(migração para PostgreSQL persistente)."),
    ("p", "**Decisões:** app como produto principal; design fiel a um mockup de referência. "
          "**Entrega:** aplicativo publicado + API em produção (ceres.up.railway.app)."),

    # ───────────────────────── 7. RESULTADOS ─────────────────────────
    ("h1", "7. Resultados Obtidos"),
    ("h3", "Produto final e funcionalidades"),
    ("bul", ["Diagnóstico de 10 categorias (9 doenças + saudável) por foto, cloud ou offline;",
             "Histórico de diagnósticos e leituras IoT em tempo real (temperatura, umidade do ar/solo);",
             "Mapa georreferenciado de ocorrências; enciclopédia das doenças; perfil com exportação CSV;",
             "Sincronização automática dos diagnósticos feitos offline ao voltar a conexão."]),
    ("fig", f"{DIAG}/casos_de_uso.png", "Figura 3 — Diagrama de casos de uso do sistema."),
    ("h3", "Principais telas do sistema"),
    ("p", "Capturas das telas do aplicativo (renderizadas a partir do protótipo de alta fidelidade):"),
    ("figrow", 3, [
        (f"{SHOT}/01_splash.png", "Abertura"),
        (f"{SHOT}/02_login.png", "Login"),
        (f"{SHOT}/04_diagnostico.png", "Diagnóstico (foto)"),
        (f"{SHOT}/05_historico_iot.png", "Histórico IoT"),
        (f"{SHOT}/09_mapa_da_lavoura.png", "Mapa da lavoura"),
        (f"{SHOT}/11_enciclopedia.png", "Enciclopédia"),
    ]),
    ("h3", "Métricas"),
    ("tab", ["Métrica", "Valor"],
     [["Acurácia (float, laboratório)", "98,13%"],
      ["Acurácia (INT8 embarcado, laboratório)", "95,76%"],
      ["Acurácia em campo real (documentada)", "20–30%"],
      ["Tamanho do modelo (INT8)", "638 KB"],
      ["Latência — ESP32-S3", "692 ms"],
      ["Latência — on-device (celular)", "~60 ms"],
      ["Latência — nuvem", "~280–330 ms"],
      ["Custo do nó de hardware", "~R$80"]]),
    ("h3", "Testes e validações"),
    ("bul", ["5/5 testes automatizados no backend (motor de diagnóstico, MQTT, histórico);",
             "Validação end-to-end (galeria → inferência → resultado) no app;",
             "Matriz de confusão INT8 em 2.734 imagens (95,76%);",
             "Benchmark do ESP32-S3 (10/10 corretos) e experimento Edge vs Cloud."]),
    ("h3", "Benefícios proporcionados"),
    ("p", "Triagem agronômica imediata, de baixo custo e funcionando sem internet — colocando na mão do "
          "pequeno produtor uma ferramenta de apoio à decisão que antes dependia de especialista."),
    ("h3", "Limitações identificadas"),
    ("bul", ["**Gap laboratório-campo:** o modelo, treinado com imagens de fundo controlado "
             "(PlantVillage), cai para 20–30% em fotos de campo real — fenômeno documentado na "
             "literatura (Mohanty 2016; Singh 2020). É a principal limitação e o foco dos próximos passos.",
             "**Câmera embarcada (OV5640):** não integrada ao ESP32-S3 na entrega (prova de conceito).",
             "**Validação com usuários reais:** ainda não realizada com produtores em campo — planejada "
             "como etapa futura."]),
    ("h3", "Reflexão"),
    ("bul", ["**Aprendizados:** transfer learning e quantização INT8 calibrada; comunicação IoT segura "
             "(MQTT/TLS); arquitetura offline-first; deploy em nuvem; a importância de documentar "
             "resultados negativos (o gap de campo não é fracasso — é achado).",
             "**Dificuldades enfrentadas:** compatibilidade de ambientes (GPU/WSL2), bibliotecas de "
             "TinyML descontinuadas, restrições de rede em PaaS.",
             "**Melhorias futuras:** dataset brasileiro de tomateiro, retreino com dados locais, câmera "
             "embarcada e validação com produtores.",
             "**Continuidade:** o projeto tem sequência natural como TinyML agrícola — “o gargalo é o "
             "dado, não o hardware”."]),

    # ───────────────────────── 8. ANEXOS ─────────────────────────
    ("h1", "8. Anexos"),
    ("h2", "8.1 Repositório GitHub"),
    ("p", "https://github.com/Namem/extensao2 — código-fonte (backend, app, firmware), histórico de "
          "commits e README com instruções."),
    ("h2", "8.2 Slides das Sprint Reviews"),
    ("p", "Apresentação Sprint MVP e roteiro de apresentação (pasta slides/ do repositório)."),

    ("h2", "8.3 Prints e fotos do projeto"),
    ("h3", "Hardware — nó IoT ESP32-S3 e testes"),
    ("figrow", 2, [
        (f"{HW}/setup_completo_v1.jpg", "Nó completo: ESP32-S3 + DHT22 + sensor de solo no vaso"),
        (f"{HW}/sensor_solo_terra.jpg", "Sensor capacitivo de umidade do solo instalado"),
        (f"{HW}/esp32_closeup.jpg", "ESP32-S3 e ligações na protoboard"),
        (f"{HW}/serial_monitor.png", "Monitor serial — leituras publicadas via MQTT"),
    ]),
    ("h3", "Aplicativo — demais telas"),
    ("figrow", 3, [
        (f"{SHOT}/03_cadastro.png", "Cadastro"),
        (f"{SHOT}/06_salvos_offline.png", "Salvos offline"),
        (f"{SHOT}/10_central_de_alertas.png", "Central de alertas"),
        (f"{SHOT}/07_agronomos_parceiros.png", "Agrônomos parceiros"),
        (f"{SHOT}/08_seja_parceiro.png", "Seja parceiro"),
        (f"{SHOT}/12_configuracoes.png", "Configurações / Perfil"),
    ]),

    ("h2", "8.4 Documentação Técnica"),
    ("p", "A documentação técnica completa está reproduzida a seguir (diagramas, modelo de dados, "
          "documentação da API e manuais de instalação e do usuário)."),

    ("h3", "8.4.1 Diagrama de Classes"),
    ("fig", f"{DIAG}/diagrama_classes.png", "Figura 4 — Diagrama de classes (models do backend)."),
    ("h3", "8.4.2 Modelo Entidade-Relacionamento (MER)"),
    ("fig", f"{DIAG}/mer.png", "Figura 5 — Modelo Entidade-Relacionamento (esquema do banco)."),

    # ── 8.4.3 API ──
    ("h3", "8.4.3 Documentação da API REST"),
    ("p", "API construída em Django REST Framework. Base de produção "
          "**https://ceres.up.railway.app/api/** · base local **http://localhost:8080/api/**. Formato "
          "JSON (exceto /inferir/, multipart/form-data). Autenticação JWT (Bearer). A maioria dos "
          "endpoints é pública (o produtor usa o diagnóstico sem login); os dependentes do usuário "
          "exigem o header Authorization: Bearer <access_token>."),
    ("tab", ["Método", "Rota", "Auth", "Descrição"],
     [["POST", "/api/auth/token/", "—", "Login: retorna access + refresh (JWT)"],
      ["POST", "/api/auth/token/refresh/", "—", "Renova o access token"],
      ["POST", "/api/auth/register/", "—", "Cadastro de produtor/agrônomo"],
      ["POST", "/api/auth/reset-password/", "—", "Redefine senha (sem e-mail)"],
      ["GET", "/api/auth/me/", "JWT", "Perfil + estatísticas do usuário"],
      ["GET", "/api/diagnostico/iniciar/", "—", "Pergunta raiz da árvore de sintomas"],
      ["POST", "/api/diagnostico/responder/", "—", "Avança na árvore (próxima ou diagnóstico)"],
      ["POST", "/api/diagnostico/inferir/", "—", "Classifica a foto da folha (TFLite)"],
      ["GET", "/api/diagnostico/historico/", "opcional", "Histórico paginado (diagnósticos + IoT)"],
      ["GET", "/api/diagnostico/sensor/", "—", "Última leitura de sensor do ESP32"]]),
    ("p", "**POST /api/diagnostico/inferir/** — recebe a imagem (campo imagem, multipart) e, "
          "opcionalmente, latitude/longitude; persiste o resultado como DiagnosticoEvento. Resposta 200:"),
    ("code", '{\n'
             '  "classe": "D01_requeima",\n'
             '  "class_index": 0,\n'
             '  "confianca": 0.857,\n'
             '  "latencia_ms": 279,\n'
             '  "scores": { "D01_requeima": 0.857, "D09_mancha_bacteriana": 0.081, "...": ... }\n'
             '}'),
    ("p", "Erros: 400 imagem ausente · 503 modelo indisponível · 504 timeout (>30s) · 500 falha. "
          "As 10 classes: D01_requeima, D02_septoriose, D03_pinta_preta, D03b_mancha_alvo, "
          "D05_mofo_foliar, D06_vira_cabeca, D06b_mosaico, D07_acaro_bronzeamento, "
          "D09_mancha_bacteriana, saudavel."),
    ("p", "**GET /iniciar/** e **POST /responder/** implementam o motor por árvore de sintomas. "
          "Resposta final de exemplo:"),
    ("code", '{ "tipo": "diagnostico",\n'
             '  "dados": { "id": 3, "nome": "Requeima",\n'
             '             "descricao": "...", "recomendacao_manejo": "..." } }'),
    ("p", "**GET /historico/** — lista paginada (page_size 10, máx. 20). Autenticado: diagnósticos do "
          "próprio usuário + eventos IoT; anônimo: apenas eventos IoT. Cada item segue o modelo "
          "DiagnosticoEvento:"),
    ("tab", ["Campo", "Tipo", "Descrição"],
     [["id", "bigint (PK)", "Identificador"],
      ["device_id", "varchar(50)", "app_flutter, app_<user> ou ceres-esp32-01"],
      ["classe_detectada", "varchar", "Classe da doença (nulo p/ leitura de sensor)"],
      ["confianca", "float", "Probabilidade 0.0–1.0"],
      ["temperatura / umidade_ar / umidade_solo", "float", "DHT22 e sensor capacitivo"],
      ["latitude / longitude", "float", "GPS do celular no diagnóstico"],
      ["timestamp / criado_em", "datetime", "Captura / recebimento no servidor"],
      ["usuario", "FK → CustomUser", "Autor (nulo para evento MQTT do ESP32)"],
      ["diagnostico", "FK → Diagnostico", "Diagnóstico associado (opcional)"]]),
    ("p", "**Comunicação IoT (fora do REST):** o ESP32-S3 publica via MQTT no broker HiveMQ Cloud "
          "(TLS 8883 / WebSocket 8884, tópico ceres/sensor/#); o comando Django mqtt_listener consome "
          "e persiste no PostgreSQL. Payload:"),
    ("code", '{"device_id":"ceres-esp32-01","temperatura":32.7,\n'
             ' "umidade_ar":41.8,"umidade_solo":34}'),

    # ── 8.4.4 Manual de Instalação ──
    ("h3", "8.4.4 Manual de Instalação"),
    ("p", "Guia para instalar e executar o sistema completo (Backend Django, App Flutter e Firmware "
          "ESP32-S3). Testado em Windows 11. Pré-requisitos: Git; Python 3.13 (Windows) / 3.12 (WSL2); "
          "PostgreSQL 18 porta 5433 (opcional — ou SQLite); Flutter SDK 3.44+; Visual Studio Build "
          "Tools (Desktop C++); PlatformIO 6.1+; Mosquitto 2.1+ (opcional)."),
    ("p", "**1) Clonar:**"),
    ("code", "git clone https://github.com/Namem/extensao2 ceres-diagnostico\ncd ceres-diagnostico"),
    ("p", "**2) Backend — Django REST API:**"),
    ("code", "cd backend\n"
             "python -m venv venv\n"
             ".\\venv\\Scripts\\activate\n"
             "pip install -r requirements.txt\n"
             "python manage.py migrate --settings=ceres_core.settings_notebook\n"
             "python manage.py test diagnostico\n"
             "python manage.py runserver 0.0.0.0:8080 --settings=ceres_core.settings_notebook"),
    ("p", "A API sobe em http://localhost:8080/api/. Banco: SQLite (settings_notebook) ou PostgreSQL 18 "
          "(porta 5433). Copie backend/.env.example → backend/.env e ajuste (SECRET_KEY, banco, MQTT, "
          "ALLOWED_HOSTS) — nunca commitar o .env. Listener IoT: python manage.py mqtt_listener "
          "--settings=ceres_core.settings_notebook."),
    ("p", "**3) App — Flutter:**"),
    ("code", "cd ..\\app_ceres\n"
             "flutter pub get\n"
             "flutter run -d windows          # desktop\n"
             "flutter build apk --release     # APK para celular"),
    ("p", "Ajuste o servidor em lib/config.dart (baseUrl): produção https://ceres.up.railway.app · "
          "local http://localhost:8080 · emulador http://10.0.2.2:8080 · celular na mesma WiFi "
          "http://192.168.X.X:8080. O APK sai em build/app/outputs/flutter-apk/app-release.apk."),
    ("p", "**4) Firmware — ESP32-S3:** dois projetos em firmware/: esp32_mqtt_sensor/ (sensores DHT22 + "
          "solo via MQTT) e esp32s3_ceres/ (benchmark TFLite Micro). Copie include/config.h.example → "
          "include/config.h e ajuste WiFi/broker (config.h é ignorado pelo Git). Gravar:"),
    ("code", "cd firmware/esp32_mqtt_sensor\n"
             "pio run --target upload --upload-port COM5\n"
             "pio device monitor"),
    ("p", "Placa esp32-s3-devkitc-1, Flash 16MB, framework Arduino. Fazer no notebook (mesma rede WiFi "
          "do ESP32). **Deploy (Railway):** automático via git push na main; "
          "DJANGO_SETTINGS_MODULE=ceres_core.settings_railway (PostgreSQL via DATABASE_URL); URL "
          "https://ceres.up.railway.app · conta de teste test@test.com / test123. **Modelos TFLite:** "
          "ceres_expe_int8.tflite (Exp E, 638 KB — backend + app) e ceres_mobilenetv2_int8.tflite "
          "(Exp B, 639 KB — ESP32-S3)."),

    # ── 8.4.5 Manual do Usuário ──
    ("h3", "8.4.5 Manual do Usuário"),
    ("p", "Guia de uso do aplicativo Ceres Diagnóstico — diagnóstico de doenças do tomateiro por foto, "
          "com IA embarcada no celular e monitoramento de sensores IoT. **Instalação:** copie o "
          "ceres_diagnostico.apk para o celular Android, permita “instalar de fonte desconhecida” e abra "
          "o app (há também versão web/desktop conectada à API em produção)."),
    ("p", "**Primeiro acesso:** o app abre no splash e vai ao Login. Opções: Entrar (e-mail + senha); "
          "Criar conta (Produtor ou Agrônomo — o agrônomo informa o CREA); Esqueci a senha (redefine "
          "pelo e-mail); Continuar sem conta (diagnóstico funciona; histórico na nuvem indisponível)."),
    ("p", "**Telas principais — 5 abas:**"),
    ("bul", ["**Diagnóstico:** tire a foto (câmera ou galeria); o app mostra a doença (ou Saudável), a "
             "confiança (%), os scores e a recomendação de manejo (Embrapa); o resultado é salvo "
             "automaticamente. Modo Cloud (envia ao servidor, entra no mapa) ou Offline (IA no celular, "
             "~60 ms, sem internet — nenhuma imagem sai do aparelho).",
             "**Mapa:** ocorrências georreferenciadas (OpenStreetMap), marcador por urgência; toque para "
             "ver doença, data, confiança e coordenadas.",
             "**IoT:** leituras do ESP32-S3 em tempo real — temperatura e umidade do ar (DHT22), umidade "
             "do solo (capacitivo), histórico e status MQTT.",
             "**Enciclopédia:** fichas das 10 categorias (sintomas, agente, ação) com busca.",
             "**Perfil:** nome, e-mail, estatísticas, modo de inferência, exportar CSV e sair."]),
    ("p", "**As 10 categorias:** D01 Requeima, D02 Septoriose, D03 Pinta-preta, D03b Mancha-alvo, "
          "D05 Mofo-foliar, D06 Vira-cabeça (TYLCV), D06b Mosaico, D07 Ácaro-do-bronzeamento, "
          "D09 Mancha-bacteriana e Saudável."),
    ("p", "**Uso offline e sincronização:** sem internet, use o modo Offline; os diagnósticos ficam "
          "marcados como “não sincronizado” e, ao voltar a conexão, são enviados automaticamente para a "
          "nuvem. **Dicas:** fotografe a folha bem iluminada, preenchendo o quadro (fotos de campo com "
          "fundo natural reduzem a confiança — limitação conhecida). A confiança é uma estimativa: em "
          "caso de dúvida, consulte um agrônomo — o app é uma ferramenta de triagem."),
]
