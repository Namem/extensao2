import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';

class CadastroScreen extends StatefulWidget {
  const CadastroScreen({super.key});

  @override
  State<CadastroScreen> createState() => _CadastroScreenState();
}

class _CadastroScreenState extends State<CadastroScreen> {
  int _tipo = 0; // 0 = Produtor, 1 = Agrônomo
  bool _carregando = false;
  String? _erro;
  final _nomeCtrl  = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _senhaCtrl = TextEditingController();
  final _confCtrl  = TextEditingController();
  final _creaCtrl  = TextEditingController();

  Future<void> _criar() async {
    final nome  = _nomeCtrl.text.trim();
    final email = _emailCtrl.text.trim();
    final senha = _senhaCtrl.text;
    final conf  = _confCtrl.text;
    final crea  = _creaCtrl.text.trim();

    if (nome.isEmpty || email.isEmpty || senha.isEmpty) {
      setState(() => _erro = 'Preencha todos os campos obrigatórios.');
      return;
    }
    if (!email.contains('@') || !email.contains('.')) {
      setState(() => _erro = 'Digite um e-mail válido.');
      return;
    }
    if (senha.length < 6) {
      setState(() => _erro = 'Senha deve ter no mínimo 6 caracteres.');
      return;
    }
    if (senha != conf) {
      setState(() => _erro = 'As senhas não coincidem.');
      return;
    }
    if (_tipo == 1 && crea.isEmpty) {
      setState(() => _erro = 'CREA obrigatório para agrônomo.');
      return;
    }

    setState(() { _carregando = true; _erro = null; });
    try {
      await ApiService.instance.registrar(
        nome: nome, email: email, senha: senha,
        tipo: _tipo == 0 ? 'produtor' : 'agronomo',
        crea: crea,
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Conta criada! Faça login para continuar.'),
        backgroundColor: CeresColors.leafDark,
      ));
      Navigator.of(context).pop();
    } catch (e) {
      setState(() => _erro = e.toString().replaceFirst('Exception: ', ''));
    } finally {
      if (mounted) setState(() => _carregando = false);
    }
  }

  @override
  void dispose() {
    _nomeCtrl.dispose();
    _emailCtrl.dispose();
    _senhaCtrl.dispose();
    _confCtrl.dispose();
    _creaCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.paper,
      body: SafeArea(
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          const CeresSubBar(title: 'Criar conta', subtitle: 'passo 1 de 1'),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(26, 6, 26, 18),
              children: [
                RichText(text: TextSpan(children: [
                  TextSpan(text: 'Abra ', style: CeresType.serif(const TextStyle(
                      fontSize: 22, fontStyle: FontStyle.italic, fontWeight: FontWeight.w400,
                      color: CeresColors.leafDeep, letterSpacing: -0.4))),
                  TextSpan(text: 'seu caderno de campo.', style: CeresType.serif(
                      const TextStyle(fontSize: 22, fontWeight: FontWeight.w500,
                          color: CeresColors.ink, letterSpacing: -0.4))),
                ])),
                const SizedBox(height: 6),
                Text(
                  'Cadastre-se para enviar diagnósticos do seu talhão e falar '
                  'com agrônomos parceiros.',
                  style: CeresType.body,
                ),
                const SizedBox(height: 12),
                _campo('NOME COMPLETO', _nomeCtrl),
                _campo('EMAIL', _emailCtrl, tipo: TextInputType.emailAddress),
                _campo('SENHA', _senhaCtrl, obscure: true),
                _campo('CONFIRMAR SENHA', _confCtrl, obscure: true),
                const SizedBox(height: 12),
                Text('TIPO DE USUÁRIO', style: CeresType.label),
                const SizedBox(height: 6),
                _segmented(),
                if (_tipo == 1) _campo('CREA · OBRIGATÓRIO PARA AGRÔNOMO', _creaCtrl),
                const SizedBox(height: 14),
                if (_erro != null) ...[
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFFFBEBE5),
                      borderRadius: BorderRadius.circular(4),
                      border: const Border(left: BorderSide(color: CeresColors.blight, width: 3)),
                    ),
                    child: Text(_erro!, style: CeresType.sans(const TextStyle(
                        fontSize: 12, color: CeresColors.blight))),
                  ),
                  const SizedBox(height: 8),
                ],
                FilledButton(
                  onPressed: _carregando ? null : _criar,
                  child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                    if (_carregando)
                      const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(
                          strokeWidth: 1.5, color: CeresColors.paper))
                    else ...[
                      const Text('Criar conta'),
                      const SizedBox(width: 8),
                      const Icon(Icons.arrow_forward, size: 18),
                    ],
                  ]),
                ),
                const SizedBox(height: 10),
                Center(child: RichText(text: TextSpan(children: [
                  TextSpan(text: 'já tem conta? ', style: CeresType.sans(
                      const TextStyle(fontSize: 11, color: CeresColors.ink2))),
                  WidgetSpan(child: GestureDetector(
                    onTap: () => Navigator.of(context).maybePop(),
                    child: Text('Entrar', style: CeresType.sans(const TextStyle(
                        fontSize: 11, fontWeight: FontWeight.w500,
                        color: CeresColors.leafDeep,
                        decoration: TextDecoration.underline,
                        decorationColor: CeresColors.leafDeep))),
                  )),
                ]))),
              ],
            ),
          ),
        ]),
      ),
    );
  }

  Widget _campo(String label, TextEditingController ctrl,
      {bool obscure = false, TextInputType tipo = TextInputType.text}) {
    return Container(
      margin: const EdgeInsets.only(top: 6),
      padding: const EdgeInsets.only(top: 8, bottom: 6),
      decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: CeresColors.hairline))),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: CeresType.label),
        const SizedBox(height: 8),
        TextField(
          controller: ctrl,
          obscureText: obscure,
          keyboardType: tipo,
          style: CeresType.sans(const TextStyle(fontSize: 14, color: CeresColors.ink)),
          decoration: const InputDecoration(
              isDense: true, contentPadding: EdgeInsets.zero, border: InputBorder.none),
        ),
      ]),
    );
  }

  Widget _segmented() {
    return Container(
      decoration: BoxDecoration(
        color: CeresColors.paper2,
        border: Border.all(color: CeresColors.hairline),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Row(children: [
        _segOpt('Produtor', 'rural', 0),
        Container(width: 1, height: 40, color: CeresColors.hairline),
        _segOpt('Agrônomo', 'parceiro', 1),
      ]),
    );
  }

  Widget _segOpt(String titulo, String sub, int i) {
    final on = _tipo == i;
    return Expanded(
      child: InkWell(
        onTap: () => setState(() => _tipo = i),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 9),
          decoration: BoxDecoration(
            color: on ? CeresColors.leafDark : Colors.transparent,
            borderRadius: BorderRadius.circular(5),
          ),
          child: Column(children: [
            Text(titulo, style: CeresType.sans(TextStyle(
                fontSize: 11.5, fontWeight: on ? FontWeight.w500 : FontWeight.w400,
                color: on ? CeresColors.paper : CeresColors.ink2))),
            const SizedBox(height: 2),
            Text(sub.toUpperCase(), style: CeresType.mono(TextStyle(
                fontSize: 8, letterSpacing: 1.2,
                color: on ? const Color(0xCCDCE6CE) : CeresColors.ink3))),
          ]),
        ),
      ),
    );
  }
}
