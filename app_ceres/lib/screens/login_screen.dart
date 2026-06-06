import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';
import '../services/auth_storage.dart';
import '../theme/ceres_theme.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl = TextEditingController();
  final _senhaCtrl = TextEditingController();
  bool _senhaVisivel = false;
  bool _lembrar = true;
  bool _carregando = false;
  String? _erro;

  @override
  void initState() {
    super.initState();
    _carregarEmailSalvo();
  }

  /// Pré-preenche o campo de e-mail se "lembrar acesso" estava ativo.
  Future<void> _carregarEmailSalvo() async {
    final email = await AuthStorage.instance.lerEmail();
    if (email.isNotEmpty && mounted) {
      setState(() => _emailCtrl.text = email);
    }
  }

  @override
  void dispose() {
    _emailCtrl.dispose();
    _senhaCtrl.dispose();
    super.dispose();
  }

  Future<void> _entrar() async {
    final email = _emailCtrl.text.trim();
    if (email.isEmpty || _senhaCtrl.text.isEmpty) {
      setState(() => _erro = 'Preencha e-mail e senha.');
      return;
    }
    if (!email.contains('@') || !email.contains('.')) {
      setState(() => _erro = 'Digite um e-mail válido (ex: nome@email.com).');
      return;
    }
    setState(() { _carregando = true; _erro = null; });
    try {
      await ApiService.instance.login(
        email: _emailCtrl.text.trim(),
        senha: _senhaCtrl.text,
      );
      // Persistir ou limpar e-mail conforme checkbox
      if (_lembrar) {
        await AuthStorage.instance.salvarEmail(_emailCtrl.text.trim());
      } else {
        await AuthStorage.instance.limparEmail();
      }
      if (!mounted) return;
      Navigator.of(context).pushReplacementNamed('/home');
    } catch (e) {
      setState(() => _erro = 'Credenciais inválidas.');
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
          // Marca no topo
          Padding(
            padding: EdgeInsets.fromLTRB(24, top + 10, 24, 0),
            child: Row(
              children: [
                Container(
                  width: 32, height: 32,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: CeresColors.hairline),
                  ),
                  child: const Center(
                      child: CeresLogo(size: 18, color: CeresColors.leafDeep)),
                ),
                const SizedBox(width: 12),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Ceres',
                      style: GoogleFonts.newsreader(
                        fontSize: 18,
                        fontWeight: FontWeight.w500,
                        color: CeresColors.ink,
                        letterSpacing: -0.012,
                        height: 1,
                      ),
                    ),
                    Text(
                      'DIAGNÓSTICO FOLIAR',
                      style: GoogleFonts.ibmPlexMono(
                        fontSize: 8.5,
                        letterSpacing: 0.2,
                        color: CeresColors.ink3,
                        height: 1,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Body principal
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(26, 36, 26, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Eyebrow
                  Row(
                    children: [
                      Text(
                        'CADERNO DE CAMPO · ACESSO',
                        style: GoogleFonts.ibmPlexMono(
                          fontSize: 9,
                          letterSpacing: 0.22,
                          color: CeresColors.ink3,
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Container(height: 0.8, color: CeresColors.hairline),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),

                  // Título
                  RichText(
                    text: TextSpan(
                      style: GoogleFonts.newsreader(
                        fontSize: 30,
                        fontWeight: FontWeight.w500,
                        color: CeresColors.ink,
                        letterSpacing: -0.018,
                        height: 1.05,
                      ),
                      children: const [
                        TextSpan(text: 'Bom dia,\n'),
                        TextSpan(
                          text: 'produtor.',
                          style: TextStyle(
                            fontStyle: FontStyle.italic,
                            fontWeight: FontWeight.w400,
                            color: CeresColors.leafDeep,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    'Acesse o caderno para diagnosticar suas plantas e registrar ocorrências do talhão.',
                    style: GoogleFonts.ibmPlexSans(
                      fontSize: 12,
                      color: CeresColors.ink2,
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Campo e-mail
                  _Campo(
                    label: 'E-MAIL',
                    controller: _emailCtrl,
                    keyboardType: TextInputType.emailAddress,
                  ),
                  const SizedBox(height: 4),

                  // Campo senha
                  _Campo(
                    label: 'SENHA',
                    controller: _senhaCtrl,
                    obscure: !_senhaVisivel,
                    trailing: GestureDetector(
                      onTap: () => setState(() => _senhaVisivel = !_senhaVisivel),
                      child: Icon(
                        _senhaVisivel
                            ? Icons.visibility_off_outlined
                            : Icons.visibility_outlined,
                        size: 16,
                        color: CeresColors.ink3,
                      ),
                    ),
                  ),

                  // Lembrar + esqueceu
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      GestureDetector(
                        onTap: () => setState(() => _lembrar = !_lembrar),
                        child: Row(
                          children: [
                            Container(
                              width: 14,
                              height: 14,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(3),
                                color: _lembrar
                                    ? CeresColors.leafDeep
                                    : Colors.transparent,
                                border: Border.all(
                                  color: _lembrar
                                      ? CeresColors.leafDeep
                                      : CeresColors.hairline,
                                ),
                              ),
                              child: _lembrar
                                  ? const Icon(Icons.check,
                                      size: 10, color: CeresColors.paper)
                                  : null,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              'Manter conectado',
                              style: GoogleFonts.ibmPlexSans(
                                fontSize: 11,
                                color: CeresColors.ink2,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const Spacer(),
                      Text(
                        'Esqueci a senha',
                        style: GoogleFonts.ibmPlexSans(
                          fontSize: 11,
                          color: CeresColors.leafDeep,
                          fontWeight: FontWeight.w500,
                          decoration: TextDecoration.underline,
                          decorationColor: CeresColors.leafDeep,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 22),

                  // Erro
                  if (_erro != null) ...[
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: CeresColors.blightSoft,
                        borderRadius: BorderRadius.circular(4),
                        border: Border(
                            left: BorderSide(
                                color: CeresColors.blight, width: 3)),
                      ),
                      child: Text(
                        _erro!,
                        style: GoogleFonts.ibmPlexSans(
                          fontSize: 12,
                          color: CeresColors.blight,
                        ),
                      ),
                    ),
                    const SizedBox(height: 14),
                  ],

                  // Botão entrar
                  FilledButton(
                    onPressed: _carregando ? null : _entrar,
                    child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                      Text(_carregando ? 'Entrando…' : 'Entrar no caderno'),
                      if (!_carregando) ...[
                        const SizedBox(width: 8),
                        const Icon(Icons.arrow_forward, size: 18),
                      ],
                    ]),
                  ),

                  // Divisor OU
                  const SizedBox(height: 16),
                  Row(children: [
                    const Expanded(child: Divider(height: 1)),
                    Padding(padding: const EdgeInsets.symmetric(horizontal: 10),
                        child: Text('OU', style: CeresType.label)),
                    const Expanded(child: Divider(height: 1)),
                  ]),
                  const SizedBox(height: 14),

                  OutlinedButton.icon(
                    onPressed: () =>
                        Navigator.of(context).pushReplacementNamed('/home'),
                    icon: const Icon(Icons.public, size: 16),
                    label: const Text('Continuar offline'),
                  ),
                  const SizedBox(height: 20),
                  Center(
                    child: GestureDetector(
                      onTap: () => Navigator.pushNamed(context, '/cadastro'),
                      child: RichText(text: TextSpan(children: [
                        TextSpan(text: 'Não tem conta? ',
                            style: GoogleFonts.ibmPlexSans(
                                fontSize: 12, color: CeresColors.ink2)),
                        TextSpan(text: 'Criar conta',
                            style: GoogleFonts.ibmPlexSans(
                                fontSize: 12,
                                fontWeight: FontWeight.w600,
                                color: CeresColors.leafDeep,
                                decoration: TextDecoration.underline,
                                decorationColor: CeresColors.leafDeep)),
                      ])),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Rodapé
          Padding(
            padding: EdgeInsets.fromLTRB(
                26, 14, 26, MediaQuery.of(context).padding.bottom + 26),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'V 0.3.2',
                  style: GoogleFonts.ibmPlexMono(
                    fontSize: 8.5,
                    letterSpacing: 0.2,
                    color: CeresColors.ink3,
                  ),
                ),
                Text(
                  'BUILD · 2026.05',
                  style: GoogleFonts.ibmPlexMono(
                    fontSize: 8.5,
                    letterSpacing: 0.2,
                    color: CeresColors.ink3,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ── Widgets locais ────────────────────────────────────────────────────────────

class _Campo extends StatelessWidget {
  final String label;
  final TextEditingController controller;
  final bool obscure;
  final TextInputType keyboardType;
  final Widget? trailing;

  const _Campo({
    required this.label,
    required this.controller,
    this.obscure = false,
    this.keyboardType = TextInputType.text,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: CeresColors.hairline, width: 0.8)),
      ),
      padding: const EdgeInsets.fromLTRB(0, 14, 0, 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: GoogleFonts.ibmPlexMono(
              fontSize: 8.5,
              letterSpacing: 0.2,
              color: CeresColors.ink3,
            ),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: controller,
                  obscureText: obscure,
                  keyboardType: keyboardType,
                  style: GoogleFonts.ibmPlexSans(
                    fontSize: 14,
                    color: CeresColors.ink,
                  ),
                  decoration: const InputDecoration(
                    isDense: true,
                    contentPadding: EdgeInsets.zero,
                    border: InputBorder.none,
                  ),
                ),
              ),
              ?trailing,
            ],
          ),
        ],
      ),
    );
  }
}

