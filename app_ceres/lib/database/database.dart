/// database.dart — Banco SQLite local via Drift.
///
/// Persiste os resultados de diagnóstico offline no dispositivo.
/// Geração de código: flutter pub run build_runner build --delete-conflicting-outputs
library;

import 'dart:io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

part 'database.g.dart';

/// Tabela de diagnósticos salvos localmente.
@DataClassName('DiagnosticoLocal')
class DiagnosticosLocais extends Table {
  /// ID auto-incrementado.
  IntColumn get id => integer().autoIncrement()();

  /// Data/hora da inferência.
  DateTimeColumn get timestamp => dateTime()();

  /// Código da classe predita (ex: D01_requeima).
  TextColumn get classe => text()();

  /// Confiança entre 0.0 e 1.0.
  RealColumn get confianca => real()();

  /// Latência da API em milissegundos.
  IntColumn get latenciaMs => integer()();

  /// Scores de todas as classes em JSON (ex: {"D01_requeima": 0.87, ...}).
  TextColumn get scoresJson => text()();

  /// Caminho local da imagem usada (nullable — pode não estar disponível).
  TextColumn get imagemPath => text().nullable()();

  /// Coordenadas GPS no momento do diagnóstico (nullable — GPS pode estar indisponível).
  RealColumn get latitude => real().nullable()();
  RealColumn get longitude => real().nullable()();

  /// Se o diagnóstico já foi sincronizado com o servidor.
  /// false = pendente de envio (diagnóstico feito offline).
  BoolColumn get sincronizado => boolean().withDefault(const Constant(true))();

  /// Modo usado: 'local' (TFLite) ou 'cloud' (API Django).
  TextColumn get modo => text().withDefault(const Constant('cloud'))();
}

@DriftDatabase(tables: [DiagnosticosLocais])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_abrirConexao());

  @override
  int get schemaVersion => 3;

  @override
  MigrationStrategy get migration => MigrationStrategy(
    onUpgrade: (migrator, from, to) async {
      if (from < 2) {
        await migrator.addColumn(diagnosticosLocais, diagnosticosLocais.latitude);
        await migrator.addColumn(diagnosticosLocais, diagnosticosLocais.longitude);
      }
      if (from < 3) {
        // v3: fila de sincronização offline
        await migrator.addColumn(diagnosticosLocais, diagnosticosLocais.sincronizado);
        await migrator.addColumn(diagnosticosLocais, diagnosticosLocais.modo);
      }
    },
  );

  /// Retorna os últimos [limite] diagnósticos, do mais recente ao mais antigo.
  Future<List<DiagnosticoLocal>> historico({int limite = 100}) =>
      (select(diagnosticosLocais)
            ..orderBy([(t) => OrderingTerm.desc(t.timestamp)])
            ..limit(limite))
          .get();

  /// Stream reativo — atualiza a UI automaticamente quando há novo registro.
  Stream<List<DiagnosticoLocal>> historicoStream({int limite = 100}) =>
      (select(diagnosticosLocais)
            ..orderBy([(t) => OrderingTerm.desc(t.timestamp)])
            ..limit(limite))
          .watch();

  /// Salva um diagnóstico e retorna o id gerado.
  Future<int> salvar(DiagnosticosLocaisCompanion entry) =>
      into(diagnosticosLocais).insert(entry);

  /// Retorna diagnósticos pendentes de sincronização.
  Future<List<DiagnosticoLocal>> pendentes() =>
      (select(diagnosticosLocais)
            ..where((t) => t.sincronizado.equals(false))
            ..orderBy([(t) => OrderingTerm.asc(t.timestamp)]))
          .get();

  /// Marca um diagnóstico como sincronizado.
  Future<void> marcarSincronizado(int id) =>
      (update(diagnosticosLocais)..where((t) => t.id.equals(id)))
          .write(const DiagnosticosLocaisCompanion(sincronizado: Value(true)));

  /// Total de diagnósticos armazenados.
  Future<int> total() async {
    final count = diagnosticosLocais.id.count();
    final query = selectOnly(diagnosticosLocais)..addColumns([count]);
    final row = await query.getSingle();
    return row.read(count) ?? 0;
  }

  /// Total de pendentes de sincronização.
  Future<int> totalPendentes() async {
    final count = diagnosticosLocais.id.count();
    final query = selectOnly(diagnosticosLocais)
      ..addColumns([count])
      ..where(diagnosticosLocais.sincronizado.equals(false));
    final row = await query.getSingle();
    return row.read(count) ?? 0;
  }

  /// Remove todos os registros locais.
  Future<void> limpar() => delete(diagnosticosLocais).go();
}

/// Singleton global — uma única instância do banco para o app inteiro.
final appDb = AppDatabase();

/// Abre (ou cria) o arquivo SQLite no diretório de documentos do app.
LazyDatabase _abrirConexao() {
  return LazyDatabase(() async {
    final dir = await getApplicationDocumentsDirectory();
    final file = File(p.join(dir.path, 'ceres.db'));
    return NativeDatabase.createInBackground(file);
  });
}
