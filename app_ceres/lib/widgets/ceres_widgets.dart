// ─────────────────────────────────────────────────────────────────────────
// CERES · WIDGETS COMPARTILHADOS
// App bars, chips e blocos reutilizados pelas telas.
// ─────────────────────────────────────────────────────────────────────────

import 'package:flutter/material.dart';
import '../theme/ceres_theme.dart';

/// App bar de marca — logo + nome + subtítulo + ações à direita.
class CeresBrandBar extends StatelessWidget {
  final String subtitle;
  final List<Widget> actions;
  const CeresBrandBar({super.key, required this.subtitle, this.actions = const []});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 8, 18, 14),
      child: Row(children: [
        Container(
          width: 30, height: 30,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: CeresColors.hairline),
          ),
          child: const Center(child: CeresLogo(size: 18, color: CeresColors.leafDeep)),
        ),
        const SizedBox(width: 10),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Ceres', style: CeresType.serif(const TextStyle(
                fontSize: 17, fontWeight: FontWeight.w500))),
            Text(subtitle.toUpperCase(), style: CeresType.label),
          ],
        ),
        const Spacer(),
        ...actions,
      ]),
    );
  }
}

/// App bar de sub-tela — botão voltar + título + subtítulo.
class CeresSubBar extends StatelessWidget {
  final String title, subtitle;
  final List<Widget> actions;
  const CeresSubBar({super.key, required this.title, required this.subtitle,
      this.actions = const []});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(18, 8, 18, 14),
      child: Row(children: [
        InkWell(
          onTap: () => Navigator.of(context).maybePop(),
          customBorder: const CircleBorder(),
          child: Container(
            width: 32, height: 32,
            decoration: BoxDecoration(
              color: CeresColors.paper, shape: BoxShape.circle,
              border: Border.all(color: CeresColors.hairline),
            ),
            child: const Icon(Icons.chevron_left, size: 18, color: CeresColors.ink),
          ),
        ),
        const SizedBox(width: 10),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: CeresType.serif(const TextStyle(
                fontSize: 15, fontWeight: FontWeight.w500))),
            Text(subtitle.toUpperCase(), style: CeresType.label),
          ],
        ),
        const Spacer(),
        ...actions,
      ]),
    );
  }
}

/// Botão de ícone circular padrão das app bars.
class CeresIconBtn extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onTap;
  const CeresIconBtn(this.icon, {super.key, this.onTap});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 6),
      child: InkWell(
        onTap: onTap,
        customBorder: const CircleBorder(),
        child: Container(
          width: 32, height: 32,
          decoration: BoxDecoration(
            color: CeresColors.paper2, shape: BoxShape.circle,
            border: Border.all(color: CeresColors.hairline),
          ),
          child: Icon(icon, size: 15, color: CeresColors.ink2),
        ),
      ),
    );
  }
}

/// Cabeçalho de página — título serifado com ênfase itálica + contador opcional.
class CeresPageTitle extends StatelessWidget {
  final String emphasis, rest, count;
  const CeresPageTitle({super.key, required this.emphasis, this.rest = '', this.count = ''});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 0, 22, 14),
      child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
        Expanded(
          child: RichText(text: TextSpan(children: [
            TextSpan(text: emphasis, style: CeresType.serif(const TextStyle(
                fontSize: 22, fontWeight: FontWeight.w500, fontStyle: FontStyle.italic,
                color: CeresColors.leafDeep, letterSpacing: -0.3))),
            if (rest.isNotEmpty)
              TextSpan(text: ' $rest', style: CeresType.serif(const TextStyle(
                  fontSize: 22, fontWeight: FontWeight.w500, color: CeresColors.ink,
                  letterSpacing: -0.3))),
          ])),
        ),
        if (count.isNotEmpty)
          Text(count, style: CeresType.monoData),
      ]),
    );
  }
}

/// Linha horizontal de chips de filtro (rolável).
class CeresChips extends StatelessWidget {
  final List<String> labels;
  final int activeIndex;
  final ValueChanged<int>? onTap;
  const CeresChips({super.key, required this.labels, this.activeIndex = 0,
      this.onTap});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 30,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 22),
        itemCount: labels.length,
        separatorBuilder: (context, index) => const SizedBox(width: 6),
        itemBuilder: (_, i) {
          final on = i == activeIndex;
          void tap() => onTap?.call(i);
          return GestureDetector(
            onTap: tap,
            child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10),
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: on ? CeresColors.leafDark : CeresColors.paper,
              borderRadius: BorderRadius.circular(999),
              border: Border.all(color: on ? CeresColors.leafDark : CeresColors.hairline),
            ),
            child: Text(labels[i], style: CeresType.sans(TextStyle(
                fontSize: 10.5,
                color: on ? CeresColors.paper : CeresColors.ink2))),
          ));
        },
      ),
    );
  }
}

/// Card de papel com borda hairline e raio padrão Ceres.
class CeresPaperCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry padding;
  final EdgeInsetsGeometry margin;
  const CeresPaperCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(14),
    this.margin = EdgeInsets.zero,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: margin,
      padding: padding,
      decoration: BoxDecoration(
        color: CeresColors.paper2,
        border: Border.all(color: CeresColors.hairline),
        borderRadius: const BorderRadius.all(CeresRadius.card),
      ),
      child: child,
    );
  }
}

/// Cabeçalho de seção/dia em mono caps com régua à direita.
class CeresSectionLabel extends StatelessWidget {
  final String text;
  const CeresSectionLabel(this.text, {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(2, 10, 2, 6),
      child: Row(children: [
        Text(text.toUpperCase(), style: CeresType.label),
        const SizedBox(width: 8),
        const Expanded(child: Divider(height: 1)),
      ]),
    );
  }
}
