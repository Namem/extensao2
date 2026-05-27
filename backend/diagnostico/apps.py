"""
apps.py — Configuração do app diagnostico.
Pré-carrega o modelo TFLite no startup do Django (método ready()).
"""
from django.apps import AppConfig


class DiagnosticoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "diagnostico"

    def ready(self):
        """Chamado uma vez quando o Django inicia. Carrega o modelo TFLite."""
        import os
        # Evita carregar duas vezes no auto-reloader (processo filho vs pai)
        if os.environ.get("RUN_MAIN") != "true":
            return

        from django.conf import settings
        from .inference_service import inferencia_service

        modelo_path = getattr(settings, "TFLITE_MODEL_PATH", None)
        if modelo_path and modelo_path.exists():
            try:
                inferencia_service.carregar(modelo_path)
                print(f"[TFLite] Modelo carregado: {modelo_path.name}")
            except Exception as e:
                print(f"[TFLite] AVISO: falha ao pre-carregar modelo: {e}")
        else:
            print("[TFLite] AVISO: TFLITE_MODEL_PATH nao configurado")