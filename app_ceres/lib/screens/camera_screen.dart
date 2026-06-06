import 'dart:convert';
import 'dart:io';

import 'package:drift/drift.dart' show Value;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:image_picker/image_picker.dart';

import '../config.dart' as app_config;
import '../data/doencas_data.dart';
import '../database/database.dart';
import '../models/resultado_inferencia.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import '../services/api_service.dart';
import '../services/inference_local_service.dart';
import '../services/modo_inferencia.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';
import '../widgets/offline_banner.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  File? _imagem;
  ResultadoInferencia? _resultado;
  bool _carregando = false;
  String? _erro;
  bool _salvo = false;
  bool _offline = false;

  // Modo de inferência: estado global compartilhado com PerfilScreen
  final _modo = ModoInferencia.instance;
  bool get _modoLocal => _modo.isLocal;
  bool get _localDisponivel => !Platform.isWindows;

  double? _latitude;
  double? _longitude;

  final _picker = ImagePicker();

  @override
  void initState() {
    super.initState();
    _modo.addListener(_onModoChanged);
    Connectivity().checkConnectivity().then(_atualizarConectividade);
    Connectivity().onConnectivityChanged.listen(_atualizarConectividade);
  }

  @override
  void dispose() {
    _modo.removeListener(_onModoChanged);
    super.dispose();
  }

  void _onModoChanged() {
    if (mounted) setState(() {});
  }

  void _atualizarConectividade(List<ConnectivityResult> results) {
    final semConexao = results.isEmpty ||
        (results.length == 1 && results.first == ConnectivityResult.none);
    if (mounted && semConexao != _offline) {
      setState(() {
        _offline = semConexao;
        if (semConexao && _localDisponivel) _modo.setLocal(true);
      });
    }
  }

  void _avisoOffline() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'Sem conexão com o servidor.',
          style: GoogleFonts.ibmPlexSans(fontSize: 13, color: CeresColors.paper),
        ),
        backgroundColor: CeresColors.dryGrass,
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  /// Captura localização GPS antes de inferir (silencioso — não bloqueia).
  Future<void> _capturarGps() async {
    try {
      // Verifica permissão
      var perm = await Geolocator.checkPermission();
      if (perm == LocationPermission.denied) {
        perm = await Geolocator.requestPermission();
      }
      if (perm == LocationPermission.denied ||
          perm == LocationPermission.deniedForever) {
        return; // sem permissão — segue sem GPS
      }
      final pos = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
          timeLimit: Duration(seconds: 10),
        ),
      );
      _latitude = pos.latitude;
      _longitude = pos.longitude;
    } catch (_) {
      // GPS indisponível — segue sem coordenadas
    }
  }

  Future<void> _capturar(ImageSource fonte) async {
    final picked = await _picker.pickImage(
      source: fonte,
      maxWidth: 640,
      maxHeight: 640,
      imageQuality: 90,
    );
    if (picked == null) return;
    setState(() {
      _imagem = File(picked.path);
      _resultado = null;
      _erro = null;
      _salvo = false;
    });
    // GPS primeiro — garante lat/lon prontos antes do POST
    await _capturarGps();
    await _inferir();
  }

  Future<void> _inferir() async {
    if (_imagem == null) return;
    setState(() { _carregando = true; _erro = null; });
    try {
      // Rota: local (TFLite on-device) ou cloud (Django API)
      final res = (_modoLocal && _localDisponivel)
          ? await InferenceLocalService.instance.inferir(_imagem!)
          : await ApiService.instance.inferir(
              _imagem!,
              latitude: _latitude,
              longitude: _longitude,
            );
      setState(() => _resultado = res);
      await appDb.salvar(DiagnosticosLocaisCompanion(
        timestamp: Value(DateTime.now()),
        classe: Value(res.classe),
        confianca: Value(res.confianca),
        latenciaMs: Value(res.latenciaMs),
        scoresJson: Value(jsonEncode(res.scores)),
        imagemPath: Value(_imagem!.path),
        latitude: Value(_latitude),
        longitude: Value(_longitude),
      ));
      setState(() => _salvo = true);
    } catch (e) {
      setState(() => _erro = e.toString());
    } finally {
      setState(() => _carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final temCamera = !kIsWeb && !Platform.isWindows;
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: SafeArea(
        bottom: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CeresBrandBar(
              subtitle: 'Diagnóstico foliar',
              actions: [
                CeresIconBtn(Icons.save_alt_outlined,
                    onTap: () => Navigator.pushNamed(context, '/salvos')),
                CeresIconBtn(Icons.sync, onTap: _resultado == null ? null : _inferir),
              ],
            ),
            Expanded(child: OfflineBanner(child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _viewfinder(),
                  const SizedBox(height: 10),
                  if (_carregando) _loadingBar(),
                  if (_erro != null) _erroCard(),
                  if (_resultado != null) ...[
                    _resultCard(),
                    const SizedBox(height: 6),
                    _sobreDoenca(),
                    const SizedBox(height: 6),
                    _scores(),
                  ],
                  const SizedBox(height: 10),
                  if (_localDisponivel) _toggleModo(),
                  _botoes(temCamera),
                  if (_salvo) _salvoIndicator(),
                  const SizedBox(height: 24),
                ],
              ),
            ))),
          ],
        ),
      ),
    );
  }

  // ── Viewfinder ─────────────────────────────────────────────────────────────
  Widget _viewfinder() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 22),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(10),
        child: Stack(
          children: [
            // Background (imagem ou gradiente verde-escuro)
            if (_imagem != null)
              Image.file(_imagem!,
                  height: 180, width: double.infinity, fit: BoxFit.cover)
            else
              Container(
                height: 180,
                decoration: const BoxDecoration(
                  gradient: RadialGradient(
                    center: Alignment(0, 0.2),
                    radius: 0.85,
                    colors: [
                      Color(0xFF3E6B40),
                      Color(0xFF2A4F2C),
                      Color(0xFF1A3320),
                    ],
                  ),
                ),
                child: const Center(
                  child: Icon(Icons.eco_outlined,
                      size: 48, color: Color(0x55A9BCA0)),
                ),
              ),
            // Brackets nos cantos
            ..._brackets(),
            // Reticle (mira circular)
            if (_imagem == null)
              Center(
                child: Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(
                        color: CeresColors.paper.withValues(alpha: 0.5),
                        width: 1),
                  ),
                ),
              ),
            // Badge superior
            Positioned(
              top: 10,
              left: 0,
              right: 0,
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: Colors.black.withValues(alpha: 0.55),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    _imagem == null ? 'AGUARDANDO AMOSTRA' : 'ANALISANDO',
                    style: GoogleFonts.ibmPlexMono(
                      fontSize: 9,
                      letterSpacing: 0.12,
                      color: CeresColors.paper.withValues(alpha: 0.85),
                    ),
                  ),
                ),
              ),
            ),
            // Meta inferior
            Positioned(
              bottom: 10,
              left: 12,
              child: Row(
                children: [
                  Container(
                    width: 6, height: 6,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: CeresColors.blight,
                      boxShadow: [
                        BoxShadow(
                            color: CeresColors.blight.withValues(alpha: 0.3),
                            blurRadius: 4,
                            spreadRadius: 2)
                      ],
                    ),
                  ),
                  const SizedBox(width: 5),
                  Text(
                    'CERES · EXP-E · INT8',
                    style: GoogleFonts.ibmPlexMono(
                      fontSize: 9,
                      letterSpacing: 0.08,
                      color: CeresColors.paper.withValues(alpha: 0.85),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<Widget> _brackets() {
    const s = 20.0;
    const t = 1.5;
    const pad = 10.0;
    const c = Color(0xCCFAF4EB);
    return [
      Positioned(top: pad, left: pad,
          child: _bracket(s, t, c, top: true, left: true)),
      Positioned(top: pad, right: pad,
          child: _bracket(s, t, c, top: true, left: false)),
      Positioned(bottom: pad, left: pad,
          child: _bracket(s, t, c, top: false, left: true)),
      Positioned(bottom: pad, right: pad,
          child: _bracket(s, t, c, top: false, left: false)),
    ];
  }

  Widget _bracket(double s, double t, Color c,
      {required bool top, required bool left}) {
    return SizedBox(
      width: s, height: s,
      child: CustomPaint(
        painter: _BracketPainter(t, c, top: top, left: left),
      ),
    );
  }

  // ── Toggle Cloud / Local ────────────────────────────────────────────────────
  Widget _toggleModo() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 0, 22, 6),
      child: Row(
        children: [
          Text(
            'MODO:',
            style: GoogleFonts.ibmPlexMono(
              fontSize: 8,
              letterSpacing: 0.5,
              color: CeresColors.ink3,
            ),
          ),
          const SizedBox(width: 8),
          _modoChip(
            label: 'Cloud',
            sublabel: 'Django API',
            ativo: !_modoLocal,
            cor: CeresColors.leafDark,
            onTap: () => _modo.setLocal(false),
          ),
          const SizedBox(width: 6),
          _modoChip(
            label: 'Local',
            sublabel: 'TFLite on-device',
            ativo: _modoLocal,
            cor: CeresColors.dryGrass,
            onTap: () => _modo.setLocal(true),
          ),
        ],
      ),
    );
  }

  Widget _modoChip({
    required String label,
    required String sublabel,
    required bool ativo,
    required Color cor,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        decoration: BoxDecoration(
          color: ativo ? cor.withValues(alpha: 0.12) : CeresColors.paper2,
          borderRadius: BorderRadius.circular(4),
          border: Border.all(
            color: ativo ? cor : CeresColors.hairline,
            width: ativo ? 1.5 : 0.8,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              label,
              style: GoogleFonts.ibmPlexSans(
                fontSize: 11,
                fontWeight: ativo ? FontWeight.w600 : FontWeight.w400,
                color: ativo ? cor : CeresColors.ink3,
              ),
            ),
            Text(
              sublabel,
              style: GoogleFonts.ibmPlexMono(
                fontSize: 8,
                color: ativo ? cor.withValues(alpha: 0.7) : CeresColors.ink3,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ── Loading ────────────────────────────────────────────────────────────────
  Widget _loadingBar() {
    return const Padding(
      padding: EdgeInsets.symmetric(horizontal: 22, vertical: 4),
      child: LinearProgressIndicator(
        backgroundColor: CeresColors.bone,
        color: CeresColors.leafLive,
        minHeight: 2,
      ),
    );
  }

  // ── Erro ───────────────────────────────────────────────────────────────────
  Widget _erroCard() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 8, 22, 0),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: CeresColors.blightSoft,
          border: Border.all(color: CeresColors.blight.withValues(alpha: 0.4)),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Text('Erro: $_erro',
            style: GoogleFonts.ibmPlexMono(
                fontSize: 12, color: CeresColors.blight)),
      ),
    );
  }

  // ── Result card ────────────────────────────────────────────────────────────
  Widget _resultCard() {
    final r = _resultado!;
    final baixaConfianca = r.confianca < app_config.Config.confiancaMinima;
    final cor = CeresColors.statusColor(r.classe, r.confianca);
    final classeNum = r.classe.split('_').first.replaceAll(RegExp(r'[^0-9]'), '');

    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 10, 22, 0),
      child: CeresPaperCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(
                  classeNum.isNotEmpty
                      ? 'DX#${r.scores.length.toString().padLeft(4, "0")} · CLASSE $classeNum'
                      : 'DX · ${r.classe.toUpperCase()}',
                  style: CeresType.label,
                ),
                const SizedBox(height: 4),
                Text(r.rotulo, style: CeresType.diseaseName),
                Text(infoDoenca(r.classe).nomeLatim, style: CeresType.latin),
              ]),
              const Spacer(),
              Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
                Text('CONFIANÇA', style: CeresType.label),
                const SizedBox(height: 4),
                Text(
                  '${(r.confianca * 100).toStringAsFixed(1)}%',
                  style: CeresType.mono(TextStyle(
                      fontSize: 13, fontWeight: FontWeight.w500, color: cor,
                      letterSpacing: 0.5)),
                ),
              ]),
            ]),
            const SizedBox(height: 14),
            Row(children: [
              Text('CONFIANÇA DO MODELO', style: CeresType.label),
              const Spacer(),
              Text('${(r.confianca * 100).toStringAsFixed(1)}%',
                  style: CeresType.mono(const TextStyle(
                      fontSize: 11, fontWeight: FontWeight.w500, color: CeresColors.ink))),
            ]),
            const SizedBox(height: 6),
            CeresConfidenceBar(value: r.confianca, color: cor),
            if (r.latenciaMs > 0) ...[
              const SizedBox(height: 6),
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                Text('LATÊNCIA', style: CeresType.label),
                Text('${r.latenciaMs} ms',
                    style: CeresType.mono(const TextStyle(
                        fontSize: 9, color: CeresColors.ink3))),
              ]),
            ],
            if (baixaConfianca) ...[
              const SizedBox(height: 8),
              Text('Confiança baixa — tente melhor iluminação.',
                  style: CeresType.mono(const TextStyle(
                      fontSize: 9.5, color: CeresColors.dryGrass))),
            ],
          ],
        ),
      ),
    );
  }

  // ── Sobre a doença ─────────────────────────────────────────────────────────
  Widget _sobreDoenca() {
    final r = _resultado!;
    final info = _infoDoenca(r.classe);
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 8, 22, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            Text('SOBRE ESTA DOENÇA', style: CeresType.label),
            const Spacer(),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
              decoration: BoxDecoration(
                color: CeresColors.boneDeep,
                border: Border.all(color: CeresColors.hairline),
                borderRadius: BorderRadius.circular(3),
              ),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                Container(width: 6, height: 6,
                    decoration: BoxDecoration(shape: BoxShape.circle, color: info.corAgente)),
                const SizedBox(width: 5),
                Text(info.tipoAgente, style: CeresType.sans(const TextStyle(
                    fontSize: 9.5, color: CeresColors.ink))),
              ]),
            ),
          ]),
          const SizedBox(height: 6),
          Text(info.descricao, style: CeresType.serif(const TextStyle(
              fontSize: 11.5, height: 1.35, color: CeresColors.ink2))),
          const SizedBox(height: 8),
          CeresActionBox(body: info.acao, priority: info.urgencia),
        ],
      ),
    );
  }

  // ── Scores ─────────────────────────────────────────────────────────────────
  Widget _scores() {
    final r = _resultado!;
    final sorted = r.scores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    final topClasse = sorted.isNotEmpty ? sorted.first.key : '';

    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 10, 22, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Divider(height: 1),
          const SizedBox(height: 8),
          Row(children: [
            Text('10 CLASSES — SCORES', style: CeresType.label),
            const Spacer(),
            Text('SOFTMAX', style: CeresType.label),
          ]),
          const SizedBox(height: 6),
          ...sorted.asMap().entries.map((entry) {
            final i = entry.key;
            final e = entry.value;
            final isTop = e.key == topClasse;
            final barColor = isTop
                ? (topClasse == 'saudavel' ? CeresColors.leafLive : CeresColors.blight)
                : CeresColors.ink3;
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 2),
              child: Row(children: [
                SizedBox(width: 16, child: Text(
                  (i + 1).toString().padLeft(2, '0'),
                  textAlign: TextAlign.right,
                  style: CeresType.mono(const TextStyle(
                      fontSize: 9, color: CeresColors.ink3)),
                )),
                const SizedBox(width: 8),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(ResultadoInferencia.rotuloDeClasse(e.key),
                      style: CeresType.sans(TextStyle(
                          fontSize: 10.5,
                          fontWeight: isTop ? FontWeight.w500 : FontWeight.w400,
                          color: isTop ? CeresColors.blight : CeresColors.ink2))),
                  const SizedBox(height: 2),
                  ClipRRect(borderRadius: BorderRadius.circular(2), child: Container(
                    height: 3, color: CeresColors.dust2,
                    child: FractionallySizedBox(alignment: Alignment.centerLeft,
                        widthFactor: e.value.clamp(0.0, 1.0),
                        child: Container(color: barColor)),
                  )),
                ])),
                const SizedBox(width: 8),
                SizedBox(width: 36, child: Text(
                  '${(e.value * 100).toStringAsFixed(1).replaceAll('.', ',')}%',
                  textAlign: TextAlign.right,
                  style: CeresType.mono(TextStyle(
                      fontSize: 10,
                      fontWeight: isTop ? FontWeight.w500 : FontWeight.w400,
                      color: isTop ? CeresColors.blight : CeresColors.ink2)),
                )),
              ]),
            );
          }),
        ],
      ),
    );
  }

  // ── Botões ─────────────────────────────────────────────────────────────────
  Widget _botoes(bool temCamera) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 6, 22, 12),
      child: Row(children: [
        Expanded(child: FilledButton.icon(
          onPressed: (temCamera && !_carregando && !(_offline && !_modoLocal))
              ? () => _capturar(ImageSource.camera)
              : null,
          icon: const Icon(Icons.photo_camera_outlined, size: 18),
          label: const Text('Câmera'),
        )),
        const SizedBox(width: 10),
        Expanded(child: OutlinedButton.icon(
          onPressed: (!_carregando && !(_offline && !_modoLocal))
              ? () => _capturar(ImageSource.gallery)
              : null,
          icon: const Icon(Icons.photo_library_outlined, size: 18),
          label: const Text('Galeria'),
        )),
      ]),
    );
  }

  Widget _salvoIndicator() {
    return Padding(
      padding: const EdgeInsets.only(top: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 5, height: 5,
            decoration: const BoxDecoration(
                shape: BoxShape.circle, color: CeresColors.leafLive),
          ),
          const SizedBox(width: 6),
          Text('Salvo localmente',
              style: GoogleFonts.ibmPlexMono(
                  fontSize: 10, color: CeresColors.leafLive, letterSpacing: 0.08)),
        ],
      ),
    );
  }

  // ── Dados estáticos das doenças ───────────────────────────────────────────
  DoencaInfo _infoDoenca(String classe) => infoDoenca(classe);

}

// ── Widgets auxiliares ───────────────────────────────────────────────────────

class _BracketPainter extends CustomPainter {
  final double t;
  final Color c;
  final bool top, left;
  const _BracketPainter(this.t, this.c, {required this.top, required this.left});

  @override
  void paint(Canvas canvas, Size size) {
    final p = Paint()..color = c..strokeWidth = t..style = PaintingStyle.stroke;
    final path = Path();
    if (top && left) {
      path.moveTo(0, size.height);
      path.lineTo(0, 0);
      path.lineTo(size.width, 0);
    } else if (top && !left) {
      path.moveTo(0, 0);
      path.lineTo(size.width, 0);
      path.lineTo(size.width, size.height);
    } else if (!top && left) {
      path.moveTo(0, 0);
      path.lineTo(0, size.height);
      path.lineTo(size.width, size.height);
    } else {
      path.moveTo(0, size.height);
      path.lineTo(size.width, size.height);
      path.lineTo(size.width, 0);
    }
    canvas.drawPath(path, p);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

