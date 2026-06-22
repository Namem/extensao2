import PptxGenJS from "pptxgenjs";

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 inches

// ── Paleta ──────────────────────────────────────────────────────────────────
const BG       = "0D1B2A";  // azul marinho escuro
const VERDE    = "4CAF50";  // verde destaque
const LARANJA  = "FF9800";  // laranja destaque
const BRANCO   = "FFFFFF";
const CINZA    = "B0BEC5";  // cinza claro para texto secundário
const CARD_BG  = "132233";  // card ligeiramente mais claro que o fundo
const CARD2_BG = "1A2E44";

const TITLE_FONT  = "Arial";
const BODY_FONT   = "Calibri";

// ── Helper: slide base ───────────────────────────────────────────────────────
function newSlide(title, subtitleLine) {
  const sl = pptx.addSlide();
  sl.background = { color: BG };

  // Barra lateral esquerda
  sl.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: 0.07, h: 7.5, fill: { color: VERDE }, line: { color: VERDE }
  });

  // Título
  if (title) {
    sl.addText(title, {
      x: 0.25, y: 0.18, w: 12.8, h: 0.6,
      fontFace: TITLE_FONT, fontSize: 28, bold: true, color: BRANCO,
      align: "left",
    });
  }

  // Linha abaixo do título
  if (title) {
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: 0.82, w: 12.8, h: 0.04,
      fill: { color: VERDE }, line: { color: VERDE }
    });
  }

  if (subtitleLine) {
    sl.addText(subtitleLine, {
      x: 0.25, y: 0.88, w: 12.8, h: 0.35,
      fontFace: BODY_FONT, fontSize: 14, color: CINZA, italic: true, align: "left"
    });
  }

  return sl;
}

// ── Helper: caixa de destaque ────────────────────────────────────────────────
function addHighlight(sl, x, y, w, h, text, color) {
  sl.addShape(pptx.ShapeType.rect, {
    x, y, w, h, fill: { color: color }, line: { color: color }, rectRadius: 0.08
  });
  sl.addText(text, {
    x: x + 0.1, y: y + 0.05, w: w - 0.2, h: h - 0.1,
    fontFace: BODY_FONT, fontSize: 12, bold: true, color: BG, align: "left", wrap: true
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 1 — CAPA
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = pptx.addSlide();
  sl.background = { color: BG };

  // Retângulo decorativo superior
  sl.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: 13.33, h: 2.2, fill: { color: "0A3D2E" }, line: { color: "0A3D2E" }
  });
  sl.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: 13.33, h: 0.12, fill: { color: VERDE }, line: { color: VERDE }
  });

  // Título principal
  sl.addText("Ceres Diagnóstico", {
    x: 0.5, y: 0.35, w: 12.33, h: 1.1,
    fontFace: TITLE_FONT, fontSize: 52, bold: true, color: BRANCO, align: "center"
  });

  // Subtítulo
  sl.addText("Sprint Review 2 — Validação IA + Pipeline IoT", {
    x: 0.5, y: 2.4, w: 12.33, h: 0.65,
    fontFace: TITLE_FONT, fontSize: 26, bold: false, color: VERDE, align: "center"
  });

  sl.addShape(pptx.ShapeType.rect, {
    x: 3.5, y: 3.15, w: 6.33, h: 0.04, fill: { color: CINZA }, line: { color: CINZA }
  });

  sl.addText("TCC — Engenharia da Computação · IFMT Cuiabá", {
    x: 0.5, y: 3.28, w: 12.33, h: 0.4,
    fontFace: BODY_FONT, fontSize: 16, color: CINZA, align: "center"
  });

  sl.addText("Namem Rachid Jaudy Neto", {
    x: 0.5, y: 3.85, w: 12.33, h: 0.38,
    fontFace: BODY_FONT, fontSize: 18, bold: true, color: BRANCO, align: "center"
  });

  sl.addText("Maio / 2026", {
    x: 0.5, y: 4.3, w: 12.33, h: 0.35,
    fontFace: BODY_FONT, fontSize: 15, color: CINZA, align: "center"
  });

  // Tags rodapé
  const tags = ["TinyML", "MobileNetV2 INT8", "PlantVillage", "Focal Loss", "3 Continentes"];
  tags.forEach((t, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const offsetX = row === 1 ? 1.65 : 0; // centraliza a linha de 2 tags
    const bx = 1.7 + offsetX + col * 3.3, by = 5.6 + row * 0.52;
    sl.addShape(pptx.ShapeType.rect, {
      x: bx, y: by, w: 2.9, h: 0.38, fill: { color: CARD2_BG }, line: { color: VERDE, pt: 1 }, rectRadius: 0.06
    });
    sl.addText(t, {
      x: bx, y: by, w: 2.9, h: 0.38,
      fontFace: BODY_FONT, fontSize: 13, color: VERDE, align: "center", bold: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 2 — VISÃO GERAL
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Ceres Diagnóstico — Visão Geral", "Sprint 0 e 1 já apresentadas — este slide é contexto rápido.");

  const blocos = [
    { cor: LARANJA, icon: "⚠", titulo: "PROBLEMA", texto: "Produtor rural sem acesso a diagnóstico rápido de doenças no tomateiro.\n\nPrejuízo: até 100% da safra." },
    { cor: VERDE,   icon: "✓", titulo: "SOLUÇÃO",  texto: "ESP32-S3 + câmera + IA embarcada (TinyML).\n\nDetecta 10 doenças em campo, sem internet." },
    { cor: "1565C0", icon: "⚙", titulo: "SISTEMA",  texto: "639 KB no chip\n→ WiFi → MQTT\n→ Django REST\n→ PostgreSQL\n→ App Flutter" },
  ];

  blocos.forEach((b, i) => {
    const bx = 0.25 + i * 4.35, by = 1.35;
    sl.addShape(pptx.ShapeType.rect, {
      x: bx, y: by, w: 4.1, h: 5.5, fill: { color: CARD_BG }, line: { color: b.cor, pt: 2 }, rectRadius: 0.1
    });
    sl.addShape(pptx.ShapeType.rect, {
      x: bx, y: by, w: 4.1, h: 0.55, fill: { color: b.cor }, line: { color: b.cor }, rectRadius: 0.08
    });
    sl.addText(b.titulo, {
      x: bx + 0.1, y: by + 0.05, w: 3.9, h: 0.45,
      fontFace: TITLE_FONT, fontSize: 16, bold: true, color: BG, align: "center"
    });
    sl.addText(b.texto, {
      x: bx + 0.15, y: by + 0.7, w: 3.8, h: 4.6,
      fontFace: BODY_FONT, fontSize: 15, color: BRANCO, align: "left", valign: "top", wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 3 — O QUE FOI PROMETIDO
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("O que prometemos na Sprint Review 1");

  // Card Flutter (original promise)
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.1, w: 12.8, h: 1.45, fill: { color: CARD_BG }, line: { color: "1565C0", pt: 1.5 }, rectRadius: 0.08
  });
  sl.addText("App Flutter (promessa original)", {
    x: 0.45, y: 1.18, w: 6, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 15, bold: true, color: "5C9BF5"
  });
  sl.addText("Telas de diagnóstico, histórico paginado e funcionamento offline para o produtor rural.", {
    x: 0.45, y: 1.58, w: 12.4, h: 0.82,
    fontFace: BODY_FONT, fontSize: 14, color: BRANCO, wrap: true
  });

  // Seta de reorganização
  sl.addShape(pptx.ShapeType.rect, {
    x: 5.9, y: 2.72, w: 1.5, h: 0.06, fill: { color: LARANJA }, line: { color: LARANJA }
  });
  sl.addText("Reorganização", {
    x: 5.5, y: 2.8, w: 2.3, h: 0.35,
    fontFace: BODY_FONT, fontSize: 11, color: LARANJA, align: "center", italic: true
  });

  // Card Reorganização
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 3.2, w: 12.8, h: 1.4, fill: { color: "3E2000" }, line: { color: LARANJA, pt: 1.5 }, rectRadius: 0.08
  });
  sl.addText("Decisão: atacar hardware antes do app", {
    x: 0.45, y: 3.28, w: 7, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 15, bold: true, color: LARANJA
  });
  sl.addText("Com o hardware disponível (ESP32-S3 N16R8) e o modelo IA pronto (639 KB), priorizamos validar a pilha completa de IA + IoT antes do app. O Flutter sem dados reais do hardware seria só UI sem substância.", {
    x: 0.45, y: 3.68, w: 12.4, h: 0.8,
    fontFace: BODY_FONT, fontSize: 13, color: BRANCO, wrap: true
  });

  // Cards metas desta sprint
  addHighlight(sl, 0.25, 4.78, 6.1, 0.72, "Meta IA: validar gap lab-campo — entender por que 20% e como melhorar", LARANJA);
  addHighlight(sl, 6.6, 4.78, 6.45, 0.72, "Meta Firmware: pipeline IoT de ponta a ponta em hardware real", VERDE);

  sl.addText("App Flutter mantido no roadmap — próxima entrega após hardware validado.", {
    x: 0.25, y: 5.65, w: 12.8, h: 0.38,
    fontFace: BODY_FONT, fontSize: 13, color: CINZA, italic: true, align: "center"
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 4 — DATASET DE TREINAMENTO
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Dataset de treinamento: PlantVillage", "Hughes & Salathé (2015) · arXiv:1511.08060 · CC BY 4.0");

  // Card esquerdo — origem e paper
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.15, w: 6.1, h: 2.9, fill: { color: CARD_BG }, line: { color: "1565C0", pt: 1.5 }, rectRadius: 0.08
  });
  sl.addText("Origem e justificativa", {
    x: 0.45, y: 1.25, w: 5.7, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 15, bold: true, color: "5C9BF5"
  });
  sl.addText(
    '"An open access repository of images on plant health to enable the development of mobile disease diagnostics"\n\n' +
    "Hughes & Salathé (2015) criaram o PlantVillage como o maior benchmark público " +
    "de doenças de plantas: imagens coletadas em laboratório, fundo controlado, " +
    "alta resolução.\n\n" +
    "Usado como base nos dois trabalhos do slide de literatura:\n" +
    "• Mohanty et al. (2016) — 99,35% lab\n" +
    "• Singh et al. (2020) — comparação lab vs campo\n\n" +
    "Licença CC BY 4.0 — uso acadêmico e comercial permitido.",
    {
      x: 0.45, y: 1.7, w: 5.7, h: 2.25,
      fontFace: BODY_FONT, fontSize: 13, color: BRANCO, wrap: true
    }
  );

  // Card direito — números
  sl.addShape(pptx.ShapeType.rect, {
    x: 6.6, y: 1.15, w: 6.45, h: 2.9, fill: { color: CARD_BG }, line: { color: VERDE, pt: 1.5 }, rectRadius: 0.08
  });
  sl.addText("Números do dataset", {
    x: 6.8, y: 1.25, w: 6.05, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 15, bold: true, color: VERDE
  });
  const nums = [
    { label: "Imagens originais", val: "18.160" },
    { label: "Após augmentation 6× (offline, seed=42)", val: "88.949" },
    { label: "Split treino / val / teste", val: "70 / 15 / 15%" },
    { label: "Classes (tomateiro)", val: "10" },
  ];
  nums.forEach((n, i) => {
    sl.addText(n.label, {
      x: 6.8, y: 1.72 + i * 0.56, w: 3.8, h: 0.48,
      fontFace: BODY_FONT, fontSize: 13, color: CINZA, valign: "middle"
    });
    sl.addText(n.val, {
      x: 10.65, y: 1.72 + i * 0.56, w: 2.2, h: 0.48,
      fontFace: BODY_FONT, fontSize: 14, bold: true, color: VERDE, valign: "middle", align: "right"
    });
  });

  // Tabela de mapeamento de classes
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 4.18, w: 12.8, h: 0.38, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  sl.addText("Mapeamento PlantVillage → Ceres (10 classes)", {
    x: 0.45, y: 4.22, w: 12.4, h: 0.3,
    fontFace: TITLE_FONT, fontSize: 13, bold: true, color: BRANCO
  });

  const classes = [
    ["D01 Requeima", "D02 Septoriose", "D03 Pinta-preta", "D03b Mancha-alvo", "D05 Mofo-foliar"],
    ["D06 Vira-cabeça", "D06b Mosaico", "D07 Ácaro-bronzeamento", "D09 Mancha-bacteriana", "Saudável"],
  ];
  classes.forEach((row, ri) => {
    row.forEach((cls, ci) => {
      const bx = 0.25 + ci * 2.57, by = 4.65 + ri * 0.82;
      const isLast = ri === 1 && ci === 4;
      sl.addShape(pptx.ShapeType.rect, {
        x: bx, y: by, w: 2.45, h: 0.72,
        fill: { color: isLast ? "0A3D2E" : CARD2_BG },
        line: { color: isLast ? VERDE : CINZA, pt: 0.5 }, rectRadius: 0.05
      });
      sl.addText(cls, {
        x: bx + 0.08, y: by + 0.06, w: 2.28, h: 0.6,
        fontFace: BODY_FONT, fontSize: 11, color: isLast ? VERDE : BRANCO,
        bold: isLast, align: "center", valign: "middle", wrap: true
      });
    });
  });

  // Limitação conhecida
  addHighlight(sl, 0.25, 6.35, 12.8, 0.65,
    "⚠  Limitação conhecida: fundo cinza uniforme controlado → modelo aprende o fundo como feature → gap lab-campo. Motivação dos experimentos C, D e E.",
    LARANJA);
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 5 — JORNADA DOS EXPERIMENTOS (A → E)
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("O que foi entregue — jornada dos experimentos");

  // Colunas: Exp | Nome descritivo | Lab | Campo | Resultado-chave
  const exps = [
    {
      exp: "A", nome: "Edge Impulse — treinamento automático (nuvem)",
      lab: "62% INT8",  campo: "—",
      resultado: "Quantização automática sem calibração: -30pp. Descartado.",
      cor: LARANJA, bg: CARD_BG,
    },
    {
      exp: "B", nome: "TensorFlow local + quantização INT8 calibrada",
      lab: "98,13%", campo: "~20%",
      resultado: "Modelo base do projeto. 50 batches val como calibração → 0pp de perda.",
      cor: VERDE, bg: CARD2_BG,
    },
    {
      exp: "C", nome: "Augmentação sintética de fundo (rembg U2-Net)",
      lab: "96,20%", campo: "20,24%",
      resultado: "177k composições, 650 min. 0pp de ganho em campo. Resultado negativo documentado.",
      cor: LARANJA, bg: CARD_BG,
    },
    {
      exp: "D", nome: "Fine-tuning com imagens reais de campo (PlantDoc)",
      lab: "97,55%", campo: "30,43%",
      resultado: "+10pp em imagens nunca vistas. Dados reais > augmentação sintética.",
      cor: VERDE, bg: CARD2_BG,
    },
    {
      exp: "E", nome: "Focal Loss + augmentação de cor agressiva",
      lab: "98,43%", campo: "27,65%*",
      resultado: "+16pp Índia · +8,5pp Bangladesh. Modelo final: 638 KB ✅",
      cor: VERDE, bg: "0A3D2E",
    },
  ];

  const hdrs = ["Exp", "Nome do Experimento", "Lab", "Campo", "Resultado-chave"];
  const colX  = [0.25, 1.15, 7.35, 8.85, 10.25];
  const colW  = [0.78, 6.0,  1.3,  1.2,   2.85];

  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.05, w: 12.8, h: 0.4, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  hdrs.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.07, y: 1.05, w: colW[i], h: 0.4,
      fontFace: TITLE_FONT, fontSize: 12, bold: true, color: BRANCO, align: "left"
    });
  });

  exps.forEach((r, idx) => {
    const ry = 1.5 + idx * 0.96;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 0.88,
      fill: { color: r.bg }, line: { color: r.cor, pt: idx === 4 ? 1.5 : 0.5 }, rectRadius: 0.05
    });
    // Badge Exp
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 0.78, h: 0.88, fill: { color: r.cor }, line: { color: r.cor }, rectRadius: 0.05
    });
    sl.addText(r.exp, {
      x: 0.25, y: ry, w: 0.78, h: 0.88,
      fontFace: TITLE_FONT, fontSize: 18, bold: true, color: BG, align: "center", valign: "middle"
    });
    // Nome
    sl.addText(r.nome, {
      x: colX[1] + 0.07, y: ry + 0.08, w: colW[1] - 0.1, h: 0.72,
      fontFace: BODY_FONT, fontSize: 12, bold: idx === 4, color: idx === 4 ? VERDE : BRANCO,
      valign: "middle", wrap: true
    });
    // Lab
    sl.addText(r.lab, {
      x: colX[2] + 0.07, y: ry + 0.08, w: colW[2] - 0.1, h: 0.72,
      fontFace: BODY_FONT, fontSize: 13, bold: true,
      color: r.lab.includes("62") ? LARANJA : VERDE,
      valign: "middle", align: "center"
    });
    // Campo
    sl.addText(r.campo, {
      x: colX[3] + 0.07, y: ry + 0.08, w: colW[3] - 0.1, h: 0.72,
      fontFace: BODY_FONT, fontSize: 13, bold: idx >= 3,
      color: r.campo === "—" ? CINZA : idx >= 3 ? VERDE : LARANJA,
      valign: "middle", align: "center"
    });
    // Resultado
    sl.addText(r.resultado, {
      x: colX[4] + 0.07, y: ry + 0.08, w: colW[4] - 0.1, h: 0.72,
      fontFace: BODY_FONT, fontSize: 10, color: idx === 4 ? VERDE : CINZA,
      valign: "middle", wrap: true
    });
  });

  sl.addText("⚠ Exp C: artefatos de borda do rembg criaram domínio sintético — modelo aprendeu franjas inexistentes em campo → 0pp de ganho → motivou o Exp D com dados reais  |  * Campo = Tomato-Village, 217 imgs, nunca vistas", {
    x: 0.25, y: 6.3, w: 12.8, h: 0.35,
    fontFace: BODY_FONT, fontSize: 10, color: LARANJA, italic: true, align: "center"
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 6 — VALIDAÇÃO EM 3 DATASETS + EXP D vs EXP E
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Validação em 3 datasets independentes", "Exp D vs Exp E — nenhum dataset usado em treino");

  // Tabela: Dataset | Região | Imgs | Exp D | Exp E | Δ
  const rows = [
    { ds: "PlantDoc / test",       regiao: "EUA / Europa",      imgs: "69",    expD: "30,43%", expE: "~67%*",   delta: "—",      corE: CINZA,  corD: CINZA },
    { ds: "Tomato-Village / test", regiao: "Rajasthan, Índia",  imgs: "217",   expD: "11,52%", expE: "27,65%",  delta: "+16pp",  corE: VERDE,  corD: LARANJA },
    { ds: "Daffodil BD",           regiao: "Bangladesh",         imgs: "1.616", expD: "9,59%",  expE: "18,13%",  delta: "+8,5pp", corE: VERDE,  corD: LARANJA },
  ];

  const hdrs = ["Dataset", "Região", "Imgs", "Exp D", "Exp E ✨", "Δ"];
  const colX = [0.25, 3.55, 6.55, 7.75,  9.55, 11.35];
  const colW = [3.1,  2.8,  1.0,  1.65,  1.65,  1.35];

  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.08, w: 12.8, h: 0.45, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  hdrs.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.08, y: 1.08, w: colW[i], h: 0.45,
      fontFace: TITLE_FONT, fontSize: 13, bold: true,
      color: i === 4 ? VERDE : BRANCO, align: "left"
    });
  });

  rows.forEach((r, idx) => {
    const ry = 1.58 + idx * 0.82;
    const bg = idx % 2 === 0 ? CARD_BG : CARD2_BG;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 0.76, fill: { color: bg }, line: { color: r.corE, pt: 1.5 }, rectRadius: 0.05
    });
    [r.ds, r.regiao, r.imgs, r.expD, r.expE, r.delta].forEach((val, i) => {
      const cor = i === 3 ? r.corD : i >= 4 ? r.corE : BRANCO;
      sl.addText(val, {
        x: colX[i] + 0.08, y: ry + 0.1, w: colW[i] - 0.1, h: 0.56,
        fontFace: BODY_FONT, fontSize: i >= 3 ? 14 : 13,
        color: cor, bold: i >= 3, valign: "middle", wrap: true
      });
    });
  });

  // Nota PlantDoc
  sl.addText("* PlantDoc avaliado em train+test (746 imgs) — Exp D treinou nesse split, não é comparação justa", {
    x: 0.25, y: 4.08, w: 12.8, h: 0.35,
    fontFace: BODY_FONT, fontSize: 11, color: CINZA, italic: true
  });

  // Conclusão Exp E
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 4.52, w: 12.8, h: 0.65, fill: { color: "0A3D2E" }, line: { color: VERDE, pt: 1.5 }, rectRadius: 0.07
  });
  sl.addText(
    "Exp E generalizou melhor em 2/3 datasets independentes. " +
    "Focal Loss corrigiu o colapso para D02 — atrator mudou para D01/D09 (features mais discriminativas).",
    { x: 0.45, y: 4.57, w: 12.4, h: 0.55, fontFace: BODY_FONT, fontSize: 13, color: VERDE, bold: true, wrap: true }
  );

  // Card único: por que Exp E melhorou — largura total
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 5.3, w: 12.8, h: 1.55, fill: { color: CARD2_BG }, line: { color: VERDE, pt: 1 }, rectRadius: 0.07
  });
  sl.addText("Por que Exp E melhorou nos datasets independentes?", {
    x: 0.45, y: 5.37, w: 12.4, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 13, bold: true, color: VERDE
  });
  sl.addText(
    "Focal Loss (Lin et al. 2017, γ=2): exemplos difíceis (erros confiantes) recebem 4× mais gradiente — força aprender features discriminativas em vez de colapsar numa classe 'segura'.  " +
    "Augmentação de cor (brilho ±30%, contraste ±40%, saturação 50–160%, matiz ±8°): simula variações de iluminação solar e câmeras distintas.  " +
    "Backbone completo descongelado (LR=1e-5): todas as features do ImageNet reajustadas para domínio de campo.",
    { x: 0.45, y: 5.78, w: 12.4, h: 1.0, fontFace: BODY_FONT, fontSize: 12, color: BRANCO, wrap: true }
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 8 — COMPARAÇÃO COM LITERATURA
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Nosso resultado não é anomalia — é o padrão da área");

  // Colunas: Autor | Título / Venue | Lab | Campo | Diferencial
  const rows = [
    {
      autor: "Mohanty et al.",
      titulo: '"Using Deep Learning for Image-Based Plant Disease Detection"\nFrontiers in Plant Science, 2016',
      lab: "99,35%", campo: "~31%",
      dif: "Só modelo, sem hardware embarcado",
      cor: CINZA, bg: CARD_BG,
    },
    {
      autor: "Singh et al.",
      titulo: '"Deep Learning-based Plant Disease Identification using Real Field Images"\nIEEE Access, 2020',
      lab: "~95%", campo: "~55%",
      dif: "Usou fotos reais de campo (+40,8pp vs lab sintético)",
      cor: CINZA, bg: CARD2_BG,
    },
    {
      autor: "Ceres (Jaudy Neto)",
      titulo: "TCC IFMT Cuiabá, 2026. Exp D: Fine-tuning com dados reais. Exp E: Focal Loss + Aug Agressiva",
      lab: "98,43%", campo: "30,43%*",
      dif: "ESP32-S3 638 KB + MQTT + Django + App Flutter",
      cor: VERDE, bg: "0A3D2E",
    },
  ];

  const hdrs = ["Autor", "Título / Venue", "Lab", "Campo"];
  const colX = [0.25, 2.55, 9.9, 11.5];
  const colW = [2.1,  7.1,  1.4,  1.35];

  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.1, w: 12.8, h: 0.45, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  hdrs.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.08, y: 1.1, w: colW[i], h: 0.45,
      fontFace: TITLE_FONT, fontSize: 13, bold: true, color: BRANCO, align: "left"
    });
  });

  rows.forEach((r, idx) => {
    const ry = 1.6 + idx * 1.35;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 1.28,
      fill: { color: r.bg }, line: { color: r.cor, pt: idx === 2 ? 1.5 : 0 }
    });
    // Autor (bold)
    sl.addText(r.autor, {
      x: colX[0] + 0.08, y: ry + 0.1, w: colW[0] - 0.1, h: 1.08,
      fontFace: BODY_FONT, fontSize: 13, bold: true, color: r.cor, valign: "middle", wrap: true
    });
    // Título em duas fontes: título em itálico menor
    sl.addText(r.titulo, {
      x: colX[1] + 0.08, y: ry + 0.08, w: colW[1] - 0.1, h: 1.12,
      fontFace: BODY_FONT, fontSize: 11, color: idx === 2 ? VERDE : CINZA,
      italic: idx < 2, valign: "top", wrap: true
    });
    // Lab
    sl.addText(r.lab, {
      x: colX[2] + 0.08, y: ry + 0.1, w: colW[2] - 0.1, h: 1.08,
      fontFace: BODY_FONT, fontSize: 14, bold: true, color: r.cor, valign: "middle", align: "center"
    });
    // Campo
    sl.addText(r.campo, {
      x: colX[3] + 0.08, y: ry + 0.1, w: colW[3] - 0.1, h: 1.08,
      fontFace: BODY_FONT, fontSize: 14, bold: idx === 2, color: idx === 2 ? VERDE : LARANJA,
      valign: "middle", align: "center"
    });
  });

  sl.addText("* Campo = PlantDoc test (69 imgs, Exp D, métrica canônica do TCC). Exp E em dataset independente Tomato-Village: 27,65%.", {
    x: 0.25, y: 5.68, w: 12.8, h: 0.3,
    fontFace: BODY_FONT, fontSize: 11, color: CINZA, italic: true
  });

  addHighlight(sl, 0.25, 6.08, 12.8, 0.85,
    "Mohanty e Singh documentaram o gap lab-campo — o Ceres resolve: sistema embarcado completo em 638 KB, " +
    "validado em 3 continentes. Howard et al. (2017): MobileNetV2 — única arquitetura que cabe no ESP32-S3.", VERDE);
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 9 — CONCLUSÃO CIENTÍFICA: GAP MULTIFATORIAL
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Por que o gap lab-campo existe?", "Análise multifatorial dos experimentos A → E");

  const fatores = [
    { num: "1", titulo: "Fundo da imagem",      desc: "PlantVillage: fundo cinza uniforme, controlado. Modelo aprende o fundo como feature discriminativa. Exp C tentou resolver com composições sintéticas (rembg) — 0pp de ganho.", cor: LARANJA },
    { num: "2", titulo: "Iluminação e câmera",  desc: "Luz solar direta, sombras, reflexos e câmeras de celular criam distribuição visual completamente diferente do laboratório.", cor: LARANJA },
    { num: "3", titulo: "Variedade geográfica", desc: "Cultivares de Rajasthan (Índia) e Bangladesh diferem morfologicamente das cultivares americanas usadas no PlantVillage.", cor: LARANJA },
    { num: "4", titulo: "Estágio fenológico",   desc: "Folhas em diferentes estágios de crescimento têm textura, cor e proporções distintas — variável ausente no dataset de laboratório.", cor: LARANJA },
  ];

  fatores.forEach((f, i) => {
    const by = 1.1 + i * 1.28;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: by, w: 12.8, h: 1.18, fill: { color: CARD_BG }, line: { color: CARD_BG }
    });
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: by, w: 0.55, h: 1.18, fill: { color: f.cor }, line: { color: f.cor }
    });
    sl.addText(f.num, {
      x: 0.25, y: by, w: 0.55, h: 1.18,
      fontFace: TITLE_FONT, fontSize: 22, bold: true, color: BG, align: "center", valign: "middle"
    });
    sl.addText(f.titulo, {
      x: 1.0, y: by + 0.1, w: 11.8, h: 0.36,
      fontFace: TITLE_FONT, fontSize: 14, bold: true, color: BRANCO
    });
    sl.addText(f.desc, {
      x: 1.0, y: by + 0.48, w: 11.8, h: 0.62,
      fontFace: BODY_FONT, fontSize: 13, color: CINZA, wrap: true
    });
  });

  addHighlight(sl, 0.25, 6.28, 12.8, 0.68,
    "Resolver só o fundo (Exp C) = insuficiente  ·  Fine-tuning com dados reais (Exp D) = +10pp  ·  Focal Loss + aug de cor (Exp E) = +16pp Índia  ·  Validação definitiva: produtores de Sorriso-MT",
    VERDE);
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 10 — PRÓXIMOS PASSOS
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("O que vem a seguir");

  // Cadeia de validação — contexto
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.1, w: 12.8, h: 0.55, fill: { color: CARD2_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.06
  });
  sl.addText(
    "Cadeia de validação do modelo:  " +
    "Nível 1 ✅ Lab (98%)  →  Nível 2 ✅ Campo PlantDoc (30%)  →  Nível 3 ⏳ Hardware real ESP32-S3  →  Nível 4 ⏳ Produtores Sorriso-MT",
    {
      x: 0.4, y: 1.13, w: 12.5, h: 0.45,
      fontFace: BODY_FONT, fontSize: 12, color: CINZA, wrap: false
    }
  );

  const itens = [
    { icone: "🛒", o_que: "Comprar OV5640 + DHT22 + sensor de umidade do solo", dep: "Loja física / AliExpress", cor: LARANJA },
    { icone: "⚙", o_que: "TFLite Micro no ESP32-S3 — modelo 639KB rodando no chip com câmera", dep: "Hardware em mãos", cor: LARANJA },
    { icone: "📊", o_que: "Benchmark: 50 imagens, latência < 300ms, RAM livre > 4MB — Nível 3 da cadeia", dep: "Hardware em mãos", cor: LARANJA },
    { icone: "📱", o_que: "App Flutter — histórico de diagnósticos, resultado, funcionamento offline", dep: "Qualquer máquina", cor: "5C9BF5" },
    { icone: "🌱", o_que: "Validação com produtores de Sorriso-MT — fotos reais brasileiras — Nível 4 da cadeia", dep: "Contato com produtores", cor: VERDE },
  ];

  const headers = ["", "O que fazer", "Depende de"];
  const colX = [0.25, 2.0, 9.4];
  const colW = [1.55, 7.2, 3.7];

  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.75, w: 12.8, h: 0.42, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  headers.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.1, y: 1.75, w: colW[i], h: 0.42,
      fontFace: TITLE_FONT, fontSize: 13, bold: true, color: BRANCO, align: "left"
    });
  });

  itens.forEach((r, idx) => {
    const ry = 2.22 + idx * 1.0;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 0.9, fill: { color: idx % 2 === 0 ? CARD_BG : CARD2_BG },
      line: { color: r.cor, pt: 1 }, rectRadius: 0.04
    });
    sl.addText(r.icone, {
      x: colX[0] + 0.1, y: ry + 0.1, w: colW[0] - 0.2, h: 0.7,
      fontFace: BODY_FONT, fontSize: 22, valign: "middle", align: "center"
    });
    sl.addText(r.o_que, {
      x: colX[1] + 0.1, y: ry + 0.08, w: colW[1] - 0.2, h: 0.74,
      fontFace: BODY_FONT, fontSize: 13, color: BRANCO, valign: "middle", wrap: true
    });
    sl.addText(r.dep, {
      x: colX[2] + 0.1, y: ry + 0.08, w: colW[2] - 0.2, h: 0.74,
      fontFace: BODY_FONT, fontSize: 12, color: r.cor, valign: "middle", wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 11 — ENCERRAMENTO
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = pptx.addSlide();
  sl.background = { color: BG };
  sl.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: 13.33, h: 0.12, fill: { color: VERDE }, line: { color: VERDE }
  });
  sl.addShape(pptx.ShapeType.rect, {
    x: 0, y: 7.38, w: 13.33, h: 0.12, fill: { color: VERDE }, line: { color: VERDE }
  });

  sl.addText("Resumo Sprint Review 2", {
    x: 0.5, y: 0.25, w: 12.33, h: 0.7,
    fontFace: TITLE_FONT, fontSize: 30, bold: true, color: BRANCO, align: "center"
  });

  const itens = [
    { icon: "✅", texto: "5 experimentos de IA concluídos (A, B, C, D, E) — metodologia científica completa" },
    { icon: "✅", texto: "Modelo final: Exp E · 638 KB · 98,43% lab · Macro F1 0,979" },
    { icon: "✅", texto: "3 validações independentes: +16pp Índia · +8,5pp Bangladesh com Exp E vs Exp D" },
    { icon: "✅", texto: "Gap lab-campo multifatorial documentado: fundo + iluminação + geografia + variedade" },
    { icon: "✅", texto: "Firmware ESP32-S3 + MQTT: 74 eventos · pipeline completo validado em hardware real" },
    { icon: "🎯", texto: "Próximo marco: TFLite Micro no ESP32-S3 com câmera OV5640 + validação Sorriso-MT" },
  ];

  itens.forEach((it, i) => {
    const cor = it.icon === "🎯" ? LARANJA : VERDE;
    const by = 1.05 + i * 0.77;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.5, y: by, w: 12.33, h: 0.7,
      fill: { color: it.icon === "🎯" ? "3E2000" : CARD_BG },
      line: { color: cor, pt: 1 }, rectRadius: 0.07
    });
    sl.addText(it.icon + "  " + it.texto, {
      x: 0.7, y: by + 0.08, w: 12.0, h: 0.54,
      fontFace: BODY_FONT, fontSize: 14, color: it.icon === "🎯" ? LARANJA : BRANCO,
      bold: it.icon === "🎯", valign: "middle", wrap: true
    });
  });

  sl.addText("github.com/Namem/extensao2", {
    x: 0.5, y: 6.95, w: 12.33, h: 0.32,
    fontFace: BODY_FONT, fontSize: 13, color: CINZA, align: "center"
  });
}

// ── Salvar ───────────────────────────────────────────────────────────────────
await pptx.writeFile({ fileName: "SprintReview_2_CeresDiagnostico.pptx" });
console.log("PPTX gerado com sucesso!");
