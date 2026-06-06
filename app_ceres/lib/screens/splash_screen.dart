import 'dart:async';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../theme/ceres_theme.dart';

class SplashScreen extends StatefulWidget {
  final Widget destino;
  const SplashScreen({super.key, required this.destino});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _progresso;
  late Animation<double> _fade;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1800),
    );
    _progresso = CurvedAnimation(parent: _ctrl, curve: Curves.easeOut);
    _fade = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(
          parent: _ctrl,
          curve: const Interval(0.0, 0.4, curve: Curves.easeIn)),
    );
    _ctrl.forward();

    // Navega depois da animação
    Timer(const Duration(milliseconds: 2200), () {
      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        PageRouteBuilder(
          pageBuilder: (context, a1, a2) => widget.destino,
          transitionsBuilder: (context, anim, _, child) =>
              FadeTransition(opacity: anim, child: child),
          transitionDuration: const Duration(milliseconds: 400),
        ),
      );
    });
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final top = MediaQuery.of(context).padding.top;
    final bottom = MediaQuery.of(context).padding.bottom;

    return Scaffold(
      backgroundColor: CeresColors.leafDeep,
      body: FadeTransition(
        opacity: _fade,
        child: Stack(
          children: [
            // Padrão topo-gráfico pontilhado (cerrado)
            CustomPaint(
              size: size,
              painter: _TopoPainter(),
            ),

            // Brackets nos cantos
            _Bracket(top: top + 60, left: 18, corners: {_Corner.tl}),
            _Bracket(top: top + 60, right: 18, corners: {_Corner.tr}),
            _Bracket(bottom: bottom + 96, left: 18, corners: {_Corner.bl}),
            _Bracket(bottom: bottom + 96, right: 18, corners: {_Corner.br}),

            // Coordenadas no topo
            Positioned(
              top: top + 56, left: 0, right: 0,
              child: Center(child: Text('15°34′S · 56°05′W',
                  style: CeresType.mono(const TextStyle(
                      fontSize: 8.5, letterSpacing: 2,
                      color: Color(0x8CF3ECD9))))),
            ),

            // Conteúdo central
            Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const CeresLogo(size: 96, color: CeresColors.paper),
                  const SizedBox(height: 26),
                  RichText(text: TextSpan(children: [
                    TextSpan(text: 'C', style: CeresType.serif(const TextStyle(
                        fontSize: 46, fontStyle: FontStyle.italic,
                        fontWeight: FontWeight.w400,
                        color: CeresColors.splashLeafAccent))),
                    TextSpan(text: 'eres', style: CeresType.serif(const TextStyle(
                        fontSize: 46, fontWeight: FontWeight.w500,
                        color: CeresColors.paper, letterSpacing: -0.9))),
                  ])),
                  const SizedBox(height: 4),
                  Text('Diagnóstico', style: CeresType.serif(const TextStyle(
                      fontSize: 14, fontStyle: FontStyle.italic,
                      color: Color(0xCCDCE6CE)))),
                  const SizedBox(height: 18),
                  Row(mainAxisSize: MainAxisSize.min, children: [
                    Container(width: 14, height: 1,
                        color: const Color(0xC7C8D7B8)),
                    const SizedBox(width: 10),
                    Text('INSTRUMENTO FOLIAR DE CAMPO',
                        style: CeresType.mono(const TextStyle(
                            fontSize: 9.5, letterSpacing: 2.8,
                            color: Color(0xC7C8D7B8)))),
                    const SizedBox(width: 10),
                    Container(width: 14, height: 1,
                        color: const Color(0xC7C8D7B8)),
                  ]),
                ],
              ),
            ),

            // Rodapé: barra de progresso + crédito
            Positioned(
              left: 28,
              right: 28,
              bottom: bottom + 32,
              child: Column(
                children: [
                  // Barra de progresso
                  AnimatedBuilder(
                    animation: _progresso,
                    builder: (context, _) => Stack(
                      children: [
                        Container(
                          height: 2,
                          decoration: BoxDecoration(
                            color: const Color(0x2DFAF2E4),
                            borderRadius: BorderRadius.circular(2),
                          ),
                        ),
                        FractionallySizedBox(
                          widthFactor: _progresso.value,
                          child: Container(
                            height: 2,
                            decoration: BoxDecoration(
                              color: const Color(0xFFFAF2E4),
                              borderRadius: BorderRadius.circular(2),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'carregando...',
                        style: GoogleFonts.ibmPlexMono(
                          fontSize: 9.5,
                          letterSpacing: 0.08,
                          color: const Color(0xB8FAF2E4),
                        ),
                      ),
                      Text(
                        'ceres_expe_int8',
                        style: GoogleFonts.ibmPlexMono(
                          fontSize: 9.5,
                          letterSpacing: 0.08,
                          color: const Color(0x72FAF2E4),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  Text(
                    'NAMEM RACHID JAUDY NETO',
                    style: GoogleFonts.ibmPlexMono(
                      fontSize: 9,
                      letterSpacing: 0.22,
                      color: const Color(0x72FAF2E4),
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
}

// ── Corner brackets ──────────────────────────────────────────────────────────
enum _Corner { tl, tr, bl, br }

class _Bracket extends StatelessWidget {
  final double? top, left, right, bottom;
  final Set<_Corner> corners;

  const _Bracket({
    this.top,
    this.left,
    this.right,
    this.bottom,
    required this.corners,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: top,
      left: left,
      right: right,
      bottom: bottom,
      child: SizedBox(
        width: 22,
        height: 22,
        child: CustomPaint(painter: _BracketPainter(corners)),
      ),
    );
  }
}

class _BracketPainter extends CustomPainter {
  final Set<_Corner> corners;
  _BracketPainter(this.corners);

  @override
  void paint(Canvas canvas, Size size) {
    final p = Paint()
      ..color = const Color(0x72FAF2E4)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    const len = 22.0;
    if (corners.contains(_Corner.tl)) {
      canvas.drawLine(Offset.zero, Offset(len, 0), p);
      canvas.drawLine(Offset.zero, Offset(0, len), p);
    }
    if (corners.contains(_Corner.tr)) {
      canvas.drawLine(Offset(size.width, 0), Offset(size.width - len, 0), p);
      canvas.drawLine(Offset(size.width, 0), Offset(size.width, len), p);
    }
    if (corners.contains(_Corner.bl)) {
      canvas.drawLine(
          Offset(0, size.height), Offset(len, size.height), p);
      canvas.drawLine(
          Offset(0, size.height), Offset(0, size.height - len), p);
    }
    if (corners.contains(_Corner.br)) {
      canvas.drawLine(Offset(size.width, size.height),
          Offset(size.width - len, size.height), p);
      canvas.drawLine(Offset(size.width, size.height),
          Offset(size.width, size.height - len), p);
    }
  }

  @override
  bool shouldRepaint(_BracketPainter old) => false;
}

// ── Padrão pontilhado cerrado ─────────────────────────────────────────────────
class _TopoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final p = Paint()
      ..color = const Color(0x14FAF2E4)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    const step = 28.0;
    for (double y = step; y < size.height; y += step) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), p);
    }
    for (double x = step; x < size.width; x += step) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), p);
    }
  }

  @override
  bool shouldRepaint(_TopoPainter old) => false;
}
