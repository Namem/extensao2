import 'package:shared_preferences/shared_preferences.dart';

/// Gerencia persistência de autenticação via SharedPreferences.
///
/// Tokens JWT e e-mail salvos em SharedPreferences (cross-platform).
/// Para produção mobile com armazenamento seguro (Keystore/Keychain),
/// substituir por flutter_secure_storage quando o build for Android-only.
class AuthStorage {
  AuthStorage._();
  static final AuthStorage instance = AuthStorage._();

  static const _keyAccess  = 'ceres_access_token';
  static const _keyRefresh = 'ceres_refresh_token';
  static const _keyEmail   = 'ceres_email';

  // ── Tokens ────────────────────────────────────────────────────────────────

  Future<void> salvarTokens({
    required String access,
    required String refresh,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyAccess,  access);
    await prefs.setString(_keyRefresh, refresh);
  }

  Future<String?> lerAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyAccess);
  }

  Future<String?> lerRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyRefresh);
  }

  Future<void> limparTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyAccess);
    await prefs.remove(_keyRefresh);
  }

  // ── E-mail ────────────────────────────────────────────────────────────────

  Future<void> salvarEmail(String email) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyEmail, email);
  }

  Future<String> lerEmail() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyEmail) ?? '';
  }

  Future<void> limparEmail() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyEmail);
  }
}
