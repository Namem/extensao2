import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';
import '../theme/ceres_theme.dart';

/// Tela de recuperação de senha em 2 etapas:
/// 1. Digita e-mail → recebe código de 6 dígitos por e-mail
/// 2. Digita código + nova senha → senha redefinida
class EsqueciSenhaScreen extends StatefulWidget {
  const EsqueciSenhaScreen({super.key});

  @override
  State<EsqueciSenhaScreen> createState() => _EsqueciSenhaScreenState();
}

class _EsqueciSenhaScreenState extends State<EsqueciSenhaScreen> {
  final _emailCtrl = TextEditingController();
  final _codigoCtrl = TextEditingController();
  final _senhaCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();

  bool _carregando = false;
  String? _erro;
  String? _sucesso;
  bool _codigoEnviado = false;
  bool _senhaVisivel = false;

  @override
  void dispose() {
    _emailCtrl.dispose();
    _codigoCtrl.dispose();
    _senhaCtrl.dispose();
    _confirmCtrl.dispose();
    super.dispose();
  }

  /// Etapa 1: solicita código de recuperação.
  Future<void> _enviarCodigo() async {
    final email = _emailCtrl.text.trim();
    if (email.isEmpty || !email.contains('@')) {
      setState(() => _erro = 'Digite um e-mail válido.');
      return;
    }
    setState(() { _carregando = true; _erro = null; _sucesso = null; });
    try {
      final msg = await ApiService.instance.esqueceuSenha(email: email);
      setState(() {
        _codigoEnviado = true;
        _sucesso = msg;
      });
    } catch (e) {
      setState(() => _erro = e.toString().replaceFirst('Exception: ', ''));
    } finally {
      setState(() => _carregando = false);
    }
  }

  /// Etapa 2: valida código e redefine senha.
  Future<void> _redefinirSenha() async {
    final codigo = _codigoCtrl.text.trim();
    final senha = _senhaCtrl.text;
    final confirm = _confirmCtrl.text;

    if (codigo.length != 6) {
      setState(() => _erro = 'O código deve ter 6 dígitos.');
      return;
    }
    if (senha.length < 6) {
      setState(() => _erro = 'Senha deve ter no mínimo 6 caracteres.');
      return;
    }
    if (senha != confirm) {
      setState(() => _erro = 'As senhas não coincidem.');
      return;
    }

    setState(() { _carregando = true; _erro = null; _sucesso = null; });
    try {
      final msg = await ApiService.instance.resetarSenha(
        email: _emailCtrl.text.trim(),
        codigo: codigo,
        novaSenha: senha,
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(msg, style: const TextStyle(color: CeresColors.paper)),
          backgroundColor: CeresColors.leafLive,
        ),
      );
      Navigator.of(context).pop(); // volta ao login
    } catch (e) {
      setState(() => _erro = e.toString().replaceFirst('Exception: ', ''));
    } finally {
      if (mounted) setState(() => _carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.of(context).padding.top;

    return Scaffold(
      backgroundColor: CeresColors.paper,
      body: Column(
        children: [
          // Appbar simples com botão voltar
          Padding(
            padding: EdgeInsets.fromLTRB(16, top + 8, 24, 0),
            child: Row(
              children: [
                GestureDetector(
                  onTap: () => Navigator.of(context).pop(),
                  child: Container(
                    width: 32, height: 32,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: CeresColors.hairline),
                    ),
                    child: const Icon(Icons.arrow_back_ios_new_rounded,
                        size: 13, color: CeresColors.ink2),
                  ),
                ),
                const SizedBox(width: 12),
                Text(
                  'Recuperar senha',
                  style: GoogleFonts.newsreader(
                    fontSize: 18,
                    fontWeight: FontWeight.w500,
                    color: CeresColors.ink,
                  ),
                ),
              ],
            ),
          ),

          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(26, 28, 26, 40),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Eyebrow
                  Row(children: [
                    Text(
                      _codigoEnviado
                          ? 'ETAPA 2 · REDEFINIR SENHA'
                          : 'ETAPA 1 · SOLICITAR CÓDIGO',
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 9, letterSpacing: 0.22, color: CeresColors.ink3,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(child: Container(height: 0.8, color: CeresColors.hairline)),
                  ]),
                  const SizedBox(height: 14),

                  // Descrição
                  Text(
                    _codigoEnviado
                        ? 'Digite o código de 6 dígitos enviado para ${_emailCtrl.text.trim()} e escolha uma nova senha.'
                        : 'Informe o e-mail cadastrado. Enviaremos um código de recuperação.',
                    style: GoogleFonts.ibmPlexSans(
                      fontSize: 12, color: CeresColors.ink2, height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Etapa 1: campo e-mail
                  if (!_codigoEnviado) ...[
                    _campo('E-MAIL', _emailCtrl, keyboard: TextInputType.emailAddress),
                    const SizedBox(height: 22),
                  ],

                  // Etapa 2: campos código + senha
                  if (_codigoEnviado) ...[
                    _campo('CÓDIGO (6 DÍGITOS)', _codigoCtrl, keyboard: TextInputType.number),
                    const SizedBox(height: 4),
                    _campo('NOVA SENHA', _senhaCtrl, obscure: !_senhaVisivel,
                      trailing: GestureDetector(
                        onTap: () => setState(() => _senhaVisivel = !_senhaVisivel),
                        child: Icon(
                          _senhaVisivel ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                          size: 16, color: CeresColors.ink3,
                        ),
                      ),
                    ),
                    const SizedBox(height: 4),
                    _campo('CONFIRMAR SENHA', _confirmCtrl, obscure: !_senhaVisivel),
                    const SizedBox(height: 22),
                  ],

                  // Mensagens de erro/sucesso
                  if (_erro != null) ...[
                    _msgBox(_erro!, CeresColors.blight, CeresColors.blightSoft),
                    const SizedBox(height: 12),
                  ],
                  if (_sucesso != null && _codigoEnviado) ...[
                    _msgBox(_sucesso!, CeresColors.leafLive,
                        CeresColors.leafLive.withValues(alpha: 0.08)),
                    const SizedBox(height: 12),
                  ],

                  // Botão principal
                  FilledButton(
                    onPressed: _carregando
                        ? null
                        : (_codigoEnviado ? _redefinirSenha : _enviarCodigo),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(_carregando
                            ? 'Aguarde...'
                            : (_codigoEnviado ? 'Redefinir senha' : 'Enviar código')),
                        if (!_carregando) ...[
                          const SizedBox(width: 8),
                          const Icon(Icons.arrow_forward, size: 18),
                        ],
                      ],
                    ),
                  ),

                  // Link reenviar código
                  if (_codigoEnviado) ...[
                    const SizedBox(height: 14),
                    Center(
                      child: GestureDetector(
                        onTap: _carregando ? null : _enviarCodigo,
                        child: Text(
                          'Reenviar código',
                          style: GoogleFonts.ibmPlexSans(
                            fontSize: 12,
                            color: CeresColors.leafDeep,
                            fontWeight: FontWeight.w500,
                            decoration: TextDecoration.underline,
                            decorationColor: CeresColors.leafDeep,
                          ),
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ── Widgets auxiliares ───────────────────────────────────────────────────

  Widget _campo(String label, TextEditingController ctrl, {
    bool obscure = false,
    TextInputType keyboard = TextInputType.text,
    Widget? trailing,
  }) {
    return Container(
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: CeresColors.hairline, width: 0.8)),
      ),
      padding: const EdgeInsets.fromLTRB(0, 14, 0, 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: GoogleFonts.ibmPlexMono(
            fontSize: 8.5, letterSpacing: 0.2, color: CeresColors.ink3,
          )),
          const SizedBox(height: 8),
          Row(children: [
            Expanded(child: TextField(
              controller: ctrl,
              obscureText: obscure,
              keyboardType: keyboard,
              style: GoogleFonts.ibmPlexSans(fontSize: 14, color: CeresColors.ink),
              decoration: const InputDecoration(
                isDense: true, contentPadding: EdgeInsets.zero, border: InputBorder.none,
              ),
            )),
            ?trailing,
          ]),
        ],
      ),
    );
  }

  Widget _msgBox(String msg, Color cor, Color bg) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(4),
        border: Border(left: BorderSide(color: cor, width: 3)),
      ),
      child: Text(msg, style: GoogleFonts.ibmPlexSans(fontSize: 12, color: cor)),
    );
  }
}
