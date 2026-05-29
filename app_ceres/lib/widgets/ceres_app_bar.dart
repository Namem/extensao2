import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/ceres_theme.dart';

/// AppBar com marca Ceres — circular "C" + wordmark + subtítulo mono
class CeresAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String pageTitle;   // ex: "Diagnóstico"
  final String? pageCount;  // ex: "74 eventos"
  final List<Widget>? actions;

  const CeresAppBar({
    super.key,
    required this.pageTitle,
    this.pageCount,
    this.actions,
  });

  @override
  Size get preferredSize => const Size.fromHeight(72);

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.of(context).padding.top;
    return Container(
      color: CeresColors.paper,
      padding: EdgeInsets.fromLTRB(20, top + 10, 16, 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // Marca circular
          Container(
            width: 30,
            height: 30,
            decoration: BoxDecoration(
              color: CeresColors.leafDark,
              shape: BoxShape.circle,
              border: Border.all(
                  color: CeresColors.hairline.withValues(alpha: 0.5), width: 1),
            ),
            alignment: Alignment.center,
            child: Text(
              'C',
              style: GoogleFonts.newsreader(
                fontSize: 17,
                fontStyle: FontStyle.italic,
                fontWeight: FontWeight.w500,
                color: CeresColors.paper,
                height: 1,
              ),
            ),
          ),
          const SizedBox(width: 10),
          // Wordmark
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Ceres',
                style: GoogleFonts.newsreader(
                  fontSize: 18,
                  fontWeight: FontWeight.w500,
                  color: CeresColors.ink,
                  letterSpacing: -0.3,
                  height: 1.1,
                ),
              ),
              Text(
                pageTitle.toUpperCase(),
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 9,
                  letterSpacing: 0.18,
                  color: CeresColors.ink3,
                  height: 1,
                ),
              ),
            ],
          ),
          if (pageCount != null) ...[
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
              decoration: BoxDecoration(
                color: CeresColors.dust,
                borderRadius: BorderRadius.circular(3),
              ),
              child: Text(
                pageCount!,
                style: GoogleFonts.ibmPlexMono(
                    fontSize: 9, color: CeresColors.ink3, letterSpacing: 0.08),
              ),
            ),
          ],
          const Spacer(),
          ...?actions,
        ],
      ),
    );
  }
}

/// Botão de ícone no estilo do design (circular, hairline border)
class CeresIconButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onPressed;
  final String? tooltip;

  const CeresIconButton({
    super.key,
    required this.icon,
    this.onPressed,
    this.tooltip,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip ?? '',
      child: GestureDetector(
        onTap: onPressed,
        child: Container(
          width: 34,
          height: 34,
          margin: const EdgeInsets.only(left: 6),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: CeresColors.hairline),
            color: CeresColors.paper2,
          ),
          child: Icon(icon, size: 17, color: CeresColors.ink2),
        ),
      ),
    );
  }
}
