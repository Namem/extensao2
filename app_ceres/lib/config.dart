/// Configurações globais do app Ceres Diagnóstico.
class Config {
  // ── Ambientes — escolha UM e comente os demais ─────────────────────────────
  //
  // Emulador Android (10.0.2.2 = localhost do host):
  // static const String baseUrl = 'http://10.0.2.2:8080'; // emulador
  static const String baseUrl = 'http://SEU_IP_AQUI:8080'; // celular real — troque pelo IP do ipconfig
  //
  // PC Windows desktop (flutter run -d windows):
  //   static const String baseUrl = 'http://localhost:8080';
  //
  // Notebook / APK na mesma rede WiFi:
  //   static const String baseUrl = 'http://192.168.X.X:8080';
  //   (descubra o IP com: ipconfig  →  procure "IPv4")
  //
  // APK via ngrok (demo sem rede local):
  //   static const String baseUrl = 'https://xxxx.ngrok-free.app';
  // ──────────────────────────────────────────────────────────────────────────

  // Endpoints da API Django
  static const String tokenEndpoint        = '$baseUrl/api/auth/token/';
  static const String tokenRefreshEndpoint = '$baseUrl/api/auth/token/refresh/';
  static const String meEndpoint           = '$baseUrl/api/auth/me/';
  static const String registerEndpoint     = '$baseUrl/api/auth/register/';
  static const String inferirEndpoint      = '$baseUrl/api/diagnostico/inferir/';
  static const String historicoEndpoint    = '$baseUrl/api/diagnostico/historico/';

  // Limiar mínimo de confiança para exibir resultado como confiável
  static const double confiancaMinima = 0.40;
}
