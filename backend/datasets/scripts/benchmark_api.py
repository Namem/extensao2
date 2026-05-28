"""
benchmark_api.py — Benchmark do endpoint de inferência Django.

Experimento Edge vs Cloud — TCC Ceres Diagnóstico.
Mede latência, acurácia e overhead HTTP do pipeline cloud,
comparando com o ESP32-S3 (692ms, standalone).

Uso:
  python benchmark_api.py
  python benchmark_api.py --url http://localhost:8080 --n 5
  python benchmark_api.py --url http://192.168.15.22:8080 --n 3

Saída:
  Console: tabela por classe + resumo comparativo
  Arquivo: docs/resultados/benchmark_api.json
"""

import argparse
import json
import random
import statistics
import time
from pathlib import Path

import requests

# Classes na mesma ordem do treino (alfabético)
CLASS_NAMES = [
    "D01_requeima",
    "D02_septoriose",
    "D03_pinta_preta",
    "D03b_mancha_alvo",
    "D05_mofo_foliar",
    "D06_vira_cabeca",
    "D06b_mosaico",
    "D07_acaro_bronzeamento",
    "D09_mancha_bacteriana",
    "saudavel",
]

# Referência ESP32-S3 (Sprint 2, benchmark_esp32s3.md)
ESP32_LATENCIA_MS  = 692
ESP32_ACURACIA     = "10/10 (100%)"
ESP32_MODELO_KB    = 638
ESP32_REQUER_REDE  = False


def parse_args():
    p = argparse.ArgumentParser(description="Benchmark API Ceres — edge vs cloud")
    p.add_argument("--url",     default="http://localhost:8080",
                   help="URL base do Django (default: http://localhost:8080)")
    p.add_argument("--val-dir", default="datasets/processed/val",
                   help="Pasta val do PlantVillage (default: datasets/processed/val)")
    p.add_argument("--n",       type=int, default=5,
                   help="Repetições por imagem para estatística (default: 5)")
    p.add_argument("--seed",    type=int, default=42)
    return p.parse_args()


def pegar_imagem(val_dir: Path, classe: str, seed: int) -> Path:
    """Retorna uma imagem determinística da classe (seed fixo = reprodutível)."""
    imgs = (
        list((val_dir / classe).glob("*.jpg")) +
        list((val_dir / classe).glob("*.JPG")) +
        list((val_dir / classe).glob("*.png"))
    )
    if not imgs:
        raise FileNotFoundError(f"Sem imagens em {val_dir / classe}")
    random.seed(seed)
    return random.choice(imgs)


def inferir_uma_vez(endpoint: str, img_path: Path) -> dict:
    """
    POST multipart para o endpoint.
    Retorna resultado + latência medida no cliente (inclui HTTP overhead).
    """
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    t0 = time.perf_counter()
    resp = requests.post(
        endpoint,
        files={"imagem": (img_path.name, img_bytes, "image/jpeg")},
        timeout=60,
    )
    latencia_cliente_ms = round((time.perf_counter() - t0) * 1000)

    resp.raise_for_status()
    data = resp.json()
    data["latencia_cliente_ms"] = latencia_cliente_ms
    return data


def main():
    args = parse_args()
    url      = args.url.rstrip("/")
    endpoint = f"{url}/api/diagnostico/inferir/"
    val_dir  = Path(args.val_dir)
    n_rep    = args.n

    print()
    print("=" * 60)
    print("  Benchmark API Ceres — Experimento Edge vs Cloud")
    print("=" * 60)
    print(f"  Endpoint  : {endpoint}")
    print(f"  Val dir   : {val_dir}")
    print(f"  Repetições: {n_rep} por imagem")
    print("=" * 60)

    # Verificar servidor acessível
    try:
        r = requests.get(f"{url}/api/diagnostico/historico/", timeout=5)
        if r.status_code not in (200, 401, 403):
            raise RuntimeError(f"HTTP {r.status_code}")
        print("  Servidor : OK")
    except Exception as e:
        print(f"\n[ERRO] Django não acessível em {url}: {e}")
        print("  Suba o servidor: python manage.py runserver 0.0.0.0:8080 "
              "--settings=ceres_core.settings_notebook")
        return

    # Warm-up: 1 requisição para carregar o modelo no subprocess antes de medir
    print("  Warm-up  : 1 req (carga do modelo)...")
    try:
        img_warm = pegar_imagem(val_dir, CLASS_NAMES[0], args.seed)
        inferir_uma_vez(endpoint, img_warm)
        print("  Warm-up  : OK")
    except Exception as e:
        print(f"  Warm-up  : falhou ({e}) — continuando mesmo assim")

    print()
    print(f"  {'Classe':<28} {'Predição':<28} {'OK':<3} {'API(ms)':<9} {'HTTP(ms)'}")
    print("  " + "-" * 82)

    resultados       = []
    todas_lat_api    = []
    todas_lat_http   = []
    acertos          = 0
    total            = 0

    for classe in CLASS_NAMES:
        try:
            img_path = pegar_imagem(val_dir, classe, args.seed)
        except FileNotFoundError as e:
            print(f"  [SKIP] {classe}: {e}")
            continue

        lats_api  = []
        lats_http = []
        pred_final = "—"
        conf_final = 0.0

        for _ in range(n_rep):
            try:
                data = inferir_uma_vez(endpoint, img_path)
                lats_api.append(data.get("latencia_ms", 0))
                lats_http.append(data["latencia_cliente_ms"])
                pred_final = data.get("classe", "—")
                conf_final = data.get("confianca", 0.0)
            except Exception as e:
                print(f"  [ERRO] {classe}: {e}")

        if not lats_api:
            continue

        total += 1
        correto = pred_final == classe
        if correto:
            acertos += 1

        med_api  = round(statistics.mean(lats_api))
        med_http = round(statistics.mean(lats_http))

        print(f"  {classe:<28} {pred_final:<28} {'✓' if correto else '✗':<3} "
              f"{med_api:<9} {med_http}")

        resultados.append({
            "classe_esperada":          classe,
            "classe_predita":           pred_final,
            "confianca":                round(conf_final, 4),
            "correto":                  correto,
            "latencia_api_media_ms":    med_api,
            "latencia_api_min_ms":      min(lats_api),
            "latencia_api_max_ms":      max(lats_api),
            "latencia_api_std_ms":      round(statistics.stdev(lats_api), 1) if len(lats_api) > 1 else 0,
            "latencia_http_media_ms":   med_http,
            "latencia_http_min_ms":     min(lats_http),
            "latencia_http_max_ms":     max(lats_http),
        })
        todas_lat_api.extend(lats_api)
        todas_lat_http.extend(lats_http)

    # Resumo
    if not todas_lat_api:
        print("\n[ERRO] Nenhuma inferência bem-sucedida.")
        return

    lat_api_med  = round(statistics.mean(todas_lat_api))
    lat_api_min  = min(todas_lat_api)
    lat_api_max  = max(todas_lat_api)
    lat_api_std  = round(statistics.stdev(todas_lat_api), 1) if len(todas_lat_api) > 1 else 0
    lat_http_med = round(statistics.mean(todas_lat_http))

    print()
    print("=" * 60)
    print("  RESUMO — Cloud API (Django/PC)")
    print("=" * 60)
    print(f"  Acurácia         : {acertos}/{total} = {acertos/total*100:.1f}%")
    print(f"  Latência API med : {lat_api_med} ms  (subprocess + TFLite)")
    print(f"  Latência API mín : {lat_api_min} ms")
    print(f"  Latência API máx : {lat_api_max} ms")
    print(f"  Latência API std : ±{lat_api_std} ms")
    print(f"  Latência HTTP med: {lat_http_med} ms  (inclui rede local + HTTP)")
    print()
    print("=" * 60)
    print("  COMPARATIVO — Edge vs Cloud")
    print("=" * 60)
    print(f"  {'Métrica':<30} {'ESP32-S3':<15} {'Django/PC'}")
    print("  " + "-" * 60)
    print(f"  {'Latência média (ms)':<30} {ESP32_LATENCIA_MS:<15} {lat_api_med}")
    print(f"  {'Latência HTTP end-to-end':<30} {'N/A (offline)':<15} {lat_http_med} ms")
    print(f"  {'Acurácia PlantVillage val':<30} {ESP32_ACURACIA:<15} {acertos}/{total} ({acertos/total*100:.1f}%)")
    print(f"  {'Modelo (KB)':<30} {ESP32_MODELO_KB:<15} {ESP32_MODELO_KB}")
    print(f"  {'Requer conectividade':<30} {'Não':<15} {'Sim (WiFi/rede)'}")
    print(f"  {'Hardware necessário':<30} {'ESP32-S3':<15} {'Servidor PC/cloud'}")
    print(f"  {'Privacidade dado':<30} {'Total (local)':<15} {'Imagem transmitida'}")
    print()

    # Salvar resultado JSON
    saida = {
        "experimento": "edge_vs_cloud",
        "data": time.strftime("%Y-%m-%d"),
        "config": {
            "url": url,
            "n_repeticoes": n_rep,
            "seed": args.seed,
            "modelo": "ceres_expe_int8.tflite (Exp E, 638KB)",
        },
        "cloud_api": {
            "acuracia": f"{acertos}/{total}",
            "acuracia_pct": round(acertos / total * 100, 1),
            "latencia_api_media_ms":  lat_api_med,
            "latencia_api_min_ms":    lat_api_min,
            "latencia_api_max_ms":    lat_api_max,
            "latencia_api_std_ms":    lat_api_std,
            "latencia_http_media_ms": lat_http_med,
            "plataforma": "Windows PC (Python 3.13 subprocess + ai-edge-litert)",
        },
        "edge_esp32": {
            "acuracia":              ESP32_ACURACIA,
            "latencia_media_ms":     ESP32_LATENCIA_MS,
            "latencia_min_ms":       692,
            "latencia_max_ms":       695,
            "modelo_kb":             ESP32_MODELO_KB,
            "plataforma":            "ESP32-S3 240MHz + Chirale_TensorFLowLite 2.0.0",
            "requer_conectividade":  False,
        },
        "por_classe": resultados,
    }

    out_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "resultados" / "benchmark_api.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(saida, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Resultado salvo em: {out_path}")
    print()


if __name__ == "__main__":
    main()
