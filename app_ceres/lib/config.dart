/// Configurações globais do app Ceres Diagnóstico.
class Config {
  // ── Ambientes — escolha UM e comente os demais ─────────────────────────────
  //
  // PC Windows desktop (flutter run -d windows):
  static const String baseUrl = 'http://localhost:8000';
  //
  // Notebook / APK na mesma rede WiFi:
  //   static const String baseUrl = 'http://192.168.X.X:8000';
  //   (descubra o IP com: ipconfig  →  procure "IPv4")
  //
  // APK via ngrok (demo sem rede local):
  //   static const String baseUrl = 'https://xxxx.ngrok-free.app';
  // ──────────────────────────────────────────────────────────────────────────

  // Endpoints da API Django
  static const String tokenEndpoint    = '$baseUrl/api/auth/token/';
  static const String inferirEndpoint  = '$baseUrl/api/diagnostico/inferir/';
  static const String historicoEndpoint= '$baseUrl/api/diagnostico/historico/';

  // Limiar mínimo de confiança para exibir resultado como confiável
  static const double confiancaMinima = 0.40;
}
