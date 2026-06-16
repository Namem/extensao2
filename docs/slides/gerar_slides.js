const pptxgen = require("pptxgenjs");

// ---------------------------------------------------------------------------
// Paleta
// ---------------------------------------------------------------------------
const VE  = "1B4332";   // verde escuro
const VM  = "2D6A4F";   // verde médio
const VC  = "52B788";   // verde claro
const DO  = "D4A017";   // dourado
const BR  = "FFFFFF";   // branco
const CI  = "F4F6F0";   // fundo conteúdo
const GT  = "1F2937";   // texto corpo escuro
const VM2 = "40916C";   // verde médio 2

const makeShadow = () => ({
  type: "outer", blur: 5, offset: 2, angle: 135,
  color: "000000", opacity: 0.14
});

// Barra de cabeçalho + fundo padrão
function headerBar(s, title) {
  s.background = { color: CI };
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.72, fill: { color: VE }, line: { color: VE } });
  s.addText(title, {
    x: 0.35, y: 0, w: 9.3, h: 0.72,
    fontSize: 22, fontFace: "Calibri", bold: true,
    color: BR, valign: "middle", margin: 0
  });
}

function slideNum(s, n) {
  s.addText(`${n} / 10`, {
    x: 9.25, y: 5.35, w: 0.65, h: 0.22,
    fontSize: 9, color: "6B7280", align: "right"
  });
}

// Caixa com header colorido e corpo branco
function infoCard(s, x, y, w, h, headerTxt, headerColor, bodyFn) {
  s.addShape("rect", { x, y, w, h, fill: { color: BR },
    line: { color: headerColor, pt: 1.5 }, rectRadius: 0.07, shadow: makeShadow() });
  s.addShape("rect", { x, y, w, h: 0.42, fill: { color: headerColor },
    line: { color: headerColor } });
  // arredondar só os cantos superiores — overlay nos inferiores
  s.addShape("rect", { x, y: y + 0.28, w, h: 0.2, fill: { color: headerColor },
    line: { color: headerColor } });
  s.addText(headerTxt, { x, y, w, h: 0.42, fontSize: 13, bold: true,
    color: BR, align: "center", valign: "middle" });
  bodyFn(x, y + 0.48, w, h - 0.48);
}

const pres = new pptxgen();
pres.layout  = "LAYOUT_16x9";
pres.author  = "Namem Rachid Jaudy Neto";
pres.title   = "Ceres Diagnóstico — PSI";

// ===========================================================================
// SLIDE 1 — CAPA
// ===========================================================================
{
  const s = pres.addSlide();
  s.background = { color: VE };

  // Faixa dourada superior
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.18, fill: { color: DO }, line: { color: DO } });
  // Faixa dourada inferior
  s.addShape("rect", { x: 0, y: 5.44, w: 10, h: 0.18, fill: { color: DO }, line: { color: DO } });

  // Badge IFMT
  s.addShape("rect", { x: 8.5, y: 0.28, w: 1.3, h: 0.52,
    fill: { color: DO }, line: { color: DO }, rectRadius: 0.06 });
  s.addText("IFMT", { x: 8.5, y: 0.28, w: 1.3, h: 0.52,
    fontSize: 15, bold: true, color: VE, align: "center", valign: "middle" });

  // Título
  s.addText("Ceres Diagnóstico", {
    x: 0.4, y: 0.7, w: 8.0, h: 1.0,
    fontSize: 42, fontFace: "Calibri", bold: true, color: BR, align: "left"
  });
  // Linha dourada decorativa abaixo do título
  s.addShape("rect", { x: 0.4, y: 1.65, w: 7.5, h: 0.05, fill: { color: DO }, line: { color: DO } });

  // Subtítulo — branco puro, fonte menor
  s.addText("Sistema TinyML Embarcado para\nDetecção de Doenças em Tomateiro", {
    x: 0.4, y: 1.75, w: 8.5, h: 1.0,
    fontSize: 21, fontFace: "Calibri", color: BR, align: "left"
  });

  // Caixa info — autor
  s.addShape("rect", { x: 0.4, y: 2.95, w: 6.8, h: 1.65,
    fill: { color: VM }, line: { color: VC, pt: 1 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText([
    { text: "Defesa de Artigo — Disciplina PSI  |  IFMT Cuiabá\n", options: { fontSize: 13, color: DO, bold: true } },
    { text: "Namem Rachid Jaudy Neto\n", options: { fontSize: 18, color: BR, bold: true } },
    { text: "Junho 2026", options: { fontSize: 14, color: "B7E4C7" } }
  ], { x: 0.4, y: 2.95, w: 6.8, h: 1.65, align: "left", valign: "middle",
    insetBottom: 0.1, insetTop: 0.1, insetLeft: 0.25 });
}

// ===========================================================================
// SLIDE 2 — PROBLEMA E MOTIVAÇÃO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Problema e Motivação");
  slideNum(s, 2);

  const bullets = [
    "Tomateiro: cultura de R$ 10 bi/ano no Brasil — 3ª maior produção mundial (FAO 2024)",
    "Doenças foliares causam até 100% de perda de safra",
    "Diagnóstico depende de agrônomos especializados — inacessíveis ao pequeno produtor rural",
    "Conectividade instável em zonas rurais inviabiliza soluções 100% cloud"
  ];

  s.addText(
    bullets.map((t, i) => ({ text: t,
      options: { bullet: { indent: 15 }, breakLine: i < bullets.length - 1, paraSpaceAfter: 14 }
    })),
    { x: 0.4, y: 0.85, w: 9.2, h: 2.35,
      fontSize: 15, fontFace: "Calibri", color: GT, valign: "top" }
  );

  // Caixa dourada — começa logo após os bullets
  s.addShape("rect", { x: 0.4, y: 3.28, w: 9.2, h: 2.02,
    fill: { color: DO }, line: { color: DO }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText([
    { text: "Por que isso importa?\n", options: { bold: true, fontSize: 15, color: VE } },
    { text: "Sorriso-MT concentra grande parte da produção de tomate de Mato Grosso. A maioria dos produtores é de pequeno porte, sem acesso regular a assistência técnica. O Ceres oferece diagnóstico em campo, offline, a menos de R$ 80 em hardware.", options: { fontSize: 13, color: VE } }
  ], { x: 0.55, y: 3.33, w: 8.9, h: 1.9, valign: "middle" });
}

// ===========================================================================
// SLIDE 3 — OBJETIVOS E CONTRIBUIÇÕES
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Objetivos e Contribuições");
  slideNum(s, 3);

  const colW = 4.55, colH = 4.45, colY = 0.82;
  const col1x = 0.25, col2x = 5.2;

  // Colunas simétricas
  [col1x, col2x].forEach((cx, ci) => {
    const hColor = ci === 0 ? VM : VE;
    s.addShape("rect", { x: cx, y: colY, w: colW, h: colH,
      fill: { color: BR }, line: { color: ci === 0 ? VC : DO, pt: 1.5 },
      rectRadius: 0.08, shadow: makeShadow() });
    s.addShape("rect", { x: cx, y: colY, w: colW, h: 0.48,
      fill: { color: hColor }, line: { color: hColor } });
    s.addShape("rect", { x: cx, y: colY + 0.32, w: colW, h: 0.22,
      fill: { color: hColor }, line: { color: hColor } });
    const titles = ["Objetivo Geral", "5 Contribuições"];
    s.addText(titles[ci], { x: cx, y: colY, w: colW, h: 0.48,
      fontSize: 14, bold: true, color: BR, align: "center", valign: "middle" });
  });

  // Corpo esquerdo
  s.addText(
    "Sistema embarcado de baixo custo para detecção precoce de 10 doenças do tomateiro integrando:\n\n" +
    "   • TinyML — ESP32-S3 N16R8\n" +
    "   • IoT — MQTT / HiveMQ Cloud\n" +
    "   • App móvel — Flutter + Dart\n\n" +
    "Código-fonte e modelos abertos ao público.\ngithub.com/Namem/extensao2",
    { x: col1x + 0.18, y: colY + 0.58, w: colW - 0.3, h: colH - 0.65,
      fontSize: 13, color: GT, valign: "top", fontFace: "Calibri" }
  );

  // Corpo direito — 5 contribuições
  const contribs = [
    "10 classes, pipeline reproduzível (código aberto)",
    "ESP32-S3: 692 ms, modelo INT8 de 638 KB",
    "3 arquiteturas: Edge / Mobile on-device / Cloud",
    "Validação em 3 datasets de campo independentes",
    "5 experimentos documentados (incl. negativos)"
  ];
  const icons = ["①","②","③","④","⑤"];
  contribs.forEach((txt, i) => {
    const iy = colY + 0.6 + i * 0.76;
    s.addShape("rect", { x: col2x + 0.15, y: iy, w: 0.38, h: 0.38,
      fill: { color: VE }, line: { color: DO, pt: 1 }, rectRadius: 0.04 });
    s.addText(icons[i], { x: col2x + 0.15, y: iy, w: 0.38, h: 0.38,
      fontSize: 12, color: DO, bold: true, align: "center", valign: "middle" });
    s.addText(txt, { x: col2x + 0.6, y: iy - 0.04, w: colW - 0.72, h: 0.46,
      fontSize: 12.5, color: GT, valign: "middle" });
  });
}

// ===========================================================================
// SLIDE 4 — ARQUITETURA
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Três Caminhos de Inferência — Mesmo Modelo");
  slideNum(s, 4);

  // Modelo central
  s.addShape("rect", { x: 3.15, y: 2.45, w: 3.7, h: 1.1,
    fill: { color: VE }, line: { color: DO, pt: 2 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText("MobileNetV2 INT8\n638 KB · 96×96 · 10 classes · T=0,25", {
    x: 3.15, y: 2.45, w: 3.7, h: 1.1,
    fontSize: 12, bold: true, color: DO, align: "center", valign: "middle"
  });

  const paths = [
    { x: 0.15, bColor: "1D4ED8", label: "① Edge", sub: "ESP32-S3 N16R8",
      items: "692 ms  •  offline\nMQTT/TLS → HiveMQ\nPrivacidade total (LGPD)", res: "692 ms" },
    { x: 3.55, bColor: VM2, label: "② Mobile", sub: "Android on-device",
      items: "~200–400 ms  •  offline\ntflite_flutter 0.12.1\nToggle Edge ↔ Cloud no app", res: "~200–400 ms" },
    { x: 6.95, bColor: "7E22CE", label: "③ Cloud", sub: "Flutter + Django",
      items: "306 ms  •  HTTPS\nAPI Railway + PostgreSQL\nPipeline completo validado", res: "306 ms" }
  ];

  paths.forEach(p => {
    // Header caixa
    s.addShape("rect", { x: p.x, y: 0.85, w: 2.85, h: 0.62,
      fill: { color: p.bColor }, line: { color: p.bColor }, rectRadius: 0.06 });
    s.addText(`${p.label}  —  ${p.sub}`, { x: p.x, y: 0.85, w: 2.85, h: 0.62,
      fontSize: 12, bold: true, color: BR, align: "center", valign: "middle" });

    // Corpo info
    s.addShape("rect", { x: p.x, y: 1.52, w: 2.85, h: 0.88,
      fill: { color: BR }, line: { color: p.bColor, pt: 1 }, rectRadius: 0.06 });
    s.addText(p.items, { x: p.x + 0.12, y: 1.52, w: 2.65, h: 0.88,
      fontSize: 11, color: GT, valign: "middle" });

    // Seta para baixo (triângulo via texto)
    s.addText("▼", { x: p.x + 1.3, y: 2.4, w: 0.3, h: 0.2,
      fontSize: 11, color: "9CA3AF", align: "center" });

    // Resultado
    s.addShape("rect", { x: p.x, y: 3.62, w: 2.85, h: 0.6,
      fill: { color: p.bColor }, line: { color: p.bColor }, rectRadius: 0.06 });
    s.addText(p.res, { x: p.x, y: 3.62, w: 2.85, h: 0.6,
      fontSize: 15, bold: true, color: BR, align: "center", valign: "middle" });

    // Seta de baixo para cima
    s.addText("▲", { x: p.x + 1.3, y: 3.3, w: 0.3, h: 0.2,
      fontSize: 11, color: "9CA3AF", align: "center" });
  });

  // Nota rodapé — 14pt para ser legível
  s.addText(
    "* Latência Mobile estimada — não medida empiricamente neste ciclo  |  Caminhos ① e ②: imagem nunca sai do dispositivo",
    { x: 0.3, y: 4.35, w: 9.4, h: 0.55,
      fontSize: 11, color: "6B7280", italic: true, align: "center",
      fill: { color: "E9F5EE" }, line: { color: "C3E6D1", pt: 1 }
    }
  );
}

// ===========================================================================
// SLIDE 5 — DATASET E PIPELINE
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Dataset e Pipeline de Treinamento");
  slideNum(s, 5);

  // Pipeline — 4 caixas + setas
  const steps = [
    { label: "PlantVillage\n18.160 imgs\n10 classes", color: VE, tc: BR },
    { label: "Split\n70 / 15 / 15\nseed = 42",        color: VM2, tc: BR },
    { label: "Augment.\noffline × 6\n(só treino)",    color: VC,  tc: BR },
    { label: "88.949 imgs\ntreino final",              color: DO,  tc: VE }
  ];

  const bw = 2.05, bh = 1.1, by = 0.88, gap = 0.28;
  steps.forEach((st, i) => {
    const bx = 0.2 + i * (bw + gap);
    s.addShape("rect", { x: bx, y: by, w: bw, h: bh,
      fill: { color: st.color }, line: { color: st.color },
      rectRadius: 0.07, shadow: makeShadow() });
    s.addText(st.label, { x: bx, y: by, w: bw, h: bh,
      fontSize: 12.5, bold: true, color: st.tc, align: "center", valign: "middle" });
    if (i < steps.length - 1) {
      s.addText("→", { x: bx + bw + 0.02, y: by + 0.32, w: gap, h: 0.46,
        fontSize: 18, color: VM, align: "center", bold: true });
    }
  });

  // Tabela splits
  const tData = [
    [
      { text: "Split",           options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
      { text: "Imagens",         options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }
    ],
    [{ text: "Treino (augmentado)", options: { bold: true } }, { text: "88.949", options: { align: "center", bold: true } }],
    ["Validação",                   { text: "2.724",  options: { align: "center" } }],
    ["Teste (nunca visto)",          { text: "2.734",  options: { align: "center" } }]
  ];
  s.addTable(tData, {
    x: 0.2, y: 2.15, w: 4.5, h: 1.8,
    fontSize: 13.5, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" },
    colW: [2.9, 1.6],
    rowH: 0.45
  });

  // Caixa classes — tabela interna 2×5
  s.addShape("rect", { x: 4.95, y: 2.15, w: 4.8, h: 3.12,
    fill: { color: "F0FFF4" }, line: { color: VC, pt: 1.5 }, rectRadius: 0.08 });
  s.addText("10 classes do modelo:", { x: 5.1, y: 2.2, w: 4.5, h: 0.38,
    fontSize: 13, bold: true, color: VE });

  // Classes em tabela 2 colunas
  const classes = [
    ["D01  Requeima",       "D06  Vira-cabeça"],
    ["D02  Septoriose",     "D06b Mosaico"],
    ["D03  Pinta-preta",    "D07  Ácaro"],
    ["D03b Mancha-alvo",   "D09  M. bacteriana"],
    ["D05  Mofo foliar",    "Saudável"]
  ];
  classes.forEach((row, i) => {
    const ry = 2.62 + i * 0.48;
    s.addShape("rect", { x: 5.05, y: ry, w: 2.3, h: 0.42,
      fill: { color: i % 2 === 0 ? "E8F5E9" : BR }, line: { color: "E8F5E9" } });
    s.addText(row[0], { x: 5.12, y: ry, w: 2.2, h: 0.42,
      fontSize: 11.5, color: GT, valign: "middle", fontFace: "Courier New" });
    s.addShape("rect", { x: 7.38, y: ry, w: 2.3, h: 0.42,
      fill: { color: i % 2 === 0 ? "E8F5E9" : BR }, line: { color: "E8F5E9" } });
    s.addText(row[1], { x: 7.45, y: ry, w: 2.2, h: 0.42,
      fontSize: 11.5, color: GT, valign: "middle", fontFace: "Courier New" });
  });
}

// ===========================================================================
// SLIDE 6 — 5 EXPERIMENTOS
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Evolução: 5 Experimentos de Treinamento");
  slideNum(s, 6);

  const hdr = [
    { text: "Exp",         options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "Estratégia",  options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "PlantVillage",options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "PlantDoc",    options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }
  ];

  const rows = [
    [
      { text: "A", options: { align: "center" } },
      "Edge Impulse — sem calibração INT8",
      { text: "92,5% (FP32)\n62,0% (INT8)", options: { color: "B91C1C", bold: true, align: "center" } },
      { text: "—", options: { align: "center" } }
    ],
    [
      { text: "B", options: { align: "center" } },
      "TF local — calibração INT8 (50 batches)",
      { text: "98,13%", options: { align: "center", bold: true } },
      { text: "20,77%", options: { align: "center" } }
    ],
    [
      { text: "C", options: { align: "center" } },
      "Exp B + augmentation sintética (rembg U2-Net)",
      { text: "96,20%", options: { align: "center" } },
      { text: "20,24%  ❌", options: { align: "center", color: "B91C1C", bold: true } }
    ],
    [
      { text: "D", options: { align: "center" } },
      "Exp B + fine-tuning real (PlantDoc/train)",
      { text: "97,55%", options: { align: "center" } },
      { text: "30,43%  ✅", options: { align: "center", color: "166534", bold: true } }
    ],
    [
      { text: "E ★", options: { align: "center", bold: true, color: DO, fill: { color: VE } } },
      { text: "Exp D + Focal Loss γ=2 + aug. agressiva  ← MODELO FINAL", options: { bold: true, fill: { color: VE }, color: BR } },
      { text: "98,43%", options: { align: "center", bold: true, fill: { color: VE }, color: DO } },
      { text: "30,43%  ✅", options: { align: "center", bold: true, fill: { color: VE }, color: VC } }
    ]
  ];

  s.addTable([hdr, ...rows], {
    x: 0.25, y: 0.85, w: 9.5, h: 3.9,
    fontSize: 13, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" },
    colW: [0.65, 4.3, 2.4, 2.15],
    rowH: 0.65
  });

  // Legenda — fonte 13pt
  s.addShape("rect", { x: 0.25, y: 4.88, w: 9.5, h: 0.65,
    fill: { color: "FFFBEB" }, line: { color: DO, pt: 1.5 }, rectRadius: 0.06 });
  s.addText([
    { text: "−30 pp", options: { bold: true, color: "B91C1C" } },
    { text: " = INT8 sem calibração (Exp A vs B)     ", options: { color: GT } },
    { text: "+36 pp", options: { bold: true, color: "166534" } },
    { text: " = calibração com 50 batches     ", options: { color: GT } },
    { text: "Exp C", options: { bold: true, color: "B91C1C" } },
    { text: " = resultado negativo documentado (augmentation sintética ineficaz)", options: { color: GT } }
  ], { x: 0.4, y: 4.91, w: 9.2, h: 0.58, fontSize: 13, valign: "middle" });
}

// ===========================================================================
// SLIDE 7 — GAP LAB-CAMPO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Gap Laboratório-Campo: Validação em 3 Datasets");
  slideNum(s, 7);

  // Anotação FORA do gráfico — acima do gráfico
  s.addShape("rect", { x: 0.25, y: 0.82, w: 5.5, h: 0.32,
    fill: { color: "FEE2E2" }, line: { color: "FCA5A5", pt: 1 }, rectRadius: 0.04 });
  s.addText("Referência lab: PlantVillage (controlado) = 98,43%  ↑↑", {
    x: 0.28, y: 0.82, w: 5.44, h: 0.32,
    fontSize: 11, color: "991B1B", bold: true, valign: "middle"
  });

  // Gráfico
  s.addChart(pres.charts.BAR, [
    { name: "Exp B (baseline)",    labels: ["PlantDoc\n(EUA/Europa)", "Tomato-Village\n(Índia)", "Daffodil BD\n(Bangladesh)"], values: [20.77, 0.01, 0.01] },
    { name: "Exp D (fine-tuning)", labels: ["PlantDoc\n(EUA/Europa)", "Tomato-Village\n(Índia)", "Daffodil BD\n(Bangladesh)"], values: [30.43, 11.52, 9.59] },
    { name: "Exp E (Focal Loss)",  labels: ["PlantDoc\n(EUA/Europa)", "Tomato-Village\n(Índia)", "Daffodil BD\n(Bangladesh)"], values: [30.43, 27.65, 18.13] }
  ], {
    x: 0.25, y: 1.2, w: 5.5, h: 3.92,
    barDir: "col", barGrouping: "clustered",
    chartColors: ["B7E4C7", VM2, VE],
    chartArea: { fill: { color: BR }, roundedCorners: false },
    catAxisLabelColor: "374151", catAxisLabelFontSize: 10,
    valAxisLabelColor: "374151", valAxisLabelFontSize: 10,
    valGridLine: { color: "E5E7EB", size: 0.5 },
    catGridLine: { style: "none" },
    showValue: true, dataLabelFontSize: 10, dataLabelColor: "111827",
    legendPos: "b", showLegend: true, legendFontSize: 11,
    valAxisMaxVal: 35,
    showTitle: false
  });

  // Caixa análise — mesma altura que área do gráfico
  s.addShape("rect", { x: 5.95, y: 0.82, w: 3.85, h: 4.3,
    fill: { color: "FFFBEB" }, line: { color: DO, pt: 1.5 },
    rectRadius: 0.08, shadow: makeShadow() });
  s.addShape("rect", { x: 5.95, y: 0.82, w: 3.85, h: 0.42,
    fill: { color: VM }, line: { color: VM } });
  s.addShape("rect", { x: 5.95, y: 1.1, w: 3.85, h: 0.18,
    fill: { color: VM }, line: { color: VM } });
  s.addText("Análise do Gap", { x: 5.95, y: 0.82, w: 3.85, h: 0.42,
    fontSize: 13, bold: true, color: BR, align: "center", valign: "middle" });

  const analise = [
    { text: "Gap persistente:\n", options: { bold: true, color: "B91C1C", fontSize: 13 } },
    { text: "98,43% (lab) → 18–30% (campo)\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Causa identificada:\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "Modelo aprende o fundo cinza do PlantVillage como feature discriminativa, não as lesões.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Exp C ineficaz:\n", options: { bold: true, color: "B91C1C", fontSize: 13 } },
    { text: "Aug. sintética (rembg) = 0 ganho\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Único método efetivo:\n", options: { bold: true, color: "166534", fontSize: 13 } },
    { text: "+10 pp com 677 imgs reais rotuladas", options: { color: GT, fontSize: 12 } }
  ];
  s.addText(analise, { x: 6.1, y: 1.35, w: 3.55, h: 3.65, valign: "top" });
}

// ===========================================================================
// SLIDE 8 — COMPARATIVO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Comparativo das Três Arquiteturas");
  slideNum(s, 8);

  const hdr = [
    { text: "Aspecto",            options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "① Edge  ESP32-S3",  options: { bold: true, color: BR, fill: { color: "1D4ED8" }, align: "center" } },
    { text: "② Mobile  Android", options: { bold: true, color: BR, fill: { color: VM2 }, align: "center" } },
    { text: "③ Cloud  Django",   options: { bold: true, color: BR, fill: { color: "7E22CE" }, align: "center" } }
  ];

  const chk = { color: "166534", bold: true, align: "center" };
  const crs = { color: "B91C1C", bold: true, align: "center" };
  const wrn = { color: "92400E", bold: true, align: "center" };

  const rows = [
    [
      "Latência CNN",
      { text: "692 ms (±1 ms)", options: { align: "center", bold: true } },
      { text: "~200–400 ms *", options: { align: "center", italic: true } },
      { text: "306 ms", options: { align: "center" } }
    ],
    [
      "Funciona offline",
      { text: "✅  Sim", options: chk },
      { text: "✅  Sim", options: chk },
      { text: "❌  Não", options: crs }
    ],
    [
      "Privacidade (LGPD)",
      { text: "✅  Total", options: chk },
      { text: "✅  Total", options: chk },
      { text: "⚠️  Imagem transmitida", options: wrn }
    ],
    [
      "Custo hardware",
      { text: "~R$ 80", options: { align: "center" } },
      { text: "Zero (app)", options: { align: "center" } },
      { text: "Servidor", options: { align: "center" } }
    ],
    [
      "Status atual",
      { text: "✅  Validado\n10/10 corretas", options: chk },
      { text: "✅  Implementado\ntflite_flutter 0.12.1", options: chk },
      { text: "✅  Produção\nRailway", options: chk }
    ]
  ];

  s.addTable([hdr, ...rows], {
    x: 0.25, y: 0.85, w: 9.5, h: 4.38,
    fontSize: 13, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" },
    colW: [2.0, 2.5, 2.5, 2.5],
    rowH: [0.5, 0.68, 0.68, 0.68, 0.68, 0.76]
  });

  s.addText("* Estimada — não medida empiricamente neste ciclo  |  Mesmo modelo INT8 (638 KB) nos três caminhos", {
    x: 0.25, y: 5.3, w: 9.5, h: 0.26,
    fontSize: 10, color: "6B7280", italic: true, align: "center"
  });
}

// ===========================================================================
// SLIDE 9 — CONCLUSÃO E LIMITAÇÕES
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Conclusão e Limitações");
  slideNum(s, 9);

  const colW = 4.6, colH = 4.52, colY = 0.8;

  // Colunas
  const cols = [
    { x: 0.25, bg: "F0FFF4", border: VC, hbg: VM2, label: "✅  O que funcionou" },
    { x: 5.15, bg: "FFF5F5", border: "FCA5A5", hbg: "B91C1C", label: "⚠️  Limitações" }
  ];
  cols.forEach(c => {
    s.addShape("rect", { x: c.x, y: colY, w: colW, h: colH,
      fill: { color: c.bg }, line: { color: c.border, pt: 1.5 },
      rectRadius: 0.08, shadow: makeShadow() });
    s.addShape("rect", { x: c.x, y: colY, w: colW, h: 0.48,
      fill: { color: c.hbg }, line: { color: c.hbg } });
    s.addShape("rect", { x: c.x, y: colY + 0.32, w: colW, h: 0.22,
      fill: { color: c.hbg }, line: { color: c.hbg } });
    s.addText(c.label, { x: c.x, y: colY, w: colW, h: 0.48,
      fontSize: 13, bold: true, color: BR, align: "center", valign: "middle" });
  });

  // Bullets esquerda
  const ok = [
    "MobileNetV2 INT8 viável no ESP32-S3 (692 ms, 638 KB)",
    "Calibração INT8 elimina quantization loss (+36 pp)",
    "Fine-tuning com dados reais: +10 pp em campo",
    "Focal Loss γ=2: +16 pp no Tomato-Village (Índia)",
    "Pipeline: ESP32-S3 → MQTT → Django → Flutter"
  ];
  s.addText(
    ok.map((t, i) => ({ text: t,
      options: { bullet: { indent: 12 }, breakLine: i < ok.length - 1, paraSpaceAfter: 22 }
    })),
    { x: 0.38, y: colY + 0.58, w: colW - 0.24, h: colH - 0.65,
      fontSize: 14, color: "166534", valign: "middle" }
  );

  // Bullets direita
  const lim = [
    "Gap lab-campo persiste (98,43% → 18–30%)",
    "Augmentation sintética ineficaz (Exp C)",
    "Latência 692 ms acima da meta de 300 ms",
    "Câmera OV5640 não integrada neste ciclo",
    "Latência Mobile não medida empiricamente"
  ];
  s.addText(
    lim.map((t, i) => ({ text: t,
      options: { bullet: { indent: 12 }, breakLine: i < lim.length - 1, paraSpaceAfter: 22 }
    })),
    { x: 5.28, y: colY + 0.58, w: colW - 0.24, h: colH - 0.65,
      fontSize: 14, color: "7F1D1D", valign: "middle" }
  );
}

// ===========================================================================
// SLIDE 10 — PRÓXIMOS PASSOS
// ===========================================================================
{
  const s = pres.addSlide();
  s.background = { color: VE };

  // Header igual aos demais (faixa escura ainda mais escura)
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.72, fill: { color: "0D2B1D" }, line: { color: "0D2B1D" } });
  s.addText("Próximos Passos", {
    x: 0.35, y: 0, w: 9.3, h: 0.72,
    fontSize: 22, fontFace: "Calibri", bold: true, color: BR, valign: "middle", margin: 0
  });

  // 4 itens — sem linha sobreposta ao texto
  const items = [
    { badge: "Sprint 2", txt: "Integração câmera OV5640 + medição de latência real no ESP32-S3" },
    { badge: "Sprint 3", txt: "Dataset em Sorriso-MT + validação com produtores rurais reais" },
    { badge: "Pesquisa", txt: "Domain Adaptation adversarial (DANN) — sem rótulos de campo" },
    { badge: "Pesquisa", txt: "Medição empírica da latência Android on-device (tflite_flutter)" }
  ];

  items.forEach((item, i) => {
    const iy = 0.9 + i * 0.85;
    // Badge
    s.addShape("rect", { x: 0.35, y: iy, w: 1.25, h: 0.55,
      fill: { color: DO }, line: { color: DO }, rectRadius: 0.06 });
    s.addText(item.badge, { x: 0.35, y: iy, w: 1.25, h: 0.55,
      fontSize: 12, bold: true, color: VE, align: "center", valign: "middle" });
    // Texto — sem linha sobreposta, fundo levemente mais claro
    s.addShape("rect", { x: 1.72, y: iy, w: 7.95, h: 0.55,
      fill: { color: VM }, line: { color: VM }, rectRadius: 0.05 });
    s.addText(item.txt, { x: 1.82, y: iy, w: 7.75, h: 0.55,
      fontSize: 14, color: BR, valign: "middle" });
  });

  // Separador
  s.addShape("rect", { x: 0.35, y: 4.38, w: 9.3, h: 0.03,
    fill: { color: DO }, line: { color: DO } });

  // Caixa GitHub — fundo VM mais claro para destacar
  s.addShape("rect", { x: 1.5, y: 4.5, w: 7.0, h: 0.55,
    fill: { color: VM2 }, line: { color: DO, pt: 1.5 }, rectRadius: 0.07 });
  s.addText("github.com/Namem/extensao2", {
    x: 1.5, y: 4.5, w: 7.0, h: 0.55,
    fontSize: 14, color: DO, align: "center", valign: "middle", bold: true
  });

  // Obrigado — com margem do GitHub
  s.addText("Obrigado!  Perguntas?", {
    x: 0, y: 5.1, w: 10, h: 0.5,
    fontSize: 24, bold: true, color: BR, align: "center"
  });
}

// ---------------------------------------------------------------------------
// Gerar
// ---------------------------------------------------------------------------
pres.writeFile({ fileName: "ceres_diagnostico_psi.pptx" })
  .then(() => console.log("✅ Slides gerados: ceres_diagnostico_psi.pptx"))
  .catch(e  => { console.error("ERRO:", e); process.exit(1); });
