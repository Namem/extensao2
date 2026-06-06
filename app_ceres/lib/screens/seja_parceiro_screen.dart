import 'package:flutter/material.dart';
import '../theme/ceres_theme.dart';
import '../widgets/ceres_widgets.dart';

class SejaParceiroScreen extends StatelessWidget {
  const SejaParceiroScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: SafeArea(
        bottom: false,
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          const CeresSubBar(title: 'Programa parceiros', subtitle: 'convite'),
          Expanded(child: ListView(
            padding: const EdgeInsets.fromLTRB(28, 8, 28, 8),
            children: [
              Row(children: [
                Text('PARA AGRÔNOMOS', style: CeresType.label),
                const SizedBox(width: 10),
                const Expanded(child: Divider(height: 1)),
              ]),
              const SizedBox(height: 14),
              RichText(text: TextSpan(children: [
                TextSpan(text: 'Seja um ', style: CeresType.serif(const TextStyle(
                    fontSize: 28, fontWeight: FontWeight.w500, height: 1.05,
                    color: CeresColors.ink, letterSpacing: -0.5))),
                TextSpan(text: 'agrônomo', style: CeresType.serif(const TextStyle(
                    fontSize: 28, fontWeight: FontWeight.w400, fontStyle: FontStyle.italic,
                    color: CeresColors.leafDeep, letterSpacing: -0.5))),
                TextSpan(text: '\nparceiro Ceres.', style: CeresType.serif(const TextStyle(
                    fontSize: 28, fontWeight: FontWeight.w500, height: 1.05,
                    color: CeresColors.ink, letterSpacing: -0.5))),
              ])),
              const SizedBox(height: 10),
              Text(
                'O caderno de campo do produtor é a sua sala de espera. '
                'Apareça na cabeça de quem precisa de você.',
                style: CeresType.serif(const TextStyle(
                    fontSize: 13.5, fontStyle: FontStyle.italic, height: 1.4,
                    color: CeresColors.ink2)),
              ),
              const SizedBox(height: 20),
              _benefit(Icons.travel_explore, 'Visibilidade regional',
                  'Produtores do seu município veem você quando o diagnóstico exige um humano.'),
              _benefit(Icons.chat_bubble_outline, 'Linha direta com o campo',
                  'Receba contatos qualificados via WhatsApp — com o diagnóstico do app já anexado.'),
              _benefit(Icons.insights, 'Painel de acompanhamento',
                  'Histórico dos casos atendidos, doenças mais frequentes na sua região.'),
            ],
          )),
          Padding(
            padding: const EdgeInsets.fromLTRB(22, 0, 22, 14),
            child: Column(children: [
              FilledButton(
                onPressed: () => Navigator.pushNamed(context, '/cadastro'),
                child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  Text('Cadastrar-se como agrônomo'),
                  SizedBox(width: 8),
                  Icon(Icons.arrow_forward, size: 18),
                ]),
              ),
              const SizedBox(height: 8),
              Text('ENVIO ANÁLISE CREA · RESPOSTA EM 48 H', style: CeresType.label),
            ]),
          ),
        ]),
      ),
    );
  }

  Widget _benefit(IconData icon, String titulo, String desc) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 14),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(width: 32, height: 32, margin: const EdgeInsets.only(top: 2),
          decoration: BoxDecoration(
            color: CeresColors.paper2, shape: BoxShape.circle,
            border: Border.all(color: CeresColors.hairline)),
          child: Icon(icon, size: 16, color: CeresColors.leafDeep),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(titulo, style: CeresType.serif(const TextStyle(
              fontSize: 14, fontWeight: FontWeight.w500, color: CeresColors.ink))),
          const SizedBox(height: 2),
          Text(desc, style: CeresType.sans(const TextStyle(
              fontSize: 11, height: 1.35, color: CeresColors.ink2))),
        ])),
      ]),
    );
  }
}
