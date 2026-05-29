/// Evento MQTT armazenado no backend (DiagnosticoEvento).
class EventoMqtt {
  final int id;
  final String deviceId;
  final String classe;
  final double? confianca;
  final int latenciaMs;
  final DateTime timestamp;

  // Sensores ambientais (opcionais — backend pode não enviar)
  final double? temperatura;
  final double? umidadeAr;
  final double? umidadeSolo;

  // GPS (opcional — capturado pelo celular no momento do diagnóstico)
  final double? latitude;
  final double? longitude;

  EventoMqtt({
    required this.id,
    required this.deviceId,
    required this.classe,
    required this.timestamp,
    this.confianca,
    this.latenciaMs = 0,
    this.temperatura,
    this.umidadeAr,
    this.umidadeSolo,
    this.latitude,
    this.longitude,
  });

  /// Alias para manter compatibilidade com MapaScreen e outros usos.
  String? get classeDetectada => classe == '—' ? null : classe;

  factory EventoMqtt.fromJson(Map<String, dynamic> json) {
    return EventoMqtt(
      id: json['id'] as int,
      deviceId: json['device_id'] as String? ?? '—',
      classe: json['classe_detectada'] as String? ??
              json['classe'] as String? ?? '—',
      confianca: (json['confianca'] as num?)?.toDouble(),
      latenciaMs: (json['latencia_ms'] as num?)?.toInt() ?? 0,
      timestamp: DateTime.tryParse(json['timestamp'] as String? ?? '') ??
                 DateTime.now(),
      temperatura: (json['temperatura'] as num?)?.toDouble(),
      umidadeAr: (json['umidade_ar'] as num?)?.toDouble(),
      umidadeSolo: (json['umidade_solo'] as num?)?.toDouble(),
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
    );
  }

  String get rotulo {
    const map = {
      'D01_requeima': 'Requeima',
      'D02_septoriose': 'Septoriose',
      'D03_pinta_preta': 'Pinta Preta',
      'D03b_mancha_alvo': 'Mancha Alvo',
      'D05_mofo_foliar': 'Mofo Foliar',
      'D06_vira_cabeca': 'Vira-cabeça',
      'D06b_mosaico': 'Mosaico',
      'D07_acaro_bronzeamento': 'Ácaro',
      'D09_mancha_bacteriana': 'Bact.',
      'saudavel': 'Saudável',
    };
    return map[classe] ?? classe;
  }
}
