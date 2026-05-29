from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from diagnostico.models import DiagnosticoEvento


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Retorna dados do usuário autenticado + estatísticas de diagnósticos."""
    user = request.user

    # Estatísticas baseadas nos eventos do usuário (ESP32 envia device_id fixo)
    # Para o TCC, buscamos todos os eventos do sistema (sem filtro por usuário)
    # pois o ESP32 não autentica — todos os eventos são do operador logado.
    total = DiagnosticoEvento.objects.count()
    saudaveis = DiagnosticoEvento.objects.filter(
        classe_detectada='saudavel'
    ).count()
    doencas = total - saudaveis

    return Response({
        'nome': user.get_full_name() or user.username,
        'email': user.email,
        'username': user.username,
        'total_diagnosticos': total,
        'total_doencas': doencas,
        'total_saudavel': saudaveis,
        'membro_desde': user.date_joined.strftime('%m/%Y'),
        'ultimo_acesso': user.last_login.strftime('%d/%m/%Y %H:%M')
        if user.last_login else '—',
    })
