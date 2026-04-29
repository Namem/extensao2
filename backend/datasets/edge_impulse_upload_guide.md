        # Edge Impulse — Guia de Upload
        **Projeto:** Ceres Diagnóstico — TCC IFMT Cuiabá
        **Gerado em:** 2026-04-28

        ## Pré-requisitos

        1. Conta criada em [edgeimpulse.com](https://edgeimpulse.com)
        2. Projeto criado: `ceres-diagnostico`
        3. Edge Impulse CLI instalado:
           ```bash
           npm install -g edge-impulse-cli
           edge-impulse-daemon  # autentica e vincula ao projeto
           ```

        ## Estrutura esperada após prepare_plantvillage.py

        ```
        backend/datasets/processed/
        ├── train/
        │   ├── D01_requeima/
        │   ├── D02_septoriose/
        │   └── ...
        ├── val/
        │   └── ...
        └── test/
            └── ...
        ```

        ## Classes disponíveis (10)

        - `D01_requeima`
- `D02_septoriose`
- `D03_pinta_preta`
- `D03b_mancha_alvo`
- `D05_mofo_foliar`
- `D06_vira_cabeca`
- `D06b_mosaico`
- `D07_acaro_bronzeamento`
- `D09_mancha_bacteriana`
- `saudavel`

        ## Upload via CLI

        ```bash
        # Treino
        edge-impulse-uploader --category training \
            backend/datasets/processed/train/**/*

        # Validação
        edge-impulse-uploader --category validation \
            backend/datasets/processed/val/**/*

        # Teste (mantido local para benchmark final)
        # NÃO fazer upload do test split — usar em benchmark_esp32s3.py
        ```

        ## Configuração do Impulse no Edge Impulse Studio

        | Campo              | Valor sugerido          |
        |--------------------|-------------------------|
        | Image width        | 96 px                   |
        | Image height       | 96 px                   |
        | Resize mode        | Fit shortest axis       |
        | Color depth        | RGB                     |
        | Architecture       | MobileNetV2 96x96 0.35  |
        | Quantização        | INT8                    |
        | Target device      | ESP32-S3 (Xtensa LX7)   |

        ## Treinamento recomendado

        | Parâmetro          | Valor     |
        |--------------------|-----------|
        | Epochs             | 50        |
        | Learning rate      | 0.0005    |
        | Batch size         | 32        |
        | Data augmentation  | Desligada (já feita offline) |
        | Min accuracy alvo  | 85%       |

        ## Exportação para ESP32-S3

        1. **Deployment** → Arduino Library → Download `.zip`
        2. Mover para `firmware/esp32s3_ceres/lib/ei_ceres/`
        3. Seguir `docs/tflite_integration.md` (Sprint 2)

        ## Verificação rápida pós-upload

        ```bash
        # Confirmar contagem de amostras por label
        edge-impulse-api-client dataset summary
        ```
