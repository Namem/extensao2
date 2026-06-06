/// inference_local_service.dart — Stub para Windows/Web.
///
/// tflite_flutter 0.10.4 tem bug de compilacao no Windows.
/// Esta versao e stub — InferenceLocalService.inferir() lanca erro se chamada.
/// O toggle "Local" ja esta guardado para nao aparecer em Platform.isWindows.
///
/// Para reativar inferencia on-device no Android:
///   1. Descomentar tflite_flutter no pubspec.yaml
///   2. Substituir este arquivo pela implementacao em inference_local_mobile.dart
library;

import 'dart:io';
import '../models/resultado_inferencia.dart';

class InferenceLocalService {
  InferenceLocalService._();
  static final InferenceLocalService instance = InferenceLocalService._();

  /// Inferencia local — apenas Android/iOS.
  /// No Windows/Web, o toggle nao e exibido (Platform.isWindows guard).
  Future<ResultadoInferencia> inferir(File imagem) async {
    throw UnsupportedError(
      'Inferencia local nao disponivel nesta plataforma. '
      'Use o modo Cloud ou rode no Android.',
    );
  }
}
