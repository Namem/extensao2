/// Resultado retornado pelo endpoint POST /api/diagnostico/inferir/
class ResultadoInferencia {
  final String classe;
  final double confianca;
  final int latenciaMs;
  final Map<String, double> scores;

  ResultadoInferencia({
    required this.classe,
    required this.confianca,
    required this.latenciaMs,
    required this.scores,
  });

  factory ResultadoInferencia.fromJson(Map<String, dynamic> json) {
    final rawScores = json['scores'] as Map<String, dynamic>? ?? {};
    return ResultadoInferencia(
      classe: json['classe'] as String,
      confianca: (json['confianca'] as num).toDouble(),
      latenciaMs: (json['latencia_ms'] as num).toInt(),
      scores: rawScores.map((k, v) => MapEntry(k, (v as num).toDouble())),
    );
  }

  /// Mapa estático de classe → rótulo legível (compartilhado com o banco local).
  static const Map<String, String> _rotulos = {
    'D01_requeima': 'Requeima (Mela)',
    'D02_septoriose': 'Septoriose',
    'D03_pinta_preta': 'Pinta Preta',
    'D03b_mancha_alvo': 'Mancha Alvo',
    'D05_mofo_foliar': 'Mofo Foliar',
    'D06_vira_cabeca': 'Vira-cabeça',
    'D06b_mosaico': 'Mosaico',
    'D07_acaro_bronzeamento': 'Ácaro Bronzeamento',
    'D09_mancha_bacteriana': 'Mancha Bacteriana',
    'saudavel': 'Saudável',
  };

  /// Rótulo legível para exibição ao produtor.
  String get rotulo => rotuloDeClasse(classe);

  /// Converte código de classe em rótulo legível (uso estático — ex: banco local).
  static String rotuloDeClasse(String classe) => _rotulos[classe] ?? classe;

  bool get isSaudavel => classe == 'saudavel';
}
