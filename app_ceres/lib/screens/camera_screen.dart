import 'dart:convert';
import 'dart:io';

import 'package:drift/drift.dart' show Value;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:image_picker/image_picker.dart';

import '../config.dart' as app_config;
import '../data/doencas_data.dart';
import '../database/database.dart';
import '../models/resultado_inferencia.dart';
import '../services/api_service.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_app_bar.dart';
import '../widgets/ceres_icons.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  File? _imagem;
  ResultadoInferencia? _resultado;
  bool _carregando = false;
  String? _erro;
  bool _salvo = false;

  final _picker = ImagePicker();

  Future<void> _capturar(ImageSource fonte) async {
    final picked = await _picker.pickImage(
      source: fonte,
      maxWidth: 640,
      maxHeight: 640,
      imageQuality: 90,
    );
    if (picked == null) return;
    setState(() {
      _imagem = File(picked.path);
      _resultado = null;
      _erro = null;
      _salvo = false;
    });
    await _inferir();
  }

  Future<void> _inferir() async {
    if (_imagem == null) return;
    setState(() { _carregando = true; _erro = null; });
    try {
      final res = await ApiService.instance.inferir(_imagem!);
      setState(() => _resultado = res);
      await appDb.salvar(DiagnosticosLocaisCompanion(
        timestamp: Value(DateTime.now()),
        classe: Value(res.classe),
        confianca: Value(res.confianca),
        latenciaMs: Value(res.latenciaMs),
        scoresJson: Value(jsonEncode(res.scores)),
        imagemPath: Value(_imagem!.path),
      ));
      setState(() => _salvo = true);
    } catch (e) {
      setState(() => _erro = e.toString());
    } finally {
      setState(() => _carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final temCamera = !kIsWeb && !Platform.isWindows;
    return Scaffold(
      appBar: CeresAppBar(
        pageTitleItalic: 'Diagnóstico',
        pageTitle: '',
        actions: [
          CeresIconButton(
            svgString: CeresIconsSvg.tabEnciclopedia,
            tooltip: 'Diagnósticos salvos',
            onPressed: () => Navigator.pushNamed(context, '/salvos'),
          ),
        ],
      ),
      backgroundColor: CeresColors.bone,
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 14),
            _viewfinder(),
            const SizedBox(height: 10),
            if (_carregando) _loadingBar(),
            if (_erro != null) _erroCard(),
            if (_resultado != null) ...[
              _resultCard(),
              const SizedBox(height: 6),
              _sobreDoenca(),
              const SizedBox(height: 6),
              _scores(),
            ],
            const SizedBox(height: 10),
            _botoes(temCamera),
            if (_salvo) _salvoIndicator(),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  // ── Viewfinder ─────────────────────────────────────────────────────────────
  Widget _viewfinder() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 22),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(10),
        child: Stack(
          children: [
            // Background (imagem ou gradiente verde-escuro)
            if (_imagem != null)
              Image.file(_imagem!,
                  height: 180, width: double.infinity, fit: BoxFit.cover)
            else
              Container(
                height: 180,
                decoration: const BoxDecoration(
                  gradient: RadialGradient(
                    center: Alignment(0, 0.2),
                    radius: 0.85,
                    colors: [
                      Color(0xFF3E6B40),
                      Color(0xFF2A4F2C),
                      Color(0xFF1A3320),
                    ],
                  ),
                ),
                child: const Center(
                  child: Icon(Icons.eco_outlined,
                      size: 48, color: Color(0x55A9BCA0)),
                ),
              ),
            // Brackets nos cantos
            ..._brackets(),
            // Reticle (mira circular)
            if (_imagem == null)
              Center(
                child: Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(
                        color: CeresColors.paper.withValues(alpha: 0.5),
                        width: 1),
                  ),
                ),
              ),
            // Badge superior
            Positioned(
              top: 10,
              left: 0,
              right: 0,
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: Colors.black.withValues(alpha: 0.55),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    _imagem == null ? 'AGUARDANDO AMOSTRA' : 'ANALISANDO',
                    style: GoogleFonts.ibmPlexMono(
                      fontSize: 9,
                      letterSpacing: 0.12,
                      color: CeresColors.paper.withValues(alpha: 0.85),
                    ),
                  ),
                ),
              ),
            ),
            // Meta inferior
            Positioned(
              bottom: 10,
              left: 12,
              child: Row(
                children: [
                  Container(
                    width: 6, height: 6,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: CeresColors.blight,
                      boxShadow: [
                        BoxShadow(
                            color: CeresColors.blight.withValues(alpha: 0.3),
                            blurRadius: 4,
                            spreadRadius: 2)
                      ],
                    ),
                  ),
                  const SizedBox(width: 5),
                  Text(
                    'CERES · EXP-E · INT8',
                    style: GoogleFonts.ibmPlexMono(
                      fontSize: 9,
                      letterSpacing: 0.08,
                      color: CeresColors.paper.withValues(alpha: 0.85),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<Widget> _brackets() {
    const s = 20.0;
    const t = 1.5;
    const pad = 10.0;
    const c = Color(0xCCFAF4EB);
    return [
      Positioned(top: pad, left: pad,
          child: _bracket(s, t, c, top: true, left: true)),
      Positioned(top: pad, right: pad,
          child: _bracket(s, t, c, top: true, left: false)),
      Positioned(bottom: pad, left: pad,
          child: _bracket(s, t, c, top: false, left: true)),
      Positioned(bottom: pad, right: pad,
          child: _bracket(s, t, c, top: false, left: false)),
    ];
  }

  Widget _bracket(double s, double t, Color c,
      {required bool top, required bool left}) {
    return SizedBox(
      width: s, height: s,
      child: CustomPaint(
        painter: _BracketPainter(t, c, top: top, left: left),
      ),
    );
  }

  // ── Loading ────────────────────────────────────────────────────────────────
  Widget _loadingBar() {
    return const Padding(
      padding: EdgeInsets.symmetric(horizontal: 22, vertical: 4),
      child: LinearProgressIndicator(
        backgroundColor: CeresColors.bone,
        color: CeresColors.leafLive,
        minHeight: 2,
      ),
    );
  }

  // ── Erro ───────────────────────────────────────────────────────────────────
  Widget _erroCard() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 8, 22, 0),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: CeresColors.blightSoft,
          border: Border.all(color: CeresColors.blight.withValues(alpha: 0.4)),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Text('Erro: $_erro',
            style: GoogleFonts.ibmPlexMono(
                fontSize: 12, color: CeresColors.blight)),
      ),
    );
  }

  // ── Result card ────────────────────────────────────────────────────────────
  Widget _resultCard() {
    final r = _resultado!;
    final baixaConfianca = r.confianca < app_config.Config.confiancaMinima;
    final cor = CeresColors.statusColor(r.classe, r.confianca);

    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 10, 22, 0),
      child: _CornerMarkedBox(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Linha principal: nome + severidade
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'DX · ${r.classe.split("_").first.toUpperCase()}',
                          style: GoogleFonts.ibmPlexMono(
                            fontSize: 9,
                            letterSpacing: 0.16,
                            color: CeresColors.ink3,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          r.rotulo,
                          style: GoogleFonts.newsreader(
                            fontSize: 22,
                            fontWeight: FontWeight.w500,
                            letterSpacing: -0.3,
                            color: CeresColors.ink,
                            height: 1.1,
                          ),
                        ),
                        Text(
                          infoDoenca(r.classe).nomeLatim,
                          style: GoogleFonts.newsreader(
                            fontSize: 12,
                            fontStyle: FontStyle.italic,
                            color: CeresColors.ink2,
                          ),
                        ),
                      ],
                    ),
                  ),
                  // Severidade
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('CONF.',
                          style: GoogleFonts.ibmPlexMono(
                              fontSize: 9,
                              letterSpacing: 0.16,
                              color: CeresColors.ink3)),
                      const SizedBox(height: 4),
                      Text(
                        '${(r.confianca * 100).toStringAsFixed(1)}%',
                        style: GoogleFonts.ibmPlexMono(
                          fontSize: 13,
                          fontWeight: FontWeight.w500,
                          color: cor,
                          letterSpacing: 0.05,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 12),
              // Barra de confiança
              _confidenceBar(r.confianca, cor),
              const SizedBox(height: 6),
              // Latência
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('LATÊNCIA API',
                      style: GoogleFonts.ibmPlexMono(
                          fontSize: 9, letterSpacing: 0.14, color: CeresColors.ink3)),
                  Text('${r.latenciaMs} ms',
                      style: GoogleFonts.ibmPlexMono(
                          fontSize: 9, letterSpacing: 0.05, color: CeresColors.ink2)),
                ],
              ),
              if (baixaConfianca) ...[
                const SizedBox(height: 8),
                Text(
                  'Confiança baixa — tente melhor iluminação.',
                  style: GoogleFonts.ibmPlexMono(
                      fontSize: 9.5, color: CeresColors.dryGrass, letterSpacing: 0.02),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _confidenceBar(double pct, Color cor) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('CONFIANÇA',
                style: GoogleFonts.ibmPlexMono(
                    fontSize: 9, letterSpacing: 0.14, color: CeresColors.ink3)),
            Text('${(pct * 100).toStringAsFixed(1)}%',
                style: GoogleFonts.ibmPlexMono(
                    fontSize: 9,
                    fontWeight: FontWeight.w500,
                    color: CeresColors.ink,
                    letterSpacing: 0.05)),
          ],
        ),
        const SizedBox(height: 5),
        ClipRRect(
          borderRadius: BorderRadius.circular(2),
          child: Stack(
            children: [
              Container(height: 7, color: CeresColors.dust),
              FractionallySizedBox(
                widthFactor: pct.clamp(0.0, 1.0),
                child: Container(
                  height: 7,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: [
                      cor.withValues(alpha: 0.7),
                      cor,
                    ]),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              // Ticks em 25% e 50%
              for (final frac in [0.25, 0.5])
                Positioned(
                  left: null,
                  top: 0, bottom: 0,
                  child: FractionallySizedBox(
                    widthFactor: frac,
                    child: Align(
                      alignment: Alignment.centerRight,
                      child: Container(width: 1, color: CeresColors.paper2),
                    ),
                  ),
                ),
            ],
          ),
        ),
        const SizedBox(height: 3),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: ['0', '25', '50', '75', '100']
              .map((t) => Text(t,
                  style: GoogleFonts.ibmPlexMono(
                      fontSize: 8, color: CeresColors.ink3, letterSpacing: 0.06)))
              .toList(),
        ),
      ],
    );
  }

  // ── Sobre a doença ─────────────────────────────────────────────────────────
  Widget _sobreDoenca() {
    final r = _resultado!;
    final info = _infoDoenca(r.classe);
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text('SOBRE A DOENÇA',
                  style: GoogleFonts.ibmPlexMono(
                      fontSize: 8.5, letterSpacing: 0.2, color: CeresColors.ink3)),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                decoration: BoxDecoration(
                  color: CeresColors.bone,
                  border: Border.all(color: CeresColors.hairline),
                  borderRadius: BorderRadius.circular(3),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 6, height: 6,
                      decoration: BoxDecoration(
                          shape: BoxShape.circle, color: info.corAgente),
                    ),
                    const SizedBox(width: 5),
                    Text(info.tipoAgente,
                        style: GoogleFonts.ibmPlexSans(
                            fontSize: 9.5, color: CeresColors.ink, letterSpacing: 0.02)),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            info.descricao,
            style: GoogleFonts.newsreader(
                fontSize: 12, color: CeresColors.ink2, height: 1.35),
          ),
          const SizedBox(height: 7),
          // Action box
          Container(
            padding: const EdgeInsets.fromLTRB(9, 6, 9, 7),
            decoration: BoxDecoration(
              color: const Color(0xFFF7EDE8),
              border: Border(
                left: BorderSide(color: CeresColors.blight, width: 3),
                top: BorderSide(
                    color: CeresColors.blight.withValues(alpha: 0.3), width: 1),
                right: BorderSide(
                    color: CeresColors.blight.withValues(alpha: 0.3), width: 1),
                bottom: BorderSide(
                    color: CeresColors.blight.withValues(alpha: 0.3), width: 1),
              ),
              borderRadius: const BorderRadius.only(
                topRight: Radius.circular(4),
                bottomRight: Radius.circular(4),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      width: 16, height: 16,
                      decoration: BoxDecoration(
                          shape: BoxShape.circle, color: CeresColors.blight),
                      alignment: Alignment.center,
                      child: Text('!',
                          style: GoogleFonts.newsreader(
                              fontSize: 11,
                              fontStyle: FontStyle.italic,
                              fontWeight: FontWeight.w700,
                              color: CeresColors.paper,
                              height: 1)),
                    ),
                    const SizedBox(width: 7),
                    Text('AÇÃO RECOMENDADA',
                        style: GoogleFonts.ibmPlexMono(
                            fontSize: 8.5,
                            letterSpacing: 0.18,
                            color: CeresColors.blight,
                            fontWeight: FontWeight.w500)),
                    const Spacer(),
                    Text(info.urgencia,
                        style: GoogleFonts.ibmPlexMono(
                            fontSize: 8, letterSpacing: 0.16, color: CeresColors.ink3)),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  info.acao,
                  style: GoogleFonts.newsreader(
                      fontSize: 12.5,
                      fontWeight: FontWeight.w500,
                      color: CeresColors.ink,
                      height: 1.25,
                      letterSpacing: -0.005),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ── Scores ─────────────────────────────────────────────────────────────────
  Widget _scores() {
    final r = _resultado!;
    final sorted = r.scores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    final topClasse = sorted.isNotEmpty ? sorted.first.key : '';

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 22),
      child: Container(
        decoration: const BoxDecoration(
          border: Border(top: BorderSide(color: CeresColors.hairline)),
          color: CeresColors.paper,
        ),
        padding: const EdgeInsets.fromLTRB(4, 6, 4, 0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(bottom: 4, left: 2, right: 2),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('SCORES POR CLASSE',
                      style: GoogleFonts.ibmPlexMono(
                          fontSize: 8.5, letterSpacing: 0.16, color: CeresColors.ink3)),
                  Text('PROB.',
                      style: GoogleFonts.ibmPlexMono(
                          fontSize: 8.5, letterSpacing: 0.16, color: CeresColors.ink3)),
                ],
              ),
            ),
            ...sorted.map((e) {
              final isTop = e.key == topClasse;
              final barColor = isTop
                  ? (topClasse == 'saudavel'
                      ? CeresColors.leafLive
                      : CeresColors.blight)
                  : CeresColors.ink3;
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 1.5),
                child: Row(
                  children: [
                    SizedBox(
                      width: 14,
                      child: Text(
                        '${sorted.indexOf(e) + 1}',
                        style: GoogleFonts.ibmPlexMono(
                            fontSize: 9, color: CeresColors.ink3, letterSpacing: 0),
                        textAlign: TextAlign.right,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            ResultadoInferencia.rotuloDeClasse(e.key),
                            style: GoogleFonts.ibmPlexSans(
                              fontSize: 10.5,
                              color: isTop ? CeresColors.ink : CeresColors.ink2,
                              fontWeight: isTop ? FontWeight.w500 : FontWeight.normal,
                            ),
                          ),
                          const SizedBox(height: 3),
                          ClipRRect(
                            borderRadius: BorderRadius.circular(2),
                            child: LinearProgressIndicator(
                              value: e.value.clamp(0.0, 1.0),
                              backgroundColor: CeresColors.dust,
                              color: barColor,
                              minHeight: 3,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    SizedBox(
                      width: 36,
                      child: Text(
                        '${(e.value * 100).toStringAsFixed(0)}%',
                        style: GoogleFonts.ibmPlexMono(
                          fontSize: 10,
                          color: isTop ? barColor : CeresColors.ink2,
                          fontWeight: isTop ? FontWeight.w500 : FontWeight.normal,
                        ),
                        textAlign: TextAlign.right,
                      ),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  // ── Botões ─────────────────────────────────────────────────────────────────
  Widget _botoes(bool temCamera) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 22),
      child: Row(
        children: [
          Expanded(
            child: _ActionBtn(
              label: 'Câmera',
              icon: Icons.camera_alt_outlined,
              primary: true,
              enabled: temCamera && !_carregando,
              onTap: () => _capturar(ImageSource.camera),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: _ActionBtn(
              label: 'Galeria',
              icon: Icons.photo_library_outlined,
              primary: false,
              enabled: !_carregando,
              onTap: () => _capturar(ImageSource.gallery),
            ),
          ),
        ],
      ),
    );
  }

  Widget _salvoIndicator() {
    return Padding(
      padding: const EdgeInsets.only(top: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 5, height: 5,
            decoration: const BoxDecoration(
                shape: BoxShape.circle, color: CeresColors.leafLive),
          ),
          const SizedBox(width: 6),
          Text('Salvo localmente',
              style: GoogleFonts.ibmPlexMono(
                  fontSize: 10, color: CeresColors.leafLive, letterSpacing: 0.08)),
        ],
      ),
    );
  }

  // ── Dados estáticos das doenças ───────────────────────────────────────────
  DoencaInfo _infoDoenca(String classe) => infoDoenca(classe);

}

// ── Widgets auxiliares ───────────────────────────────────────────────────────

/// Box com marcas de registro nos cantos (estilo caderno botânico)
class _CornerMarkedBox extends StatelessWidget {
  final Widget child;
  const _CornerMarkedBox({required this.child});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          decoration: BoxDecoration(
            color: CeresColors.paper2,
            border: Border.all(color: CeresColors.hairline),
            borderRadius: BorderRadius.circular(10),
          ),
          child: child,
        ),
        // Marcas de registro
        Positioned(top: -1, left: -1,
            child: _cornerMark(top: true, left: true)),
        Positioned(bottom: -1, right: -1,
            child: _cornerMark(top: false, left: false)),
      ],
    );
  }

  Widget _cornerMark({required bool top, required bool left}) {
    return SizedBox(
      width: 8, height: 8,
      child: CustomPaint(painter: _CornerPainter(top: top, left: left)),
    );
  }
}

class _CornerPainter extends CustomPainter {
  final bool top, left;
  const _CornerPainter({required this.top, required this.left});

  @override
  void paint(Canvas canvas, Size size) {
    final p = Paint()
      ..color = CeresColors.ink3
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;
    final path = Path();
    if (top && left) {
      path.moveTo(0, size.height);
      path.lineTo(0, 0);
      path.lineTo(size.width, 0);
    } else {
      path.moveTo(0, size.height);
      path.lineTo(size.width, size.height);
      path.lineTo(size.width, 0);
    }
    canvas.drawPath(path, p);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class _BracketPainter extends CustomPainter {
  final double t;
  final Color c;
  final bool top, left;
  const _BracketPainter(this.t, this.c, {required this.top, required this.left});

  @override
  void paint(Canvas canvas, Size size) {
    final p = Paint()..color = c..strokeWidth = t..style = PaintingStyle.stroke;
    final path = Path();
    if (top && left) {
      path.moveTo(0, size.height);
      path.lineTo(0, 0);
      path.lineTo(size.width, 0);
    } else if (top && !left) {
      path.moveTo(0, 0);
      path.lineTo(size.width, 0);
      path.lineTo(size.width, size.height);
    } else if (!top && left) {
      path.moveTo(0, 0);
      path.lineTo(0, size.height);
      path.lineTo(size.width, size.height);
    } else {
      path.moveTo(0, size.height);
      path.lineTo(size.width, size.height);
      path.lineTo(size.width, 0);
    }
    canvas.drawPath(path, p);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class _ActionBtn extends StatelessWidget {
  final String label;
  final IconData icon;
  final bool primary;
  final bool enabled;
  final VoidCallback onTap;

  const _ActionBtn({
    required this.label,
    required this.icon,
    required this.primary,
    required this.enabled,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: enabled ? onTap : null,
      child: Container(
        height: 38,
        decoration: BoxDecoration(
          color: primary
              ? (enabled ? CeresColors.leafDark : CeresColors.dust)
              : CeresColors.paper2,
          border: Border.all(
            color: primary
                ? (enabled ? CeresColors.leafDeep : CeresColors.dust)
                : CeresColors.hairline,
          ),
          borderRadius: BorderRadius.circular(8),
          boxShadow: primary && enabled
              ? [
                  BoxShadow(
                      color: CeresColors.leafDeep.withValues(alpha: 0.2),
                      blurRadius: 4,
                      offset: const Offset(0, 1))
                ]
              : null,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 16,
              color: primary
                  ? (enabled ? CeresColors.paper : CeresColors.ink3)
                  : CeresColors.ink,
            ),
            const SizedBox(width: 8),
            Text(
              label,
              style: GoogleFonts.ibmPlexSans(
                fontSize: 12.5,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.02,
                color: primary
                    ? (enabled ? CeresColors.paper : CeresColors.ink3)
                    : CeresColors.ink,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
