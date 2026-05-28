/// Configurações globais do app Ceres Diagnóstico.
/// Altere BASE_URL conforme o IP do notebook na rede local.
class Config {
  // localhost = PC com Windows desktop
  // 10.0.2.2 = host machine no emulador Android
  // Trocar para o IP real do PC ao usar celular físico na rede
  static const String baseUrl = 'http://localhost:8080';

  static const String inferirEndpoint = '$baseUrl/api/diagnostico/inferir/';
  static const String historicoEndpoint = '$baseUrl/api/diagnostico/historico/';

  // Limiar mínimo de confiança para exibir resultado como confiável
  static const double confiancaMinima = 0.40;
}
