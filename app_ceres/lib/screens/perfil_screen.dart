import 'dart:io';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

import '../database/database.dart';
import '../services/api_service.dart';
import '../services/auth_storage.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_app_bar.dart';
import '../widgets/offline_banner.dart';

class PerfilScreen extends StatefulWidget {
  const PerfilScreen({super.key});

  @override
  State<PerfilScreen> createState() => _PerfilScreenState();
}

class _PerfilScreenState extends State<PerfilScreen> {
  late Future<Map<String, dynamic>?> _futurePerfil;
  bool _exportando = false;

  @override
  void initState() {
    super.initState();
    _futurePerfil = _carregarPerfil();
  }

  Future<Map<String, dynamic>?> _carregarPerfil() async {
    try {
      return await ApiService.instance.me();
    } catch (_) {
      return null; // offline ou sem token
    }
  }

  // ── Logout ────────────────────────────────────────────────────────────────
  Future<void> _logout() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        backgroundColor: CeresColors.paper,
        title: Text('Sair', style: GoogleFonts.newsreader(color: CeresColors.ink)),
        content: Text(
          'Deseja encerrar a sessão?',
          style: GoogleFonts.ibmPlexSans(fontSize: 13, color: CeresColors.ink2),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('Cancelar',
                style: GoogleFonts.ibmPlexSans(color: CeresColors.ink3)),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text('Sair',
                style: GoogleFonts.ibmPlexSans(color: CeresColors.blight)),
          ),
        ],
      ),
    );
    if (ok != true || !mounted) return;
    await AuthStorage.instance.limparTokens();
    if (!mounted) return;
    Navigator.of(context).pushNamedAndRemoveUntil('/login', (_) => false);
  }

  // ── Exportar CSV ──────────────────────────────────────────────────────────
  Future<void> _exportarCsv() async {
    setState(() => _exportando = true);
    try {
      final lista = await appDb.historicoStream().first;
      if (lista.isEmpty) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Nenhum diagnóstico salvo.',
              style: GoogleFonts.ibmPlexSans(color: CeresColors.paper)),
          backgroundColor: CeresColors.ink2,
        ));
        return;
      }

      final buf = StringBuffer();
      buf.writeln('id,classe,confianca,latencia_ms,timestamp');
      for (final d in lista) {
        buf.writeln('${d.id},${d.classe},${d.confianca},'
            '${d.latenciaMs},${d.timestamp}');
      }

      final dir = await getTemporaryDirectory();
      final file = File(
          '${dir.path}/ceres_diagnosticos_${DateFormat('yyyyMMdd_HHmm').format(DateTime.now())}.csv');
      await file.writeAsString(buf.toString());

      await Share.shareXFiles(
        [XFile(file.path)],
        subject: 'Diagnósticos Ceres',
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Erro ao exportar: $e',
            style: GoogleFonts.ibmPlexSans(color: CeresColors.paper)),
        backgroundColor: CeresColors.blight,
      ));
    } finally {
      if (mounted) setState(() => _exportando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      appBar: const CeresAppBar(
        pageTitleItalic: 'Meu',
        pageTitle: 'Perfil',
      ),
      body: OfflineBanner(
        child: FutureBuilder<Map<String, dynamic>?>(
          future: _futurePerfil,
          builder: (context, snap) {
            if (snap.connectionState != ConnectionState.done) {
              return const Center(
                child: CircularProgressIndicator(
                  color: CeresColors.leafLive,
                  strokeWidth: 1.5,
                ),
              );
            }
            return _conteudo(snap.data);
          },
        ),
      ),
    );
  }

  Widget _conteudo(Map<String, dynamic>? perfil) {
    final nome    = perfil?['nome']    as String? ?? 'Usuário';
    final email   = perfil?['email']   as String? ?? '—';
    final total   = perfil?['total_diagnosticos'] as int? ?? 0;
    final doencas = perfil?['total_doencas']      as int? ?? 0;
    final saudavel= perfil?['total_saudavel']      as int? ?? 0;
    final desde   = perfil?['membro_desde']        as String? ?? '—';
    final ultimo  = perfil?['ultimo_acesso']       as String? ?? '—';
    final inicial = nome.isNotEmpty ? nome[0].toUpperCase() : 'U';

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(16, 20, 16, 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // ── Card de identidade ─────────────────────────────────────────
          Container(
            padding: const EdgeInsets.fromLTRB(16, 20, 16, 20),
            decoration: BoxDecoration(
              color: CeresColors.paper,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: CeresColors.hairline, width: 0.8),
            ),
            child: Row(
              children: [
                // Avatar
                Container(
                  width: 52,
                  height: 52,
                  decoration: BoxDecoration(
                    color: CeresColors.leafDeep,
                    shape: BoxShape.circle,
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    inicial,
                    style: GoogleFonts.newsreader(
                      fontSize: 24,
                      fontWeight: FontWeight.w500,
                      color: CeresColors.paper,
                      height: 1,
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        nome,
                        style: GoogleFonts.newsreader(
                          fontSize: 17,
                          fontWeight: FontWeight.w500,
                          color: CeresColors.ink,
                          height: 1.1,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        email,
                        style: GoogleFonts.ibmPlexSans(
                          fontSize: 11,
                          color: CeresColors.ink3,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Desde $desde',
                        style: GoogleFonts.ibmPlexMono(
                          fontSize: 8.5,
                          color: CeresColors.ink3,
                          letterSpacing: 0.1,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),

          // ── Stats ──────────────────────────────────────────────────────
          Container(
            padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
            decoration: BoxDecoration(
              color: CeresColors.paper,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: CeresColors.hairline, width: 0.8),
            ),
            child: Row(
              children: [
                _statCol('TOTAL', '$total', CeresColors.ink2),
                _divisor(),
                _statCol('DOENÇAS', '$doencas', CeresColors.blight),
                _divisor(),
                _statCol('SAUDÁVEL', '$saudavel', CeresColors.leafLive),
              ],
            ),
          ),
          const SizedBox(height: 6),

          // Último acesso
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            decoration: BoxDecoration(
              color: CeresColors.paper,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: CeresColors.hairline, width: 0.8),
            ),
            child: Row(
              children: [
                Text('ÚLTIMO ACESSO',
                    style: GoogleFonts.ibmPlexMono(
                        fontSize: 8, letterSpacing: 0.18, color: CeresColors.ink3)),
                const Spacer(),
                Text(ultimo,
                    style: GoogleFonts.ibmPlexSans(
                        fontSize: 11, color: CeresColors.ink2)),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // ── Ações ──────────────────────────────────────────────────────
          _botaoAcao(
            label: 'Exportar diagnósticos (.csv)',
            icon: Icons.download_outlined,
            cor: CeresColors.leafDeep,
            carregando: _exportando,
            onTap: _exportarCsv,
          ),
          const SizedBox(height: 8),
          _botaoAcao(
            label: 'Sair da conta',
            icon: Icons.logout_rounded,
            cor: CeresColors.blight,
            onTap: _logout,
          ),

          if (perfil == null) ...[
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(
                color: CeresColors.dryGrass.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(4),
                border: Border(
                    left: BorderSide(color: CeresColors.dryGrass, width: 3)),
              ),
              child: Text(
                'Estatísticas indisponíveis — sem conexão com o servidor.',
                style: GoogleFonts.ibmPlexSans(
                    fontSize: 11, color: CeresColors.dryGrass, height: 1.4),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _statCol(String label, String valor, Color cor) {
    return Expanded(
      child: Column(
        children: [
          Text(label,
              style: GoogleFonts.ibmPlexMono(
                  fontSize: 8, letterSpacing: 0.16, color: CeresColors.ink3)),
          const SizedBox(height: 4),
          Text(valor,
              style: GoogleFonts.newsreader(
                  fontSize: 24, fontWeight: FontWeight.w500, color: cor, height: 1)),
        ],
      ),
    );
  }

  Widget _divisor() {
    return Container(
        width: 0.8, height: 36,
        margin: const EdgeInsets.symmetric(horizontal: 8),
        color: CeresColors.hairline);
  }

  Widget _botaoAcao({
    required String label,
    required IconData icon,
    required Color cor,
    required VoidCallback onTap,
    bool carregando = false,
  }) {
    return GestureDetector(
      onTap: carregando ? null : onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 13),
        decoration: BoxDecoration(
          color: CeresColors.paper,
          borderRadius: BorderRadius.circular(6),
          border: Border.all(color: CeresColors.hairline, width: 0.8),
        ),
        child: Row(
          children: [
            carregando
                ? SizedBox(
                    width: 16, height: 16,
                    child: CircularProgressIndicator(
                        strokeWidth: 1.5, color: cor))
                : Icon(icon, size: 16, color: cor),
            const SizedBox(width: 12),
            Text(label,
                style: GoogleFonts.ibmPlexSans(
                    fontSize: 13, color: cor, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
}
