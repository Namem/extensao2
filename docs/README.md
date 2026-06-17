# docs/ — Documentação do Ceres Diagnóstico

**TCC Engenharia da Computação — IFMT Cuiabá**  
**Autor:** Namem Rachid Jaudy Neto · `namem.rachid.jaudy@gmail.com`  
**Repositório:** https://github.com/Namem/extensao2

---

## Estrutura

```
docs/
  PSI/              ← Entregas finais para a disciplina PSI
  artigo/           ← Artigo científico (LaTeX + Markdown)
  TCC/              ← Rascunho do TCC (Word + gerador)
  sprints/          ← Histórico de apresentações por sprint
  core/             ← Documentação interna de desenvolvimento
  resultados/       ← Resultados quantitativos dos experimentos
  slides_psi/       ← Scripts e assets dos slides PSI
```

---

## PSI/ — Entregas PSI (disciplina)

| Arquivo | Descrição |
|---|---|
| `slides/Ceres_Diagnostico_Defesa_PSI.pptx` | Apresentação final — 23 slides, preenchida com imagens e vídeo |
| `roteiros/roteiro_apresentacao.pdf` | Roteiro compacto de apresentação |
| `roteiros/roteiro_expandido.pdf` | Roteiro rico com notas de estudo e Q&A |
| `artigo/main_psi.tex` | Artigo desanonimizado — **usar este no Overleaf** |
| `artigo/referencias.bib` | Referências bibliográficas |
| `artigo/sbc-template.sty` + `sbc.bst` | Template SBC |
| `artigo/historico_treino.png` | Figura 2 do artigo |
| `artigo/matriz_confusao_int8.png` | Figura 3 do artigo |

---

## artigo/ — Artigo Científico

| Arquivo | Descrição |
|---|---|
| `main_blind.tex` | Versão blind para submissão em conferência |
| `artigo_ceres_psi.md` | Versão Markdown completa (para referência) |
| `referencias.bib` | Base bibliográfica completa |

> Para gerar o PDF: abrir `PSI/artigo/main_psi.tex` no Overleaf e compilar com pdfLaTeX.

---

## TCC/ — Rascunho do TCC

| Arquivo | Descrição |
|---|---|
| `TCC_CERES.docx` | Documento Word do TCC (rascunho atual) |
| `gerar_tcc_docx.js` | Script Node.js para gerar/atualizar o docx |

---

## sprints/ — Histórico de Sprints

| Pasta | Conteúdo |
|---|---|
| `sprint_2/slides/` | SprintReview 2 (com imagens) |
| `sprint_2/roteiro/` | Roteiro + resumo executivo da Sprint 2 |
| `sprint_2/scripts/` | Gerador JS da Sprint 2 |
| `sprint_2/sprint_mvp_extensao2/` | Assets completos do kit de demo Sprint 2 |

> Sprint 0: ver `Pre_arquivos/SprintReview_1_CeresDiagnostico.pptx` na raiz.

---

## core/ — Documentação Interna

| Arquivo | Descrição |
|---|---|
| `BACKLOG.md` | Estado atual de cada tarefa do produto |
| `BACKLOG_ESCRITA.md` | Tarefas de escrita do TCC e artigo |
| `RELATORIO_TECNICO.md` | Log cronológico de tudo implementado |
| `FUNDAMENTACAO_TECNICA.md` | Justificativa técnica + referências acadêmicas |
| `TCC_CERES.md` | Rascunho vivo das seções do TCC |

---

## resultados/ — Resultados dos Experimentos

| Arquivo | Descrição |
|---|---|
| `plantdoc_results.md` | Exp B–E no PlantDoc (EUA/Europa) |
| `tomatovillage_results.md` | Exp D–E no Tomato-Village (Índia) |
| `daffodil_results.md` | Exp E no Daffodil BD (Bangladesh) |
| `benchmark_esp32s3.md` | Latência medida no ESP32-S3 (692 ms) |
| `experimento_edge_vs_cloud.md` | Comparativo Edge 692 ms vs Cloud 306 ms |
| `background_augment_stats.md` | Estatísticas do Exp C (177.698 composições) |
| `matriz_confusao_int8.png` + `.json` | Matriz de confusão do modelo final |
| `acuracia_por_classe_int8.png` | Acurácia por classe do modelo INT8 |

---

## slides_psi/ — Scripts e Assets dos Slides

| Arquivo | Descrição |
|---|---|
| `scripts/gerar_roteiro.py` | Gera `roteiro_apresentacao.pdf` |
| `scripts/gerar_roteiro_expandido.py` | Gera `roteiro_expandido.pdf` (versão rica) |
| `scripts/preencher_slides.py` | Embute imagens + vídeo no PPTX |
| `assets/cls_01_*.jpg … cls_10_*.jpg` | Fotos das 10 classes (slide 7) |
| `assets/hardware_setup.jpg` | Foto do hardware ESP32 + sensores |
| `assets/app_iot.jpg` | Screenshot da tela IoT do app Flutter |
| `assets/historico_treino.png` | Curvas de treinamento |
| `assets/matriz_confusao_int8.png` | Matriz de confusão |
| `Ceres_Diagnostico_-_Defesa_PSI.pptx` | Template original (sem preenchimento) |
