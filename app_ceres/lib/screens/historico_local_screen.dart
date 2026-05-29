import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

import '../database/database.dart';
import '../models/resultado_inferencia.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_app_bar.dart';

class HistoricoLocalScreen extends StatelessWidget {
  const HistoricoLocalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      appBar: CeresAppBar(
        pageTitle: 'Diagnósticos Salvos',
        actions: [
          CeresIconButton(
            icon: Icons.delete_sweep_outlined,
            tooltip: 'Limpar histórico',
            onPressed: () => _confirmarLimpeza(context),
          ),
        ],
      ),
      body: StreamBuilder<List<DiagnosticoLocal>>(
        stream: appDb.historicoStream(),
        builder: (context, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(
                color: CeresColors.leafLive,
                strokeWidth: 1.5,
              ),
            );
          }
          final lista = snap.data ?? [];
          if (lista.isEmpty) {
            return _vazio();
          }
          return CustomScrollView(
            slivers: [
              SliverToBoxAdapter(child: _offlineBanner()),
              const SliverToBoxAdapter(child: SizedBox(height: 12)),
              SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, i) => _itemDiagnostico(lista[i]),
                  childCount: lista.length,
                ),
              ),
              const SliverToBoxAdapter(child: SizedBox(height: 24)),
            ],
          );
        },
      ),
    );
  }

  // ── Offline banner ───────────────────────────────────────────────────────────
  Widget _offlineBanner() {
    return Container(
      margin: const EdgeInsets.fromLTRB(16, 14, 16, 0),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: CeresColors.paper2,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: Row(
        children: [
          Icon(Icons.offline_bolt_outlined,
              size: 13, color: CeresColors.dryGrass),
          const SizedBox(width: 8),
          Text(
            'ARMAZENAMENTO LOCAL',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 9,
              letterSpacing: 0.5,
              color: CeresColors.dryGrass,
            ),
          ),
          const Spacer(),
          Text(
            'sem sincronização',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 9,
              color: CeresColors.ink3,
            ),
          ),
        ],
      ),
    );
  }

  // ── Item com faixa vertical ──────────────────────────────────────────────────
  Widget _itemDiagnostico(DiagnosticoLocal d) {
    final isSaudavel = d.classe == 'saudavel';
    final Color cor = CeresColors.statusColor(d.classe, d.confianca);
    final rotulo = ResultadoInferencia.rotuloDeClasse(d.classe);
    final ts = DateFormat('dd/MM/yyyy HH:mm').format(d.timestamp.toLocal());
    final baixaConfianca = d.confianca < 0.40;

    Map<String, double> scores = {};
    try {
      final raw = jsonDecode(d.scoresJson) as Map<String, dynamic>;
      scores = raw.map((k, v) => MapEntry(k, (v as num).toDouble()));
    } catch (_) {}

    return Container(
      margin: const EdgeInsets.fromLTRB(16, 0, 16, 6),
      decoration: BoxDecoration(
        color: CeresColors.paper,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(6),
        child: IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Faixa vertical colorida — 3px
              Container(width: 3, color: cor),
              // Conteúdo
              Expanded(
                child: Theme(
                  data: ThemeData(
                    dividerColor: Colors.transparent,
                    splashColor: Colors.transparent,
                    highlightColor: Colors.transparent,
                  ),
                  child: ExpansionTile(
                    tilePadding:
                        const EdgeInsets.fromLTRB(12, 4, 12, 4),
                    childrenPadding:
                        const EdgeInsets.fromLTRB(12, 0, 12, 12),
                    expandedCrossAxisAlignment: CrossAxisAlignment.start,
                    title: Row(
                      children: [
                        // Ícone pequeno
                        Container(
                          width: 22,
                          height: 22,
                          decoration: BoxDecoration(
                            color: cor.withValues(alpha: 0.12),
                            shape: BoxShape.circle,
                          ),
                          child: Icon(
                            isSaudavel
                                ? Icons.check
                                : Icons.warning_amber_rounded,
                            color: cor,
                            size: 12,
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                rotulo,
                                style: GoogleFonts.newsreader(
                                  fontSize: 15,
                                  fontWeight: FontWeight.w500,
                                  color: cor,
                                  height: 1.1,
                                ),
                              ),
                              Text(
                                ts,
                                style: GoogleFonts.ibmPlexMono(
                                  fontSize: 9,
                                  color: CeresColors.ink3,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          '${(d.confianca * 100).toStringAsFixed(0)}%',
                          style: GoogleFonts.newsreader(
                            fontSize: 18,
                            fontWeight: FontWeight.w500,
                            color: cor,
                            height: 1,
                          ),
                        ),
                        if (baixaConfianca)
                          Text(
                            '⚠ baixa',
                            style: GoogleFonts.ibmPlexMono(
                              fontSize: 8,
                              color: CeresColors.dryGrass,
                            ),
                          )
                        else
                          Text(
                            '${d.latenciaMs} ms',
                            style: GoogleFonts.ibmPlexMono(
                              fontSize: 8,
                              color: CeresColors.ink3,
                            ),
                          ),
                      ],
                    ),
                    children: [
                      if (scores.isNotEmpty) ...[
                        Container(
                          height: 0.5,
                          color: CeresColors.hairline,
                          margin: const EdgeInsets.only(bottom: 10),
                        ),
                        Text(
                          'SCORES POR CLASSE',
                          style: GoogleFonts.ibmPlexMono(
                            fontSize: 8,
                            letterSpacing: 0.5,
                            color: CeresColors.ink3,
                          ),
                        ),
                        const SizedBox(height: 8),
                        ..._barras(scores),
                      ],
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ── Score bars ───────────────────────────────────────────────────────────────
  List<Widget> _barras(Map<String, double> scores) {
    final sorted = scores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    return sorted.take(5).map((e) {
      final isTop = e == sorted.first;
      final barColor = isTop
          ? (e.key == 'saudavel' ? CeresColors.leafLive : CeresColors.blight)
          : CeresColors.hairline;
      return Padding(
        padding: const EdgeInsets.only(bottom: 6),
        child: Row(
          children: [
            SizedBox(
              width: 140,
              child: Text(
                ResultadoInferencia.rotuloDeClasse(e.key),
                style: GoogleFonts.ibmPlexSans(
                  fontSize: 10,
                  color: CeresColors.ink2,
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Stack(
                children: [
                  // Track
                  Container(
                    height: 3,
                    decoration: BoxDecoration(
                      color: CeresColors.dust,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                  // Fill
                  FractionallySizedBox(
                    widthFactor: e.value.clamp(0.0, 1.0),
                    child: Container(
                      height: 3,
                      decoration: BoxDecoration(
                        color: barColor,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 6),
            SizedBox(
              width: 32,
              child: Text(
                '${(e.value * 100).toStringAsFixed(0)}%',
                textAlign: TextAlign.right,
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 9,
                  color: CeresColors.ink3,
                ),
              ),
            ),
          ],
        ),
      );
    }).toList();
  }

  // ── Estado vazio ─────────────────────────────────────────────────────────────
  Widget _vazio() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.save_outlined,
            size: 48,
            color: CeresColors.ink3.withValues(alpha: 0.35),
          ),
          const SizedBox(height: 14),
          Text(
            'Nenhum diagnóstico salvo',
            style: GoogleFonts.newsreader(
              fontSize: 18,
              color: CeresColors.ink2,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'os resultados são salvos automaticamente',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 10,
              color: CeresColors.ink3,
            ),
          ),
        ],
      ),
    );
  }

  // ── Confirmar limpeza ────────────────────────────────────────────────────────
  Future<void> _confirmarLimpeza(BuildContext context) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        backgroundColor: CeresColors.paper,
        title: Text(
          'Limpar histórico local?',
          style: GoogleFonts.newsreader(
            fontSize: 18,
            color: CeresColors.ink,
          ),
        ),
        content: Text(
          'Todos os diagnósticos salvos serão removidos do dispositivo.',
          style: GoogleFonts.ibmPlexSans(
            fontSize: 13,
            color: CeresColors.ink2,
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text(
              'Cancelar',
              style: GoogleFonts.ibmPlexSans(color: CeresColors.ink3),
            ),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text(
              'Limpar',
              style: GoogleFonts.ibmPlexSans(color: CeresColors.blight),
            ),
          ),
        ],
      ),
    );
    if (ok == true) await appDb.limpar();
  }
}
