from rest_framework import serializers
from .models import Diagnostico, Pergunta, Opcao

class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ['id', 'nome', 'descricao', 'recomendacao_manejo']

class OpcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcao
        fields = ['id', 'texto']

class PerguntaSerializer(serializers.ModelSerializer):
    # O many=True e read_only=True garantem que ao buscar uma pergunta, 
    # a API já traga a lista de opções dela embutida no JSON.
    opcoes = OpcaoSerializer(many=True, read_only=True)

    class Meta:
        model = Pergunta
        fields = ['id', 'texto', 'opcoes']