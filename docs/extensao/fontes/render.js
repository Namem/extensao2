// Renderiza os SVG dos diagramas para PNG em alta resolucao (resvg).
const fs = require("fs");
const path = require("path");
const { Resvg } = require(path.join(
  "C:/Users/Rachid/AppData/Local/Temp/claude/C--Users-Rachid-Desktop-NR-Semestre-2026-1-extensao-ceres-diagnostico--claude-worktrees-keen-borg-09cccb/d5f05484-c972-4d12-ae8e-05516e2508a0/scratchpad/node_modules/@resvg/resvg-js"
));

const dir = "C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/extensao/anexos/diagramas";
const files = ["casos_de_uso", "arquitetura", "diagrama_classes", "mer", "roadmap"];
for (const f of files) {
  const svg = fs.readFileSync(path.join(dir, f + ".svg"), "utf8");
  const r = new Resvg(svg, { fitTo: { mode: "zoom", value: 2 } });
  const png = r.render().asPng();
  fs.writeFileSync(path.join(dir, f + ".png"), png);
  console.log(f + ".png  " + (png.length / 1024).toFixed(0) + " KB");
}
