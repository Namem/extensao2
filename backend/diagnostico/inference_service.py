"""
inference_service.py — Serviço de inferência TFLite para o backend Django.

Carrega o modelo uma vez na inicialização e expõe `inferir(imagem_bytes)`.
Usa ai-edge-litert (substituto oficial do tflite-runtime).
"""

import io
import time
import numpy as np
from pathlib import Path
from PIL import Image

# ai-edge-litert é o novo nome do tflite-runtime (Google, 2024)
from ai_edge_litert.interpreter import Interpreter

# Classes na mesma ordem do treino (diretórios ordenados alfabeticamente)
CLASS_NAMES = [
    "D01_requeima",
    "D02_septoriose",
    "D03_pinta_preta",
    "D03b_mancha_alvo",
    "D05_mofo_foliar",
    "D06_vira_cabeca",
    "D06b_mosaico",
    "D07_acaro_bronzeamento",
    "D09_mancha_bacteriana",
    "saudavel",
]

IMG_SIZE = 96  # modelo 96×96


class InferenciaService:
    """Singleton que mantém o interpreter TFLite carregado."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def carregar(self, modelo_path: Path):
        """Carrega o modelo TFLite. Chamar uma vez no startup."""
        self._interpreter = Interpreter(model_path=str(modelo_path))
        self._interpreter.allocate_tensors()

        self._input_details  = self._interpreter.get_input_details()
        self._output_details = self._interpreter.get_output_details()

        self._scale     = self._output_details[0]['quantization_parameters']['scales'][0]
        self._zero_pt   = self._output_details[0]['quantization_parameters']['zero_points'][0]
        self._in_scale  = self._input_details[0]['quantization_parameters']['scales'][0]
        self._in_zero   = self._input_details[0]['quantization_parameters']['zero_points'][0]

        self._loaded = True

    def inferir(self, imagem_bytes: bytes) -> dict:
        """
        Executa inferência sobre imagem bruta (JPEG/PNG/etc).

        Args:
            imagem_bytes: conteúdo binário da imagem

        Returns:
            dict com classe, confiança, latência e lista de scores
        """
        if not self._loaded:
            raise RuntimeError("Modelo não carregado. Chame carregar() primeiro.")

        # Pré-processamento: redimensionar para 96×96 RGB
        img = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
        img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)

        # uint8 → int8: normalização idêntica ao ESP32 (subtract 128)
        arr = np.array(img, dtype=np.uint8)
        arr_int8 = (arr.astype(np.int32) - 128).astype(np.int8)
        arr_int8 = arr_int8[np.newaxis, ...]  # [1, 96, 96, 3]

        # Inferência
        t0 = time.perf_counter()
        self._interpreter.set_tensor(self._input_details[0]['index'], arr_int8)
        self._interpreter.invoke()
        latencia_ms = int((time.perf_counter() - t0) * 1000)

        # Saída: dequantizar INT8 → float
        raw = self._interpreter.get_tensor(self._output_details[0]['index'])[0]
        scores_float = (raw.astype(np.float32) - self._zero_pt) * self._scale

        # Softmax
        exp = np.exp(scores_float - scores_float.max())
        probs = exp / exp.sum()

        best_idx = int(np.argmax(probs))

        return {
            "classe":      CLASS_NAMES[best_idx],
            "class_index": best_idx,
            "confianca":   float(round(probs[best_idx], 4)),
            "latencia_ms": latencia_ms,
            "scores":      {CLASS_NAMES[i]: float(round(probs[i], 4))
                            for i in range(len(CLASS_NAMES))},
        }


# Instância global (singleton)
inferencia_service = InferenciaService()
