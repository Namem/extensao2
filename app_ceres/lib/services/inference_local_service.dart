import 'dart:io';
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';
import '../models/resultado_inferencia.dart';

class InferenceLocalService {
  static const _modelAsset = 'assets/models/ceres_mobilenetv2_int8.tflite';
  static const _inputSize = 96;

  // Ordem alfabética das pastas PlantVillage — define índice de cada classe
  static const _classes = [
    'D09_mancha_bacteriana', // Bacterial_spot
    'D03_pinta_preta',       // Early_blight
    'D01_requeima',          // Late_blight
    'D05_mofo_foliar',       // Leaf_Mold
    'D02_septoriose',        // Septoria_leaf_spot
    'D07_acaro_bronzeamento',// Spider_mites
    'D03b_mancha_alvo',      // Target_Spot
    'D06_vira_cabeca',       // Yellow_Leaf_Curl_Virus
    'D06b_mosaico',          // mosaic_virus
    'saudavel',              // healthy
  ];

  Interpreter? _interpreter;

  InferenceLocalService._();
  static final InferenceLocalService instance = InferenceLocalService._();

  Future<void> _init() async {
    if (_interpreter != null) return;
    _interpreter = await Interpreter.fromAsset(_modelAsset);
  }

  Future<ResultadoInferencia> inferir(File imagem) async {
    if (Platform.isWindows) {
      throw UnsupportedError('TFLite não disponível no Windows. Use modo Cloud.');
    }

    final sw = Stopwatch()..start();
    await _init();

    final bytes = await imagem.readAsBytes();
    final original = img.decodeImage(bytes)!;
    final resized = img.copyResize(original, width: _inputSize, height: _inputSize);

    // Input INT8: uint8 - 128 → [-128, 127]
    final input = List.generate(1, (_) =>
      List.generate(_inputSize, (y) =>
        List.generate(_inputSize, (x) =>
          List.generate(3, (c) {
            final pixel = resized.getPixel(x, y);
            final ch = c == 0 ? pixel.r : (c == 1 ? pixel.g : pixel.b);
            return (ch.toInt() - 128).clamp(-128, 127);
          }))));

    // Output: [1, 10] float32
    final output = [List.filled(_classes.length, 0.0)];
    _interpreter!.run(input, output);

    final scores = output[0];
    int maxIdx = 0;
    for (int i = 1; i < scores.length; i++) {
      if (scores[i] > scores[maxIdx]) maxIdx = i;
    }

    sw.stop();

    final scoreMap = <String, double>{
      for (int i = 0; i < _classes.length; i++) _classes[i]: scores[i],
    };

    return ResultadoInferencia(
      classe: _classes[maxIdx],
      confianca: scores[maxIdx],
      latenciaMs: sw.elapsedMilliseconds,
      scores: scoreMap,
    );
  }
}
