import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/resultado_inferencia.dart';
import '../models/evento_mqtt.dart';

class ApiService {
  ApiService._();
  static final ApiService instance = ApiService._();

  /// Envia a imagem para o endpoint de inferência.
  /// Retorna ResultadoInferencia ou lança Exception.
  Future<ResultadoInferencia> inferir(File imagem) async {
    final uri = Uri.parse(Config.inferirEndpoint);
    final req = http.MultipartRequest('POST', uri);
    req.files.add(await http.MultipartFile.fromPath('imagem', imagem.path));

    final streamed = await req.send().timeout(const Duration(seconds: 60));
    final body = await streamed.stream.bytesToString();

    if (streamed.statusCode == 200) {
      return ResultadoInferencia.fromJson(jsonDecode(body) as Map<String, dynamic>);
    }
    throw Exception('Servidor retornou ${streamed.statusCode}: $body');
  }

  /// Login com e-mail e senha — retorna tokens JWT ou lança Exception.
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
      return {
        'access': data['access'] as String,
        'refresh': data['refresh'] as String,
      };
    }
    throw Exception('Login falhou: ${resp.statusCode}');
  }

  /// Busca página [page] do histórico de eventos MQTT.
  /// Retorna mapa com count, next, previous e results (lista de EventoMqtt).
  Future<Map<String, dynamic>> historico({int page = 1}) async {
    final uri = Uri.parse('${Config.historicoEndpoint}?page=$page');
    final resp = await http.get(uri).timeout(const Duration(seconds: 30));

    if (resp.statusCode == 200) {
      final data = jsonDecode(resp.body) as Map<String, dynamic>;
      final results = (data['results'] as List)
          .map((e) => EventoMqtt.fromJson(e as Map<String, dynamic>))
          .toList();
      return {
        'count': data['count'],
        'next': data['next'],
        'previous': data['previous'],
        'results': results,
      };
    }
    throw Exception('Histórico: ${resp.statusCode}');
  }
}
