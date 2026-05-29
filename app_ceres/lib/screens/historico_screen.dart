import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import '../models/evento_mqtt.dart';
import '../services/api_service.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_app_bar.dart';
import '../widgets/ceres_icons.dart';

class HistoricoScreen extends StatefulWidget {
  const HistoricoScreen({super.key});

  @override
  State<HistoricoScreen> createState() => _HistoricoScreenState();
}

class _HistoricoScreenState extends State<HistoricoScreen> {
  List<EventoMqtt> _eventos = [];
  bool _carregando = false;
  String? _erro;
  int _paginaAtual = 1;
  bool _temProxima = false;
  int _total = 0;

  // Dados do sensor (último evento recebido)
  EventoMqtt? get _ultimoEvento =>
      _eventos.isNotEmpty ? _eventos.first : null;

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  Future<void> _carregar({int pagina = 1}) async {
    setState(() {
      _carregando = true;
      _erro = null;
    });
    try {
      final data = await ApiService.instance.historico(page: pagina);
      setState(() {
        _eventos = data['results'] as List<EventoMqtt>;
        _temProxima = data['next'] != null;
        _total = data['count'] as int;
        _paginaAtual = pagina;
      });
    } catch (e) {
      setState(() => _erro = e.toString());
    } finally {
      setState(() => _carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      appBar: CeresAppBar(
        pageTitleItalic: 'Histórico',
        pageTitle: 'IoT',
        pageCount: '$_total · últ. 24h',
        actions: [
          CeresIconButton(
            svgString: CeresIconsSvg.iconFilter,
            tooltip: 'Filtrar',
            onPressed: _carregando ? null : () => _carregar(),
          ),
          CeresIconButton(
            svgString: CeresIconsSvg.iconMapGrid,
            tooltip: 'Mapa',
            onPressed: () {},
          ),
        ],
      ),
      body: Column(
        children: [
          _sensorCard(),
          Expanded(child: _body()),
          if (_eventos.isNotEmpty || _erro != null || _carregando)
            _rodapePaginacao(),
        ],
      ),
    );
  }

  // ── Sensor status card ──────────────────────────────────────────────────────
  Widget _sensorCard() {
    final e = _ultimoEvento;
    return Container(
      margin: const EdgeInsets.fromLTRB(16, 14, 16, 0),
      padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
      decoration: BoxDecoration(
        color: CeresColors.paper,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              // Pulse dot
              Container(
                width: 7,
                height: 7,
                decoration: BoxDecoration(
                  color: e != null ? CeresColors.leafLive : CeresColors.hairline,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 7),
              Text(
                'ESP32-S3 · SENSOR',
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 9,
                  letterSpacing: 0.6,
                  color: CeresColors.ink3,
                ),
              ),
              const Spacer(),
              if (e != null)
                Text(
                  _formatTimestampShort(e.timestamp),
                  style: GoogleFonts.ibmPlexMono(
                    fontSize: 9,
                    color: CeresColors.ink3,
                  ),
                ),
            ],
          ),
          const SizedBox(height: 12),
          // 3-col grid: temperatura / umidade_ar / umidade_solo
          Row(
            children: [
              _sensorCol(
                label: 'TEMP',
                value: e?.temperatura != null
                    ? '${e!.temperatura!.toStringAsFixed(1)}°'
                    : '--',
                unit: 'ºC',
              ),
              _divisor(),
              _sensorCol(
                label: 'UM. AR',
                value: e?.umidadeAr != null
                    ? '${e!.umidadeAr!.toStringAsFixed(0)}%'
                    : '--',
                unit: '%',
              ),
              _divisor(),
              _sensorCol(
                label: 'UM. SOLO',
                value: e?.umidadeSolo != null
                    ? '${e!.umidadeSolo!.toStringAsFixed(0)}%'
                    : '--',
                unit: '%',
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _sensorCol({
    required String label,
    required String value,
    required String unit,
  }) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text(
            label,
            style: GoogleFonts.ibmPlexMono(
              fontSize: 8,
              letterSpacing: 0.5,
              color: CeresColors.ink3,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: GoogleFonts.newsreader(
              fontSize: 26,
              fontWeight: FontWeight.w400,
              color: CeresColors.ink,
              height: 1,
            ),
          ),
        ],
      ),
    );
  }

  Widget _divisor() {
    return Container(
      width: 0.8,
      height: 40,
      color: CeresColors.hairline,
      margin: const EdgeInsets.symmetric(horizontal: 4),
    );
  }

  // ── Live MQTT strip ─────────────────────────────────────────────────────────
  Widget _liveMqttStrip() {
    return Container(
      margin: const EdgeInsets.fromLTRB(16, 10, 16, 0),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: CeresColors.paper,
        border: Border.all(
          color: CeresColors.leafSoft.withValues(alpha: 0.5),
          width: 0.8,
        ),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Row(
        children: [
          Container(
            width: 6,
            height: 6,
            decoration: const BoxDecoration(
              color: CeresColors.leafLive,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Text(
            'MQTT · broker local',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 9,
              color: CeresColors.leafLive,
              letterSpacing: 0.4,
            ),
          ),
          const Spacer(),
          Text(
            'ceres/diagnostico',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 9,
              color: CeresColors.ink3,
            ),
          ),
        ],
      ),
    );
  }

  // ── Body ────────────────────────────────────────────────────────────────────
  Widget _body() {
    if (_carregando) {
      return const Center(
        child: CircularProgressIndicator(
          color: CeresColors.leafLive,
          strokeWidth: 1.5,
        ),
      );
    }
    if (_erro != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.wifi_off_rounded,
                  size: 48, color: CeresColors.ink3.withValues(alpha: 0.4)),
              const SizedBox(height: 16),
              Text(
                'Sem conexão',
                style: GoogleFonts.newsreader(
                  fontSize: 20,
                  color: CeresColors.ink2,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                _erro!,
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 10,
                  color: CeresColors.blight,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              _BtnRetentar(onPressed: () => _carregar()),
            ],
          ),
        ),
      );
    }
    if (_eventos.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.sensors_off_rounded,
                size: 48, color: CeresColors.ink3.withValues(alpha: 0.4)),
            const SizedBox(height: 12),
            Text(
              'Nenhum evento recebido',
              style: GoogleFonts.newsreader(
                fontSize: 18,
                color: CeresColors.ink2,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              'aguardando ESP32...',
              style: GoogleFonts.ibmPlexMono(
                fontSize: 10,
                color: CeresColors.ink3,
              ),
            ),
          ],
        ),
      );
    }

    // Agrupa eventos por dia
    final agrupado = _agruparPorDia(_eventos);

    return RefreshIndicator(
      onRefresh: () => _carregar(),
      color: CeresColors.leafLive,
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(child: _iotSummary()),
          const SliverToBoxAdapter(child: SizedBox(height: 10)),
          SliverToBoxAdapter(child: _liveMqttStrip()),
          const SliverToBoxAdapter(child: SizedBox(height: 14)),
          for (final grupo in agrupado) ...[
            SliverToBoxAdapter(child: _daySeparator(grupo.dia)),
            SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, i) => _itemEvento(grupo.eventos[i]),
                childCount: grupo.eventos.length,
              ),
            ),
          ],
          const SliverToBoxAdapter(child: SizedBox(height: 16)),
        ],
      ),
    );
  }

  // ── Day separator ───────────────────────────────────────────────────────────
  Widget _daySeparator(String dia) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
      child: Row(
        children: [
          Text(
            dia,
            style: GoogleFonts.ibmPlexMono(
              fontSize: 9,
              letterSpacing: 0.5,
              color: CeresColors.ink3,
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Container(height: 0.5, color: CeresColors.hairline),
          ),
        ],
      ),
    );
  }

  // ── IoT summary (2-col: total eventos / % doentes) ─────────────────────────
  Widget _iotSummary() {
    final total = _total;
    final doentes = _eventos.where((e) => e.classe != 'saudavel').length;
    final pctDoentes = total > 0
        ? (doentes / _eventos.length * 100).toStringAsFixed(0)
        : '--';

    return Container(
      margin: const EdgeInsets.fromLTRB(16, 10, 16, 0),
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
      decoration: BoxDecoration(
        color: CeresColors.paper2,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: IntrinsicHeight(
        child: Row(
          children: [
            _summaryCol(
              label: 'TOTAL EVENTOS',
              value: '$total',
              unit: 'registros',
              valueColor: CeresColors.ink,
            ),
            Container(
              width: 0.8,
              margin: const EdgeInsets.symmetric(vertical: 2),
              color: CeresColors.hairline,
            ),
            _summaryCol(
              label: '% DOENTES',
              value: pctDoentes,
              unit: 'desta página',
              valueColor: doentes > 0 ? CeresColors.blight : CeresColors.leafLive,
            ),
          ],
        ),
      ),
    );
  }

  Widget _summaryCol({
    required String label,
    required String value,
    required String unit,
    required Color valueColor,
  }) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              label,
              style: GoogleFonts.ibmPlexMono(
                fontSize: 8,
                letterSpacing: 0.16,
                color: CeresColors.ink3,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              value,
              style: GoogleFonts.newsreader(
                fontSize: 24,
                fontWeight: FontWeight.w500,
                color: valueColor,
                height: 1,
              ),
            ),
            const SizedBox(height: 3),
            Text(
              unit,
              style: GoogleFonts.ibmPlexMono(
                fontSize: 8,
                color: CeresColors.ink3,
                letterSpacing: 0.04,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ── Event item — flat grid, status icon anel+dot ────────────────────────────
  Widget _itemEvento(EventoMqtt e) {
    final Color cor = CeresColors.statusColor(e.classe, e.confianca);
    String hora = '';
    try {
      final dt = DateTime.parse(e.timestamp).toLocal();
      hora = DateFormat('HH:mm').format(dt);
    } catch (_) {}

    return Container(
      padding: const EdgeInsets.fromLTRB(16, 7, 16, 7),
      decoration: const BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Color(0xFFEBE7E1), width: 0.8),
        ),
      ),
      child: Row(
        children: [
          // Status icon: anel externo semitransparente + dot central
          Container(
            width: 24,
            height: 24,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(
                  color: cor.withValues(alpha: 0.25), width: 1),
            ),
            child: Center(
              child: Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: cor,
                ),
              ),
            ),
          ),
          const SizedBox(width: 10),
          // Conteúdo central
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  e.rotulo,
                  style: GoogleFonts.newsreader(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: CeresColors.ink,
                    letterSpacing: -0.005,
                    height: 1.15,
                  ),
                ),
                const SizedBox(height: 3),
                Row(
                  children: [
                    Text(
                      e.deviceId,
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 9,
                        color: CeresColors.ink2,
                        letterSpacing: 0.04,
                      ),
                    ),
                    Container(
                      width: 2,
                      height: 2,
                      margin: const EdgeInsets.symmetric(horizontal: 5),
                      decoration: const BoxDecoration(
                        shape: BoxShape.circle,
                        color: CeresColors.ink3,
                      ),
                    ),
                    Text(
                      '${e.latenciaMs} ms',
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 9,
                        color: CeresColors.ink3,
                        letterSpacing: 0.04,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          // Direita: %  + hora
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                '${(e.confianca * 100).toStringAsFixed(0)}%',
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 13,
                  fontWeight: FontWeight.w500,
                  color: cor,
                  letterSpacing: 0.02,
                  height: 1,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                hora,
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 9,
                  color: CeresColors.ink3,
                  letterSpacing: 0.04,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // ── Paginação rodapé ────────────────────────────────────────────────────────
  Widget _rodapePaginacao() {
    return Container(
      color: CeresColors.paper,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _BtnPagina(
            icon: Icons.chevron_left,
            label: 'Anterior',
            enabled: _paginaAtual > 1 && !_carregando,
            onPressed: () => _carregar(pagina: _paginaAtual - 1),
          ),
          Text(
            'p. $_paginaAtual',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 10,
              color: CeresColors.ink3,
            ),
          ),
          _BtnPagina(
            icon: Icons.chevron_right,
            label: 'Próxima',
            enabled: _temProxima && !_carregando,
            onPressed: () => _carregar(pagina: _paginaAtual + 1),
          ),
        ],
      ),
    );
  }

  // ── Helpers ─────────────────────────────────────────────────────────────────
  String _formatTimestampShort(String ts) {
    try {
      final dt = DateTime.parse(ts).toLocal();
      return DateFormat('dd/MM HH:mm').format(dt);
    } catch (_) {
      return ts;
    }
  }

  List<_GrupoDia> _agruparPorDia(List<EventoMqtt> eventos) {
    final map = <String, List<EventoMqtt>>{};
    for (final e in eventos) {
      String dia = e.timestamp;
      try {
        final dt = DateTime.parse(e.timestamp).toLocal();
        dia = DateFormat('dd/MM/yyyy').format(dt);
      } catch (_) {}
      map.putIfAbsent(dia, () => []).add(e);
    }
    return map.entries.map((e) => _GrupoDia(e.key, e.value)).toList();
  }
}

class _GrupoDia {
  final String dia;
  final List<EventoMqtt> eventos;
  const _GrupoDia(this.dia, this.eventos);
}

// ── Shared small widgets ─────────────────────────────────────────────────────
class _BtnPagina extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool enabled;
  final VoidCallback onPressed;

  const _BtnPagina({
    required this.icon,
    required this.label,
    required this.enabled,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: enabled ? onPressed : null,
      child: Opacity(
        opacity: enabled ? 1.0 : 0.35,
        child: Row(
          children: [
            if (icon == Icons.chevron_left) ...[
              Icon(icon, size: 16, color: CeresColors.leafDark),
              Text(
                label,
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 10,
                  color: CeresColors.leafDark,
                ),
              ),
            ] else ...[
              Text(
                label,
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 10,
                  color: CeresColors.leafDark,
                ),
              ),
              Icon(icon, size: 16, color: CeresColors.leafDark),
            ],
          ],
        ),
      ),
    );
  }
}

class _BtnRetentar extends StatelessWidget {
  final VoidCallback onPressed;
  const _BtnRetentar({required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          color: CeresColors.leafDark,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(
          'Tentar novamente',
          style: GoogleFonts.ibmPlexSans(
            fontSize: 13,
            color: CeresColors.paper,
          ),
        ),
      ),
    );
  }
}
