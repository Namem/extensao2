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
  static const Color hairline   = Color(0xFFC8C1B9); // divisórias finas

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
