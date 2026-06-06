// Paleta Taxonomia Viva — derivada do cerrado mato-grossense
// Convertida de OKLCH (design) para sRGB hex (Flutter)
//
// bone        : terra seca clareada pelo sol — fundo do app
// paper       : caderno botânico — cards e superfícies elevadas
// ink         : nanquim castanho-escuro — texto principal
// leaf-deep   : verde profundo do dossel — AppBar / header
// leaf-dark   : verde de folha madura — botões primários
// leaf-live   : verde vigoroso — status saudável
// blight      : ferrugem terracota — status doença
// dry-grass   : capim do cerrado na seca — alerta / baixa confiança
// dust        : poeira de estrada — bordas e divisórias

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CeresColors {
  CeresColors._();

  // ── Superfícies ────────────────────────────────────────────────────────────
  static const Color bone       = Color(0xFFF1ECE5); // fundo geral
  static const Color paper      = Color(0xFFFAF4EB); // cards / screens
  static const Color paper2     = Color(0xFFF5EFE4); // cards ligeiramente mais escuros

  // ── Texto ─────────────────────────────────────────────────────────────────
  static const Color ink        = Color(0xFF261E19); // texto principal
  static const Color ink2       = Color(0xFF4F4741); // texto secundário
  static const Color ink3       = Color(0xFF7E7872); // rótulos, placeholders

  // ── Verde cerrado ─────────────────────────────────────────────────────────
  static const Color leafDeep   = Color(0xFF1A2D1D); // AppBar / header
  static const Color leafDark   = Color(0xFF2B412B); // botões primários
  static const Color leafLive   = Color(0xFF5D8650); // status saudável
  static const Color leafSoft   = Color(0xFFA9BCA0); // tag / badge verde claro

  // ── Diagnóstico ───────────────────────────────────────────────────────────
  static const Color blight     = Color(0xFFA64636); // doença crítica
  static const Color blightSoft = Color(0xFFECC5BC); // fundo badge doença
  static const Color dryGrass   = Color(0xFFC69245); // alerta / baixa confiança
  static const Color dryGrassSoft = Color(0xFFF2E4C4); // fundo badge alerta

  // ── Estrutura ─────────────────────────────────────────────────────────────
  static const Color dust       = Color(0xFFD4CEC6); // bordas
  static const Color dust2      = Color(0xFFE6E0D9); // bordas suaves / fundo de barra
  static const Color hairline   = Color(0xFFC8C1B9); // divisórias finas

  // ── Tons adicionais ───────────────────────────────────────────────────────
  static const Color boneDeep          = Color(0xFFE9E2D9); // fundo recuado / chips
  static const Color actionBoxBg       = Color(0xFFFFEFEA); // fundo box "ação recomendada"
  static const Color actionBoxBorder   = Color(0xFFE8B7AA); // borda box ação
  static const Color splashLeafAccent  = Color(0xFFB8CBAA); // wordmark sobre verde (splash)

  // ── Semântica ─────────────────────────────────────────────────────────────
  /// Retorna a cor de status com base na classe e confiança.
  static Color statusColor(String classe, double confianca) {
    if (classe == 'saudavel') return leafLive;
    if (confianca < 0.40) return dryGrass;
    return blight;
  }

  /// Retorna a cor de fundo do badge de status.
  static Color statusBgColor(String classe, double confianca) {
    if (classe == 'saudavel') return leafSoft.withValues(alpha: 0.3);
    if (confianca < 0.40) return dryGrassSoft;
    return blightSoft;
  }

  /// Retorna a cor primária de um CeresStatus (usado em ceres_widgets).
  static Color forStatus(CeresStatus s) {
    switch (s) {
      case CeresStatus.healthy: return leafLive;
      case CeresStatus.warn:    return dryGrass;
      case CeresStatus.disease: return blight;
    }
  }
}

class CeresTheme {
  CeresTheme._();

  static ThemeData get theme {
    final base = ThemeData(
      colorScheme: const ColorScheme(
        brightness: Brightness.light,
        primary:          CeresColors.leafDark,
        onPrimary:        CeresColors.paper,
        primaryContainer: CeresColors.leafSoft,
        onPrimaryContainer: CeresColors.leafDeep,
        secondary:        CeresColors.leafLive,
        onSecondary:      CeresColors.paper,
        secondaryContainer: Color(0xFFD6E8CF),
        onSecondaryContainer: CeresColors.leafDeep,
        error:            CeresColors.blight,
        onError:          CeresColors.paper,
        errorContainer:   CeresColors.blightSoft,
        onErrorContainer: CeresColors.blight,
        surface:          CeresColors.paper,
        onSurface:        CeresColors.ink,
        onSurfaceVariant: CeresColors.ink2,
        outline:          CeresColors.dust,
        outlineVariant:   CeresColors.hairline,
        shadow:           Color(0xFF1A120A),
        scrim:            Color(0xFF1A120A),
        inverseSurface:   CeresColors.ink,
        onInverseSurface: CeresColors.bone,
        inversePrimary:   CeresColors.leafSoft,
      ),
      scaffoldBackgroundColor: CeresColors.bone,
      useMaterial3: true,
    );

    // Tipografia: IBM Plex Sans corpo + IBM Plex Mono para dados
    final textTheme = GoogleFonts.ibmPlexSansTextTheme(base.textTheme).copyWith(
      displayLarge:  GoogleFonts.newsreader(fontSize: 57, fontWeight: FontWeight.w500, letterSpacing: -1.5, color: CeresColors.ink),
      displayMedium: GoogleFonts.newsreader(fontSize: 45, fontWeight: FontWeight.w500, letterSpacing: -1.0, color: CeresColors.ink),
      displaySmall:  GoogleFonts.newsreader(fontSize: 36, fontWeight: FontWeight.w500, letterSpacing: -0.5, color: CeresColors.ink),
      headlineLarge: GoogleFonts.newsreader(fontSize: 32, fontWeight: FontWeight.w500, letterSpacing: -0.3, color: CeresColors.ink),
      headlineMedium:GoogleFonts.newsreader(fontSize: 26, fontWeight: FontWeight.w500, letterSpacing: -0.2, color: CeresColors.ink),
      headlineSmall: GoogleFonts.newsreader(fontSize: 22, fontWeight: FontWeight.w500, color: CeresColors.ink),
      titleLarge:    GoogleFonts.ibmPlexSans(fontSize: 18, fontWeight: FontWeight.w600, letterSpacing: -0.1, color: CeresColors.ink),
      titleMedium:   GoogleFonts.ibmPlexSans(fontSize: 16, fontWeight: FontWeight.w600, color: CeresColors.ink),
      titleSmall:    GoogleFonts.ibmPlexSans(fontSize: 14, fontWeight: FontWeight.w600, color: CeresColors.ink),
      bodyLarge:     GoogleFonts.ibmPlexSans(fontSize: 16, fontWeight: FontWeight.w400, color: CeresColors.ink),
      bodyMedium:    GoogleFonts.ibmPlexSans(fontSize: 14, fontWeight: FontWeight.w400, color: CeresColors.ink2),
      bodySmall:     GoogleFonts.ibmPlexSans(fontSize: 12, fontWeight: FontWeight.w400, color: CeresColors.ink3),
      labelLarge:    GoogleFonts.ibmPlexSans(fontSize: 14, fontWeight: FontWeight.w600, letterSpacing: 0.1, color: CeresColors.ink),
      labelMedium:   GoogleFonts.ibmPlexMono(fontSize: 12, fontWeight: FontWeight.w500, letterSpacing: 0.05, color: CeresColors.ink2),
      labelSmall:    GoogleFonts.ibmPlexMono(fontSize: 10, fontWeight: FontWeight.w400, letterSpacing: 0.15, color: CeresColors.ink3),
    );

    return base.copyWith(
      textTheme: textTheme,
      primaryTextTheme: textTheme,

      appBarTheme: AppBarTheme(
        backgroundColor: CeresColors.leafDeep,
        foregroundColor: CeresColors.paper,
        elevation: 0,
        scrolledUnderElevation: 1,
        titleTextStyle: GoogleFonts.ibmPlexSans(
          fontSize: 17,
          fontWeight: FontWeight.w600,
          letterSpacing: -0.1,
          color: CeresColors.paper,
        ),
        iconTheme: const IconThemeData(color: CeresColors.paper),
      ),

      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: CeresColors.hairline, width: 1),
        ),
        color: CeresColors.paper,
        margin: EdgeInsets.zero,
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: CeresColors.leafDark,
          foregroundColor: CeresColors.paper,
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          elevation: 0,
          textStyle: GoogleFonts.ibmPlexSans(
            fontSize: 14, fontWeight: FontWeight.w600, letterSpacing: 0.1),
        ),
      ),

      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: CeresColors.leafDark,
          side: const BorderSide(color: CeresColors.leafDark, width: 1.5),
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          textStyle: GoogleFonts.ibmPlexSans(
            fontSize: 14, fontWeight: FontWeight.w600, letterSpacing: 0.1),
        ),
      ),

      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: CeresColors.paper,
        indicatorColor: CeresColors.leafSoft.withValues(alpha: 0.35),
        iconTheme: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return const IconThemeData(color: CeresColors.leafDark, size: 22);
          }
          return const IconThemeData(color: CeresColors.ink3, size: 22);
        }),
        labelTextStyle: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return GoogleFonts.ibmPlexSans(
              fontSize: 11, fontWeight: FontWeight.w600, color: CeresColors.leafDark);
          }
          return GoogleFonts.ibmPlexSans(
            fontSize: 11, fontWeight: FontWeight.w400, color: CeresColors.ink3);
        }),
      ),

      dividerTheme: const DividerThemeData(
        color: CeresColors.hairline,
        thickness: 1,
        space: 1,
      ),

      progressIndicatorTheme: const ProgressIndicatorThemeData(
        color: CeresColors.leafLive,
        linearTrackColor: CeresColors.dust,
      ),

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: CeresColors.paper2,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: CeresColors.dust),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: CeresColors.dust),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: CeresColors.leafDark, width: 1.5),
        ),
        labelStyle: GoogleFonts.ibmPlexSans(color: CeresColors.ink2, fontSize: 14),
        hintStyle: GoogleFonts.ibmPlexSans(color: CeresColors.ink3, fontSize: 14),
      ),

      listTileTheme: const ListTileThemeData(
        tileColor: CeresColors.paper,
        contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      ),

      chipTheme: ChipThemeData(
        backgroundColor: CeresColors.paper2,
        labelStyle: GoogleFonts.ibmPlexMono(fontSize: 11, color: CeresColors.ink2),
        side: const BorderSide(color: CeresColors.dust),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      ),
    );
  }
}

// ===========================================================================
// STATUS — enum semântico de saúde da planta
// ===========================================================================
enum CeresStatus { healthy, warn, disease }

extension CeresStatusColor on CeresStatus {
  Color get color {
    switch (this) {
      case CeresStatus.healthy: return CeresColors.leafLive;
      case CeresStatus.warn:    return CeresColors.dryGrass;
      case CeresStatus.disease: return CeresColors.blight;
    }
  }
}

// ===========================================================================
// TIPOGRAFIA — atalhos estáticos para os três pesos visuais
// ===========================================================================
class CeresType {
  CeresType._();

  static TextStyle serif([TextStyle? s]) => GoogleFonts.newsreader(textStyle: s);
  static TextStyle sans([TextStyle? s])  => GoogleFonts.ibmPlexSans(textStyle: s);
  static TextStyle mono([TextStyle? s])  => GoogleFonts.ibmPlexMono(textStyle: s);

  static TextStyle get display => serif(const TextStyle(
        fontSize: 32, fontWeight: FontWeight.w500, height: 1.02,
        letterSpacing: -0.7, color: CeresColors.ink));

  static TextStyle get pageTitle => serif(const TextStyle(
        fontSize: 22, fontWeight: FontWeight.w500,
        letterSpacing: -0.3, color: CeresColors.ink));

  /// Nome da doença em destaque.
  static TextStyle get diseaseName => serif(const TextStyle(
        fontSize: 22, fontWeight: FontWeight.w500, height: 1.1,
        letterSpacing: -0.35, color: CeresColors.ink));

  /// Nome científico — itálico de herbário.
  static TextStyle get latin => serif(const TextStyle(
        fontSize: 13, fontStyle: FontStyle.italic, color: CeresColors.ink2));

  /// Valor grande de sensor ou métrica.
  static TextStyle get metricValue => serif(const TextStyle(
        fontSize: 24, fontWeight: FontWeight.w500, height: 1,
        letterSpacing: -0.45, color: CeresColors.ink));

  static TextStyle get body => sans(const TextStyle(
        fontSize: 13, height: 1.45, color: CeresColors.ink2));

  static TextStyle get button => sans(const TextStyle(
        fontSize: 13, fontWeight: FontWeight.w500, letterSpacing: 0.2));

  /// Rótulo técnico — mono caps espaçado.
  static TextStyle get label => mono(const TextStyle(
        fontSize: 9, fontWeight: FontWeight.w400, letterSpacing: 1.8,
        color: CeresColors.ink3));

  static TextStyle get monoData => mono(const TextStyle(
        fontSize: 10, color: CeresColors.ink2, letterSpacing: 0.3));
}

// ===========================================================================
// ESPAÇAMENTO / RAIOS / SOMBRAS
// ===========================================================================
class CeresSpacing {
  CeresSpacing._();
  static const double xs = 4, sm = 8, md = 12, lg = 16, xl = 22, xxl = 32;
}

class CeresRadius {
  CeresRadius._();
  static const card   = Radius.circular(10);
  static const button = Radius.circular(8);
  static const chip   = Radius.circular(999);
}

class CeresShadows {
  CeresShadows._();
  static const card = [
    BoxShadow(color: Color(0x22332A1F), blurRadius: 24, offset: Offset(0, 12)),
    BoxShadow(color: Color(0x14332A1F), blurRadius: 4,  offset: Offset(0, 2)),
  ];
}

// ===========================================================================
// WIDGETS-ASSINATURA
// ===========================================================================

/// Logo Ceres — disco de instrumento + folha lanceolada + ponto focal.
/// Escala via [size]; cor via [color].
class CeresLogo extends StatelessWidget {
  final double size;
  final Color color;
  const CeresLogo({super.key, this.size = 48, this.color = CeresColors.leafDeep});

  @override
  Widget build(BuildContext context) =>
      CustomPaint(size: Size.square(size), painter: _CeresLogoPainter(color));
}

class _CeresLogoPainter extends CustomPainter {
  final Color color;
  const _CeresLogoPainter(this.color);

  @override
  void paint(Canvas canvas, Size size) {
    final c = Offset(size.width / 2, size.height / 2);
    final u = size.width / 64;
    final stroke = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2 * u
      ..strokeCap = StrokeCap.round;
    final fill = Paint()..color = color;

    canvas.drawCircle(c, 27 * u, stroke);
    for (final deg in [0.0, 90.0, 180.0, 270.0]) {
      final dx = (deg == 0) ? 1.0 : (deg == 180) ? -1.0 : 0.0;
      final dy = (deg == 90) ? 1.0 : (deg == 270) ? -1.0 : 0.0;
      final dir = Offset(dx, dy);
      canvas.drawLine(c + dir * (30 * u), c + dir * (33.5 * u), stroke);
    }
    canvas.save();
    canvas.translate(c.dx, c.dy);
    canvas.rotate(-32 * 3.1415926 / 180);
    final leaf = Path()
      ..moveTo(-19 * u, 0)
      ..quadraticBezierTo(0, -19 * u, 19 * u, 0)
      ..quadraticBezierTo(0, 19 * u, -19 * u, 0)
      ..close();
    canvas.drawPath(leaf, stroke..strokeWidth = 2.4 * u);
    canvas.drawLine(Offset(-19 * u, 0), Offset(19 * u, 0),
        Paint()
          ..color = color.withValues(alpha: 0.65)
          ..strokeWidth = 1.2 * u);
    canvas.drawCircle(Offset(8 * u, 0), 2.8 * u, fill);
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant _CeresLogoPainter old) => old.color != color;
}

/// Barra de confiança do modelo (0–1) com cor de status.
class CeresConfidenceBar extends StatelessWidget {
  final double value;
  final Color color;
  const CeresConfidenceBar({
    super.key,
    required this.value,
    this.color = CeresColors.blight,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(2),
      child: Container(
        height: 8,
        color: CeresColors.dust2,
        child: FractionallySizedBox(
          alignment: Alignment.centerLeft,
          widthFactor: value.clamp(0.0, 1.0),
          child: Container(color: color),
        ),
      ),
    );
  }
}

/// Box "Ação Recomendada" — borda esquerda colorida + ícone "!".
class CeresActionBox extends StatelessWidget {
  final String label;
  final String priority;
  final String body;
  final Color accent;
  const CeresActionBox({
    super.key,
    this.label    = 'AÇÃO RECOMENDADA',
    this.priority = 'imediata',
    required this.body,
    this.accent = CeresColors.blight,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(10, 8, 10, 9),
      decoration: BoxDecoration(
        color: CeresColors.actionBoxBg,
        border: Border(left: BorderSide(color: accent, width: 3)),
        borderRadius: const BorderRadius.all(Radius.circular(4)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            Container(
              width: 16, height: 16,
              alignment: Alignment.center,
              decoration: BoxDecoration(color: accent, shape: BoxShape.circle),
              child: Text('!', style: CeresType.serif(TextStyle(
                  color: Colors.white, fontStyle: FontStyle.italic,
                  fontWeight: FontWeight.w700, fontSize: 11, height: 1))),
            ),
            const SizedBox(width: 7),
            Text(label, style: CeresType.mono(TextStyle(
                fontSize: 8.5, letterSpacing: 1.6,
                fontWeight: FontWeight.w500, color: accent))),
            const Spacer(),
            Text(priority.toUpperCase(), style: CeresType.label),
          ]),
          const SizedBox(height: 4),
          Text(body, style: CeresType.serif(const TextStyle(
              fontSize: 12.5, fontWeight: FontWeight.w500,
              height: 1.25, color: CeresColors.ink))),
        ],
      ),
    );
  }
}

/// Métrica de sensor (temp / umidade) com ícone, valor e estado.
class CeresSensorMetric extends StatelessWidget {
  final IconData icon;
  final String name;
  final String value;
  final String unit;
  final String state;
  final CeresStatus status;
  const CeresSensorMetric({
    super.key,
    required this.icon,
    required this.name,
    required this.value,
    required this.unit,
    required this.state,
    this.status = CeresStatus.healthy,
  });

  @override
  Widget build(BuildContext context) {
    final c = status.color;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Row(children: [
          Icon(icon, size: 13, color: CeresColors.ink2),
          const SizedBox(width: 6),
          Text(name.toUpperCase(), style: CeresType.mono(const TextStyle(
              fontSize: 8, letterSpacing: 1.1, color: CeresColors.ink3))),
        ]),
        const SizedBox(height: 4),
        RichText(text: TextSpan(children: [
          TextSpan(text: value, style: CeresType.metricValue),
          TextSpan(text: unit, style: CeresType.mono(const TextStyle(
              fontSize: 11, color: CeresColors.ink3))),
        ])),
        const SizedBox(height: 6),
        Row(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 5, height: 5,
              decoration: BoxDecoration(color: c, shape: BoxShape.circle)),
          const SizedBox(width: 5),
          Text(state.toUpperCase(), style: CeresType.mono(TextStyle(
              fontSize: 8, letterSpacing: 1.1, color: c))),
        ]),
      ],
    );
  }
}

/// Pílula de status — anel semitransparente + dot central.
class CeresStatusDot extends StatelessWidget {
  final CeresStatus status;
  final double size;
  const CeresStatusDot({super.key, required this.status, this.size = 24});

  @override
  Widget build(BuildContext context) {
    final c = status.color;
    return Container(
      width: size, height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: Border.all(color: c.withValues(alpha: 0.25)),
      ),
      child: Center(
        child: Container(
          width: size / 3, height: size / 3,
          decoration: BoxDecoration(color: c, shape: BoxShape.circle),
        ),
      ),
    );
  }
}

