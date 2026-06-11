/**
 * Gerador de slides — Ceres Diagnóstico Sprint MVP
 * Uso: node gerar_slides.js
 */

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const BASE = path.join(__dirname, "assets");
const HW = path.join(BASE, "fotos_hardware");
const SS = path.join(BASE, "screenshots");
const VID = path.join(BASE, "video");
const OUT_DIR = path.join(BASE, "slides");

if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

// ── Paleta ────────────────────────────────────────────────────────────────────
const C = {
  verde:  "1a3a1a",
  verde2: "2d5a2d",
  bege:   "f5f0e8",
  ouro:   "c8860a",
  ouro2:  "e8a020",
  branco: "FFFFFF",
  texto:  "1a1a1a",
  cinza:  "666666",
  tag_bg: "2d5a2d",
};

// ── Helpers ───────────────────────────────────────────────────────────────────
const imgPath = (folder, name) => path.join(folder, name);

function addTag(slide, label, x = 0.4, y = 0.22) {
  slide.addShape("rect", {
    x, y, w: label.length * 0.115 + 0.3, h: 0.28,
    fill: { color: C.ouro }, line: { color: C.ouro }
  });
  slide.addText(label, {
    x, y: y - 0.01, w: label.length * 0.115 + 0.3, h: 0.28,
    fontSize: 9, bold: true, color: C.verde, align: "center",
    valign: "middle", margin: 0, charSpacing: 1
  });
}

function addFooter(slide, light = false) {
  const bg = light ? C.verde : "2a4a2a";
  slide.addShape("rect", { x: 0, y: 5.35, w: 10, h: 0.275, fill: { color: bg }, line: { color: bg } });
  slide.addText("Ceres Diagnóstico — Sprint MVP  ·  IFMT Cuiabá  ·  Junho 2026", {
    x: 0.3, y: 5.35, w: 9.4, h: 0.275,
    fontSize: 8, color: "ffffff80".slice(0, 6), align: "center", valign: "middle",
    transparency: 30
  });
}

function addStatCard(slide, num, label, x, y, w = 2.1, h = 1.0) {
  slide.addShape("rect", { x, y, w, h, fill: { color: C.verde2 }, line: { color: C.ouro, width: 1.5 } });
  slide.addText(num, { x, y: y + 0.05, w, h: 0.55, fontSize: 28, bold: true, color: C.ouro, align: "center", valign: "bottom" });
  slide.addText(label, { x, y: y + 0.58, w, h: 0.38, fontSize: 9.5, color: C.branco, align: "center", valign: "top" });
}

// ── Slide 1: Capa ─────────────────────────────────────────────────────────────
function slide1(pres) {
  const s = pres.addSlide();
  s.background = { color: C.verde };

  // Imagem de fundo com overlay
  s.addImage({ path: imgPath(HW, "setup_completo_v1.jpg"), x: 0, y: 0, w: 10, h: 5.625, transparency: 65 });

  // Overlay escuro no topo e base
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 5.625, fill: { color: "000000", transparency: 45 }, line: { color: "000000", transparency: 45 } });

  // Faixa ouro vertical esquerda
  s.addShape("rect", { x: 0, y: 0, w: 0.08, h: 5.625, fill: { color: C.ouro }, line: { color: C.ouro } });

  // Tag topo
  s.addText("PROJETO DE EXTENSÃO · ENGENHARIA DA COMPUTAÇÃO · IFMT CUIABÁ", {
    x: 0.3, y: 0.3, w: 9.4, h: 0.3,
    fontSize: 9, color: C.ouro, align: "center", charSpacing: 2, bold: true
  });

  // Título
  s.addText("CERES\nDIAGNÓSTICO", {
    x: 0.5, y: 1.1, w: 9, h: 2.0,
    fontSize: 64, bold: true, color: C.branco, align: "center", valign: "middle"
  });

  // Linha ouro
  s.addShape("rect", { x: 2.5, y: 3.15, w: 5, h: 0.05, fill: { color: C.ouro }, line: { color: C.ouro } });

  // Subtítulo
  s.addText("Sprint Review — Sprint MVP", {
    x: 0.5, y: 3.25, w: 9, h: 0.5,
    fontSize: 22, color: C.ouro, align: "center", bold: false
  });

  // Autor
  s.addText("Namem Rachid Jaudy Neto", {
    x: 0.5, y: 3.85, w: 9, h: 0.35,
    fontSize: 13, color: C.branco, align: "center"
  });

  // Junho 2026
  s.addText("Junho de 2026", {
    x: 0.5, y: 5.1, w: 9, h: 0.3,
    fontSize: 10, color: C.ouro, align: "center"
  });
}

// ── Slide 2: O Problema ───────────────────────────────────────────────────────
function slide2(pres) {
  const s = pres.addSlide();
  s.background = { color: C.bege };

  addTag(s, "01 | O PROBLEMA");

  s.addText("O agricultor perde antes de\nsaber o que perdeu", {
    x: 0.4, y: 0.55, w: 9.2, h: 1.0,
    fontSize: 26, bold: true, color: C.verde, align: "left"
  });

  // Parágrafo
  s.addText("Um tomateiro doente não grita. Ele murcha em silêncio enquanto a doença avança. Quando o produtor percebe, já é tarde — e a safra, já é prejuízo.", {
    x: 0.4, y: 1.55, w: 4.8, h: 0.75,
    fontSize: 12, color: C.texto, align: "left"
  });

  // 3 bullets esquerda
  const bullets = [
    "Diagnóstico depende de agrônomos inacessíveis ao pequeno produtor",
    "Soluções digitais exigem internet que não chega na lavoura",
    "Quanto mais tarde, maior o custo e a perda"
  ];
  bullets.forEach((b, i) => {
    s.addShape("rect", { x: 0.4, y: 2.4 + i * 0.65, w: 0.06, h: 0.42, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(b, { x: 0.55, y: 2.4 + i * 0.65, w: 4.5, h: 0.42, fontSize: 11.5, color: C.texto, valign: "middle" });
  });

  // 3 stat cards direita
  const stats = [
    ["até 100%", "de perda por\nrequeima sem tratamento"],
    ["10 doenças", "difíceis de distinguir\na olho nu"],
    ["0 especialistas", "disponíveis no campo\nna hora certa"],
  ];
  stats.forEach(([num, lbl], i) => {
    const cx = 5.6;
    const cy = 1.5 + i * 1.22;
    s.addShape("rect", { x: cx, y: cy, w: 4.0, h: 1.05, fill: { color: C.verde }, line: { color: C.ouro, width: 1.5 } });
    s.addText(num, { x: cx + 0.15, y: cy + 0.05, w: 3.7, h: 0.45, fontSize: 19, bold: true, color: C.ouro, valign: "bottom" });
    s.addText(lbl, { x: cx + 0.15, y: cy + 0.52, w: 3.7, h: 0.48, fontSize: 10.5, color: C.branco, valign: "top" });
  });

  addFooter(s, true);
}

// ── Slide 3: Roadmap ──────────────────────────────────────────────────────────
function slide3(pres) {
  const s = pres.addSlide();
  s.background = { color: C.verde };

  addTag(s, "02 | ROADMAP", 0.4, 0.22);

  s.addText("De onde viemos e para onde vamos", {
    x: 0.4, y: 0.55, w: 9.2, h: 0.55,
    fontSize: 26, bold: true, color: C.branco
  });

  // Linha de timeline
  s.addShape("rect", { x: 0.5, y: 3.0, w: 9.0, h: 0.05, fill: { color: C.ouro2 }, line: { color: C.ouro2 } });

  const etapas = [
    { sprint: "Sprint 0", desc: "Motor de diagnóstico\npor perguntas (API)", done: true, current: false },
    { sprint: "Sprint 1", desc: "Treinamento da IA\n+ pipeline MQTT", done: true, current: false },
    { sprint: "Sprint 2", desc: "IA embarcada\nESP32-S3 · 692ms", done: true, current: false },
    { sprint: "Sprint 3\nMVP", desc: "App completo\n+ hardware real", done: true, current: true },
    { sprint: "Próximos\nPassos", desc: "Câmera embarcada\n+ Dataset BR", done: false, current: false },
  ];

  etapas.forEach((e, i) => {
    const cx = 0.7 + i * 1.85;
    const isC = e.current;
    const isDone = e.done && !isC;

    // Círculo maior
    s.addShape("oval", {
      x: cx, y: 2.72, w: 0.6, h: 0.6,
      fill: { color: isC ? C.ouro : (isDone ? C.verde2 : "555555") },
      line: { color: isC ? C.ouro2 : (isDone ? C.ouro : "888888"), width: 2 }
    });

    s.addText(isDone ? "✓" : (isC ? "★" : "→"), {
      x: cx, y: 2.72, w: 0.6, h: 0.6,
      fontSize: 16, bold: true,
      color: isC ? C.verde : (isDone ? C.ouro : "aaaaaa"),
      align: "center", valign: "middle"
    });

    // Label sprint
    s.addText(e.sprint, {
      x: cx - 0.5, y: 1.65, w: 1.6, h: 0.7,
      fontSize: isC ? 12 : 10.5, bold: isC, color: isC ? C.ouro : C.branco,
      align: "center"
    });

    // Descrição mais espaçada
    s.addText(e.desc, {
      x: cx - 0.5, y: 3.42, w: 1.6, h: 0.85,
      fontSize: 10, color: isC ? C.ouro2 : "aaaaaa",
      align: "center"
    });

    // Destaque "ESTAMOS AQUI"
    if (isC) {
      s.addShape("rect", {
        x: cx - 0.58, y: 2.24, w: 1.76, h: 0.3,
        fill: { color: C.ouro }, line: { color: C.ouro }
      });
      s.addText("ESTAMOS AQUI", {
        x: cx - 0.58, y: 2.24, w: 1.76, h: 0.3,
        fontSize: 8, bold: true, color: C.verde, align: "center", valign: "middle"
      });
    }
  });

  // Texto resumo abaixo
  s.addText("4 sprints concluídas · 1 ano de desenvolvimento · defesa em breve", {
    x: 0.5, y: 4.42, w: 9.0, h: 0.35,
    fontSize: 11, color: "88aa88", align: "center"
  });

  addFooter(s);
}

// ── Slide 4: Evolução ─────────────────────────────────────────────────────────
function slide4(pres) {
  const s = pres.addSlide();
  s.background = { color: C.bege };

  addTag(s, "03 | EVOLUÇÃO");

  s.addText("Prometemos. Entregamos. E fomos além.", {
    x: 0.4, y: 0.55, w: 9.2, h: 0.55,
    fontSize: 24, bold: true, color: C.verde
  });

  // Card Sprint 1 (esquerda)
  s.addShape("rect", { x: 0.35, y: 1.2, w: 4.0, h: 3.85, fill: { color: "e8e0d0" }, line: { color: "ccbb99", width: 1 } });
  s.addShape("rect", { x: 0.35, y: 1.2, w: 4.0, h: 0.45, fill: { color: "999988" }, line: { color: "999988" } });
  s.addText("Sprint 1", { x: 0.35, y: 1.2, w: 4.0, h: 0.45, fontSize: 12, bold: true, color: C.branco, align: "center", valign: "middle" });

  const s1 = [
    "Motor por perguntas e respostas (regras Embrapa)",
    "Produtor respondia ~3 perguntas em texto",
    "API funcional — sem câmera, sem IA visual",
    "Modelo na nuvem, sem modo offline",
  ];
  s1.forEach((t, i) => {
    s.addShape("oval", { x: 0.5, y: 1.78 + i * 0.7, w: 0.18, h: 0.18, fill: { color: "999988" }, line: { color: "999988" } });
    s.addText(t, { x: 0.75, y: 1.75 + i * 0.7, w: 3.45, h: 0.4, fontSize: 11, color: "444444" });
  });

  // Seta
  s.addText("→", { x: 4.5, y: 2.8, w: 0.9, h: 0.6, fontSize: 32, color: C.ouro, align: "center", bold: true });

  // Card MVP (direita — destaque)
  s.addShape("rect", { x: 5.55, y: 1.2, w: 4.1, h: 3.85, fill: { color: C.verde }, line: { color: C.ouro, width: 2 } });
  s.addShape("rect", { x: 5.55, y: 1.2, w: 4.1, h: 0.45, fill: { color: C.ouro }, line: { color: C.ouro } });
  s.addText("Sprint MVP  ★", { x: 5.55, y: 1.2, w: 4.1, h: 0.45, fontSize: 12, bold: true, color: C.verde, align: "center", valign: "middle" });

  const s2 = [
    "Foto da folha → IA classifica em < 2 segundos",
    "98,43% de acurácia · 10 doenças identificadas",
    "Offline completo: IA no celular sem internet",
    "App Flutter com mapa, histórico e enciclopédia",
    "ESP32-S3 monitorando ambiente em tempo real",
  ];
  s2.forEach((t, i) => {
    s.addShape("oval", { x: 5.7, y: 1.78 + i * 0.68, w: 0.18, h: 0.18, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(t, { x: 5.95, y: 1.75 + i * 0.68, w: 3.55, h: 0.4, fontSize: 11, color: C.branco });
  });

  addFooter(s, true);
}

// ── Slide 5: A Solução ────────────────────────────────────────────────────────
function slide5(pres) {
  const s = pres.addSlide();
  s.background = { color: C.bege };

  addTag(s, "04 | A SOLUÇÃO");

  s.addText("Um sistema completo — do campo ao celular", {
    x: 0.4, y: 0.55, w: 9.2, h: 0.55,
    fontSize: 24, bold: true, color: C.verde
  });

  // Foto setup
  s.addImage({ path: imgPath(HW, "setup_completo_v1.jpg"), x: 0.35, y: 1.2, w: 3.5, h: 2.6, sizing: { type: "cover", w: 3.5, h: 2.6 } });

  // 3 blocos de fluxo
  const blocos = [
    { icon: "📡", title: "ESP32-S3", desc: "Sensores\ntemperatura · umidade · solo\nMQTT a cada 30s" },
    { icon: "☁️", title: "Backend Railway", desc: "Django REST API\nIA + JWT + Histórico\nceres.up.railway.app" },
    { icon: "📱", title: "App Flutter", desc: "Diagnóstico · Mapa\nHistórico · Offline\niOS + Android" },
  ];

  blocos.forEach((b, i) => {
    const bx = 4.15 + i * 1.95;
    s.addShape("rect", { x: bx, y: 1.2, w: 1.7, h: 2.6, fill: { color: C.verde }, line: { color: C.ouro, width: 1.5 } });
    s.addText(b.icon, { x: bx, y: 1.25, w: 1.7, h: 0.5, fontSize: 22, align: "center" });
    s.addText(b.title, { x: bx, y: 1.75, w: 1.7, h: 0.4, fontSize: 11, bold: true, color: C.ouro, align: "center" });
    s.addShape("rect", { x: bx + 0.15, y: 2.17, w: 1.4, h: 0.03, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(b.desc, { x: bx + 0.05, y: 2.24, w: 1.6, h: 1.4, fontSize: 9.5, color: C.branco, align: "center" });

    // Seta entre blocos
    if (i < 2) {
      s.addText("→", { x: bx + 1.7, y: 2.1, w: 0.25, h: 0.5, fontSize: 14, color: C.ouro, align: "center", bold: true });
    }
  });

  // 3 bullets abaixo
  const pts = [
    "Hardware IoT monitora o ambiente 24h sem intervenção",
    "App fotografa a folha — IA identifica a doença com ou sem internet",
    "Mapa mostra onde e quando cada doença apareceu no talhão",
  ];
  pts.forEach((p, i) => {
    s.addShape("rect", { x: 0.35, y: 4.0 + i * 0.42, w: 0.06, h: 0.3, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(p, { x: 0.5, y: 3.98 + i * 0.42, w: 9.1, h: 0.3, fontSize: 11.5, color: C.texto, valign: "middle" });
  });

  addFooter(s, true);
}

// ── Slide 6: Diagnóstico + Offline ────────────────────────────────────────────
function slide6(pres) {
  const s = pres.addSlide();
  s.background = { color: C.verde };

  addTag(s, "05 | DIAGNÓSTICO", 0.4, 0.22);

  s.addText("Foto a folha. Saiba o que está acontecendo.\nOnde quer que esteja.", {
    x: 0.4, y: 0.55, w: 9.2, h: 0.85,
    fontSize: 21, bold: true, color: C.branco
  });

  // Screenshot do app (esquerda)
  const ssFile = imgPath(SS, "iot_sensor_card.jpg");
  s.addImage({ path: ssFile, x: 0.35, y: 1.5, w: 2.2, h: 3.7, sizing: { type: "contain", w: 2.2, h: 3.7 } });

  // 3 passos (direita topo)
  const passos = [
    ["1", "Fotografa a folha", "pela câmera ou galeria"],
    ["2", "IA classifica", "a doença em < 2 segundos"],
    ["3", "Resultado completo", "doença · confiança · top-3 · tratamento"],
  ];
  passos.forEach(([n, t, d], i) => {
    const px = 2.8;
    const py = 1.5 + i * 0.82;
    s.addShape("oval", { x: px, y: py, w: 0.42, h: 0.42, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(n, { x: px, y: py, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: C.verde, align: "center", valign: "middle" });
    s.addText(t, { x: px + 0.5, y: py + 0.01, w: 6.7, h: 0.25, fontSize: 12, bold: true, color: C.branco });
    s.addText(d, { x: px + 0.5, y: py + 0.25, w: 6.7, h: 0.25, fontSize: 10, color: "aaccaa" });
  });

  // Separador + badge acurácia inline
  s.addShape("rect", { x: 2.7, y: 3.9, w: 7.0, h: 0.03, fill: { color: C.ouro }, line: { color: C.ouro } });
  s.addText("98,43% acurácia · 10 doenças · 638 KB · funciona em qualquer lavoura", {
    x: 2.7, y: 3.95, w: 7.0, h: 0.28,
    fontSize: 10, bold: true, color: C.ouro, align: "center"
  });

  // 2 cards: cloud vs offline (lado a lado sem sobreposição)
  const modos = [
    { title: "COM INTERNET", sub: "Modo Cloud", items: ["Resultado em ~2s via Railway", "Histórico salvo na nuvem", "Mapa atualizado em tempo real"], ic: "☁️" },
    { title: "SEM INTERNET", sub: "Modo Offline", items: ["IA no celular em <1s", "Nenhum dado sai do dispositivo", "Funciona em qualquer lavoura remota"], ic: "✈️" },
  ];
  modos.forEach((m, i) => {
    const mx = 2.75 + i * 3.65;
    s.addShape("rect", { x: mx, y: 4.28, w: 3.4, h: 1.05, fill: { color: C.verde2 }, line: { color: C.ouro, width: 1.5 } });
    s.addText(`${m.ic} ${m.title}`, { x: mx + 0.1, y: 4.31, w: 3.2, h: 0.26, fontSize: 10, bold: true, color: C.ouro });
    s.addText(m.sub, { x: mx + 0.1, y: 4.55, w: 3.2, h: 0.18, fontSize: 8.5, color: "88cc88" });
    m.items.forEach((it, j) => {
      s.addText(`· ${it}`, { x: mx + 0.1, y: 4.73 + j * 0.19, w: 3.2, h: 0.19, fontSize: 8.5, color: C.branco });
    });
  });

  addFooter(s);
}

// ── Slide 7: Hardware IoT ─────────────────────────────────────────────────────
function slide7(pres) {
  const s = pres.addSlide();
  s.background = { color: C.bege };

  addTag(s, "06 | HARDWARE IoT");

  s.addText("ESP32-S3 — sentinela da lavoura", {
    x: 0.4, y: 0.55, w: 9.2, h: 0.5,
    fontSize: 24, bold: true, color: C.verde
  });

  // Texto descritivo esquerda
  s.addText("A cada 30 segundos mede temperatura, umidade do ar e umidade do solo — e envia tudo para a nuvem via MQTT. O app exibe em tempo real com status ONLINE.", {
    x: 0.35, y: 1.15, w: 3.8, h: 1.0,
    fontSize: 11, color: C.texto
  });

  // 3 leituras reais
  const leituras = [
    { icon: "🌡️", val: "29,5°C", lbl: "Temperatura" },
    { icon: "💧", val: "49%", lbl: "Umidade ar" },
    { icon: "🌱", val: "34%", lbl: "Umidade solo" },
  ];
  leituras.forEach((l, i) => {
    const lx = 0.35 + i * 1.3;
    s.addShape("rect", { x: lx, y: 2.3, w: 1.15, h: 0.95, fill: { color: C.verde }, line: { color: C.ouro, width: 1.5 } });
    s.addText(l.icon, { x: lx, y: 2.32, w: 1.15, h: 0.3, fontSize: 16, align: "center" });
    s.addText(l.val, { x: lx, y: 2.6, w: 1.15, h: 0.3, fontSize: 13, bold: true, color: C.ouro, align: "center" });
    s.addText(l.lbl, { x: lx, y: 2.9, w: 1.15, h: 0.28, fontSize: 8, color: C.branco, align: "center" });
  });

  // Componentes texto
  const comps = [
    ["ESP32-S3", "o cérebro do sistema — Wi-Fi + TFLite"],
    ["DHT22", "temperatura e umidade do ar"],
    ["Sensor capacitivo", "umidade do solo sem corrosão"],
    ["MQTT HiveMQ", "conexão segura com a nuvem"],
  ];
  comps.forEach(([name, desc], i) => {
    s.addShape("rect", { x: 0.35, y: 3.42 + i * 0.4, w: 0.08, h: 0.28, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(name, { x: 0.5, y: 3.4 + i * 0.4, w: 1.4, h: 0.28, fontSize: 10.5, bold: true, color: C.verde, valign: "middle" });
    s.addText(desc, { x: 1.95, y: 3.4 + i * 0.4, w: 2.25, h: 0.28, fontSize: 10, color: C.texto, valign: "middle" });
  });

  // Grid de fotos hardware (direita)
  const fotos = [
    { file: "esp32_closeup.jpg", label: "ESP32-S3 DevKit" },
    { file: "dht22_componente.jpg", label: "Sensor DHT22" },
    { file: "sensor_solo_terra.jpg", label: "Sensor no solo" },
    { file: "serial_monitor.png", label: "Monitor serial" },
  ];
  fotos.forEach((f, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const fx = 4.35 + col * 2.85;
    const fy = 1.12 + row * 2.15;
    s.addImage({ path: imgPath(HW, f.file), x: fx, y: fy, w: 2.65, h: 1.85, sizing: { type: "cover", w: 2.65, h: 1.85 } });
    // Label
    s.addShape("rect", { x: fx, y: fy + 1.55, w: 2.65, h: 0.3, fill: { color: "00000060".slice(0, 6), transparency: 40 }, line: { color: C.verde } });
    s.addText(f.label, { x: fx, y: fy + 1.58, w: 2.65, h: 0.27, fontSize: 8.5, color: C.branco, align: "center" });
  });

  addFooter(s, true);
}

// ── Slide 8: Resultados ───────────────────────────────────────────────────────
function slide8(pres) {
  const s = pres.addSlide();
  s.background = { color: C.verde };

  addTag(s, "07 | RESULTADOS", 0.4, 0.22);

  s.addText("O que entregamos — em números", {
    x: 0.4, y: 0.55, w: 9.2, h: 0.5,
    fontSize: 26, bold: true, color: C.branco
  });

  // 6 stat cards em grid 3x2
  const stats = [
    ["98,43%", "acurácia no\ntest set PlantVillage"],
    ["692ms", "latência no hardware\nESP32-S3"],
    ["10/10", "acertos no\nbenchmark offline"],
    ["638 KB", "modelo INT8\nno dispositivo"],
    ["88.949", "imagens de treino\n(augmentation x6)"],
    ["184+", "eventos IoT\nregistrados"],
  ];

  stats.forEach(([num, lbl], i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    addStatCard(s, num, lbl, 0.4 + col * 3.1, 1.2 + row * 1.35, 2.85, 1.1);
  });

  // Badges linha inferior
  const badges = [
    "5 experimentos de treinamento",
    "3 datasets de validação",
    "App publicado em Railway",
    "5 testes automatizados ✅",
  ];
  badges.forEach((b, i) => {
    const bx = 0.35 + i * 2.35;
    s.addShape("rect", { x: bx, y: 3.75, w: 2.2, h: 0.4, fill: { color: C.verde2 }, line: { color: C.ouro, width: 1 } });
    s.addText(b, { x: bx, y: 3.75, w: 2.2, h: 0.4, fontSize: 9, color: C.branco, align: "center", valign: "middle" });
  });

  addFooter(s);
}

// ── Slide 9: Demo ao Vivo ─────────────────────────────────────────────────────
function slide9(pres) {
  const s = pres.addSlide();
  s.background = { color: C.verde };

  // Faixa ouro topo
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.ouro }, line: { color: C.ouro } });

  // Título compacto
  s.addText("Demo ao Vivo", {
    x: 0.3, y: 0.1, w: 7, h: 0.62,
    fontSize: 28, bold: true, color: C.ouro
  });
  s.addText("Demonstração gravada — plano B se o ao vivo falhar", {
    x: 0.3, y: 0.68, w: 9.4, h: 0.28,
    fontSize: 10, color: "88aa88"
  });

  // Vídeo embutido (ocupa a maior parte do slide)
  const videoFile = path.join(VID, "demo_ceres.mp4");
  s.addMedia({
    type: "video",
    path: videoFile,
    x: 0.3, y: 1.0, w: 9.4, h: 3.5
  });

  // 3 labels do roteiro abaixo do vídeo
  const itens = [
    ["🌿", "Cloud: Requeima 94%"],
    ["✈️", "Offline: Saudável <1s"],
    ["🗺️", "Mapa: 30+ pins MT"],
  ];
  itens.forEach(([ic, t], i) => {
    const ix = 0.3 + i * 3.15;
    s.addShape("rect", { x: ix, y: 4.62, w: 3.0, h: 0.52, fill: { color: C.verde2 }, line: { color: C.ouro, width: 1 } });
    s.addText(`${ic}  ${t}`, { x: ix + 0.1, y: 4.62, w: 2.8, h: 0.52, fontSize: 10.5, bold: true, color: C.branco, valign: "middle" });
  });

  addFooter(s);
}

// ── Slide 10: Próximos Passos + Encerramento ──────────────────────────────────
function slide10(pres) {
  const s = pres.addSlide();
  s.background = { color: C.verde };

  // Faixa ouro topo
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.08, fill: { color: C.ouro }, line: { color: C.ouro } });

  // Título
  s.addText("Obrigado!", {
    x: 0.4, y: 0.15, w: 5, h: 0.65,
    fontSize: 30, bold: true, color: C.ouro
  });
  s.addText("Ceres Diagnóstico — Sprint MVP Concluída", {
    x: 0.4, y: 0.75, w: 9.2, h: 0.35,
    fontSize: 13, color: C.branco
  });

  // 5 cards próximos passos
  const passos = [
    ["01", "Câmera OV5640\nno ESP32-S3", "Diagnóstico autônomo\nsem celular na lavoura"],
    ["02", "Dataset brasileiro\nde tomate", "Imagens reais de MT\n1º dataset com condições BR"],
    ["03", "Retreino com\ndados locais", "Reduzir gap\nlaboratório ↔ campo"],
    ["04", "Validação com\nprodutores reais", "Sorriso-MT e\nCuiabá-MT"],
    ["05", "Artigo científico", "Conferência de\nIA agrícola"],
  ];
  passos.forEach(([n, t, d], i) => {
    const px = 0.35 + i * 1.88;
    s.addShape("rect", { x: px, y: 1.2, w: 1.72, h: 2.4, fill: { color: C.verde2 }, line: { color: C.ouro, width: 1.5 } });
    s.addShape("rect", { x: px, y: 1.2, w: 1.72, h: 0.4, fill: { color: C.ouro }, line: { color: C.ouro } });
    s.addText(n, { x: px, y: 1.2, w: 1.72, h: 0.4, fontSize: 13, bold: true, color: C.verde, align: "center", valign: "middle" });
    s.addText(t, { x: px + 0.08, y: 1.65, w: 1.56, h: 0.7, fontSize: 9.5, bold: true, color: C.ouro, align: "center" });
    s.addText(d, { x: px + 0.08, y: 2.35, w: 1.56, h: 0.8, fontSize: 8.5, color: C.branco, align: "center" });
  });

  // 3 perguntas de validação
  s.addText("Perguntas para validação:", {
    x: 0.4, y: 3.72, w: 9.2, h: 0.3,
    fontSize: 11, bold: true, color: C.ouro
  });
  const pergs = [
    "O diagnóstico por foto resolve o problema do agricultor?",
    "O modo offline é suficiente para uso em lavoura remota?",
    "Quais culturas ou regiões priorizar nos próximos passos?",
  ];
  pergs.forEach((p, i) => {
    s.addText(`${i + 1}. ${p}`, {
      x: 0.4, y: 4.04 + i * 0.3, w: 9.2, h: 0.28,
      fontSize: 10.5, color: C.branco
    });
  });

  // Footer com links
  s.addShape("rect", { x: 0, y: 5.25, w: 10, h: 0.375, fill: { color: "0d1e0d" }, line: { color: C.ouro, width: 0 } });
  s.addText("github.com/Namem/extensao2  ·  ceres.up.railway.app  ·  namem.rachid.jaudy@gmail.com  ·  Junho 2026", {
    x: 0.3, y: 5.25, w: 9.4, h: 0.375,
    fontSize: 8, color: C.ouro, align: "center", valign: "middle"
  });
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Namem Rachid Jaudy Neto";
  pres.title = "Ceres Diagnóstico — Sprint MVP";

  console.log("Gerando slides...");
  slide1(pres);  console.log("  ✓ Slide 1: Capa");
  slide2(pres);  console.log("  ✓ Slide 2: O Problema");
  slide3(pres);  console.log("  ✓ Slide 3: Roadmap");
  slide4(pres);  console.log("  ✓ Slide 4: Evolução");
  slide5(pres);  console.log("  ✓ Slide 5: A Solução");
  slide6(pres);  console.log("  ✓ Slide 6: Diagnóstico + Offline");
  slide7(pres);  console.log("  ✓ Slide 7: Hardware IoT");
  slide8(pres);  console.log("  ✓ Slide 8: Resultados");
  slide9(pres);  console.log("  ✓ Slide 9: Demo ao Vivo");
  slide10(pres); console.log("  ✓ Slide 10: Próximos Passos");

  const out = path.join(OUT_DIR, "sprint_mvp_extensao2.pptx");
  await pres.writeFile({ fileName: out });
  console.log(`\n✅ Salvo em: ${out}`);
}

main().catch(e => { console.error("ERRO:", e.message); process.exit(1); });
