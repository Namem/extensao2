"""
wsgi_notebook.py — Entry point WSGI para desenvolvimento no notebook.
Usa SQLite e carrega o modelo TFLite na inicialização.

Uso:
  waitress-serve --threads=1 --host=0.0.0.0 --port=8000 ceres_core.wsgi_notebook:application
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceres_core.settings_notebook")

import django
django.setup()

# Pre-carregar modelo
from django.conf import settings
from diagnostico.inference_service import inferencia_service

modelo_path = getattr(settings, "TFLITE_MODEL_PATH", None)
if modelo_path and modelo_path.exists():
    inferencia_service.carregar(modelo_path)
    print(f"[TFLite] Modelo carregado: {modelo_path.name}")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
