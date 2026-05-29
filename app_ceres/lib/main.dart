import 'package:flutter/material.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/camera_screen.dart';
import 'screens/historico_screen.dart';
import 'screens/historico_local_screen.dart';
import 'screens/login_screen.dart';
import 'screens/splash_screen.dart';
import 'theme/ceres_theme.dart';

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
        '/home': (_) => const HomeScreen(),
        '/login': (_) => const LoginScreen(),
      },
      home: SplashScreen(destino: const LoginScreen()),
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

  static const _telas = [
    CameraScreen(),
    HistoricoScreen(),
    HistoricoLocalScreen(),
    _PlaceholderScreen(
      icon: Icons.map_outlined,
      titulo: 'Mapa de Ocorrências',
      subtitulo: 'em desenvolvimento',
    ),
    _PlaceholderScreen(
      icon: Icons.menu_book_outlined,
      titulo: 'Enciclopédia',
      subtitulo: '10 doenças catalogadas',
    ),
  ];

  @override
  void initState() {
    super.initState();
    // Native splash já foi removido no main()
  }

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
    const items = [
      _NavItem(icon: Icons.camera_alt_outlined, selIcon: Icons.camera_alt,    label: 'Diagnóstico'),
      _NavItem(icon: Icons.sensors_outlined,    selIcon: Icons.sensors,        label: 'IoT'),
      _NavItem(icon: Icons.save_outlined,       selIcon: Icons.save,           label: 'Salvo'),
      _NavItem(icon: Icons.map_outlined,        selIcon: Icons.map,            label: 'Mapa'),
      _NavItem(icon: Icons.menu_book_outlined,  selIcon: Icons.menu_book,      label: 'Guia'),
    ];

    return Container(
      decoration: const BoxDecoration(
        border: Border(top: BorderSide(color: CeresColors.hairline, width: 0.8)),
        color: CeresColors.paper2,
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          height: 60,
          child: Row(
            children: List.generate(items.length, (i) {
              final sel = _abaSelecionada == i;
              return Expanded(
                child: GestureDetector(
                  behavior: HitTestBehavior.opaque,
                  onTap: () => setState(() => _abaSelecionada = i),
                  child: Column(
                    children: [
                      // Linha indicadora no topo (igual HTML)
                      Container(
                        height: 2,
                        color: sel ? CeresColors.leafDeep : Colors.transparent,
                      ),
                      Expanded(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              sel ? items[i].selIcon : items[i].icon,
                              size: 17,
                              color: sel ? CeresColors.leafDeep : CeresColors.ink3,
                            ),
                            const SizedBox(height: 3),
                            Text(
                              items[i].label,
                              style: GoogleFonts.ibmPlexSans(
                                fontSize: 8.5,
                                letterSpacing: 0.04,
                                color: sel ? CeresColors.leafDeep : CeresColors.ink3,
                                fontWeight: sel ? FontWeight.w500 : FontWeight.w400,
                              ),
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
  final IconData icon;
  final IconData selIcon;
  final String label;
  const _NavItem({required this.icon, required this.selIcon, required this.label});
}

/// Placeholder para telas ainda não implementadas
class _PlaceholderScreen extends StatelessWidget {
  final IconData icon;
  final String titulo;
  final String subtitulo;

  const _PlaceholderScreen({
    required this.icon,
    required this.titulo,
    required this.subtitulo,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CeresColors.bone,
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 52,
              color: CeresColors.ink3.withValues(alpha: 0.35),
            ),
            const SizedBox(height: 16),
            Text(
              titulo,
              style: GoogleFonts.newsreader(
                fontSize: 20,
                color: CeresColors.ink2,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              subtitulo,
              style: GoogleFonts.ibmPlexMono(
                fontSize: 10,
                color: CeresColors.ink3,
              ),
            ),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              decoration: BoxDecoration(
                border: Border.all(
                    color: CeresColors.hairline.withValues(alpha: 0.6)),
                borderRadius: BorderRadius.circular(3),
              ),
              child: Text(
                'em breve',
                style: GoogleFonts.ibmPlexMono(
                  fontSize: 10,
                  color: CeresColors.ink3,
                  letterSpacing: 0.5,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
