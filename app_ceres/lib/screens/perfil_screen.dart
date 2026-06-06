import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../services/auth_storage.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';
import '../widgets/offline_banner.dart';

class PerfilScreen extends StatefulWidget {
  const PerfilScreen({super.key});

  @override
  State<PerfilScreen> createState() => _PerfilScreenState();
}

class _PerfilScreenState extends State<PerfilScreen> {
  late Future<Map<String, dynamic>?> _futurePerfil;

  // Estado local de configurações
  int _modo = 0; // 0 = Online API, 1 = Offline TFLite
  bool _pushDoenca = true, _pushAmbiente = true, _resumoDiario = false;

  @override
  void initState() {
    super.initState();
    _futurePerfil = _carregarPerfil();
  }

  Future<Map<String, dynamic>?> _carregarPerfil() async {
    try {
      return await ApiService.instance.me();
    } catch (_) {
      return null; // offline ou sem token
    }
  }

  // ── Logout ────────────────────────────────────────────────────────────────
  Future<void> _logout() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        backgroundColor: CeresColors.paper,
        title: Text('Sair', style: CeresType.serif(const TextStyle(
            fontSize: 17, color: CeresColors.ink))),
        content: Text('Deseja encerrar a sessão?',
            style: CeresType.sans(const TextStyle(
                fontSize: 13, color: CeresColors.ink2))),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('Cancelar', style: CeresType.sans(const TextStyle(
                color: CeresColors.ink3))),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text('Sair', style: CeresType.sans(const TextStyle(
                color: CeresColors.blight))),
          ),
        ],
      ),
    );
    if (ok != true || !mounted) return;
    await AuthStorage.instance.limparTokens();
    if (!mounted) return;
    Navigator.of(context).pushNamedAndRemoveUntil('/login', (_) => false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: SafeArea(
        bottom: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const CeresSubBar(
              title: 'Configurações',
              subtitle: 'conta · sistema',
            ),
            Expanded(child: OfflineBanner(
              child: FutureBuilder<Map<String, dynamic>?>(
                future: _futurePerfil,
                builder: (context, snap) {
                  if (snap.connectionState != ConnectionState.done) {
                    return const Center(
                      child: CircularProgressIndicator(
                        color: CeresColors.leafLive,
                        strokeWidth: 1.5,
                      ),
                    );
                  }
                  return _conteudo(snap.data);
                },
              ),
            )),
          ],
        ),
      ),
    );
  }

  Widget _conteudo(Map<String, dynamic>? perfil) {
    final nome   = perfil?['nome']  as String? ?? 'Usuário';
    final email  = perfil?['email'] as String? ?? '—';
    final inicial = nome.isNotEmpty ? nome[0].toUpperCase() : 'U';

    return ListView(
      padding: const EdgeInsets.fromLTRB(22, 0, 22, 16),
      children: [
        // ── Modo de inferência ───────────────────────────────────────────
        _secao('Modo de inferência'),
        Container(
          decoration: BoxDecoration(
            border: Border.all(color: CeresColors.hairline),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Column(children: [
            _modoOpt(0, 'Online · API Django',
                'Modelo na nuvem · maior acurácia, requer rede', '98,1%'),
            const Divider(height: 1, color: CeresColors.hairline),
            _modoOpt(1, 'Offline · IA no dispositivo',
                'Modelo TFLite local · funciona sem rede', '639 KB'),
          ]),
        ),

        // ── Notificações push ────────────────────────────────────────────
        _secao('Notificações push'),
        _toggleRow('Doença detectada pelo sensor',
            'enviar push imediato em qualquer horário',
            _pushDoenca, (v) => setState(() => _pushDoenca = v)),
        _toggleRow('Ambiente fora do ideal',
            'umidade, temperatura, irrigação',
            _pushAmbiente, (v) => setState(() => _pushAmbiente = v)),
        _toggleRow('Resumo diário',
            '06:00 · diário do talhão',
            _resumoDiario, (v) => setState(() => _resumoDiario = v)),

        // ── Conexão ──────────────────────────────────────────────────────
        _secao('Conexão'),
        _dataRow('URL do servidor', 'para técnicos · endpoint da API', '10.0.2.2:8080'),
        _dataRow('MQTT broker', '', 'localhost:1883'),

        // ── Comunidade ───────────────────────────────────────────────────
        _secao('Comunidade'),
        _linkRow(context, Icons.notifications_outlined,
            'Central de alertas', 'push · IoT · doenças e sensores', '/alertas'),
        _linkRow(context, Icons.people_outline,
            'Agrônomos parceiros', 'especialistas em fitopatologia · MT', '/agronomos'),

        // ── Conta ────────────────────────────────────────────────────────
        _secao('Conta'),
        _accountCard(nome, email, inicial),
      ],
    );
  }

  Widget _linkRow(BuildContext context, IconData icon, String titulo,
      String sub, String rota) {
    return GestureDetector(
      onTap: () => Navigator.pushNamed(context, rota),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: const BoxDecoration(
            border: Border(bottom: BorderSide(color: Color(0xFFEAE4DA)))),
        child: Row(children: [
          Container(width: 28, height: 28,
            decoration: BoxDecoration(
              color: CeresColors.paper2, shape: BoxShape.circle,
              border: Border.all(color: CeresColors.hairline)),
            child: Icon(icon, size: 14, color: CeresColors.leafDeep),
          ),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
              children: [
            Text(titulo, style: CeresType.sans(const TextStyle(
                fontSize: 12, fontWeight: FontWeight.w500, color: CeresColors.ink))),
            const SizedBox(height: 2),
            Text(sub, style: CeresType.sans(const TextStyle(
                fontSize: 10, color: CeresColors.ink3))),
          ])),
          const Icon(Icons.chevron_right, size: 16, color: CeresColors.ink3),
        ]),
      ),
    );
  }

  // ── Helpers de seção ────────────────────────────────────────────────────────
  Widget _secao(String t) => Padding(
    padding: const EdgeInsets.only(top: 16, bottom: 8),
    child: Row(children: [
      Text(t.toUpperCase(), style: CeresType.label),
      const SizedBox(width: 8),
      const Expanded(child: Divider(height: 1)),
    ]),
  );

  Widget _modoOpt(int i, String nome, String desc, String tag) {
    final on = _modo == i;
    return InkWell(
      onTap: () => setState(() => _modo = i),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
        child: Row(children: [
          Container(width: 16, height: 16,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: on ? CeresColors.leafDark : CeresColors.ink3),
            ),
            child: on ? Center(child: Container(width: 8, height: 8,
                decoration: const BoxDecoration(
                    color: CeresColors.leafDark, shape: BoxShape.circle))) : null,
          ),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(nome, style: CeresType.sans(TextStyle(
                fontSize: 13,
                fontWeight: on ? FontWeight.w500 : FontWeight.w400,
                color: on ? CeresColors.leafDeep : CeresColors.ink))),
            const SizedBox(height: 2),
            Text(desc, style: CeresType.sans(const TextStyle(
                fontSize: 10, color: CeresColors.ink3))),
          ])),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: on ? const Color(0xFFD7E8CE) : CeresColors.boneDeep,
              borderRadius: BorderRadius.circular(3),
            ),
            child: Text(tag, style: CeresType.mono(TextStyle(
                fontSize: 8.5, letterSpacing: 1.2,
                color: on ? CeresColors.leafDeep : CeresColors.ink3))),
          ),
        ]),
      ),
    );
  }

  Widget _toggleRow(String l1, String l2, bool value, ValueChanged<bool> onChanged) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8),
      decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: Color(0xFFEAE4DA)))),
      child: Row(children: [
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(l1, style: CeresType.sans(const TextStyle(
              fontSize: 12, color: CeresColors.ink))),
          if (l2.isNotEmpty) ...[
            const SizedBox(height: 2),
            Text(l2, style: CeresType.sans(const TextStyle(
                fontSize: 10, color: CeresColors.ink3))),
          ],
        ])),
        _switch(value, onChanged),
      ]),
    );
  }

  Widget _switch(bool on, ValueChanged<bool> onChanged) {
    return GestureDetector(
      onTap: () => onChanged(!on),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        width: 34, height: 18,
        decoration: BoxDecoration(
          color: on ? CeresColors.leafDark : CeresColors.dust,
          borderRadius: BorderRadius.circular(999),
        ),
        child: AnimatedAlign(
          duration: const Duration(milliseconds: 150),
          alignment: on ? Alignment.centerRight : Alignment.centerLeft,
          child: Container(
            width: 14, height: 14, margin: const EdgeInsets.all(2),
            decoration: const BoxDecoration(
              color: CeresColors.paper, shape: BoxShape.circle,
              boxShadow: [BoxShadow(
                  color: Color(0x33000000), blurRadius: 2, offset: Offset(0, 1))],
            ),
          ),
        ),
      ),
    );
  }

  Widget _dataRow(String l1, String l2, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8),
      decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: Color(0xFFEAE4DA)))),
      child: Row(children: [
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(l1, style: CeresType.sans(const TextStyle(
              fontSize: 12, color: CeresColors.ink))),
          if (l2.isNotEmpty) ...[
            const SizedBox(height: 2),
            Text(l2, style: CeresType.sans(const TextStyle(
                fontSize: 10, color: CeresColors.ink3))),
          ],
        ])),
        Text(value, style: CeresType.mono(const TextStyle(
            fontSize: 10.5, color: CeresColors.ink2))),
      ]),
    );
  }

  Widget _accountCard(String nome, String email, String inicial) {
    return Container(
      margin: const EdgeInsets.only(top: 4),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: CeresColors.paper2,
        border: Border.all(color: CeresColors.hairline),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(children: [
        Container(width: 36, height: 36, alignment: Alignment.center,
          decoration: const BoxDecoration(
              color: CeresColors.leafDark, shape: BoxShape.circle),
          child: Text(inicial, style: CeresType.serif(const TextStyle(
              fontSize: 15, fontStyle: FontStyle.italic,
              fontWeight: FontWeight.w500, color: CeresColors.paper))),
        ),
        const SizedBox(width: 10),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(nome, style: CeresType.sans(const TextStyle(
              fontSize: 12, fontWeight: FontWeight.w500, color: CeresColors.ink))),
          const SizedBox(height: 2),
          Text(email, style: CeresType.mono(const TextStyle(
              fontSize: 9.5, color: CeresColors.ink3))),
        ])),
        GestureDetector(
          onTap: _logout,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: const Color(0xFFFBEBE5),
              border: Border.all(color: CeresColors.actionBoxBorder),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Text('Sair', style: CeresType.sans(const TextStyle(
                fontSize: 10.5, fontWeight: FontWeight.w500,
                color: CeresColors.blight))),
          ),
        ),
      ]),
    );
  }
}
