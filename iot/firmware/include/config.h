/*
 * ESP32 Configuration — WiFi & MQTT Credentials
 * Author: Jaswanth
 *
 * ⚠️ CHANGE THESE VALUES for your network!
 */

#ifndef CONFIG_H
#define CONFIG_H

// WiFi Credentials
const char *WIFI_SSID = "YOUR_WIFI_SSID";
const char *WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// MQTT Broker
const char *MQTT_BROKER = "192.168.1.100"; // Change to your broker IP
const int MQTT_PORT = 1883;

#endif
