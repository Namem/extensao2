#pragma once
#include <stdint.h>

/**
 * Resultado de uma inferência TFLite Micro.
 */
struct InferenceResult {
    int     class_index;       // índice da classe predita (0-9)
    float   confidence;        // confiança [0.0, 1.0]
    char    class_name[32];    // nome da classe Ceres (ex: "D01_requeima")
    int32_t latency_ms;        // tempo de inferência em ms
    bool    valid;             // false se inicialização falhou
};

/**
 * Inicializa o runtime TFLite Micro.
 * Aloca tensor arena na PSRAM (512KB).
 * Deve ser chamado uma vez no setup().
 * @return true se OK, false se falhou.
 */
bool inference_init();

/**
 * Executa inferência sobre uma imagem int8 96x96x3.
 * @param image_data  Ponteiro para array int8 [96*96*3], valores [-128,127]
 * @return InferenceResult com classe, confiança e latência
 */
InferenceResult inference_run(const int8_t* image_data);
