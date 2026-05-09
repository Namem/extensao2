# Background Augmentation — Relatorio de Execucao

**Data:** 2026-05-08 23:25
**Modelo rembg:** u2net
**Composicoes por imagem:** 2
**Sample:** 10
**Duracao:** 0m 52s

## Estrategia

Baseado em Singh et al. (2020): remocao de fundo no PlantDoc
aumentou acuracia de 29,73% para 70,53% (+40,8 pp).
Aqui aplicamos a estrategia inversa: inserimos fundos naturais
nas imagens PlantVillage para o modelo aprender a ignorar o fundo.

## Resultado por Classe

| Classe | Imgs fonte | Composicoes | Puladas | Erros |
|---|---|---|---|---|
| D01_requeima | 10 | 20 | 0 | 0 |
| D02_septoriose | 10 | 20 | 0 | 0 |
| D03_pinta_preta | 10 | 20 | 0 | 0 |
| D03b_mancha_alvo | 10 | 20 | 0 | 0 |
| D05_mofo_foliar | 10 | 20 | 0 | 0 |
| D06_vira_cabeca | 10 | 20 | 0 | 0 |
| D06b_mosaico | 10 | 20 | 0 | 0 |
| D07_acaro_bronzeamento | 10 | 20 | 0 | 0 |
| D09_mancha_bacteriana | 10 | 20 | 0 | 0 |
| saudavel | 10 | 20 | 0 | 0 |

## Resultado Geral

| Metrica | Valor |
|---|---|
| Total imagens fonte | 100 |
| Total composicoes geradas | 200 |
| Total erros | 0 |
| Tempo total | 0m 52s |

## Proximo Passo

Retreinar o modelo com o dataset augmentado:

```bash
# No WSL2, com o novo dataset:
python train_local.py --data-dir datasets/processed_field
```

Em seguida, rodar novamente a avaliacao PlantDoc:

```bash
python avaliar_plantdoc.py
```
