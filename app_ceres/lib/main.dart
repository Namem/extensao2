import 'package:flutter/material.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/agronomos_screen.dart';
import 'screens/alertas_screen.dart';
import 'screens/cadastro_screen.dart';
import 'screens/camera_screen.dart';
import 'screens/enciclopedia_screen.dart';
import 'screens/esqueci_senha_screen.dart';
import 'screens/historico_screen.dart';
import 'screens/historico_local_screen.dart';
import 'screens/login_screen.dart';
import 'screens/mapa_screen.dart';
import 'screens/perfil_screen.dart';
import 'screens/seja_parceiro_screen.dart';
import 'screens/splash_screen.dart';
import 'services/auth_storage.dart';
import 'theme/ceres_theme.dart';
import 'widgets/ceres_icons.dart';

void main() {
  final binding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: binding);
  runApp(const CeresApp());
  FlutterNativeSplash.remove();
}

class CeresApp extends StatelessWidget {
  const CeresApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ceres Diagnóstico',
      debugShowCheckedModeBanner: false,
      theme: CeresTheme.theme,
      routes: {
        '/home':          (_) => const HomeScreen(),
        '/login':         (_) => const LoginScreen(),
        '/salvos':        (_) => const HistoricoLocalScreen(),
        '/alertas':       (_) => const AlertasScreen(),
        '/agronomos':     (_) => const AgronomosScreen(),
        '/seja-parceiro': (_) => const SejaParceiroScreen(),
        '/cadastro':      (_) => const CadastroScreen(),
        '/esqueci-senha': (_) => const EsqueciSenhaScreen(),
      },
      home: const _BootScreen(),
    );
  }
}

/// Decide o destino da splash conforme token salvo:
/// - Token presente → HomeScreen (pula login)
/// - Token ausente  → LoginScreen
class _BootScreen extends StatelessWidget {
  const _BootScreen();

  @override
  Widget build(BuildContext context) {
    return SplashScreen(
      destino: FutureBuilder<String?>(
        future: AuthStorage.instance.lerAccessToken(),
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) {
            return const SizedBox.shrink();
          }
          final temToken = snap.data != null && snap.data!.isNotEmpty;
          return temToken ? const HomeScreen() : const LoginScreen();
        },
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _abaSelecionada = 0;

  // Ordem exata do HTML: Diagnóstico, Mapa, IoT, Enciclopédia, Perfil
  static final _telas = [
    const CameraScreen(),
    const MapaScreen(),
    const HistoricoScreen(),
    const EnciclopediaScreen(),
    const PerfilScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _abaSelecionada,
        children: _telas,
      ),
      bottomNavigationBar: _navBar(),
    );
  }

  Widget _navBar() {
    // Tab order e ícones exatos do HTML de design
    const tabs = [
      _NavItem(svg: CeresIconsSvg.tabDiagnostico, label: 'Diagnóstico'),
      _NavItem(svg: CeresIconsSvg.tabMapa,        label: 'Mapa'),
      _NavItem(svg: CeresIconsSvg.tabIot,         label: 'IoT'),
      _NavItem(svg: CeresIconsSvg.tabEnciclopedia, label: 'Enciclopédia'),
      _NavItem(svg: CeresIconsSvg.tabPerfil,      label: 'Perfil'),
    ];

    return Container(
      decoration: const BoxDecoration(
        border: Border(top: BorderSide(color: CeresColors.hairline, width: 1)),
        color: CeresColors.paper2,
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          height: 60,
          child: Row(
            children: List.generate(tabs.length, (i) {
              final sel = _abaSelecionada == i;
              final color = sel ? CeresColors.leafDeep : CeresColors.ink3;
              return Expanded(
                child: GestureDetector(
                  behavior: HitTestBehavior.opaque,
                  onTap: () => setState(() => _abaSelecionada = i),
                  child: Column(
                    children: [
                      // Linha indicadora no topo (2px leafDeep quando ativo)
                      Container(
                        height: 2,
                        width: 18,
                        color: sel ? CeresColors.leafDeep : Colors.transparent,
                      ),
                      Expanded(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            CeresSvgIcon(
                              svgString: tabs[i].svg,
                              color: color,
                              size: 17,
                            ),
                            const SizedBox(height: 3),
                            Text(
                              tabs[i].label,
                              style: GoogleFonts.ibmPlexSans(
                                fontSize: 8.5,
                                letterSpacing: 0.04,
                                color: color,
                                fontWeight: sel
                                    ? FontWeight.w500
                                    : FontWeight.w400,
                              ),
                              overflow: TextOverflow.ellipsis,
                              maxLines: 1,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              );
            }),
          ),
        ),
      ),
    );
  }
}

class _NavItem {
  final String svg;
  final String label;
  const _NavItem({required this.svg, required this.label});
}

