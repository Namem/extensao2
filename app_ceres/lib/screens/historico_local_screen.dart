import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../database/database.dart';
import '../models/resultado_inferencia.dart';

class HistoricoLocalScreen extends StatelessWidget {
  const HistoricoLocalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnósticos Salvos'),
        backgroundColor: Colors.green[700],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_sweep_outlined),
            tooltip: 'Limpar histórico local',
            onPressed: () => _confirmarLimpeza(context),
          ),
        ],
      ),
      body: StreamBuilder<List<DiagnosticoLocal>>(
        stream: appDb.historicoStream(),
        builder: (context, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final lista = snap.data ?? [];
          if (lista.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.save_outlined, size: 64, color: Colors.grey),
                  SizedBox(height: 8),
                  Text('Nenhum diagnóstico salvo ainda.',
                      style: TextStyle(color: Colors.grey)),
                  SizedBox(height: 4),
                  Text('Os resultados são salvos automaticamente.',
                      style: TextStyle(color: Colors.grey, fontSize: 12)),
                ],
              ),
            );
          }
          return ListView.separated(
            padding: const EdgeInsets.all(12),
            itemCount: lista.length,
            separatorBuilder: (context, index) => const SizedBox(height: 6),
            itemBuilder: (context, i) => _cartao(lista[i]),
          );
        },
      ),
    );
  }

  Widget _cartao(DiagnosticoLocal d) {
    final isSaudavel = d.classe == 'saudavel';
    final cor = isSaudavel ? Colors.green : Colors.red;
    final rotulo = ResultadoInferencia.rotuloDeClasse(d.classe);
    final ts = DateFormat('dd/MM/yyyy HH:mm').format(d.timestamp.toLocal());
    final baixaConfianca = d.confianca < 0.40;

    // Decodifica scores para mostrar a barra principal
    Map<String, double> scores = {};
    try {
      final raw = jsonDecode(d.scoresJson) as Map<String, dynamic>;
      scores = raw.map((k, v) => MapEntry(k, (v as num).toDouble()));
    } catch (_) {}

    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ExpansionTile(
        leading: CircleAvatar(
          backgroundColor: cor.withValues(alpha: 0.15),
          child: Icon(
            isSaudavel ? Icons.check : Icons.warning_amber,
            color: cor,
            size: 20,
          ),
        ),
        title: Text(
          rotulo,
          style: TextStyle(fontWeight: FontWeight.bold, color: cor),
        ),
        subtitle: Text(
          '$ts  •  ${(d.confianca * 100).toStringAsFixed(1)}%'
          '${baixaConfianca ? "  ⚠ baixa" : ""}',
          style: const TextStyle(fontSize: 12),
        ),
        trailing: Text(
          '${d.latenciaMs} ms',
          style: const TextStyle(fontSize: 12, color: Colors.grey),
        ),
        children: [
          if (scores.isNotEmpty)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Scores:',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 12)),
                  const SizedBox(height: 4),
                  ..._barras(scores),
                ],
              ),
            ),
        ],
      ),
    );
  }

  List<Widget> _barras(Map<String, double> scores) {
    final sorted = scores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    return sorted.take(5).map((e) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 1),
        child: Row(
          children: [
            SizedBox(
              width: 150,
              child: Text(e.key,
                  style: const TextStyle(fontSize: 11),
                  overflow: TextOverflow.ellipsis),
            ),
            Expanded(
              child: LinearProgressIndicator(
                value: e.value.clamp(0.0, 1.0),
                backgroundColor: Colors.grey[200],
                color: Colors.green[600],
                minHeight: 6,
              ),
            ),
            const SizedBox(width: 4),
            Text('${(e.value * 100).toStringAsFixed(0)}%',
                style: const TextStyle(fontSize: 11)),
          ],
        ),
      );
    }).toList();
  }

  Future<void> _confirmarLimpeza(BuildContext context) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Limpar histórico local?'),
        content: const Text(
            'Todos os diagnósticos salvos serão removidos do dispositivo.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancelar')),
          TextButton(
              onPressed: () => Navigator.pop(context, true),
              child:
                  const Text('Limpar', style: TextStyle(color: Colors.red))),
        ],
      ),
    );
    if (ok == true) await appDb.limpar();
  }
}
