// Ícones SVG do Ceres — strings exatas do HTML de design
// Todos usam viewBox="0 0 24 24", stroke-width="1.6", stroke icons thin

import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

/// SVG strings extraídas literalmente do HTML de design (não alterar)
class CeresIconsSvg {
  CeresIconsSvg._();

  // ── Marca botânica (appbar + splash) ──────────────────────────────────────
  // Lente botânica: círculo + cruzes cardinais + lente/folha rotacionada + ponto focal
  static const String mark = '''<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="27" stroke-width="2"/>
  <line x1="32" y1="0.5" x2="32" y2="4" stroke-width="2"/>
  <line x1="32" y1="60" x2="32" y2="63.5" stroke-width="2"/>
  <line x1="0.5" y1="32" x2="4" y2="32" stroke-width="2"/>
  <line x1="60" y1="32" x2="63.5" y2="32" stroke-width="2"/>
  <g transform="rotate(-32 32 32)">
    <path d="M 13 32 Q 32 13 51 32 Q 32 51 13 32 Z" stroke-width="2.4"/>
    <line x1="13" y1="32" x2="51" y2="32" stroke-width="1.2" opacity="0.7"/>
    <circle cx="40" cy="32" r="2.8" fill="currentColor" stroke="none"/>
  </g>
</svg>''';

  // ── Ícones da tab bar ─────────────────────────────────────────────────────
  // Tab 1: Diagnóstico — câmera com lente
  static const String tabDiagnostico = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 8h3l2-2h6l2 2h3v11H4z"/>
  <circle cx="12" cy="13" r="3.5"/>
</svg>''';

  // Tab 2: Mapa — pin de localização
  static const String tabMapa = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 21s-7-7-7-12a7 7 0 0 1 14 0c0 5-7 12-7 12z"/>
  <circle cx="12" cy="9" r="2.5"/>
</svg>''';

  // Tab 3: IoT — forma de onda ECG
  static const String tabIot = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 12h4l2-5 4 10 2-5h6"/>
</svg>''';

  // Tab 4: Enciclopédia — caderno com lombada e linhas
  static const String tabEnciclopedia = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M5 4h13a2 2 0 0 1 2 2v14H7a2 2 0 0 1-2-2V4z"/>
  <path d="M5 4v16"/>
  <path d="M9 9h7M9 13h5"/>
</svg>''';

  // Tab 5: Perfil — silhueta de pessoa
  static const String tabPerfil = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="9" r="3"/>
  <path d="M5 20a7 7 0 0 1 14 0"/>
</svg>''';

  // ── Ícones de ação no appbar ───────────────────────────────────────────────
  // Filtro / funil
  static const String iconFilter = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 5h16l-6 8v6l-4 -2v-4z"/>
</svg>''';

  // Mapa / grid de ruas
  static const String iconMapGrid = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M9 4l-6 2v14l6-2 6 2 6-2V4l-6 2z"/>
  <path d="M9 4v14M15 6v14"/>
</svg>''';

  // Busca / lupa
  static const String iconSearch = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <circle cx="11" cy="11" r="6"/>
  <path d="M16 16l4 4"/>
</svg>''';

  // Exportar / seta para cima
  static const String iconExport = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 4v12"/>
  <path d="M7 9l5-5 5 5"/>
  <path d="M5 20h14"/>
</svg>''';

  // Salvar / disquete (para ação de salvar diagnóstico)
  static const String iconSave = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 4h11a2 2 0 0 1 2 2v14H8a2 2 0 0 1-2-2V4z"/>
  <path d="M6 4v16"/>
  <path d="M10 9h6M10 13h6"/>
</svg>''';

  // Câmera (botão Câmera na tela de diagnóstico)
  static const String iconCamera = tabDiagnostico;

  // Galeria (botão Galeria na tela de diagnóstico)
  static const String iconGallery = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="5" width="18" height="14" rx="1.5"/>
  <path d="M3 16l5-5 4 4 3-3 6 6"/>
  <circle cx="9" cy="9.5" r="1.2" fill="currentColor"/>
</svg>''';

  // Seta para direita (chevron right)
  static const String iconArrowRight = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M5 12h14"/>
  <path d="M13 6l6 6-6 6"/>
</svg>''';
}

/// Widget helper — renderiza um SVG do design com cor dinâmica
class CeresSvgIcon extends StatelessWidget {
  final String svgString;
  final Color color;
  final double size;

  const CeresSvgIcon({
    super.key,
    required this.svgString,
    required this.color,
    this.size = 17,
  });

  @override
  Widget build(BuildContext context) {
    return SvgPicture.string(
      svgString,
      width: size,
      height: size,
      theme: SvgTheme(currentColor: color),
    );
  }
}

/// Marca botânica Ceres em widget — círculo com borda + lente SVG interna
class CeresMark extends StatelessWidget {
  final double size;
  final Color color;       // cor do SVG (stroke + fill)
  final Color borderColor; // cor da borda do círculo
  final Color bgColor;     // fundo do círculo

  const CeresMark({
    super.key,
    this.size = 30,
    required this.color,
    required this.borderColor,
    this.bgColor = Colors.transparent,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: bgColor,
        border: Border.all(color: borderColor, width: 1),
      ),
      padding: EdgeInsets.all(size * 0.12),
      child: SvgPicture.string(
        CeresIconsSvg.mark,
        theme: SvgTheme(currentColor: color),
      ),
    );
  }
}
