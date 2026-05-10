# Background Augmentation — Relatorio de Execucao

**Data:** 2026-05-09 10:16
**Modelo rembg:** u2net
**Composicoes por imagem:** 2
**Sample:** todas
**Duracao:** 650m 12s

## Estrategia

Baseado em Singh et al. (2020): remocao de fundo no PlantDoc
aumentou acuracia de 29,73% para 70,53% (+40,8 pp).
Aqui aplicamos a estrategia inversa: inserimos fundos naturais
nas imagens PlantVillage para o modelo aprender a ignorar o fundo.

## Resultado por Classe

| Classe | Imgs fonte | Composicoes | Puladas | Erros |
|---|---|---|---|---|
| D01_requeima | 9352 | 18684 | 20 | 0 |
| D02_septoriose | 8673 | 17326 | 20 | 0 |
| D03_pinta_preta | 4900 | 9780 | 20 | 0 |
| D03b_mancha_alvo | 6874 | 13728 | 20 | 0 |
| D05_mofo_foliar | 4662 | 9304 | 20 | 0 |
| D06_vira_cabeca | 26243 | 52466 | 20 | 0 |
| D06b_mosaico | 1827 | 3634 | 20 | 0 |
| D07_acaro_bronzeamento | 8211 | 16402 | 20 | 0 |
| D09_mancha_bacteriana | 10416 | 20812 | 20 | 0 |
| saudavel | 7791 | 15562 | 20 | 0 |

## Resultado Geral

| Metrica | Valor |
|---|---|
| Total imagens fonte | 88949 |
| Total composicoes geradas | 177698 |
| Total erros | 0 |
| Tempo total | 650m 12s |

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
