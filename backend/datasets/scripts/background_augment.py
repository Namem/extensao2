"""
background_augment.py — Augmentacao com remocao de fundo e recomposicao natural

Estrategia para resolver o gap laboratorio-campo (lab-to-field gap):
  1. Remove o fundo cinza/preto do PlantVillage com rembg (U2-Net)
  2. Recompoe a folha sobre fundos naturais retirados do PlantDoc
  3. Salva dataset augmentado em datasets/processed_field/train

Baseado em Singh et al. (2020): apenas remover o fundo das imagens
aumentou a acuracia no PlantDoc de 29,73% para 70,53% (+40,8 pp).
DOI: 10.1145/3371158.3371196

Uso:
    # Teste rapido: 10 imagens por classe
    python background_augment.py --sample 10

    # Processamento completo (lento — ~2-8h dependendo da CPU/GPU)
    python background_augment.py

    # Gerar 3 composicoes por imagem (mais dados de treino)
    python background_augment.py --n-backgrounds 3 --sample 20

Saida:
    datasets/processed_field/train/<classe>/
        <nome>.jpg          — original copiado (fundo controlado)
        <nome>_bg0.jpg      — folha + fundo PlantDoc aleatorio #1
        <nome>_bg1.jpg      — folha + fundo PlantDoc aleatorio #2
        ...

    docs/background_augment_stats.md  — relatorio de execucao

Dependencias (instalar no venv):
    pip install rembg[gpu] tqdm pillow onnxruntime-gpu
    # Se nao tiver GPU CUDA disponivel:
    pip install rembg tqdm pillow onnxruntime
"""

import argparse
import random
import shutil
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuracoes de caminho
# ---------------------------------------------------------------------------

BASE_DIR      = Path(__file__).resolve().parents[2]          # backend/
SOURCE_TRAIN  = BASE_DIR / "datasets" / "processed" / "train"
PLANTDOC_DIR  = BASE_DIR / "datasets" / "raw" / "plantdoc" / "train"
OUTPUT_TRAIN  = BASE_DIR / "datasets" / "processed_field" / "train"
RESULTADO     = BASE_DIR.parent / "docs" / "background_augment_stats.md"

IMG_SIZE = 96   # mesma resolucao do treinamento original

# ---------------------------------------------------------------------------
# Argparse
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="Remove fundo PlantVillage e recompoe sobre fundos naturais PlantDoc"
)
parser.add_argument(
    "--sample", type=int, default=0,
    help="Processar apenas N imagens por classe (0 = todas). Use para testar."
)
parser.add_argument(
    "--n-backgrounds", type=int, default=2,
    help="Quantas composicoes gerar por imagem (default: 2)."
)
parser.add_argument(
    "--model", type=str, default="u2net",
    choices=["u2net", "u2net_human_seg", "isnet-general-use", "silueta"],
    help="Modelo rembg para segmentacao (default: u2net — melhor qualidade)."
)
parser.add_argument(
    "--skip-original", action="store_true",
    help="Nao copiar imagens originais para o destino (so composicoes)."
)
parser.add_argument(
    "--seed", type=int, default=42,
    help="Seed aleatorio para reproducibilidade (default: 42)."
)
args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)

# ---------------------------------------------------------------------------
# Importar rembg (verificar instalacao)
# ---------------------------------------------------------------------------

try:
    from rembg import remove, new_session
except ImportError:
    print("\n[ERRO] rembg nao encontrado. Instale com:")
    print("    pip install rembg[gpu] onnxruntime-gpu")
    print("    # ou sem GPU:")
    print("    pip install rembg onnxruntime")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# Verificacoes iniciais
# ---------------------------------------------------------------------------

print("=" * 60)
print("Ceres Diagnostico — Background Augmentation")
print("=" * 60)
print(f"Fonte       : {SOURCE_TRAIN}")
print(f"Fundos (PD) : {PLANTDOC_DIR}")
print(f"Saida       : {OUTPUT_TRAIN}")
print(f"Modelo rembg: {args.model}")
print(f"Composicoes : {args.n_backgrounds} por imagem")
print(f"Sample      : {'todas' if args.sample == 0 else f'{args.sample} por classe'}")
print()

if not SOURCE_TRAIN.exists():
    print(f"[ERRO] Pasta de treino nao encontrada: {SOURCE_TRAIN}")
    print("Execute primeiro: python prepare_plantvillage.py")
    raise SystemExit(1)

if not PLANTDOC_DIR.exists():
    print(f"[ERRO] PlantDoc nao encontrado: {PLANTDOC_DIR}")
    print("Copie o PlantDoc para datasets/raw/plantdoc/")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# Carregar todos os fundos do PlantDoc
# ---------------------------------------------------------------------------

print("Carregando fundos do PlantDoc...")
exts = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
fundos = [
    p for p in PLANTDOC_DIR.rglob("*")
    if p.is_file() and p.suffix in exts
]

if not fundos:
    print(f"[ERRO] Nenhuma imagem encontrada em {PLANTDOC_DIR}")
    raise SystemExit(1)

print(f"  {len(fundos)} imagens de fundo disponiveis do PlantDoc")
print()

# ---------------------------------------------------------------------------
# Carregar modelo rembg uma unica vez (evita recarregar a cada imagem)
# ---------------------------------------------------------------------------

print(f"Carregando modelo rembg '{args.model}' (pode demorar na 1a vez)...")
session = new_session(args.model)
print("  Modelo carregado.")
print()

# ---------------------------------------------------------------------------
# Funcoes auxiliares
# ---------------------------------------------------------------------------

def remover_fundo(img_path: Path, sess) -> Image.Image:
    """
    Remove o fundo de uma imagem usando rembg.
    Retorna imagem RGBA com fundo transparente.
    """
    with open(img_path, "rb") as f:
        dados = f.read()
    saida = remove(dados, session=sess)
    from io import BytesIO
    return Image.open(BytesIO(saida)).convert("RGBA")


def compor_sobre_fundo(folha_rgba: Image.Image, fundo_path: Path) -> Image.Image:
    """
    Recompoe a folha (RGBA) sobre um fundo natural do PlantDoc.
    Retorna imagem RGB 96x96.
    """
    # Carregar e redimensionar fundo para 96x96
    fundo = Image.open(fundo_path).convert("RGB").resize(
        (IMG_SIZE, IMG_SIZE), Image.LANCZOS
    )

    # Redimensionar folha para 96x96 (mantendo RGBA)
    folha = folha_rgba.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)

    # Composicao: colar folha sobre fundo usando o canal alpha como mascara
    resultado = fundo.copy()
    resultado.paste(folha, (0, 0), mask=folha.split()[3])  # canal A como mascara

    return resultado


def salvar_jpg(img: Image.Image, destino: Path, qualidade: int = 92):
    """Salva imagem RGB como JPEG."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(destino, "JPEG", quality=qualidade)


# ---------------------------------------------------------------------------
# Processar cada classe
# ---------------------------------------------------------------------------

classes = sorted([p for p in SOURCE_TRAIN.iterdir() if p.is_dir()])

if not classes:
    print(f"[ERRO] Nenhuma subpasta de classe encontrada em {SOURCE_TRAIN}")
    raise SystemExit(1)

print(f"Classes encontradas: {len(classes)}")
for c in classes:
    print(f"  {c.name}")
print()

# Estatisticas globais
stats = {}
total_geradas = 0
total_erros   = 0
t_inicio      = time.time()

for pasta_classe in classes:
    nome_classe = pasta_classe.name
    imagens = sorted(
        p for p in pasta_classe.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )

    # Limitar ao sample se solicitado
    if args.sample > 0:
        imagens = imagens[:args.sample]

    pasta_saida = OUTPUT_TRAIN / nome_classe
    pasta_saida.mkdir(parents=True, exist_ok=True)

    geradas_classe  = 0
    puladas_classe  = 0
    erros_classe    = 0

    desc = f"{nome_classe:<35}"
    for img_path in tqdm(imagens, desc=desc, unit="img", ncols=80):
        stem = img_path.stem

        # --- Copiar original (se nao pulando) ---
        if not args.skip_original:
            dest_orig = pasta_saida / img_path.name
            if not dest_orig.exists():
                shutil.copy2(img_path, dest_orig)

        # --- Checar se composicoes ja existem (resumivel) ---
        composicoes_faltam = [
            i for i in range(args.n_backgrounds)
            if not (pasta_saida / f"{stem}_bg{i}.jpg").exists()
        ]

        if not composicoes_faltam:
            puladas_classe += args.n_backgrounds
            continue

        # --- Remover fundo ---
        try:
            folha_rgba = remover_fundo(img_path, session)
        except Exception as e:
            erros_classe += 1
            tqdm.write(f"  [ERRO remocao] {img_path.name}: {e}")
            continue

        # --- Compor sobre N fundos aleatorios ---
        for i in composicoes_faltam:
            fundo_escolhido = random.choice(fundos)
            dest = pasta_saida / f"{stem}_bg{i}.jpg"
            try:
                composta = compor_sobre_fundo(folha_rgba, fundo_escolhido)
                salvar_jpg(composta, dest)
                geradas_classe += 1
            except Exception as e:
                erros_classe += 1
                tqdm.write(f"  [ERRO composicao] {img_path.name} bg{i}: {e}")

    total_geradas += geradas_classe
    total_erros   += erros_classe

    stats[nome_classe] = {
        "imagens_fonte"  : len(imagens),
        "composicoes"    : geradas_classe,
        "puladas"        : puladas_classe,
        "erros"          : erros_classe,
    }

    tqdm.write(
        f"  {nome_classe}: {len(imagens)} imgs → "
        f"+{geradas_classe} composicoes | "
        f"{puladas_classe} ja existiam | "
        f"{erros_classe} erros"
    )

# ---------------------------------------------------------------------------
# Relatorio final
# ---------------------------------------------------------------------------

t_total = time.time() - t_inicio
mins    = int(t_total // 60)
segs    = int(t_total % 60)

print()
print("=" * 60)
print(f"Concluido em {mins}m {segs}s")
print(f"Total composicoes geradas : {total_geradas}")
print(f"Total erros               : {total_erros}")
print(f"Saida                     : {OUTPUT_TRAIN}")
print("=" * 60)

# ---------------------------------------------------------------------------
# Salvar relatorio Markdown
# ---------------------------------------------------------------------------

RESULTADO.parent.mkdir(parents=True, exist_ok=True)
with open(RESULTADO, "w", encoding="utf-8") as f:
    f.write("# Background Augmentation — Relatorio de Execucao\n\n")
    f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Modelo rembg:** {args.model}\n")
    f.write(f"**Composicoes por imagem:** {args.n_backgrounds}\n")
    f.write(f"**Sample:** {'todas' if args.sample == 0 else args.sample}\n")
    f.write(f"**Duracao:** {mins}m {segs}s\n\n")

    f.write("## Estrategia\n\n")
    f.write("Baseado em Singh et al. (2020): remocao de fundo no PlantDoc\n")
    f.write("aumentou acuracia de 29,73% para 70,53% (+40,8 pp).\n")
    f.write("Aqui aplicamos a estrategia inversa: inserimos fundos naturais\n")
    f.write("nas imagens PlantVillage para o modelo aprender a ignorar o fundo.\n\n")

    f.write("## Resultado por Classe\n\n")
    f.write("| Classe | Imgs fonte | Composicoes | Puladas | Erros |\n")
    f.write("|---|---|---|---|---|\n")
    for cls, v in stats.items():
        f.write(
            f"| {cls} | {v['imagens_fonte']} | "
            f"{v['composicoes']} | {v['puladas']} | {v['erros']} |\n"
        )
    f.write("\n## Resultado Geral\n\n")
    f.write("| Metrica | Valor |\n|---|---|\n")
    total_fonte = sum(v["imagens_fonte"] for v in stats.values())
    f.write(f"| Total imagens fonte | {total_fonte} |\n")
    f.write(f"| Total composicoes geradas | {total_geradas} |\n")
    f.write(f"| Total erros | {total_erros} |\n")
    f.write(f"| Tempo total | {mins}m {segs}s |\n\n")
    f.write("## Proximo Passo\n\n")
    f.write("Retreinar o modelo com o dataset augmentado:\n\n")
    f.write("```bash\n")
    f.write("# No WSL2, com o novo dataset:\n")
    f.write("python train_local.py --data-dir datasets/processed_field\n")
    f.write("```\n\n")
    f.write("Em seguida, rodar novamente a avaliacao PlantDoc:\n\n")
    f.write("```bash\n")
    f.write("python avaliar_plantdoc.py\n")
    f.write("```\n")

print(f"\nRelatorio salvo em: {RESULTADO}")
print()
print("Proximo passo:")
print("  1. Verifique algumas imagens em datasets/processed_field/train/")
print("  2. Se a qualidade estiver boa, retreine:")
print("       python train_local.py  (no WSL2, aponte para processed_field)")
print("  3. Rode avaliar_plantdoc.py novamente para medir a melhora")
