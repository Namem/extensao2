import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/ceres_theme.dart';
import 'ceres_icons.dart';

/// AppBar com marca botânica SVG + wordmark + subtítulo mono
/// Fidelidade pixel-perfect ao design HTML (paleta Taxonomia Viva)
///
/// [showBack] — exibe seta de voltar no lugar da marca (para telas pushadas)
/// [onBack]  — callback do back; se null usa Navigator.pop
class CeresAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String pageTitle;    // ex: "Histórico" (parte após o italic)
  final String? pageTitleItalic; // parte em itálico antes do título
  final String? pageCount;   // ex: "74 eventos"
  final List<Widget>? actions;
  final bool showBack;
  final VoidCallback? onBack;

  const CeresAppBar({
    super.key,
    required this.pageTitle,
    this.pageTitleItalic,
    this.pageCount,
    this.actions,
    this.showBack = false,
    this.onBack,
  });

  @override
  Size get preferredSize => const Size.fromHeight(84);

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.of(context).padding.top;
    return Container(
      color: CeresColors.paper,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Brand row
          Padding(
            padding: EdgeInsets.fromLTRB(showBack ? 8 : 22, top + 8, 16, 0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                if (showBack) ...[
                  // Botão de voltar estilo Ceres
                  GestureDetector(
                    onTap: onBack ?? () => Navigator.of(context).pop(),
                    child: Container(
                      width: 32,
                      height: 32,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: CeresColors.hairline),
                        color: CeresColors.paper2,
                      ),
                      child: const Icon(
                        Icons.arrow_back_ios_new_rounded,
                        size: 13,
                        color: CeresColors.ink2,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                ] else ...[
                  // Marca botânica SVG (círculo com hairline border + lente leafDeep)
                  CeresMark(
                    size: 28,
                    color: CeresColors.leafDeep,
                    borderColor: CeresColors.hairline,
                    bgColor: Colors.transparent,
                  ),
                  const SizedBox(width: 10),
                ],
                // Wordmark: "Ceres" Newsreader 17px + subtítulo mono 9px
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'Ceres',
                      style: GoogleFonts.newsreader(
                        fontSize: 17,
                        fontWeight: FontWeight.w500,
                        color: CeresColors.ink,
                        letterSpacing: -0.18,
                        height: 1.1,
                      ),
                    ),
                    Text(
                      'DIAGNÓSTICO FOLIAR',
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 8.5,
                        letterSpacing: 0.18,
                        color: CeresColors.ink3,
                        height: 1,
                      ),
                    ),
                  ],
                ),
                const Spacer(),
                ...?actions,
              ],
            ),
          ),
          // Page bar (título da tela + count)
          Padding(
            padding: const EdgeInsets.fromLTRB(22, 6, 22, 12),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.baseline,
              textBaseline: TextBaseline.alphabetic,
              children: [
                RichText(
                  text: TextSpan(
                    children: [
                      if (pageTitleItalic != null)
                        TextSpan(
                          text: pageTitle.isEmpty
                              ? '$pageTitleItalic'
                              : '$pageTitleItalic ',
                          style: GoogleFonts.newsreader(
                            fontSize: 22,
                            fontStyle: FontStyle.italic,
                            fontWeight: FontWeight.w400,
                            color: CeresColors.leafDeep,
                            letterSpacing: -0.26,
                          ),
                        ),
                      TextSpan(
                        text: pageTitle,
                        style: GoogleFonts.newsreader(
                          fontSize: 22,
                          fontWeight: FontWeight.w500,
                          color: CeresColors.ink,
                          letterSpacing: -0.26,
                        ),
                      ),
                    ],
                  ),
                ),
                if (pageCount != null) ...[
                  const Spacer(),
                  Text(
                    pageCount!,
                    style: GoogleFonts.ibmPlexMono(
                      fontSize: 10,
                      color: CeresColors.ink3,
                      letterSpacing: 0.1,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// Botão de ícone SVG circular — fiel ao `.iconbtn` do HTML design
class CeresIconButton extends StatelessWidget {
  final String svgString;
  final VoidCallback? onPressed;
  final String? tooltip;

  const CeresIconButton({
    super.key,
    required this.svgString,
    this.onPressed,
    this.tooltip,
  });

  /// Construtor de conveniência para ícones Material (fallback)
  static Widget material(
    IconData icon, {
    VoidCallback? onPressed,
    String? tooltip,
  }) {
    return _CeresIconButtonMaterial(
      icon: icon,
      onPressed: onPressed,
      tooltip: tooltip ?? '',
    );
  }

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip ?? '',
      child: GestureDetector(
        onTap: onPressed,
        child: Container(
          width: 32,
          height: 32,
          margin: const EdgeInsets.only(left: 6),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: CeresColors.hairline),
            color: CeresColors.paper2,
          ),
          padding: const EdgeInsets.all(8),
          child: SvgPicture.string(
            svgString,
            theme: const SvgTheme(currentColor: CeresColors.ink2),
          ),
        ),
      ),
    );
  }
}

class _CeresIconButtonMaterial extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onPressed;
  final String tooltip;

  const _CeresIconButtonMaterial({
    required this.icon,
    required this.tooltip,
    this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip,
      child: GestureDetector(
        onTap: onPressed,
        child: Container(
          width: 32,
          height: 32,
          margin: const EdgeInsets.only(left: 6),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: CeresColors.hairline),
            color: CeresColors.paper2,
          ),
          child: Icon(icon, size: 15, color: CeresColors.ink2),
        ),
      ),
    );
  }
}
