"""
inferir_worker.py — Worker de inferência TFLite rodando no main thread.

Lê uma imagem base64 do stdin, roda inferência TFLite, imprime JSON no stdout.
Chamado como subprocess pela view Django para contornar restrição de thread
do XNNPACK delegate no Windows.

Uso interno (não chamar diretamente):
  echo <base64_image> | python inferir_worker.py <caminho_modelo>
"""
import sys
import base64
import json
from pathlib import Path

def main():
    modelo_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not modelo_path or not modelo_path.exists():
        print(json.dumps({"erro": "Modelo nao encontrado"}))
        sys.exit(1)

    img_b64 = sys.stdin.read().strip()
    img_bytes = base64.b64decode(img_b64)

    from diagnostico.inference_service import inferencia_service
    inferencia_service.carregar(modelo_path)
    resultado = inferencia_service.inferir(img_bytes)
    print(json.dumps(resultado))

if __name__ == "__main__":
    main()
