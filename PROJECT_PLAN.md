# AI-Based Biometric Cattle Identification & Smart Livestock Monitoring System

## Capstone Project — Master Plan

**Project Duration:** February 11 – March 20, 2026 (4 Weeks + Buffer)
**Python Version:** 3.12 (All Members)
**Team Size:** 5 Members

---

## Team Members & Roles

| #   | Member          | Role                    | Primary Module                                        |
| --- | --------------- | ----------------------- | ----------------------------------------------------- |
| 1   | **Ramakrishna** | AI/ML Lead              | Cattle Face Detection + Recognition (YOLOv8, ArcFace) |
| 2   | **Jaswanth**    | IoT & Edge Lead         | ESP32 Neckband + MQTT Pipeline + Sensor Simulator     |
| 3   | **Akash**       | Backend & API Lead      | Flask REST API + MongoDB + Integration                |
| 4   | **Poshith**     | Frontend & Dashboard    | React Dashboard + Real-time Monitoring                |
| 5   | **Aditi**       | Health & Insurance Lead | Health Detection AI + Fraud Detection + Alerts        |

---

## Problem Statement

Current livestock management in India suffers from:

- **Identity fraud** — Ear tags/RFID can be removed or swapped
- **Duplicate insurance claims** — Same cattle registered multiple times
- **Ghost cattle** in government subsidy lists
- **No real-time health monitoring** — Diseases detected too late
- **Ownership disputes** — No biometric proof of ownership
- **Theft tracking** — No GPS-based monitoring

### Our Solution

A biometric identity system for livestock (like Aadhaar for animals) integrated with IoT-based real-time monitoring to prevent fraud in government insurance and subsidy programs.

---

## System Architecture (High-Level)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  EDGE LAYER  │    │   AI LAYER   │    │    CLOUD LAYER       │   │
│  │              │    │              │    │                      │   │
│  │  📷 Camera   │───▶│  YOLOv8      │───▶│  Flask REST API      │   │
│  │              │    │  Detection   │    │  (Python 3.12)       │   │
│  │  📡 ESP32    │    │              │    │                      │   │
│  │  Neckband    │    │  ArcFace     │    │  MongoDB Database    │   │
│  │  - GPS       │    │  Embedding   │    │                      │   │
│  │  - Temp      │    │              │    │  MQTT Broker         │   │
│  │  - Accel     │    │  Health      │    │  (Mosquitto)         │   │
│  │  - Heart     │    │  Detector    │    │                      │   │
│  └──────┬───────┘    └──────────────┘    └──────────┬───────────┘   │
│         │                                           │               │
│         │            MQTT Protocol                  │               │
│         └───────────────────────────────────────────┘               │
│                              │                                      │
│                    ┌─────────▼──────────┐                           │
│                    │  FRONTEND LAYER    │                           │
│                    │                    │                           │
│                    │  React Dashboard   │                           │
│                    │  - Live Sensors    │                           │
│                    │  - GPS Map         │                           │
│                    │  - Health Alerts   │                           │
│                    │  - Insurance       │                           │
│                    │  - Identification  │                           │
│                    └────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
ESP32 Sensors ──MQTT──▶ Mosquitto Broker ──▶ Python MQTT Worker ──▶ MongoDB
Camera Feed ──▶ YOLOv8 Detection ──▶ ArcFace Embedding ──▶ MongoDB (Cattle ID)
Camera Feed ──▶ YOLOv8 Health Detection ──▶ MongoDB (Health Alerts)
MongoDB ◀── Flask REST API ──HTTP──▶ React Dashboard (+ WebSocket for real-time)
Insurance Module ◀── Flask API ──▶ Fraud Detection Engine ──▶ Alerts (SMS/Email)
```

---

## Technology Stack

| Layer               | Technology                        | Version          |
| ------------------- | --------------------------------- | ---------------- |
| **Language**        | Python                            | 3.12             |
| **ML Detection**    | Ultralytics YOLOv8                | 8.3.x            |
| **ML Recognition**  | ArcFace (InsightFace)             | 0.7.3            |
| **Deep Learning**   | PyTorch                           | 2.2+             |
| **Computer Vision** | OpenCV                            | 4.9+             |
| **Backend**         | Flask                             | 3.0+             |
| **Database**        | MongoDB                           | 7.x              |
| **DB Driver**       | PyMongo                           | 4.6+             |
| **MQTT**            | Paho-MQTT                         | 2.1.x            |
| **MQTT Broker**     | Mosquitto                         | 2.x              |
| **Frontend**        | React + Vite                      | React 18, Vite 5 |
| **Charts**          | Recharts                          | 2.x              |
| **Maps**            | React-Leaflet                     | 4.x              |
| **Real-time**       | Flask-SocketIO + Socket.IO client | 5.x              |
| **IoT Hardware**    | ESP32 + PlatformIO                | —                |
| **Auth**            | Flask-JWT-Extended                | 4.x              |
| **Validation**      | Marshmallow                       | 3.x              |

---

## Complete Project Folder Structure

```
cap/
│
├── README.md                          # Project overview & setup guide
├── PROJECT_PLAN.md                    # This file — master plan
├── .gitignore                         # Git ignore rules
├── .python-version                    # Python 3.12
├── .env.example                       # Environment variables template
├── docker-compose.yml                 # MongoDB + Mosquitto + Services
├── requirements-common.txt            # Shared Python dependencies
│
├── RAMAKRISHNA_WORKFLOW.md            # AI/ML Lead workflow
├── JASWANTH_WORKFLOW.md               # IoT Lead workflow
├── AKASH_WORKFLOW.md                  # Backend Lead workflow
├── POSHITH_WORKFLOW.md                # Frontend Lead workflow
├── ADITI_WORKFLOW.md                  # Health & Insurance Lead workflow
│
├── ml/                                # 🔬 Machine Learning Module
│   │                                  #    Owner: Ramakrishna + Aditi
│   ├── detection/                     # YOLOv8 cattle face/muzzle detection
│   │   ├── train_detector.py          #   Training script
│   │   ├── predict.py                 #   Inference script
│   │   ├── data.yaml                  #   Dataset config
│   │   ├── datasets/                  #   Training images (gitignored)
│   │   │   ├── images/
│   │   │   │   ├── train/
│   │   │   │   └── val/
│   │   │   └── labels/
│   │   │       ├── train/
│   │   │       └── val/
│   │   └── weights/                   #   Trained model weights (gitignored)
│   │       └── best.pt
│   │
│   ├── recognition/                   # ArcFace embedding & matching
│   │   ├── train_embedding.py         #   ArcFace training
│   │   ├── inference.py               #   Generate embeddings
│   │   ├── face_matcher.py            #   Compare embeddings against DB
│   │   ├── gallery_builder.py         #   Build embedding gallery
│   │   └── weights/                   #   ArcFace model weights
│   │
│   ├── health/                        # Health condition detection (Aditi)
│   │   ├── train_health.py            #   Train health detection model
│   │   ├── predict_health.py          #   Health inference
│   │   ├── anomaly_detector.py        #   Sensor data anomaly detection
│   │   ├── data.yaml                  #   Health dataset config
│   │   ├── datasets/
│   │   └── weights/
│   │
│   ├── notebooks/                     # Jupyter notebooks for experiments
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_model_comparison.ipynb
│   │   └── 03_gradcam_analysis.ipynb
│   │
│   ├── utils/                         # Shared ML utilities
│   │   ├── __init__.py
│   │   ├── preprocessing.py           #   Image preprocessing
│   │   ├── augmentation.py            #   Data augmentation
│   │   └── evaluation.py              #   Metrics & evaluation
│   │
│   └── requirements.txt               # ML-specific dependencies
│
├── iot/                               # 📡 IoT Module
│   │                                  #    Owner: Jaswanth
│   ├── firmware/                      # ESP32 firmware (PlatformIO)
│   │   ├── src/
│   │   │   └── main.cpp               #   Main firmware code
│   │   ├── include/
│   │   │   ├── config.h               #   WiFi/MQTT credentials
│   │   │   └── sensors.h              #   Sensor pin definitions
│   │   ├── lib/                       #   Custom libraries
│   │   └── platformio.ini             #   PlatformIO config
│   │
│   ├── mqtt_worker/                   # Python MQTT subscriber service
│   │   ├── worker.py                  #   Main MQTT subscriber
│   │   ├── handlers.py                #   Message handlers per topic
│   │   ├── config.py                  #   Broker config
│   │   └── __init__.py
│   │
│   ├── simulation/                    # Sensor data simulator (for testing)
│   │   ├── sensor_simulator.py        #   Simulates ESP32 sensor data
│   │   ├── scenarios.json             #   Predefined test scenarios
│   │   └── __init__.py
│   │
│   └── requirements.txt               # IoT-specific dependencies
│
├── backend/                           # 🖥️ Backend Module
│   │                                  #    Owner: Akash
│   ├── app/
│   │   ├── __init__.py                #   Flask app factory (create_app)
│   │   ├── config.py                  #   Config classes (Dev/Prod/Test)
│   │   ├── extensions.py              #   PyMongo, JWT, SocketIO init
│   │   │
│   │   ├── routes/                    #   Flask Blueprints
│   │   │   ├── __init__.py            #     Register all blueprints
│   │   │   ├── cattle.py              #     /api/cattle — CRUD
│   │   │   ├── owner.py               #     /api/owners — CRUD
│   │   │   ├── sensor.py              #     /api/sensors — sensor data
│   │   │   ├── health.py              #     /api/health — health alerts
│   │   │   ├── insurance.py           #     /api/insurance — claims
│   │   │   ├── identification.py      #     /api/identify — face matching
│   │   │   └── auth.py                #     /api/auth — login/register
│   │   │
│   │   ├── models/                    #   Data schemas (Marshmallow)
│   │   │   ├── __init__.py
│   │   │   ├── cattle.py              #     Cattle schema
│   │   │   ├── owner.py               #     Owner schema
│   │   │   ├── sensor_data.py         #     Sensor reading schema
│   │   │   ├── health_alert.py        #     Health alert schema
│   │   │   └── insurance_claim.py     #     Insurance claim schema
│   │   │
│   │   ├── services/                  #   Business logic
│   │   │   ├── __init__.py
│   │   │   ├── identification_service.py  # Calls ML inference
│   │   │   ├── health_service.py      #     Health analysis
│   │   │   ├── insurance_service.py   #     Claim verification
│   │   │   └── mqtt_service.py        #     MQTT subscriber bridge
│   │   │
│   │   └── utils/                     #   Helpers
│   │       ├── __init__.py
│   │       ├── auth.py                #     JWT helpers
│   │       ├── helpers.py             #     Utility functions
│   │       └── validators.py          #     Custom validators
│   │
│   ├── tests/                         #   Unit + integration tests
│   │   ├── test_cattle.py
│   │   ├── test_auth.py
│   │   └── test_insurance.py
│   │
│   ├── requirements.txt               # Backend dependencies
│   └── run.py                         # Flask entry point
│
├── frontend/                          # 🎨 Frontend Module
│   │                                  #    Owner: Poshith
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── components/                #   Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── SensorCard.jsx
│   │   │   ├── AnimalCard.jsx
│   │   │   ├── HealthAlertCard.jsx
│   │   │   ├── InsuranceClaimCard.jsx
│   │   │   ├── MapView.jsx
│   │   │   ├── SensorChart.jsx
│   │   │   └── ImageUploader.jsx
│   │   │
│   │   ├── pages/                     #   Page-level components
│   │   │   ├── Dashboard.jsx          #     Main dashboard
│   │   │   ├── AnimalRegistry.jsx     #     Animal list + details
│   │   │   ├── AnimalDetail.jsx       #     Single animal view
│   │   │   ├── HealthAlerts.jsx       #     Health alert list
│   │   │   ├── InsuranceClaims.jsx    #     Insurance management
│   │   │   ├── LiveMap.jsx            #     GPS tracking map
│   │   │   ├── Identify.jsx           #     Upload image to identify
│   │   │   ├── Login.jsx              #     Login page
│   │   │   └── Register.jsx           #     Register page
│   │   │
│   │   ├── hooks/                     #   Custom React hooks
│   │   │   ├── useSensorData.js       #     Real-time sensor hook
│   │   │   ├── useSocket.js           #     WebSocket hook
│   │   │   └── useAuth.js             #     Auth hook
│   │   │
│   │   ├── services/                  #   API communication
│   │   │   ├── api.js                 #     Axios instance
│   │   │   ├── cattleService.js       #     Cattle API calls
│   │   │   ├── sensorService.js       #     Sensor API calls
│   │   │   └── authService.js         #     Auth API calls
│   │   │
│   │   ├── context/                   #   React context providers
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── utils/                     #   Helper functions
│   │   │   └── helpers.js
│   │   │
│   │   ├── App.jsx                    #   Root component
│   │   ├── App.css
│   │   └── main.jsx                   #   React entry point
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .env
│
├── insurance/                         # 🛡️ Insurance & Fraud Module
│   │                                  #    Owner: Aditi
│   ├── claim_verifier.py              #   Verify insurance claims
│   ├── fraud_detector.py              #   Detect fraudulent patterns
│   ├── subsidy_tracker.py             #   Track government subsidies
│   ├── geo_verifier.py                #   Geo-fence verification
│   ├── death_claim_handler.py         #   Death claim processing
│   └── requirements.txt
│
├── alerts/                            # 🔔 Alert & Notification Module
│   │                                  #    Owner: Aditi
│   ├── sms_alert.py                   #   SMS notifications (Twilio)
│   ├── email_alert.py                 #   Email notifications
│   ├── notification_manager.py        #   Central alert router
│   └── __init__.py
│
├── data/                              # 📁 Datasets (gitignored)
│   ├── raw/                           #   Raw collected images
│   ├── processed/                     #   Preprocessed data
│   └── annotations/                   #   YOLO annotation files
│
└── scripts/                           # 🔧 Utility Scripts
    ├── setup_env.py                   #   Auto-setup Python 3.12 venv
    ├── seed_db.py                     #   Seed MongoDB with sample data
    ├── export_model.py                #   Export models to ONNX
    └── download_dataset.py            #   Download/prepare datasets
```

---

## 4-Week Plan Overview

### Week 1: Foundation (Feb 11–17)

| Member          | Tasks                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **ALL**         | Install Python 3.12, create venv, clone repo, set up IDE                                                                               |
| **Ramakrishna** | Collect cattle face/muzzle dataset (500+ images), annotate with Roboflow, set up YOLOv8 training pipeline                              |
| **Jaswanth**    | Set up Mosquitto broker, design MQTT topic structure, build sensor simulator in Python, wire ESP32 prototype                           |
| **Akash**       | Initialize Flask app factory, design MongoDB schemas, set up docker-compose (MongoDB + Mosquitto), create base API routes              |
| **Poshith**     | Initialize Vite + React project, install dependencies (Recharts, Leaflet, Socket.IO), build Navbar + Sidebar + routing                 |
| **Aditi**       | Collect health condition images (wound, eye redness), annotate dataset, study insurance fraud patterns, design anomaly detection logic |

### Week 2: Core Development (Feb 18–24)

| Member          | Tasks                                                                                                                                                     |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ramakrishna** | Train YOLOv8 detector, train ArcFace embedding model, build face_matcher.py, test identification pipeline end-to-end                                      |
| **Jaswanth**    | Complete ESP32 firmware (GPS + Temp + Accel + Heart), MQTT publish from device, build Python mqtt_worker to subscribe and store in MongoDB                |
| **Akash**       | Complete all REST API routes (cattle CRUD, owner CRUD, sensor, health, insurance, auth), JWT authentication, connect with ML inference service            |
| **Poshith**     | Build Dashboard page (sensor cards + charts), AnimalRegistry page, LiveMap page with Leaflet, Identify page (image upload + result display)               |
| **Aditi**       | Train YOLOv8 health detector, build anomaly_detector.py for sensor data, implement claim_verifier.py and fraud_detector.py, build notification_manager.py |

### Week 3: Integration & Testing (Feb 25–Mar 3)

| Member          | Tasks                                                                                                                               |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **ALL**         | Integration testing — all modules talking to each other                                                                             |
| **Ramakrishna** | Integrate ML models with Flask API (identification_service.py), optimize model accuracy, run Grad-CAM explainability analysis       |
| **Jaswanth**    | End-to-end test: ESP32 → MQTT → MongoDB → Dashboard, refine sensor simulator scenarios, test real-time data flow                    |
| **Akash**       | Integrate all services (ML, IoT, Insurance), write API tests, set up Flask-SocketIO for real-time push to frontend                  |
| **Poshith**     | Connect all pages to live API, implement WebSocket real-time updates, build HealthAlerts + InsuranceClaims pages, responsive design |
| **Aditi**       | Integrate health detection with API, test fraud detection algorithm, implement SMS/email alerts, test geo-verification              |

### Week 4: Polish & Documentation (Mar 4–11)

| Member          | Tasks                                                                                                                        |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **ALL**         | Bug fixes, code cleanup, write documentation, prepare demo                                                                   |
| **Ramakrishna** | Write model evaluation report (accuracy, confusion matrix), create Jupyter notebooks for demonstration, document ML pipeline |
| **Jaswanth**    | Finalize IoT documentation, create hardware setup guide, ensure simulator covers all test scenarios                          |
| **Akash**       | API documentation, final integration testing, deploy backend (local/cloud), seed database with demo data                     |
| **Poshith**     | UI polish, loading states, error handling, mobile responsiveness, create demo walkthrough                                    |
| **Aditi**       | Write insurance module documentation, create sample fraud scenarios for demo, finalize alert system                          |

### Buffer: Final Prep (Mar 11–20)

| Activity       | Details                                      |
| -------------- | -------------------------------------------- |
| Demo rehearsal | Full system demo walkthrough (all 5 members) |
| Viva prep      | Each member prepares to explain their module |
| Presentation   | PowerPoint/slides with architecture diagrams |
| Report         | Final capstone report with all sections      |
| Edge cases     | Test with unusual inputs, error scenarios    |

---

## Python 3.12 Environment Setup (ALL MEMBERS)

```bash
# Step 1: Install Python 3.12
# Download from https://www.python.org/downloads/release/python-3120/
# During install: CHECK "Add Python to PATH"

# Step 2: Verify installation
python --version
# Output: Python 3.12.x

# Step 3: Clone the repository
git clone <repo-url>
cd cap

# Step 4: Create virtual environment
python -m venv venv

# Step 5: Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Step 6: Install common dependencies
pip install -r requirements-common.txt

# Step 7: Install module-specific dependencies
# Ramakrishna/Aditi:
pip install -r ml/requirements.txt
# Jaswanth:
pip install -r iot/requirements.txt
# Akash:
pip install -r backend/requirements.txt
# Poshith (Python deps only, frontend uses npm):
cd frontend && npm install
```

### requirements-common.txt

```
python-dotenv==1.0.1
numpy==1.26.4
```

---

## MongoDB Collections Design

| Collection         | Key Fields                                                                     | Used By            |
| ------------------ | ------------------------------------------------------------------------------ | ------------------ |
| `cattle`           | cattle_id, name, breed, age, owner_id, muzzle_embedding, photo_url, created_at | Akash, Ramakrishna |
| `owners`           | owner_id, name, phone, aadhaar, farm_location, cattle_ids                      | Akash              |
| `sensor_readings`  | cattle_id, timestamp, temperature, heart_rate, gps, activity_level             | Jaswanth, Akash    |
| `health_alerts`    | cattle_id, alert_type, severity, confidence, image_url, timestamp              | Aditi, Akash       |
| `insurance_claims` | claim_id, cattle_id, owner_id, type, status, verification_result               | Aditi, Akash       |
| `users`            | user_id, username, password_hash, role, created_at                             | Akash              |
| `embeddings`       | cattle_id, embedding_vector, model_version, created_at                         | Ramakrishna        |

---

## MQTT Topic Structure

```
livestock/{farm_id}/{cattle_id}/temperature     → float (°C)
livestock/{farm_id}/{cattle_id}/heartrate       → int (bpm)
livestock/{farm_id}/{cattle_id}/gps             → {lat, lng}
livestock/{farm_id}/{cattle_id}/activity        → {x, y, z accelerometer}
livestock/{farm_id}/{cattle_id}/status          → online/offline
livestock/alerts/{cattle_id}/health             → {alert_type, severity}
livestock/alerts/{cattle_id}/geofence           → {breach_type, location}
```

---

## API Endpoints Summary

| Method | Endpoint                   | Description                    | Owner               |
| ------ | -------------------------- | ------------------------------ | ------------------- |
| POST   | `/api/auth/register`       | Register new user              | Akash               |
| POST   | `/api/auth/login`          | Login, get JWT                 | Akash               |
| GET    | `/api/cattle`              | List all cattle                | Akash               |
| POST   | `/api/cattle`              | Register new cattle            | Akash               |
| GET    | `/api/cattle/<id>`         | Get cattle details             | Akash               |
| PUT    | `/api/cattle/<id>`         | Update cattle info             | Akash               |
| DELETE | `/api/cattle/<id>`         | Remove cattle                  | Akash               |
| POST   | `/api/identify`            | Upload image → identify cattle | Akash + Ramakrishna |
| GET    | `/api/sensors/<cattle_id>` | Get sensor readings            | Akash + Jaswanth    |
| GET    | `/api/sensors/latest`      | Get latest readings all cattle | Akash + Jaswanth    |
| GET    | `/api/health/alerts`       | List health alerts             | Akash + Aditi       |
| POST   | `/api/health/detect`       | Upload image → health check    | Akash + Aditi       |
| GET    | `/api/insurance/claims`    | List insurance claims          | Akash + Aditi       |
| POST   | `/api/insurance/verify`    | Verify a claim                 | Akash + Aditi       |
| GET    | `/api/owners`              | List owners                    | Akash               |
| POST   | `/api/owners`              | Register owner                 | Akash               |

---

## Cross-Team Dependencies

```
Ramakrishna ──(trained models)──▶ Akash (backend loads models for inference)
Jaswanth ──(MQTT data)──▶ Akash (backend stores sensor data in MongoDB)
Akash ──(REST API)──▶ Poshith (frontend calls API endpoints)
Akash ──(WebSocket)──▶ Poshith (real-time sensor updates)
Aditi ──(health models)──▶ Akash (backend uses for health detection API)
Aditi ──(fraud logic)──▶ Akash (backend uses for insurance verification API)
Ramakrishna ──(embedding format)──▶ Aditi (shared ML utilities)
Jaswanth ──(sensor data format)──▶ Aditi (anomaly detection input)
```

### Integration Checkpoints

| Date   | Checkpoint                                                        |
| ------ | ----------------------------------------------------------------- |
| Feb 17 | All environments set up, Git repo working, basic folder structure |
| Feb 24 | Individual modules working standalone                             |
| Mar 1  | ML models callable from Flask API                                 |
| Mar 3  | Full pipeline: Sensor → Backend → Frontend                        |
| Mar 7  | Insurance & fraud detection integrated                            |
| Mar 11 | Complete system with documentation                                |
| Mar 20 | Submission-ready with presentation                                |

---

## Git Workflow

```
main
 └── develop
      ├── feature/ramakrishna-detection
      ├── feature/ramakrishna-recognition
      ├── feature/jaswanth-firmware
      ├── feature/jaswanth-mqtt-worker
      ├── feature/akash-api
      ├── feature/akash-auth
      ├── feature/poshith-dashboard
      ├── feature/poshith-pages
      ├── feature/aditi-health-detection
      └── feature/aditi-insurance
```

**Rules:**

1. Each member works on their own `feature/` branch
2. PR to `develop` branch after completing a feature
3. Code review by at least 1 other member before merge
4. `main` branch only for stable, tested releases
5. Commit messages: `[Module] Description` (e.g., `[ML] Add YOLOv8 training script`)

---

## Viva Talking Points

> _"We built a biometric identity system for livestock — similar to Aadhaar for humans — integrated with IoT-based real-time monitoring to prevent fraud in government insurance and subsidy programs."_

Each member should be able to explain:

1. **Their module** in depth (architecture, tech choices, challenges)
2. **How their module connects** to the rest of the system
3. **The real-world problem** this solves
4. **Technical decisions** (why YOLOv8? why Flask? why MongoDB?)
5. **Future improvements** (blockchain records, edge deployment, mobile app)
