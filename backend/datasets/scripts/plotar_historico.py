"""
plotar_historico.py — Gera grafico de curvas de treinamento (accuracy + loss)

Le historico_treino.csv e salva PNG em docs/historico_treino.png.
Marca visualmente Fase 1 vs Fase 2 e a melhor epoca.

Uso:
    python plotar_historico.py

Saida:
    docs/assets/historico_treino.png
"""

import csv
from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------

BASE_DIR  = Path(__file__).resolve().parents[2]
CSV_PATH  = BASE_DIR / "datasets" / "modelo" / "historico_treino.csv"
OUT_PNG   = BASE_DIR.parent / "docs" / "assets" / "historico_treino.png"

# ---------------------------------------------------------------------------
# Ler CSV
# ---------------------------------------------------------------------------

fase1 = {"epoch": [], "loss": [], "accuracy": [], "val_loss": [], "val_accuracy": []}
fase2 = {"epoch": [], "loss": [], "accuracy": [], "val_loss": [], "val_accuracy": []}

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    ep_global = 0
    for row in reader:
        ep_global += 1
        alvo = fase1 if row["fase"] == "1" else fase2
        alvo["epoch"].append(ep_global)
        alvo["loss"].append(float(row["loss"]))
        alvo["accuracy"].append(float(row["accuracy"]) * 100)
        alvo["val_loss"].append(float(row["val_loss"]))
        alvo["val_accuracy"].append(float(row["val_accuracy"]) * 100)

# Melhor val_acc da fase 2
melhor_ep  = fase2["epoch"][fase2["val_accuracy"].index(max(fase2["val_accuracy"]))]
melhor_acc = max(fase2["val_accuracy"])
divisao    = fase1["epoch"][-1]   # ultimo epoch da fase 1

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

try:
    import matplotlib
    matplotlib.use("Agg")   # sem janela — salva direto em arquivo
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("[ERRO] matplotlib nao instalado.")
    print("  pip install matplotlib")
    raise SystemExit(1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
fig.suptitle(
    "Ceres Diagnóstico — MobileNetV2 96×96 INT8\nCurvas de Treinamento (Exp B)",
    fontsize=13, fontweight="bold"
)

AZUL     = "#1f77b4"
LARANJA  = "#ff7f0e"
CINZA    = "#cccccc"

todas_ep  = fase1["epoch"] + fase2["epoch"]
todas_acc = fase1["accuracy"] + fase2["accuracy"]
todas_vac = fase1["val_accuracy"] + fase2["val_accuracy"]
todas_los = fase1["loss"] + fase2["loss"]
todas_vlo = fase1["val_loss"] + fase2["val_loss"]

# --- Accuracy ---
ax1.plot(todas_ep, todas_acc, color=AZUL,    label="Train acc",  linewidth=1.8)
ax1.plot(todas_ep, todas_vac, color=LARANJA, label="Val acc",    linewidth=1.8)
ax1.axvline(divisao, color=CINZA, linestyle="--", linewidth=1.2)
ax1.axvline(melhor_ep, color="green", linestyle=":", linewidth=1.5,
            label=f"Melhor val acc (ep {melhor_ep}: {melhor_acc:.2f}%)")
ax1.annotate(
    f"{melhor_acc:.2f}%",
    xy=(melhor_ep, melhor_acc),
    xytext=(melhor_ep + 1.5, melhor_acc - 3),
    fontsize=8, color="green",
    arrowprops=dict(arrowstyle="->", color="green", lw=1)
)
ax1.set_ylabel("Acurácia (%)", fontsize=10)
ax1.set_ylim(75, 101)
ax1.legend(fontsize=8, loc="lower right")
ax1.grid(True, alpha=0.3)
ax1.text(divisao / 2, 76.5, "Fase 1\n(backbone congelado)", ha="center",
         fontsize=8, color="gray")
ax1.text((divisao + todas_ep[-1]) / 2, 76.5, "Fase 2\n(fine-tuning 30 camadas)",
         ha="center", fontsize=8, color="gray")

# --- Loss ---
ax2.plot(todas_ep, todas_los, color=AZUL,    label="Train loss", linewidth=1.8)
ax2.plot(todas_ep, todas_vlo, color=LARANJA, label="Val loss",   linewidth=1.8)
ax2.axvline(divisao, color=CINZA, linestyle="--", linewidth=1.2)
ax2.axvline(melhor_ep, color="green", linestyle=":", linewidth=1.5)
ax2.set_ylabel("Loss", fontsize=10)
ax2.set_xlabel("Época global", fontsize=10)
ax2.legend(fontsize=8, loc="upper right")
ax2.grid(True, alpha=0.3)

# Anotacao final
ax1.annotate(
    f"Test set: 98,13%\n(2.734 imgs)",
    xy=(todas_ep[-1], todas_acc[-1]),
    xytext=(todas_ep[-1] - 8, 82),
    fontsize=8, color=AZUL,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="gray"),
    arrowprops=dict(arrowstyle="->", color=AZUL, lw=1)
)

plt.tight_layout()
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
print(f"Salvo em: {OUT_PNG}")
