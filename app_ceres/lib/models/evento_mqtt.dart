/// Evento MQTT armazenado no backend (DiagnosticoEvento).
class EventoMqtt {
  final int id;
  final String deviceId;
  final String classe;
  final double confianca;
  final int latenciaMs;
  final String timestamp;

  // Sensores ambientais (opcionais — backend pode não enviar)
  final double? temperatura;
  final double? umidadeAr;
  final double? umidadeSolo;

  EventoMqtt({
    required this.id,
    required this.deviceId,
    required this.classe,
    required this.confianca,
    required this.latenciaMs,
    required this.timestamp,
    this.temperatura,
    this.umidadeAr,
    this.umidadeSolo,
  });

  factory EventoMqtt.fromJson(Map<String, dynamic> json) {
    return EventoMqtt(
      id: json['id'] as int,
      deviceId: json['device_id'] as String? ?? '—',
      classe: json['classe'] as String? ?? '—',
      confianca: (json['confianca'] as num?)?.toDouble() ?? 0.0,
      latenciaMs: (json['latencia_ms'] as num?)?.toInt() ?? 0,
      timestamp: json['timestamp'] as String? ?? '',
      temperatura: (json['temperatura'] as num?)?.toDouble(),
      umidadeAr: (json['umidade_ar'] as num?)?.toDouble(),
      umidadeSolo: (json['umidade_solo'] as num?)?.toDouble(),
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
