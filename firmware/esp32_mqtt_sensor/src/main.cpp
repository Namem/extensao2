#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"

WiFiClient   wifiClient;
PubSubClient mqtt(wifiClient);

void conectarWifi() {
    Serial.printf("Conectando WiFi %s", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.printf("\nWiFi OK — IP: %s\n", WiFi.localIP().toString().c_str());
}

void conectarMqtt() {
    while (!mqtt.connected()) {
        Serial.print("Conectando MQTT...");
        if (mqtt.connect(DEVICE_ID)) {
            Serial.println("OK");
        } else {
            Serial.printf("falhou rc=%d — tentando em 5s\n", mqtt.state());
            delay(5000);
        }
    }
}

void publicarSensores() {
    // Valores simulados — substituir por DHT22 + ADC quando tiver sensores
    float temperatura  = 25.0f + random(-30, 50) / 10.0f;
    float umidade_ar   = 60.0f + random(-100, 100) / 10.0f;
    int   umidade_solo = 40    + random(-10, 10);

    char payload[128];
    snprintf(payload, sizeof(payload),
        "{\"device_id\":\"%s\",\"temperatura\":%.1f,"
        "\"umidade_ar\":%.1f,\"umidade_solo\":%d,\"ts\":%lu}",
        DEVICE_ID, temperatura, umidade_ar, umidade_solo,
        (unsigned long)(esp_timer_get_time() / 1000000ULL)
    );

    mqtt.publish(MQTT_TOPIC, payload);
    Serial.printf("Publicado: %s\n", payload);
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    conectarWifi();
    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
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