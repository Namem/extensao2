/// sync_service.dart — Fila de sincronização offline → servidor.
///
/// Monitora conectividade e envia diagnósticos pendentes (feitos offline)
/// para a API Django quando a internet volta.
library;

import 'dart:async';
import 'dart:io';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/foundation.dart';

import '../database/database.dart';
import 'api_service.dart';

class SyncService {
  SyncService._();
  static final instance = SyncService._();

  StreamSubscription<List<ConnectivityResult>>? _sub;
  bool _sincronizando = false;

  /// Quantidade de pendentes — UI pode escutar para mostrar badge.
  final pendentes = ValueNotifier<int>(0);

  /// Inicia o monitoramento de conectividade.
  void iniciar() {
    _atualizarContador();
    _sub?.cancel();
    _sub = Connectivity().onConnectivityChanged.listen((results) {
      final online = results.isNotEmpty &&
          !(results.length == 1 && results.first == ConnectivityResult.none);
      if (online) sincronizar();
    });
  }

  /// Para o monitoramento.
  void parar() {
    _sub?.cancel();
    _sub = null;
  }

  /// Tenta enviar todos os diagnósticos pendentes.
  Future<void> sincronizar() async {
    if (_sincronizando) return;
    _sincronizando = true;

    try {
      final lista = await appDb.pendentes();
      if (lista.isEmpty) return;

      for (final diag in lista) {
        // Precisa da imagem original para enviar ao servidor
        if (diag.imagemPath == null || !File(diag.imagemPath!).existsSync()) {
          // Sem imagem — marca como sincronizado para não travar a fila
          await appDb.marcarSincronizado(diag.id);
          continue;
        }

        try {
          await ApiService.instance.inferir(
            File(diag.imagemPath!),
            latitude: diag.latitude,
            longitude: diag.longitude,
          );
          await appDb.marcarSincronizado(diag.id);
          debugPrint('[Sync] Enviado #${diag.id} ${diag.classe}');
        } catch (e) {
          // Falha de rede — para e tenta na próxima vez
          debugPrint('[Sync] Falha #${diag.id}: $e');
          break;
        }
      }
    } finally {
      _sincronizando = false;
      _atualizarContador();
    }
  }

  Future<void> _atualizarContador() async {
    pendentes.value = await appDb.totalPendentes();
  }
}
