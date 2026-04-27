from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Pergunta, Opcao, DiagnosticoEvento
from .serializers import PerguntaSerializer, DiagnosticoSerializer, DiagnosticoEventoSerializer

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

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Lista os eventos mais recentes, do mais novo para o mais antigo."""
        eventos = DiagnosticoEvento.objects.all()
        paginator = HistoricoPaginator()
        pagina = paginator.paginate_queryset(eventos, request)
        serializer = DiagnosticoEventoSerializer(pagina, many=True)
        return paginator.get_paginated_response(serializer.data)