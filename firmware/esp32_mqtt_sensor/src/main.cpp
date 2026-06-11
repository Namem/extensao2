#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <DHTesp.h>
#include "config.h"

#ifdef MQTT_TLS
WiFiClientSecure wifiClient;
#else
WiFiClient       wifiClient;
#endif
PubSubClient mqtt(wifiClient);
DHTesp       dht;

// ── WiFi ──────────────────────────────────────────────────────────────────────
void conectarWifi() {
    Serial.printf("Conectando WiFi %s", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.printf("\nWiFi OK — IP: %s\n", WiFi.localIP().toString().c_str());
}

// ── MQTT ──────────────────────────────────────────────────────────────────────
void conectarMqtt() {
    while (!mqtt.connected()) {
        Serial.print("Conectando MQTT...");
        #ifdef MQTT_USER
        if (mqtt.connect(DEVICE_ID, MQTT_USER, MQTT_PASSWORD)) {
        #else
        if (mqtt.connect(DEVICE_ID)) {
        #endif
            Serial.println("OK");
        } else {
            Serial.printf("falhou rc=%d — tentando em 5s\n", mqtt.state());
            delay(5000);
        }
    }
}

// ── Leitura do solo (ADC) ─────────────────────────────────────────────────────
// Raw ADC 0-4095: seco=alto, molhado=baixo → inverte para %
int lerUmidadeSolo() {
    int raw = analogRead(PIN_SOLO);
    int pct = map(raw, 3400, 600, 0, 100);
    return constrain(pct, 0, 100);
}

// ── Leitura DHT22 com retry (WiFi IRQs corrompem timing one-wire) ────────────
bool lerDHT22(float &temp, float &umid) {
    for (int tentativa = 0; tentativa < DHT_MAX_RETRIES; tentativa++) {
        if (tentativa > 0) delay(DHT_RETRY_DELAY_MS);

        TempAndHumidity leitura = dht.getTempAndHumidity();
        if (dht.getStatus() == DHTesp::ERROR_NONE) {
            temp = leitura.temperature;
            umid = leitura.humidity;
            return true;
        }
        Serial.printf("DHT22 tentativa %d/%d: %s\n",
                      tentativa + 1, DHT_MAX_RETRIES, dht.getStatusString());
    }
    return false;
}

// ── Publicação MQTT ───────────────────────────────────────────────────────────
void publicarSensores() {
    float temp, umid;
    bool dhtOk = lerDHT22(temp, umid);

    int umidade_solo = lerUmidadeSolo();

    char payload[200];

    if (dhtOk) {
        Serial.printf("Temp: %.1f°C  Umid.Ar: %.1f%%  Umid.Solo: %d%%\n",
                      temp, umid, umidade_solo);
        snprintf(payload, sizeof(payload),
            "{"
            "\"device_id\":\"%s\","
            "\"temperatura\":%.1f,"
            "\"umidade_ar\":%.1f,"
            "\"umidade_solo\":%d"
            "}",
            DEVICE_ID, temp, umid, umidade_solo
        );
    } else {
        Serial.printf("Solo: %d%% (DHT22 falhou %d tentativas)\n",
                      umidade_solo, DHT_MAX_RETRIES);
        snprintf(payload, sizeof(payload),
            "{"
            "\"device_id\":\"%s\","
            "\"umidade_solo\":%d"
            "}",
            DEVICE_ID, umidade_solo
        );
    }

    if (mqtt.publish(MQTT_TOPIC, payload)) {
        Serial.printf("Publicado em %s\n", MQTT_TOPIC);
    } else {
        Serial.println("Falha ao publicar MQTT");
    }
}

// ── Setup / Loop ──────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    delay(1000);

    // GPIO 4 (DHT22) e GPIO 5 (solo) estão ambos no ADC1 do ESP32-S3.
    // Forçar GPIO 4 como digital ANTES do DHT para evitar que o ADC1
    // peripheral deixe o pin mux em modo analógico.
    pinMode(PIN_DHT22, INPUT_PULLUP);
    delay(100);

    dht.setup(PIN_DHT22, DHTesp::DHT22);
    Serial.printf("DHT22 em IO%d  |  Solo ADC em IO%d\n", PIN_DHT22, PIN_SOLO);

    // ADC só para o pino do solo — DEPOIS do DHT para não corromper pin mux
    analogReadResolution(12);
    analogSetPinAttenuation(PIN_SOLO, ADC_11db);

    conectarWifi();

    #ifdef MQTT_TLS
    wifiClient.setInsecure();
    #endif

    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    mqtt.setBufferSize(256);
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) conectarWifi();
    if (!mqtt.connected())             conectarMqtt();
    mqtt.loop();

    static unsigned long ultimoEnvio = 0;
    if (millis() - ultimoEnvio >= PUBLISH_INTERVAL_MS) {
        publicarSensores();
        ultimoEnvio = millis();
    }
}
