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
    // Calibração básica: ar livre ~3400 (0%), submerso ~600 (100%)
    int pct = map(raw, 3400, 600, 0, 100);
    return constrain(pct, 0, 100);
}

// ── Publicação MQTT ───────────────────────────────────────────────────────────
void publicarSensores() {
    // Lê DHT22
    TempAndHumidity leitura = dht.getTempAndHumidity();

    if (dht.getStatus() != DHTesp::ERROR_NONE) {
        Serial.printf("DHT22 erro: %s\n", dht.getStatusString());
        return;
    }

    float temperatura  = leitura.temperature;
    float umidade_ar   = leitura.humidity;
    int   umidade_solo = lerUmidadeSolo();

    Serial.printf("Temp: %.1f°C  Umid.Ar: %.1f%%  Umid.Solo: %d%%\n",
                  temperatura, umidade_ar, umidade_solo);

    char payload[160];
    snprintf(payload, sizeof(payload),
        "{"
        "\"device_id\":\"%s\","
        "\"temperatura\":%.1f,"
        "\"umidade_ar\":%.1f,"
        "\"umidade_solo\":%d"
        "}",
        DEVICE_ID, temperatura, umidade_ar, umidade_solo
    );

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

    // Inicializa DHT22 no pino IO4
    dht.setup(PIN_DHT22, DHTesp::DHT22);
    Serial.printf("DHT22 em IO%d  |  Solo ADC em IO%d\n", PIN_DHT22, PIN_SOLO);

    // ADC 12 bits (0-4095)
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db); // faixa 0-3.3V

    conectarWifi();

    #ifdef MQTT_TLS
    wifiClient.setInsecure(); // aceita qualquer cert — suficiente para HiveMQ Cloud
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
