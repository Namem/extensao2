import 'package:flutter/material.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';

class _Agro {
  final String initials, name, spec, rating, place;
  final Color avatarBg, avatarFg;
  const _Agro(this.initials, this.name, this.spec, this.rating, this.place,
      this.avatarBg, this.avatarFg);
}

class AgronomosScreen extends StatefulWidget {
  const AgronomosScreen({super.key});

  @override
  State<AgronomosScreen> createState() => _AgronomosScreenState();
}

class _AgronomosScreenState extends State<AgronomosScreen> {
  int _filtro = 0; // 0=Todos 1=Fitopatologia 2=Manejo 3=Solo

  static const _a1bg = Color(0xFFE6D0A8), _a1fg = Color(0xFF6B5526);
  static const _a2bg = Color(0xFFCDE0BE), _a2fg = Color(0xFF2E4A2A);
  static const _a3bg = Color(0xFFEBCBBE), _a3fg = Color(0xFF7A3A28);
  static const _a4bg = Color(0xFFCAD6E6), _a4fg = Color(0xFF2F4459);

  static const _list = [
    _Agro('RB', 'Roberta Bittencourt', 'Fitopatologia', '4,9', 'Sinop · MT', _a2bg, _a2fg),
    _Agro('JS', 'João Silveira', 'Manejo integrado', '4,8', 'Cuiabá · MT', _a1bg, _a1fg),
    _Agro('MA', 'Márcia Andrade', 'Fitopatologia · solanáceas', '4,9', 'Rondonópolis · MT', _a3bg, _a3fg),
    _Agro('DC', 'Daniel Carvalho', 'Solo · irrigação', '4,7', 'Lucas do Rio Verde', _a4bg, _a4fg),
    _Agro('FN', 'Fernanda Nogueira', 'Fitopatologia', '5,0', 'Sorriso · MT', _a2bg, _a2fg),
    _Agro('PE', 'Paulo Esteves', 'Manejo · nutrição', '4,6', 'Tangará da Serra', _a1bg, _a1fg),
  ];

  List<_Agro> get _filtrados {
    switch (_filtro) {
      case 1: return _list.where((a) => a.spec.toLowerCase().contains('fito')).toList();
      case 2: return _list.where((a) => a.spec.toLowerCase().contains('manejo')).toList();
      case 3: return _list.where((a) => a.spec.toLowerCase().contains('solo')).toList();
      default: return _list;
    }
  }

  void _abrirChat(_Agro a) {
    showModalBottomSheet(
      context: context,
      backgroundColor: CeresColors.paper,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(12))),
      builder: (_) => Padding(
        padding: const EdgeInsets.fromLTRB(22, 18, 22, 32),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 36, height: 3,
              decoration: BoxDecoration(color: CeresColors.hairline,
                  borderRadius: BorderRadius.circular(2))),
          const SizedBox(height: 16),
          Row(children: [
            Container(width: 42, height: 42, alignment: Alignment.center,
              decoration: BoxDecoration(color: a.avatarBg, shape: BoxShape.circle),
              child: Text(a.initials, style: CeresType.serif(TextStyle(
                  fontSize: 16, fontWeight: FontWeight.w500, color: a.avatarFg))),
            ),
            const SizedBox(width: 12),
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(a.name, style: CeresType.serif(const TextStyle(
                  fontSize: 15, fontWeight: FontWeight.w500, color: CeresColors.ink))),
              Text(a.spec.toUpperCase(), style: CeresType.mono(const TextStyle(
                  fontSize: 9, letterSpacing: 1.2, color: CeresColors.leafDeep))),
            ])),
          ]),
          const SizedBox(height: 16),
          Text(
            'O contato por chat será implementado na Sprint 3 com integração '
            'WhatsApp Business API. Por enquanto, o diagnóstico é salvo e '
            'enviado ao agrônomo quando a funcionalidade estiver ativa.',
            style: CeresType.sans(const TextStyle(
                fontSize: 12, height: 1.5, color: CeresColors.ink2)),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () => Navigator.pop(context),
            child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
              Icon(Icons.check, size: 16),
              SizedBox(width: 8),
              Text('Entendido'),
            ]),
          ),
        ]),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final lista = _filtrados;
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: SafeArea(
        bottom: false,
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          CeresSubBar(
            title: 'Agrônomos',
            subtitle: 'parceiros · MT',
            actions: [CeresIconBtn(Icons.search, onTap: () {})],
          ),
          CeresPageTitle(
              emphasis: 'Agrônomos', rest: 'parceiros',
              count: '${lista.length} · MT'),
          CeresChips(
            labels: const ['Todos', 'Fitopatologia', 'Manejo', 'Solo'],
            activeIndex: _filtro,
            onTap: (i) => setState(() => _filtro = i),
          ),
          const SizedBox(height: 10),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.fromLTRB(22, 0, 22, 16),
              itemCount: lista.length,
              itemBuilder: (_, i) => _row(lista[i]),
            ),
          ),
          // Rodapé — convite para agrônomos
          Padding(
            padding: const EdgeInsets.fromLTRB(22, 0, 22, 14),
            child: OutlinedButton.icon(
              onPressed: () => Navigator.pushNamed(context, '/seja-parceiro'),
              icon: const Icon(Icons.star_border, size: 16),
              label: const Text('Seja um agrônomo parceiro'),
            ),
          ),
        ]),
      ),
    );
  }

  Widget _row(_Agro a) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 11),
      decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: Color(0xFFEAE4DA)))),
      child: Row(children: [
        Container(width: 40, height: 40, alignment: Alignment.center,
          decoration: BoxDecoration(color: a.avatarBg, shape: BoxShape.circle),
          child: Text(a.initials, style: CeresType.serif(TextStyle(
              fontSize: 15, fontWeight: FontWeight.w500, color: a.avatarFg))),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(a.name, maxLines: 1, overflow: TextOverflow.ellipsis,
              style: CeresType.serif(const TextStyle(
                  fontSize: 14, fontWeight: FontWeight.w500, color: CeresColors.ink))),
          const SizedBox(height: 3),
          Text(a.spec.toUpperCase(), style: CeresType.mono(const TextStyle(
              fontSize: 9, letterSpacing: 1.4, color: CeresColors.leafDeep))),
          const SizedBox(height: 4),
          Row(children: [
            Text('★ ', style: CeresType.sans(const TextStyle(
                fontSize: 9.5, color: CeresColors.dryGrass))),
            Text(a.rating, style: CeresType.sans(const TextStyle(
                fontSize: 10, fontWeight: FontWeight.w500, color: CeresColors.ink))),
            const SizedBox(width: 6),
            Container(width: 2, height: 2, decoration: const BoxDecoration(
                color: CeresColors.ink3, shape: BoxShape.circle)),
            const SizedBox(width: 6),
            Text(a.place, style: CeresType.sans(const TextStyle(
                fontSize: 10, color: CeresColors.ink3))),
          ]),
        ])),
        const SizedBox(width: 8),
        GestureDetector(
          onTap: () => _abrirChat(a),
          child: Container(width: 32, height: 32,
            decoration: BoxDecoration(
              shape: BoxShape.circle, color: CeresColors.paper,
              border: Border.all(color: CeresColors.leafDeep)),
            child: const Icon(Icons.chat_bubble_outline,
                size: 15, color: CeresColors.leafDeep),
          ),
        ),
      ]),
    );
  }
}
