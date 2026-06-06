import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';
import '../theme/ceres_theme.dart';

/// Tela de redefinição de senha direta (sem código por e-mail).
/// Usuário informa e-mail cadastrado + nova senha.
class EsqueciSenhaScreen extends StatefulWidget {
  const EsqueciSenhaScreen({super.key});

  @override
  State<EsqueciSenhaScreen> createState() => _EsqueciSenhaScreenState();
}

class _EsqueciSenhaScreenState extends State<EsqueciSenhaScreen> {
  final _emailCtrl = TextEditingController();
  final _senhaCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();

  bool _carregando = false;
  String? _erro;
  bool _senhaVisivel = false;

  @override
  void dispose() {
    _emailCtrl.dispose();
    _senhaCtrl.dispose();
    _confirmCtrl.dispose();
    super.dispose();
  }

  Future<void> _redefinir() async {
    final email = _emailCtrl.text.trim();
    final senha = _senhaCtrl.text;
    final confirm = _confirmCtrl.text;

    if (email.isEmpty || !email.contains('@') || !email.contains('.')) {
      setState(() => _erro = 'Digite um e-mail válido.');
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

    setState(() { _carregando = true; _erro = null; });
    try {
      final msg = await ApiService.instance.resetarSenha(
        email: email,
        novaSenha: senha,
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(msg, style: const TextStyle(color: CeresColors.paper)),
          backgroundColor: CeresColors.leafLive,
        ),
      );
      Navigator.of(context).pop();
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
          // Appbar com botão voltar
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
                  'Redefinir senha',
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
                      'RECUPERAÇÃO DE ACESSO',
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 9, letterSpacing: 0.22, color: CeresColors.ink3,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(child: Container(height: 0.8, color: CeresColors.hairline)),
                  ]),
                  const SizedBox(height: 14),

                  Text(
                    'Informe o e-mail cadastrado e escolha uma nova senha.',
                    style: GoogleFonts.ibmPlexSans(
                      fontSize: 12, color: CeresColors.ink2, height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 20),

                  _campo('E-MAIL', _emailCtrl, keyboard: TextInputType.emailAddress),
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

                  // Erro
                  if (_erro != null) ...[
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: CeresColors.blightSoft,
                        borderRadius: BorderRadius.circular(4),
                        border: const Border(left: BorderSide(color: CeresColors.blight, width: 3)),
                      ),
                      child: Text(_erro!,
                          style: GoogleFonts.ibmPlexSans(fontSize: 12, color: CeresColors.blight)),
                    ),
                    const SizedBox(height: 14),
                  ],

                  // Botão
                  FilledButton(
                    onPressed: _carregando ? null : _redefinir,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(_carregando ? 'Aguarde...' : 'Redefinir senha'),
                        if (!_carregando) ...[
                          const SizedBox(width: 8),
                          const Icon(Icons.arrow_forward, size: 18),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

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
}
