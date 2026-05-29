import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../data/doencas_data.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_app_bar.dart';

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
      appBar: const CeresAppBar(
        pageTitleItalic: 'Guia',
        pageTitle: 'de Doenças',
        pageCount: '10 classes',
      ),
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(child: _cabecalho()),
          const SliverToBoxAdapter(child: SizedBox(height: 12)),
          SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, i) {
                final codigo = _ordem[i];
                final info = kDoencas[codigo]!;
                return _itemDoenca(codigo, info);
              },
              childCount: _ordem.length,
            ),
          ),
          const SliverToBoxAdapter(child: SizedBox(height: 32)),
        ],
      ),
    );
  }

  // ── Cabeçalho informativo ────────────────────────────────────────────────────
  Widget _cabecalho() {
    final urgentes =
        _ordem.where((k) => kDoencas[k]!.urgencia == 'URGENTE').length;
    final moderadas =
        _ordem.where((k) => kDoencas[k]!.urgencia == 'MODERADO').length;

    return Container(
      margin: const EdgeInsets.fromLTRB(16, 14, 16, 0),
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
      decoration: BoxDecoration(
        color: CeresColors.paper,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: Row(
        children: [
          _statCol('URGENTES', '$urgentes', CeresColors.blight),
          Container(
              width: 0.8,
              height: 36,
              margin: const EdgeInsets.symmetric(horizontal: 16),
              color: CeresColors.hairline),
          _statCol('MODERADAS', '$moderadas', CeresColors.dryGrass),
          Container(
              width: 0.8,
              height: 36,
              margin: const EdgeInsets.symmetric(horizontal: 16),
              color: CeresColors.hairline),
          _statCol('TOTAL', '10', CeresColors.ink2),
        ],
      ),
    );
  }

  Widget _statCol(String label, String value, Color cor) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: GoogleFonts.ibmPlexMono(
              fontSize: 8, letterSpacing: 0.16, color: CeresColors.ink3),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: GoogleFonts.newsreader(
              fontSize: 22,
              fontWeight: FontWeight.w500,
              color: cor,
              height: 1),
        ),
      ],
    );
  }

  // ── Item de doença expansível ────────────────────────────────────────────────
  Widget _itemDoenca(String codigo, DoencaInfo info) {
    final aberto = _expandido == codigo;
    final isSaudavel = codigo == 'saudavel';

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
        margin: const EdgeInsets.fromLTRB(16, 0, 16, 6),
        decoration: BoxDecoration(
          color: aberto ? CeresColors.paper2 : CeresColors.paper,
          borderRadius: BorderRadius.circular(6),
          border: Border.all(
            color: aberto ? CeresColors.hairline : CeresColors.hairline,
            width: 0.8,
          ),
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(6),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Linha principal — código + nome + urgência
              IntrinsicHeight(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Faixa vertical colorida
                    Container(width: 3, color: corUrgencia),
                    // Conteúdo
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
                        child: Row(
                          children: [
                            // Código mono
                            Text(
                              info.codigo,
                              style: GoogleFonts.ibmPlexMono(
                                fontSize: 9,
                                letterSpacing: 0.14,
                                color: CeresColors.ink3,
                              ),
                            ),
                            const SizedBox(width: 10),
                            // Nome + nome latino
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    info.nomePopular,
                                    style: GoogleFonts.newsreader(
                                      fontSize: 15,
                                      fontWeight: FontWeight.w500,
                                      color: CeresColors.ink,
                                      letterSpacing: -0.005,
                                      height: 1.1,
                                    ),
                                  ),
                                  Text(
                                    info.nomeLatim,
                                    style: GoogleFonts.newsreader(
                                      fontSize: 11,
                                      fontStyle: FontStyle.italic,
                                      color: CeresColors.ink3,
                                      height: 1.2,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(width: 8),
                            // Agente + urgência
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.end,
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                _agenteBadge(info),
                                const SizedBox(height: 4),
                                Text(
                                  aberto ? '∧' : '∨',
                                  style: GoogleFonts.ibmPlexMono(
                                    fontSize: 11,
                                    color: CeresColors.ink3,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              // Conteúdo expandido
              if (aberto) ...[
                Container(height: 0.5, color: CeresColors.hairline),
                Padding(
                  padding: const EdgeInsets.fromLTRB(15, 12, 15, 14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // ── Descrição técnica ──────────────────────────────
                      Text(
                        info.descricao,
                        style: GoogleFonts.newsreader(
                          fontSize: 12.5,
                          color: CeresColors.ink2,
                          height: 1.5,
                          letterSpacing: 0.005,
                        ),
                      ),
                      const SizedBox(height: 10),

                      // ── Condições favoráveis ───────────────────────────
                      _infoRow('CONDIÇÕES', info.condicoes),
                      const SizedBox(height: 8),

                      // ── Partes afetadas (chips) ────────────────────────
                      Row(
                        children: [
                          Text(
                            'AFETA',
                            style: GoogleFonts.ibmPlexMono(
                              fontSize: 8,
                              letterSpacing: 0.18,
                              color: CeresColors.ink3,
                            ),
                          ),
                          const SizedBox(width: 8),
                          ...info.partesAfetadas.map(
                            (p) => Container(
                              margin: const EdgeInsets.only(right: 4),
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                border: Border.all(
                                    color: CeresColors.dust, width: 0.8),
                                borderRadius: BorderRadius.circular(2),
                                color: CeresColors.bone,
                              ),
                              child: Text(
                                p,
                                style: GoogleFonts.ibmPlexSans(
                                  fontSize: 9,
                                  color: CeresColors.ink2,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),

                      // ── Caixa de ação recomendada ──────────────────────
                      Container(
                        padding: const EdgeInsets.fromLTRB(10, 9, 10, 10),
                        decoration: BoxDecoration(
                          color: isSaudavel
                              ? CeresColors.leafLive.withValues(alpha: 0.05)
                              : const Color(0xFFF7EFED),
                          border: Border(
                            left: BorderSide(color: corUrgencia, width: 3),
                            top: BorderSide(
                                color: CeresColors.hairline, width: 0.8),
                            right: BorderSide(
                                color: CeresColors.hairline, width: 0.8),
                            bottom: BorderSide(
                                color: CeresColors.hairline, width: 0.8),
                          ),
                          borderRadius: const BorderRadius.only(
                            topRight: Radius.circular(4),
                            bottomRight: Radius.circular(4),
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Cabeçalho da caixa
                            Row(
                              children: [
                                Text(
                                  isSaudavel
                                      ? 'BOAS PRÁTICAS'
                                      : 'AÇÃO RECOMENDADA',
                                  style: GoogleFonts.ibmPlexMono(
                                    fontSize: 8,
                                    letterSpacing: 0.18,
                                    color: corUrgencia,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                                const Spacer(),
                                Text(
                                  info.urgencia,
                                  style: GoogleFonts.ibmPlexMono(
                                    fontSize: 8,
                                    letterSpacing: 0.14,
                                    color: CeresColors.ink3,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            // Passos numerados (split em \n)
                            ...info.acao
                                .split('\n')
                                .where((s) => s.trim().isNotEmpty)
                                .map(
                                  (passo) => Padding(
                                    padding:
                                        const EdgeInsets.only(bottom: 4),
                                    child: Text(
                                      passo,
                                      style: GoogleFonts.ibmPlexSans(
                                        fontSize: 11,
                                        color: CeresColors.ink,
                                        height: 1.4,
                                      ),
                                    ),
                                  ),
                                ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  // ── Linha de informação rótulo + valor ────────────────────────────────────
  Widget _infoRow(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: GoogleFonts.ibmPlexMono(
            fontSize: 8,
            letterSpacing: 0.18,
            color: CeresColors.ink3,
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            value,
            style: GoogleFonts.ibmPlexSans(
              fontSize: 11,
              color: CeresColors.ink2,
              height: 1.35,
            ),
          ),
        ),
      ],
    );
  }

  Widget _agenteBadge(DoencaInfo info) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: CeresColors.bone,
        borderRadius: BorderRadius.circular(3),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 5,
            height: 5,
            decoration: BoxDecoration(
              color: info.corAgente,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 4),
          Text(
            info.tipoAgente,
            style: GoogleFonts.ibmPlexSans(
              fontSize: 9,
              color: CeresColors.ink2,
              letterSpacing: 0.02,
            ),
          ),
        ],
      ),
    );
  }
}
