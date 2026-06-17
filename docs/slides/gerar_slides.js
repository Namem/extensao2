const pptxgen = require("pptxgenjs");

// ---------------------------------------------------------------------------
// Paleta
// ---------------------------------------------------------------------------
const VE  = "1B4332"; const VM  = "2D6A4F"; const VC  = "52B788";
const DO  = "D4A017"; const BR  = "FFFFFF"; const CI  = "F4F6F0";
const GT  = "1F2937"; const VM2 = "40916C"; const RD  = "B91C1C"; const GN  = "166534";
const TOTAL = 23;

const makeShadow = () => ({ type: "outer", blur: 5, offset: 2, angle: 135, color: "000000", opacity: 0.14 });

function headerBar(s, title) {
  s.background = { color: CI };
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.72, fill: { color: VE }, line: { color: VE } });
  s.addText(title, { x: 0.35, y: 0, w: 9.3, h: 0.72,
    fontSize: 22, fontFace: "Calibri", bold: true, color: BR, valign: "middle", margin: 0 });
}
function slideNum(s, n) {
  s.addText(`${n} / ${TOTAL}`, { x: 9.2, y: 5.35, w: 0.7, h: 0.22,
    fontSize: 9, color: "6B7280", align: "right" });
}
function card(s, x, y, w, h, hbg, border, label) {
  s.addShape("rect", { x, y, w, h, fill: { color: BR }, line: { color: border, pt: 1.5 },
    rectRadius: 0.08, shadow: makeShadow() });
  s.addShape("rect", { x, y, w, h: 0.46, fill: { color: hbg }, line: { color: hbg } });
  s.addShape("rect", { x, y: y + 0.28, w, h: 0.2, fill: { color: hbg }, line: { color: hbg } });
  s.addText(label, { x, y, w, h: 0.46, fontSize: 13, bold: true, color: BR,
    align: "center", valign: "middle" });
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
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.18, fill: { color: DO }, line: { color: DO } });
  s.addShape("rect", { x: 0, y: 5.44, w: 10, h: 0.18, fill: { color: DO }, line: { color: DO } });
  s.addShape("rect", { x: 8.5, y: 0.28, w: 1.3, h: 0.52, fill: { color: DO }, line: { color: DO }, rectRadius: 0.06 });
  s.addText("IFMT", { x: 8.5, y: 0.28, w: 1.3, h: 0.52, fontSize: 15, bold: true, color: VE, align: "center", valign: "middle" });
  s.addText("Ceres Diagnóstico", { x: 0.4, y: 0.7, w: 8.0, h: 1.0, fontSize: 42, fontFace: "Calibri", bold: true, color: BR, align: "left" });
  s.addShape("rect", { x: 0.4, y: 1.65, w: 7.5, h: 0.05, fill: { color: DO }, line: { color: DO } });
  s.addText("Sistema TinyML Embarcado para\nDetecção de Doenças em Tomateiro", { x: 0.4, y: 1.75, w: 8.5, h: 1.0, fontSize: 21, fontFace: "Calibri", color: BR, align: "left" });
  s.addShape("rect", { x: 0.4, y: 2.95, w: 6.8, h: 1.65, fill: { color: VM }, line: { color: VC, pt: 1 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText([
    { text: "Defesa de Artigo — Disciplina PSI  |  IFMT Cuiabá\n", options: { fontSize: 13, color: DO, bold: true } },
    { text: "Namem Rachid Jaudy Neto\n", options: { fontSize: 18, color: BR, bold: true } },
    { text: "Junho 2026", options: { fontSize: 14, color: "B7E4C7" } }
  ], { x: 0.4, y: 2.95, w: 6.8, h: 1.65, align: "left", valign: "middle", insetLeft: 0.25 });
}

// ===========================================================================
// SLIDE 2 — AGENDA
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Roteiro da Apresentação");
  slideNum(s, 2);
  const ag = [
    ["1", "Problema e proposta"],
    ["2", "Como construímos o modelo"],
    ["3", "A surpresa: gap laboratório–campo"],
    ["4", "Os cinco experimentos"],
    ["5", "Gap geográfico e colapso de classe"],
    ["6", "Arquitetura: onde rodar o modelo?"],
    ["7", "Sistema em funcionamento"],
    ["8", "Conclusão e trabalhos futuros"]
  ];
  ag.forEach((it, i) => {
    const col = i < 4 ? 0 : 1;
    const row = col === 0 ? i : i - 4;
    const x = col === 0 ? 0.5 : 5.15;
    const y = 1.1 + row * 0.95;
    s.addShape("rect", { x, y, w: 0.55, h: 0.55, fill: { color: VE }, line: { color: DO, pt: 1 }, rectRadius: 0.05 });
    s.addText(it[0], { x, y, w: 0.55, h: 0.55, fontSize: 17, bold: true, color: DO, align: "center", valign: "middle" });
    s.addText(it[1], { x: x + 0.68, y: y - 0.02, w: 3.9, h: 0.6, fontSize: 14, color: GT, valign: "middle" });
  });
}

// ===========================================================================
// SLIDE 3 — PROBLEMA E MOTIVAÇÃO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Problema e Motivação");
  slideNum(s, 3);
  const bullets = [
    "Tomateiro: cultura de R$ 10 bi/ano no Brasil — 3ª maior produção mundial (FAO 2024)",
    "Doenças foliares causam até 100% de perda de safra",
    "Diagnóstico depende de agrônomos especializados — inacessíveis ao pequeno produtor rural",
    "Conectividade instável em zonas rurais inviabiliza soluções 100% cloud"
  ];
  s.addText(bullets.map((t, i) => ({ text: t,
    options: { bullet: { indent: 15 }, breakLine: i < bullets.length - 1, paraSpaceAfter: 14 } })),
    { x: 0.4, y: 0.85, w: 9.2, h: 2.35, fontSize: 15, fontFace: "Calibri", color: GT, valign: "top" });
  s.addShape("rect", { x: 0.4, y: 3.28, w: 9.2, h: 2.02, fill: { color: DO }, line: { color: DO }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText([
    { text: "Por que isso importa?\n", options: { bold: true, fontSize: 15, color: VE } },
    { text: "Pequenos produtores rurais não têm acesso regular a assistência técnica. Um diagnóstico em campo, offline, ao alcance do bolso, pode evitar perdas significativas de safra e acelerar a resposta a surtos.", options: { fontSize: 13, color: VE } }
  ], { x: 0.55, y: 3.33, w: 8.9, h: 1.9, valign: "middle" });
}

// ===========================================================================
// SLIDE 4 — NOSSA PROPOSTA
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Nossa Proposta");
  slideNum(s, 4);
  s.addShape("rect", { x: 0.35, y: 0.92, w: 9.3, h: 1.2, fill: { color: VE }, line: { color: DO, pt: 1.5 }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText([
    { text: "Um sistema TinyML embarcado ", options: { color: DO, bold: true, fontSize: 18 } },
    { text: "que classifica ", options: { color: BR, fontSize: 18 } },
    { text: "10 doenças do tomateiro", options: { color: DO, bold: true, fontSize: 18 } },
    { text: ", com baixo custo de hardware e que funciona ", options: { color: BR, fontSize: 18 } },
    { text: "sem internet.", options: { color: DO, bold: true, fontSize: 18 } }
  ], { x: 0.55, y: 0.97, w: 8.9, h: 1.1, valign: "middle" });
  const pillars = [
    { color: VM,  num: "10",   suf: "classes",  t: "Diagnóstico preciso", d: "9 doenças foliares + folha saudável" },
    { color: VM2, num: "638",  suf: "KB",       t: "Modelo pequeno",      d: "INT8 — cabe num microcontrolador de baixo custo" },
    { color: DO,  num: "100%", suf: "local",    t: "Funciona offline",    d: "Sem dependência de nuvem nem internet" }
  ];
  pillars.forEach((p, i) => {
    const x = 0.35 + i * 3.18, y = 2.4;
    s.addShape("rect", { x, y, w: 2.95, h: 2.85, fill: { color: BR }, line: { color: p.color, pt: 1.5 }, rectRadius: 0.1, shadow: makeShadow() });
    s.addShape("ellipse", { x: x + 0.85, y: y + 0.2, w: 1.25, h: 1.25, fill: { color: p.color }, line: { color: p.color } });
    s.addText(p.num, { x: x + 0.85, y: y + 0.3, w: 1.25, h: 0.78, fontSize: 22, bold: true, color: BR, align: "center", valign: "middle" });
    s.addText(p.suf, { x: x + 0.85, y: y + 0.95, w: 1.25, h: 0.42, fontSize: 11, color: BR, align: "center", valign: "middle" });
    s.addText(p.t, { x: x + 0.15, y: y + 1.6, w: 2.65, h: 0.45, fontSize: 16, bold: true, color: VE, align: "center", valign: "middle" });
    s.addText(p.d, { x: x + 0.25, y: y + 2.1, w: 2.45, h: 0.7, fontSize: 12.5, color: GT, align: "center", valign: "top" });
  });
}

// ===========================================================================
// SLIDE 5 — OBJETIVOS E CONTRIBUIÇÕES
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Objetivos e Contribuições");
  slideNum(s, 5);
  const colW = 4.55, colH = 4.45, colY = 0.82, col1x = 0.25, col2x = 5.2;
  card(s, col1x, colY, colW, colH, VM, VC, "Objetivo Geral");
  card(s, col2x, colY, colW, colH, VE, DO, "5 Contribuições");
  s.addText(
    "Sistema embarcado de baixo custo para detecção precoce de 10 doenças do tomateiro integrando:\n\n" +
    "   • TinyML — ESP32-S3 N16R8\n   • IoT — MQTT / HiveMQ Cloud\n   • App móvel — Flutter + Dart\n\n" +
    "Código-fonte e modelos abertos.\ngithub.com/Namem/extensao2",
    { x: col1x + 0.18, y: colY + 0.58, w: colW - 0.3, h: colH - 0.65, fontSize: 13, color: GT, valign: "top", fontFace: "Calibri" });
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
    s.addShape("rect", { x: col2x + 0.15, y: iy, w: 0.38, h: 0.38, fill: { color: VE }, line: { color: DO, pt: 1 }, rectRadius: 0.04 });
    s.addText(icons[i], { x: col2x + 0.15, y: iy, w: 0.38, h: 0.38, fontSize: 12, color: DO, bold: true, align: "center", valign: "middle" });
    s.addText(txt, { x: col2x + 0.6, y: iy - 0.04, w: colW - 0.72, h: 0.46, fontSize: 12.5, color: GT, valign: "middle" });
  });
}

// ===========================================================================
// SLIDE 6 — DATASET PLANTVILLAGE (pipeline + splits)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Dataset e Pipeline de Treinamento");
  slideNum(s, 6);
  const steps = [
    { label: "PlantVillage\n18.160 imgs\n10 classes", color: VE, tc: BR },
    { label: "Split\n70 / 15 / 15\nseed = 42", color: VM2, tc: BR },
    { label: "Augment.\noffline × 6\n(só treino)", color: VC, tc: BR },
    { label: "88.949 imgs\ntreino final", color: DO, tc: VE }
  ];
  const bw = 2.05, bh = 1.25, by = 0.95, gap = 0.28;
  steps.forEach((st, i) => {
    const bx = 0.2 + i * (bw + gap);
    s.addShape("rect", { x: bx, y: by, w: bw, h: bh, fill: { color: st.color }, line: { color: st.color }, rectRadius: 0.07, shadow: makeShadow() });
    s.addText(st.label, { x: bx, y: by, w: bw, h: bh, fontSize: 13, bold: true, color: st.tc, align: "center", valign: "middle" });
    if (i < steps.length - 1) s.addText("→", { x: bx + bw + 0.02, y: by + 0.4, w: gap, h: 0.46, fontSize: 18, color: VM, align: "center", bold: true });
  });
  // Tabela splits maior
  const tData = [
    [{ text: "Split", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }, { text: "Imagens", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }],
    [{ text: "Treino (augmentado)", options: { bold: true } }, { text: "88.949", options: { align: "center", bold: true } }],
    ["Validação", { text: "2.724", options: { align: "center" } }],
    ["Teste (nunca visto)", { text: "2.734", options: { align: "center" } }]
  ];
  s.addTable(tData, { x: 0.45, y: 2.5, w: 4.9, h: 2.3, fontSize: 15, fontFace: "Calibri", border: { pt: 1, color: "D1D5DB" }, colW: [3.1, 1.8], rowH: 0.57 });
  // Caixa de origem do dataset
  card(s, 5.55, 2.5, 4.2, 2.3, VM, VC, "Origem dos dados");
  s.addText([
    { text: "PlantVillage", options: { bold: true, color: VE, fontSize: 13.5 } },
    { text: " (Hughes & Salathé, 2015)\n", options: { color: GT, fontSize: 12.5 } },
    { text: "~18.000 imagens de folhas de tomate em laboratório, distribuídas em 10 categorias (9 doenças + saudável). Licença CC BY 4.0.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "→ Próximo slide:", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: " exemplos visuais de cada uma das 10 classes.", options: { color: GT, fontSize: 12 } }
  ], { x: 5.75, y: 3.1, w: 3.85, h: 1.6, valign: "top" });
}

// ===========================================================================
// SLIDE 7 — AS 10 CLASSES DO MODELO (NOVO — mosaico de fotos)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "As 10 Classes do Modelo — Exemplos Reais");
  slideNum(s, 7);
  const classes = [
    { f: "cls_01_requeima.jpg",       l: "D01 · Requeima" },
    { f: "cls_02_septoriose.jpg",     l: "D02 · Septoriose" },
    { f: "cls_03_pinta_preta.jpg",    l: "D03 · Pinta-preta" },
    { f: "cls_04_mancha_alvo.jpg",    l: "D03b · Mancha-alvo" },
    { f: "cls_05_mofo_foliar.jpg",    l: "D05 · Mofo foliar" },
    { f: "cls_06_vira_cabeca.jpg",    l: "D06 · Vira-cabeça" },
    { f: "cls_07_mosaico.jpg",        l: "D06b · Mosaico" },
    { f: "cls_08_acaro.jpg",          l: "D07 · Ácaro" },
    { f: "cls_09_mancha_bact.jpg",    l: "D09 · Mancha bact." },
    { f: "cls_10_saudavel.jpg",       l: "Saudável" }
  ];
  const cols = 5, cellW = 1.85, cellH = 1.85, gapX = 0.07, gapY = 0.05;
  const totalW = cols * cellW + (cols - 1) * gapX; // 9.53
  const startX = (10 - totalW) / 2; // ~0.23
  classes.forEach((c, i) => {
    const r = Math.floor(i / cols), col = i % cols;
    const x = startX + col * (cellW + gapX);
    const y = 0.9 + r * (cellH + gapY + 0.35);
    // Foto quadrada
    s.addShape("rect", { x: x - 0.02, y: y - 0.02, w: cellW + 0.04, h: cellH + 0.04, fill: { color: VE }, line: { color: VE } });
    s.addImage({ path: c.f, x, y, w: cellW, h: cellH });
    // Label embaixo
    s.addShape("rect", { x, y: y + cellH + 0.02, w: cellW, h: 0.32, fill: { color: BR }, line: { color: VC, pt: 0.75 } });
    s.addText(c.l, { x, y: y + cellH + 0.02, w: cellW, h: 0.32, fontSize: 10.5, bold: true, color: VE, align: "center", valign: "middle" });
  });
}

// ===========================================================================
// SLIDE 8 — POR QUE MOBILENETV2? (comparativo de arquiteturas)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Por que MobileNetV2? — Comparativo de Arquiteturas");
  slideNum(s, 8);

  // Tabela comparativa — dados do artigo PSI
  const hdr = [
    { text: "Modelo", options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "Parâmetros", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "Tamanho float", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "INT8", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "ESP32-S3", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
  ];
  const trows = [
    ["ResNet-50",
      { text: "25 M",    options: { align: "center" } },
      { text: ">100 MB", options: { align: "center", color: RD } },
      { text: ">25 MB",  options: { align: "center", color: RD } },
      { text: "Nao",     options: { align: "center", color: RD, bold: true } }],
    ["EfficientNet-B0",
      { text: "5,3 M",  options: { align: "center" } },
      { text: "~20 MB", options: { align: "center", color: RD } },
      { text: "~5 MB",  options: { align: "center", color: RD } },
      { text: "Nao",    options: { align: "center", color: RD, bold: true } }],
    ["YOLO (minimo)*",
      { text: "~6 M",   options: { align: "center" } },
      { text: ">10 MB", options: { align: "center", color: RD } },
      { text: ">6 MB",  options: { align: "center", color: RD } },
      { text: "Nao — Detector*", options: { align: "center", color: RD, bold: true } }],
    ["MobileNetV1",
      { text: "4,2 M",  options: { align: "center" } },
      { text: "~3 MB",  options: { align: "center" } },
      { text: "~1,1 MB",options: { align: "center" } },
      { text: "Sim — v1 inferior", options: { align: "center", color: "92400E", bold: true } }],
    [
      { text: "MobileNetV2  *", options: { bold: true, fill: { color: VE }, color: DO } },
      { text: "3,4 M",  options: { align: "center", bold: true, fill: { color: VE }, color: VC } },
      { text: "<4 MB",  options: { align: "center", bold: true, fill: { color: VE }, color: VC } },
      { text: "638 KB", options: { align: "center", bold: true, fill: { color: VE }, color: DO } },
      { text: "Sim — Escolhido", options: { align: "center", bold: true, fill: { color: VE }, color: "52B788" } }
    ],
  ];
  s.addTable([hdr, ...trows], {
    x: 0.25, y: 0.85, w: 9.5, h: 3.4,
    fontSize: 12, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" },
    colW: [2.6, 1.55, 2.0, 1.55, 1.8],
    rowH: [0.5, 0.54, 0.54, 0.54, 0.54, 0.64],
  });

  s.addText("*YOLO é um detector de objetos (bounding box) — incompatível com classificação de folha única.", {
    x: 0.25, y: 4.32, w: 9.5, h: 0.28, fontSize: 9.5, italic: true, color: "6B7280" });

  s.addShape("rect", { x: 0.25, y: 4.65, w: 9.5, h: 0.55, fill: { color: "F0FFF4" }, line: { color: VC, pt: 1 }, rectRadius: 0.05 });
  s.addText([
    { text: "Depthwise separable convolutions ", options: { bold: true, color: VE, fontSize: 10.5 } },
    { text: "→ 8–9× menos FLOPs vs. convoluções densas  ·  Alpha = 0,35  ·  entrada 96×96×3", options: { color: GT, fontSize: 10.5 } },
    { text: "  →  Arena ESP32-S3: 200 KB / 512 KB (39%)", options: { bold: true, color: GN, fontSize: 10.5 } },
  ], { x: 0.4, y: 4.67, w: 9.2, h: 0.51, valign: "middle" });
}

// ===========================================================================
// SLIDE 9 — TREINAMENTO + QUANTIZAÇÃO (fundido)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Treinamento e Quantização — do Float ao INT8 Embarcado");
  slideNum(s, 9);

  // Esquerda: curvas
  s.addImage({ path: "historico_treino.png", x: 0.25, y: 0.85, w: 5.3, h: 3.6 });
  s.addText("2 fases · 50 épocas · backbone ImageNet · melhor val_acc 97,90% (ép. 46)", {
    x: 0.25, y: 4.5, w: 5.3, h: 0.3, fontSize: 10.5, italic: true, color: GT, align: "center"
  });

  // Direita: 3 números
  const nums = [
    { v: "62,0%",  l: "INT8 sem calibração", sub: "Edge Impulse (1ª tentativa)", c: RD },
    { v: "98,13%", l: "modelo float (teto)",  sub: "TensorFlow local — só PC",    c: VM },
    { v: "95,76%", l: "INT8 embarcado",       sub: "TF local + calibração — vai pro ESP32", c: GN }
  ];
  nums.forEach((n, i) => {
    const y = 0.95 + i * 1.12;
    s.addShape("rect", { x: 5.7, y, w: 4.05, h: 1.0, fill: { color: BR }, line: { color: n.c, pt: 1.5 }, rectRadius: 0.07, shadow: makeShadow() });
    s.addText(n.v, { x: 5.75, y: y + 0.05, w: 1.55, h: 0.9, fontSize: 24, bold: true, color: n.c, align: "center", valign: "middle" });
    s.addText(n.l, { x: 7.35, y: y + 0.1, w: 2.35, h: 0.4, fontSize: 11.5, bold: true, color: VE, valign: "middle" });
    s.addText(n.sub, { x: 7.35, y: y + 0.5, w: 2.35, h: 0.45, fontSize: 10, color: "6B7280", italic: true, valign: "middle" });
  });

  // Rodapé: frase-chave (não invade número da página)
  s.addShape("rect", { x: 0.25, y: 4.85, w: 8.85, h: 0.45, fill: { color: VE }, line: { color: DO, pt: 1 }, rectRadius: 0.05 });
  s.addText([
    { text: "Calibração: ", options: { bold: true, color: DO, fontSize: 10.5 } },
    { text: "perda de quantização caiu de 30,5 pp para 2,37 pp. O modelo embarcado entrega 95,76% — não os 98,13% do float que só roda no PC.", options: { color: BR, fontSize: 10.5 } }
  ], { x: 0.35, y: 4.87, w: 8.65, h: 0.41, valign: "middle" });
}

// ===========================================================================
// SLIDE 9 — MATRIZ DE CONFUSÃO (texto ajustado conforme matriz)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Matriz de Confusão — Modelo INT8 (95,76% em Laboratório)");
  slideNum(s, 10);
  s.addImage({ path: "matriz_confusao_int8.png", x: 0.3, y: 0.85, w: 5.65, h: 4.4 });
  card(s, 6.15, 0.85, 3.6, 4.4, VM, VC, "Leitura da matriz");
  s.addText([
    { text: "Test set: 2.618 / 2.734 corretas\n\n", options: { bold: true, color: GN, fontSize: 13 } },
    { text: "Classes quase perfeitas (≥99%):\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Mancha bacteriana, vira-cabeça, saudável\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Classe mais difícil:\n", options: { bold: true, color: "92400E", fontSize: 12.5 } },
    { text: "Pinta-preta (83%) — confundida principalmente com septoriose, requeima e mancha bacteriana.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Padrão: ", options: { bold: true, color: VE, fontSize: 12 } },
    { text: "doenças com lesões necróticas (manchas escuras) tendem a se confundir entre si.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Resultado em laboratório: muito bom. Mas e em campo real?", options: { bold: true, color: RD, fontSize: 12, italic: true } }
  ], { x: 6.33, y: 1.45, w: 3.25, h: 3.6, valign: "top" });
}

// ===========================================================================
// SLIDE 10 — A SURPRESA: GAP LAB–CAMPO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "A Surpresa: o Gap Laboratório–Campo");
  slideNum(s, 11);
  s.addShape("rect", { x: 0.4, y: 0.95, w: 3.0, h: 1.6, fill: { color: BR }, line: { color: GN, pt: 1.5 }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText("Em laboratório", { x: 0.4, y: 1.0, w: 3.0, h: 0.4, fontSize: 12.5, bold: true, color: VE, align: "center" });
  s.addText("95,76%", { x: 0.4, y: 1.35, w: 3.0, h: 0.85, fontSize: 38, bold: true, color: GN, align: "center", valign: "middle" });
  s.addText("PlantVillage test set", { x: 0.4, y: 2.18, w: 3.0, h: 0.32, fontSize: 11, color: "6B7280", italic: true, align: "center" });
  s.addText("→", { x: 3.35, y: 1.0, w: 0.55, h: 1.5, fontSize: 50, color: VE, align: "center", valign: "middle", bold: true });
  s.addShape("rect", { x: 3.9, y: 0.85, w: 5.75, h: 1.8, fill: { color: "FEF2F2" }, line: { color: RD, pt: 2 }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText("Em campo real (PlantDoc)", { x: 3.9, y: 0.9, w: 5.75, h: 0.4, fontSize: 13, bold: true, color: RD, align: "center" });
  s.addText("20,77%", { x: 3.9, y: 1.25, w: 5.75, h: 1.0, fontSize: 64, bold: true, color: RD, align: "center", valign: "middle" });
  s.addText("− 75 pp em uma transição de domínio", { x: 3.9, y: 2.28, w: 5.75, h: 0.32, fontSize: 12, color: "7F1D1D", italic: true, align: "center", bold: true });
  s.addShape("rect", { x: 0.4, y: 2.85, w: 9.25, h: 2.4, fill: { color: VE }, line: { color: DO, pt: 1.5 }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText("Não estamos sozinhos — a literatura já descrevia esse fenômeno:", {
    x: 0.6, y: 2.95, w: 8.9, h: 0.4, fontSize: 14, bold: true, color: DO, valign: "middle" });
  const lit = [
    { autor: "Mohanty (2016)", n: "99,35%", d: "PlantVillage — lab" },
    { autor: "Singh (2020)",   n: "~31%",   d: "PlantDoc — sem adaptação" },
    { autor: "Xu (2024)",      n: "−29 a −58 pp", d: "revisão de 42 trabalhos" }
  ];
  lit.forEach((l, i) => {
    const x = 0.7 + i * 3.0;
    s.addShape("rect", { x, y: 3.5, w: 2.7, h: 1.55, fill: { color: VM }, line: { color: DO, pt: 1 }, rectRadius: 0.06 });
    s.addText(l.autor, { x, y: 3.55, w: 2.7, h: 0.32, fontSize: 12, bold: true, color: DO, align: "center" });
    s.addText(l.n, { x, y: 3.85, w: 2.7, h: 0.55, fontSize: 18, bold: true, color: BR, align: "center", valign: "middle" });
    s.addText(l.d, { x: x + 0.1, y: 4.45, w: 2.5, h: 0.5, fontSize: 10.5, color: "B7E4C7", align: "center", italic: true });
  });
}

// ===========================================================================
// SLIDE 11 — OS 5 EXPERIMENTOS (tabela 4 colunas)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "A Jornada para Fechar o Gap — 5 Experimentos");
  slideNum(s, 12);
  const hdr = [
    { text: "Exp", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "Estratégia", options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "PlantVillage", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "PlantDoc", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "Tomato-V.", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "Daffodil", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }
  ];
  const rows = [
    [{ text: "A", options: { align: "center" } }, "Edge Impulse — sem calibração INT8",
      { text: "62,0% (INT8)", options: { color: RD, bold: true, align: "center" } },
      { text: "—", options: { align: "center" } }, { text: "—", options: { align: "center" } }, { text: "—", options: { align: "center" } }],
    [{ text: "B", options: { align: "center" } }, "TF local — calibração INT8 (50 batches)",
      { text: "95,76% INT8", options: { align: "center", bold: true } },
      { text: "20,77%", options: { align: "center" } }, { text: "—", options: { align: "center" } }, { text: "—", options: { align: "center" } }],
    [{ text: "C", options: { align: "center" } }, "Exp B + augmentation sintética (rembg)",
      { text: "96,20%", options: { align: "center" } },
      { text: "20,24% ❌", options: { align: "center", color: RD, bold: true } }, { text: "—", options: { align: "center" } }, { text: "—", options: { align: "center" } }],
    [{ text: "D", options: { align: "center" } }, "Exp B + fine-tuning com dados reais",
      { text: "97,55%", options: { align: "center" } },
      { text: "30,43% ✅", options: { align: "center", color: GN, bold: true } },
      { text: "11,52%", options: { align: "center" } }, { text: "—", options: { align: "center" } }],
    [{ text: "E ★", options: { align: "center", bold: true, color: DO, fill: { color: VE } } },
      { text: "Exp D + Focal Loss γ=2 ← MODELO FINAL", options: { bold: true, fill: { color: VE }, color: BR } },
      { text: "98,43% float", options: { align: "center", bold: true, fill: { color: VE }, color: DO } },
      { text: "30,43% ✅", options: { align: "center", bold: true, fill: { color: VE }, color: VC } },
      { text: "27,65%", options: { align: "center", bold: true, fill: { color: VE }, color: VC } },
      { text: "18,13%", options: { align: "center", bold: true, fill: { color: VE }, color: VC } }]
  ];
  s.addTable([hdr, ...rows], { x: 0.25, y: 0.85, w: 9.5, h: 3.6, fontSize: 11.5, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" }, colW: [0.55, 3.65, 1.6, 1.4, 1.15, 1.15], rowH: 0.6 });
  s.addShape("rect", { x: 0.25, y: 4.6, w: 9.5, h: 0.6, fill: { color: "FFFBEB" }, line: { color: DO, pt: 1.5 }, rectRadius: 0.06 });
  s.addText([
    { text: "−30,5 pp", options: { bold: true, color: RD } }, { text: " sem calibração   ", options: { color: GT } },
    { text: "+34 pp", options: { bold: true, color: GN } }, { text: " com calibração (Exp B)   ", options: { color: GT } },
    { text: "+10 pp", options: { bold: true, color: GN } }, { text: " em campo (Exp D)   ", options: { color: GT } },
    { text: "+16 pp", options: { bold: true, color: GN } }, { text: " com Focal Loss (Exp E)", options: { color: GT } }
  ], { x: 0.4, y: 4.63, w: 9.2, h: 0.54, fontSize: 12, valign: "middle" });
}

// ===========================================================================
// SLIDE 12 — EXP C: RESULTADO NEGATIVO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Exp. C — Resultado Negativo (Augmentation Sintética)");
  slideNum(s, 13);
  card(s, 0.25, 0.85, 4.6, 4.4, VM2, VC, "O que tentamos");
  s.addText([
    { text: "Hipótese:\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "se o modelo aprende o fundo cinza, trocar o fundo deveria forçá-lo a olhar a lesão.\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Método:\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "rembg (U2-Net) remove o fundo de cada folha e recompõe sobre fundos naturais do PlantDoc.\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Escala:\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "177.698 composições sintéticas geradas.", options: { color: GT, fontSize: 12.5 } }
  ], { x: 0.45, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
  card(s, 5.15, 0.85, 4.6, 4.4, "B91C1C", "FCA5A5", "O que aconteceu");
  s.addText([
    { text: "+0 pp em campo\n", options: { bold: true, color: RD, fontSize: 16 } },
    { text: "20,24% vs. 20,77% do Exp. B\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Classe saudável: 0,0% em campo\n", options: { bold: true, color: RD, fontSize: 12.5 } },
    { text: "o modelo nunca acerta folha saudável real.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Por quê:\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "artefatos de borda e iluminação inconsistente — o domínio sintético não captura a distribuição real.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Lição: ", options: { bold: true, color: GN, fontSize: 12.5 } },
    { text: "síntese não substitui dado de campo. Resultado negativo reprodutível.", options: { color: GT, fontSize: 12 } }
  ], { x: 5.35, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
}

// ===========================================================================
// SLIDE 13 — EXP D e E
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Exp. D e E — O Que Realmente Funcionou");
  slideNum(s, 14);
  card(s, 0.25, 0.85, 4.6, 4.4, VM, VC, "Exp. D — Fine-tuning real");
  s.addText([
    { text: "+10 pp em campo\n", options: { bold: true, color: GN, fontSize: 18 } },
    { text: "20,77% → 30,43% (PlantDoc)\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Como:\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "677 imagens reais do PlantDoc/train (repetidas 10×), avaliadas em 69 imagens nunca vistas.\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Conclusão:\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "o fator limitante é o volume de dados de campo, não o método de treinamento.", options: { color: GT, fontSize: 12.5 } }
  ], { x: 0.45, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
  card(s, 5.15, 0.85, 4.6, 4.4, VE, DO, "Exp. E — Focal Loss (final)");
  s.addText([
    { text: "+16 pp no Tomato-Village\n", options: { bold: true, color: GN, fontSize: 16 } },
    { text: "11,52% → 27,65% (Índia)\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Como:\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Focal Loss (γ=2) reduz o peso de exemplos fáceis — as imagens de laboratório com fundo cinza.\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Efeito:\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "força o modelo a focar nas features diagnósticas da lesão. É o modelo final embarcado.", options: { color: GT, fontSize: 12.5 } }
  ], { x: 5.35, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
}

// ===========================================================================
// SLIDE 14 — GAP GEOGRÁFICO + COLAPSO DE CLASSE
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Gap Geográfico e Colapso de Classe");
  slideNum(s, 15);
  card(s, 0.25, 0.85, 4.6, 4.4, VM, VC, "Especificidade geográfica");
  s.addText([
    { text: "A acurácia cai com a distância do PlantDoc:\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "EUA/Europa   30,43%\n", options: { bold: true, color: GN, fontSize: 14 } },
    { text: "Índia            27,65%\n", options: { bold: true, color: "92400E", fontSize: 14 } },
    { text: "Bangladesh   18,13%\n\n", options: { bold: true, color: RD, fontSize: 14 } },
    { text: "Confirma Barbedo (2019): variedades locais, iluminação tropical e estágio fenológico distinto degradam o desempenho.", options: { color: GT, fontSize: 12 } }
  ], { x: 0.45, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
  card(s, 5.15, 0.85, 4.6, 4.4, "B91C1C", "FCA5A5", "Colapso de classe");
  s.addText([
    { text: "Exp. D no Tomato-Village (Índia):\n\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "73%\n", options: { bold: true, color: RD, fontSize: 30, align: "center" } },
    { text: "das folhas saudáveis indianas foram classificadas como D02_septoriose.\n\n", options: { color: GT, fontSize: 12.5, align: "center" } },
    { text: "Padrão típico de colapso sob shift de domínio extremo — o modelo \"despeja\" tudo numa classe. Parcialmente mitigado no Exp. E com Focal Loss.", options: { color: GT, fontSize: 12 } }
  ], { x: 5.35, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
}

// ===========================================================================
// SLIDE 15 — PIVÔ: ARQUITETURA (modelo pronto, onde rodar?)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Modelo Pronto. Onde Rodar?");
  slideNum(s, 16);
  s.addShape("rect", { x: 3.15, y: 2.45, w: 3.7, h: 1.1, fill: { color: VE }, line: { color: DO, pt: 2 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText("MobileNetV2 INT8\n638 KB · 96×96 · 10 classes · T=0,25", { x: 3.15, y: 2.45, w: 3.7, h: 1.1, fontSize: 12, bold: true, color: DO, align: "center", valign: "middle" });
  const paths = [
    { x: 0.15, bColor: "1D4ED8", label: "① Edge", sub: "ESP32-S3 N16R8", items: "692 ms  •  offline\nMQTT/TLS → HiveMQ\nSem internet — 100% local", res: "692 ms" },
    { x: 3.55, bColor: VM2, label: "② Mobile", sub: "Android on-device", items: "~200–400 ms  •  offline\ntflite_flutter 0.12.1\nToggle Edge ↔ Cloud no app", res: "~200–400 ms" },
    { x: 6.95, bColor: "7E22CE", label: "③ Cloud", sub: "Flutter + Django", items: "306 ms  •  HTTPS\nAPI Railway + PostgreSQL\nPipeline completo validado", res: "306 ms" }
  ];
  paths.forEach(p => {
    s.addShape("rect", { x: p.x, y: 0.85, w: 2.85, h: 0.62, fill: { color: p.bColor }, line: { color: p.bColor }, rectRadius: 0.06 });
    s.addText(`${p.label}  —  ${p.sub}`, { x: p.x, y: 0.85, w: 2.85, h: 0.62, fontSize: 12, bold: true, color: BR, align: "center", valign: "middle" });
    s.addShape("rect", { x: p.x, y: 1.52, w: 2.85, h: 0.88, fill: { color: BR }, line: { color: p.bColor, pt: 1 }, rectRadius: 0.06 });
    s.addText(p.items, { x: p.x + 0.12, y: 1.52, w: 2.65, h: 0.88, fontSize: 11, color: GT, valign: "middle" });
    s.addText("▼", { x: p.x + 1.3, y: 2.4, w: 0.3, h: 0.2, fontSize: 11, color: "9CA3AF", align: "center" });
    s.addShape("rect", { x: p.x, y: 3.62, w: 2.85, h: 0.6, fill: { color: p.bColor }, line: { color: p.bColor }, rectRadius: 0.06 });
    s.addText(p.res, { x: p.x, y: 3.62, w: 2.85, h: 0.6, fontSize: 15, bold: true, color: BR, align: "center", valign: "middle" });
    s.addText("▲", { x: p.x + 1.3, y: 3.3, w: 0.3, h: 0.2, fontSize: 11, color: "9CA3AF", align: "center" });
  });
  // Nota pivô câmera
  s.addShape("rect", { x: 0.3, y: 4.4, w: 9.4, h: 0.55, fill: { color: "FFFBEB" }, line: { color: DO, pt: 1 }, rectRadius: 0.04 });
  s.addText([
    { text: "Pivô de engenharia: ", options: { bold: true, color: "92400E", fontSize: 10.5 } },
    { text: "plano original era ESP32-S3 + câmera OV5640, 100% autônomo. Câmera ainda não integrada (Sprint 2). Adaptação: smartphone como sensor no caminho ②. Mesmo modelo INT8, mais flexibilidade.", options: { color: GT, fontSize: 10.5 } }
  ], { x: 0.45, y: 4.42, w: 9.1, h: 0.51, valign: "middle" });
}

// ===========================================================================
// SLIDE 16 — COMPARATIVO + LATÊNCIA
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Comparativo Edge / Mobile / Cloud");
  slideNum(s, 17);
  const hdr = [
    { text: "Aspecto", options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "① Edge", options: { bold: true, color: BR, fill: { color: "1D4ED8" }, align: "center" } },
    { text: "② Mobile", options: { bold: true, color: BR, fill: { color: VM2 }, align: "center" } },
    { text: "③ Cloud", options: { bold: true, color: BR, fill: { color: "7E22CE" }, align: "center" } }
  ];
  const chk = { color: GN, bold: true, align: "center" };
  const crs = { color: RD, bold: true, align: "center" };
  const rows = [
    ["Latência CNN", { text: "692 ms (±1)", options: { align: "center", bold: true } },
      { text: "~200–400 ms", options: { align: "center" } }, { text: "306 ms", options: { align: "center" } }],
    ["Funciona offline", { text: "✅  Sim", options: chk }, { text: "✅  Sim", options: chk }, { text: "❌  Não", options: crs }],
    ["Infraestrutura", { text: "ESP32-S3 ~R$ 80", options: { align: "center" } }, { text: "App no celular do produtor", options: { align: "center" } }, { text: "Railway (free tier)", options: { align: "center" } }],
    ["Status atual", { text: "✅ Validado\n10/10 corretas", options: chk }, { text: "✅ Implementado", options: chk }, { text: "✅ Produção\n(Railway)", options: chk }]
  ];
  s.addTable([hdr, ...rows], { x: 0.25, y: 0.85, w: 9.5, h: 3.2, fontSize: 13, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" }, colW: [2.6, 2.3, 2.3, 2.3], rowH: [0.5, 0.55, 0.6, 0.6, 0.8] });

  // Destaque latência ESP32
  s.addShape("rect", { x: 0.25, y: 4.2, w: 9.5, h: 1.1, fill: { color: BR }, line: { color: "1D4ED8", pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText("692 ms", { x: 0.4, y: 4.3, w: 2.4, h: 0.9, fontSize: 36, bold: true, color: "1D4ED8", align: "center", valign: "middle" });
  s.addShape("line", { x: 2.85, y: 4.4, w: 0, h: 0.7, line: { color: "1D4ED8", width: 1 } });
  s.addText([
    { text: "Latência real do ESP32 — determinística, ±1 ms\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "10/10 imagens corretas no benchmark · 2× mais rápida que a estimativa do Edge Impulse · imperceptível em campo (produtor leva 2–5 s para posicionar a folha).", options: { color: GT, fontSize: 11.5 } }
  ], { x: 3.0, y: 4.25, w: 6.6, h: 1.0, valign: "middle" });
}

// ===========================================================================
// SLIDE 19 — O QUE CONSTRUÍMOS (storytelling / pipeline integrado)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "O Que Construímos — Da Decisão ao Sistema Integrado");
  slideNum(s, 18);

  const comps = [
    { color: "1D4ED8", label: "Firmware\nESP32-S3", items: [
      "PlatformIO / ESP-IDF 5.x",
      "MQTT QoS 1 · TLS 1.3",
      "DHT22 + sensor de solo",
      "Arena 200 KB · 692 ms",
    ]},
    { color: VM2, label: "Broker\nMQTT", items: [
      "HiveMQ Cloud",
      "Porta 8883 (TLS)",
      "JSON payload",
      "Pub/Sub em tempo real",
    ]},
    { color: VE, label: "Backend\nDjango REST", items: [
      "12 endpoints REST",
      "JWT + refresh token",
      "MQTT listener",
      "PostgreSQL · Railway",
    ]},
    { color: "7E22CE", label: "App\nFlutter", items: [
      "10+ telas implementadas",
      "Drift SQLite offline",
      "tflite_flutter 0.12.1",
      "Sync offline → online",
    ]},
  ];

  const cw = 2.2, ch = 3.5, cy = 0.9, cgap = 0.2;
  comps.forEach((c, i) => {
    const cx = 0.2 + i * (cw + cgap);
    if (i > 0) {
      s.addText("→", { x: cx - cgap, y: cy + ch / 2 - 0.3, w: cgap, h: 0.6,
        fontSize: 22, color: DO, bold: true, align: "center", valign: "middle" });
    }
    s.addShape("rect", { x: cx, y: cy, w: cw, h: ch, fill: { color: BR },
      line: { color: c.color, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
    s.addShape("rect", { x: cx, y: cy, w: cw, h: 0.68, fill: { color: c.color }, line: { color: c.color } });
    s.addShape("rect", { x: cx, y: cy + 0.46, w: cw, h: 0.24, fill: { color: c.color }, line: { color: c.color } });
    s.addText(c.label, { x: cx, y: cy, w: cw, h: 0.68, fontSize: 12, bold: true, color: BR,
      align: "center", valign: "middle" });
    c.items.forEach((item, j) => {
      s.addText("• " + item, { x: cx + 0.12, y: cy + 0.8 + j * 0.62, w: cw - 0.2, h: 0.6,
        fontSize: 11.5, color: GT, valign: "middle" });
    });
  });

  // Faixa inferior: telas do app
  s.addShape("rect", { x: 0.2, y: 4.5, w: 9.6, h: 0.68, fill: { color: VE },
    line: { color: DO, pt: 1 }, rectRadius: 0.06 });
  s.addText([
    { text: "Modelo no celular: ", options: { bold: true, color: DO, fontSize: 11 } },
    { text: "ceres_mobilenetv2_int8.tflite  ·  638 KB  ·  tflite_flutter 0.12.1  ·  ", options: { color: BR, fontSize: 11 } },
    { text: "mesmo arquivo do ESP32-S3", options: { bold: true, color: VC, fontSize: 11 } },
    { text: "  ·  inferência offline ~200–400 ms  ·  sem câmera dedicada", options: { color: BR, fontSize: 11 } },
  ], { x: 0.35, y: 4.52, w: 9.3, h: 0.64, valign: "middle" });
}

// ===========================================================================
// SLIDE 20 — APP + HARDWARE
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "O Sistema em Funcionamento");
  slideNum(s, 19);
  s.addImage({ path: "app_iot.jpg", x: 0.5, y: 0.92, w: 1.85, h: 4.0 });
  s.addText("App Flutter — tela IoT", { x: 0.35, y: 4.95, w: 2.15, h: 0.3, fontSize: 10.5, italic: true, color: "6B7280", align: "center" });
  s.addImage({ path: "hardware_setup.jpg", x: 2.7, y: 0.92, w: 2.25, h: 4.0 });
  s.addText("ESP32-S3 + DHT22 + sensor de solo", { x: 2.55, y: 4.95, w: 2.55, h: 0.3, fontSize: 10.5, italic: true, color: "6B7280", align: "center" });
  card(s, 5.35, 0.92, 4.4, 4.0, VM, VC, "O que está em produção");
  s.addText([
    { text: "Decisão de engenharia\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Plano original: ESP32-S3 + câmera OV5640, totalmente autônomo. Câmera pendente (Sprint 2) — ESP32 foi adaptado para coletar sensores e publicar via MQTT.\n\n", options: { color: GT, fontSize: 11.5, italic: true } },
    { text: "Sensoriamento em tempo real\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Temperatura · Umidade do ar · Umidade do solo via MQTT (QoS 1). Tela: 29,5 °C · 49% · 34%, status ONLINE.\n\n", options: { color: GT, fontSize: 11.5 } },
    { text: "Pipeline integrado\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Django persiste cada evento com GPS; app sincroniza diagnósticos offline → online ao reconectar.", options: { color: GT, fontSize: 11.5 } }
  ], { x: 5.55, y: 1.5, w: 4.05, h: 3.3, valign: "top" });
}

// ===========================================================================
// SLIDE 21 — DEMONSTRAÇÃO (vídeo CENTRAL + descrição esquerda + QR direita)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Demonstração e Recursos");
  slideNum(s, 20);

  // ESQUERDA — descrição do vídeo
  card(s, 0.25, 0.95, 3.05, 4.2, VM, VC, "O que o vídeo mostra");
  s.addText([
    { text: "1. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Captura da folha pela câmera do app\n\n", options: { color: GT, fontSize: 12 } },
    { text: "2. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Diagnóstico INT8 (Edge / Mobile / Cloud)\n\n", options: { color: GT, fontSize: 12 } },
    { text: "3. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Publicação via MQTT do ESP32-S3\n\n", options: { color: GT, fontSize: 12 } },
    { text: "4. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Histórico e mapa de eventos com GPS", options: { color: GT, fontSize: 12 } }
  ], { x: 0.45, y: 1.55, w: 2.7, h: 3.5, valign: "top" });

  // MEIO — vídeo (destaque central)
  s.addMedia({ type: "video", path: "demo_ceres_1.5x.mp4", x: 3.5, y: 0.95, w: 3.0, h: 4.2 });
  s.addText("▶  Vídeo demonstrativo (1,5×)", { x: 3.5, y: 5.0, w: 3.0, h: 0.3, fontSize: 10.5, italic: true, color: "6B7280", align: "center" });

  // DIREITA — QR
  s.addShape("rect", { x: 6.7, y: 0.95, w: 3.05, h: 4.2, fill: { color: BR }, line: { color: DO, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addImage({ path: "qrcode_drive.png", x: 6.95, y: 1.25, w: 2.55, h: 2.69 });
  s.addText([
    { text: "Baixe e teste\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "APK + imagens de teste\ngithub.com/Namem/extensao2", options: { color: GT, fontSize: 11.5 } }
  ], { x: 6.8, y: 4.05, w: 2.85, h: 1.0, align: "center", valign: "top" });
}

// ===========================================================================
// SLIDE 22 — CONCLUSÃO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Conclusao");
  slideNum(s, 21);

  // Manchete central
  s.addShape("rect", { x: 0.25, y: 0.85, w: 9.5, h: 0.62, fill: { color: VE }, line: { color: DO, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText("TinyML agricola funciona — o gargalo e o dado, nao o hardware", {
    x: 0.4, y: 0.87, w: 9.2, h: 0.58,
    fontSize: 17, bold: true, color: DO, align: "center", valign: "middle",
  });

  // 3 cards de conclusao
  const cards = [
    {
      icon: "① Viabilidade",
      titulo: "Prova de conceito concluida",
      corpo: "MobileNetV2 INT8 roda no ESP32-S3 em 692 ms com modelo de 638 KB e ~R$ 80 de hardware. Diagnostica 10 doencas sem internet.",
      cor: VM,
    },
    {
      icon: "② Gap lab-campo",
      titulo: "Fenomeno estrutural, nao falha do modelo",
      corpo: "Sem adaptacao: 95,76% em laboratorio cai para 18–30% em campo. Documentado na literatura (Xu 2024, Singh 2020) — nao e particular deste trabalho.",
      cor: "B45309",
    },
    {
      icon: "③ O gargalo real",
      titulo: "Falta um dataset brasileiro",
      corpo: "A ausencia de imagens com variedades locais, iluminacao tropical e estagios fenologicos reais e o fator limitante. Nenhum metodo sintetico supriu essa lacuna (Exp C).",
      cor: RD,
    },
  ];

  const cw = 2.95, ch = 3.55, cy = 1.62, gap = 0.275;
  cards.forEach((c, i) => {
    const cx = 0.25 + i * (cw + gap);
    s.addShape("rect", { x: cx, y: cy, w: cw, h: ch, fill: { color: BR }, line: { color: c.cor, pt: 1.5 }, rectRadius: 0.09, shadow: makeShadow() });
    // header do card
    s.addShape("rect", { x: cx, y: cy, w: cw, h: 0.54, fill: { color: c.cor }, line: { color: c.cor } });
    s.addShape("rect", { x: cx, y: cy + 0.36, w: cw, h: 0.2, fill: { color: c.cor }, line: { color: c.cor } });
    s.addText(c.icon, { x: cx, y: cy, w: cw, h: 0.54, fontSize: 13, bold: true, color: BR, align: "center", valign: "middle" });
    // titulo e corpo
    s.addText(c.titulo, { x: cx + 0.18, y: cy + 0.65, w: cw - 0.32, h: 0.52, fontSize: 12.5, bold: true, color: VE, valign: "top" });
    s.addText(c.corpo,  { x: cx + 0.18, y: cy + 1.22, w: cw - 0.32, h: 1.85, fontSize: 11.5, color: GT, valign: "top" });
  });

}

// ===========================================================================
// SLIDE 23 — TRABALHOS FUTUROS (4 cards limpos, sem badges)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Trabalhos Futuros");
  slideNum(s, 22);
  const items = [
    { t: "Dataset brasileiro de campo", d: "Coleta com pequenos produtores rurais, com variedades locais e condições reais — o fator que mais limita a generalização do modelo." },
    { t: "Integração da câmera OV5640", d: "Validar o pipeline de captura completo no ESP32-S3 e medir a latência com sensor real, fechando o ciclo embarcado." },
    { t: "Validação com produtores reais", d: "Levar o sistema a propriedades agrícolas e avaliar usabilidade, acurácia em condições reais e adoção pelo pequeno produtor." },
    { t: "Expansão para outras culturas", d: "Generalizar o pipeline para soja, milho ou café — outras culturas brasileiras com forte impacto econômico." }
  ];
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.3 + col * 4.85, y = 0.95 + row * 2.2;
    s.addShape("rect", { x, y, w: 4.55, h: 2.0, fill: { color: BR }, line: { color: VC, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
    s.addShape("rect", { x, y, w: 4.55, h: 0.5, fill: { color: VE }, line: { color: VE } });
    s.addShape("rect", { x, y: y + 0.32, w: 4.55, h: 0.22, fill: { color: VE }, line: { color: VE } });
    s.addText(it.t, { x: x + 0.15, y, w: 4.25, h: 0.5, fontSize: 14, bold: true, color: DO, valign: "middle" });
    s.addText(it.d, { x: x + 0.2, y: y + 0.6, w: 4.15, h: 1.3, fontSize: 12.5, color: GT, valign: "top" });
  });
}

// ===========================================================================
// SLIDE 24 — OBRIGADO
// ===========================================================================
{
  const s = pres.addSlide();
  s.background = { color: VE };
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.18, fill: { color: DO }, line: { color: DO } });
  s.addShape("rect", { x: 0, y: 5.44, w: 10, h: 0.18, fill: { color: DO }, line: { color: DO } });
  s.addText("Obrigado!", { x: 0, y: 1.5, w: 10, h: 1.0, fontSize: 48, bold: true, color: BR, align: "center" });
  s.addText("Perguntas?", { x: 0, y: 2.55, w: 10, h: 0.7, fontSize: 26, color: DO, align: "center", bold: true });
  s.addShape("rect", { x: 2.0, y: 3.7, w: 6.0, h: 0.6, fill: { color: VM2 }, line: { color: DO, pt: 1.5 }, rectRadius: 0.07 });
  s.addText("github.com/Namem/extensao2", { x: 2.0, y: 3.7, w: 6.0, h: 0.6, fontSize: 14, color: DO, align: "center", valign: "middle", bold: true });
  s.addText("Namem Rachid Jaudy Neto  ·  IFMT Cuiabá  ·  Junho 2026", { x: 0, y: 4.5, w: 10, h: 0.4, fontSize: 13, color: "B7E4C7", align: "center" });
}

// ---------------------------------------------------------------------------
pres.writeFile({ fileName: "ceres_diagnostico_psi.pptx" })
  .then(() => console.log(`✅ Slides gerados (${TOTAL}): ceres_diagnostico_psi.pptx`))
  .catch(e  => { console.error("ERRO:", e); process.exit(1); });
