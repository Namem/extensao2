from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rota base para a nossa API de diagnóstico:
    path('api/diagnostico/', include('diagnostico.urls')), 
]