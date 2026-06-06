import 'dart:io';
import 'dart:math' as math;
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';
import '../models/resultado_inferencia.dart';

class InferenceLocalService {
  static const _modelAsset = 'assets/models/ceres_mobilenetv2_int8.tflite';
  static const _inputSize = 96;

  // Ordem IDÊNTICA ao Django inference_service.py (diretórios ordenados alfabeticamente)
  static const _classes = [
    'D01_requeima',
    'D02_septoriose',
    'D03_pinta_preta',
    'D03b_mancha_alvo',
    'D05_mofo_foliar',
    'D06_vira_cabeca',
    'D06b_mosaico',
    'D07_acaro_bronzeamento',
    'D09_mancha_bacteriana',
    'saudavel',
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

    // Output INT8 quantizado
    final outTensor = _interpreter!.getOutputTensor(0);
    final scale     = outTensor.params.scale;
    final zeroPoint = outTensor.params.zeroPoint;

    final outputRaw = [List.filled(_classes.length, 0)];
    _interpreter!.run(input, outputRaw);

    // Dequantização: float = (int8 - zero_point) * scale
    final logits = outputRaw[0]
        .map((v) => ((v - zeroPoint) * scale).toDouble())
        .toList();

    // Softmax (idêntico ao Django)
    final maxLogit = logits.reduce(math.max);
    final exps = logits.map((v) => math.exp(v - maxLogit)).toList();
    final sumExp = exps.reduce((a, b) => a + b);
    final probs = exps.map((e) => e / sumExp).toList();

    int maxIdx = 0;
    for (int i = 1; i < probs.length; i++) {
      if (probs[i] > probs[maxIdx]) maxIdx = i;
    }

    sw.stop();

    final scoreMap = <String, double>{
      for (int i = 0; i < _classes.length; i++) _classes[i]: probs[i],
    };

    return ResultadoInferencia(
      classe: _classes[maxIdx],
      confianca: probs[maxIdx],
      latenciaMs: sw.elapsedMilliseconds,
      scores: scoreMap,
    );
  }
}
