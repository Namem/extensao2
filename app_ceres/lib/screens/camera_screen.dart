import 'dart:convert';
import 'dart:io';

import 'package:drift/drift.dart' show Value;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../config.dart';
import '../database/database.dart';
import '../models/resultado_inferencia.dart';
import '../services/api_service.dart';

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

  final _picker = ImagePicker();

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
    await _inferir();
  }

  Future<void> _inferir() async {
    if (_imagem == null) return;
    setState(() {
      _carregando = true;
      _erro = null;
    });
    try {
      final res = await ApiService.instance.inferir(_imagem!);
      setState(() => _resultado = res);
      // Salvar automaticamente no banco local (offline)
      await appDb.salvar(DiagnosticosLocaisCompanion(
        timestamp: Value(DateTime.now()),
        classe: Value(res.classe),
        confianca: Value(res.confianca),
        latenciaMs: Value(res.latenciaMs),
        scoresJson: Value(jsonEncode(res.scores)),
        imagemPath: Value(_imagem!.path),
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnóstico — Câmera'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _painelImagem(),
            const SizedBox(height: 12),
            _botoesFonte(),
            const SizedBox(height: 16),
            if (_carregando) const Center(child: CircularProgressIndicator()),
            if (_erro != null) _painelErro(),
            if (_resultado != null) _painelResultado(),
            if (_salvo)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.check_circle, size: 14, color: Colors.green[700]),
                    const SizedBox(width: 4),
                    Text('Salvo localmente',
                        style: TextStyle(
                            fontSize: 12, color: Colors.green[700])),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _painelImagem() {
    if (_imagem == null) {
      return Container(
        height: 260,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: const Color(0xFFDDDAD5), width: 1.5),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: const BoxDecoration(
                color: Color(0xFFE8F5E9),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.eco_outlined,
                  size: 44, color: Color(0xFF2E7D32)),
            ),
            const SizedBox(height: 14),
            const Text('Tire ou selecione uma foto da folha',
                style: TextStyle(
                    color: Color(0xFF888880),
                    fontSize: 14,
                    fontWeight: FontWeight.w500)),
            const SizedBox(height: 4),
            const Text('JPG ou PNG · máx 640×640 px',
                style: TextStyle(color: Color(0xFFAAAAAA), fontSize: 12)),
          ],
        ),
      );
    }
    return ClipRRect(
      borderRadius: BorderRadius.circular(14),
      child: Image.file(_imagem!, height: 260, fit: BoxFit.cover),
    );
  }

  Widget _botoesFonte() {
    // camera não é suportada no Windows desktop via image_picker
    final temCamera = !kIsWeb && !Platform.isWindows;
    return Row(
      children: [
        Expanded(
          child: ElevatedButton.icon(
            icon: const Icon(Icons.camera_alt),
            label: const Text('Câmera'),
            onPressed: (temCamera && !_carregando)
                ? () => _capturar(ImageSource.camera)
                : null,
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: OutlinedButton.icon(
            icon: const Icon(Icons.photo_library),
            label: const Text('Galeria'),
            onPressed:
                _carregando ? null : () => _capturar(ImageSource.gallery),
          ),
        ),
      ],
    );
  }

  Widget _painelErro() {
    return Container(
      padding: const EdgeInsets.all(12),
      margin: const EdgeInsets.only(top: 8),
      decoration: BoxDecoration(
        color: Colors.red[50],
        border: Border.all(color: Colors.red[300]!),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text('Erro: $_erro',
          style: TextStyle(color: Colors.red[800])),
    );
  }

  Widget _painelResultado() {
    final r = _resultado!;
    final baixaConfianca = r.confianca < Config.confiancaMinima;
    final cor = r.isSaudavel
        ? Colors.green
        : (baixaConfianca ? Colors.orange : Colors.red);

    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  r.isSaudavel ? Icons.check_circle : Icons.warning_amber,
                  color: cor,
                  size: 32,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    r.rotulo,
                    style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: cor),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _linhaInfo('Confiança', '${(r.confianca * 100).toStringAsFixed(1)}%'),
            _linhaInfo('Latência API', '${r.latenciaMs} ms'),
            if (baixaConfianca)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  'Confiança baixa — tente uma foto com melhor iluminação.',
                  style: TextStyle(color: Colors.orange[800], fontSize: 13),
                ),
              ),
            const Divider(height: 24),
            const Text('Scores por classe:',
                style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            ..._barrasScores(r.scores),
          ],
        ),
      ),
    );
  }

  Widget _linhaInfo(String label, String valor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Text('$label: ', style: const TextStyle(fontWeight: FontWeight.w500)),
          Text(valor),
        ],
      ),
    );
  }

  List<Widget> _barrasScores(Map<String, double> scores) {
    final sorted = scores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    final topClasse = sorted.isNotEmpty ? sorted.first.key : '';
    return sorted.map((e) {
      final isTop = e.key == topClasse;
      final barColor = isTop
          ? (topClasse == 'saudavel'
              ? const Color(0xFF2E7D32)
              : const Color(0xFFC62828))
          : const Color(0xFFBDBDBD);
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 3),
        child: Row(
          children: [
            SizedBox(
              width: 140,
              child: Text(
                ResultadoInferencia.rotuloDeClasse(e.key),
                style: TextStyle(
                  fontSize: 12,
                  fontWeight:
                      isTop ? FontWeight.w600 : FontWeight.normal,
                  color: isTop
                      ? const Color(0xFF1A1A1A)
                      : const Color(0xFF888880),
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Expanded(
              child: LinearProgressIndicator(
                value: e.value.clamp(0.0, 1.0),
                backgroundColor: const Color(0xFFF0EDE9),
                color: barColor,
                minHeight: 7,
                borderRadius: BorderRadius.circular(4),
              ),
            ),
            const SizedBox(width: 6),
            SizedBox(
              width: 36,
              child: Text(
                '${(e.value * 100).toStringAsFixed(0)}%',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight:
                      isTop ? FontWeight.w600 : FontWeight.normal,
                ),
                textAlign: TextAlign.right,
              ),
            ),
          ],
        ),
      );
    }).toList();
  }
}
