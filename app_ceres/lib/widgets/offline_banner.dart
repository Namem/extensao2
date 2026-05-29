import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/ceres_theme.dart';

/// Banner âmbar que aparece automaticamente quando não há conexão.
/// Uso: envolver o body do Scaffold com [OfflineBanner].
///
/// Exemplo:
/// ```dart
/// body: OfflineBanner(child: MinhaListaWidget())
/// ```
class OfflineBanner extends StatefulWidget {
  final Widget child;

  const OfflineBanner({super.key, required this.child});

  @override
  State<OfflineBanner> createState() => _OfflineBannerState();
}

class _OfflineBannerState extends State<OfflineBanner> {
  bool _offline = false;
  late StreamSubscription<List<ConnectivityResult>> _sub;

  @override
  void initState() {
    super.initState();
    // Checar estado inicial
    Connectivity().checkConnectivity().then(_atualizar);
    // Ouvir mudanças
    _sub = Connectivity().onConnectivityChanged.listen(_atualizar);
  }

  void _atualizar(List<ConnectivityResult> results) {
    final semConexao = results.isEmpty ||
        (results.length == 1 && results.first == ConnectivityResult.none);
    if (mounted && semConexao != _offline) {
      setState(() => _offline = semConexao);
    }
  }

  @override
  void dispose() {
    _sub.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Faixa animada — visível apenas quando offline
        AnimatedSize(
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
          child: _offline
              ? Container(
                  color: CeresColors.dryGrass.withValues(alpha: 0.12),
                  padding: const EdgeInsets.symmetric(
                      horizontal: 16, vertical: 7),
                  child: Row(
                    children: [
                      Container(
                        width: 6,
                        height: 6,
                        decoration: const BoxDecoration(
                          color: CeresColors.dryGrass,
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'Sem conexão · modo offline',
                          style: GoogleFonts.ibmPlexMono(
                            fontSize: 9.5,
                            letterSpacing: 0.1,
                            color: CeresColors.dryGrass,
                          ),
                        ),
                      ),
                    ],
                  ),
                )
              : const SizedBox.shrink(),
        ),
        // Conteúdo da tela
        Expanded(child: widget.child),
      ],
    );
  }
}
