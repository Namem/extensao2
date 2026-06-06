"""
settings_railway.py — Configurações para deploy no Railway.

Diferenças do settings.py principal:
  - Banco: PostgreSQL via DATABASE_URL do Railway
  - ALLOWED_HOSTS aberto (Railway faz proxy)
  - SECRET_KEY via env var
  - CORS aberto (Flutter app)
"""

import os
import dj_database_url
from .settings import *

SECRET_KEY = os.getenv('SECRET_KEY', 'railway-fallback-key-trocar-em-prod')

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1')

ALLOWED_HOSTS = ['*']

# PostgreSQL via DATABASE_URL do Railway (persistente entre deploys)
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
        )
    }

# CORS — permite Flutter app
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True

# Caminho do modelo TFLite
TFLITE_MODEL_PATH = BASE_DIR / 'datasets' / 'modelo' / (
    'ceres_expe_int8.tflite'
    if (BASE_DIR / 'datasets' / 'modelo' / 'ceres_expe_int8.tflite').exists()
    else 'ceres_mobilenetv2_int8.tflite'
)
