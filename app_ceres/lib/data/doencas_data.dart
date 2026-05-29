import 'package:flutter/material.dart';
import '../theme/ceres_theme.dart';

/// Dados estáticos das 10 classes do Ceres — compartilhado entre
/// CameraScreen e EnciclopediaScreen.
/// Fonte: Embrapa Hortaliças, Manual de Pragas e Doenças do Tomateiro (2023).
class DoencaInfo {
  final String codigo;
  final String nomePopular;
  final String nomeLatim;
  final String tipoAgente;
  final Color corAgente;
  // Descrição técnica — 2-3 frases sobre sintomas visuais
  final String descricao;
  // Ação de manejo Embrapa — 3-4 passos
  final String acao;
  final String urgencia;
  // Condições que favorecem o problema
  final String condicoes;
  // Partes da planta afetadas (para exibir na enciclopédia)
  final List<String> partesAfetadas;

  const DoencaInfo({
    required this.codigo,
    required this.nomePopular,
    required this.nomeLatim,
    required this.tipoAgente,
    required this.corAgente,
    required this.descricao,
    required this.acao,
    required this.urgencia,
    required this.condicoes,
    required this.partesAfetadas,
  });
}

/// Mapa completo: código Ceres → DoencaInfo
const Map<String, DoencaInfo> kDoencas = {
  // ── URGENTES ──────────────────────────────────────────────────────────────
  'D01_requeima': DoencaInfo(
    codigo: 'D01',
    nomePopular: 'Requeima',
    nomeLatim: 'Phytophthora infestans',
    tipoAgente: 'Oomiceto',
    corAgente: CeresColors.blight,
    descricao:
        'Phytophthora infestans é o patógeno mais destrutivo do tomateiro. '
        'Provoca lesões encharcadas verde-escuras na folha que evoluem rapidamente '
        'para necrose marrom com halo branco em condições de alta umidade. '
        'Em 3 a 5 dias pode destruir toda a lavoura sob temperaturas entre 10–20 °C.',
    acao:
        '1. Aplicar fungicida cúprico (oxicloreto de cobre) imediatamente.\n'
        '2. Remover e queimar todas as folhas, caules e frutos afetados.\n'
        '3. Suspender irrigação por aspersão — usar gotejamento.\n'
        '4. Aplicar fungicidas sistêmicos (metalaxil-M) a cada 5 dias até controle.',
    urgencia: 'URGENTE',
    condicoes: 'Alta umidade relativa (> 90%), temperatura entre 10–20 °C, '
        'nevoeiro noturno e orvalho frequente.',
    partesAfetadas: ['Folha', 'Caule', 'Fruto'],
  ),

  'D06_vira_cabeca': DoencaInfo(
    codigo: 'D06',
    nomePopular: 'Vira-cabeça',
    nomeLatim: 'TSWV — vetor: Frankliniella schultzei',
    tipoAgente: 'Vírus',
    corAgente: CeresColors.blight,
    descricao:
        'Tomato Spotted Wilt Virus (TSWV) é transmitido por tripes '
        '(Frankliniella schultzei e F. occidentalis). Causa bronzeamento, '
        'enrolamento das bordas das folhas para cima, manchas cloróticas '
        'anelares e tombamento dos ponteiros — daí o nome "vira-cabeça". '
        'Plantas infectadas não se recuperam.',
    acao:
        '1. Erradicar e destruir imediatamente todas as plantas com sintomas.\n'
        '2. Controlar tripes com inseticida seletivo (spinosade ou imidacloprido).\n'
        '3. Instalar armadilhas adesivas azuis para monitorar tripes.\n'
        '4. Usar variedades com gene Sw-5 (resistência ao TSWV) no próximo plantio.',
    urgencia: 'URGENTE',
    condicoes: 'Períodos secos e quentes que favorecem proliferação de tripes. '
        'Plantios próximos a outras solanáceas infectadas.',
    partesAfetadas: ['Folha', 'Broto'],
  ),

  'D06b_mosaico': DoencaInfo(
    codigo: 'D06b',
    nomePopular: 'Mosaico',
    nomeLatim: 'Tomato mosaic virus (ToMV)',
    tipoAgente: 'Vírus',
    corAgente: CeresColors.blight,
    descricao:
        'ToMV (Tobamovirus) causa padrão de mosaico claro-escuro nas folhas, '
        'bolhosidade e redução foliar. Em frutos provoca amadurecimento desigual '
        'com áreas internas acastanhadas. É transmitido mecanicamente por contato '
        'direto entre plantas, ferramentas e mãos contaminadas.',
    acao:
        '1. Erradicar plantas sintomáticas imediatamente — não compotar restos.\n'
        '2. Desinfetar ferramentas com hipoclorito de sódio 1% entre cortes.\n'
        '3. Lavar mãos com sabão antes e após manuseio das plantas.\n'
        '4. Usar sementes termotratadas (70 °C × 72 h) ou certificadas livres de vírus.',
    urgencia: 'URGENTE',
    condicoes: 'Qualquer temperatura. Transmissão mecânica facilita '
        'disseminação rápida em operações de poda e desbrota.',
    partesAfetadas: ['Folha', 'Fruto'],
  ),

  'D09_mancha_bacteriana': DoencaInfo(
    codigo: 'D09',
    nomePopular: 'Mancha Bacteriana',
    nomeLatim: 'Xanthomonas vesicatoria',
    tipoAgente: 'Bactéria',
    corAgente: CeresColors.blight,
    descricao:
        'Xanthomonas vesicatoria (Xv) provoca manchas pequenas encharcadas '
        'que evoluem para lesões necróticas escuras rodeadas por halo amarelado. '
        'Em frutos causa lesões corticosas superficiais. A bactéria sobrevive '
        'em restos culturais e sementes infectadas por até 2 anos.',
    acao:
        '1. Aplicar calda bordalesa (1%) ou cobre-oxicloreto preventivamente.\n'
        '2. Evitar irrigação por aspersão — splashing propaga a bactéria.\n'
        '3. Usar sementes tratadas com hipoclorito de cálcio 2% por 15 min.\n'
        '4. Remover restos culturais e incorporar ao solo após a colheita.',
    urgencia: 'URGENTE',
    condicoes: 'Temperatura entre 25–30 °C, chuvas frequentes e ventos fortes '
        'que facilitam o espirramento de água entre plantas.',
    partesAfetadas: ['Folha', 'Caule', 'Fruto'],
  ),

  // ── MODERADOS ─────────────────────────────────────────────────────────────
  'D02_septoriose': DoencaInfo(
    codigo: 'D02',
    nomePopular: 'Septoriose',
    nomeLatim: 'Septoria lycopersici',
    tipoAgente: 'Fungo',
    corAgente: CeresColors.dryGrass,
    descricao:
        'Septoria lycopersici forma manchas circulares de 2–4 mm com centro '
        'branco-acinzentado e bordas escuras nas folhas basais, avançando '
        'gradualmente para cima. No centro das lesões formam-se picnídios '
        '(pontos negros) com esporos que disseminam o fungo pela chuva.',
    acao:
        '1. Remover e destruir folhas infectadas, começando pelas basais.\n'
        '2. Aplicar fungicida preventivo (mancozebe ou clorotalonil).\n'
        '3. Aumentar espaçamento entre plantas para melhorar ventilação.\n'
        '4. Evitar trabalhar na lavoura com folhagem molhada.',
    urgencia: 'MODERADO',
    condicoes: 'Temperatura entre 20–25 °C, alta umidade e molhamento foliar '
        'prolongado. Favorecida por plantios adensados.',
    partesAfetadas: ['Folha'],
  ),

  'D03_pinta_preta': DoencaInfo(
    codigo: 'D03',
    nomePopular: 'Pinta Preta',
    nomeLatim: 'Alternaria solani',
    tipoAgente: 'Fungo',
    corAgente: CeresColors.dryGrass,
    descricao:
        'Alternaria solani causa lesões necróticas com anéis concêntricos '
        'característicos (aspecto de "alvo"), rodeadas por halo amarelado. '
        'Inicia nas folhas inferiores e progride. O fungo também ataca '
        'o colo (tombamento de mudas) e produz lesões em frutos próximos ao '
        'cálice.',
    acao:
        '1. Fungicida à base de mancozebe + cimoxanil a cada 7 dias.\n'
        '2. Eliminação de restos culturais (Alternaria sobrevive até 18 meses).\n'
        '3. Rotação de cultura com leguminosas por pelo menos 2 ciclos.\n'
        '4. Evitar estresse hídrico — plantas debilitadas são mais suscetíveis.',
    urgencia: 'MODERADO',
    condicoes: 'Temperatura entre 24–29 °C, períodos alternados de seco e '
        'úmido. Comum em plantas com deficiência de cálcio ou potássio.',
    partesAfetadas: ['Folha', 'Caule', 'Fruto'],
  ),

  'D03b_mancha_alvo': DoencaInfo(
    codigo: 'D03b',
    nomePopular: 'Mancha Alvo',
    nomeLatim: 'Corynespora cassiicola',
    tipoAgente: 'Fungo',
    corAgente: CeresColors.dryGrass,
    descricao:
        'Corynespora cassiicola provoca manchas de 1–3 cm com padrão '
        'de anéis concêntricos (alvo), inicialmente amareladas, depois '
        'castanho-escuras com tecido central seco. Difere da Pinta Preta '
        'por ter halo mais difuso e ocorrer em toda a copa, não apenas na base.',
    acao:
        '1. Fungicida sistêmico (azoxistrobina ou tebuconazol).\n'
        '2. Reduzir umidade relativa — melhorar ventilação na estufa.\n'
        '3. Evitar molhamento foliar por aspersão.\n'
        '4. Monitorar plantas vizinhas para evitar disseminação.',
    urgencia: 'MODERADO',
    condicoes: 'Temperatura entre 25–32 °C com alta umidade. '
        'Mais frequente em cultivos protegidos (estufa/telado).',
    partesAfetadas: ['Folha'],
  ),

  'D05_mofo_foliar': DoencaInfo(
    codigo: 'D05',
    nomePopular: 'Mofo Foliar',
    nomeLatim: 'Passalora fulva (sin. Cladosporium fulvum)',
    tipoAgente: 'Fungo',
    corAgente: CeresColors.dryGrass,
    descricao:
        'Passalora fulva causa manchas irregulares amarelo-pálidas na face '
        'superior e mofo oliváceo-acastanhado (esporodóquios) na face inferior. '
        'As folhas amarelam, enrolam e caem prematuramente. Principalmente '
        'em cultivos protegidos onde a umidade é mais alta.',
    acao:
        '1. Melhorar ventilação — abrir laterais da estufa.\n'
        '2. Fungicida à base de trifloxistrobina + tebuconazol.\n'
        '3. Reduzir umidade relativa para abaixo de 85%.\n'
        '4. Evitar excesso de adubação nitrogenada que torna as folhas mais tenras.',
    urgencia: 'MODERADO',
    condicoes: 'Umidade relativa > 85%, temperatura entre 18–24 °C. '
        'Quase exclusivo de cultivos protegidos.',
    partesAfetadas: ['Folha'],
  ),

  'D07_acaro_bronzeamento': DoencaInfo(
    codigo: 'D07',
    nomePopular: 'Ácaro Bronzeamento',
    nomeLatim: 'Aculops lycopersici',
    tipoAgente: 'Ácaro',
    corAgente: CeresColors.dryGrass,
    descricao:
        'Aculops lycopersici (ácaro do bronzeamento) é microscópico — '
        'não visível a olho nu. Suga células da epiderme causando '
        'bronzeamento, endurecimento e brilho metálico no caule e folhas. '
        'Em infestações severas provoca morte descendente da planta.',
    acao:
        '1. Acaricida à base de enxofre molhável (0,3%) em todo o dossel.\n'
        '2. Monitorar semanalmente com lupa 10× — focar caule e faces das folhas.\n'
        '3. Aumentar umidade relativa (ácaro prolifera em tempo seco e quente).\n'
        '4. Preservar predadores naturais — evitar inseticidas desnecessários.',
    urgencia: 'MODERADO',
    condicoes: 'Temperatura acima de 30 °C, baixa umidade relativa (< 50%), '
        'período seco prolongado. Surtos comuns no Cerrado no auge da seca.',
    partesAfetadas: ['Folha', 'Caule'],
  ),

  // ── SAUDÁVEL ───────────────────────────────────────────────────────────────
  'saudavel': DoencaInfo(
    codigo: 'S00',
    nomePopular: 'Saudável',
    nomeLatim: 'Solanum lycopersicum — sem patógeno detectado',
    tipoAgente: 'Normal',
    corAgente: CeresColors.leafLive,
    descricao:
        'Nenhum sinal de doença detectado pelo modelo Ceres. '
        'A folha apresenta coloração verde uniforme, superfície integra '
        'e ausência de manchas, lesões ou deformações características '
        'das 9 patologias monitoradas.',
    acao:
        '1. Manter monitoramento semanal de toda a lavoura.\n'
        '2. Adubação equilibrada (NPK + Ca + Mg) conforme análise de solo.\n'
        '3. Irrigação adequada — evitar estresse hídrico e encharcamento.\n'
        '4. Registrar imagem na plataforma para histórico de diagnósticos.',
    urgencia: 'NORMAL',
    condicoes: 'Condições sanitárias ideais. Monitorar temperatura, umidade '
        'e aparecimento de vetores (tripes, mosca-branca, ácaros).',
    partesAfetadas: ['—'],
  ),
};

/// Retorna DoencaInfo ou fallback
DoencaInfo infoDoenca(String classe) =>
    kDoencas[classe] ??
    const DoencaInfo(
      codigo: '???',
      nomePopular: 'Desconhecido',
      nomeLatim: '',
      tipoAgente: 'Desconhecido',
      corAgente: CeresColors.ink3,
      descricao:
          'Classe não reconhecida pelo banco de dados atual do Ceres.',
      acao: 'Consultar agrônomo para avaliação presencial.',
      urgencia: 'A VERIFICAR',
      condicoes: '—',
      partesAfetadas: ['—'],
    );
