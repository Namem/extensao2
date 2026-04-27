from rest_framework import serializers
from .models import Diagnostico, Pergunta, Opcao, DiagnosticoEvento

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


class DiagnosticoEventoSerializer(serializers.ModelSerializer):
    """Serializa os eventos recebidos via MQTT dos dispositivos ESP32."""

    class Meta:
        model = DiagnosticoEvento
        fields = [
            'id',
            'device_id',
            'classe_detectada',
            'confianca',
            'temperatura',
            'umidade_ar',
            'umidade_solo',
            'timestamp',
            'diagnostico',
            'criado_em',
        ]