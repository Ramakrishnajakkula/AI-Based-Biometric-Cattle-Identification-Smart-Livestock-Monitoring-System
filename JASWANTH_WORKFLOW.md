# Jaswanth — IoT & Edge Lead Workflow

## Role: ESP32 Neckband + MQTT Pipeline + Sensor Simulator

**Member:** Jaswanth
**Module:** `iot/firmware/` + `iot/mqtt_worker/` + `iot/simulation/`
**Python Version:** 3.12 (for MQTT worker & simulator)
**Primary Tech:** ESP32, PlatformIO, MQTT (Mosquitto), Paho-MQTT, Arduino Framework

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                JASWANTH's IoT ARCHITECTURE                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │  EDGE LAYER: ESP32 Smart Neckband                               │     │
│  │                                                                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │     │
│  │  │ DHT22    │  │ NEO-6M   │  │ MPU6050  │  │ MAX30102     │    │     │
│  │  │ Temp/    │  │ GPS      │  │ Accel/   │  │ Heart Rate   │    │     │
│  │  │ Humidity │  │ Module   │  │ Gyro     │  │ + SpO2       │    │     │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘    │     │
│  │       │              │              │               │            │     │
│  │       └──────────────┴──────┬───────┴───────────────┘            │     │
│  │                             │                                    │     │
│  │                    ┌────────▼────────┐                           │     │
│  │                    │    ESP32        │                           │     │
│  │                    │  Microcontroller│                           │     │
│  │                    │  - WiFi/GSM    │                           │     │
│  │                    │  - Deep Sleep  │                           │     │
│  │                    │  - JSON Build  │                           │     │
│  │                    └────────┬────────┘                           │     │
│  └─────────────────────────────┼───────────────────────────────────┘     │
│                                │                                         │
│                          MQTT Publish                                    │
│                          (WiFi/GSM)                                      │
│                                │                                         │
│  ┌─────────────────────────────▼───────────────────────────────────┐     │
│  │  BROKER LAYER: Mosquitto MQTT Broker                            │     │
│  │                                                                  │     │
│  │  Topics:                                                         │     │
│  │  livestock/{farm_id}/{cattle_id}/temperature                     │     │
│  │  livestock/{farm_id}/{cattle_id}/heartrate                       │     │
│  │  livestock/{farm_id}/{cattle_id}/gps                             │     │
│  │  livestock/{farm_id}/{cattle_id}/activity                        │     │
│  │  livestock/{farm_id}/{cattle_id}/status                          │     │
│  │  livestock/alerts/{cattle_id}/health                             │     │
│  │  livestock/alerts/{cattle_id}/geofence                           │     │
│  │                                                                  │     │
│  │  Port 1883 (TCP) | Port 9001 (WebSocket for frontend)           │     │
│  └─────────────────────────────┬───────────────────────────────────┘     │
│                                │                                         │
│                          MQTT Subscribe                                  │
│                                │                                         │
│  ┌─────────────────────────────▼───────────────────────────────────┐     │
│  │  WORKER LAYER: Python MQTT Subscriber                           │     │
│  │                                                                  │     │
│  │  worker.py ──subscribe──▶ handlers.py ──parse──▶ MongoDB        │     │
│  │                                                                  │     │
│  │  - Receives all sensor messages                                  │     │
│  │  - Validates JSON payload                                        │     │
│  │  - Stores in sensor_readings collection                          │     │
│  │  - Triggers alerts for abnormal values                           │     │
│  │  - Forwards real-time data to Flask-SocketIO                     │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  SIMULATION LAYER: Python Sensor Simulator                       │     │
│  │                                                                  │     │
│  │  sensor_simulator.py                                             │     │
│  │  - Generates realistic sensor data (no hardware needed)          │     │
│  │  - Supports N virtual cattle with unique IDs                     │     │
│  │  - Scenarios: normal, fever, low_activity, geofence_breach       │     │
│  │  - Publishes to Mosquitto just like real ESP32                   │     │
│  └──────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘
```

### Hardware Wiring Schematic

```
                        ESP32 DevKit V1
                    ┌──────────────────────┐
                    │                      │
    DHT22 ─────────│ GPIO 4    (Data)      │
    (Temp/Humidity) │                      │
                    │                      │
    NEO-6M GPS ────│ GPIO 16   (RX2)      │
                   │ GPIO 17   (TX2)      │
                    │                      │
    MPU6050 ───────│ GPIO 21   (SDA)      │
    (Accelerometer)│ GPIO 22   (SCL)      │
                    │                      │
    MAX30102 ──────│ GPIO 21   (SDA)*     │  * Shared I2C bus
    (Heart Rate)   │ GPIO 22   (SCL)*     │
                    │                      │
    LED Indicator ─│ GPIO 2    (Built-in) │
                    │                      │
    Battery ───────│ VIN (3.7V LiPo)      │
                    └──────────────────────┘
```

### MQTT Message Formats

```json
// Temperature (livestock/{farm_id}/{cattle_id}/temperature)
{
    "value": 38.5,
    "unit": "celsius",
    "timestamp": "2026-02-15T10:30:00Z",
    "device_id": "ESP32-FARM01-CTL001"
}

// Heart Rate (livestock/{farm_id}/{cattle_id}/heartrate)
{
    "bpm": 72,
    "spo2": 98,
    "timestamp": "2026-02-15T10:30:00Z",
    "device_id": "ESP32-FARM01-CTL001"
}

// GPS (livestock/{farm_id}/{cattle_id}/gps)
{
    "lat": 17.3850,
    "lng": 78.4867,
    "altitude": 542.3,
    "speed": 0.5,
    "timestamp": "2026-02-15T10:30:00Z",
    "device_id": "ESP32-FARM01-CTL001"
}

// Activity (livestock/{farm_id}/{cattle_id}/activity)
{
    "accel_x": 0.12,
    "accel_y": -0.34,
    "accel_z": 9.78,
    "activity_level": "resting",
    "timestamp": "2026-02-15T10:30:00Z",
    "device_id": "ESP32-FARM01-CTL001"
}

// Status (livestock/{farm_id}/{cattle_id}/status)
{
    "online": true,
    "battery": 85,
    "signal_strength": -67,
    "timestamp": "2026-02-15T10:30:00Z"
}
```

---

## Folder Structure (Jaswanth's Files)

```
cap/
├── iot/
│   ├── firmware/                      # 🔌 ESP32 Firmware (PlatformIO)
│   │   ├── src/
│   │   │   └── main.cpp               #   Main firmware: read sensors + MQTT publish
│   │   ├── include/
│   │   │   ├── config.h               #   WiFi SSID/password, MQTT broker IP
│   │   │   ├── sensors.h              #   Sensor pin definitions & read functions
│   │   │   └── mqtt_handler.h         #   MQTT connect, publish, reconnect
│   │   ├── lib/
│   │   │   └── README                 #   PlatformIO custom libraries
│   │   ├── test/
│   │   │   └── test_sensors.cpp       #   Unit tests for sensor reads
│   │   └── platformio.ini             #   Board: esp32dev, libs, build flags
│   │
│   ├── mqtt_worker/                   # 🐍 Python MQTT Subscriber Service
│   │   ├── __init__.py
│   │   ├── worker.py                  #   Main subscriber loop
│   │   ├── handlers.py                #   Message handlers per topic
│   │   ├── config.py                  #   Broker address, MongoDB URI
│   │   ├── db.py                      #   MongoDB connection & insert
│   │   └── alert_checker.py           #   Check sensor thresholds → trigger alerts
│   │
│   ├── simulation/                    # 🎮 Sensor Data Simulator
│   │   ├── __init__.py
│   │   ├── sensor_simulator.py        #   Main simulator (N cattle)
│   │   ├── cattle_profiles.py         #   Virtual cattle with normal ranges
│   │   ├── scenarios.json             #   Predefined scenarios (fever, escape)
│   │   └── generate_data.py           #   Generate CSV dataset for testing
│   │
│   └── requirements.txt               # IoT Python dependencies
│
├── docker-compose.yml                 # Mosquitto + MongoDB services
└── mosquitto/
    └── mosquitto.conf                 # Mosquitto broker configuration
```

---

## Dependencies (iot/requirements.txt)

```txt
# MQTT
paho-mqtt==2.1.0

# Database
pymongo==4.10.1

# Data
numpy==1.26.4
pandas==2.2.2

# Utilities
python-dotenv==1.0.1
pyyaml==6.0.1
schedule==1.2.1

# Logging
colorlog==6.8.2
```

---

## Setup Instructions

```bash
# ===== PYTHON MQTT WORKER & SIMULATOR =====

# 1. Python 3.12 environment
cd cap
python -m venv venv
venv\Scripts\activate

# 2. Install IoT dependencies
pip install -r iot/requirements.txt

# 3. Install Mosquitto MQTT Broker
# Windows: Download from https://mosquitto.org/download/
# Or use Docker (recommended):
docker run -d --name mosquitto -p 1883:1883 -p 9001:9001 eclipse-mosquitto:2

# 4. Start MongoDB (Docker):
docker run -d --name mongodb -p 27017:27017 mongo:7

# Or use docker-compose (includes both):
docker-compose up -d

# 5. Test MQTT connection:
python -c "import paho.mqtt.client as mqtt; print('paho-mqtt OK')"

# 6. Run sensor simulator:
python iot/simulation/sensor_simulator.py

# 7. Run MQTT worker (separate terminal):
python iot/mqtt_worker/worker.py

# ===== ESP32 FIRMWARE (if using real hardware) =====

# 1. Install PlatformIO:
pip install platformio

# 2. Build firmware:
cd iot/firmware
pio run

# 3. Upload to ESP32:
pio run --target upload

# 4. Monitor serial output:
pio device monitor --baud 115200
```

---

## 4-Week Schedule

### WEEK 1 (Feb 11–17): Environment + MQTT + Simulator

| Day | Date   | Tasks                                                                                                                 | Deliverable               |
| --- | ------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| Tue | Feb 11 | Set up Python 3.12 venv, install dependencies. Install Docker Desktop. Run Mosquitto + MongoDB containers             | Docker services running   |
| Wed | Feb 12 | Design MQTT topic structure. Write `mosquitto.conf`. Test publish/subscribe with `mosquitto_pub`/`mosquitto_sub` CLI  | MQTT broker configured    |
| Thu | Feb 13 | Build `sensor_simulator.py` — simulate 5 virtual cattle with realistic sensor data (temp, GPS, heartrate, accel)      | Simulator publishing data |
| Fri | Feb 14 | Build `mqtt_worker/worker.py` — subscribe to all topics, parse JSON, print to console                                 | Worker receiving messages |
| Sat | Feb 15 | Build `mqtt_worker/handlers.py` — separate handler for each sensor type. Build `db.py` — store in MongoDB             | Data stored in MongoDB    |
| Sun | Feb 16 | Build `cattle_profiles.py` — define normal ranges per cattle. Build `scenarios.json` — fever, escape, death scenarios | Scenarios ready           |
| Mon | Feb 17 | Test end-to-end: Simulator → MQTT → Worker → MongoDB. Verify data in MongoDB Compass                                  | ✅ Data pipeline working  |

**Coordination:**

- Share with **Akash**: MongoDB collection name & document format for `sensor_readings`
- Share with **Akash**: MQTT topic structure documentation
- Discuss with **Aditi**: What sensor thresholds trigger health alerts

---

### WEEK 2 (Feb 18–24): ESP32 Firmware + Alert System

| Day | Date   | Tasks                                                                                              | Deliverable                     |
| --- | ------ | -------------------------------------------------------------------------------------------------- | ------------------------------- |
| Tue | Feb 18 | Set up PlatformIO project for ESP32. Write `config.h` (WiFi, MQTT), `sensors.h` (pin defs)         | PlatformIO project compiles     |
| Wed | Feb 19 | Write DHT22 temperature reading code. Write MQTT publish for temperature topic                     | Temp data publishing from ESP32 |
| Thu | Feb 20 | Add NEO-6M GPS module reading. Publish GPS data as JSON to MQTT                                    | GPS tracking working            |
| Fri | Feb 21 | Add MPU6050 accelerometer. Calculate activity level (resting/walking/running). Publish activity    | Motion detection working        |
| Sat | Feb 22 | Add MAX30102 heart rate sensor. Implement deep sleep for battery saving                            | Heart rate + power management   |
| Sun | Feb 23 | Build `alert_checker.py` — check thresholds (temp > 39.5°C → fever alert, no GPS → device offline) | Alert system ready              |
| Mon | Feb 24 | Complete firmware with all sensors. Test real ESP32 device if available. Refine simulator accuracy | ✅ Firmware + alerts working    |

**Coordination:**

- Deliver to **Akash**: `alert_checker.py` interface for Flask integration
- Share with **Aditi**: Real-time alert format for notification system

---

### WEEK 3 (Feb 25–Mar 3): Integration & Real-time

| Day | Date   | Tasks                                                                                    | Deliverable                 |
| --- | ------ | ---------------------------------------------------------------------------------------- | --------------------------- |
| Tue | Feb 25 | Integrate mqtt_worker with Akash's Flask backend. Worker forwards data to Flask-SocketIO | Real-time bridge working    |
| Wed | Feb 26 | Test: Simulator → MQTT → Worker → MongoDB → Flask API → Frontend (with Poshith)          | Full data pipeline verified |
| Thu | Feb 27 | Add geo-fencing logic — define farm boundaries, detect breach                            | Geofence alerts working     |
| Fri | Feb 28 | Add Last Will & Testament (LWT) to ESP32 — auto-detect device offline                    | Device status tracking      |
| Sat | Mar 1  | Stress test simulator with 50+ virtual cattle. Optimize MongoDB batch inserts            | Performance tested          |
| Sun | Mar 2  | Add scenario switching to simulator (normal → fever → recovered). Test alert flow        | Scenario testing complete   |
| Mon | Mar 3  | Debug integration issues with all team members                                           | ✅ Fully integrated         |

**Coordination:**

- With **Akash**: Debug Flask-SocketIO bridge
- With **Poshith**: Verify real-time data appears on dashboard
- With **Aditi**: Verify health alerts trigger from sensor anomalies

---

### WEEK 4 (Mar 4–11): Polish & Documentation

| Day | Date   | Tasks                                                                            | Deliverable            |
| --- | ------ | -------------------------------------------------------------------------------- | ---------------------- |
| Tue | Mar 4  | Write hardware setup guide (wiring diagram, parts list, assembly)                | Hardware documentation |
| Wed | Mar 5  | Create IoT module documentation (MQTT topics, data formats, worker architecture) | IoT docs complete      |
| Thu | Mar 6  | Add error handling to worker (reconnect on disconnect, malformed JSON handling)  | Robust worker          |
| Fri | Mar 7  | Create demo scenario — live demonstration of sensor data flowing through system  | Demo script ready      |
| Sat | Mar 8  | Code cleanup, add logging, add docstrings                                        | Clean codebase         |
| Sun | Mar 9  | Final testing with full team — sensor → backend → frontend → alerts              | System verified        |
| Mon | Mar 11 | Final commit, update README                                                      | ✅ Complete            |

---

## Key Technical Decisions

| Decision         | Choice        | Why                                                    |
| ---------------- | ------------- | ------------------------------------------------------ |
| MQTT Broker      | Mosquitto     | Lightweight, supports WebSocket, easy Docker setup     |
| MQTT Library     | Paho-MQTT 2.x | Official Eclipse library, Python 3.12 compatible       |
| Microcontroller  | ESP32         | WiFi built-in, low cost, Arduino ecosystem             |
| Sensor protocol  | I2C + OneWire | Standard for all chosen sensors                        |
| Data format      | JSON          | Human-readable, easy to parse in Python & JavaScript   |
| Simulator        | Python script | Team can test without hardware, reproducible scenarios |
| Power management | Deep sleep    | Essential for battery-powered neckband                 |
| QoS Level        | QoS 1         | At-least-once delivery — sensor data must not be lost  |

---

## Output Contracts (for other team members)

### For Akash (Backend):

```python
# MongoDB document format (sensor_readings collection):
{
    "_id": ObjectId("..."),
    "cattle_id": "CTL-001",
    "farm_id": "FARM-01",
    "sensor_type": "temperature",   # temperature | heartrate | gps | activity
    "data": {
        "value": 38.5,
        "unit": "celsius"
    },
    "device_id": "ESP32-FARM01-CTL001",
    "timestamp": ISODate("2026-02-15T10:30:00Z"),
    "received_at": ISODate("2026-02-15T10:30:01Z")
}
```

### For Poshith (Frontend via WebSocket):

```json
// Socket.IO event: "sensor_update"
{
  "cattle_id": "CTL-001",
  "sensor_type": "temperature",
  "value": 38.5,
  "timestamp": "2026-02-15T10:30:00Z"
}
```

### For Aditi (Alert triggers):

```python
# Alert threshold config:
THRESHOLDS = {
    "temperature": {"min": 37.5, "max": 39.5, "unit": "celsius"},
    "heartrate": {"min": 40, "max": 80, "unit": "bpm"},
    "activity": {"min_daily_steps": 500},
    "geofence": {"radius_meters": 500, "center": {"lat": 17.385, "lng": 78.486}}
}
```

---

## Verification Checklist

- [ ] Python 3.12 environment with paho-mqtt working
- [ ] Mosquitto broker running (Docker or local)
- [ ] MongoDB running and accessible
- [ ] Sensor simulator publishes data to MQTT topics
- [ ] MQTT worker receives and stores data in MongoDB
- [ ] Data visible in MongoDB Compass
- [ ] ESP32 firmware compiles (PlatformIO)
- [ ] ESP32 reads all 4 sensors (DHT22, GPS, MPU6050, MAX30102)
- [ ] ESP32 publishes correctly formatted JSON to MQTT
- [ ] Deep sleep mode working on ESP32
- [ ] Alert checker detects abnormal sensor values
- [ ] Geo-fencing logic detects breach
- [ ] LWT detects device offline
- [ ] Real-time data flows to Flask-SocketIO → Frontend
- [ ] Simulator supports multiple scenarios (fever, escape, normal)
- [ ] All code documented with comments
