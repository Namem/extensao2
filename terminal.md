Avaliando no test set...

=======================================================
RESULTADO FINAL — Experimento E
Acurácia test set : 98.43%
Macro F1 test set : 0.9791
INT8              : 638.1 KB → /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/modelo/ceres_expe_int8.tflite
Relatório         : /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/modelo/relatorio_expe.txt
=======================================================

Próximo passo: rodar os 3 avaliadores de campo sequencialmente.
  python3 datasets/scripts/avaliar_plantdoc.py
  python3 datasets/scripts/avaliar_tomatovillage.py
  python3 datasets/scripts/avaliar_daffodil.py

  (venv_ceres) namem@DESKTOP-2UU9SQN:/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend$ python3 datasets/scripts/avaliar_plantdoc.py     --modelo ceres_expe_int8.tflite
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1778591063.462767  226320 cpu_feature_guard.cc:227] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
Carregando modelo: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/modelo/ceres_expe_int8.tflite
/home/namem/venv_ceres/lib/python3.12/site-packages/tensorflow/lite/python/interpreter.py:457: UserWarning:     Warning: tf.lite.Interpreter is deprecated and is scheduled for deletion in
    TF 2.20. Please use the LiteRT interpreter from the ai_edge_litert package.
    See the [migration guide](https://ai.google.dev/edge/litert/migration)
    for details.
    
  warnings.warn(_INTERPRETER_DELETION_WARNING)
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
Input shape : [ 1 96 96  3]  dtype: <class 'numpy.int8'>
Output shape: [ 1 10]  dtype: <class 'numpy.int8'>
Escala: 0.007843137718737125  Zero-point: -1
Classes: ['D01_requeima', 'D02_septoriose', 'D03_pinta_preta', 'D03b_mancha_alvo', 'D05_mofo_foliar', 'D06_vira_cabeca', 'D06b_mosaico', 'D07_acaro_bronzeamento', 'D09_mancha_bacteriana', 'saudavel']

Avaliando imagens em: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/raw/plantdoc (splits: ['train', 'test'])
  D01_requeima                         78/111  70.3%
  D02_septoriose                       95/151  62.9%
  D03_pinta_preta                      46/88   52.3%
  D05_mofo_foliar                      77/91   84.6%
  D06_vira_cabeca                      64/76   84.2%
  D06b_mosaico                         37/54   68.5%
  D07_acaro_bronzeamento                1/2    50.0%
  D09_mancha_bacteriana                71/110  64.5%
  saudavel                             36/63   57.1%

==================================================
Acuracia geral PlantDoc (campo real): 67.69%
Total imagens avaliadas: 746
Erros de leitura: 0
==================================================

Resultado salvo em: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/docs/resultados/plantdoc_results.md

(venv_ceres) namem@DESKTOP-2UU9SQN:/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend$ python3 datasets/scripts/avaliar_tomatovillage.py --modelo ceres_expe_int8.tflite
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1778591113.349059  226379 cpu_feature_guard.cc:227] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
Carregando modelo: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/modelo/ceres_expe_int8.tflite
/home/namem/venv_ceres/lib/python3.12/site-packages/tensorflow/lite/python/interpreter.py:457: UserWarning:     Warning: tf.lite.Interpreter is deprecated and is scheduled for deletion in
    TF 2.20. Please use the LiteRT interpreter from the ai_edge_litert package.
    See the [migration guide](https://ai.google.dev/edge/litert/migration)
    for details.
    
  warnings.warn(_INTERPRETER_DELETION_WARNING)
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
Input shape : [ 1 96 96  3]  dtype: <class 'numpy.int8'>
Output shape: [ 1 10]  dtype: <class 'numpy.int8'>
Escala: 0.007843137718737125  Zero-point: -1
Classes Ceres: ['D01_requeima', 'D02_septoriose', 'D03_pinta_preta', 'D03b_mancha_alvo', 'D05_mofo_foliar', 'D06_vira_cabeca', 'D06b_mosaico', 'D07_acaro_bronzeamento', 'D09_mancha_bacteriana', 'saudavel']
Splits a avaliar: ['test']

Dataset Tomato-Village: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/raw/tomato_village
  D01_requeima                         52/92   56.5%
    → D01_requeima: 52
    → D09_mancha_bacteriana: 19
    → D03_pinta_preta: 9
  D03_pinta_preta                       4/50   8.0%
    → D01_requeima: 27
    → D06_vira_cabeca: 8
    → D02_septoriose: 6
  D06_vira_cabeca                       3/53   5.7%
    → D01_requeima: 29
    → D09_mancha_bacteriana: 9
    → D02_septoriose: 8
  saudavel                              1/22   4.5%
    → D01_requeima: 12
    → D06_vira_cabeca: 7
    → D02_septoriose: 1

=======================================================
Acurácia geral Tomato-Village (campo real): 27.65%
Total imagens avaliadas: 217
Erros de leitura: 0
Splits avaliados: ['test']
=======================================================

Resultado salvo em: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/docs/resultados/tomatovillage_results.md
(venv_ceres) namem@DESKTOP-2UU9SQN:/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend$ 
(venv_ceres) namem@DESKTOP-2UU9SQN:/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend$ python3 datasets/scripts/avaliar_daffodil.py      --modelo ceres_expe_int8.tflite
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1778591134.336653  226433 cpu_feature_guard.cc:227] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
Carregando modelo: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/modelo/ceres_expe_int8.tflite
/home/namem/venv_ceres/lib/python3.12/site-packages/tensorflow/lite/python/interpreter.py:457: UserWarning:     Warning: tf.lite.Interpreter is deprecated and is scheduled for deletion in
    TF 2.20. Please use the LiteRT interpreter from the ai_edge_litert package.
    See the [migration guide](https://ai.google.dev/edge/litert/migration)
    for details.
    
  warnings.warn(_INTERPRETER_DELETION_WARNING)
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
Input : [ 1 96 96  3]  dtype=<class 'numpy.int8'>
Output: [ 1 10]  dtype=<class 'numpy.int8'>
Classes Ceres: ['D01_requeima', 'D02_septoriose', 'D03_pinta_preta', 'D03b_mancha_alvo', 'D05_mofo_foliar', 'D06_vira_cabeca', 'D06b_mosaico', 'D07_acaro_bronzeamento', 'D09_mancha_bacteriana', 'saudavel']

Dataset: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/raw/daffodil_bd/Tomato leaf diseases/Tomato Leaf
Classes avaliadas: ['Late Blight', 'Leaf Mold', 'Early Blight', 'Spider Mites', 'Tomato Leaf Curl Virus', 'Bacterial Spot', 'Healthy']

  D01_requeima                         68/166  41.0%
    → D09_mancha_bacteriana: 86
    → D01_requeima: 68
    → D03_pinta_preta: 6
  D05_mofo_foliar                      29/66   43.9%
    → D09_mancha_bacteriana: 33
    → D05_mofo_foliar: 29
    → D02_septoriose: 2
  D03_pinta_preta                      11/204  5.4%
    → D01_requeima: 91
    → D09_mancha_bacteriana: 82
    → D02_septoriose: 13
  D07_acaro_bronzeamento                0/307  0.0%
    → D05_mofo_foliar: 153
    → D09_mancha_bacteriana: 105
    → D01_requeima: 44
  D06_vira_cabeca                       0/394  0.0%
    → D01_requeima: 259
    → D09_mancha_bacteriana: 63
    → D05_mofo_foliar: 46
  D09_mancha_bacteriana               137/376  36.4%
    → D01_requeima: 172
    → D09_mancha_bacteriana: 137
    → D05_mofo_foliar: 31
  saudavel                             48/103  46.6%
    → saudavel: 48
    → D01_requeima: 25
    → D05_mofo_foliar: 22

=======================================================
Acurácia geral Daffodil BD (campo real): 18.13%
Total imagens avaliadas: 1616
Erros de leitura: 0
=======================================================

Resultado salvo em: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/docs/resultados/daffodil_results.md
(venv_ceres) namem@DESKTOP-2UU9SQN:/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend$ 

(venv_ceres) namem@DESKTOP-2UU9SQN:/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend$ python3 datasets/scripts/avaliar_plantdoc.py 
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1778591441.689149  226503 cpu_feature_guard.cc:227] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
Carregando modelo: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/modelo/ceres_mobilenetv2_int8.tflite
/home/namem/venv_ceres/lib/python3.12/site-packages/tensorflow/lite/python/interpreter.py:457: UserWarning:     Warning: tf.lite.Interpreter is deprecated and is scheduled for deletion in
    TF 2.20. Please use the LiteRT interpreter from the ai_edge_litert package.
    See the [migration guide](https://ai.google.dev/edge/litert/migration)
    for details.
    
  warnings.warn(_INTERPRETER_DELETION_WARNING)
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
Input shape : [ 1 96 96  3]  dtype: <class 'numpy.int8'>
Output shape: [ 1 10]  dtype: <class 'numpy.int8'>
Escala: 0.007843137718737125  Zero-point: -1
Classes: ['D01_requeima', 'D02_septoriose', 'D03_pinta_preta', 'D03b_mancha_alvo', 'D05_mofo_foliar', 'D06_vira_cabeca', 'D06b_mosaico', 'D07_acaro_bronzeamento', 'D09_mancha_bacteriana', 'saudavel']

Avaliando imagens em: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/raw/plantdoc (splits: ['train', 'test'])
  D01_requeima                         99/111  89.2%
  D02_septoriose                      140/151  92.7%
  D03_pinta_preta                      82/88   93.2%
  D05_mofo_foliar                      82/91   90.1%
  D06_vira_cabeca                      72/76   94.7%
  D06b_mosaico                         39/54   72.2%
  D07_acaro_bronzeamento                2/2    100.0%
  D09_mancha_bacteriana                95/110  86.4%
  saudavel                             49/63   77.8%

==================================================
Acuracia geral PlantDoc (campo real): 88.47%
Total imagens avaliadas: 746
Erros de leitura: 0
==================================================

Resultado salvo em: /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/docs/resultados/plantdoc_results.md