/*
 * ESP32 Smart Neckband Firmware
 * Author: Jaswanth
 *
 * Reads sensors (DHT22, NEO-6M GPS, MPU6050, MAX30102)
 * Publishes data to MQTT broker as JSON
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
// TODO: Add GPS, MPU6050, MAX30102 libraries

// ===== Configuration =====
#include "config.h"

// ===== Pin Definitions =====
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define LED_PIN 2

// ===== Objects =====
WiFiClient espClient;
PubSubClient mqttClient(espClient);
DHT dht(DHT_PIN, DHT_TYPE);

// ===== Cattle & Farm IDs =====
const char *FARM_ID = "FARM-01";
const char *CATTLE_ID = "CTL-001";

// ===== Timing =====
unsigned long lastPublish = 0;
const long PUBLISH_INTERVAL = 30000; // 30 seconds

void setup()
{
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);

    // Initialize sensors
    dht.begin();
    // TODO: Initialize GPS, MPU6050, MAX30102

    // Connect WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected");

    // Connect MQTT
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    reconnectMQTT();
}

void loop()
{
    if (!mqttClient.connected())
    {
        reconnectMQTT();
    }
    mqttClient.loop();

    unsigned long now = millis();
    if (now - lastPublish >= PUBLISH_INTERVAL)
    {
        lastPublish = now;
        publishSensorData();
    }
}

void reconnectMQTT()
{
    while (!mqttClient.connected())
    {
        Serial.print("Connecting to MQTT...");
        String clientId = "ESP32-" + String(FARM_ID) + "-" + String(CATTLE_ID);

        if (mqttClient.connect(clientId.c_str()))
        {
            Serial.println("connected");
            digitalWrite(LED_PIN, HIGH);
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.println(mqttClient.state());
            delay(5000);
        }
    }
}

void publishSensorData()
{
    // Read temperature
    float temperature = dht.readTemperature();
    if (!isnan(temperature))
    {
        StaticJsonDocument<256> doc;
        doc["value"] = temperature;
        doc["unit"] = "celsius";
        doc["timestamp"] = getTimestamp();
        doc["device_id"] = String("ESP32-") + FARM_ID + "-" + CATTLE_ID;

        char buffer[256];
        serializeJson(doc, buffer);

        String topic = String("livestock/") + FARM_ID + "/" + CATTLE_ID + "/temperature";
        mqttClient.publish(topic.c_str(), buffer);
        Serial.printf("Published temp: %.1f°C\n", temperature);
    }

    // TODO: Read and publish GPS, accelerometer, heart rate
}

String getTimestamp()
{
    // TODO: Use NTP or GPS time
    return "2026-02-15T10:30:00Z";
}
