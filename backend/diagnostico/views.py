from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Pergunta, Opcao
from .serializers import PerguntaSerializer, DiagnosticoSerializer

class IniciarDiagnosticoView(APIView):
    """ Retorna a primeira pergunta da triagem (a raiz da árvore) """
    
    def get(self, request):
        # A raiz lógica é a pergunta que NÃO é destino de nenhuma opção.
        raiz = Pergunta.objects.filter(opcoes_que_trazem_aqui__isnull=True).first()
        
        if not raiz:
            return Response(
                {"erro": "Nenhuma árvore de decisão cadastrada no sistema."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PerguntaSerializer(raiz)
        return Response({"tipo": "pergunta", "dados": serializer.data})


class ResponderDiagnosticoView(APIView):
    """ Processa a resposta do usuário e retorna o próximo passo """
    
    def post(self, request):
        opcao_id = request.data.get('opcao_id')
        
        if not opcao_id:
            return Response(
                {"erro": "O campo 'opcao_id' é obrigatório."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        opcao = get_object_or_404(Opcao, id=opcao_id)
        
        # A Mágica do Motor de Inferência:
        if opcao.diagnostico_final:
            # Se a opção aponta para uma folha, devolvemos a doença e o manejo
            serializer = DiagnosticoSerializer(opcao.diagnostico_final)
            return Response({"tipo": "diagnostico", "dados": serializer.data})
            
        elif opcao.proxima_pergunta:
            # Se aponta para outro nó, devolvemos a próxima pergunta
            serializer = PerguntaSerializer(opcao.proxima_pergunta)
            return Response({"tipo": "pergunta", "dados": serializer.data})
            
        else:
            return Response(
                {"erro": "Esta opção não leva a lugar nenhum (banco de dados inconsistente)."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )