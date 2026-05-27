/**
 * main.cpp — Ceres Diagnóstico Sprint 2
 *
 * Fluxo:
 *   setup()  → WiFi + MQTT + TFLite init
 *   loop()   → itera sobre g_test_images[], roda inferência,
 *              imprime Serial, publica MQTT, indica LED
 *
 * Hardware : ESP32-S3-WROOM-1-N16R8
 * LED RGB  : pinos configuráveis em config.h (ou use o LED builtin)
 * MQTT     : PubSubClient → broker definido em config.h
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <esp_heap_caps.h>

#include "config.h"
#include "inference.h"
#include "model_data.h"
#include "test_images.h"

// ---------------------------------------------------------------------------
// LED RGB — adapte os pinos ao seu módulo
// Muitos ESP32-S3-DevKitC-1 têm RGB WS2812 no pino 48
// Para LED simples (anodo comum), troque para GPIOs disponíveis
// ---------------------------------------------------------------------------
#ifndef LED_PIN_R
  #define LED_PIN_R  4
#endif
#ifndef LED_PIN_G
  #define LED_PIN_G  5
#endif
#ifndef LED_PIN_B
  #define LED_PIN_B  6
#endif

// ---------------------------------------------------------------------------
// MQTT
// ---------------------------------------------------------------------------
static WiFiClient   s_wifi_client;
static PubSubClient s_mqtt(s_wifi_client);

// ---------------------------------------------------------------------------
// Estado do benchmark
// ---------------------------------------------------------------------------
static int     s_img_index   = 0;
static int32_t s_total_ms    = 0;
static int     s_total_count = 0;
static bool    s_done        = false;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
static void led_set(bool r, bool g, bool b) {
    digitalWrite(LED_PIN_R, r ? HIGH : LOW);
    digitalWrite(LED_PIN_G, g ? HIGH : LOW);
    digitalWrite(LED_PIN_B, b ? HIGH : LOW);
}

static void wifi_connect() {
    Serial.printf("[WiFi] Conectando a %s", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    int tentativas = 0;
    while (WiFi.status() != WL_CONNECTED && tentativas < 30) {
        delay(500);
        Serial.print(".");
        tentativas++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.printf("\n[WiFi] OK — IP: %s\n", WiFi.localIP().toString().c_str());
    } else {
        Serial.println("\n[WiFi] FALHA — continuando sem WiFi");
    }
}

static bool mqtt_connect() {
    if (!s_mqtt.connected()) {
        String client_id = "ceres-" + String(DEVICE_ID);
        if (s_mqtt.connect(client_id.c_str())) {
            Serial.printf("[MQTT] Conectado ao broker %s:%d\n", MQTT_BROKER, MQTT_PORT);
            return true;
        } else {
            Serial.printf("[MQTT] Falha (state=%d)\n", s_mqtt.state());
            return false;
        }
    }
    return true;
}

static void mqtt_publish_result(const InferenceResult& r, int img_idx) {
    if (!mqtt_connect()) return;

    char payload[256];
    snprintf(payload, sizeof(payload),
        "{\"device_id\":\"%s\","
        "\"img_idx\":%d,"
        "\"classe\":\"%s\","
        "\"class_index\":%d,"
        "\"confianca\":%.4f,"
        "\"latencia_ms\":%d,"
        "\"ram_livre\":%d}",
        DEVICE_ID,
        img_idx,
        r.class_name,
        r.class_index,
        r.confidence,
        r.latency_ms,
        (int) ESP.getFreeHeap()
    );

    s_mqtt.publish(MQTT_TOPIC, payload);
    Serial.printf("[MQTT] Publicado: %s\n", payload);
}

static void print_result(const InferenceResult& r, int img_idx) {
    Serial.println("----------------------------------------");
    Serial.printf("[IMG %d/%d] Classe esperada : %s\n",
                  img_idx + 1, TEST_IMG_COUNT, g_class_names[img_idx]);
    Serial.printf("[IMG %d/%d] Predição        : %s (idx=%d)\n",
                  img_idx + 1, TEST_IMG_COUNT, r.class_name, r.class_index);
    Serial.printf("[IMG %d/%d] Confiança       : %.1f%%\n",
                  img_idx + 1, TEST_IMG_COUNT, r.confidence * 100.0f);
    Serial.printf("[IMG %d/%d] Latência        : %d ms\n",
                  img_idx + 1, TEST_IMG_COUNT, r.latency_ms);
    Serial.printf("[IMG %d/%d] RAM livre       : %d bytes\n",
                  img_idx + 1, TEST_IMG_COUNT, (int) ESP.getFreeHeap());

    // Acerto?
    bool acertou = (r.class_index == img_idx);
    Serial.printf("[IMG %d/%d] Resultado       : %s\n",
                  img_idx + 1, TEST_IMG_COUNT, acertou ? "✓ CORRETO" : "✗ ERRADO");
    Serial.println("----------------------------------------");
}

static void indicar_led(const InferenceResult& r) {
    if (!r.valid) {
        led_set(true, false, false);   // vermelho: erro
        return;
    }
    if (r.confidence < CONFIDENCE_THRESHOLD) {
        led_set(true, true, false);    // amarelo: baixa confiança
        return;
    }
    bool saudavel = (strcmp(r.class_name, "saudavel") == 0);
    if (saudavel) {
        led_set(false, true, false);   // verde: saudável
    } else {
        led_set(true, false, false);   // vermelho: doença detectada
    }
}

static void print_benchmark_summary() {
    Serial.println("\n========================================");
    Serial.println("       BENCHMARK ESP32-S3 — Sprint 2    ");
    Serial.println("========================================");
    Serial.printf("Imagens testadas : %d\n", s_total_count);
    if (s_total_count > 0) {
        Serial.printf("Latência média   : %d ms\n", s_total_ms / s_total_count);
        Serial.printf("Latência total   : %d ms\n", s_total_ms);
    }
    Serial.printf("Modelo           : MobileNetV2 0.35 INT8\n");
    Serial.printf("Entrada          : 96x96x3 INT8\n");
    Serial.printf("Arena PSRAM      : 512 KB\n");
    Serial.printf("RAM livre (heap) : %d bytes\n", (int) ESP.getFreeHeap());
    Serial.printf("PSRAM livre      : %d bytes\n", (int) ESP.getFreePsram());
    Serial.println("========================================");
    Serial.println("Benchmark concluído. Reiniciando em 30s...");
}

// ---------------------------------------------------------------------------
void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n=== Ceres Diagnóstico — Sprint 2 ===");

    // LED
    pinMode(LED_PIN_R, OUTPUT);
    pinMode(LED_PIN_G, OUTPUT);
    pinMode(LED_PIN_B, OUTPUT);
    led_set(false, false, true);   // azul: inicializando

    // PSRAM
    if (psramFound()) {
        Serial.printf("[SYS] PSRAM: %d bytes livres\n", (int) ESP.getFreePsram());
    } else {
        Serial.println("[SYS] AVISO: PSRAM não encontrada — tensor arena falhará!");
    }

    // WiFi
    wifi_connect();

    // MQTT
    s_mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    s_mqtt.setBufferSize(512);
    mqtt_connect();

    // TFLite Micro
    led_set(true, true, false);    // amarelo: carregando modelo
    if (!inference_init()) {
        Serial.println("[ERRO FATAL] TFLite init falhou — halt");
        led_set(true, false, false);
        while (true) { delay(1000); }
    }

    led_set(false, true, false);   // verde: pronto
    Serial.printf("\n[OK] Iniciando benchmark com %d imagens de teste...\n\n",
                  TEST_IMG_COUNT);
    delay(500);
}

// ---------------------------------------------------------------------------
void loop() {
    if (s_done) {
        // Benchmark concluído — pisca lentamente e reinicia
        delay(30000);
        ESP.restart();
        return;
    }

    s_mqtt.loop();   // mantém conexão MQTT ativa

    if (s_img_index < TEST_IMG_COUNT) {
        const int8_t* img = g_test_images[s_img_index];

        InferenceResult result = inference_run(img);

        print_result(result, s_img_index);
        indicar_led(result);
        mqtt_publish_result(result, s_img_index);

        if (result.valid) {
            s_total_ms    += result.latency_ms;
            s_total_count += 1;
        }

        s_img_index++;
        delay(200);   // pausa entre inferências para não saturar Serial/MQTT
    } else {
        // Todas as imagens processadas
        print_benchmark_summary();
        s_done = true;
        led_set(false, true, false);   // verde estático: concluído
    }
}
