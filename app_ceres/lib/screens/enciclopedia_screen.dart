import 'package:flutter/material.dart';

import '../data/doencas_data.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';

class EnciclopediaScreen extends StatefulWidget {
  const EnciclopediaScreen({super.key});

  @override
  State<EnciclopediaScreen> createState() => _EnciclopediaScreenState();
}

class _EnciclopediaScreenState extends State<EnciclopediaScreen> {
  // Ordenação: doenças primeiro (urgentes → moderadas), saudável por último
  static final _ordem = [
    'D01_requeima',
    'D06_vira_cabeca',
    'D06b_mosaico',
    'D09_mancha_bacteriana',
    'D02_septoriose',
    'D03_pinta_preta',
    'D03b_mancha_alvo',
    'D05_mofo_foliar',
    'D07_acaro_bronzeamento',
    'saudavel',
  ];

  String? _expandido;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: SafeArea(
        bottom: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CeresBrandBar(
              subtitle: 'Enciclopédia',
              actions: [CeresIconBtn(Icons.filter_list, onTap: () {})],
            ),
            const CeresPageTitle(
              emphasis: 'Enciclopédia',
              count: '10 doenças · tomateiro',
            ),
            // barra de busca
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 22),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
                decoration: BoxDecoration(
                  color: CeresColors.paper2,
                  border: Border.all(color: CeresColors.hairline),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Row(children: [
                  const Icon(Icons.search, size: 14, color: CeresColors.ink3),
                  const SizedBox(width: 8),
                  Text('buscar por nome, sintoma, agente…',
                      style: CeresType.sans(const TextStyle(
                          fontSize: 12, color: CeresColors.ink3))),
                ]),
              ),
            ),
            const SizedBox(height: 8),
            Expanded(child: ListView(
              padding: const EdgeInsets.fromLTRB(22, 0, 22, 32),
              children: [
                const CeresSectionLabel('Fungos · 5'),
                ..._ordem.where((k) => _tipoTag(k) == 'F').map((k) =>
                    _itemDoenca(k, kDoencas[k]!)),
                const CeresSectionLabel('Bactérias · 1'),
                ..._ordem.where((k) => _tipoTag(k) == 'B').map((k) =>
                    _itemDoenca(k, kDoencas[k]!)),
                const CeresSectionLabel('Vírus · Ácaros · Saudável'),
                ..._ordem.where((k) => !['F','B'].contains(_tipoTag(k))).map((k) =>
                    _itemDoenca(k, kDoencas[k]!)),
              ],
            )),
          ],
        ),
      ),
    );
  }

  String _tipoTag(String k) {
    if (k == 'saudavel') return 'S';
    final info = kDoencas[k]!;
    if (info.tipoAgente.toLowerCase().contains('fungo')) { return 'F'; }
    if (info.tipoAgente.toLowerCase().contains('bact')) { return 'B'; }
    if (info.tipoAgente.toLowerCase().contains('vírus') ||
        info.tipoAgente.toLowerCase().contains('virus')) { return 'V'; }
    if (info.tipoAgente.toLowerCase().contains('ácar') ||
        info.tipoAgente.toLowerCase().contains('acar')) { return 'A'; }
    return 'O';
  }

  // ── Cores das tags por tipo ──────────────────────────────────────────────────
  static const _tagColors = {
    'F': (Color(0xFFF7E7DC), Color(0xFF7A3A22), Color(0xFFE3C3B2)),
    'B': (Color(0xFFF6EACF), Color(0xFF6F551E), Color(0xFFE0CB9C)),
    'V': (Color(0xFFECE2F2), Color(0xFF4F3A6B), Color(0xFFCDBCDD)),
    'A': (Color(0xFFF5E5DA), Color(0xFF6B3A22), Color(0xFFDFC2AF)),
    'S': (Color(0xFFD7E8CE), Color(0xFF2E4A2A), Color(0xFFA9BCA0)),
    'O': (Color(0xFFEAE4DA), Color(0xFF4F4741), Color(0xFFC8C1B9)),
  };

  // ── Item de doença expansível ────────────────────────────────────────────────
  Widget _itemDoenca(String codigo, DoencaInfo info) {
    final aberto = _expandido == codigo;
    final isSaudavel = codigo == 'saudavel';
    final tag = _tipoTag(codigo);
    final tc = _tagColors[tag] ?? _tagColors['O']!;

    // Cor do indicador de urgência
    Color corUrgencia;
    switch (info.urgencia) {
      case 'URGENTE':
        corUrgencia = CeresColors.blight;
        break;
      case 'MODERADO':
        corUrgencia = CeresColors.dryGrass;
        break;
      default:
        corUrgencia = CeresColors.leafLive;
    }

    return GestureDetector(
      onTap: () => setState(() => _expandido = aberto ? null : codigo),
      child: Container(
        decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: Color(0xFFEAE4DA)))),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Row(children: [
                // Tag tipo (F/B/V/A/S)
                Container(width: 32, height: 32, alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: tc.$1,
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: tc.$3),
                  ),
                  child: Text(tag, style: CeresType.serif(TextStyle(
                      fontSize: 14, fontStyle: FontStyle.italic,
                      fontWeight: FontWeight.w500, color: tc.$2))),
                ),
                const SizedBox(width: 11),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(info.nomePopular, style: CeresType.serif(const TextStyle(
                      fontSize: 13.5, fontWeight: FontWeight.w500, color: CeresColors.ink))),
                  const SizedBox(height: 1),
                  Text(info.nomeLatim, style: CeresType.latin),
                ])),
                Text(aberto ? '∨' : '›',
                    style: const TextStyle(fontSize: 16, color: CeresColors.ink3)),
              ]),
            ),

            // Conteúdo expandido
            if (aberto) ...[
              Padding(
                padding: const EdgeInsets.fromLTRB(0, 0, 0, 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(info.descricao, style: CeresType.serif(const TextStyle(
                        fontSize: 11.5, height: 1.35, color: CeresColors.ink2))),
                    const SizedBox(height: 8),

                    // Ação recomendada usando CeresActionBox
                    CeresActionBox(
                      label: isSaudavel ? 'BOAS PRÁTICAS' : 'AÇÃO RECOMENDADA',
                      body: info.acao.replaceAll('\n', ' '),
                      priority: info.urgencia,
                      accent: corUrgencia,
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

}
