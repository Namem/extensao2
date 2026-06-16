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
const RD  = "B91C1C";   // vermelho
const GN  = "166534";   // verde escuro positivo

const TOTAL = 24;

const makeShadow = () => ({
  type: "outer", blur: 5, offset: 2, angle: 135, color: "000000", opacity: 0.14
});

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

// Caixa com header colorido + corpo
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
  s.addText("Ceres Diagnóstico", { x: 0.4, y: 0.7, w: 8.0, h: 1.0,
    fontSize: 42, fontFace: "Calibri", bold: true, color: BR, align: "left" });
  s.addShape("rect", { x: 0.4, y: 1.65, w: 7.5, h: 0.05, fill: { color: DO }, line: { color: DO } });
  s.addText("Sistema TinyML Embarcado para\nDetecção de Doenças em Tomateiro", {
    x: 0.4, y: 1.75, w: 8.5, h: 1.0, fontSize: 21, fontFace: "Calibri", color: BR, align: "left" });
  s.addShape("rect", { x: 0.4, y: 2.95, w: 6.8, h: 1.65,
    fill: { color: VM }, line: { color: VC, pt: 1 }, rectRadius: 0.08, shadow: makeShadow() });
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
    ["1", "Problema e o gap laboratório-campo"],
    ["2", "Objetivos e contribuições"],
    ["3", "Arquitetura: três caminhos de inferência"],
    ["4", "Dataset e pipeline de treinamento"],
    ["5", "Quantização INT8: float vs. embarcado"],
    ["6", "Os cinco experimentos (A → E)"],
    ["7", "Validação em campo: três datasets"],
    ["8", "Comparativo e latência no ESP32-S3"],
    ["9", "Conclusão e trabalhos futuros"]
  ];
  ag.forEach((it, i) => {
    const col = i < 5 ? 0 : 1;
    const row = col === 0 ? i : i - 5;
    const x = col === 0 ? 0.5 : 5.15;
    const y = 1.0 + row * 0.82;
    s.addShape("rect", { x, y, w: 0.5, h: 0.5, fill: { color: VE }, line: { color: DO, pt: 1 }, rectRadius: 0.05 });
    s.addText(it[0], { x, y, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: DO, align: "center", valign: "middle" });
    s.addText(it[1], { x: x + 0.62, y: y - 0.02, w: 3.85, h: 0.54, fontSize: 13.5, color: GT, valign: "middle" });
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
    { text: "Sorriso-MT concentra grande parte da produção de tomate de Mato Grosso. A maioria dos produtores é de pequeno porte, sem acesso regular a assistência técnica. O Ceres oferece diagnóstico em campo, offline, a menos de R$ 80 em hardware.", options: { fontSize: 13, color: VE } }
  ], { x: 0.55, y: 3.33, w: 8.9, h: 1.9, valign: "middle" });
}

// ===========================================================================
// SLIDE 4 — O DESAFIO CENTRAL: GAP LAB-CAMPO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "O Desafio Central: Gap Laboratório-Campo");
  slideNum(s, 4);

  const steps = [
    { t: "Mohanty et al. (2016)", v: "99,35%", sub: "PlantVillage — laboratório\n(fundo uniforme, luz controlada)", c: GN },
    { t: "Singh et al. (2020)",   v: "≈31%",   sub: "PlantDoc — campo real\nsem adaptação de domínio", c: "92400E" },
    { t: "Xu et al. (2024)",      v: "−29 a −58 pp", sub: "revisão de 42 trabalhos\nqueda ao ir p/ campo", c: RD }
  ];
  steps.forEach((st, i) => {
    const x = 0.35 + i * 3.18;
    s.addShape("rect", { x, y: 1.0, w: 2.95, h: 1.95, fill: { color: BR }, line: { color: st.c, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
    s.addText(st.t, { x, y: 1.12, w: 2.95, h: 0.4, fontSize: 12.5, bold: true, color: VE, align: "center" });
    s.addText(st.v, { x, y: 1.5, w: 2.95, h: 0.65, fontSize: 26, bold: true, color: st.c, align: "center", valign: "middle" });
    s.addText(st.sub, { x: x + 0.1, y: 2.2, w: 2.75, h: 0.7, fontSize: 10.5, color: GT, align: "center", valign: "top" });
    if (i < 2) s.addText("→", { x: x + 2.92, y: 1.7, w: 0.3, h: 0.5, fontSize: 22, bold: true, color: VM, align: "center" });
  });

  s.addShape("rect", { x: 0.35, y: 3.35, w: 9.3, h: 1.85, fill: { color: VE }, line: { color: DO, pt: 1.5 }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText([
    { text: "Pergunta de pesquisa\n", options: { bold: true, fontSize: 16, color: DO } },
    { text: "Um modelo TinyML quantizado, pequeno o bastante para caber num microcontrolador de R$ 80, consegue generalizar para imagens de campo real? E quais técnicas reduzem esse gap?", options: { fontSize: 14, color: BR } }
  ], { x: 0.6, y: 3.45, w: 8.8, h: 1.65, valign: "middle" });
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
// SLIDE 6 — ARQUITETURA (visão geral)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Três Caminhos de Inferência — Mesmo Modelo");
  slideNum(s, 6);
  s.addShape("rect", { x: 3.15, y: 2.45, w: 3.7, h: 1.1, fill: { color: VE }, line: { color: DO, pt: 2 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText("MobileNetV2 INT8\n638 KB · 96×96 · 10 classes · T=0,25", { x: 3.15, y: 2.45, w: 3.7, h: 1.1, fontSize: 12, bold: true, color: DO, align: "center", valign: "middle" });
  const paths = [
    { x: 0.15, bColor: "1D4ED8", label: "① Edge", sub: "ESP32-S3 N16R8", items: "692 ms  •  offline\nMQTT/TLS → HiveMQ\nPrivacidade total (LGPD)", res: "692 ms" },
    { x: 3.55, bColor: VM2, label: "② Mobile", sub: "Android on-device", items: "~200–400 ms  •  offline\ntflite_flutter 0.12.1\nToggle Edge ↔ Cloud no app", res: "~200–400 ms *" },
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
  s.addText("* Latência Mobile estimada — não medida empiricamente neste ciclo  |  Caminhos ① e ②: imagem nunca sai do dispositivo", {
    x: 0.3, y: 4.35, w: 9.4, h: 0.55, fontSize: 11, color: "6B7280", italic: true, align: "center",
    fill: { color: "E9F5EE" }, line: { color: "C3E6D1", pt: 1 } });
}

// ===========================================================================
// SLIDE 7 — CAMINHO EDGE (detalhe)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "① Caminho Edge — ESP32-S3 (TinyML)");
  slideNum(s, 7);

  card(s, 0.25, 0.85, 4.6, 4.4, "1D4ED8", "1D4ED8", "Hardware e Runtime");
  s.addText([
    { text: "ESP32-S3 N16R8\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "• Xtensa LX7 dual-core @ 240 MHz\n• Flash 16 MB · PSRAM 8 MB\n• TensorFlow Lite Micro (sem SO)\n• Arena de inferência: 200 KB / 512 KB (39%)\n• Heap livre ~290 KB com WiFi+MQTT\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Imagem carregada como array C\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "(câmera OV5640 = etapa futura — isola a latência da CNN pura)", options: { color: GT, fontSize: 11.5, italic: true } }
  ], { x: 0.45, y: 1.45, w: 4.2, h: 3.7, valign: "top" });

  card(s, 5.15, 0.85, 4.6, 4.4, "1D4ED8", "1D4ED8", "Resultado e Privacidade");
  s.addText([
    { text: "692 ms ", options: { bold: true, color: "1D4ED8", fontSize: 22 } },
    { text: "± 1 ms  (determinístico)\n", options: { color: GT, fontSize: 13 } },
    { text: "10/10 imagens corretas no benchmark\n\n", options: { color: GN, fontSize: 12.5, bold: true } },
    { text: "Publicação do diagnóstico:\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "MQTT QoS 1 sobre TLS → HiveMQ Cloud (porta 8883)\n\n", options: { color: GT, fontSize: 12 } },
    { text: "🔒 A imagem nunca sai do dispositivo\n", options: { bold: true, color: GN, fontSize: 13 } },
    { text: "Privacidade por design — conformidade com a LGPD. Funciona 100% offline.", options: { color: GT, fontSize: 12 } }
  ], { x: 5.35, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
}

// ===========================================================================
// SLIDE 8 — CAMINHOS MOBILE E CLOUD (detalhe)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "② Mobile on-device  e  ③ Cloud");
  slideNum(s, 8);

  card(s, 0.25, 0.85, 4.6, 4.4, VM2, VM2, "② Mobile — Android");
  s.addText([
    { text: "Flutter + tflite_flutter 0.12.1\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "• Modelo INT8 (638 KB) como asset no APK\n• Inferência local, sem servidor\n• ~200–400 ms (estimada *)\n• Funciona offline\n• Mesmo temperature scaling T=0,25\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Toggle Local ↔ Cloud\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "O usuário escolhe o modo na tela de câmera.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "* não medida empiricamente neste ciclo", options: { italic: true, color: "6B7280", fontSize: 10.5 } }
  ], { x: 0.45, y: 1.45, w: 4.2, h: 3.7, valign: "top" });

  card(s, 5.15, 0.85, 4.6, 4.4, "7E22CE", "7E22CE", "③ Cloud — Django REST");
  s.addText([
    { text: "Pipeline em produção (Railway)\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "câmera → app → HTTPS → API → modelo → JSON\n\n", options: { color: GT, fontSize: 11.5, italic: true } },
    { text: "• 306 ms inferência (subprocess TFLite)\n• 2.333 ms end-to-end (servidor dev)\n• Produção (Gunicorn/Linux): < 200 ms estimado\n• Persiste evento + GPS no PostgreSQL\n• Histórico com cache local (Drift/SQLite)\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "⚠️ Imagem é transmitida ao servidor", options: { bold: true, color: "92400E", fontSize: 12 } }
  ], { x: 5.35, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
}

// ===========================================================================
// SLIDE 9 — DATASET E PIPELINE
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Dataset e Pipeline de Treinamento");
  slideNum(s, 9);
  const steps = [
    { label: "PlantVillage\n18.160 imgs\n10 classes", color: VE, tc: BR },
    { label: "Split\n70 / 15 / 15\nseed = 42", color: VM2, tc: BR },
    { label: "Augment.\noffline × 6\n(só treino)", color: VC, tc: BR },
    { label: "88.949 imgs\ntreino final", color: DO, tc: VE }
  ];
  const bw = 2.05, bh = 1.1, by = 0.88, gap = 0.28;
  steps.forEach((st, i) => {
    const bx = 0.2 + i * (bw + gap);
    s.addShape("rect", { x: bx, y: by, w: bw, h: bh, fill: { color: st.color }, line: { color: st.color }, rectRadius: 0.07, shadow: makeShadow() });
    s.addText(st.label, { x: bx, y: by, w: bw, h: bh, fontSize: 12.5, bold: true, color: st.tc, align: "center", valign: "middle" });
    if (i < steps.length - 1) s.addText("→", { x: bx + bw + 0.02, y: by + 0.32, w: gap, h: 0.46, fontSize: 18, color: VM, align: "center", bold: true });
  });
  const tData = [
    [{ text: "Split", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }, { text: "Imagens", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }],
    [{ text: "Treino (augmentado)", options: { bold: true } }, { text: "88.949", options: { align: "center", bold: true } }],
    ["Validação", { text: "2.724", options: { align: "center" } }],
    ["Teste (nunca visto)", { text: "2.734", options: { align: "center" } }]
  ];
  s.addTable(tData, { x: 0.2, y: 2.15, w: 4.5, h: 1.8, fontSize: 13.5, fontFace: "Calibri", border: { pt: 1, color: "D1D5DB" }, colW: [2.9, 1.6], rowH: 0.45 });
  s.addShape("rect", { x: 4.95, y: 2.15, w: 4.8, h: 3.12, fill: { color: "F0FFF4" }, line: { color: VC, pt: 1.5 }, rectRadius: 0.08 });
  s.addText("10 classes do modelo:", { x: 5.1, y: 2.2, w: 4.5, h: 0.38, fontSize: 13, bold: true, color: VE });
  const classes = [
    ["D01  Requeima", "D06  Vira-cabeça"], ["D02  Septoriose", "D06b Mosaico"],
    ["D03  Pinta-preta", "D07  Ácaro"], ["D03b Mancha-alvo", "D09  M. bacteriana"],
    ["D05  Mofo foliar", "Saudável"]
  ];
  classes.forEach((row, i) => {
    const ry = 2.62 + i * 0.48;
    s.addShape("rect", { x: 5.05, y: ry, w: 2.3, h: 0.42, fill: { color: i % 2 === 0 ? "E8F5E9" : BR }, line: { color: "E8F5E9" } });
    s.addText(row[0], { x: 5.12, y: ry, w: 2.2, h: 0.42, fontSize: 11.5, color: GT, valign: "middle", fontFace: "Courier New" });
    s.addShape("rect", { x: 7.38, y: ry, w: 2.3, h: 0.42, fill: { color: i % 2 === 0 ? "E8F5E9" : BR }, line: { color: "E8F5E9" } });
    s.addText(row[1], { x: 7.45, y: ry, w: 2.2, h: 0.42, fontSize: 11.5, color: GT, valign: "middle", fontFace: "Courier New" });
  });
}

// ===========================================================================
// SLIDE 10 — TREINAMENTO EM 2 FASES (curvas)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Treinamento em Duas Fases (Transfer Learning)");
  slideNum(s, 10);
  s.addImage({ path: "historico_treino.png", x: 0.25, y: 0.85, w: 6.2, h: 4.25 });
  card(s, 6.6, 0.85, 3.15, 4.25, VM, VC, "Como foi treinado");
  s.addText([
    { text: "Fase 1 — 10 épocas\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Backbone ImageNet congelado, só a cabeça. LR = 1e-3.\nval_acc ≈ 87,4%\n\n", options: { color: GT, fontSize: 11.5 } },
    { text: "Fase 2 — 40 épocas\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Últimas 30 camadas descongeladas. LR = 5e-4.\nEarlyStopping + ReduceLROnPlateau.\n\n", options: { color: GT, fontSize: 11.5 } },
    { text: "Melhor val_acc: 97,90%\n", options: { bold: true, color: GN, fontSize: 13 } },
    { text: "na época 46 (modelo float).", options: { color: GT, fontSize: 11.5 } }
  ], { x: 6.78, y: 1.45, w: 2.8, h: 3.6, valign: "top" });
}

// ===========================================================================
// SLIDE 11 — QUANTIZAÇÃO INT8: FLOAT vs EMBARCADO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Quantização INT8: Float vs. Modelo Embarcado");
  slideNum(s, 11);

  // Três números-destaque
  const big = [
    { v: "62,0%", t: "INT8 SEM calibração\n(Exp. A) — colapso", c: RD, x: 0.3 },
    { v: "95,76%", t: "INT8 calibrado\n(embarcado no ESP32)", c: GN, x: 3.5 },
    { v: "98,13%", t: "modelo float\n(teto de referência)", c: VM, x: 6.7 }
  ];
  big.forEach(b => {
    s.addShape("rect", { x: b.x, y: 0.9, w: 3.0, h: 1.5, fill: { color: BR }, line: { color: b.c, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
    s.addText(b.v, { x: b.x, y: 1.0, w: 3.0, h: 0.75, fontSize: 30, bold: true, color: b.c, align: "center", valign: "middle" });
    s.addText(b.t, { x: b.x + 0.1, y: 1.75, w: 2.8, h: 0.6, fontSize: 11.5, color: GT, align: "center", valign: "top" });
  });
  // setas entre eles
  s.addText("+34 pp →", { x: 3.0, y: 2.45, w: 1.5, h: 0.3, fontSize: 12, bold: true, color: GN, align: "center" });
  s.addText("−2,37 pp", { x: 6.2, y: 2.45, w: 1.5, h: 0.3, fontSize: 12, bold: true, color: "92400E", align: "center" });

  s.addShape("rect", { x: 0.3, y: 2.95, w: 9.4, h: 2.3, fill: { color: VE }, line: { color: DO, pt: 1.5 }, rectRadius: 0.09, shadow: makeShadow() });
  s.addText([
    { text: "O que a calibração faz\n", options: { bold: true, color: DO, fontSize: 14 } },
    { text: "50 batches reais do conjunto de validação (representative_dataset) calibram os fatores de escala e zero-point por tensor. Sem isso, a quantização estima a escala de forma imprecisa e a acurácia colapsa (−30,5 pp).\n\n", options: { color: BR, fontSize: 12.5 } },
    { text: "Mensagem-chave:  ", options: { bold: true, color: DO, fontSize: 13 } },
    { text: "a calibração não elimina a perda — reduz a apenas 2,37 pp. O modelo embarcado de verdade entrega 95,76%, não os 98,13% do float. Pós-processamento: temperature scaling (T = 0,25) nos logits.", options: { color: BR, fontSize: 12.5 } }
  ], { x: 0.55, y: 3.05, w: 8.9, h: 2.1, valign: "middle" });
}

// ===========================================================================
// SLIDE 12 — MATRIZ DE CONFUSÃO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Matriz de Confusão — Modelo INT8 (95,76%)");
  slideNum(s, 12);
  s.addImage({ path: "matriz_confusao_int8.png", x: 0.3, y: 0.85, w: 5.65, h: 4.4 });
  card(s, 6.15, 0.85, 3.6, 4.4, VM, VC, "Leitura da matriz");
  s.addText([
    { text: "Test set: 2.618 / 2.734 corretas\n\n", options: { bold: true, color: GN, fontSize: 13 } },
    { text: "Classes fáceis (≥99%):\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Mancha bacteriana (100%), vira-cabeça (99%), saudável (99%)\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Maiores confusões:\n", options: { bold: true, color: "92400E", fontSize: 12.5 } },
    { text: "pinta-preta ↔ septoriose ↔ requeima — doenças com lesões necróticas visualmente semelhantes.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "São justamente as classes com menos amostras de validação — as mais afetadas pela quantização.", options: { color: GT, fontSize: 12, italic: true } }
  ], { x: 6.33, y: 1.45, w: 3.25, h: 3.6, valign: "top" });
}

// ===========================================================================
// SLIDE 13 — OS 5 EXPERIMENTOS
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Evolução: 5 Experimentos de Treinamento");
  slideNum(s, 13);
  const hdr = [
    { text: "Exp", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "Estratégia", options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "PlantVillage", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } },
    { text: "PlantDoc", options: { bold: true, color: BR, fill: { color: VE }, align: "center" } }
  ];
  const rows = [
    [{ text: "A", options: { align: "center" } }, "Edge Impulse — sem calibração INT8",
      { text: "92,5% (FP32)\n62,0% (INT8)", options: { color: RD, bold: true, align: "center" } }, { text: "—", options: { align: "center" } }],
    [{ text: "B", options: { align: "center" } }, "TF local — calibração INT8 (50 batches)",
      { text: "98,13% float\n95,76% INT8", options: { align: "center", bold: true } }, { text: "20,77%", options: { align: "center" } }],
    [{ text: "C", options: { align: "center" } }, "Exp B + augmentation sintética (rembg U2-Net)",
      { text: "96,20%", options: { align: "center" } }, { text: "20,24%  ❌", options: { align: "center", color: RD, bold: true } }],
    [{ text: "D", options: { align: "center" } }, "Exp B + fine-tuning real (PlantDoc/train)",
      { text: "97,55%", options: { align: "center" } }, { text: "30,43%  ✅", options: { align: "center", color: GN, bold: true } }],
    [{ text: "E ★", options: { align: "center", bold: true, color: DO, fill: { color: VE } } },
      { text: "Exp D + Focal Loss γ=2 + aug. agressiva  ← MODELO FINAL", options: { bold: true, fill: { color: VE }, color: BR } },
      { text: "98,43% float", options: { align: "center", bold: true, fill: { color: VE }, color: DO } },
      { text: "30,43%  ✅", options: { align: "center", bold: true, fill: { color: VE }, color: VC } }]
  ];
  s.addTable([hdr, ...rows], { x: 0.25, y: 0.85, w: 9.5, h: 3.85, fontSize: 12.5, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" }, colW: [0.65, 4.3, 2.4, 2.15], rowH: 0.64 });
  s.addShape("rect", { x: 0.25, y: 4.85, w: 9.5, h: 0.68, fill: { color: "FFFBEB" }, line: { color: DO, pt: 1.5 }, rectRadius: 0.06 });
  s.addText([
    { text: "−30,5 pp", options: { bold: true, color: RD } }, { text: " = INT8 sem calibração    ", options: { color: GT } },
    { text: "+34 pp", options: { bold: true, color: GN } }, { text: " = calibração (62,0% → 95,76% INT8)    ", options: { color: GT } },
    { text: "Exp C", options: { bold: true, color: RD } }, { text: " = resultado negativo documentado", options: { color: GT } }
  ], { x: 0.4, y: 4.88, w: 9.2, h: 0.62, fontSize: 12.5, valign: "middle" });
}

// ===========================================================================
// SLIDE 14 — EXP C: RESULTADO NEGATIVO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Exp. C — Resultado Negativo (Augmentation Sintética)");
  slideNum(s, 14);

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
    { text: "síntese não substitui dado de campo. Resultado negativo reprodutível (Pineau 2021).", options: { color: GT, fontSize: 12 } }
  ], { x: 5.35, y: 1.45, w: 4.2, h: 3.7, valign: "top" });
}

// ===========================================================================
// SLIDE 15 — EXP D e E
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Exp. D e E — O Que Realmente Funcionou");
  slideNum(s, 15);

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
// SLIDE 16 — GAP 3 DATASETS (gráfico)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Validação em Campo: Três Datasets, Três Continentes");
  slideNum(s, 16);
  s.addShape("rect", { x: 0.25, y: 0.82, w: 5.5, h: 0.32, fill: { color: "FEE2E2" }, line: { color: "FCA5A5", pt: 1 }, rectRadius: 0.04 });
  s.addText("Referência lab: PlantVillage = 98,43% (float) / 95,76% (INT8)  ↑↑", { x: 0.28, y: 0.82, w: 5.44, h: 0.32, fontSize: 10.5, color: "991B1B", bold: true, valign: "middle" });
  s.addChart(pres.charts.BAR, [
    { name: "Exp B (baseline)",    labels: ["PlantDoc\n(EUA/Europa)", "Tomato-Village\n(Índia)", "Daffodil BD\n(Bangladesh)"], values: [20.77, 0.01, 0.01] },
    { name: "Exp D (fine-tuning)", labels: ["PlantDoc\n(EUA/Europa)", "Tomato-Village\n(Índia)", "Daffodil BD\n(Bangladesh)"], values: [30.43, 11.52, 9.59] },
    { name: "Exp E (Focal Loss)",  labels: ["PlantDoc\n(EUA/Europa)", "Tomato-Village\n(Índia)", "Daffodil BD\n(Bangladesh)"], values: [30.43, 27.65, 18.13] }
  ], {
    x: 0.25, y: 1.2, w: 5.5, h: 3.92, barDir: "col", barGrouping: "clustered",
    chartColors: ["B7E4C7", VM2, VE], chartArea: { fill: { color: BR } },
    catAxisLabelColor: "374151", catAxisLabelFontSize: 10, valAxisLabelColor: "374151", valAxisLabelFontSize: 10,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showValue: true, dataLabelFontSize: 10, dataLabelColor: "111827",
    legendPos: "b", showLegend: true, legendFontSize: 11, valAxisMaxVal: 35, showTitle: false
  });
  s.addShape("rect", { x: 5.95, y: 0.82, w: 3.85, h: 4.3, fill: { color: "FFFBEB" }, line: { color: DO, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addShape("rect", { x: 5.95, y: 0.82, w: 3.85, h: 0.42, fill: { color: VM }, line: { color: VM } });
  s.addShape("rect", { x: 5.95, y: 1.1, w: 3.85, h: 0.18, fill: { color: VM }, line: { color: VM } });
  s.addText("Análise do Gap", { x: 5.95, y: 0.82, w: 3.85, h: 0.42, fontSize: 13, bold: true, color: BR, align: "center", valign: "middle" });
  s.addText([
    { text: "Gap persistente:\n", options: { bold: true, color: RD, fontSize: 13 } },
    { text: "98,43% (lab) → 18–30% (campo)\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Causa identificada:\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "modelo aprende o fundo cinza do PlantVillage como feature, não as lesões.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Exp C ineficaz:\n", options: { bold: true, color: RD, fontSize: 13 } },
    { text: "aug. sintética = 0 ganho\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Único método efetivo:\n", options: { bold: true, color: GN, fontSize: 13 } },
    { text: "+10 pp com 677 imgs reais rotuladas", options: { color: GT, fontSize: 12 } }
  ], { x: 6.1, y: 1.35, w: 3.55, h: 3.65, valign: "top" });
}

// ===========================================================================
// SLIDE 17 — GAP GEOGRÁFICO + COLAPSO DE CLASSE
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Gap Geográfico e Colapso de Classe");
  slideNum(s, 17);

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
// SLIDE 18 — COMPARATIVO
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Comparativo das Três Arquiteturas");
  slideNum(s, 18);
  const hdr = [
    { text: "Aspecto", options: { bold: true, color: BR, fill: { color: VE } } },
    { text: "① Edge  ESP32-S3", options: { bold: true, color: BR, fill: { color: "1D4ED8" }, align: "center" } },
    { text: "② Mobile  Android", options: { bold: true, color: BR, fill: { color: VM2 }, align: "center" } },
    { text: "③ Cloud  Django", options: { bold: true, color: BR, fill: { color: "7E22CE" }, align: "center" } }
  ];
  const chk = { color: GN, bold: true, align: "center" };
  const crs = { color: RD, bold: true, align: "center" };
  const wrn = { color: "92400E", bold: true, align: "center" };
  const rows = [
    ["Latência CNN", { text: "692 ms (±1 ms)", options: { align: "center", bold: true } }, { text: "~200–400 ms *", options: { align: "center", italic: true } }, { text: "306 ms", options: { align: "center" } }],
    ["Funciona offline", { text: "✅  Sim", options: chk }, { text: "✅  Sim", options: chk }, { text: "❌  Não", options: crs }],
    ["Privacidade (LGPD)", { text: "✅  Total", options: chk }, { text: "✅  Total", options: chk }, { text: "⚠️  Imagem transmitida", options: wrn }],
    ["Custo hardware", { text: "~R$ 80", options: { align: "center" } }, { text: "Zero (app)", options: { align: "center" } }, { text: "Servidor", options: { align: "center" } }],
    ["Status atual", { text: "✅  Validado\n10/10 corretas", options: chk }, { text: "✅  Implementado\ntflite_flutter 0.12.1", options: chk }, { text: "✅  Produção\nRailway", options: chk }]
  ];
  s.addTable([hdr, ...rows], { x: 0.25, y: 0.85, w: 9.5, h: 4.38, fontSize: 13, fontFace: "Calibri",
    border: { pt: 1, color: "D1D5DB" }, colW: [2.0, 2.5, 2.5, 2.5], rowH: [0.5, 0.68, 0.68, 0.68, 0.68, 0.76] });
  s.addText("* Estimada — não medida empiricamente neste ciclo  |  Mesmo modelo INT8 (638 KB) nos três caminhos", {
    x: 0.25, y: 5.3, w: 9.5, h: 0.26, fontSize: 10, color: "6B7280", italic: true, align: "center" });
}

// ===========================================================================
// SLIDE 19 — LATÊNCIA NO ESP32-S3
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Latência no ESP32-S3 — Medição Real");
  slideNum(s, 19);

  // Destaque
  s.addShape("rect", { x: 0.3, y: 0.9, w: 4.6, h: 1.6, fill: { color: BR }, line: { color: "1D4ED8", pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText("692 ms", { x: 0.3, y: 1.0, w: 4.6, h: 0.85, fontSize: 40, bold: true, color: "1D4ED8", align: "center", valign: "middle" });
  s.addText("± 1 ms — determinístico · 10/10 corretas", { x: 0.3, y: 1.85, w: 4.6, h: 0.5, fontSize: 12.5, color: GT, align: "center" });

  s.addShape("rect", { x: 5.1, y: 0.9, w: 4.6, h: 1.6, fill: { color: "F0FFF4" }, line: { color: VC, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addText([
    { text: "2× mais rápido que o estimado\n", options: { bold: true, color: GN, fontSize: 14 } },
    { text: "Edge Impulse estimou 1.365 ms — simuladores superestimam o tempo no Xtensa LX7.", options: { color: GT, fontSize: 12 } }
  ], { x: 5.28, y: 1.0, w: 4.25, h: 1.4, valign: "middle" });

  card(s, 0.3, 2.7, 9.4, 2.55, VM, VC, "Por que não chegou aos 300 ms da meta?");
  s.addText([
    { text: "O Xtensa LX7 não tem unidade SIMD INT8 dedicada", options: { bold: true, color: VE, fontSize: 13 } },
    { text: " — as convoluções rodam em instruções escalares de propósito geral, sem aceleração vetorial.\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Mas isso não compromete o uso: ", options: { bold: true, color: GN, fontSize: 13 } },
    { text: "692 ms é imperceptível no campo — o produtor leva 2 a 5 segundos só para posicionar e estabilizar a folha diante da câmera. E a variância de ±1 ms garante previsibilidade total, independente de rede.\n\n", options: { color: GT, fontSize: 12.5 } },
    { text: "Memória: ", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "arena de inferência usa 200 KB de 512 KB (39%) — sobra margem para modelos maiores.", options: { color: GT, fontSize: 12.5 } }
  ], { x: 0.5, y: 3.3, w: 9.0, h: 1.85, valign: "top" });
}

// ===========================================================================
// SLIDE 20 — O SISTEMA EM FUNCIONAMENTO (app + hardware)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "O Sistema em Funcionamento");
  slideNum(s, 20);

  // App (print do celular)
  s.addImage({ path: "app_iot.jpg", x: 0.5, y: 0.92, w: 1.85, h: 4.0 });
  s.addText("App Flutter — tela IoT", { x: 0.35, y: 4.95, w: 2.15, h: 0.3, fontSize: 10.5, italic: true, color: "6B7280", align: "center" });

  // Hardware (foto real)
  s.addImage({ path: "hardware_setup.jpg", x: 2.7, y: 0.92, w: 2.25, h: 4.0 });
  s.addText("ESP32-S3 + DHT22 + sensor de solo", { x: 2.55, y: 4.95, w: 2.55, h: 0.3, fontSize: 10.5, italic: true, color: "6B7280", align: "center" });

  card(s, 5.35, 0.92, 4.4, 4.0, VM, VC, "O que está em produção");
  s.addText([
    { text: "App Flutter (Android)\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Diagnóstico · Histórico IoT · Mapa · Enciclopédia · Perfil\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Sensoriamento em tempo real\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "ESP32-S3 publica temperatura, umidade do ar e do solo via MQTT (QoS 1). A tela mostra 29,5 °C · 49% · 34%, status ONLINE.\n\n", options: { color: GT, fontSize: 12 } },
    { text: "Pipeline integrado\n", options: { bold: true, color: VE, fontSize: 12.5 } },
    { text: "Backend Django persiste cada evento com GPS; o app sincroniza diagnósticos offline → online ao reconectar.", options: { color: GT, fontSize: 12 } }
  ], { x: 5.55, y: 1.5, w: 4.05, h: 3.3, valign: "top" });
}

// ===========================================================================
// SLIDE 21 — DEMONSTRAÇÃO (vídeo + QR)
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Demonstração e Recursos");
  slideNum(s, 21);

  // Vídeo embarcado (toca no PowerPoint)
  s.addMedia({ type: "video", path: "demo_ceres.mp4", x: 0.55, y: 0.95, w: 2.55, h: 4.2 });
  s.addText("▶  Vídeo demonstrativo", { x: 0.55, y: 5.0, w: 2.55, h: 0.3, fontSize: 10.5, italic: true, color: "6B7280", align: "center" });

  card(s, 3.35, 0.95, 3.0, 4.2, VM, VC, "O que o vídeo mostra");
  s.addText([
    { text: "1. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Captura da folha pela câmera do app\n\n", options: { color: GT, fontSize: 12 } },
    { text: "2. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Diagnóstico INT8 (Edge / Mobile / Cloud)\n\n", options: { color: GT, fontSize: 12 } },
    { text: "3. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Publicação via MQTT do ESP32-S3\n\n", options: { color: GT, fontSize: 12 } },
    { text: "4. ", options: { bold: true, color: DO, fontSize: 12.5 } },
    { text: "Histórico e mapa de eventos com GPS", options: { color: GT, fontSize: 12 } }
  ], { x: 3.55, y: 1.55, w: 2.65, h: 3.5, valign: "top" });

  // QR
  s.addShape("rect", { x: 6.55, y: 0.95, w: 3.2, h: 4.2, fill: { color: BR }, line: { color: DO, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
  s.addImage({ path: "qrcode_drive.png", x: 6.85, y: 1.25, w: 2.6, h: 2.74 });
  s.addText([
    { text: "Baixe e teste\n", options: { bold: true, color: VE, fontSize: 13 } },
    { text: "APK + imagens de teste\ngithub.com/Namem/extensao2", options: { color: GT, fontSize: 11.5 } }
  ], { x: 6.65, y: 4.1, w: 3.0, h: 0.95, align: "center", valign: "top" });
}

// ===========================================================================
// SLIDE 22 — CONCLUSÃO E LIMITAÇÕES
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Conclusão e Limitações");
  slideNum(s, 22);
  const colW = 4.6, colH = 4.52, colY = 0.8;
  const cols = [
    { x: 0.25, bg: "F0FFF4", border: VC, hbg: VM2, label: "✅  O que funcionou" },
    { x: 5.15, bg: "FFF5F5", border: "FCA5A5", hbg: "B91C1C", label: "⚠️  Limitações" }
  ];
  cols.forEach(c => {
    s.addShape("rect", { x: c.x, y: colY, w: colW, h: colH, fill: { color: c.bg }, line: { color: c.border, pt: 1.5 }, rectRadius: 0.08, shadow: makeShadow() });
    s.addShape("rect", { x: c.x, y: colY, w: colW, h: 0.48, fill: { color: c.hbg }, line: { color: c.hbg } });
    s.addShape("rect", { x: c.x, y: colY + 0.32, w: colW, h: 0.22, fill: { color: c.hbg }, line: { color: c.hbg } });
    s.addText(c.label, { x: c.x, y: colY, w: colW, h: 0.48, fontSize: 13, bold: true, color: BR, align: "center", valign: "middle" });
  });
  const ok = [
    "MobileNetV2 INT8 viável no ESP32-S3 (692 ms, 638 KB)",
    "Calibração INT8: +34 pp (perda residual de só 2,37 pp)",
    "Fine-tuning com dados reais: +10 pp em campo",
    "Focal Loss γ=2: +16 pp no Tomato-Village (Índia)",
    "Pipeline: ESP32-S3 → MQTT → Django → Flutter"
  ];
  s.addText(ok.map((t, i) => ({ text: t, options: { bullet: { indent: 12 }, breakLine: i < ok.length - 1, paraSpaceAfter: 22 } })),
    { x: 0.38, y: colY + 0.58, w: colW - 0.24, h: colH - 0.65, fontSize: 14, color: GN, valign: "middle" });
  const lim = [
    "Gap lab-campo persiste (98,43% → 18–30%)",
    "Augmentation sintética ineficaz (Exp C)",
    "Latência 692 ms acima da meta de 300 ms",
    "Câmera OV5640 não integrada neste ciclo",
    "Latência Mobile não medida empiricamente"
  ];
  s.addText(lim.map((t, i) => ({ text: t, options: { bullet: { indent: 12 }, breakLine: i < lim.length - 1, paraSpaceAfter: 22 } })),
    { x: 5.28, y: colY + 0.58, w: colW - 0.24, h: colH - 0.65, fontSize: 14, color: "7F1D1D", valign: "middle" });
}

// ===========================================================================
// SLIDE 21 — TRABALHOS FUTUROS
// ===========================================================================
{
  const s = pres.addSlide();
  headerBar(s, "Trabalhos Futuros");
  slideNum(s, 23);
  const items = [
    { badge: "Sprint 2", txt: "Integração da câmera OV5640 + medição de latência real com sensor no ESP32-S3" },
    { badge: "Sprint 3", txt: "Coleta de dataset em lavouras de Sorriso-MT + validação com produtores rurais" },
    { badge: "Pesquisa", txt: "Domain Adaptation adversarial (DANN) — reduzir o gap sem rótulos de campo" },
    { badge: "Pesquisa", txt: "Medição empírica da latência Android on-device (tflite_flutter)" },
    { badge: "Modelo",   txt: "Ampliar fine-tuning com mais dados reais brasileiros — fator limitante identificado" }
  ];
  items.forEach((item, i) => {
    const iy = 0.95 + i * 0.86;
    s.addShape("rect", { x: 0.35, y: iy, w: 1.3, h: 0.62, fill: { color: DO }, line: { color: DO }, rectRadius: 0.06 });
    s.addText(item.badge, { x: 0.35, y: iy, w: 1.3, h: 0.62, fontSize: 12, bold: true, color: VE, align: "center", valign: "middle" });
    s.addShape("rect", { x: 1.78, y: iy, w: 7.9, h: 0.62, fill: { color: BR }, line: { color: VC, pt: 1 }, rectRadius: 0.05, shadow: makeShadow() });
    s.addText(item.txt, { x: 1.9, y: iy, w: 7.7, h: 0.62, fontSize: 13, color: GT, valign: "middle" });
  });
}

// ===========================================================================
// SLIDE 22 — OBRIGADO / PERGUNTAS
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
