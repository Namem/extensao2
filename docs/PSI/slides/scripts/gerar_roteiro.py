"""Gera roteiro_apresentacao.pdf — guia de fala para a defesa de 30 min (PSI)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

VE   = HexColor("#1B4332")
VM   = HexColor("#2D6A4F")
VC   = HexColor("#52B788")
DO   = HexColor("#D4A017")
CI   = HexColor("#F4F6F0")
GT   = HexColor("#1F2937")
RD   = HexColor("#B91C1C")
GN   = HexColor("#166534")
AZUL = HexColor("#1D4ED8")
AMA  = HexColor("#FFFBEB")
BOR  = HexColor("#92400E")
LGREY = HexColor("#F3F4F6")

OUT = "roteiro_apresentacao.pdf"

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.0*cm, rightMargin=2.0*cm,
    topMargin=2.2*cm, bottomMargin=2.0*cm
)

styles = getSampleStyleSheet()

def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

TituloDoc  = sty("TituloDoc", fontSize=18, textColor=white,   alignment=TA_CENTER, leading=24, spaceAfter=4)
SubtituloDoc = sty("SubtituloDoc", fontSize=11, textColor=HexColor("#B7E4C7"), alignment=TA_CENTER, leading=16, spaceAfter=0)
SlideHdr   = sty("SlideHdr",  fontSize=13, textColor=white,   leading=18, spaceAfter=0)
Tempo      = sty("Tempo",     fontSize=10, textColor=DO,      leading=14, spaceAfter=0)
FalaNormal = sty("FalaNormal",fontSize=10, textColor=GT,      leading=15, spaceAfter=4, leftIndent=8)
FalaNegrito = sty("FalaNegrito",fontSize=10,textColor=VE,     leading=15, spaceAfter=2, leftIndent=8, fontName="Helvetica-Bold")
Alerta     = sty("Alerta",    fontSize=9.5,textColor=BOR,     leading=13, spaceAfter=4, leftIndent=8, fontName="Helvetica-Oblique")
Destaque   = sty("Destaque",  fontSize=9.5,textColor=GN,      leading=13, spaceAfter=4, leftIndent=8, fontName="Helvetica-Bold")
Rodape     = sty("Rodape",    fontSize=8,  textColor=HexColor("#9CA3AF"), alignment=TA_CENTER, leading=12, spaceAfter=0)

def slide_bloco(numero, titulo, tempo, falas):
    """Retorna lista de flowables para um bloco de slide."""
    bloco = []
    bloco.append(Spacer(1, 0.25*cm))
    # Header
    hdr_data = [[
        Paragraph(f"<b>SLIDE {numero}</b>", SlideHdr),
        Paragraph(titulo, sty("TituloSlide", fontSize=12, textColor=white, leading=16)),
        Paragraph(f"<b>{tempo}</b>", sty("TempoR", fontSize=11, textColor=DO, alignment=2, leading=16))
    ]]
    hdr_t = Table(hdr_data, colWidths=[2.2*cm, 11.3*cm, 3.0*cm])
    hdr_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), VE),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING",(0,0), (-1,-1), 6),
        ("TOPPADDING",  (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [4,4,4,4]),
    ]))
    bloco.append(hdr_t)
    for f in falas:
        tag, texto = f
        if tag == "fala":
            bloco.append(Paragraph("▸ " + texto, FalaNormal))
        elif tag == "enfase":
            bloco.append(Paragraph("★ " + texto, FalaNegrito))
        elif tag == "alerta":
            bloco.append(Paragraph("⚠ " + texto, Alerta))
        elif tag == "ok":
            bloco.append(Paragraph("✓ " + texto, Destaque))
        elif tag == "transicao":
            bloco.append(Paragraph("→ " + texto, sty("Trans", fontSize=9.5, textColor=AZUL,
                leading=13, spaceAfter=3, leftIndent=8, fontName="Helvetica-Oblique")))
    bloco.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#D1D5DB"), spaceAfter=2, spaceBefore=1))
    return bloco

slides = [
    (1, "Capa", "0:00–0:30", [
        ("fala", "Bom dia. Meu nome é Namem, e vou apresentar o Ceres Diagnóstico — um sistema TinyML embarcado para detecção de doenças em tomateiro."),
        ("fala", "O trabalho integra três frentes: um microcontrolador ESP32-S3, um backend Django e um app Flutter. Tudo conectado por MQTT."),
        ("transicao", "Vou começar pelo problema que motivou o projeto."),
    ]),
    (2, "Roteiro", "0:30–0:45", [
        ("fala", "Mostrarei o problema, como construí o modelo, a surpresa que foi o gap campo-laboratório, os cinco experimentos, as três arquiteturas de inferência e o sistema em funcionamento."),
        ("transicao", "Partindo do problema."),
    ]),
    (3, "Problema e Motivação", "0:45–2:00", [
        ("fala", "O tomateiro é a terceira maior produção mundial de vegetais — R$ 10 bilhões por ano só no Brasil."),
        ("fala", "Doenças foliares podem causar perda total de safra. E diagnóstico preciso depende de agrônomos especializados que simplesmente não chegam ao pequeno produtor rural."),
        ("enfase", "Sorriso-MT concentra grande parte dos produtores de tomate do MT. A maioria são pequenos agricultores sem assistência técnica regular."),
        ("fala", "Conectividade rural é instável. Uma solução 100% cloud não funciona no campo."),
        ("transicao", "Nossa proposta resolve exatamente esse cenário."),
    ]),
    (4, "Nossa Proposta", "2:00–3:00", [
        ("fala", "Um sistema de baixo custo que classifica 10 doenças do tomateiro e funciona offline — sem internet."),
        ("fala", "O modelo cabe em 638 KB, roda em microcontrolador, e o código é totalmente aberto."),
        ("transicao", "Para construir isso, precisávamos de dados. Vou mostrar o pipeline."),
    ]),
    (5, "Objetivos e Contribuições", "3:00–4:00", [
        ("fala", "O objetivo é integrar TinyML, IoT e app móvel num único pipeline reproduzível."),
        ("fala", "As cinco contribuições: dez classes com pipeline aberto; ESP32-S3 validado a 692 ms; três arquiteturas de inferência; validação em três datasets independentes; e cinco experimentos documentados, incluindo os negativos."),
        ("enfase", "Resultado negativo documentado é contribuição — é o que evita que outros repitam o mesmo caminho."),
        ("transicao", "Começando pelo dataset."),
    ]),
    (6, "Dataset e Pipeline", "4:00–5:00", [
        ("fala", "Usamos o PlantVillage — 18.160 imagens de folha de tomate, 10 classes, licença CC BY 4.0."),
        ("fala", "Split 70/15/15 com seed fixo para reproduzibilidade. Augmentation offline multiplicou o treino por 6, chegando a 88.949 imagens. O test set de 2.734 imagens nunca foi visto durante o treinamento."),
        ("transicao", "Vamos ver como são essas dez classes."),
    ]),
    (7, "As 10 Classes", "5:00–5:30", [
        ("fala", "Estas são as dez classes reais do modelo — fotos do PlantVillage. Notem a variabilidade: requeima tem lesão úmida escura, septoriose tem pontos brancos com halo amarelo, pinta-preta tem manchas concêntricas."),
        ("fala", "É essa diversidade visual que torna o problema desafiador."),
        ("transicao", "Antes de treinar, precisei escolher a arquitetura. Próximo slide."),
    ]),
    (8, "Comparativo de Modelos", "5:30–6:30", [
        ("fala", "Esta tabela está no artigo. Cinco arquiteturas avaliadas para rodar no ESP32-S3."),
        ("fala", "ResNet-50 e EfficientNet-B0: grandes demais para o microcontrolador — sem suporte no ESP32-S3. YOLO foi descartado imediatamente — é um detector de objetos com bounding box, incompatível com classificação de folha única. Tamanho mínimo ~6 MB, dez vezes maior que o nosso."),
        ("enfase", "MobileNetV2: único com suporte comprovado no ESP32-S3, arena de 200 KB dentro dos 512 KB disponíveis, acurácia superior ao MobileNetV1. Escolha evidente."),
        ("transicao", "Com a arquitetura definida, vamos ao treinamento."),
    ]),
    (9, "Treinamento e Quantização", "6:30–9:00", [
        ("fala", "Treinamento em duas fases — transfer learning correto. Fase 1: backbone ImageNet congelado, dez épocas. Fase 2: fine-tuning das últimas 30 camadas, quarenta épocas. Melhor val_acc: 97,90% na época 46."),
        ("fala", "Os três números contam a história da quantização: 62% com INT8 sem calibração — queda de 30 pp. Isso é o que acontece no Edge Impulse automático."),
        ("fala", "No TensorFlow local, com 50 batches do validation set como representative_dataset, a perda caiu de 30,5 pp para apenas 2,37 pp. O modelo embarcado entrega 95,76% — não os 98,13% do float."),
        ("alerta", "Esse delta de 2,37 pp é o custo da quantização bem feita. Vale o ganho: 4× menos espaço, 3× menos latência."),
        ("transicao", "Ótimo resultado em laboratório. O problema veio quando testamos em campo."),
    ]),
    (10, "Matriz de Confusão", "9:00–10:00", [
        ("fala", "2.618 de 2.734 corretas no test set de laboratório. As classes difíceis são as com lesões necróticas escuras — pinta-preta, septoriose e mancha bacteriana tendem a se confundir entre si."),
        ("fala", "Classes quase perfeitas: vira-cabeça e saudável — padrões visuais bem distintos."),
        ("alerta", "Esse padrão de confusão persistiu em todos os experimentos. É uma limitação do modelo atual."),
        ("transicao", "E em campo real?"),
    ]),
    (11, "Gap Laboratório–Campo", "10:00–12:00", [
        ("fala", "Testamos com o PlantDoc — 1.353 imagens capturadas no campo por vários fotógrafos, em condições reais de iluminação, ângulo e fundo."),
        ("enfase", "95,76% em laboratório. 20,77% em campo. Queda de 75 pp."),
        ("fala", "Mas não estamos sozinhos. Mohanty 2016 publicou 99% no PlantVillage. Singh 2020 avaliou o mesmo tipo de modelo no PlantDoc e obteve ~31%. Xu 2024 revisou 42 trabalhos e documentou queda entre 29 e 58 pp."),
        ("alerta", "Esse fenômeno tem nome: domain shift. O modelo aprende o fundo cinza controlado do laboratório, não as features diagnósticas da lesão."),
        ("transicao", "Então abrimos uma investigação com cinco experimentos para tentar resolver."),
    ]),
    (12, "Os 5 Experimentos", "12:00–14:30", [
        ("fala", "Exp A: Edge Impulse sem calibração INT8. 62% — confirmou o problema da quantização."),
        ("fala", "Exp B: TF local com calibração. 95,76% em laboratório, 20,77% em campo. Esse é o modelo base."),
        ("alerta", "Exp C: Tentamos trocar o fundo com augmentation sintética — rembg, U2-Net, 177.698 composições. Resultado: 20,24% em campo. Pior do que o Exp B. Resultado negativo documentado."),
        ("fala", "Exp D: Fine-tuning com 677 imagens reais do PlantDoc. Subiu para 30,43% em campo — +10 pp."),
        ("ok", "Exp E: Adicionamos Focal Loss γ=2, que reduz o peso das imagens fáceis de laboratório. +16 pp no Tomato-Village indiano. É o modelo final."),
        ("transicao", "Vou detalhar o resultado negativo — é pedagógico."),
    ]),
    (13, "Exp C — Resultado Negativo", "14:30–16:00", [
        ("fala", "A hipótese era razoável: se o modelo aprende o fundo, trocar o fundo deveria forçá-lo a olhar a lesão."),
        ("fala", "Geramos 177.698 composições sintéticas com rembg. O resultado foi 20,24% — marginalmente pior que o baseline."),
        ("alerta", "O que aconteceu: artefatos de borda do rembg e iluminação inconsistente criaram um domínio sintético que não representa o campo real. A classe saudável caiu a 0% em campo."),
        ("enfase", "Lição: síntese não substitui dado de campo. Só fine-tuning com imagens reais foi efetivo."),
        ("transicao", "O que funcionou — Exp D e E."),
    ]),
    (14, "Exp D e E — O Que Funcionou", "16:00–17:30", [
        ("fala", "Exp D: 677 imagens reais do PlantDoc/train, repetidas 10 vezes, com as 69 de teste nunca vistas. +10 pp."),
        ("fala", "O fator limitante identificado: volume de dados de campo, não o método de treinamento."),
        ("ok", "Exp E: Focal Loss γ=2 força o modelo a focar nas features da lesão, reduzindo o peso das imagens fáceis de fundo cinza. +16 pp no Tomato-Village."),
        ("transicao", "Mas esse ganho não é uniforme geograficamente."),
    ]),
    (15, "Gap Geográfico e Colapso de Classe", "17:30–18:30", [
        ("fala", "A acurácia em campo cai com a distância geográfica do PlantDoc: EUA/Europa 30,43%, Índia 27,65%, Bangladesh 18,13%."),
        ("fala", "Barbedo 2019 previu isso: variedades locais, iluminação tropical e estágio fenológico distinto degradam o desempenho."),
        ("alerta", "No Tomato-Village, 73% das folhas saudáveis indianas foram classificadas como septoriose — colapso de classe clássico sob domain shift extremo. O Exp E mitigou parcialmente."),
        ("transicao", "Com o modelo definido, a questão passou a ser: onde rodar?"),
    ]),
    (16, "Modelo Pronto — Onde Rodar?", "18:30–20:30", [
        ("fala", "O mesmo modelo INT8 de 638 KB pode rodar em três caminhos: direto no ESP32-S3, no smartphone Android, ou na nuvem via Django."),
        ("fala", "Caminho ①: ESP32-S3, 692 ms, offline, MQTT/TLS."),
        ("fala", "Caminho ②: Android on-device, tflite_flutter. Offline, sem hardware adicional."),
        ("fala", "Caminho ③: Cloud Django, 306 ms, HTTPS, Railway + PostgreSQL. Online, pipeline completo validado."),
        ("enfase", "Pivô de engenharia: o plano original era ESP32-S3 com câmera OV5640, 100% autônomo. Ao integrar, percebemos que a câmera precisaria de Sprint 2 para calibração. A adaptação foi oferecer o smartphone como sensor — mesmo modelo, mais flexibilidade imediata."),
        ("transicao", "Comparando os três caminhos."),
    ]),
    (17, "Comparativo Edge / Mobile / Cloud", "20:30–21:30", [
        ("fala", "Edge: 692 ms determinístico, offline, ESP32-S3 ~R$ 80. Mobile: ~200–400 ms estimados — não medimos empiricamente neste ciclo, limitação documentada — app no celular do produtor. Cloud: 306 ms via HTTPS, Railway."),
        ("fala", "Os três estão em produção ou validados. O mesmo arquivo INT8 de 638 KB nos três caminhos."),
        ("transicao", "Agora deixa eu mostrar o que de fato construímos."),
    ]),
    (18, "O Que Construímos", "21:30–22:30", [
        ("fala", "Este slide conta a história da construção. Começamos com o plano: ESP32-S3 autônomo com câmera OV5640. Durante a integração, percebemos que a câmera demandaria Sprint 2 completa para calibração de buffer e exposição."),
        ("fala", "A decisão: transformar o ESP32 em sensor IoT de ambientação — temperatura, umidade do ar, umidade do solo, publicados via MQTT. O smartphone assume o papel de câmera inteligente, com o mesmo modelo INT8 embarcado via tflite_flutter."),
        ("enfase", "ceres_mobilenetv2_int8.tflite · 638 KB · tflite_flutter 0.12.1 · mesmo arquivo do ESP32-S3 · inferência offline ~200–400 ms."),
        ("fala", "Essa não foi uma limitação — foi uma decisão de engenharia. O sistema ficou mais flexível e mais acessível ao produtor."),
        ("transicao", "Vamos ver o sistema funcionando."),
    ]),
    (19, "O Sistema em Funcionamento", "22:30–23:30", [
        ("fala", "App Flutter: tela IoT mostrando 29,5 °C, 49% umidade do ar, 34% umidade do solo, status ONLINE."),
        ("fala", "Hardware real: ESP32-S3 com DHT22 e sensor capacitivo de solo funcionando."),
        ("fala", "Pipeline completo: ESP32 publica via MQTT QoS 1 → HiveMQ Cloud → Django persiste com timestamp e GPS → Flutter sincroniza offline/online com Drift SQLite."),
        ("transicao", "Vou mostrar o vídeo demonstrativo."),
    ]),
    (20, "Demonstração", "23:30–25:30", [
        ("fala", "Vídeo a 1,5× — dura cerca de 1 minuto. Mostra: captura de folha pela câmera do app, diagnóstico nos três caminhos, publicação MQTT do ESP32, histórico com GPS no mapa."),
        ("alerta", "Se o vídeo não abrir: abra demo_ceres_1.5x.mp4 diretamente no player."),
        ("transicao", "Conclusão."),
    ]),
    (21, "Conclusão", "25:30–27:30", [
        ("enfase", "Manchete: TinyML agrícola funciona — o gargalo é o dado, não o hardware."),
        ("ok", "Card 1 — Viabilidade: MobileNetV2 INT8 roda no ESP32-S3 em 638 KB e 692 ms. Calibração INT8 reduziu a queda de quantização de 30,5 pp para 2,37 pp. Pipeline completo: ESP32-S3, Android, Django — integrados."),
        ("alerta", "Card 2 — Gap lab-campo: 95,76% em laboratório, 18–30% em campo. Aug. sintética falhou. Fine-tuning real: +10 pp. Focal Loss: +16 pp. Gap persiste — o método está identificado, o dado ainda falta."),
        ("alerta", "Card 3 — O gargalo real: não é o hardware — é o dado. Não existe dataset brasileiro de campo com volume e diversidade suficientes para generalização real. Esse é o próximo passo da pesquisa."),
        ("transicao", "Trabalhos futuros."),
    ]),
    (22, "Trabalhos Futuros", "27:30–29:00", [
        ("fala", "Quatro próximos passos: dataset de campo brasileiro com produtores locais — é o fator que mais limita a generalização. Integração da câmera OV5640, fechando o ciclo embarcado autônomo. Validação com produtores de Sorriso-MT. Expansão para outras culturas."),
        ("transicao", "Para encerrar."),
    ]),
    (23, "Obrigado / Perguntas", "29:00–30:00", [
        ("fala", "O Ceres Diagnóstico demonstra que TinyML embarcado é viável para diagnóstico agrícola de baixo custo. O gap campo-laboratório é o principal desafio aberto — e o caminho para resolvê-lo está identificado: dados reais de campo."),
        ("enfase", "Código e modelos: github.com/Namem/extensao2"),
        ("fala", "Obrigado. Fico à disposição para perguntas."),
    ]),
]

story = []

# Capa do roteiro
capa = Table(
    [[Paragraph("ROTEIRO DE APRESENTAÇÃO", TituloDoc)],
     [Paragraph("Ceres Diagnóstico — Defesa de Artigo PSI", SubtituloDoc)],
     [Paragraph("Namem Rachid Jaudy Neto · IFMT Cuiabá · Junho 2026", SubtituloDoc)]],
    colWidths=[16.5*cm]
)
capa.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), VE),
    ("LEFTPADDING",  (0,0), (-1,-1), 18),
    ("RIGHTPADDING", (0,0), (-1,-1), 18),
    ("TOPPADDING",   (0,0), (0,0),   14),
    ("BOTTOMPADDING",(0,-1),(-1,-1), 14),
    ("ROUNDEDCORNERS",(0,0),(-1,-1), [6,6,6,6]),
]))
story.append(capa)
story.append(Spacer(1, 0.3*cm))

info_data = [
    ["Duração total", "30 minutos (mais 10 min Q&A)"],
    ["Slides", "23 slides"],
    ["Ritmo médio", "~1 min 18 s / slide"],
    ["Vídeo", "demo_ceres_1.5x.mp4 (slide 20)"],
]
info_t = Table(info_data, colWidths=[4.0*cm, 12.5*cm])
info_t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (0,-1), CI),
    ("FONTNAME",     (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0), (-1,-1), 9.5),
    ("TEXTCOLOR",    (0,0), (0,-1), VE),
    ("TEXTCOLOR",    (1,0), (1,-1), GT),
    ("GRID",         (0,0), (-1,-1), 0.5, HexColor("#D1D5DB")),
    ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING",   (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
]))
story.append(info_t)
story.append(Spacer(1, 0.35*cm))

legenda_data = [
    ["▸ Fala normal", "★ Ênfase / ponto-chave",
     "⚠ Alerta / limitação", "✓ Resultado positivo",
     "→ Transição"],
]
leg_t = Table(legenda_data, colWidths=[3.3*cm, 3.8*cm, 3.8*cm, 3.0*cm, 2.6*cm])
leg_t.setStyle(TableStyle([
    ("FONTSIZE",     (0,0), (-1,-1), 8),
    ("TEXTCOLOR",    (0,0), (-1,-1), HexColor("#6B7280")),
    ("BACKGROUND",   (0,0), (-1,-1), LGREY),
    ("LEFTPADDING",  (0,0), (-1,-1), 6),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 4),
]))
story.append(leg_t)
story.append(Spacer(1, 0.2*cm))
story.append(HRFlowable(width="100%", thickness=1, color=VC, spaceBefore=2, spaceAfter=6))

for (num, titulo, tempo, falas) in slides:
    for el in slide_bloco(num, titulo, tempo, falas):
        story.append(el)

# Perguntas frequentes
story.append(Spacer(1, 0.5*cm))
faq_header = Table(
    [[Paragraph("PERGUNTAS FREQUENTES (Q&A)", sty("FaqHdr", fontSize=13, textColor=white,
       leading=18, fontName="Helvetica-Bold"))]],
    colWidths=[16.5*cm]
)
faq_header.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), VM),
    ("LEFTPADDING",  (0,0), (-1,-1), 12),
    ("TOPPADDING",   (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ("ROUNDEDCORNERS",(0,0),(-1,-1), [4,4,4,4]),
]))
story.append(faq_header)
story.append(Spacer(1, 0.2*cm))

faqs = [
    ("Por que não usar YOLO?",
     "YOLO é um detector de objetos — retorna bounding boxes, não classes de classificação. "
     "Incompatível com nossa tarefa de classificar a folha inteira. Além disso, o menor YOLO "
     "ocupa ~6 MB, 10× maior que nosso modelo de 638 KB."),
    ("Por que MobileNetV2 e não ResNet ou EfficientNet?",
     "MobileNetV2 foi projetado para dispositivos móveis e MCUs: depthwise separable convolutions "
     "reduzem FLOPs em ~8–9×. ResNet50 tem ~25 MB de parâmetros. EfficientNet-Lite requer "
     "arenas maiores e não havia suporte estável para TFLite Micro INT8 na época dos experimentos."),
    ("20–30% em campo é aceitável?",
     "É um resultado honesto para um primeiro ciclo de pesquisa. A literatura mostra queda similar. "
     "O caminho foi identificado: fine-tuning com dados reais (Exp D/E). O próximo passo é coletar "
     "imagens no campo com produtores de Sorriso-MT."),
    ("Por que a câmera OV5640 não foi integrada neste ciclo?",
     "Integração da câmera requer calibração de buffer de captura, correção de exposição e latência "
     "de leitura — trabalho de Sprint 2. A decisão foi isolar a latência da CNN pura (692 ms) "
     "carregando imagens como array C. O smartphone serve como sensor alternativo no caminho ②."),
    ("692 ms é rápido o suficiente para uso em campo?",
     "Sim. O produtor leva 2–5 segundos para posicionar a folha adequadamente. 692 ms é imperceptível. "
     "A meta de 300 ms é para futura otimização com OV5640 pipeline completo, não um bloqueador atual."),
    ("Como garantir privacidade dos dados do produtor?",
     "No caminho Edge (ESP32-S3) e no caminho Mobile (Android), a imagem nunca sai do dispositivo — "
     "apenas o resultado da classificação em texto é transmitido. No caminho Cloud, a imagem trafega "
     "via HTTPS para o servidor Django. O produtor escolhe o caminho."),
    ("O sistema funciona sem internet?",
     "Os caminhos Edge e Mobile funcionam 100% offline. O histórico é sincronizado quando o usuário reconecta "
     "via Drift SQLite. O caminho Cloud requer conectividade."),
    ("Como o sistema será validado com produtores reais?",
     "Sprint 3 prevê coleta de imagens com pequenos produtores de Sorriso-MT, validação de usabilidade "
     "e teste de campo. Esse dataset brasileiro de campo é o principal trabalho futuro."),
]

for q, a in faqs:
    story.append(Paragraph(
        f"<b>Q: {q}</b>",
        sty("PergH", fontSize=10, textColor=VE, leading=14, spaceAfter=1, leftIndent=0, fontName="Helvetica-Bold")
    ))
    story.append(Paragraph(
        f"R: {a}",
        sty("PergR", fontSize=9.5, textColor=GT, leading=14, spaceAfter=8, leftIndent=10)
    ))
    story.append(HRFlowable(width="100%", thickness=0.3, color=HexColor("#E5E7EB"), spaceAfter=2, spaceBefore=0))

doc.build(story)
print(f"OK Roteiro gerado: {OUT}")
