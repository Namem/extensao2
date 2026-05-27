/**
 * inference.cpp — TFLite Micro engine para ESP32-S3
 *
 * Modelo: ceres_mobilenetv2_int8.tflite (MobileNetV2 0.35 INT8)
 * Entrada: int8_t [96*96*3], valores [-128,127]
 * Saída:   10 classes (logits INT8 → dequantizados para float)
 * Arena:   512KB alocada na PSRAM via ps_malloc()
 */

#include "inference.h"
#include "model_data.h"

#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/micro/micro_log.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <esp_timer.h>
#include <Arduino.h>

// ---------------------------------------------------------------------------
// Constantes
// ---------------------------------------------------------------------------
static const int kTensorArenaSize = 512 * 1024;  // 512KB na PSRAM
static const int kImgSize         = 96 * 96 * 3;

// Nomes das 10 classes (mesma ordem do treino — diretórios ordenados)
static const char* kClassNames[] = {
    "D01_requeima",
    "D02_septoriose",
    "D03_pinta_preta",
    "D03b_mancha_alvo",
    "D05_mofo_foliar",
    "D06_vira_cabeca",
    "D06b_mosaico",
    "D07_acaro_bronzeamento",
    "D09_mancha_bacteriana",
    "saudavel"
};
static const int kNumClasses = 10;

// ---------------------------------------------------------------------------
// Estado global do runtime
// ---------------------------------------------------------------------------
static uint8_t*                          s_tensor_arena = nullptr;
static tflite::AllOpsResolver            s_resolver;
static const tflite::Model*              s_model  = nullptr;
static tflite::MicroInterpreter*         s_interp = nullptr;
static TfLiteTensor*                     s_input  = nullptr;
static TfLiteTensor*                     s_output = nullptr;
static bool                              s_ready  = false;

// ---------------------------------------------------------------------------
bool inference_init() {
    Serial.println("[TFLite] Iniciando...");

    // Alocar tensor arena na PSRAM
    s_tensor_arena = (uint8_t*) ps_malloc(kTensorArenaSize);
    if (!s_tensor_arena) {
        Serial.println("[TFLite] ERRO: ps_malloc falhou — PSRAM disponível?");
        return false;
    }
    Serial.printf("[TFLite] Arena: %d KB na PSRAM\n", kTensorArenaSize / 1024);

    // Carregar modelo
    s_model = tflite::GetModel(g_model_data);
    if (s_model->version() != TFLITE_SCHEMA_VERSION) {
        Serial.printf("[TFLite] ERRO: versão do schema incompatível (%d != %d)\n",
                      s_model->version(), TFLITE_SCHEMA_VERSION);
        return false;
    }

    // Criar interpreter
    static tflite::MicroInterpreter static_interp(
        s_model, s_resolver, s_tensor_arena, kTensorArenaSize);
    s_interp = &static_interp;

    // Alocar tensores
    TfLiteStatus status = s_interp->AllocateTensors();
    if (status != kTfLiteOk) {
        Serial.println("[TFLite] ERRO: AllocateTensors falhou");
        return false;
    }

    // Validar I/O
    s_input  = s_interp->input(0);
    s_output = s_interp->output(0);

    Serial.printf("[TFLite] Input : [%d, %d, %d, %d] tipo=%d\n",
        s_input->dims->data[0], s_input->dims->data[1],
        s_input->dims->data[2], s_input->dims->data[3],
        s_input->type);
    Serial.printf("[TFLite] Output: [%d, %d] tipo=%d\n",
        s_output->dims->data[0], s_output->dims->data[1],
        s_output->type);
    Serial.printf("[TFLite] Arena usada: %d bytes\n", s_interp->arena_used_bytes());
    Serial.printf("[TFLite] RAM livre: %d bytes\n", ESP.getFreeHeap());

    s_ready = true;
    Serial.println("[TFLite] Pronto.");
    return true;
}

// ---------------------------------------------------------------------------
InferenceResult inference_run(const int8_t* image_data) {
    InferenceResult result;
    result.valid      = false;
    result.class_index = -1;
    result.confidence  = 0.0f;
    result.latency_ms  = 0;
    strncpy(result.class_name, "erro", sizeof(result.class_name));

    if (!s_ready) {
        Serial.println("[TFLite] ERRO: inference_init() não foi chamado");
        return result;
    }

    // Copiar imagem para o tensor de entrada
    memcpy(s_input->data.int8, image_data, kImgSize);

    // Executar inferência e medir latência
    int64_t t0 = esp_timer_get_time();
    TfLiteStatus status = s_interp->Invoke();
    int64_t t1 = esp_timer_get_time();

    if (status != kTfLiteOk) {
        Serial.println("[TFLite] ERRO: Invoke() falhou");
        return result;
    }

    result.latency_ms = (int32_t)((t1 - t0) / 1000);

    // Dequantizar saídas INT8 → float e encontrar classe com maior score
    float   scale      = s_output->params.scale;
    int32_t zero_point = s_output->params.zero_point;

    int   best_idx   = 0;
    float best_score = -1e9f;

    for (int i = 0; i < kNumClasses; i++) {
        float score = (s_output->data.int8[i] - zero_point) * scale;
        if (score > best_score) {
            best_score = score;
            best_idx   = i;
        }
    }

    // Softmax simples para converter logits em probabilidade
    float sum = 0.0f;
    float scores[10];
    for (int i = 0; i < kNumClasses; i++) {
        scores[i] = expf((s_output->data.int8[i] - zero_point) * scale);
        sum += scores[i];
    }
    float confidence = (sum > 0.0f) ? scores[best_idx] / sum : 0.0f;

    result.valid       = true;
    result.class_index = best_idx;
    result.confidence  = confidence;
    result.latency_ms  = result.latency_ms;
    strncpy(result.class_name, kClassNames[best_idx], sizeof(result.class_name));

    return result;
}
