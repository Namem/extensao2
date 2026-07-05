from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT

OUT = "C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/extensao/slides/roteiro_ceres_sprint_mvp.pdf"

VERDE  = HexColor('#1A3A1A')
DOURADO = HexColor('#C8860A')
CREME  = HexColor('#F5F0E8')
CINZA  = HexColor('#444444')
MUTED  = HexColor('#777777')
AZUL   = HexColor('#0C447C')
AZUL_BG = HexColor('#E8F1FB')

doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

def sty(name, **kw):
    return ParagraphStyle(name, **kw)

S = {
    'h1':    sty('h1', fontSize=20, fontName='Helvetica-Bold', textColor=VERDE, spaceAfter=4),
    'sub':   sty('sub', fontSize=10, fontName='Helvetica', textColor=MUTED, spaceAfter=14),
    'slabel':sty('sl', fontSize=8, fontName='Helvetica-Bold', textColor=DOURADO, spaceAfter=0),
    'stitle':sty('st', fontSize=13, fontName='Helvetica-Bold', textColor=VERDE, spaceAfter=6),
    'flabel':sty('fl', fontSize=8, fontName='Helvetica-Bold', textColor=MUTED, spaceAfter=2, spaceBefore=4),
    'fala':  sty('fa', fontSize=10, fontName='Helvetica', textColor=CINZA, leading=15, spaceAfter=4),
    'dlabel':sty('dl', fontSize=8, fontName='Helvetica-Bold', textColor=AZUL, spaceAfter=2, spaceBefore=4),
    'dica':  sty('di', fontSize=9, fontName='Helvetica', textColor=AZUL, leading=13, spaceAfter=6),
    'tempo': sty('te', fontSize=9, fontName='Helvetica-Bold', textColor=DOURADO),
}

slides = [
    ('01','CAPA','Ceres Diagnostico — Sprint Review','30 seg',
     'Boa tarde. Sou Namem Rachid, aluno de Engenharia da Computacao do IFMT Cuiaba. Vou apresentar o Ceres Diagnostico — sistema embarcado de deteccao precoce de doencas no tomateiro. Em vinte minutos: o problema, o que construimos, onde chegamos e onde erramos.',
     'Fala curta. Postura confiante. Deixe o slide dark falar por si.'),
    ('02','ROADMAP','De onde viemos e para onde vamos','1 min',
     'Quatro sprints concluidos — um ano de desenvolvimento. Sprint 0: motor de diagnostico por perguntas. Sprint 1: treinamento da IA e pipeline MQTT. Sprint 2: IA embarcada no ESP32-S3, validada em 692ms. Sprint MVP — estamos aqui — app completo e hardware real. Proximos passos: camera embarcada e dataset brasileiro.',
     'Aponte para os marcos no roadmap. Pause em "estamos aqui".'),
    ('03','O PROBLEMA','O agricultor perde antes de saber o que perdeu','1 min',
     'Um tomateiro doente nao grita. Ele murcha em silencio enquanto a doenca avanca. A requeima pode destruir 100% da lavoura sem tratamento. Diagnostico depende de agronomo inacessivel ao pequeno produtor. Existem 10 doencas dificeis de separar a olho nu. E a internet que permitiria diagnostico digital nao chega na lavoura.',
     'Fale devagar nos tres pilares: acesso ao especialista, volume de doencas e infraestrutura.'),
    ('04','OBJETIVO INICIAL','Tres pilares — um sistema integrado','45 seg',
     'O objetivo inicial era uma solucao em tres camadas. Hardware: ESP32-S3 com camera OV5640, IA embarcada sem internet. App: Flutter com TFLite local sincronizado com a nuvem. Backend: Django REST no Railway com historico e alertas MQTT. Esse era o plano — em breve vou mostrar o que mudou.',
     'Slide rapido. Plante a semente dos pivos sem revelar ainda.'),
    ('05','DIAGNOSTICO','Foto a folha. Saiba o que esta acontecendo.','1 min',
     'O produtor fotografa a folha, a IA classifica em menos de 2 segundos, e o resultado aparece com doenca, confianca, top-3 e recomendacao de tratamento. Com internet: resultado sincroniza com Railway, historico na nuvem, mapa em tempo real. Sem internet: IA roda no celular em menos de 1 segundo, nenhum dado sai do dispositivo. 98,43% de acuracia. 638KB. Funciona em qualquer lavoura.',
     'Este e o slide do PRODUTO — fale como se estivesse vendendo. Cloud e offline sao diferenciais claros.'),
    ('06','10 CLASSES','9 doencas + saudavel','45 seg',
     'O modelo classifica 10 categorias: requeima, septoriose, pinta preta, mancha alvo, mofo foliar, vira-cabeca, mosaico, acaro de bronzeamento, mancha bacteriana e saudavel. Dataset PlantVillage — 18.160 imagens, CC BY 4.0. Aqui fica evidente por que o gap existe: todas as fotos tem fundo cinza uniforme, totalmente diferente de uma lavoura real.',
     'Slide visual. Deixe as fotos falarem. Conecte ao proximo slide: "o modelo aprendeu essas imagens de lab".'),
    ('07','O MODELO','Unico modelo que cabe no chip','1,5 min',
     'Para rodar IA num microcontrolador de 80 reais, a escolha e critica. ResNet-50: 100MB — nao cabe no ESP32-S3. YOLO: detecta objetos, nao classifica folha — ferramenta errada. EfficientNet: 20MB, latencia acima de 2s em MCU — inviavel. MobileNetV2 INT8 calibrado: 638KB, 692ms, 98,43%. Unico que fecha todas as restricoes ao mesmo tempo.',
     'Aponte para a linha dourada na tabela. Diga: "e o unico que fecha TODAS as restricoes simultaneamente".'),
    ('08','A DESCOBERTA','95,76% no lab -> 20,77% em campo real','2 min',
     '95,76% de acuracia no PlantVillage — imagens de laboratorio, fundo cinza. Testamos com o PlantDoc, 1.353 imagens de campo real: caiu para 20,77%. Queda de 75 pontos. A causa: o modelo aprendeu o fundo cinza como feature, nao a doenca. Fenomeno em 42 trabalhos — Mohanty 2016: 99% lab e 31% campo. Singh 2020: trocar o fundo recupera 40pp. Decisao: documentar honestamente. Proximo passo: dataset com condicoes brasileiras.',
     'Slide mais importante. Fale com calma. "Documentamos honestamente" mostra maturidade — nao e fracasso, e resultado.'),
    ('09','EXPERIMENTOS','5 experimentos para fechar o gap','2 min',
     'Exp A: Edge Impulse sem calibracao — 62%, descartado. Exp B: TF local duas fases + INT8 calibrado — 98,43% lab, 20,77% campo, modelo base. Exp C: 177k sinteses rembg — 20,24%, pior que B, descartado. Exp D: fine-tuning com 677 imagens reais do PlantDoc — 30,43%, +10pp, melhor resultado. Exp E: Focal Loss + dataset India — 27,65%, abaixo do D, descartado. Conclusao: dado real supera dado sintetico.',
     'Percorra linha por linha. Pause no Exp D. Encerre: "dados reais > sinteticos — isso guia os proximos passos".'),
    ('10','RESULTADOS','Resultados do Sprint MVP — em numeros','1 min',
     '98,43% de acuracia (18-30% campo documentado). 692ms de latencia no ESP32-S3. 638KB de modelo INT8 no dispositivo. 10/10 acertos no benchmark offline. 88.949 imagens de treino com augmentation x6. 184 eventos IoT registrados durante os testes.',
     'Slide de impacto — deixe os numeros respirarem. Escolha 2-3 e conecte ao problema inicial.'),
    ('11','PIVOS','3 pivos que definiram o MVP','1,5 min',
     'Pivo 1 ESP32-S3: camera OV5640 nao chegou no prazo por custo. ESP32-S3 ficou como prova de conceito — 692ms validados. App mobile virou produto principal end-to-end. Pivo 2 Experimentos: Exp C com 177k sinteses falhou — pior que B. Dado real vence sintetico. Pivo 3 Gap lab-campo: documentamos o fenomeno honestamente. Proximo: dataset proprio de MT.',
     'Nao se desculpe pelos pivos. Explique a logica de cada decisao — soa como mercado de trabalho real.'),
    ('12','O QUE CONSTRUIMOS','Sprint 1 vs Sprint MVP','1 min',
     'Sprint 1 tinha: motor por perguntas, API sem camera, modelo na nuvem sem offline. O Sprint MVP entregou: foto com IA em menos de 2 segundos, 98,43% de acuracia, offline completo no celular, app com mapa, historico e enciclopedia, e ESP32-S3 monitorando ambiente em tempo real via MQTT.',
     'Leia as colunas lado a lado. Finalize: "entregamos mais do que o planejado".'),
    ('13','APP CERES','Flutter completo — 4 telas','1,5 min',
     'Tela 1 Diagnostico: TFLite local, resultado offline em menos de 1 segundo. Tela 2 Historico IoT: historico sincronizado com sensores ESP32, temperatura e umidade em tempo real. Tela 3 Enciclopedia: fichas das 10 doencas. Tela 4 Mapa: geolocalizacao de ocorrencias. Backend Django REST em producao no Railway, JWT, SQLite local com Drift.',
     '"Em producao" e a palavra-chave — nao e prototipo. Railway + offline mostra que funciona em condicoes reais.'),
    ('14','HARDWARE IoT','ESP32-S3 — sentinela da lavoura','1,5 min',
     'Esse e o hardware real do projeto — ESP32 com DHT22 no vaso e sensor capacitivo enterrado no solo. A cada 30 segundos mede temperatura, umidade do ar e umidade do solo, e envia tudo via MQTT para a nuvem. O app exibe em tempo real. Latencia do sensor ate o app: menos de 2 segundos. Custo total do no: ~R$80.',
     'Aponte para a foto no slide — o setup real esta ali. Se tiver o ESP32 fisico na mao, melhor ainda.'),
    ('15','CONCLUSAO','TinyML agricola funciona. O gargalo e o dado.','1 min',
     'Duas conclusoes. Viabilidade tecnica: MobileNetV2 INT8, 638KB, 692ms, hardware de ~R$80. Roda no ESP32-S3. O gap de 20-30% em campo nao e fracasso — e fenomeno documentado. Mohanty 2016 tinha 31%, Singh 2020 mostrou que trocar o fundo recupera 40pp. O gargalo nao e o algoritmo nem o hardware. E o dado. Dataset brasileiro de tomateiro e o proximo passo.',
     'Diga as duas conclusoes devagar — uma pause entre elas. Ultima frase: "o gargalo e o dado, nao o hardware" — deixe no ar.'),
    ('16','DEMO','Demonstracao ao vivo','3 min',
     'Tres cenarios. Cloud: foto de requeima, resultado 94% em menos de 2 segundos sincronizado com Railway. Offline: foto de folha saudavel, classificacao em menos de 1 segundo sem nenhuma conexao. Mapa: 30 ou mais pins de ocorrencias registrados nos testes em MT. [Abrir app ao vivo] — se algo falhar, gravacao de backup disponivel.',
     'Prepare antes: app aberto, WiFi ligado e modo aviao prontos para trocar rapidamente. Mencione o backup antes de comecar — mostra preparo. 3 minutos passam rapido.'),
    ('17','PROXIMOS PASSOS','O caminho ate o campo real','1 min',
     'Cinco passos. Um: camera OV5640 no ESP32-S3 — diagnostico autonomo sem celular na lavoura. Dois: dataset brasileiro de tomate — primeiras imagens reais de MT, com condicoes locais. Tres: retreino com dados locais para reduzir o gap de laboratorio. Quatro: validacao com tomaticultores de Mato Grosso em campo real. Cinco: publicar em conferencia de IA agricola. Codigo em github.com/Namem/extensao2, API em ceres.up.railway.app. Obrigado.',
     '"Podem acessar agora" — mostra que e real e esta no ar. Abra para perguntas.'),
]

story = []
story.append(Paragraph('Ceres Diagnostico - Sprint MVP', S['h1']))
story.append(Paragraph('Roteiro de Apresentacao  |  17 slides  |  20 minutos', S['sub']))
story.append(HRFlowable(width='100%', thickness=1, color=VERDE, spaceAfter=14))

for num, label, titulo, tempo, fala, dica in slides:
    # Linha de cabecalho do slide
    hdr = Table([[
        Paragraph(f'SLIDE {num}  -  {label}', S['slabel']),
        Paragraph(tempo, S['tempo'])
    ]], colWidths=[13*cm, 3*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), CREME),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('ALIGN', (1,0),(1,0), 'RIGHT'),
    ]))
    story.append(hdr)

    inner = [
        Paragraph(titulo, S['stitle']),
        Paragraph('FALA', S['flabel']),
        Paragraph(fala, S['fala']),
        Paragraph('DICA', S['dlabel']),
        Paragraph('-> ' + dica, S['dica']),
    ]
    body = Table([[inner]], colWidths=[16*cm])
    body.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), white),
        ('BOX', (0,0),(-1,-1), 0.5, HexColor('#CCCCCC')),
        ('LEFTPADDING', (0,0),(-1,-1), 10),
        ('RIGHTPADDING', (0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
    ]))
    story.append(body)
    story.append(Spacer(1, 8))

doc.build(story)
print('OK:', OUT)
