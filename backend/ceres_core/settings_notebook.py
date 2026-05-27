"""
settings_notebook.py — Configurações para desenvolvimento no notebook.

Diferenças do settings.py principal:
  - Banco: SQLite (sem PostgreSQL)
  - ALLOWED_HOSTS aberto para IP local
  - DEBUG sempre True
  - SECRET_KEY hardcoded (apenas dev)

Uso:
  $env:DJANGO_SETTINGS_MODULE = "ceres_core.settings_notebook"
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
"""

from .settings import *   # herda tudo do settings.py principal

# Sobrescreve apenas o necessário para o notebook

SECRET_KEY = 'dev-notebook-secret-key-nao-usar-em-producao'

DEBUG = True

ALLOWED_HOSTS = ['*']   # aceita qualquer IP local (notebook + celular na mesma rede)

# SQLite — sem PostgreSQL no notebook
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_notebook.sqlite3',
    }
}

# CORS — permite Flutter em qualquer origem durante dev
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True

# Caminho do modelo TFLite
TFLITE_MODEL_PATH = BASE_DIR / 'datasets' / 'modelo' / 'ceres_mobilenetv2_int8.tflite'
