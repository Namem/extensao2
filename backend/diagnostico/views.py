from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny 
from django.shortcuts import get_object_or_404
from .models import Pergunta, Opcao
from .serializers import PerguntaSerializer, DiagnosticoSerializer

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

    # Certifique-se de que está escrito 'post' (tudo minúsculo)
    def post(self, request):
        print("DEBUG: O POST chegou com sucesso!") # Isso vai aparecer no seu terminal
        
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