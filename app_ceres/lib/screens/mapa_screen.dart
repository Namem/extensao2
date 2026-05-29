import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:latlong2/latlong.dart';

import '../data/doencas_data.dart';
import '../models/evento_mqtt.dart';
import '../services/api_service.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_app_bar.dart';
import '../widgets/offline_banner.dart';

class MapaScreen extends StatefulWidget {
  const MapaScreen({super.key});

  @override
  State<MapaScreen> createState() => _MapaScreenState();
}

class _MapaScreenState extends State<MapaScreen> {
  // Centro padrão: Sorriso-MT (público-alvo do projeto)
  static const _sorriso = LatLng(-12.5428, -55.7214);

  final _mapController = MapController();
  List<EventoMqtt> _eventos = [];
  LatLng? _posicaoAtual;
  bool _carregando = true;
  String? _erro;

  @override
  void initState() {
    super.initState();
    _inicializar();
  }

  Future<void> _inicializar() async {
    await Future.wait([_carregarEventos(), _obterPosicao()]);
  }

  Future<void> _carregarEventos() async {
    try {
      final data = await ApiService.instance.historico(page: 1);
      if (mounted) {
        setState(() {
          _eventos = (data['results'] as List<EventoMqtt>)
              .where((e) => e.latitude != null && e.longitude != null)
              .toList();
          _carregando = false;
        });
      }
    } catch (e) {
      if (mounted) setState(() { _carregando = false; _erro = '$e'; });
    }
  }

  Future<void> _obterPosicao() async {
    // GPS não suportado no Windows/Web (apenas dev)
    if (kIsWeb || defaultTargetPlatform == TargetPlatform.windows) return;
    try {
      var permissao = await Geolocator.checkPermission();
      if (permissao == LocationPermission.denied) {
        permissao = await Geolocator.requestPermission();
      }
      if (permissao == LocationPermission.deniedForever) return;
      final pos = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.medium,
          timeLimit: Duration(seconds: 10),
        ),
      );
      if (mounted) setState(() => _posicaoAtual = LatLng(pos.latitude, pos.longitude));
    } catch (_) {
      // GPS indisponível — usar fallback Sorriso-MT
    }
  }

  // ── Cor do marcador por urgência ─────────────────────────────────────────
  Color _corMarcador(String? classe) {
    if (classe == null) return CeresColors.ink3;
    final info = kDoencas[classe];
    if (info == null) return CeresColors.ink3;
    switch (info.urgencia) {
      case 'URGENTE':   return CeresColors.blight;
      case 'MODERADO':  return CeresColors.dryGrass;
      default:          return CeresColors.leafLive;
    }
  }

  @override
  Widget build(BuildContext context) {
    final centro = _posicaoAtual ?? _sorriso;

    return Scaffold(
      backgroundColor: CeresColors.bone,
      appBar: CeresAppBar(
        pageTitleItalic: 'Mapa',
        pageTitle: 'de Ocorrências',
        pageCount: _eventos.isEmpty ? null : '${_eventos.length} eventos',
      ),
      body: OfflineBanner(
        child: Stack(
          children: [
            // ── Mapa ────────────────────────────────────────────────────────
            FlutterMap(
              mapController: _mapController,
              options: MapOptions(
                initialCenter: centro,
                initialZoom: 11,
              ),
              children: [
                // Tiles OpenStreetMap
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'br.edu.ifmt.ceres',
                ),
                // Marcadores de diagnósticos
                MarkerLayer(markers: _marcadores()),
                // Posição atual (apenas mobile)
                if (_posicaoAtual != null)
                  MarkerLayer(markers: [_marcadorUsuario()]),
              ],
            ),

            // ── Overlay de status (carregando / erro) ────────────────────
            if (_carregando || _erro != null)
              Positioned(
                top: 12,
                left: 0,
                right: 0,
                child: Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                    decoration: BoxDecoration(
                      color: CeresColors.paper,
                      borderRadius: BorderRadius.circular(4),
                      border: Border.all(color: CeresColors.hairline),
                    ),
                    child: Text(
                      _carregando ? 'Carregando eventos...' : 'Sem conexão — exibindo cache',
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 10,
                        color: _erro != null ? CeresColors.dryGrass : CeresColors.ink3,
                      ),
                    ),
                  ),
                ),
              ),

            // ── Legenda ──────────────────────────────────────────────────
            Positioned(
              bottom: 16,
              right: 12,
              child: _legenda(),
            ),
          ],
        ),
      ),
    );
  }

  List<Marker> _marcadores() {
    return _eventos.map((e) {
      final cor = _corMarcador(e.classeDetectada);
      return Marker(
        point: LatLng(e.latitude!, e.longitude!),
        width: 28,
        height: 28,
        child: GestureDetector(
          onTap: () => _mostrarBottomSheet(e),
          child: Container(
            decoration: BoxDecoration(
              color: cor.withValues(alpha: 0.15),
              shape: BoxShape.circle,
              border: Border.all(color: cor, width: 1.5),
            ),
            child: Center(
              child: Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(color: cor, shape: BoxShape.circle),
              ),
            ),
          ),
        ),
      );
    }).toList();
  }

  Marker _marcadorUsuario() {
    return Marker(
      point: _posicaoAtual!,
      width: 20,
      height: 20,
      child: Container(
        decoration: BoxDecoration(
          color: CeresColors.leafDeep.withValues(alpha: 0.2),
          shape: BoxShape.circle,
          border: Border.all(color: CeresColors.leafDeep, width: 2),
        ),
        child: const Center(
          child: Icon(Icons.my_location, size: 10, color: CeresColors.leafDeep),
        ),
      ),
    );
  }

  Widget _legenda() {
    return Container(
      padding: const EdgeInsets.fromLTRB(10, 8, 10, 8),
      decoration: BoxDecoration(
        color: CeresColors.paper,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: CeresColors.hairline, width: 0.8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          _legendaItem('URGENTE',  CeresColors.blight),
          const SizedBox(height: 4),
          _legendaItem('MODERADO', CeresColors.dryGrass),
          const SizedBox(height: 4),
          _legendaItem('SAUDÁVEL', CeresColors.leafLive),
        ],
      ),
    );
  }

  Widget _legendaItem(String label, Color cor) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 8, height: 8,
          decoration: BoxDecoration(color: cor, shape: BoxShape.circle),
        ),
        const SizedBox(width: 6),
        Text(
          label,
          style: GoogleFonts.ibmPlexMono(
            fontSize: 8,
            letterSpacing: 0.1,
            color: CeresColors.ink2,
          ),
        ),
      ],
    );
  }

  void _mostrarBottomSheet(EventoMqtt e) {
    final info = e.classeDetectada != null ? kDoencas[e.classeDetectada] : null;
    final cor = _corMarcador(e.classeDetectada);
    final fmt = DateFormat('dd/MM/yyyy HH:mm');

    showModalBottomSheet(
      context: context,
      backgroundColor: CeresColors.paper,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(8)),
      ),
      builder: (_) => Padding(
        padding: const EdgeInsets.fromLTRB(20, 16, 20, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Handle
            Center(
              child: Container(
                width: 36, height: 3,
                decoration: BoxDecoration(
                  color: CeresColors.hairline,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            const SizedBox(height: 14),
            // Faixa colorida + nome
            Row(
              children: [
                Container(width: 3, height: 36, color: cor),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        info?.nomePopular ?? e.classeDetectada ?? 'Desconhecido',
                        style: GoogleFonts.newsreader(
                          fontSize: 17,
                          fontWeight: FontWeight.w500,
                          color: CeresColors.ink,
                        ),
                      ),
                      if (info != null)
                        Text(
                          info.nomeLatim,
                          style: GoogleFonts.newsreader(
                            fontSize: 11,
                            fontStyle: FontStyle.italic,
                            color: CeresColors.ink3,
                          ),
                        ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            // Metadados
            _metaRow('DISPOSITIVO', e.deviceId),
            const SizedBox(height: 6),
            _metaRow('DATA', fmt.format(e.timestamp.toLocal())),
            if (e.confianca != null) ...[
              const SizedBox(height: 6),
              _metaRow('CONFIANÇA', '${(e.confianca! * 100).toStringAsFixed(1)}%'),
            ],
            if (e.latitude != null) ...[
              const SizedBox(height: 6),
              _metaRow('GPS', '${e.latitude!.toStringAsFixed(4)}, ${e.longitude!.toStringAsFixed(4)}'),
            ],
          ],
        ),
      ),
    );
  }

  Widget _metaRow(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 82,
          child: Text(
            label,
            style: GoogleFonts.ibmPlexMono(
              fontSize: 8,
              letterSpacing: 0.18,
              color: CeresColors.ink3,
            ),
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: GoogleFonts.ibmPlexSans(
              fontSize: 12,
              color: CeresColors.ink2,
            ),
          ),
        ),
      ],
    );
  }
}
