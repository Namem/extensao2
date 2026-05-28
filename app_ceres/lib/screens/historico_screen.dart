import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/evento_mqtt.dart';
import '../services/api_service.dart';

class HistoricoScreen extends StatefulWidget {
  const HistoricoScreen({super.key});

  @override
  State<HistoricoScreen> createState() => _HistoricoScreenState();
}

class _HistoricoScreenState extends State<HistoricoScreen> {
  List<EventoMqtt> _eventos = [];
  bool _carregando = false;
  String? _erro;
  int _paginaAtual = 1;
  bool _temProxima = false;
  int _total = 0;

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  Future<void> _carregar({int pagina = 1}) async {
    setState(() {
      _carregando = true;
      _erro = null;
    });
    try {
      final data = await ApiService.instance.historico(page: pagina);
      setState(() {
        _eventos = data['results'] as List<EventoMqtt>;
        _temProxima = data['next'] != null;
        _total = data['count'] as int;
        _paginaAtual = pagina;
      });
    } catch (e) {
      setState(() => _erro = e.toString());
    } finally {
      setState(() => _carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ESP32 · $_total eventos'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _carregando ? null : () => _carregar(),
          ),
        ],
      ),
      body: _body(),
      bottomNavigationBar: _paginacao(),
    );
  }

  Widget _body() {
    if (_carregando) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_erro != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.wifi_off, size: 64, color: Colors.grey[400]),
            const SizedBox(height: 12),
            Text('Sem conexão com o servidor',
                style: TextStyle(color: Colors.grey[600], fontSize: 16)),
            const SizedBox(height: 4),
            Text(_erro!, style: const TextStyle(fontSize: 12, color: Colors.red)),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.refresh),
              label: const Text('Tentar novamente'),
              onPressed: () => _carregar(),
            ),
          ],
        ),
      );
    }
    if (_eventos.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox, size: 64, color: Colors.grey),
            SizedBox(height: 8),
            Text('Nenhum evento MQTT recebido ainda.',
                style: TextStyle(color: Colors.grey)),
          ],
        ),
      );
    }
    return RefreshIndicator(
      onRefresh: () => _carregar(),
      child: ListView.separated(
        padding: const EdgeInsets.all(12),
        itemCount: _eventos.length,
        separatorBuilder: (context, index) => const SizedBox(height: 6),
        itemBuilder: (context, i) => _cartaoEvento(_eventos[i]),
      ),
    );
  }

  Widget _cartaoEvento(EventoMqtt e) {
    final isSaudavel = e.classe == 'saudavel';
    final baixaConfianca = e.confianca < 0.40;
    final Color cor = isSaudavel
        ? const Color(0xFF2E7D32)
        : (baixaConfianca ? const Color(0xFFE65100) : const Color(0xFFC62828));
    String tsFormatado = e.timestamp;
    try {
      final dt = DateTime.parse(e.timestamp).toLocal();
      tsFormatado = DateFormat('dd/MM/yyyy HH:mm').format(dt);
    } catch (e) {
      debugPrint('Timestamp inválido: $e');
    }

    return Card(
      child: ListTile(
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        leading: CircleAvatar(
          backgroundColor: cor.withValues(alpha: 0.12),
          child: Icon(
            isSaudavel ? Icons.check : Icons.warning_amber_rounded,
            color: cor,
            size: 20,
          ),
        ),
        title: Text(
          e.rotulo,
          style:
              TextStyle(fontWeight: FontWeight.w600, color: cor, fontSize: 14),
        ),
        subtitle: Text(
          'dev: ${e.deviceId}  ·  $tsFormatado',
          style: const TextStyle(fontSize: 11, color: Color(0xFF888880)),
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              '${(e.confianca * 100).toStringAsFixed(0)}%',
              style: TextStyle(
                  fontWeight: FontWeight.w700, color: cor, fontSize: 16),
            ),
            Text('${e.latenciaMs} ms',
                style: const TextStyle(
                    fontSize: 11, color: Color(0xFFAAAAAA))),
          ],
        ),
      ),
    );
  }

  Widget? _paginacao() {
    if (_eventos.isEmpty && _erro == null && !_carregando) return null;
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          TextButton.icon(
            icon: const Icon(Icons.chevron_left),
            label: const Text('Anterior'),
            onPressed: (_paginaAtual > 1 && !_carregando)
                ? () => _carregar(pagina: _paginaAtual - 1)
                : null,
          ),
          Text('Página $_paginaAtual'),
          TextButton.icon(
            icon: const Icon(Icons.chevron_right),
            label: const Text('Próxima'),
            onPressed: (_temProxima && !_carregando)
                ? () => _carregar(pagina: _paginaAtual + 1)
                : null,
          ),
        ],
      ),
    );
  }
}
