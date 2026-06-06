import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/resultado_inferencia.dart';
import '../models/evento_mqtt.dart';
import 'auth_storage.dart';

class ApiService {
  ApiService._();
  static final ApiService instance = ApiService._();

  // ── Helpers ───────────────────────────────────────────────────────────────

  /// Cabeçalho Authorization com o access token salvo.
  Future<Map<String, String>> _authHeader() async {
    final token = await AuthStorage.instance.lerAccessToken();
    if (token == null) return {};
    return {'Authorization': 'Bearer $token'};
  }

  /// Tenta renovar o access token usando o refresh token.
  /// Retorna true se conseguiu; false se o refresh também expirou.
  Future<bool> _refresh() async {
    final refreshToken = await AuthStorage.instance.lerRefreshToken();
    if (refreshToken == null) return false;

    final uri = Uri.parse(Config.tokenRefreshEndpoint);
    final resp = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refreshToken}),
    ).timeout(const Duration(seconds: 20));

    if (resp.statusCode == 200) {
      final data = jsonDecode(resp.body) as Map<String, dynamic>;
      await AuthStorage.instance.salvarTokens(
        access:  data['access']  as String,
        refresh: data['refresh'] as String? ?? refreshToken,
      );
      return true;
    }
    return false;
  }

  // ── API pública ───────────────────────────────────────────────────────────

  /// Login com e-mail e senha — salva tokens e retorna-os.
  Future<Map<String, String>> login({
    required String email,
    required String senha,
  }) async {
    final uri = Uri.parse(Config.tokenEndpoint);
    final resp = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': email, 'password': senha}),
    ).timeout(const Duration(seconds: 20));

    if (resp.statusCode == 200) {
      final data = jsonDecode(resp.body) as Map<String, dynamic>;
      final tokens = {
        'access':  data['access']  as String,
        'refresh': data['refresh'] as String,
      };
      await AuthStorage.instance.salvarTokens(
        access:  tokens['access']!,
        refresh: tokens['refresh']!,
      );
      return tokens;
    }
    throw Exception('Login falhou: ${resp.statusCode}');
  }

  /// Envia a imagem para o endpoint de inferência.
  /// Reenvia com token renovado automaticamente em caso de 401.
  /// [latitude] e [longitude] opcionais — incluídos no POST se disponíveis.
  Future<ResultadoInferencia> inferir(File imagem, {
    double? latitude,
    double? longitude,
  }) async {
    Future<http.StreamedResponse> enviar() async {
      final uri = Uri.parse(Config.inferirEndpoint);
      final req = http.MultipartRequest('POST', uri);
      req.headers.addAll(await _authHeader());
      req.files.add(await http.MultipartFile.fromPath('imagem', imagem.path));
      if (latitude != null) req.fields['latitude'] = latitude.toString();
      if (longitude != null) req.fields['longitude'] = longitude.toString();
      return req.send().timeout(const Duration(seconds: 60));
    }

    var streamed = await enviar();

    // Tentativa de refresh em 401
    if (streamed.statusCode == 401) {
      final ok = await _refresh();
      if (!ok) throw Exception('Sessão expirada — faça login novamente.');
      streamed = await enviar();
    }

    final body = await streamed.stream.bytesToString();
    if (streamed.statusCode == 200) {
      return ResultadoInferencia.fromJson(
          jsonDecode(body) as Map<String, dynamic>);
    }
    throw Exception('Servidor retornou ${streamed.statusCode}: $body');
  }

  /// Cria novo usuário (sem autenticação).
  Future<void> registrar({
    required String nome,
    required String email,
    required String senha,
    required String tipo,   // 'produtor' | 'agronomo'
    String crea = '',
  }) async {
    final uri  = Uri.parse(Config.registerEndpoint);
    final resp = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'nome': nome, 'email': email, 'senha': senha,
        'tipo': tipo, 'crea': crea,
      }),
    ).timeout(const Duration(seconds: 20));

    if (resp.statusCode == 201) return;
    final body = jsonDecode(resp.body) as Map<String, dynamic>;
    throw Exception(body['erro'] ?? 'Erro ao criar conta.');
  }

  /// Redefine a senha diretamente (sem código por e-mail).
  Future<String> resetarSenha({
    required String email,
    required String novaSenha,
  }) async {
    final uri = Uri.parse(Config.resetPasswordEndpoint);
    final resp = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'nova_senha': novaSenha,
      }),
    ).timeout(const Duration(seconds: 20));

    final body = jsonDecode(resp.body) as Map<String, dynamic>;
    if (resp.statusCode == 200) {
      return body['mensagem'] as String;
    }
    throw Exception(body['erro'] ?? 'Erro ao redefinir senha.');
  }

  /// Busca dados do usuário autenticado + estatísticas.
  Future<Map<String, dynamic>> me() async {
    Future<http.Response> buscar() async {
      final uri = Uri.parse(Config.meEndpoint);
      return http.get(uri, headers: await _authHeader())
          .timeout(const Duration(seconds: 20));
    }

    var resp = await buscar();

    if (resp.statusCode == 401) {
      final ok = await _refresh();
      if (!ok) throw Exception('Sessão expirada — faça login novamente.');
      resp = await buscar();
    }

    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    throw Exception('Perfil: ${resp.statusCode}');
  }

  /// Busca página [page] do histórico de eventos MQTT.
  Future<Map<String, dynamic>> historico({int page = 1}) async {
    Future<http.Response> buscar() async {
      final uri = Uri.parse('${Config.historicoEndpoint}?page=$page');
      return http.get(uri, headers: await _authHeader())
          .timeout(const Duration(seconds: 30));
    }

    var resp = await buscar();

    if (resp.statusCode == 401) {
      final ok = await _refresh();
      if (!ok) throw Exception('Sessão expirada — faça login novamente.');
      resp = await buscar();
    }

    if (resp.statusCode == 200) {
      final data = jsonDecode(resp.body) as Map<String, dynamic>;
      final results = (data['results'] as List)
          .map((e) => EventoMqtt.fromJson(e as Map<String, dynamic>))
          .toList();
      return {
        'count':    data['count'],
        'next':     data['next'],
        'previous': data['previous'],
        'results':  results,
      };
    }
    throw Exception('Histórico: ${resp.statusCode}');
  }
}
