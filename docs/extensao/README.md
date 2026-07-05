# Relatório Final — Atividade de Extensão II (Ceres Diagnóstico)

Pacote de entrega da disciplina. **O relatório é autocontido** — toda a documentação
técnica (diagramas, API, manuais, backlog) está reproduzida dentro dele.

## Entregável principal
- **[relatorio_final_extensao.pdf](relatorio_final_extensao.pdf)** — versão final para entrega
- **[relatorio_final_extensao.docx](relatorio_final_extensao.docx)** — versão editável (Word)
- [RELATORIO_FINAL_EXTENSAO.md](RELATORIO_FINAL_EXTENSAO.md) — resumo em Markdown

## Estrutura da pasta
```
extensao/
├─ relatorio_final_extensao.pdf / .docx     ← ENTREGÁVEL (autocontido)
├─ RELATORIO_FINAL_EXTENSAO.md
├─ anexos/                                   ← material de apoio
│  ├─ diagramas/    casos_de_uso · arquitetura · diagrama_classes · mer · roadmap (png/svg)
│  ├─ backlog_produto_ceres.xlsx
│  ├─ BACKLOG_PRODUTO.md
│  ├─ API_CERES.md · MANUAL_INSTALACAO.md · MANUAL_USUARIO.md
├─ assets/
│  ├─ screenshots/  12 telas do app (renderizadas do protótipo)
│  └─ fotos_hardware/  fotos do ESP32-S3, sensores e testes
├─ slides/          apresentação Sprint MVP + roteiro
└─ fontes/          scripts geradores (Python + Node)
```

## Como regenerar
```bash
cd fontes
python gen_diagramas.py && node render.js   # diagramas (anexos/diagramas)
python gen_backlog_xlsx.py                   # backlog (anexos)
python gen_relatorio_pdf.py                  # relatório PDF
python gen_relatorio_docx.py                 # relatório DOCX
```
O conteúdo do relatório vive em `fontes/relatorio_conteudo.py` (fonte única — alimenta
PDF e DOCX). Editar lá e rodar os dois geradores mantém os formatos sincronizados.

## Mapa relatório × seções do guia
| Seção do guia | Onde está |
|---|---|
| 1–3 (Identificação, Resumo, Visão) | Relatório, seções 1–3 |
| 4 Roadmap / Backlog | Relatório §4 + `anexos/backlog_produto_ceres.xlsx` |
| 5 Gestão e Tecnologias | Relatório §5 |
| 6 Desenvolvimento (todas as tarefas por sprint) | Relatório §6 |
| 7 Resultados | Relatório §7 (telas + métricas + limitações) |
| 8.1–8.3 GitHub / Slides / Fotos | Relatório §8 + `slides/` + `assets/` |
| 8.4 Documentação técnica (diagramas, API, manuais) | Relatório §8.4 (embutido) |
