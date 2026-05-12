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
  const tags = ["TinyML", "ESP32-S3", "MobileNetV2 INT8", "MQTT", "Django REST", "Flutter"];
  tags.forEach((t, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const bx = 1.7 + col * 3.3, by = 5.6 + row * 0.52;
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
// SLIDE 4 — O QUE FOI ENTREGUE
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("O que foi entregue");

  const rows = [
    { frente: "Exp C — Background Augmentation sintética",     status: "✅", cor: LARANJA, resultado: "20,24% campo — igual ao anterior. Meta 70% não atingida." },
    { frente: "Exp D — Fine-tuning com fotos reais de campo",  status: "✅", cor: VERDE,   resultado: "97,55% lab · 30,43% campo não visto · +10pp" },
    { frente: "Validação Tomato-Village (Rajasthan, Índia)",   status: "✅", cor: VERDE,   resultado: "11,52% · 217 imgs · gap geográfico confirmado" },
    { frente: "Validação Daffodil BD (Bangladesh) — 3ª opinião", status: "✅", cor: VERDE, resultado: "9,59% · 1.616 imgs · D05_mofo 77,3% (outlier positivo)" },
    { frente: "Firmware ESP32-S3 + Pipeline MQTT completo",    status: "✅", cor: VERDE,   resultado: "74 eventos · ESP32-S3 → Mosquitto → Django → PostgreSQL → API" },
  ];

  const headers = ["Entrega", "Status", "Resultado"];
  const colX = [0.25, 8.2, 9.6];
  const colW = [7.75, 1.2, 3.5];

  // Header da tabela
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.05, w: 12.8, h: 0.42, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  headers.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.1, y: 1.05, w: colW[i], h: 0.42,
      fontFace: TITLE_FONT, fontSize: 13, bold: true, color: BRANCO, align: "left"
    });
  });

  rows.forEach((r, idx) => {
    const ry = 1.53 + idx * 1.1;
    const bg = idx % 2 === 0 ? CARD_BG : CARD2_BG;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 1.0, fill: { color: bg }, line: { color: r.cor, pt: 1 }, rectRadius: 0.05
    });
    sl.addText(r.frente, {
      x: colX[0] + 0.1, y: ry + 0.08, w: colW[0] - 0.2, h: 0.84,
      fontFace: BODY_FONT, fontSize: 12, bold: true, color: BRANCO, valign: "middle", wrap: true
    });
    sl.addText(r.status, {
      x: colX[1] + 0.05, y: ry + 0.08, w: colW[1] - 0.05, h: 0.84,
      fontFace: BODY_FONT, fontSize: 15, bold: true, color: r.cor, valign: "middle", align: "center"
    });
    sl.addText(r.resultado, {
      x: colX[2] + 0.1, y: ry + 0.08, w: colW[2] - 0.2, h: 0.84,
      fontFace: BODY_FONT, fontSize: 11, color: BRANCO, valign: "middle", wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 5 — EXP C: QUANDO O PLANO FALHA
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Exp C — Background Augmentation: por que falhou?");

  // Card esquerdo — O que fizemos
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.15, w: 5.9, h: 5.5, fill: { color: CARD_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.08
  });
  sl.addText("O que fizemos", {
    x: 0.4, y: 1.25, w: 5.6, h: 0.4,
    fontFace: TITLE_FONT, fontSize: 15, bold: true, color: CINZA
  });
  const itens = [
    "177.698 composições sintéticas geradas",
    "rembg (rede U2-Net) remove fundo da folha",
    "Recompõe sobre fundos naturais do PlantDoc",
    "650 minutos de processamento contínuo",
    "Retreino completo WSL2 (RTX 3060 Ti)",
    "96,20% acurácia no laboratório",
  ];
  itens.forEach((it, i) => {
    sl.addText("• " + it, {
      x: 0.4, y: 1.75 + i * 0.72, w: 5.6, h: 0.65,
      fontFace: BODY_FONT, fontSize: 13, color: BRANCO, wrap: true
    });
  });

  // Card direito — Resultado
  sl.addShape(pptx.ShapeType.rect, {
    x: 6.4, y: 1.15, w: 6.7, h: 2.4, fill: { color: CARD_BG }, line: { color: LARANJA, pt: 2 }, rectRadius: 0.08
  });
  sl.addText("Resultado", {
    x: 6.6, y: 1.25, w: 6.3, h: 0.4,
    fontFace: TITLE_FONT, fontSize: 15, bold: true, color: LARANJA
  });
  sl.addText("Antes (Exp B):  20,24%\nDepois (Exp C): 20,24%\nDiferença:         0 pp ❌", {
    x: 6.6, y: 1.72, w: 6.3, h: 1.65,
    fontFace: "Consolas", fontSize: 17, color: BRANCO, wrap: true
  });

  // Caixa por quê falhou
  sl.addShape(pptx.ShapeType.rect, {
    x: 6.4, y: 3.75, w: 6.7, h: 1.65, fill: { color: "3E2000" }, line: { color: LARANJA, pt: 1.5 }, rectRadius: 0.08
  });
  sl.addText("Por quê falhou?", {
    x: 6.6, y: 3.83, w: 6.3, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 14, bold: true, color: LARANJA
  });
  sl.addText(
    "Alpha-matting gera artefatos de borda e iluminação inconsistente. " +
    "O modelo aprendeu o domínio sintético, não o real.\n" +
    "Singh et al. (2020) usaram fotos reais — por isso funcionou para eles.",
    {
      x: 6.6, y: 4.24, w: 6.3, h: 1.1,
      fontFace: BODY_FONT, fontSize: 12, color: BRANCO, wrap: true
    }
  );

  // Por que não usamos fotos reais desde o início?
  sl.addShape(pptx.ShapeType.rect, {
    x: 6.4, y: 5.55, w: 6.7, h: 1.6, fill: { color: CARD2_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.08
  });
  sl.addText("Por que não usamos fotos reais de campo?", {
    x: 6.6, y: 5.63, w: 6.3, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 13, bold: true, color: CINZA
  });
  sl.addText(
    "Não existe dataset público de folhas de tomate em campo brasileiro. " +
    "O PlantDoc (fotos reais, EUA/Europa) foi usado no Exp D (+10pp). " +
    "A coleta no Brasil acontece na próxima sprint (Sorriso-MT).",
    {
      x: 6.6, y: 6.05, w: 6.3, h: 1.0,
      fontFace: BODY_FONT, fontSize: 12, color: BRANCO, wrap: true
    }
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 6 — EXP D: PIVÔ CIENTÍFICO
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Exp D — Fine-tuning com Dados Reais de Campo", "Quando o plano A falha, você faz ciência");

  // Estratégia
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.28, w: 12.8, h: 0.65, fill: { color: "0A3D2E" }, line: { color: VERDE, pt: 1 }, rectRadius: 0.07
  });
  sl.addText("Estratégia: 677 fotos reais do PlantDoc/train + PlantVillage = 95.719 imagens no treino total", {
    x: 0.45, y: 1.33, w: 12.4, h: 0.55,
    fontFace: BODY_FONT, fontSize: 14, color: VERDE, bold: true
  });

  // Tabela comparativa
  const rows = [
    { metrica: "Lab — PlantVillage test",       expB: "98,13%", expD: "97,55%",         cor: CINZA },
    { metrica: "Campo — imagens CONHECIDAS",     expB: "—",      expD: "88,47%",         cor: CINZA },
    { metrica: "Campo — imagens NUNCA VISTAS",   expB: "~20%",   expD: "30,43% ← +10pp", cor: VERDE },
    { metrica: "Tamanho do modelo",              expB: "639 KB", expD: "639 KB (igual)", cor: CINZA },
  ];

  const headers = ["Métrica", "Exp B (linha base)", "Exp D (fine-tuning)"];
  const colX = [0.25, 6.2, 9.5];
  const colW = [5.7, 3.0, 3.6];

  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 2.1, w: 12.8, h: 0.48, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  headers.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.1, y: 2.1, w: colW[i], h: 0.48,
      fontFace: TITLE_FONT, fontSize: 13, bold: true, color: BRANCO, align: "left"
    });
  });

  rows.forEach((r, idx) => {
    const ry = 2.63 + idx * 0.78;
    const isHighlight = r.cor === VERDE;
    const bg = isHighlight ? "0A3D2E" : (idx % 2 === 0 ? CARD_BG : CARD2_BG);
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 0.72, fill: { color: bg }, line: { color: bg }
    });
    sl.addText(r.metrica, {
      x: colX[0] + 0.1, y: ry + 0.08, w: colW[0] - 0.2, h: 0.56,
      fontFace: BODY_FONT, fontSize: 13, color: isHighlight ? VERDE : BRANCO, bold: isHighlight, valign: "middle"
    });
    sl.addText(r.expB, {
      x: colX[1] + 0.1, y: ry + 0.08, w: colW[1] - 0.2, h: 0.56,
      fontFace: BODY_FONT, fontSize: 13, color: CINZA, align: "center", valign: "middle"
    });
    sl.addText(r.expD, {
      x: colX[2] + 0.1, y: ry + 0.08, w: colW[2] - 0.2, h: 0.56,
      fontFace: BODY_FONT, fontSize: 14, color: isHighlight ? VERDE : BRANCO, bold: isHighlight, align: "center", valign: "middle"
    });
  });

  addHighlight(sl, 0.25, 6.3, 12.8, 0.65,
    "Modelo final escolhido: Exp D — mesmo tamanho (639 KB), melhor desempenho em campo", VERDE);
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 7 — VALIDAÇÃO EM 3 DATASETS INDEPENDENTES
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Validação em 3 datasets independentes", "Nenhum deles foi usado em qualquer etapa de treino");

  // Tabela comparativa 3 datasets
  const rows = [
    { ds: "PlantDoc / test",       regiao: "EUA / Europa",       clima: "Temperado",       imgs: "69",    classes: "4", res: "30,43%", cor: VERDE },
    { ds: "Tomato-Village / test", regiao: "Rajasthan, Índia",   clima: "Árido tropical",  imgs: "217",   classes: "4", res: "11,52%", cor: LARANJA },
    { ds: "Daffodil BD",           regiao: "Bangladesh",          clima: "Tropical úmido",  imgs: "1.616", classes: "7", res: "9,59%",  cor: "F57C00" },
  ];

  const hdrs = ["Dataset", "Região", "Clima", "Imgs", "Cls", "Exp D"];
  const colX = [0.25, 3.5, 6.4, 9.35, 10.5, 11.3];
  const colW = [3.0,  2.7, 2.75, 0.95, 0.65, 1.7];

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
    const ry = 1.6 + idx * 0.82;
    const bg = idx % 2 === 0 ? CARD_BG : CARD2_BG;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 0.76, fill: { color: bg }, line: { color: r.cor, pt: 1.5 }, rectRadius: 0.05
    });
    [r.ds, r.regiao, r.clima, r.imgs, r.classes, r.res].forEach((val, i) => {
      sl.addText(val, {
        x: colX[i] + 0.08, y: ry + 0.1, w: colW[i] - 0.1, h: 0.56,
        fontFace: BODY_FONT, fontSize: i === 5 ? 15 : 13,
        color: i === 5 ? r.cor : BRANCO, bold: i === 5, valign: "middle", wrap: true
      });
    });
  });

  // Descoberta principal
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 4.12, w: 12.8, h: 0.65, fill: { color: "3E2000" }, line: { color: LARANJA, pt: 1.5 }, rectRadius: 0.07
  });
  sl.addText("Descoberta: o gap não é de fundo — é geográfico e climático. O modelo melhorou no contexto do PlantDoc, não globalmente.",
    { x: 0.45, y: 4.17, w: 12.4, h: 0.55, fontFace: BODY_FONT, fontSize: 13, color: LARANJA, bold: true, wrap: true }
  );

  // Achado positivo D05
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 4.9, w: 6.1, h: 1.45, fill: { color: "0A3D2E" }, line: { color: VERDE, pt: 1.5 }, rectRadius: 0.07
  });
  sl.addText("Outlier positivo — D05_mofo_foliar", {
    x: 0.45, y: 4.97, w: 5.8, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 14, bold: true, color: VERDE
  });
  sl.addText(
    "77,3% no Daffodil BD. Passalora fulva cria textura fúngica branco-acinzentada única, " +
    "invariante geograficamente. A única classe que o modelo reconhece confiável em campo real.",
    { x: 0.45, y: 5.38, w: 5.8, h: 0.92, fontFace: BODY_FONT, fontSize: 12, color: BRANCO, wrap: true }
  );

  // Colapso D02
  sl.addShape(pptx.ShapeType.rect, {
    x: 6.6, y: 4.9, w: 6.45, h: 1.45, fill: { color: CARD2_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.07
  });
  sl.addText("Colapso para D02_septoriose", {
    x: 6.75, y: 4.97, w: 6.15, h: 0.38,
    fontFace: TITLE_FONT, fontSize: 14, bold: true, color: CINZA
  });
  sl.addText(
    "Atrator universal: sob shift de domínio extremo, o modelo converge para 'septoriose' — " +
    "manchas escuras irregulares são a representação genérica de doença foliar aprendida no treino.",
    { x: 6.75, y: 5.38, w: 6.15, h: 0.92, fontFace: BODY_FONT, fontSize: 12, color: CINZA, wrap: true }
  );

  sl.addText("A validação que realmente importa: produtores de Sorriso-MT — fotos brasileiras reais (Sprint 3)", {
    x: 0.25, y: 6.5, w: 12.8, h: 0.42,
    fontFace: BODY_FONT, fontSize: 14, color: VERDE, bold: true, align: "center"
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 8 — COMPARAÇÃO COM LITERATURA
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Nosso resultado não é anomalia — é o padrão da área");

  const rows = [
    { trab: "Mohanty et al.", ano: "2016", lab: "99,35%", campo: "~31%",  hw: "❌", sis: "❌ Só modelo" },
    { trab: "Singh et al.",   ano: "2020", lab: "~95%",   campo: "~55%",  hw: "❌", sis: "❌ Só modelo" },
    { trab: "Ceres (você)",   ano: "2026", lab: "97,55%", campo: "30,43%",hw: "✅", sis: "✅ ESP32-S3 + MQTT + App" },
  ];

  const headers = ["Trabalho", "Ano", "Laboratório", "Campo", "Hardware", "Sistema"];
  const colX = [0.25, 3.4, 4.8, 6.35, 8.0, 9.4];
  const colW = [2.9, 1.2, 1.35, 1.45, 1.2, 3.7];

  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 1.12, w: 12.8, h: 0.48, fill: { color: "1A3A5C" }, line: { color: "1A3A5C" }
  });
  headers.forEach((h, i) => {
    sl.addText(h, {
      x: colX[i] + 0.05, y: 1.12, w: colW[i], h: 0.48,
      fontFace: TITLE_FONT, fontSize: 13, bold: true, color: BRANCO, align: "left"
    });
  });

  rows.forEach((r, idx) => {
    const ry = 1.65 + idx * 0.95;
    const isCeres = idx === 2;
    const bg = isCeres ? "0A3D2E" : (idx % 2 === 0 ? CARD_BG : CARD2_BG);
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: ry, w: 12.8, h: 0.88, fill: { color: bg }, line: { color: isCeres ? VERDE : bg }
    });
    [r.trab, r.ano, r.lab, r.campo, r.hw, r.sis].forEach((val, i) => {
      sl.addText(val, {
        x: colX[i] + 0.05, y: ry + 0.1, w: colW[i] - 0.05, h: 0.68,
        fontFace: BODY_FONT, fontSize: 13, color: isCeres ? VERDE : BRANCO,
        bold: isCeres, valign: "middle", wrap: true
      });
    });
  });

  // Destaque
  addHighlight(sl, 0.25, 4.68, 12.8, 0.9,
    "Diferencial do Ceres: sistema completo embarcado em 639 KB. " +
    "Mohanty e Singh documentaram o problema — o Ceres implementa a solução em hardware real.", VERDE);

  // Cards justificativa de escolha
  sl.addShape(pptx.ShapeType.rect, {
    x: 0.25, y: 5.75, w: 6.1, h: 0.95, fill: { color: CARD2_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.07
  });
  sl.addText("Por que MobileNetV2 e não ResNet?", {
    x: 0.4, y: 5.82, w: 5.8, h: 0.3,
    fontFace: BODY_FONT, fontSize: 12, bold: true, color: CINZA
  });
  sl.addText("Howard et al. (2017): projetado para dispositivos com restrição de memória. ResNet-50 > 90 MB — incompatível com ESP32-S3.", {
    x: 0.4, y: 6.15, w: 5.8, h: 0.48,
    fontFace: BODY_FONT, fontSize: 11, color: BRANCO, wrap: true
  });

  sl.addShape(pptx.ShapeType.rect, {
    x: 6.6, y: 5.75, w: 6.45, h: 0.95, fill: { color: CARD2_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.07
  });
  sl.addText("Por que TFLite INT8 e não FP32?", {
    x: 6.75, y: 5.82, w: 6.15, h: 0.3,
    fontFace: BODY_FONT, fontSize: 12, bold: true, color: CINZA
  });
  sl.addText("Exp A: INT8 sem calibração = -30pp (62%). Exp B: INT8 com representative_dataset = 0pp de perda, 4x menor.", {
    x: 6.75, y: 6.15, w: 6.15, h: 0.48,
    fontFace: BODY_FONT, fontSize: 11, color: BRANCO, wrap: true
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 9 — FIRMWARE ESP32-S3
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Sprint 1b — Pipeline IoT validado de ponta a ponta");

  // Diagrama de fluxo
  const nos = [
    { label: "ESP32-S3\nWROOM-1\nN16R8", cor: VERDE },
    { label: "WiFi\n2.4 GHz", cor: "1565C0" },
    { label: "Mosquitto\nMQTT :1883", cor: "F57C00" },
    { label: "Django\nmqtt_listener", cor: "6A1B9A" },
    { label: "PostgreSQL", cor: "00838F" },
    { label: "REST API\nJWT", cor: VERDE },
  ];

  nos.forEach((n, i) => {
    const bx = 0.25 + i * 2.17;
    sl.addShape(pptx.ShapeType.rect, {
      x: bx, y: 1.25, w: 2.0, h: 1.0, fill: { color: n.cor }, line: { color: n.cor }, rectRadius: 0.1
    });
    sl.addText(n.label, {
      x: bx, y: 1.25, w: 2.0, h: 1.0,
      fontFace: BODY_FONT, fontSize: 11, bold: true, color: BG, align: "center", valign: "middle"
    });
    if (i < nos.length - 1) {
      sl.addShape(pptx.ShapeType.rect, {
        x: bx + 2.0, y: 1.68, w: 0.17, h: 0.15, fill: { color: BRANCO }, line: { color: BRANCO }
      });
    }
  });

  // Tópico MQTT
  sl.addText("Tópico: ceres/sensor/001   |   JSON: device_id, temperatura, umidade_ar, umidade_solo, timestamp", {
    x: 0.25, y: 2.38, w: 12.8, h: 0.4,
    fontFace: "Consolas", fontSize: 12, color: VERDE, align: "center"
  });

  // Cards detalhes
  const cards = [
    { titulo: "Hardware", texto: "ESP32-S3-WROOM-1-N16R8 · 16MB Flash + 8MB PSRAM\nEspressif Datasheet (2022) — escolhido por ter PSRAM suficiente para TFLite Micro (modelo 639KB + buffers)" },
    { titulo: "Firmware: PlatformIO + PubSubClient", texto: "PlatformIO: gerenciamento de libs + upload + monitor em um tool. Arduino IDE alternativa, menos robusta para múltiplos módulos.\nPubSubClient (Knolleary, 2023): cliente MQTT leve para Arduino — sem overhead de frameworks maiores." },
    { titulo: "Por que MQTT e não HTTP?", texto: "Al-Fuqaha et al. (2015), IEEE — IoT Survey: MQTT tem overhead de 2 bytes vs ~820 bytes do HTTP. Projetado para redes instáveis e dispositivos com restrição de energia." },
    { titulo: "Resultado validado", texto: "74 eventos persistidos no PostgreSQL\nAPI GET /historico/ retornando JSON paginado com JWT\nLatência média publish → DB: < 500ms" },
  ];

  cards.forEach((c, i) => {
    const bx = 0.25 + (i % 2) * 6.55, by = 3.0 + Math.floor(i / 2) * 2.1;
    sl.addShape(pptx.ShapeType.rect, {
      x: bx, y: by, w: 6.3, h: 1.9, fill: { color: CARD_BG }, line: { color: CINZA, pt: 1 }, rectRadius: 0.08
    });
    sl.addText(c.titulo, {
      x: bx + 0.15, y: by + 0.1, w: 5.9, h: 0.38,
      fontFace: TITLE_FONT, fontSize: 14, bold: true, color: VERDE
    });
    sl.addText(c.texto, {
      x: bx + 0.15, y: by + 0.5, w: 5.9, h: 1.3,
      fontFace: BODY_FONT, fontSize: 13, color: BRANCO, wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 10 — PROBLEMAS RESOLVIDOS
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("Dificuldades técnicas e soluções");

  const problemas = [
    {
      titulo: "Firmware — Boot loop no ESP32-S3",
      problema: "Flag board_build.arduino.memory_type=qio_opi incompatível com Arduino framework → reinício infinito.",
      solucao: "Remover flags de memória customizadas. Arduino gerencia PSRAM internamente."
    },
    {
      titulo: "Firmware — Serial Monitor silencioso",
      problema: "ARDUINO_USB_CDC_ON_BOOT=1 redireciona Serial para USB nativa. Nada aparecia no monitor serial.",
      solucao: "Remover flags USB CDC. Serial.begin(115200) volta para a porta CH343 padrão."
    },
    {
      titulo: "Firmware — MQTT rc=-2 (conexão recusada)",
      problema: "Mosquitto com 'bind_address localhost' rejeita conexões de outro IP. ESP32 conecta por IP da rede local.",
      solucao: "mosquitto.conf: 'listener 1883' sem bind. Regra de firewall Windows liberando porta 1883."
    },
    {
      titulo: "IA — Quantization loss -30pp no Exp A",
      problema: "Edge Impulse quantizou INT8 sem representative_dataset → pesos calibrados com distribuição errada → 92,5% FP32 virou 62,0% INT8.",
      solucao: "Exp B: quantização com 50 batches do val set como representative_dataset → 0pp de perda na quantização."
    },
    {
      titulo: "IA — class_names perdido após .prefetch()",
      problema: "TensorFlow perde o atributo class_names do dataset após aplicar .map().prefetch(). export_tflite.py travava com AttributeError.",
      solucao: "Capturar ds_raw.class_names antes de aplicar transformações e passar como retorno da função."
    },
    {
      titulo: "Git — Symlinks WSL2 quebrando git add",
      problema: "processed_mixed/ criada com symlinks Linux no WSL2. Windows Git não indexa symlinks → 'fatal: unable to index'.",
      solucao: "Adicionar datasets/processed_mixed/ ao .gitignore. Nunca commitar datasets locais."
    },
  ];

  // 6 problemas em grid 2x3
  problemas.forEach((p, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const bx = 0.25 + col * 6.55, by = 1.12 + row * 2.05;
    const corTit = i < 3 ? LARANJA : "5C9BF5"; // laranja = firmware, azul = IA/git
    sl.addShape(pptx.ShapeType.rect, {
      x: bx, y: by, w: 6.3, h: 1.9, fill: { color: CARD_BG }, line: { color: corTit, pt: 1 }, rectRadius: 0.08
    });
    sl.addText(p.titulo, {
      x: bx + 0.15, y: by + 0.08, w: 5.9, h: 0.4,
      fontFace: TITLE_FONT, fontSize: 12, bold: true, color: corTit, wrap: true
    });
    sl.addText("↳ " + p.problema, {
      x: bx + 0.15, y: by + 0.5, w: 5.9, h: 0.62,
      fontFace: BODY_FONT, fontSize: 11, color: CINZA, wrap: true
    });
    sl.addText("✓ " + p.solucao, {
      x: bx + 0.15, y: by + 1.14, w: 5.9, h: 0.65,
      fontFace: BODY_FONT, fontSize: 11, color: VERDE, wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 11 — CONCLUSÃO CIENTÍFICA
// ═══════════════════════════════════════════════════════════════════════════
{
  const sl = newSlide("O gap lab-campo é multifatorial");

  const fatores = [
    { num: "1", titulo: "Fundo da imagem",        desc: "PlantVillage: fundo cinza uniforme, controlado. Modelo aprende o fundo como feature discriminativa.", cor: LARANJA },
    { num: "2", titulo: "Iluminação e câmera",    desc: "Luz solar direta, sombras, reflexos e câmeras de celular criam distribuição visual completamente diferente.", cor: LARANJA },
    { num: "3", titulo: "Variedade geográfica",   desc: "Cultivares indianas (Rajasthan) diferem morfologicamente das cultivares americanas e brasileiras.", cor: LARANJA },
    { num: "4", titulo: "Estágio fenológico",     desc: "Folhas em diferentes estágios de crescimento têm textura, cor e proporções distintas.", cor: LARANJA },
  ];

  fatores.forEach((f, i) => {
    const by = 1.12 + i * 1.3;
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: by, w: 12.8, h: 1.2, fill: { color: CARD_BG }, line: { color: CARD_BG }
    });
    sl.addShape(pptx.ShapeType.rect, {
      x: 0.25, y: by, w: 0.55, h: 1.2, fill: { color: f.cor }, line: { color: f.cor }
    });
    sl.addText(f.num, {
      x: 0.25, y: by, w: 0.55, h: 1.2,
      fontFace: TITLE_FONT, fontSize: 22, bold: true, color: BG, align: "center", valign: "middle"
    });
    sl.addText(f.titulo, {
      x: 1.0, y: by + 0.1, w: 11.8, h: 0.38,
      fontFace: TITLE_FONT, fontSize: 14, bold: true, color: BRANCO
    });
    sl.addText(f.desc, {
      x: 1.0, y: by + 0.5, w: 11.8, h: 0.6,
      fontFace: BODY_FONT, fontSize: 13, color: CINZA, wrap: true
    });
  });

  addHighlight(sl, 0.25, 6.35, 12.8, 0.65,
    "Resolver só o fundo (Exp C) = insuficiente  ·  Fine-tuning local (Exp D) = melhora, mas não generaliza globalmente  ·  Validação em Sorriso-MT = a métrica que importa",
    VERDE);
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 12 — PRÓXIMOS PASSOS
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
// SLIDE 13 — ENCERRAMENTO
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
    { icon: "✅", texto: "4 experimentos de validação IA concluídos (Exp A, B, C, D)" },
    { icon: "✅", texto: "Gap lab-campo documentado e analisado com base na literatura" },
    { icon: "✅", texto: "Modelo final: Exp D · 639 KB · 97,55% lab / 30,43% campo" },
    { icon: "✅", texto: "3 validações independentes: PlantDoc 30,43% · Tomato-Village 11,52% · Daffodil BD 9,59%" },
    { icon: "✅", texto: "Achado: D05_mofo_foliar 77,3% — única classe robusta em campo real (distinção visual)" },
    { icon: "✅", texto: "Firmware ESP32-S3 + MQTT: 74 eventos · pipeline completo validado" },
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
