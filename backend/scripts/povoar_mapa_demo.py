"""
Povoa o mapa da conta de teste com diagnósticos reais.

Faz login na conta test@test.com, escolhe 1 imagem de cada classe do test set
do PlantVillage e dispara 10 diagnósticos contra Railway com coordenadas GPS
espalhadas em ~5km ao redor de Sorriso-MT.

Uso:
    python povoar_mapa_demo.py
    python povoar_mapa_demo.py --por-classe 2   # 20 pins
    python povoar_mapa_demo.py --base http://localhost:8000  # contra local

Pré-requisitos:
    pip install requests
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path

import requests


# Sorriso-MT (centro aprox.)
SORRISO_LAT = -12.5448
SORRISO_LON = -55.7156
# raio ~5km
SPREAD = 0.045

ROOT = Path(__file__).resolve().parents[1]  # backend/
TEST_SET = ROOT / "datasets" / "processed" / "test"


def autenticar(base: str, email: str, senha: str) -> str:
    """Faz POST /api/auth/token/ e devolve o access token."""
    url = f"{base}/api/auth/token/"
    r = requests.post(url, json={"username": email, "password": senha}, timeout=30)
    if r.status_code != 200:
        # Tentar com chave 'email'
        r = requests.post(url, json={"email": email, "password": senha}, timeout=30)
    r.raise_for_status()
    return r.json()["access"]


def amostrar_imagens(por_classe: int) -> list[Path]:
    """Pega N imagens aleatórias de cada classe do test set."""
    imagens: list[Path] = []
    if not TEST_SET.exists():
        sys.exit(f"Test set não encontrado em {TEST_SET}")
    for classe_dir in sorted(TEST_SET.iterdir()):
        if not classe_dir.is_dir():
            continue
        arquivos = list(classe_dir.glob("*.JPG")) + list(classe_dir.glob("*.jpg"))
        if not arquivos:
            continue
        random.shuffle(arquivos)
        imagens.extend(arquivos[:por_classe])
    return imagens


def coord_sorriso() -> tuple[float, float]:
    """Coordenada aleatória num raio de ~5km de Sorriso-MT."""
    lat = SORRISO_LAT + random.uniform(-SPREAD, SPREAD)
    lon = SORRISO_LON + random.uniform(-SPREAD, SPREAD)
    return round(lat, 6), round(lon, 6)


def inferir(base: str, token: str, imagem: Path) -> dict:
    url = f"{base}/api/diagnostico/inferir/"
    lat, lon = coord_sorriso()
    with imagem.open("rb") as f:
        files = {"imagem": (imagem.name, f, "image/jpeg")}
        data = {"latitude": str(lat), "longitude": str(lon)}
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(url, files=files, data=data, headers=headers, timeout=120)
    r.raise_for_status()
    return {"resp": r.json(), "lat": lat, "lon": lon}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="https://ceres.up.railway.app")
    p.add_argument("--email", default="test@test.com")
    p.add_argument("--senha", default="test123")
    p.add_argument("--por-classe", type=int, default=1, help="Imagens por classe (10 classes)")
    p.add_argument("--delay", type=float, default=3.0, help="Segundos entre inferências")
    args = p.parse_args()

    print(f"[1/3] Autenticando {args.email}...")
    token = autenticar(args.base, args.email, args.senha)
    print(f"      OK (token {token[:20]}...)")

    print(f"[2/3] Amostrando {args.por_classe} imagem(ns) por classe...")
    imagens = amostrar_imagens(args.por_classe)
    print(f"      {len(imagens)} imagens selecionadas")

    print(f"[3/3] Enviando para {args.base}/api/diagnostico/inferir/")
    print(f"      Delay entre requisições: {args.delay}s\n")

    sucesso = 0
    for i, img in enumerate(imagens, 1):
        classe_esperada = img.parent.name
        try:
            res = inferir(args.base, token, img)
            r = res["resp"]
            classe = r.get("classe_detectada") or r.get("classe") or "?"
            conf = r.get("confianca") or r.get("confidence") or 0
            ok = "✓" if classe_esperada.startswith(classe[:3]) else "≠"
            print(f"  [{i:2d}/{len(imagens)}] {ok} {classe_esperada:25s} → {classe:25s} "
                  f"({conf*100:.1f}%) @ ({res['lat']:.4f}, {res['lon']:.4f})")
            sucesso += 1
        except requests.HTTPError as e:
            print(f"  [{i:2d}/{len(imagens)}] ✗ {classe_esperada}: HTTP {e.response.status_code}")
        except Exception as e:
            print(f"  [{i:2d}/{len(imagens)}] ✗ {classe_esperada}: {e}")

        if i < len(imagens):
            time.sleep(args.delay)

    print(f"\n✅ Concluído: {sucesso}/{len(imagens)} diagnósticos publicados.")
    print(f"   Verifique o mapa no app → conta {args.email}")


if __name__ == "__main__":
    main()
