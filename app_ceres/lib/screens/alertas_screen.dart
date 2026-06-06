import 'package:flutter/material.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';

class _Alert {
  final CeresStatus status;
  final bool unread;
  final String name, meta, action, pct, ts;
  const _Alert(this.status, this.unread, this.name, this.meta, this.action,
      this.pct, this.ts);
}

class AlertasScreen extends StatelessWidget {
  const AlertasScreen({super.key});

  static const _list = [
    _Alert(CeresStatus.disease, true, 'Requeima detectada',
        'esp32-fz-04 · talhão 04 · 03:12',
        'Aplicar fungicida cobre · isolar linha 12', '94,1%', 'agora'),
    _Alert(CeresStatus.disease, true, 'Pinta-preta detectada',
        'esp32-fz-02 · talhão 02 · 06:48',
        'Fungicida cúprico · remover folhas afetadas', '87,3%', '3 h'),
    _Alert(CeresStatus.warn, true, 'Umidade do ar alta',
        'esp32-fz-04 · 74% · 09:30',
        'Risco de fungo · ventilar talhão', '74%', '15 min'),
    _Alert(CeresStatus.healthy, false, 'Mancha-de-Septoria',
        'esp32-fz-05 · ontem 17:24', '', '71,5%', 'ontem'),
    _Alert(CeresStatus.healthy, false, 'Mancha-bacteriana',
        'esp32-fz-06 · ontem 11:08', '', '82,4%', 'ontem'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: SafeArea(
        bottom: false,
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          CeresSubBar(
            title: 'Alertas',
            subtitle: 'push · IoT',
            actions: [CeresIconBtn(Icons.done_all, onTap: () {})],
          ),
          const CeresPageTitle(
              emphasis: '3', rest: 'não lidos · 12 hoje', count: 'push · ativo'),
          const CeresChips(
              labels: ['Não lidos', 'Todos', 'Doenças', 'Ambiente'],
              activeIndex: 0),
          const SizedBox(height: 8),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.fromLTRB(22, 0, 22, 16),
              itemCount: _list.length,
              itemBuilder: (_, i) => _row(_list[i]),
            ),
          ),
        ]),
      ),
    );
  }

  Widget _row(_Alert a) {
    final c = CeresColors.forStatus(a.status);
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 10),
      decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: Color(0xFFEAE4DA)))),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Ícone com badge de não lido
        a.unread
            ? Stack(clipBehavior: Clip.none, children: [
                Container(
                  width: 28, height: 28,
                  decoration: BoxDecoration(color: c, shape: BoxShape.circle),
                  child: Icon(
                      a.status == CeresStatus.warn
                          ? Icons.water_drop_outlined
                          : Icons.warning_amber_rounded,
                      size: 14, color: CeresColors.paper),
                ),
                Positioned(
                  top: -2, right: -2,
                  child: Container(width: 8, height: 8,
                    decoration: BoxDecoration(
                        color: CeresColors.blight, shape: BoxShape.circle,
                        border: Border.all(color: CeresColors.bone, width: 1.5))),
                ),
              ])
            : Container(
                width: 28, height: 28,
                decoration: BoxDecoration(shape: BoxShape.circle,
                    border: Border.all(color: CeresColors.ink3)),
                child: const Icon(Icons.check, size: 13, color: CeresColors.ink3)),
        const SizedBox(width: 10),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(a.name, style: CeresType.serif(TextStyle(
              fontSize: a.unread ? 14 : 13.5,
              fontWeight: a.unread ? FontWeight.w500 : FontWeight.w400,
              color: a.unread ? CeresColors.ink : CeresColors.ink2))),
          const SizedBox(height: 3),
          Text(a.meta, style: CeresType.mono(const TextStyle(
              fontSize: 9, color: CeresColors.ink3))),
          if (a.unread && a.action.isNotEmpty) ...[
            const SizedBox(height: 5),
            Container(
              padding: const EdgeInsets.only(left: 8),
              decoration: BoxDecoration(border: Border(left: BorderSide(
                  color: a.status == CeresStatus.warn
                      ? CeresColors.dryGrass
                      : CeresColors.blight,
                  width: 2))),
              child: Text(a.action, style: CeresType.sans(const TextStyle(
                  fontSize: 11, height: 1.3, color: CeresColors.ink))),
            ),
          ],
        ])),
        const SizedBox(width: 8),
        Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text(a.pct, style: CeresType.mono(TextStyle(
              fontSize: 11, fontWeight: FontWeight.w500,
              color: a.unread ? c : CeresColors.ink3))),
          const SizedBox(height: 3),
          Text(a.ts, style: CeresType.mono(const TextStyle(
              fontSize: 9, color: CeresColors.ink3))),
        ]),
      ]),
    );
  }
}
