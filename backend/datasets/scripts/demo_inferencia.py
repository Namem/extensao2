"""
demo_inferencia.py — Demo visual de inferencia do modelo Ceres

Classifica imagens usando ceres_mobilenetv2_int8.tflite e exibe
predicao, confianca e barra visual no terminal. Salva relatorio MD.

Uso:
    # Uma imagem
    python demo_inferencia.py --imagem caminho/foto.jpg

    # Pasta inteira
    python demo_inferencia.py --pasta caminho/pasta/

    # Pasta com limite de imagens
    python demo_inferencia.py --pasta caminho/pasta/ --max 20

Saida:
    Terminal: tabela com predicao + barra de confianca
    docs/demo_results.md: relatorio completo
"""

import argparse
import sys
import time
from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------

BASE_DIR    = Path(__file__).resolve().parents[2]
MODELO_PATH = BASE_DIR / "datasets" / "modelo" / "ceres_mobilenetv2_int8.tflite"
RESULTADO   = BASE_DIR.parent / "docs" / "demo_results.md"
IMG_SIZE    = 96

CLASSES_CERES = sorted([
    "D01_requeima", "D02_septoriose", "D03_pinta_preta",
    "D03b_mancha_alvo", "D05_mofo_foliar", "D06_vira_cabeca",
    "D06b_mosaico", "D07_acaro_bronzeamento", "D09_mancha_bacteriana",
    "saudavel"
])

NOMES_PT = {
    "D01_requeima"          : "Requeima",
    "D02_septoriose"        : "Septoriose",
    "D03_pinta_preta"       : "Pinta Preta",
    "D03b_mancha_alvo"      : "Mancha Alvo",
    "D05_mofo_foliar"       : "Mofo Foliar",
    "D06_vira_cabeca"       : "Vira-Cabeca",
    "D06b_mosaico"          : "Mosaico",
    "D07_acaro_bronzeamento": "Acaro Bronzeamento",
    "D09_mancha_bacteriana" : "Mancha Bacteriana",
    "saudavel"              : "Saudavel",
}

# Cores terminal
VERDE   = "\033[92m"
AMARELO = "\033[93m"
VERMELHO= "\033[91m"
AZUL    = "\033[94m"
RESET   = "\033[0m"
NEGRITO = "\033[1m"

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Demo de inferencia Ceres")
grupo = parser.add_mutually_exclusive_group(required=True)
grupo.add_argument("--imagem", type=str, help="Caminho de uma imagem")
grupo.add_argument("--pasta",  type=str, help="Caminho de uma pasta de imagens")
parser.add_argument("--max",   type=int, default=0,
                    help="Maximo de imagens da pasta (0 = todas)")
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Carregar modelo
# ---------------------------------------------------------------------------

try:
    import tensorflow as tf
    interp = tf.lite.Interpreter(model_path=str(MODELO_PATH))
except ImportError:
    try:
        import tflite_runtime.interpreter as tflite
        interp = tflite.Interpreter(model_path=str(MODELO_PATH))
    except ImportError:
        print("[ERRO] Instale tensorflow ou tflite-runtime:")
        print("  pip install tflite-runtime")
        raise SystemExit(1)

interp.allocate_tensors()
inp = interp.get_input_details()[0]
out = interp.get_output_details()[0]
esc_in,  zp_in  = inp["quantization"]
esc_out, zp_out = out["quantization"]

# ---------------------------------------------------------------------------
# Funcao de inferencia
# ---------------------------------------------------------------------------

def inferir(caminho: Path):
    """Retorna (classe, confianca_float, tempo_ms, scores_todos)."""
    img = Image.open(caminho).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32) / 127.5 - 1.0
    arr_int8 = np.round(arr / esc_in + zp_in).clip(-128, 127).astype(np.int8)
    arr_int8 = arr_int8[np.newaxis, ...]

    t0 = time.perf_counter()
    interp.set_tensor(inp["index"], arr_int8)
    interp.invoke()
    t1 = time.perf_counter()

    saida = interp.get_tensor(out["index"])[0]
    scores = (saida.astype(np.float32) - zp_out) * esc_out

    # Softmax para converter logits em probabilidades
    exp = np.exp(scores - scores.max())
    probs = exp / exp.sum()

    idx = int(np.argmax(probs))
    return CLASSES_CERES[idx], float(probs[idx]), (t1 - t0) * 1000, probs

# ---------------------------------------------------------------------------
# Coletar imagens
# ---------------------------------------------------------------------------

EXTS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

if args.imagem:
    imagens = [Path(args.imagem)]
else:
    pasta = Path(args.pasta)
    if not pasta.exists():
        print(f"[ERRO] Pasta nao encontrada: {pasta}")
        raise SystemExit(1)
    imagens = [p for p in pasta.rglob("*") if p.suffix in EXTS]
    imagens.sort()
    if args.max > 0:
        imagens = imagens[:args.max]

if not imagens:
    print("[ERRO] Nenhuma imagem encontrada.")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# Executar e exibir
# ---------------------------------------------------------------------------

print()
print(f"{NEGRITO}{'='*65}{RESET}")
print(f"{NEGRITO}  Ceres Diagnostico — Demo de Inferencia{RESET}")
print(f"  Modelo : ceres_mobilenetv2_int8.tflite (639 KB)")
print(f"  Imagens: {len(imagens)}")
print(f"{'='*65}{RESET}")
print()

LARGURA_BARRA = 25

resultados = []
for img_path in imagens:
    try:
        classe, confianca, ms, probs = inferir(img_path)
    except Exception as e:
        print(f"  {VERMELHO}[ERRO]{RESET} {img_path.name}: {e}")
        continue

    nome_pt = NOMES_PT.get(classe, classe)

    # Barra de confianca
    preenchido = int(confianca * LARGURA_BARRA)
    barra = "█" * preenchido + "░" * (LARGURA_BARRA - preenchido)

    # Cor por confianca
    if confianca >= 0.80:
        cor = VERDE
    elif confianca >= 0.50:
        cor = AMARELO
    else:
        cor = VERMELHO

    print(f"  {AZUL}{img_path.name:<30}{RESET} "
          f"{cor}{nome_pt:<20}{RESET} "
          f"{cor}[{barra}]{RESET} "
          f"{cor}{confianca*100:5.1f}%{RESET}  "
          f"{ms:5.1f}ms")

    resultados.append({
        "arquivo"   : img_path.name,
        "classe"    : classe,
        "nome_pt"   : nome_pt,
        "confianca" : confianca,
        "ms"        : ms,
        "probs"     : probs,
    })

# ---------------------------------------------------------------------------
# Resumo
# ---------------------------------------------------------------------------

if resultados:
    media_conf = sum(r["confianca"] for r in resultados) / len(resultados)
    media_ms   = sum(r["ms"]        for r in resultados) / len(resultados)
    acima_80   = sum(1 for r in resultados if r["confianca"] >= 0.80)
    abaixo_50  = sum(1 for r in resultados if r["confianca"] < 0.50)

    print()
    print(f"  {'─'*63}")
    print(f"  {NEGRITO}Resumo{RESET}")
    print(f"  Total processadas : {len(resultados)}")
    print(f"  Confianca media   : {media_conf*100:.1f}%")
    print(f"  Latencia media    : {media_ms:.1f} ms")
    print(f"  Alta confianca (>= 80%) : {acima_80}  "
          f"{VERDE}{'█'*acima_80}{RESET}")
    print(f"  Baixa confianca  (< 50%): {abaixo_50}  "
          f"{VERMELHO}{'█'*abaixo_50}{RESET}")
    print()

    # Distribuicao de classes preditas
    from collections import Counter
    dist = Counter(r["classe"] for r in resultados)
    print(f"  {NEGRITO}Distribuicao de predicoes:{RESET}")
    for cls, n in dist.most_common():
        barra = "█" * n
        print(f"    {NOMES_PT.get(cls, cls):<22} {n:3}x  {barra}")

# ---------------------------------------------------------------------------
# Salvar relatorio Markdown
# ---------------------------------------------------------------------------

with open(RESULTADO, "w", encoding="utf-8") as f:
    f.write("# Demo de Inferencia — Ceres Diagnostico\n\n")
    f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB)\n")
    f.write(f"**Total imagens:** {len(resultados)}\n\n")
    f.write("| Arquivo | Predicao | Confianca | Latencia |\n")
    f.write("|---|---|---|---|\n")
    for r in resultados:
        barra = "█" * int(r["confianca"] * 10) + "░" * (10 - int(r["confianca"] * 10))
        f.write(f"| {r['arquivo']} | {r['nome_pt']} ({r['classe']}) "
                f"| {barra} {r['confianca']*100:.1f}% | {r['ms']:.1f}ms |\n")
    if resultados:
        f.write(f"\n**Confianca media:** {media_conf*100:.1f}%  \n")
        f.write(f"**Latencia media:** {media_ms:.1f} ms  \n")

print(f"  Relatorio salvo em: {RESULTADO}")
