"""
Prepara dataset misto PlantVillage + PlantDoc para Experimento D.

processed_mixed/train/ = PlantVillage train (symlinks) + PlantDoc/train (copiado N vezes)
processed_mixed/val    = symlink para processed/val  (PlantVillage — avaliação justa)
processed_mixed/test   = symlink para processed/test (PlantVillage — avaliação justa)

Avaliação de campo: continua usando avaliar_plantdoc.py separadamente.

Uso:
    python3 preparar_mixed.py                    # padrão: 10 repetições PlantDoc
    python3 preparar_mixed.py --repeticoes 5
    python3 preparar_mixed.py --limpar           # apaga processed_mixed/ e recria
"""

import argparse
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Argumentos
# ---------------------------------------------------------------------------

_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument("--repeticoes", type=int, default=10,
    help="Quantas vezes repetir cada imagem PlantDoc (default: 10)")
_parser.add_argument("--limpar", action="store_true",
    help="Remove processed_mixed/ antes de recriar")
_args, _ = _parser.parse_known_args()

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------

BASE_DIR       = Path(__file__).resolve().parents[2]
PROCESSED      = BASE_DIR / "datasets" / "processed"
PLANTDOC_TRAIN = BASE_DIR / "datasets" / "raw" / "plantdoc" / "train"
MIXED          = BASE_DIR / "datasets" / "processed_mixed"

# Mapeamento PlantDoc → classe Ceres (mesma ordem do avaliar_plantdoc.py)
MAPA_CLASSES = {
    "Tomato leaf late blight"              : "D01_requeima",
    "Tomato Septoria leaf spot"            : "D02_septoriose",
    "Tomato Early blight leaf"             : "D03_pinta_preta",
    "Tomato mold leaf"                     : "D05_mofo_foliar",
    "Tomato leaf yellow virus"             : "D06_vira_cabeca",
    "Tomato leaf mosaic virus"             : "D06b_mosaico",
    "Tomato two spotted spider mites leaf" : "D07_acaro_bronzeamento",
    "Tomato leaf bacterial spot"           : "D09_mancha_bacteriana",
    "Tomato leaf"                          : "saudavel",
}

REPETICOES = _args.repeticoes

# ---------------------------------------------------------------------------
# Limpeza opcional
# ---------------------------------------------------------------------------

if _args.limpar and MIXED.exists():
    print(f"Removendo {MIXED} ...")
    shutil.rmtree(MIXED)

# ---------------------------------------------------------------------------
# 1. Criar pastas de classe (10 classes Ceres)
# ---------------------------------------------------------------------------

mixed_train = MIXED / "train"
mixed_train.mkdir(parents=True, exist_ok=True)

classes = sorted([d.name for d in (PROCESSED / "train").iterdir() if d.is_dir()])
for cls in classes:
    (mixed_train / cls).mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 2. Symlinks PlantVillage → processed_mixed/train/
# ---------------------------------------------------------------------------

print("Criando symlinks PlantVillage → processed_mixed/train/ ...")
total_pv = 0
for cls in classes:
    src_dir = PROCESSED / "train" / cls
    dst_dir = mixed_train / cls
    for img in src_dir.glob("*.*"):
        dst = dst_dir / img.name
        if not dst.exists():
            dst.symlink_to(img.resolve())
        total_pv += 1

print(f"  {total_pv:,} symlinks criados")

# ---------------------------------------------------------------------------
# 3. Copiar PlantDoc/train N vezes → processed_mixed/train/
# ---------------------------------------------------------------------------

print(f"\nCopiando PlantDoc/train × {REPETICOES} → processed_mixed/train/ ...")
total_pd_unico = 0
total_pd_copiado = 0

for pasta_pd, classe_ceres in MAPA_CLASSES.items():
    pasta = PLANTDOC_TRAIN / pasta_pd
    if not pasta.exists():
        print(f"  [AVISO] Pasta PlantDoc não encontrada: {pasta_pd}")
        continue

    imgs = list(pasta.glob("*.jpg")) + list(pasta.glob("*.JPG")) + \
           list(pasta.glob("*.png")) + list(pasta.glob("*.jpeg"))

    if not imgs:
        print(f"  [AVISO] Nenhuma imagem em: {pasta_pd}")
        continue

    dst_dir = mixed_train / classe_ceres
    for rep in range(REPETICOES):
        for img in imgs:
            stem = f"pd_r{rep:02d}_{img.stem}{img.suffix}"
            dst  = dst_dir / stem
            if not dst.exists():
                shutil.copy2(img, dst)
            total_pd_copiado += 1

    total_pd_unico += len(imgs)
    print(f"  {classe_ceres:<35} {len(imgs):>3} imgs × {REPETICOES} = {len(imgs)*REPETICOES}")

print(f"\n  {total_pd_unico} imagens PlantDoc únicas → {total_pd_copiado:,} cópias no treino")

# ---------------------------------------------------------------------------
# 4. Symlinks val e test (PlantVillage — avaliação justa)
# ---------------------------------------------------------------------------

for split in ["val", "test"]:
    dst = MIXED / split
    src = (PROCESSED / split).resolve()
    if not dst.exists():
        dst.symlink_to(src)
        print(f"  Symlink {split}: {src}")

# ---------------------------------------------------------------------------
# 5. Estatísticas finais
# ---------------------------------------------------------------------------

print("\n=== processed_mixed/train — imagens por classe ===")
total_geral = 0
for cls in classes:
    n = len(list((mixed_train / cls).iterdir()))
    pv = len(list((PROCESSED / "train" / cls).glob("*.*")))
    pd = n - pv
    print(f"  {cls:<35} {n:>7} total  ({pv} PV + {pd} PD)")
    total_geral += n

print(f"  {'TOTAL':<35} {total_geral:>7}")
print(f"\n  Proporção PlantDoc no treino: "
      f"{total_pd_copiado/total_geral*100:.1f}%")

print(f"""
=== Próximos passos ===
1. Retreinar Exp D:
   python3 train_local.py --data-dir datasets/processed_mixed

2. Avaliar campo:
   python3 avaliar_plantdoc.py

3. Comparar com Exp B (20,77%) e Exp C (20,24%)
""")
