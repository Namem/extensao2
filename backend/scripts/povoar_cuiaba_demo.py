"""
Povoa o mapa com diagnósticos em múltiplos bairros de Cuiabá-MT.

Usa coordenadas reais de bairros/pontos de Cuiabá para o mapa ficar
realista e espalhado pela cidade.

Uso:
    python povoar_cuiaba_demo.py
    python povoar_cuiaba_demo.py --base http://localhost:8000

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

ROOT = Path(__file__).resolve().parents[1]
TEST_SET = ROOT / "datasets" / "processed" / "test"

# Pontos reais espalhados por Cuiabá-MT (bairros + regiões rurais ao redor)
PONTOS_CUIABA = [
    (-15.5989, -56.0949, "Centro"),
    (-15.5731, -56.0822, "Coxipó da Ponte"),
    (-15.6218, -56.0712, "Jardim Leblon"),
    (-15.5512, -56.0631, "Pascoal Ramos"),
    (-15.6087, -56.1301, "CPA"),
    (-15.5834, -56.1056, "Duque de Caxias"),
    (-15.6401, -56.0534, "Morada da Serra"),
    (-15.5301, -56.0978, "Araés"),
    (-15.6654, -56.0821, "Coxipó"),
    (-15.5723, -56.1412, "Novo Terceiro"),
    (-15.6102, -56.0202, "Grande Terceiro"),
    (-15.5189, -56.1102, "Tijucal"),
    (-15.6891, -56.1023, "Pedra 90"),
    (-15.5445, -56.0412, "Dom Aquino"),
    (-15.6312, -56.1512, "Planalto"),
    (-15.5978, -56.0534, "Santa Rosa"),
    (-15.6512, -56.0312, "Boa Esperança"),
    (-15.5612, -56.1234, "Osmar Cabral"),
    (-15.6789, -56.0678, "Novo Colorado"),
    (-15.5089, -56.0789, "Alvorada"),
]


def autenticar(base: str, email: str, senha: str) -> str:
    url = f"{base}/api/auth/token/"
    r = requests.post(url, json={"username": email, "password": senha}, timeout=30)
    if r.status_code != 200:
        r = requests.post(url, json={"email": email, "password": senha}, timeout=30)
    r.raise_for_status()
    return r.json()["access"]


def amostrar_imagens(por_classe: int) -> list[Path]:
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


def inferir(base: str, token: str, imagem: Path, lat: float, lon: float) -> dict:
    url = f"{base}/api/diagnostico/inferir/"
    with imagem.open("rb") as f:
        files = {"imagem": (imagem.name, f, "image/jpeg")}
        data = {"latitude": str(round(lat, 6)), "longitude": str(round(lon, 6))}
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(url, files=files, data=data, headers=headers, timeout=120)
    r.raise_for_status()
    return r.json()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="https://ceres.up.railway.app")
    p.add_argument("--email", default="test@test.com")
    p.add_argument("--senha", default="test123")
    p.add_argument("--por-classe", type=int, default=2,
                   help="Imagens por classe (10 classes × N = total de pins)")
    p.add_argument("--delay", type=float, default=3.0)
    args = p.parse_args()

    print(f"[1/3] Autenticando {args.email}...")
    token = autenticar(args.base, args.email, args.senha)
    print(f"      OK (token {token[:20]}...)")

    print(f"[2/3] Amostrando {args.por_classe} imagem(ns) por classe...")
    imagens = amostrar_imagens(args.por_classe)
    total = len(imagens)
    print(f"      {total} imagens selecionadas → {total} pins em Cuiabá-MT")

    # Distribui as imagens ciclicamente pelos pontos de Cuiabá
    pontos = PONTOS_CUIABA * ((total // len(PONTOS_CUIABA)) + 1)
    random.shuffle(pontos)

    print(f"[3/3] Enviando para {args.base}/api/diagnostico/inferir/")
    print(f"      Pontos disponíveis: {len(PONTOS_CUIABA)} bairros de Cuiabá\n")

    sucesso = 0
    for i, (img, (lat, lon, bairro)) in enumerate(zip(imagens, pontos), 1):
        classe_esperada = img.parent.name
        # Pequeno offset aleatório para não empilhar pins no mesmo pixel
        lat_r = lat + random.uniform(-0.003, 0.003)
        lon_r = lon + random.uniform(-0.003, 0.003)
        try:
            r = inferir(args.base, token, img, lat_r, lon_r)
            classe = r.get("classe_detectada") or r.get("classe") or "?"
            conf = r.get("confianca") or r.get("confidence") or 0
            ok = "✓" if classe_esperada.startswith(classe[:3]) else "≠"
            print(f"  [{i:2d}/{total}] {ok} {classe_esperada:25s} → {classe:25s} "
                  f"({conf*100:.1f}%) @ {bairro}")
            sucesso += 1
        except requests.HTTPError as e:
            print(f"  [{i:2d}/{total}] ✗ {classe_esperada}: HTTP {e.response.status_code}")
        except Exception as e:
            print(f"  [{i:2d}/{total}] ✗ {classe_esperada}: {e}")

        if i < total:
            time.sleep(args.delay)

    print(f"\n✅ Concluído: {sucesso}/{total} pins publicados em Cuiabá-MT.")
    print(f"   + 10 pins em Sorriso-MT já existentes")
    print(f"   Total no mapa: ~{sucesso + 10} diagnósticos")
    print(f"   Conta: {args.email}")


if __name__ == "__main__":
    main()
