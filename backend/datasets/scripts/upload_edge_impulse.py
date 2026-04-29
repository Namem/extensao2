"""
Upload do dataset processado para o Edge Impulse via API REST.

Uso:
    python datasets/scripts/upload_edge_impulse.py

Pre-requisitos:
    - EDGE_IMPULSE_API_KEY no arquivo backend/.env
    - Dataset processado em backend/datasets/processed/train/ e /val/
    - pip install requests python-dotenv tqdm

O split /test/ NAO e enviado — reservado para benchmark final no ESP32-S3.
"""

import os
import sys
import time
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dotenv import load_dotenv

try:
    from tqdm import tqdm
except ImportError:
    raise SystemExit("tqdm nao instalado. Execute: pip install tqdm")

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"
PROCESSED_DIR = BASE_DIR / "datasets" / "processed"

load_dotenv(ENV_FILE)

API_KEY = os.getenv("EDGE_IMPULSE_API_KEY")
if not API_KEY:
    raise SystemExit("EDGE_IMPULSE_API_KEY nao encontrada no .env")

INGESTION_URL = "https://ingestion.edgeimpulse.com/api/{category}/files"

# Mapeamento split local -> categoria Edge Impulse
SPLITS = {
    "train": "training",
    "val":   "testing",   # Edge Impulse chama de "testing" o que usamos como val
    # "test" NAO sobe — reservado para benchmark final
}

WORKERS     = 4    # uploads paralelos
BATCH_DELAY = 0.1  # segundos entre batches (evitar rate limit)
EXTENSIONS  = {".jpg", ".jpeg", ".png"}

LOG_FILE = BASE_DIR / "datasets" / "upload_log.txt"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Upload de um arquivo
# ---------------------------------------------------------------------------

def upload_file(img_path: Path, category: str, label: str) -> tuple[bool, str]:
    """
    Envia um arquivo de imagem para o Edge Impulse.
    Retorna (sucesso, mensagem).
    """
    url = INGESTION_URL.format(category=category)
    headers = {
        "x-api-key": API_KEY,
        "x-label":   label,
        "x-add-date-id": "true",
    }
    try:
        with open(img_path, "rb") as f:
            resp = requests.post(
                url,
                headers=headers,
                files={"data": (img_path.name, f, "image/jpeg")},
                timeout=30,
            )
        if resp.status_code in (200, 201):
            return True, ""
        return False, f"{img_path.name}: HTTP {resp.status_code} — {resp.text[:120]}"
    except Exception as exc:
        return False, f"{img_path.name}: {exc}"


# ---------------------------------------------------------------------------
# Upload de uma classe inteira
# ---------------------------------------------------------------------------

def upload_class(class_dir: Path, category: str, label: str) -> tuple[int, int]:
    """
    Faz upload de todas as imagens de uma classe.
    Retorna (enviados, erros).
    """
    imagens = [f for f in class_dir.iterdir() if f.suffix.lower() in EXTENSIONS]
    if not imagens:
        log.warning("Nenhuma imagem em %s", class_dir)
        return 0, 0

    enviados = erros = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(upload_file, img, category, label): img
            for img in imagens
        }
        with tqdm(total=len(imagens), desc=f"  {label}", unit="img", leave=False) as bar:
            for future in as_completed(futures):
                ok, msg = future.result()
                if ok:
                    enviados += 1
                else:
                    erros += 1
                    log.error(msg)
                bar.update(1)
        time.sleep(BATCH_DELAY)

    return enviados, erros


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def main():
    if not PROCESSED_DIR.exists():
        raise SystemExit(
            f"[ERRO] Pasta processed/ nao encontrada em:\n  {PROCESSED_DIR}\n"
            "Execute primeiro: python datasets/scripts/prepare_plantvillage.py"
        )

    log.info("=== Ceres Diagnostico — Upload Edge Impulse ===")
    log.info("API Key: %s...%s", API_KEY[:8], API_KEY[-4:])
    log.info("Splits a enviar: train -> training | val -> testing")
    log.info("Split test/ NAO sera enviado (reservado para benchmark)\n")

    total_env = total_err = 0

    for split_local, categoria_ei in SPLITS.items():
        split_dir = PROCESSED_DIR / split_local
        if not split_dir.exists():
            log.warning("Pasta %s nao encontrada, pulando.", split_dir)
            continue

        classes = sorted([d for d in split_dir.iterdir() if d.is_dir()])
        log.info("--- %s -> %s (%d classes) ---", split_local, categoria_ei, len(classes))

        for class_dir in classes:
            label = class_dir.name
            env, err = upload_class(class_dir, categoria_ei, label)
            total_env += env
            total_err += err
            status = "OK" if err == 0 else f"{err} ERROS"
            log.info("  %-35s %4d imgs  [%s]", label, env, status)

    log.info("\n=== Resultado Final ===")
    log.info("Enviados com sucesso : %d", total_env)
    log.info("Erros               : %d", total_err)
    log.info("Log completo        : %s", LOG_FILE)

    if total_err == 0:
        log.info("\nUpload concluido! Verifique o Edge Impulse Studio -> Data acquisition.")
    else:
        log.warning("\nUpload com erros. Verifique upload_log.txt para detalhes.")


if __name__ == "__main__":
    main()
