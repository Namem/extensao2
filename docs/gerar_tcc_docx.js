const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  PageNumber, PageBreak, LevelFormat, ShadingType, TableOfContents
} = require("docx");

// ABNT: margens 3cm sup/esq, 2cm inf/dir (1cm = 567 DXA)
const MARGIN_TOP = 1701;    // 3cm
const MARGIN_LEFT = 1701;   // 3cm
const MARGIN_BOTTOM = 1134; // 2cm
const MARGIN_RIGHT = 1134;  // 2cm
const PAGE_WIDTH = 11906;   // A4
const PAGE_HEIGHT = 16838;  // A4
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT; // 9071 DXA

const FONT = "Times New Roman";
const SIZE = 24; // 12pt

// Helper functions
function p(text, opts = {}) {
  const runOpts = { font: FONT, size: opts.size || SIZE };
  if (opts.bold) runOpts.bold = true;
  if (opts.italics) runOpts.italics = true;
  const parOpts = { spacing: { line: 360 } }; // 1.5 line spacing
  if (opts.alignment) parOpts.alignment = opts.alignment;
  if (opts.heading) parOpts.heading = opts.heading;
  if (opts.spacing) parOpts.spacing = { ...parOpts.spacing, ...opts.spacing };
  if (opts.indent) parOpts.indent = opts.indent;
  parOpts.children = [new TextRun({ ...runOpts, text })];
  return new Paragraph(parOpts);
}

function emptyLine() {
  return new Paragraph({ spacing: { line: 360 }, children: [] });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 480, after: 240, line: 360 },
    children: [new TextRun({ font: FONT, size: 28, bold: true, text: text.toUpperCase() })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 360, after: 180, line: 360 },
    children: [new TextRun({ font: FONT, size: 26, bold: true, text })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 240, after: 120, line: 360 },
    children: [new TextRun({ font: FONT, size: 24, bold: true, text })]
  });
}

function tableFromData(headers, rows) {
  const colCount = headers.length;
  const colWidth = Math.floor(CONTENT_WIDTH / colCount);
  const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
  const borders = { top: border, bottom: border, left: border, right: border };

  const headerRow = new TableRow({
    children: headers.map(h => new TableCell({
      borders,
      width: { size: colWidth, type: WidthType.DXA },
      shading: { fill: "D9E2F3", type: ShadingType.CLEAR },
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({
        spacing: { line: 276 },
        children: [new TextRun({ font: FONT, size: 20, bold: true, text: h })]
      })]
    }))
  });

  const dataRows = rows.map(row => new TableRow({
    children: row.map(cell => new TableCell({
      borders,
      width: { size: colWidth, type: WidthType.DXA },
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({
        spacing: { line: 276 },
        children: [new TextRun({ font: FONT, size: 20, text: String(cell) })]
      })]
    }))
  }));

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: Array(colCount).fill(colWidth),
    rows: [headerRow, ...dataRows]
  });
}

// ============= BUILD DOCUMENT =============

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: FONT, size: SIZE } }
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: FONT },
        paragraph: { spacing: { before: 480, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: FONT },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: FONT },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 } },
    ]
  },
  sections: [
    // ============= CAPA =============
    {
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
          margin: { top: MARGIN_TOP, bottom: MARGIN_BOTTOM, left: MARGIN_LEFT, right: MARGIN_RIGHT }
        }
      },
      children: [
        emptyLine(), emptyLine(), emptyLine(),
        p("INSTITUTO FEDERAL DE MATO GROSSO", { alignment: AlignmentType.CENTER, bold: true, size: 28 }),
        p("CAMPUS CUIABÁ", { alignment: AlignmentType.CENTER, bold: true, size: 28 }),
        p("ENGENHARIA DA COMPUTAÇÃO", { alignment: AlignmentType.CENTER, bold: true, size: 26 }),
        emptyLine(), emptyLine(), emptyLine(), emptyLine(), emptyLine(),
        p("NAMEM RACHID JAUDY NETO", { alignment: AlignmentType.CENTER, bold: true, size: 28 }),
        emptyLine(), emptyLine(), emptyLine(), emptyLine(),
        p("CERES DIAGNÓSTICO: SISTEMA EMBARCADO DE DETECÇÃO PRECOCE DE DOENÇAS NO TOMATEIRO COM TINYML E IoT", { alignment: AlignmentType.CENTER, bold: true, size: 32 }),
        emptyLine(), emptyLine(), emptyLine(), emptyLine(), emptyLine(),
        emptyLine(), emptyLine(), emptyLine(), emptyLine(), emptyLine(),
        emptyLine(), emptyLine(), emptyLine(),
        p("CUIABÁ — MT", { alignment: AlignmentType.CENTER, size: 24 }),
        p("2026", { alignment: AlignmentType.CENTER, size: 24 }),
      ]
    },
    // ============= RESUMO =============
    {
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
          margin: { top: MARGIN_TOP, bottom: MARGIN_BOTTOM, left: MARGIN_LEFT, right: MARGIN_RIGHT }
        }
      },
      headers: {
        default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ font: FONT, size: 20, children: [PageNumber.CURRENT] })] })] })
      },
      footers: { default: new Footer({ children: [] }) },
      children: [
        heading1("RESUMO"),
        p("O tomateiro (Solanum lycopersicum) é uma das culturas de maior importância econômica no Brasil, com produção anual superior a 4 milhões de toneladas. Doenças foliares como requeima (Phytophthora infestans), septoriose (Septoria lycopersici) e mancha-bacteriana (Xanthomonas spp.) podem causar perdas de até 100% da safra quando não detectadas precocemente."),
        emptyLine(),
        p("Este trabalho propõe o Ceres Diagnóstico, um sistema embarcado de baixo custo para detecção precoce de doenças em folhas de tomateiro. O sistema integra um microcontrolador ESP32-S3 executando modelo MobileNetV2 quantizado (INT8) via TensorFlow Lite Micro diretamente no dispositivo (TinyML), sem necessidade de conexão com servidor de nuvem para inferência. Os resultados são transmitidos via protocolo MQTT para um backend Django REST, acessível por aplicativo Flutter."),
        emptyLine(),
        p("O modelo foi treinado com o dataset PlantVillage (Hughes & Salathé, 2015), contendo 18.160 imagens de folhas de tomate em 10 classes, expandido para 88.949 imagens via augmentation offline. O modelo final (Exp E — Focal Loss) atingiu 98,43% de acurácia no test set com 638 KB INT8. A validação em hardware real (ESP32-S3 N16R8, 240 MHz) mediu latência de 692 ms por inferência com 10/10 imagens corretas. O experimento Edge vs Cloud demonstrou a viabilidade do diagnóstico embarcado sem dependência de nuvem."),
        emptyLine(),
        p("Palavras-chave: TinyML, ESP32-S3, detecção de doenças em plantas, MobileNetV2, MQTT, Django REST, Flutter, agricultura de precisão.", { bold: true }),

        // ABSTRACT
        new Paragraph({ children: [new PageBreak()] }),
        heading1("ABSTRACT"),
        p("Tomato (Solanum lycopersicum) is one of the most economically important crops in Brazil. This work proposes Ceres Diagnóstico, a low-cost embedded system for early detection of tomato leaf diseases. The system integrates an ESP32-S3 microcontroller running a quantized MobileNetV2 model (INT8) via TensorFlow Lite Micro directly on-device (TinyML). The final model (Exp E — Focal Loss) achieved 98.43% test accuracy with a 638 KB INT8 model. On-device inference measured 692 ms latency with 10/10 correct predictions. The Edge vs Cloud experiment demonstrated the viability of embedded diagnosis without cloud dependency."),
        emptyLine(),
        p("Keywords: TinyML, ESP32-S3, plant disease detection, MobileNetV2, MQTT, Django REST, Flutter, precision agriculture.", { bold: true }),

        // SUMARIO
        new Paragraph({ children: [new PageBreak()] }),
        heading1("SUMÁRIO"),
        new TableOfContents("Sumário", { hyperlink: true, headingStyleRange: "1-3" }),

        // 1. INTRODUCAO
        new Paragraph({ children: [new PageBreak()] }),
        heading1("1. INTRODUÇÃO"),
        heading2("1.1 Contextualização"),
        p("O Brasil é o nono maior produtor mundial de tomate, com produção de aproximadamente 4,4 milhões de toneladas em 2023 (FAO, 2024). O estado de Mato Grosso apresenta expansão crescente da tomaticultura, impulsionada pela fronteira agrícola do Cerrado. Contudo, o manejo fitossanitário ainda é majoritariamente reativo: o produtor detecta a doença visualmente após o aparecimento de sintomas severos, quando a perda já é significativa."),
        emptyLine(),
        p("A detecção precoce de doenças foliares é fundamental para reduzir o uso de agrotóxicos, diminuir perdas e aumentar a rentabilidade da cultura. O paradigma TinyML — execução de modelos de aprendizado de máquina diretamente em microcontroladores de baixo custo — surge como alternativa viável para este contexto."),

        heading2("1.2 Problema"),
        p("Como detectar precocemente doenças foliares no tomateiro de forma automatizada, de baixo custo e funcionando offline, acessível ao pequeno produtor rural do Centro-Oeste brasileiro?"),

        heading2("1.3 Hipótese"),
        p("Um sistema embarcado baseado em ESP32-S3 com modelo MobileNetV2 quantizado (TinyML) é capaz de classificar doenças foliares do tomateiro com acurácia superior a 85%, latência inferior a 300ms e custo de hardware inferior a R$ 200,00, viabilizando o diagnóstico em tempo real sem conectividade."),

        heading2("1.4 Objetivos"),
        p("Objetivo Geral: Desenvolver e validar um sistema embarcado de detecção precoce de doenças em folhas de tomateiro integrando TinyML, IoT e aplicativo mobile.", { bold: true }),
        emptyLine(),
        p("Objetivos Específicos:", { bold: true }),
        p("1. Preparar e aumentar o dataset PlantVillage com 10 classes de doenças do tomateiro"),
        p("2. Treinar modelo MobileNetV2 INT8 com acurácia > 85%"),
        p("3. Implantar o modelo no ESP32-S3 com latência < 300ms"),
        p("4. Desenvolver backend Django REST com persistência de eventos via MQTT"),
        p("5. Desenvolver aplicativo Flutter com funcionamento offline"),
        p("6. Comparar experimentalmente inferência edge vs cloud"),

        // 2. REFERENCIAL TEORICO
        new Paragraph({ children: [new PageBreak()] }),
        heading1("2. REFERENCIAL TEÓRICO"),
        heading2("2.1 Doenças do Tomateiro e Impacto Econômico"),
        p("O tomateiro é acometido por diversas doenças foliares de origem fúngica, bacteriana e viral. As 10 classes monitoradas pelo Ceres correspondem às doenças foliares identificáveis por imagem, com base no mapeamento da Embrapa Hortaliças."),
        emptyLine(),
        tableFromData(
          ["Código", "Doença", "Agente", "Perda"],
          [
            ["D01", "Requeima", "P. infestans", "Até 100%"],
            ["D02", "Septoriose", "S. lycopersici", "20–50%"],
            ["D03", "Pinta-Preta", "A. solani", "30–70%"],
            ["D03b", "Mancha-Alvo", "C. cassiicola", "20–40%"],
            ["D05", "Mofo-Foliar", "P. fulva", "20–30%"],
            ["D06", "Vira-Cabeça", "TSWV", "30–80%"],
            ["D06b", "Mosaico", "ToMV", "10–30%"],
            ["D07", "Ácaro-Bronzeamento", "A. lycopersici", "20–40%"],
            ["D09", "Mancha-Bacteriana", "Xanthomonas", "15–35%"],
            ["saudavel", "Saudável", "—", "—"],
          ]
        ),

        heading2("2.2 Visão Computacional para Diagnóstico Fitossanitário"),
        p("O uso de CNNs para classificação de doenças em plantas foi popularizado por Mohanty et al. (2016), com acurácia de 99,35% em condições laboratoriais. Entretanto, Singh et al. (2020) mostraram queda para ~30% em campo real sem adaptação de domínio, evidenciando o gap laboratório-campo."),
        emptyLine(),
        p("MobileNetV2 (Sandler et al., 2018) introduziu blocos inverted residual com linear bottleneck, reduzindo parâmetros de 138M (VGG16) para ~4,2M sem perda crítica de acurácia, viabilizando execução em MCUs."),

        heading2("2.3 TinyML e Inferência na Borda"),
        p("TinyML refere-se à execução de modelos de machine learning em microcontroladores com restrições severas de memória (< 1MB RAM) e energia (< 1mW). A quantização INT8 é a técnica central que viabiliza TinyML: converte pesos FP32 para INT8, reduzindo o modelo ~4x (Warden & Situnayake, 2019)."),

        heading2("2.4 Protocolos IoT para Agricultura de Precisão"),
        p("O protocolo MQTT (OASIS, 2019), com header mínimo de 2 bytes e modelo publish/subscribe, é o protocolo dominante em sistemas IoT agrícolas. O broker HiveMQ Cloud fornece conectividade TLS segura entre ESP32 e backend Django em produção."),

        heading2("2.5 Trabalhos Relacionados"),
        tableFromData(
          ["Trabalho", "Hardware", "Modelo", "Acurácia"],
          [
            ["LeafSense (ACM 2024)", "ESP32-CAM", "TinyML CNN", "92%"],
            ["Springer IoT (2025)", "ESP32", "TinyML", "n/d"],
            ["Ceres (este trabalho)", "ESP32-S3 N16R8", "MobileNetV2 INT8 638KB", "98,43% lab"],
          ]
        ),

        // 3. METODOLOGIA
        new Paragraph({ children: [new PageBreak()] }),
        heading1("3. METODOLOGIA"),
        heading2("3.1 Arquitetura Geral do Sistema"),
        p("ESP32-S3 (TFLite Micro) → MQTT TLS → HiveMQ Cloud → Railway Django → PostgreSQL → Flutter App"),
        emptyLine(),
        p("O ciclo de operação: (1) ESP32-S3 executa inferência local no modelo INT8; (2) publica resultado via MQTT; (3) Django persiste no PostgreSQL; (4) Flutter consulta API REST."),

        heading2("3.2 Dataset e Pré-processamento"),
        p("Dataset primário: PlantVillage (Hughes & Salathé, 2015) — 18.160 imagens, 10 classes, CC BY 4.0. Split estratificado (seed=42): 70% train / 15% val / 15% test. Augmentation offline: flip H/V, rotação ±15°, brilho ±20% → 88.949 imagens de treino."),

        heading2("3.3 Treinamento do Modelo"),
        p("Arquitetura: MobileNetV2 96×96 alpha=0.35. Cinco experimentos conduzidos (A–E). Modelo final: Exp E (Focal Loss, γ=2, label_smoothing=0.1, backbone completo LR=1e-5) — 98,43% test acc, 638 KB INT8."),
        emptyLine(),
        tableFromData(
          ["Exp", "Estratégia", "PlantVillage test", "Campo real"],
          [
            ["A", "Edge Impulse (INT8 sem calibração)", "62,0%", "—"],
            ["B", "TF local 2 fases + calibração", "98,13%", "20,77%"],
            ["C", "Background augmentation sintética", "96,20%", "20,24%"],
            ["D", "Fine-tuning PlantDoc real", "97,55%", "30,43%"],
            ["E", "Focal Loss + aug agressiva", "98,43%", "27,65%"],
          ]
        ),

        heading2("3.4 Firmware ESP32-S3"),
        p("Plataforma PlatformIO + Arduino. Tensor Arena: 512 KB (PSRAM). Biblioteca: Chirale_TensorFLowLite@2.0.0. Normalização INT8: uint8 - 128. Latência medida: 692 ms. Sensores: DHT22 (GPIO 4) + capacitivo solo (GPIO 5, ADC). Comunicação: WiFi → MQTT TLS → HiveMQ Cloud."),

        heading2("3.5 Backend Django REST"),
        p("Framework: Django 6.0.4 + DRF 3.17.1. Banco: PostgreSQL (Railway). Autenticação: SimpleJWT. Deploy: Railway com Dockerfile. MQTT: mqtt_listener via WebSocket+TLS (HiveMQ). Endpoints: /inferir/, /historico/, /sensor/, /me/, /register/."),

        heading2("3.6 Aplicativo Flutter"),
        p("12 telas implementadas: Splash, Login, Cadastro, Câmera (diagnóstico), Histórico IoT, Histórico Local, Mapa, Enciclopédia, Perfil, Alertas, Agrônomos, Seja Parceiro. Persistência offline com Drift (SQLite). Design System: paleta Cerrado, fontes Newsreader + IBM Plex Sans."),

        // 4. DESENVOLVIMENTO
        new Paragraph({ children: [new PageBreak()] }),
        heading1("4. DESENVOLVIMENTO E IMPLEMENTAÇÃO"),
        heading2("4.1 Sprint 0 — Motor de Diagnóstico"),
        p("Árvore de decisão como motor inicial. Multi-tenant estruturado. JWT stateless. 5/5 testes passando."),

        heading2("4.2 Sprint 1 — MQTT + Dataset + Treino"),
        p("Dataset PlantVillage preparado (88.949 imgs treino). Exp A (Edge Impulse): 92,5% FP32, 62,0% INT8. Exp B (TF local): 98,13% INT8, 639 KB. Backend MQTT: DiagnosticoEvento + mqtt_listener + historico/. Pipeline validado: ESP32 → Mosquitto → Django → PostgreSQL."),

        heading2("4.3 Sprint 2 — ESP32-S3 + TFLite Micro"),
        p("Modelo integrado como array C. Benchmark: 10/10 corretas, 692 ms latência média, 200 KB arena PSRAM. MQTT publicado com WiFi ativo simultaneamente."),
        emptyLine(),
        tableFromData(
          ["Métrica", "Valor"],
          [
            ["Acurácia", "10/10 = 100%"],
            ["Latência média", "692 ms"],
            ["Desvio padrão", "±1 ms"],
            ["Arena PSRAM", "200 KB / 512 KB (39%)"],
            ["RAM livre", "290 KB"],
          ]
        ),

        heading2("4.4 Sprint 3 — Flutter + Experimentos"),
        p("App Flutter com 12 telas. Django containerizado e deployado no Railway. Experimento Edge vs Cloud realizado. Pipeline IoT: ESP32 → HiveMQ Cloud → Railway → PostgreSQL → Flutter."),

        // 5. RESULTADOS
        new Paragraph({ children: [new PageBreak()] }),
        heading1("5. RESULTADOS E DISCUSSÃO"),
        heading2("5.1 Experimento de Treinamento"),
        tableFromData(
          ["Métrica", "Exp A FP32", "Exp A INT8", "Exp B INT8", "Exp E INT8"],
          [
            ["Acurácia val", "92,5%", "62,0%", "97,79%", "98,43%"],
            ["Tamanho", "1.637 KB", "547 KB", "639 KB", "638 KB"],
            ["Calibração INT8", "Não", "Não", "Sim (50 batches)", "Sim"],
          ]
        ),
        emptyLine(),
        p("A quantização INT8 sem representative_dataset causou queda de 30,5 pp (Exp A). Com calibração adequada (Exp B/E), a queda foi eliminada. Focal Loss (Exp E) melhorou robustez em campo (+16 pp no Tomato-Village vs Exp D)."),

        heading2("5.2 Latência de Inferência"),
        p("Latência real medida com esp_timer_get_time() no ESP32-S3: 692 ms (±1 ms). Meta de 300 ms não atingida, porém 2x mais rápido que estimativa Edge Impulse (1.365 ms). Viável para uso agrícola: interação humana (posicionar folha) consome mais tempo que a inferência."),

        heading2("5.3 Validação em Campo Real"),
        tableFromData(
          ["Dataset", "Origem", "Imagens", "Acurácia Exp E"],
          [
            ["PlantDoc test-only", "EUA/Europa", "69", "30,43%"],
            ["Tomato-Village", "Rajasthan, Índia", "217", "27,65%"],
            ["Daffodil BD", "Bangladesh", "1.616", "18,13%"],
          ]
        ),
        emptyLine(),
        p("Gap laboratório-campo (98,43% → ~20-30%) consistente com literatura (Mohanty 2016, Singh 2020). Causa: modelo aprendeu fundo controlado como feature discriminativa."),

        heading2("5.4 Experimento Edge vs Cloud"),
        tableFromData(
          ["Métrica", "ESP32-S3 (Edge)", "Django/PC (Cloud)"],
          [
            ["Acurácia", "10/10 (100%)", "9/10 (90%)"],
            ["Latência", "692 ms", "306 ms / 2.333 ms HTTP"],
            ["Offline", "Sim", "Não"],
            ["Privacidade", "Total (local)", "Imagem transmitida"],
            ["Custo", "~R$80", "Servidor"],
          ]
        ),

        // 6. CONCLUSAO
        new Paragraph({ children: [new PageBreak()] }),
        heading1("6. CONCLUSÃO"),
        heading2("6.1 Verificação da Hipótese"),
        p("1. Acurácia > 85%: ATINGIDA — 98,43% no PlantVillage test set."),
        p("2. Latência < 300 ms: NÃO ATINGIDA — 692 ms medidos. Contudo, viável para uso agrícola e 2x mais rápido que estimativa Edge Impulse."),
        p("3. Custo < R$200: ATINGIDA — ESP32-S3 (~R$80) + sensores (~R$50) = ~R$130."),

        heading2("6.2 Contribuições"),
        p("1. Pipeline reproduzível: PlantVillage → MobileNetV2 INT8 638 KB → ESP32-S3"),
        p("2. Análise quantitativa do impacto da calibração INT8 (+36 pp)"),
        p("3. Benchmark em 3 datasets de campo real (PlantDoc, Tomato-Village, Daffodil BD)"),
        p("4. Documentação de resultado negativo: augmentation sintética ineficaz"),
        p("5. Experimento Edge vs Cloud com dados reais de latência"),
        p("6. Sistema completo: TinyML + IoT + REST + mobile — código aberto"),
        p("7. Focal Loss (Exp E) como estratégia para robustez de campo (+16 pp)"),

        heading2("6.3 Trabalhos Futuros"),
        p("1. Coleta de dataset brasileiro (Sorriso-MT) para fine-tuning local"),
        p("2. Integração câmera OV5640 para captura real"),
        p("3. Domain adaptation (DANN) sem labels de campo"),
        p("4. Federated learning para atualização sem transmitir imagens"),
        p("5. Validação com produtores em cooperativas de Sorriso-MT"),

        // 7. REFERENCIAS
        new Paragraph({ children: [new PageBreak()] }),
        heading1("7. REFERÊNCIAS"),
        p("AGRIOS, G. N. Plant Pathology. 5. ed. Elsevier Academic Press, 2005."),
        emptyLine(),
        p("BARBEDO, J. G. A. Plant disease identification from individual lesions and spots using deep learning. Biosystems Engineering, v. 180, p. 96-107, 2019."),
        emptyLine(),
        p("EMBRAPA HORTALIÇAS. Doenças do Tomateiro. Disponível em: https://www.embrapa.br/hortalicas/tomate/doencas."),
        emptyLine(),
        p("FAO. FAOSTAT — Production: Crops and livestock products. 2024."),
        emptyLine(),
        p("HOWARD, A. G. et al. MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. arXiv, 2017."),
        emptyLine(),
        p("HUGHES, D.; SALATHÉ, M. An open access repository of images on plant health. arXiv, 2015."),
        emptyLine(),
        p("JACOB, B. et al. Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference. CVPR, 2018."),
        emptyLine(),
        p("LIN, T. Y. et al. Focal Loss for Dense Object Detection. ICCV, 2017."),
        emptyLine(),
        p("MOHANTY, S. P.; HUGHES, D. P.; SALATHÉ, M. Using Deep Learning for Image-Based Plant Disease Detection. Frontiers in Plant Science, v. 7, 2016."),
        emptyLine(),
        p("SANDLER, M. et al. MobileNetV2: Inverted Residuals and Linear Bottlenecks. CVPR, 2018."),
        emptyLine(),
        p("SINGH, D. et al. PlantDoc: A Dataset for Visual Plant Disease Detection. ACM CODS-COMAD, 2020."),
        emptyLine(),
        p("WARDEN, P.; SITUNAYAKE, D. TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers. O'Reilly, 2019."),
        emptyLine(),
        p("XU, M. et al. Plant disease recognition datasets in the age of deep learning. Frontiers in Plant Science, v. 15, 2024."),
        emptyLine(),
        p("YOSINSKI, J. et al. How transferable are features in deep neural networks? NeurIPS, v. 27, 2014."),
      ]
    }
  ]
});

const OUTPUT = "C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/TCC_CERES.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT, buffer);
  console.log("TCC_CERES.docx gerado com sucesso: " + OUTPUT);
  console.log("Tamanho: " + (buffer.length / 1024).toFixed(1) + " KB");
});
