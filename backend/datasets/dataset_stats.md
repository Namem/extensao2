        # Dataset Stats — PlantVillage (Tomate)
        **Gerado em:** 2026-04-28
        **Projeto:** Ceres Diagnóstico — TCC IFMT Cuiabá

        ## Resumo

        | Métrica               | Valor       |
        |-----------------------|-------------|
        | Classes               | 10 |
        | Imagens originais     | 18160 |
        | Treino (originais)    | 12707 |
        | Augmentações geradas  | 76242 |
        | Treino total          | 88949 |
        | Validação             | 2719 |
        | Teste                 | 2734 |
        | Split                 | 70 / 15 / 15 |
        | Seed                  | 42 |

        ## Por Classe

        | Classe                              | Original | Train   | Aug (+) | Train total  | Val   | Test  |
        |-------------------------------------|----------|---------|---------|--------------|-------|-------|
        | D01_requeima                        |     1909 |    1336 |       8016 |          9352 |   286 |   287 |
| D02_septoriose                      |     1771 |    1239 |       7434 |          8673 |   265 |   267 |
| D03_pinta_preta                     |     1000 |     700 |       4200 |          4900 |   150 |   150 |
| D03b_mancha_alvo                    |     1404 |     982 |       5892 |          6874 |   210 |   212 |
| D05_mofo_foliar                     |      952 |     666 |       3996 |          4662 |   142 |   144 |
| D06_vira_cabeca                     |     5357 |    3749 |      22494 |         26243 |   803 |   805 |
| D06b_mosaico                        |      373 |     261 |       1566 |          1827 |    55 |    57 |
| D07_acaro_bronzeamento              |     1676 |    1173 |       7038 |          8211 |   251 |   252 |
| D09_mancha_bacteriana               |     2127 |    1488 |       8928 |         10416 |   319 |   320 |
| saudavel                            |     1591 |    1113 |       6678 |          7791 |   238 |   240 |
        | **TOTAL**                           | **18160** | **12707** | **76242** | **88949** | **2719** | **2734** |

        ## Alertas

        _Nenhum alerta._

        ## Augmentations aplicadas (somente treino)

        | Operação     | Descrição                         |
        |--------------|-----------------------------------|
        | flip_h       | Espelhamento horizontal           |
        | flip_v       | Espelhamento vertical             |
        | rot_p15      | Rotação +15°                      |
        | rot_m15      | Rotação −15°                      |
        | bright_p     | Brilho +20%                       |
        | bright_m     | Brilho −20%                       |
