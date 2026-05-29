from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Autenticação JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Perfil do usuário autenticado:
    path('api/auth/', include('accounts.urls')),
    # Rota base para a nossa API de diagnóstico:
    path('api/diagnostico/', include('diagnostico.urls')),
]