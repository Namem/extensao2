from django.urls import path
from .views import IniciarDiagnosticoView, ResponderDiagnosticoView, HistoricoEventosView

urlpatterns = [
    path('iniciar/', IniciarDiagnosticoView.as_view(), name='iniciar_diagnostico'),
    path('responder/', ResponderDiagnosticoView.as_view(), name='responder_diagnostico'),
    path('historico/', HistoricoEventosView.as_view(), name='historico_eventos'),
]