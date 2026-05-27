"""
asgi_notebook.py — Entry point ASGI para desenvolvimento no notebook.
Usa SQLite (sem PostgreSQL) e carrega o modelo TFLite na inicialização.

Uso:
  uvicorn ceres_core.asgi_notebook:application --host 0.0.0.0 --port 8000 --workers 1
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceres_core.settings_notebook")

import django
django.setup()

# Pre-carregar modelo TFLite antes de começar a servir requests
from django.conf import settings
from diagnostico.inference_service import inferencia_service

modelo_path = getattr(settings, "TFLITE_MODEL_PATH", None)
if modelo_path and modelo_path.exists():
    inferencia_service.carregar(modelo_path)
    print(f"[TFLite] Modelo carregado: {modelo_path.name}")
else:
    print("[TFLite] AVISO: modelo nao encontrado")

from django.core.asgi import get_asgi_application
application = get_asgi_application()
