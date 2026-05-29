import 'package:flutter/material.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/camera_screen.dart';
import 'screens/historico_screen.dart';
import 'screens/historico_local_screen.dart';
import 'theme/ceres_theme.dart';

void main() {
  final binding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: binding);
  runApp(const CeresApp());
}

class CeresApp extends StatelessWidget {
  const CeresApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ceres Diagnóstico',
      debugShowCheckedModeBanner: false,
      theme: CeresTheme.theme,
      home: const HomeScreen(),
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
    WidgetsBinding.instance.addPostFrameCallback((_) {
      FlutterNativeSplash.remove();
    });
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
    return Container(
      decoration: const BoxDecoration(
        border: Border(
          top: BorderSide(color: CeresColors.hairline, width: 0.8),
        ),
        color: CeresColors.paper,
      ),
      child: NavigationBar(
        selectedIndex: _abaSelecionada,
        onDestinationSelected: (i) => setState(() => _abaSelecionada = i),
        backgroundColor: CeresColors.paper,
        indicatorColor: CeresColors.leafDeep.withValues(alpha: 0.12),
        labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
        destinations: [
          _dest(
            icon: Icons.camera_alt_outlined,
            selIcon: Icons.camera_alt,
            label: 'Diagnóstico',
          ),
          _dest(
            icon: Icons.sensors_outlined,
            selIcon: Icons.sensors,
            label: 'IoT',
          ),
          _dest(
            icon: Icons.save_outlined,
            selIcon: Icons.save,
            label: 'Salvo',
          ),
          _dest(
            icon: Icons.map_outlined,
            selIcon: Icons.map,
            label: 'Mapa',
          ),
          _dest(
            icon: Icons.menu_book_outlined,
            selIcon: Icons.menu_book,
            label: 'Guia',
          ),
        ],
      ),
    );
  }

  NavigationDestination _dest({
    required IconData icon,
    required IconData selIcon,
    required String label,
  }) {
    return NavigationDestination(
      icon: Icon(icon),
      selectedIcon: Icon(selIcon),
      label: label,
    );
  }
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
