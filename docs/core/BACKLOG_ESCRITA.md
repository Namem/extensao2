# Backlog de Escrita — TCC e Artigo Científico
**TCC Engenharia da Computação — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto
**Última atualização:** 2026-06-16

> Backlog exclusivo da produção escrita do TCC e do artigo científico.
> Para o produto (software + firmware), veja [BACKLOG.md](BACKLOG.md).

---

## Artigo Científico SBC — CONCLUÍDO (2026-06-16)

Duas versões em `docs/artigo_sbc/`, ambas ~98/100 na rubrica da orientadora:

- [x] **`main.tex` — versão PSI** (5 seções, conteúdo mais denso)
- [x] **`main_eniac.tex` — versão ENIAC** (6 seções, Referencial Teórico separado + keywords)
- [x] Estrutura completa (intro com lacuna+objetivo+estrutura, M&M com tabela de recursos/custo, resultados, conclusão com lições + trabalhos futuros)
- [x] Abstract (EN) + Resumo (PT); ENIAC com `\keywords`/`\palavraschave`
- [x] Figuras: arquitetura (TikZ), curvas de treino, matriz de confusão INT8
- [x] Correção float (98,13%) vs INT8 embarcado (95,76%) propagada nos dois artigos
- [x] Auditoria das 18 referências (`referencias.bib`) — 2 erros corrigidos (singh2020, gehlot2023)
- [x] Declaração de uso de IA em seção dedicada
- [ ] **Decidir evento-alvo** (PSI = disciplina; ENIAC = submissão a evento)
- [ ] (opcional) Merge na ENIAC dos 2 trechos só do PSI (colapso de classe, ESP32 vs RPi)
- [ ] **Apresentação de 30 min** (defesa) — detalhar slides `docs/slides/`
- [ ] Propagar float/INT8 (98,13% / 95,76%) para `TCC_CERES.md` e `FUNDAMENTACAO_TECNICA.md`

---

## Fase 1 — Escrita Inicial (paralela à Sprint 1 do produto)

Capítulos que não dependem de resultados experimentais — podem ser escritos desde o início.

- [ ] **Capítulo 1 — Introdução**
  - Contextualização do problema (doenças no tomateiro, impacto econômico em Sorriso-MT)
  - Objetivos geral e específicos
  - Justificativa e motivação
  - Estrutura do trabalho

- [ ] **Capítulo 2 — Revisão Bibliográfica**
  - Doenças do tomateiro e base técnica Embrapa
  - TinyML e modelos edge (MobileNetV2, TFLite Micro)
  - PlantVillage dataset (Hughes & Salathé 2015)
  - Sistemas IoT agrícolas (ESP32, MQTT, Mosquitto)
  - Trabalhos relacionados (incluir: Springer 2025 "Automated tomato leaf disease detection and alert system using IoT and TinyML")

- [ ] **Capítulo 3 — Metodologia**
  - Arquitetura geral do sistema (diagrama)
  - Pipeline de treinamento (Edge Impulse + PlantVillage)
  - Protocolo de medição de latência e RAM
  - Redigir rascunho — refinar após Sprint 2 com dados reais

---

## Fase 2 — Resultados Experimentais (após Sprint 2 do produto)

Depende dos arquivos: `docs/benchmark_results.md`, `docs/e2e_test_results.md`, `docs/benchmark_raw.csv`.

- [ ] **Capítulo 4 — Implementação e Resultados**
  - Descrição da implementação (firmware, backend, app)
  - Tabela de benchmark (latência média, p95, acurácia por classe)
  - Matriz de confusão
  - Resultados do teste end-to-end (T0→T4)
  - Salvar rascunho em `docs/tcc_capitulo4.md`

- [ ] **Seção 4 do Artigo — Metodologia Experimental** (max 600 palavras, estilo IEEE/SBC)
  - Dataset: PlantVillage, 18.160 imgs, 10 classes, split 70/15/15 + augmentation
  - Pipeline Edge Impulse: MobileNetV2 transfer learning, quantização INT8
  - Protocolo de medição no ESP32-S3
  - Salvar em `docs/artigo_secao4.md`

---

## Fase 3 — Discussão e Conclusão (após Sprint 3 do produto)

Depende dos arquivos: `docs/experiment_a_results.md`.

- [ ] **Capítulo 5 — Discussão e Conclusão**
  - Comparativo edge vs cloud (latência, acurácia, disponibilidade offline)
  - Análise de degradação com PlantDoc (campo real)
  - Limitações e trabalhos futuros
  - Conclusão geral
  - Salvar rascunho em `docs/tcc_capitulo5.md`

- [ ] **Seção 5 do Artigo — Resultados e Discussão** (max 800 palavras, estilo IEEE/SBC)
  - Tabela comparativa edge vs cloud
  - Gráfico de distribuição de latência
  - Diferencial do Ceres: sistema especialista Embrapa + TinyML + MQTT em loop único
  - Comparação com Springer 2025
  - Salvar em `docs/artigo_secao5.md`

---

## Fase 4 — Finalização e Submissão

- [ ] Revisão completa do TCC (capítulos 1–5, normas ABNT)
- [ ] Validação com orientador
- [ ] Testes de campo com produtores de Sorriso-MT (valida usabilidade real)
- [ ] Montar artigo completo (Seções 1–5) em `docs/artigo_completo.md`
- [ ] Submeter artigo para SBSI / WSCAD / ERRC
- [ ] Defesa do TCC
- [ ] Publicar Versão 1.0 nas lojas e repositórios
- [ ] Commit final + tag `v1.0-tcc` + `git push origin main --tags`

---

## Dependências entre Produto e Escrita

```
Sprint 1 do Produto  →  Fase 1 da Escrita (paralela, sem dependência)
Sprint 2 do Produto  →  Fase 2 da Escrita (benchmark + e2e disponíveis)
Sprint 3 do Produto  →  Fase 3 da Escrita (experimento edge vs cloud disponível)
Sprint 3 concluída   →  Fase 4 da Escrita (finalização + defesa)
```

---

## Resumo

| Fase | Tema | Depende de | Status |
|------|------|-----------|--------|
| Fase 1 | Introdução, Revisão, Metodologia | Nada (escrever agora) | ⏳ Pendente |
| Fase 2 | Cap. 4 + Seção 4 do Artigo | Sprint 2 do produto | ⏳ Pendente |
| Fase 3 | Cap. 5 + Seção 5 do Artigo | Sprint 3 do produto | ⏳ Pendente |
| Fase 4 | Finalização + Defesa + Submissão | Fases 1–3 | ⏳ Pendente |
