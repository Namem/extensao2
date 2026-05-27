/// Configurações globais do app Ceres Diagnóstico.
/// Altere BASE_URL conforme o IP do notebook na rede local.
class Config {
  // IP do notebook com Django rodando na porta 8080
  // 10.0.2.2 = host machine no emulador Android
  // Trocar para o IP real do notebook ao usar celular físico
  static const String baseUrl = 'http://10.0.2.2:8080';

  static const String inferirEndpoint = '$baseUrl/api/diagnostico/inferir/';
  static const String historicoEndpoint = '$baseUrl/api/diagnostico/historico/';

  // Limiar mínimo de confiança para exibir resultado como confiável
  static const double confiancaMinima = 0.40;
}
