import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../config.dart';
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
        backgroundColor: Colors.green[700],
        foregroundColor: Colors.white,
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
          color: Colors.grey[200],
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey[400]!),
        ),
        child: const Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.camera_alt, size: 64, color: Colors.grey),
            SizedBox(height: 8),
            Text('Tire ou selecione uma foto da folha',
                style: TextStyle(color: Colors.grey)),
          ],
        ),
      );
    }
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.file(_imagem!, height: 260, fit: BoxFit.cover),
    );
  }

  Widget _botoesFonte() {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton.icon(
            icon: const Icon(Icons.camera_alt),
            label: const Text('Câmera'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green[700],
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
            onPressed: _carregando ? null : () => _capturar(ImageSource.camera),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: OutlinedButton.icon(
            icon: const Icon(Icons.photo_library),
            label: const Text('Galeria'),
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.green[700],
              side: BorderSide(color: Colors.green[700]!),
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
            onPressed: _carregando ? null : () => _capturar(ImageSource.gallery),
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
    return sorted.map((e) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 2),
        child: Row(
          children: [
            SizedBox(
              width: 130,
              child: Text(e.key, style: const TextStyle(fontSize: 12)),
            ),
            Expanded(
              child: LinearProgressIndicator(
                value: e.value.clamp(0.0, 1.0),
                backgroundColor: Colors.grey[200],
                color: Colors.green[600],
                minHeight: 8,
              ),
            ),
            const SizedBox(width: 6),
            Text('${(e.value * 100).toStringAsFixed(0)}%',
                style: const TextStyle(fontSize: 12)),
          ],
        ),
      );
    }).toList();
  }
}
