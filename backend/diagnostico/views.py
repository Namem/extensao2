import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Pergunta, Opcao, DiagnosticoEvento
from .serializers import PerguntaSerializer, DiagnosticoSerializer, DiagnosticoEventoSerializer
from .inference_service import inferencia_service

class IniciarDiagnosticoView(APIView):
    permission_classes = [AllowAny] # Aberto para o produtor no campo
    
    def get(self, request):
        raiz = Pergunta.objects.filter(opcoes_que_trazem_aqui__isnull=True).first()
        if not raiz:
            return Response({"erro": "Arvore vazia."}, status=404)
        serializer = PerguntaSerializer(raiz)
        return Response({"tipo": "pergunta", "dados": serializer.data})

class ResponderDiagnosticoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        opcao_id = request.data.get('opcao_id')
        if not opcao_id:
            return Response({"erro": "Envie o opcao_id no body."}, status=400)
            
        opcao = get_object_or_404(Opcao, id=opcao_id)
        
        if opcao.diagnostico_final:
            serializer = DiagnosticoSerializer(opcao.diagnostico_final)
            return Response({"tipo": "diagnostico", "dados": serializer.data})
        
        if opcao.proxima_pergunta:
            serializer = PerguntaSerializer(opcao.proxima_pergunta)
            return Response({"tipo": "pergunta", "dados": serializer.data})

        return Response({"erro": "Fim de linha."}, status=500)


class HistoricoPaginator(PageNumberPagination):
    """Paginador padrão do histórico de eventos."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class HistoricoEventosView(APIView):
    """
    Retorna o histórico de eventos recebidos via MQTT dos dispositivos ESP32.

    GET /api/diagnostico/historico/
        Retorna os últimos eventos paginados (page_size=10, max=20).
        Suporta ?page=2 para navegar nas páginas.
    """

    permission_classes = [AllowAny]  # Sprint 3: Flutter ainda sem JWT

    def get(self, request):
        """Lista os eventos mais recentes, do mais novo para o mais antigo."""
        eventos = DiagnosticoEvento.objects.all()
        paginator = HistoricoPaginator()
        pagina = paginator.paginate_queryset(eventos, request)
        serializer = DiagnosticoEventoSerializer(pagina, many=True)
        return paginator.get_paginated_response(serializer.data)


class InferirImagemView(APIView):
    """
    POST /api/diagnostico/inferir/
    Recebe imagem de folha de tomate e retorna diagnóstico via TFLite.

    Body: multipart/form-data com campo 'imagem' (JPEG/PNG)
    Resposta: {"classe": "D01_requeima", "confianca": 0.87, "latencia_ms": 45, ...}

    Permissão: AllowAny — produtor no campo não precisa de login.

    Implementação: delega ao inferir_worker.py via subprocess para garantir
    execução no main thread (necessário para XNNPACK delegate no Windows).
    """

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        import subprocess
        import base64
        import json as json_mod
        from pathlib import Path
        from django.utils import timezone

        imagem = request.FILES.get('imagem')
        if not imagem:
            return Response(
                {"erro": "Envie a imagem no campo 'imagem' (multipart/form-data)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        modelo_path = getattr(settings, 'TFLITE_MODEL_PATH', None)
        if not modelo_path or not Path(modelo_path).exists():
            return Response(
                {"erro": "Modelo TFLite nao encontrado. Verifique TFLITE_MODEL_PATH."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # GPS opcional — enviado pelo app Flutter
        lat_str = request.data.get('latitude')
        lon_str = request.data.get('longitude')
        latitude = float(lat_str) if lat_str else None
        longitude = float(lon_str) if lon_str else None

        img_bytes = imagem.read()
        img_b64 = base64.b64encode(img_bytes).decode()

        import time as _time
        try:
            worker = Path(__file__).resolve().parent.parent / "inferir_worker.py"
            t0 = _time.perf_counter()
            proc = subprocess.run(
                [sys.executable, str(worker), str(modelo_path)],
                input=img_b64,
                capture_output=True,
                text=True,
                timeout=30,
            )
            latencia_api_ms = max(1, round(((_time.perf_counter() - t0) * 1000)))

            if proc.returncode != 0:
                raise RuntimeError(proc.stderr or "worker falhou")

            # Pega a última linha (ignora logs do TFLite no stdout)
            output = [l for l in proc.stdout.strip().splitlines() if l.startswith('{')]
            if not output:
                raise RuntimeError(f"Sem JSON na saída: {proc.stdout}")

            resultado = json_mod.loads(output[-1])
            # Sobrescreve com a latência real percebida pela API (inclui subprocess)
            resultado['latencia_ms'] = latencia_api_ms

            # ── Persistir como DiagnosticoEvento (alimenta o mapa) ──────
            device_id = 'app_flutter'
            if hasattr(request, 'user') and request.user.is_authenticated:
                device_id = f'app_{request.user.username}'

            DiagnosticoEvento.objects.create(
                device_id=device_id,
                classe_detectada=resultado.get('classe'),
                confianca=resultado.get('confianca'),
                latitude=latitude,
                longitude=longitude,
                timestamp=timezone.now(),
            )

            return Response(resultado, status=status.HTTP_200_OK)

        except subprocess.TimeoutExpired:
            return Response(
                {"erro": "Timeout na inferência (>30s)"},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except Exception as e:
            return Response(
                {"erro": f"Falha na inferencia: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )