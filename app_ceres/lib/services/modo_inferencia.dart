import 'package:flutter/foundation.dart';

/// Estado global do modo de inferência (Cloud vs Local).
/// Compartilhado entre CameraScreen e PerfilScreen.
class ModoInferencia extends ChangeNotifier {
  ModoInferencia._();
  static final instance = ModoInferencia._();

  bool _local = false;

  /// true = TFLite on-device, false = Django API cloud
  bool get isLocal => _local;

  void setLocal(bool valor) {
    if (_local != valor) {
      _local = valor;
      notifyListeners();
    }
  }

  void toggle() => setLocal(!_local);
}
