from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from diagnostico.models import DiagnosticoEvento


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Cria novo usuário produtor ou agrônomo."""
    nome  = request.data.get('nome',  '').strip()
    email = request.data.get('email', '').strip().lower()
    senha = request.data.get('senha', '')
    tipo  = request.data.get('tipo',  'produtor')   # 'produtor' | 'agronomo'
    crea  = request.data.get('crea',  '').strip()

    # Validações
    if not nome or not email or not senha:
        return Response({'erro': 'Nome, e-mail e senha são obrigatórios.'}, status=400)
    if '@' not in email or '.' not in email.split('@')[-1]:
        return Response({'erro': 'E-mail inválido.'}, status=400)
    if len(senha) < 6:
        return Response({'erro': 'Senha deve ter no mínimo 6 caracteres.'}, status=400)
    if tipo == 'agronomo' and not crea:
        return Response({'erro': 'CREA obrigatório para agrônomo.'}, status=400)
    if User.objects.filter(username=email).exists():
        return Response({'erro': 'E-mail já cadastrado.'}, status=400)

    partes = nome.split()
    user = User.objects.create_user(
        username=email,
        email=email,
        password=senha,
        first_name=partes[0],
        last_name=' '.join(partes[1:]) if len(partes) > 1 else '',
    )
    # Armazena tipo e CREA no campo `last_name` se necessário — ou simplesmente retorna
    _ = user  # variável mantida para extensão futura (campo Profile)

    return Response({
        'mensagem': 'Conta criada com sucesso.',
        'tipo': tipo,
    }, status=201)


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
