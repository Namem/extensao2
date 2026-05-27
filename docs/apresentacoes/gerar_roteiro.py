"""
Gera o roteiro completo da apresentação Sprint Review 2 em PDF.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = "Roteiro_Sprint2_CeresDiagnostico.pdf"

# ── Cores ────────────────────────────────────────────────────────────────────
AZUL_ESCURO  = colors.HexColor("#0D1B2A")
VERDE        = colors.HexColor("#4CAF50")
LARANJA      = colors.HexColor("#FF9800")
CINZA_CLARO  = colors.HexColor("#B0BEC5")
CINZA_BG     = colors.HexColor("#F5F5F5")
AZUL_HEADER  = colors.HexColor("#1A3A5C")
AMARELO_BG   = colors.HexColor("#FFF8E1")
VERDE_BG     = colors.HexColor("#E8F5E9")
LARANJA_BG   = colors.HexColor("#FFF3E0")
AZUL_BG      = colors.HexColor("#E3F2FD")

# ── Estilos ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

titulo_doc = ParagraphStyle("titulo_doc",
    fontSize=20, leading=26, textColor=AZUL_ESCURO,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)

subtitulo_doc = ParagraphStyle("subtitulo_doc",
    fontSize=12, leading=16, textColor=colors.HexColor("#555555"),
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)

slide_header = ParagraphStyle("slide_header",
    fontSize=14, leading=18, textColor=colors.white,
    fontName="Helvetica-Bold", alignment=TA_LEFT,
    leftIndent=8, spaceAfter=0, spaceBefore=0)

fala_style = ParagraphStyle("fala",
    fontSize=10.5, leading=16, textColor=colors.HexColor("#1A1A1A"),
    fontName="Helvetica", alignment=TA_JUSTIFY,
    leftIndent=6, rightIndent=6, spaceAfter=6)

termo_titulo = ParagraphStyle("termo_titulo",
    fontSize=9.5, leading=13, textColor=AZUL_ESCURO,
    fontName="Helvetica-Bold", leftIndent=6)

termo_def = ParagraphStyle("termo_def",
    fontSize=9.5, leading=13, textColor=colors.HexColor("#333333"),
    fontName="Helvetica", leftIndent=6)

secao_titulo = ParagraphStyle("secao_titulo",
    fontSize=13, leading=18, textColor=colors.white,
    fontName="Helvetica-Bold", alignment=TA_CENTER,
    spaceAfter=0, spaceBefore=0)

banca_pergunta = ParagraphStyle("banca_pergunta",
    fontSize=10, leading=14, textColor=colors.HexColor("#7B3F00"),
    fontName="Helvetica-Bold", leftIndent=6, spaceAfter=2)

banca_resposta = ParagraphStyle("banca_resposta",
    fontSize=10, leading=15, textColor=colors.HexColor("#1A1A1A"),
    fontName="Helvetica", leftIndent=6, alignment=TA_JUSTIFY)

glossario_item = ParagraphStyle("glossario_item",
    fontSize=9.5, leading=14, textColor=colors.HexColor("#1A1A1A"),
    fontName="Helvetica", leftIndent=6)

nota_style = ParagraphStyle("nota",
    fontSize=9, leading=13, textColor=colors.HexColor("#555555"),
    fontName="Helvetica-Oblique", leftIndent=6)

# ── Helpers ──────────────────────────────────────────────────────────────────

def slide_box(numero, titulo):
    """Cabeçalho colorido do slide."""
    label = f"SLIDE {numero} — {titulo}"
    data = [[Paragraph(label, slide_header)]]
    t = Table(data, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_HEADER),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [AZUL_HEADER]),
    ]))
    return t

def fala_box(texto, bg=CINZA_BG):
    """Caixa de fala com fundo claro."""
    paras = []
    for linha in texto.strip().split("\n"):
        linha = linha.strip()
        if linha:
            paras.append(Paragraph(linha, fala_style))
        else:
            paras.append(Spacer(1, 4))
    data = [[paras]]
    t = Table(data, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ]))
    return t

def termos_box(termos):
    """Caixa de termos técnicos: [(termo, definição)]"""
    rows = []
    for t, d in termos:
        rows.append([
            Paragraph(f"<b>{t}</b>", termo_titulo),
            Paragraph(d, termo_def),
        ])
    tbl = Table(rows, colWidths=[4.5*cm, 12.5*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("LINEBELOW",     (0,0), (-1,-2), 0.3, colors.HexColor("#BBDEFB")),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#90CAF9")),
    ]))
    return tbl

def secao_header(texto, cor=AZUL_ESCURO):
    data = [[Paragraph(texto, secao_titulo)]]
    t = Table(data, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), cor),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

def banca_box(pergunta, resposta):
    paras_r = []
    for linha in resposta.strip().split("\n"):
        linha = linha.strip()
        if linha:
            paras_r.append(Paragraph(linha, banca_resposta))
        else:
            paras_r.append(Spacer(1, 4))
    data = [
        [Paragraph(f"❓ {pergunta}", banca_pergunta)],
        [paras_r],
    ]
    t = Table(data, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AMARELO_BG),
        ("BACKGROUND",    (0,1), (-1,-1), LARANJA_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("BOX",           (0,0), (-1,-1), 0.8, LARANJA),
    ]))
    return t

def label(texto, cor=VERDE):
    p = ParagraphStyle("lbl", fontSize=9, fontName="Helvetica-Bold",
                       textColor=cor, spaceBefore=8, spaceAfter=2)
    return Paragraph(texto.upper(), p)

# ═══════════════════════════════════════════════════════════════════════════
# CONTEÚDO
# ═══════════════════════════════════════════════════════════════════════════

story = []

# Capa do roteiro
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Roteiro de Apresentação", titulo_doc))
story.append(Paragraph("Sprint Review 2 — Ceres Diagnóstico", subtitulo_doc))
story.append(Paragraph("TCC Engenharia da Computação · IFMT Cuiabá · Maio / 2026", subtitulo_doc))
story.append(Spacer(1, 0.3*cm))

tempo_data = [
    [Paragraph("<b>Tempo total</b>", termo_titulo), Paragraph("~15 minutos", termo_def)],
    [Paragraph("<b>Slides</b>", termo_titulo), Paragraph("10 slides", termo_def)],
    [Paragraph("<b>Ritmo</b>", termo_titulo), Paragraph("Slides 6 e 7 são os mais densos — não apresse. No slide 5, passe rápido em A e B, foque em C, D e E.", termo_def)],
    [Paragraph("<b>Se estourar</b>", termo_titulo), Paragraph("Corte o slide 8 (gap) pela metade — cite os 4 fatores em 30 segundos.", termo_def)],
]
t = Table(tempo_data, colWidths=[4.5*cm, 12.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), VERDE_BG),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("LINEBELOW",     (0,0), (-1,-2), 0.3, colors.HexColor("#C8E6C9")),
    ("BOX",           (0,0), (-1,-1), 0.8, VERDE),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width="100%", thickness=1, color=AZUL_ESCURO))
story.append(Spacer(1, 0.3*cm))

# ── SLIDES ────────────────────────────────────────────────────────────────────

slides = [
    {
        "num": 1, "titulo": "CAPA", "tempo": "20 segundos",
        "fala": (
            "Boa tarde. Meu nome é Namem, e esse é o Sprint Review 2 do Ceres Diagnóstico — "
            "meu TCC de Engenharia da Computação aqui no IFMT Cuiabá. O projeto constrói um "
            "sistema embarcado de detecção de doenças no tomateiro usando inteligência artificial "
            "em microcontrolador, sem depender de internet."
        ),
        "termos": [],
        "dica": "Fale com calma. Olhe para a banca, não para o slide.",
    },
    {
        "num": 2, "titulo": "VISÃO GERAL", "tempo": "1 minuto",
        "fala": (
            "O problema: o produtor rural, especialmente em Mato Grosso, não tem acesso rápido "
            "a diagnóstico de doenças. Uma doença não detectada pode destruir 100% da safra.\n\n"
            "A solução é um ESP32-S3 — um microcontrolador, que é basicamente um computador do "
            "tamanho de uma moeda — com câmera acoplada e inteligência artificial embarcada. O "
            "produtor aponta para a folha e recebe o diagnóstico no campo, sem internet.\n\n"
            "O sistema publica os dados via MQTT — um protocolo de comunicação leve para IoT, "
            "Internet das Coisas. Esses dados são recebidos pelo Django, o servidor web em Python "
            "que desenvolvemos, persistidos no PostgreSQL e exibidos no app Flutter.\n\n"
            "As sprints 0 e 1 já foram apresentadas — esse slide é só contexto para quem não acompanhou."
        ),
        "termos": [
            ("ESP32-S3", "Microcontrolador da Espressif com WiFi, Bluetooth e 8MB de memória PSRAM. É o 'cérebro' do dispositivo de campo."),
            ("Microcontrolador", "Computador compacto em um único chip — processa, armazena e controla periféricos com pouquíssima energia."),
            ("MQTT", "Protocolo de mensagens leve para IoT. Usa apenas 2 bytes de cabeçalho vs ~820 bytes do HTTP. Projetado para redes instáveis."),
            ("IoT", "Internet das Coisas — dispositivos físicos conectados que coletam e enviam dados."),
            ("Django", "Framework web em Python usado para construir o servidor REST que recebe, processa e expõe os dados via API."),
            ("Flutter", "Framework do Google para criar apps móveis multiplataforma (Android/iOS) com um único código."),
        ],
        "dica": "Sprint 0 e 1 = contexto rápido. Não entre em detalhes técnicos aqui.",
    },
    {
        "num": 3, "titulo": "O QUE PROMETEMOS", "tempo": "1 minuto e 30 segundos",
        "fala": (
            "Na Sprint Review 1, a promessa original era entregar o app Flutter. Tomamos uma "
            "decisão técnica: com o hardware ESP32-S3 em mãos e o modelo de IA pronto, fazia "
            "mais sentido validar a pilha completa de IA e IoT antes de construir uma interface "
            "sem dados reais. O Flutter sem dados reais do hardware seria só interface sem substância.\n\n"
            "As duas metas desta sprint foram: primeiro, entender por que o modelo vai bem no "
            "laboratório mas mal no campo — e tentar melhorar isso. Segundo, validar o pipeline "
            "IoT de ponta a ponta em hardware real, do sensor ao banco de dados."
        ),
        "termos": [
            ("Pipeline IoT", "Caminho completo dos dados: ESP32 coleta → publica via MQTT → servidor recebe → banco de dados armazena → API entrega."),
            ("API REST", "Interface que permite ao app e a outros sistemas buscar dados do servidor via HTTP com autenticação."),
        ],
        "dica": "Deixe claro que foi uma decisão consciente, não um atraso.",
    },
    {
        "num": 4, "titulo": "DATASET PLANTVILLAGE", "tempo": "1 minuto e 30 segundos",
        "fala": (
            "Para treinar qualquer modelo de inteligência artificial, precisamos de um dataset — "
            "um conjunto de dados rotulados, nesse caso fotos de folhas de tomate com a doença identificada.\n\n"
            "Usamos o PlantVillage, criado por Hughes e Salathé em 2015. O título do paper é "
            "'An open access repository of images on plant health to enable the development of "
            "mobile disease diagnostics'. É o maior benchmark público de doenças de plantas — "
            "benchmark significa conjunto de referência usado pela comunidade científica para "
            "comparar resultados.\n\n"
            "São 18 mil imagens coletadas em laboratório com fundo controlado. Aplicamos "
            "augmentation — multiplicação dos dados com variações como rotação, flip e mudança "
            "de brilho — e chegamos a 88 mil imagens de treino. Licença CC BY 4.0, uso acadêmico "
            "e comercial permitido.\n\n"
            "Detalhe importante: esse fundo cinza uniforme de laboratório é a raiz do problema "
            "que investigamos nessa sprint inteira."
        ),
        "termos": [
            ("Dataset", "Conjunto de dados rotulados usado para treinar e avaliar modelos de IA."),
            ("Benchmark", "Conjunto de referência padrão da comunidade científica para comparar resultados entre trabalhos diferentes."),
            ("Augmentation", "Técnica de multiplicar dados aplicando variações nas imagens: rotação, flip, zoom, brilho, saturação."),
            ("CC BY 4.0", "Licença Creative Commons que permite uso, redistribuição e modificação com atribuição ao autor — inclusive comercialmente."),
            ("Split 70/15/15", "Divisão do dataset: 70% para treino, 15% para validação durante o treino, 15% para teste final (dados nunca vistos)."),
        ],
        "dica": "Enfatize o fundo cinza — é a ponte para o próximo slide.",
    },
    {
        "num": 5, "titulo": "JORNADA A → E", "tempo": "2 minutos e 30 segundos",
        "fala": (
            "Nessa sprint conduzimos 5 experimentos. Vou passar rápido nos dois primeiros, "
            "que são da sprint anterior, e focar nos três novos.\n\n"
            "Exp A: treinamos na nuvem pelo Edge Impulse usando MobileNetV2 — uma arquitetura "
            "de rede neural do Google otimizada para dispositivos pequenos. O problema foi a "
            "quantização INT8 automática: quantização é o processo de comprimir o modelo de "
            "números de 32 bits para 8 bits — reduz o tamanho drasticamente, mas sem calibração "
            "perdeu 30 pontos percentuais de acurácia. Descartado.\n\n"
            "Exp B: treinamos localmente com TensorFlow no WSL2 — subsistema Linux dentro do "
            "Windows — usando a GPU RTX 3060 Ti. A quantização desta vez foi calibrada: passamos "
            "50 amostras reais durante a compressão. Resultado: 98% de acurácia, 639 KB. "
            "Esse virou a base do projeto.\n\n"
            "Exp C: tentamos resolver o gap de campo com augmentação sintética de fundo — "
            "177 mil composições, 650 minutos de GPU. Zero pontos de ganho em campo. "
            "O rembg gerou artefatos de borda que o modelo aprendeu como feature falsa — "
            "isso motivou o Exp D.\n\n"
            "Exp D: misturamos 677 fotos reais de campo ao treinamento. Fine-tuning — ajuste "
            "fino do modelo já treinado. Resultado: +10 pontos percentuais em imagens nunca vistas.\n\n"
            "Exp E: adicionamos Focal Loss — uma função de perda que prioriza exemplos difíceis "
            "no treino — e augmentação de cor agressiva. +16 pontos na Índia, +8,5 em Bangladesh. "
            "Esse é o modelo final: 638 KB."
        ),
        "termos": [
            ("MobileNetV2", "Arquitetura de rede neural do Google (Howard et al., 2017) otimizada para dispositivos com restrição de memória."),
            ("Quantização INT8", "Compressão do modelo: converte pesos de float32 (4 bytes) para int8 (1 byte). Reduz tamanho ~4x com pequena perda de acurácia SE calibrada."),
            ("Calibração", "Processo de passar amostras reais pelo modelo durante a quantização para que ele aprenda a ajustar os valores comprimidos."),
            ("TensorFlow", "Principal biblioteca de machine learning do Google. Usada para definir, treinar e exportar modelos de IA."),
            ("WSL2", "Windows Subsystem for Linux 2 — ambiente Linux dentro do Windows com acesso direto à GPU via CUDA."),
            ("GPU / CUDA", "GPU (placa de vídeo) processa milhares de operações em paralelo — essencial para treinar redes neurais rapidamente. CUDA é a interface da NVIDIA."),
            ("Fine-tuning", "Ajuste fino: continuar o treinamento de um modelo já treinado com novos dados específicos, sem partir do zero."),
            ("Focal Loss", "Função de perda (Lin et al., 2017, Facebook AI Research) que dá 4× mais peso de aprendizado para exemplos que o modelo erra com alta confiança."),
            ("rembg", "Ferramenta que usa a rede U2-Net para remover o fundo de imagens (segmentação semântica pixel a pixel)."),
        ],
        "dica": "A linha do rodapé em laranja explica por que C falhou — não precisa elaborar muito aqui, já está na tabela.",
    },
    {
        "num": 6, "titulo": "VALIDAÇÃO EM 3 DATASETS", "tempo": "2 minutos",
        "fala": (
            "O Exp D misturou 677 fotos reais do PlantDoc ao treinamento. Com isso, o modelo "
            "passou de ~20% para 30,43% em imagens de campo nunca vistas — 10 pontos de ganho real.\n\n"
            "Para garantir que esse ganho não era específico ao PlantDoc, validamos em dois "
            "datasets completamente independentes — nunca tocados em nenhum experimento.\n\n"
            "O Tomato-Village: 217 fotos de Rajasthan, na Índia. O Daffodil BD: 1.616 fotos "
            "de Bangladesh. Nenhum desses dados existia durante o treino.\n\n"
            "O Exp E — Focal Loss com augmentação de cor — melhorou ainda mais: +16 pontos "
            "na Índia, +8,5 pontos em Bangladesh comparado ao Exp D. Esse é o modelo final.\n\n"
            "A linha do PlantDoc está marcada como não comparável porque o Exp D treinou "
            "nesse split — seria comparação injusta."
        ),
        "termos": [
            ("Dataset independente", "Conjunto de dados que não foi usado em nenhuma etapa do treinamento — garante que o resultado não é memorização."),
            ("PlantDoc", "Dataset de campo real com ~1.353 fotos, coletadas nos EUA e Europa, usado como validação de campo."),
            ("Tomato-Village", "217 fotos de tomateiros em Rajasthan, Índia. Nunca usado no treino — validação independente geográfica."),
            ("Daffodil BD", "1.616 fotos de Bangladesh coletadas com iPhone 11 em campo aberto. Terceira validação independente."),
            ("Δ (delta)", "Diferença em pontos percentuais entre Exp D e Exp E no mesmo dataset."),
        ],
        "dica": "Esse slide é o ponto mais forte da sprint — mostre com segurança os números +16pp e +8,5pp.",
    },
    {
        "num": 7, "titulo": "COMPARAÇÃO COM LITERATURA", "tempo": "1 minuto e 30 segundos",
        "fala": (
            "Esses resultados não são uma anomalia — é o padrão documentado na literatura.\n\n"
            "Mohanty et al. em 2016, no Frontiers in Plant Science, criou o primeiro trabalho "
            "relevante usando deep learning para doenças de plantas. 99% no laboratório, ~31% "
            "em campo real. Nunca embarcou em hardware.\n\n"
            "Singh et al. em 2020, no IEEE Access, foi o primeiro a comparar sistematicamente "
            "laboratório versus campo, chegando a 55% usando fotos reais. Também sem hardware embarcado.\n\n"
            "O diferencial do Ceres: 638 KB rodando dentro de um ESP32-S3 — nenhum dos dois "
            "trabalhos embarcou a solução em microcontrolador. MobileNetV2 do Howard et al., "
            "2017, é a única arquitetura que consegue esse nível de acurácia dentro das "
            "restrições de memória de um microcontrolador."
        ),
        "termos": [
            ("Deep learning", "Aprendizado profundo — redes neurais com muitas camadas que aprendem representações hierárquicas dos dados."),
            ("Frontiers in Plant Science", "Periódico científico de acesso aberto, Qualis B1 na área de Ciências Agrárias."),
            ("IEEE Access", "Periódico multidisciplinar do IEEE, Qualis A2, acesso aberto."),
            ("30,43% vs 55% (Singh)", "Nossa acurácia de campo é menor, mas com modelo 638KB em microcontrolador. Singh usou servidor com modelo de dezenas de MB."),
        ],
        "dica": "Se perguntarem '30% é ruim': 'É o padrão da área para sistemas sem servidor. O diferencial é funcionar offline em 638KB.'",
    },
    {
        "num": 8, "titulo": "POR QUE O GAP LAB-CAMPO EXISTE?", "tempo": "1 minuto e 30 segundos",
        "fala": (
            "Por que o gap laboratório-campo existe mesmo depois de todos esses experimentos? "
            "São quatro fatores independentes.\n\n"
            "Primeiro: o fundo. PlantVillage tem fundo cinza uniforme — o modelo aprende o "
            "fundo como parte da identidade da doença. Resolvido parcialmente pelo Exp D.\n\n"
            "Segundo: iluminação e câmera. Luz solar direta, sombras e câmeras de celular "
            "criam uma distribuição visual completamente diferente do laboratório. O Exp E "
            "ataca isso com augmentação de cor.\n\n"
            "Terceiro: variedade geográfica. Uma cultivar de tomate de Rajasthan tem morfologia "
            "foliar diferente de uma cultivar americana ou mato-grossense. O modelo nunca viu "
            "folhas indianas ou brasileiras durante o treino.\n\n"
            "Quarto: estágio fenológico — a fase de desenvolvimento da planta. Folha jovem e "
            "folha velha da mesma planta doente parecem diferentes, e o laboratório não cobre isso.\n\n"
            "Resolver só um fator não fecha o gap. A validação definitiva é com produtores "
            "de Sorriso-MT — fotos brasileiras, condições reais do Mato Grosso."
        ),
        "termos": [
            ("Gap lab-campo", "Diferença de desempenho entre o modelo no laboratório (controlado) e no campo (condições reais)."),
            ("Distribuição visual", "Padrão estatístico dos pixels de um conjunto de imagens. Laboratório e campo têm distribuições diferentes."),
            ("Cultivar", "Variedade específica de uma planta desenvolvida por seleção ou melhoramento genético."),
            ("Estágio fenológico", "Fase de desenvolvimento da planta: germinação, crescimento vegetativo, floração, frutificação etc."),
            ("Domain shift", "Mudança de domínio — quando o modelo é testado em condições diferentes das do treinamento."),
        ],
        "dica": "Se o tempo apertar: cite os 4 fatores rapidamente e vá direto para a frase final sobre Sorriso-MT.",
    },
    {
        "num": 9, "titulo": "PRÓXIMOS PASSOS", "tempo": "1 minuto",
        "fala": (
            "A cadeia de validação do modelo tem quatro níveis. Nível 1, laboratório: feito, "
            "98%. Nível 2, campo com datasets públicos internacionais: feito, 30% PlantDoc. "
            "Faltam os níveis 3 e 4.\n\n"
            "Nível 3 é a Sprint 2: embarcar o modelo TFLite Micro — formato do TensorFlow para "
            "microcontroladores — no ESP32-S3 com câmera OV5640. A meta é latência menor que "
            "300 milissegundos por inferência. Depende da chegada do hardware.\n\n"
            "Nível 4 é a Sprint 3: validação com produtores de Sorriso-MT — a métrica que vai "
            "para o TCC como resultado final. Paralelamente, o app Flutter entra nessa sprint."
        ),
        "termos": [
            ("TFLite Micro", "Versão do TensorFlow Lite para microcontroladores. Roda modelos .tflite com pouquíssima RAM e sem sistema operacional."),
            ("Inferência", "O ato do modelo analisar uma nova imagem e produzir uma classificação. Diferente do treino — aqui ele só prevê."),
            ("Latência", "Tempo entre a captura da imagem e o resultado da classificação. Meta: < 300ms no ESP32-S3."),
            ("OV5640", "Sensor de câmera 5MP com interface MIPI/DVP — compatível com ESP32-S3, captura frames em resolução suficiente para inferência."),
            ("Sorriso-MT", "Município do Mato Grosso, maior produtor de soja do Brasil e importante polo de tomateiro — contexto real do sistema."),
        ],
        "dica": "Mencione que o Flutter não sumiu do roadmap — só foi reordenado.",
    },
    {
        "num": 10, "titulo": "ENCERRAMENTO", "tempo": "30 segundos",
        "fala": (
            "Resumindo a Sprint 2: cinco experimentos com metodologia científica completa — "
            "incluindo dois resultados negativos, os experimentos A e C, que têm tanto valor "
            "acadêmico quanto os positivos porque documentam o que não funciona e por quê.\n\n"
            "Modelo final: Exp E, 638 KB, validado em três continentes. O gap laboratório-campo "
            "está documentado com respaldo na literatura. O próximo marco é TFLite Micro no "
            "ESP32-S3 com câmera real.\n\n"
            "Obrigado — fico à disposição para perguntas."
        ),
        "termos": [],
        "dica": "Fale com calma. Não apresse o encerramento — é a última impressão.",
    },
]

for sl in slides:
    block = []
    block.append(slide_box(sl["num"], sl["titulo"]))

    tempo_p = ParagraphStyle("tp", fontSize=9, fontName="Helvetica-Bold",
                             textColor=VERDE, spaceBefore=3, spaceAfter=3)
    block.append(Paragraph(f"⏱  Tempo estimado: {sl['tempo']}", tempo_p))

    block.append(label("O que dizer", AZUL_ESCURO))
    block.append(fala_box(sl["fala"]))

    if sl.get("termos"):
        block.append(label("Termos técnicos deste slide", AZUL_ESCURO))
        block.append(termos_box(sl["termos"]))

    if sl.get("dica"):
        dica_p = ParagraphStyle("dica", fontSize=9, fontName="Helvetica-Oblique",
                                textColor=colors.HexColor("#7B3F00"),
                                leftIndent=6, spaceAfter=0)
        block.append(Paragraph(f"💡 Dica: {sl['dica']}", dica_p))

    block.append(Spacer(1, 0.5*cm))
    story.append(KeepTogether(block[:3]))  # mantém cabeçalho + fala juntos
    story.extend(block[3:])

# ── SEÇÃO: PERGUNTAS DA BANCA ────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=1.5, color=LARANJA))
story.append(Spacer(1, 0.2*cm))
story.append(secao_header("PERGUNTAS PROVÁVEIS DA BANCA", LARANJA))
story.append(Spacer(1, 0.3*cm))

bancas = [
    (
        "30% de acurácia em campo é um bom resultado?",
        "Sim — é o padrão da área para sistemas embarcados offline. Mohanty et al. 2016 "
        "obteve ~31% em campo com um modelo de servidor. O diferencial do Ceres é que roda "
        "em 638KB dentro de um microcontrolador, sem internet, no campo. Nenhum dos trabalhos "
        "de referência embarcou a solução em hardware real."
    ),
    (
        "O que pode ser feito para melhorar a acurácia em campo?",
        "A principal alavanca é coletar fotos reais locais — tomateiros de Mato Grosso, nas "
        "condições reais de Sorriso. Isso está planejado como Nível 4 da cadeia de validação. "
        "Tecnicamente, domain adaptation — técnicas que treinam o modelo para ser invariante "
        "à diferença entre laboratório e campo — é a direção mais promissora na literatura. "
        "Singh et al. 2020 confirmam: dados reais de campo superam qualquer augmentação sintética."
    ),
    (
        "MobileNetV2 é o limite da arquitetura para o ESP32-S3?",
        "Para o ESP32-S3 N16R8 com 8MB de PSRAM, MobileNetV2 96×96 INT8 é uma das poucas "
        "arquiteturas que cabem com folga — 638KB de modelo mais aproximadamente 2–3MB de "
        "buffers em tempo de inferência. EfficientNet-Lite0 e MobileNetV3-Small também "
        "caberiam com resultados similares. O gargalo real não é a arquitetura — é a "
        "resolução de entrada: 96×96 pixels é muito baixo para capturar detalhes finos de "
        "textura foliar. Com 224×224 a acurácia de campo provavelmente subiria, mas não "
        "cabe na memória do ESP32-S3."
    ),
    (
        "Se fosse um sistema em nuvem, sem o ESP32, a acurácia seria melhor?",
        "Sim, substancialmente. Sem a restrição de 638KB, poderíamos usar ResNet50 ou "
        "EfficientNetB4 com entrada de 224×224 ou maior — a literatura mostra 55–65% em "
        "campo real com esses modelos. Mas o requisito central do projeto é funcionar "
        "offline, no campo, sem internet e sem custo de infraestrutura. Um produtor em "
        "campo no Mato Grosso muitas vezes não tem sinal. A restrição de tamanho não é "
        "uma limitação — é o requisito que define o projeto."
    ),
    (
        "Por que usaram o PlantVillage e não outro dataset?",
        "PlantVillage é o benchmark padrão da área, com licença aberta CC BY 4.0, "
        "usado pelos dois trabalhos de referência — Mohanty 2016 e Singh 2020 — "
        "o que permite comparação direta de resultados. Com 18.160 imagens e 10 classes "
        "do tomateiro exatamente mapeadas para o escopo do Ceres, é o único dataset "
        "público que atende simultaneamente os requisitos de tamanho, licença e cobertura "
        "de doenças."
    ),
    (
        "Resultados negativos (Exp A e C) têm valor científico?",
        "Sim — documentar o que não funciona e por quê é parte essencial do método científico. "
        "O Exp A mostrou que quantização sem calibração perde 30 pontos percentuais, "
        "informação útil para qualquer trabalho futuro com TinyML. O Exp C mostrou que "
        "augmentação sintética de fundo não resolve o gap de campo, contradizendo a "
        "hipótese inicial e motivando o Exp D. Ambos estão documentados com análise de causa."
    ),
]

for p, r in bancas:
    story.append(banca_box(p, r))
    story.append(Spacer(1, 0.3*cm))

# ── SEÇÃO: GLOSSÁRIO RÁPIDO ──────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=1.5, color=AZUL_ESCURO))
story.append(Spacer(1, 0.2*cm))
story.append(secao_header("GLOSSÁRIO RÁPIDO — USE SE PERGUNTAREM", AZUL_ESCURO))
story.append(Spacer(1, 0.2*cm))

glossario = [
    ("Dataset", "Conjunto de dados rotulados para treinar IA"),
    ("Acurácia", "Percentual de acertos do modelo"),
    ("Quantização INT8", "Compressão do modelo de 32 bits para 8 bits"),
    ("Fine-tuning", "Ajuste fino de um modelo já treinado com novos dados"),
    ("Focal Loss", "Função que prioriza exemplos difíceis no treino"),
    ("Inferência", "O modelo analisando uma imagem nova e dando um resultado"),
    ("TFLite Micro", "TensorFlow comprimido para rodar em microcontroladores"),
    ("MQTT", "Protocolo de comunicação leve para IoT"),
    ("MobileNetV2", "Arquitetura de rede neural otimizada para dispositivos pequenos"),
    ("Augmentation", "Multiplicar dados aplicando variações nas imagens"),
    ("Benchmark", "Conjunto de referência padrão da comunidade científica"),
    ("Domain shift", "Modelo testado em condições diferentes do treino"),
    ("Gap lab-campo", "Diferença de acurácia entre laboratório e campo real"),
    ("PSRAM", "Memória RAM externa no ESP32-S3 — 8MB, onde o modelo é carregado"),
    ("WSL2", "Linux dentro do Windows, com acesso à GPU para treino"),
    ("PlantVillage", "Dataset de 18.160 imagens de doenças de plantas — Hughes & Salathé 2015"),
]

rows_g = []
for i in range(0, len(glossario), 2):
    row = []
    for j in range(2):
        if i + j < len(glossario):
            t, d = glossario[i+j]
            row.append(Paragraph(f"<b>{t}:</b> {d}", glossario_item))
        else:
            row.append(Paragraph("", glossario_item))
    rows_g.append(row)

tg = Table(rows_g, colWidths=[8.5*cm, 8.5*cm])
tg.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), CINZA_BG),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("LINEBELOW",     (0,0), (-1,-2), 0.3, colors.HexColor("#CCCCCC")),
    ("LINEBEFORE",    (1,0), (1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("BOX",           (0,0), (-1,-1), 0.8, AZUL_ESCURO),
]))
story.append(tg)
story.append(Spacer(1, 0.5*cm))

rodape = ParagraphStyle("rodape", fontSize=8, fontName="Helvetica",
                        textColor=CINZA_CLARO, alignment=TA_CENTER)
story.append(Paragraph(
    "Ceres Diagnóstico · TCC Engenharia da Computação · IFMT Cuiabá · "
    "Namem Rachid Jaudy Neto · Maio/2026",
    rodape
))

# ── Gerar PDF ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Roteiro Sprint Review 2 — Ceres Diagnóstico",
    author="Namem Rachid Jaudy Neto",
)
doc.build(story)
print(f"PDF gerado: {OUTPUT}")
