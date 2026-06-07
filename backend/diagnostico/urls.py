from django.urls import path
from .views import (
    IniciarDiagnosticoView,
    ResponderDiagnosticoView,
    HistoricoEventosView,
    InferirImagemView,
    UltimoSensorView,
)

urlpatterns = [
    path('iniciar/', IniciarDiagnosticoView.as_view(), name='iniciar_diagnostico'),
    path('responder/', ResponderDiagnosticoView.as_view(), name='responder_diagnostico'),
    path('historico/', HistoricoEventosView.as_view(), name='historico_eventos'),
    path('inferir/', InferirImagemView.as_view(), name='inferir_imagem'),
    path('sensor/', UltimoSensorView.as_view(), name='ultimo_sensor'),
]