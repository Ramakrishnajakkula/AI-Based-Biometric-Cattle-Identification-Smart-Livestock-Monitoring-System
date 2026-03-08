# AI-Based Biometric Cattle Identification & Smart Livestock Monitoring System

> A capstone project that combines Deep Learning, Computer Vision, and a full-stack web dashboard for biometric cattle identification, real-time health monitoring, and insurance fraud prevention.

---

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Proposed Solution](#proposed-solution)
3. [Key Features](#key-features)
4. [System Architecture](#system-architecture)
5. [Tech Stack](#tech-stack)
6. [Team](#team)
7. [Project Structure](#project-structure)
8. [Quick Start](#quick-start)
9. [API Endpoints](#api-endpoints)
10. [Demo Credentials](#demo-credentials)
11. [Screenshots](#screenshots)

---

## Problem Statement

India has over **300 million** cattle, forming the backbone of the rural economy. Despite this, livestock management still relies heavily on manual tagging methods (ear tags, branding) that are **easily tampered, duplicated, or lost**. This gap leads to:

- **Insurance fraud** — fake or duplicate claims on the same animal.
- **Delayed disease detection** — sick animals go unnoticed until an outbreak spreads.
- **Theft & identity disputes** — no tamper-proof way to verify ownership.
- **Lack of real-time monitoring** — farmers discover problems only during manual inspections.

There is no widely adopted, non-invasive, technology-driven approach for uniquely identifying and continuously monitoring individual cattle in India.

---

## Proposed Solution

This system introduces a **non-invasive biometric identification pipeline** (muzzle print recognition, analogous to human fingerprints) combined with a **smart livestock monitoring dashboard**:

1. **Biometric Identification** — A YOLOv8 object detector localises the cattle muzzle in a photograph, then an ArcFace-based embedding network generates a unique 512-D feature vector. This vector is matched against a gallery of registered cattle to confirm identity with high accuracy.

2. **Health Monitoring** — Sensor readings (temperature, heart rate, activity level) are tracked continuously. An anomaly-detection model flags abnormal readings (e.g., fever, low activity) and generates real-time health alerts.

3. **GPS Tracking** — Each animal's geolocation is plotted on a live map, enabling geofence-breach detection and anti-theft alerts.

4. **Insurance Fraud Prevention** — When an insurance claim is submitted, the system cross-checks the cattle's biometric identity, health history, GPS trail, and claim history to produce a fraud-risk score, preventing duplicate or fabricated claims.

5. **Web Dashboard** — A React-based single-page application gives farmers, veterinarians, and insurance officers a unified view of the entire herd — stats, alerts, claims, maps, and identification — all in one place.

---

## Key Features

| Feature | Description |
|---|---|
| **Muzzle Biometric ID** | Upload a cattle face photo → YOLOv8 detects muzzle → ArcFace embedding → gallery match → returns identity with confidence score |
| **Health Alerts** | Automated anomaly detection on temperature, heart rate and activity; severity levels (high / medium / low) with one-click resolve |
| **Live GPS Map** | Real-time Leaflet map showing all cattle positions (Hyderabad region demo data), auto-refreshes every 5 seconds |
| **Insurance Claims** | Submit, review (pending → under_review → approved/rejected) and verify claims with integrated fraud scoring |
| **Dashboard Analytics** | Summary cards (total cattle, healthy count, active alerts, pending claims), herd health pie chart, recent alerts table |
| **JWT Authentication** | Secure login/register with role-based access (admin, farmer, veterinarian) |
| **Sensor History Charts** | Interactive Recharts line graphs for temperature and heart rate over the last 24 hours per animal |

---

## System Architecture

```
┌─────────────┐       REST / JSON        ┌──────────────────┐
│  React 18   │  ◄─────────────────────►  │  Flask 3.x API   │
│  (Vite 5)   │    /api/* via proxy       │  (Python 3.12)   │
│  Port 3000  │                           │  Port 5000       │
└─────────────┘                           └────────┬─────────┘
       │                                           │
       │  Ant Design UI                   In-Memory Data Store
       │  Recharts graphs                 (data_store.py)
       │  Leaflet maps                    ┌────────┴─────────┐
       │                                  │ CATTLE list (5)   │
       │                                  │ HEALTH_ALERTS (5) │
       │                                  │ INSURANCE_CLAIMS  │
       │                                  │ GPS positions     │
       │                                  │ Sensor generators │
       │                                  └──────────────────┘
       │
  ┌────┴────────────────────────────────────┐
  │  ML Pipeline (ml/)                       │
  │  ├── YOLOv8 detection (muzzle localise)  │
  │  ├── ArcFace recognition (512-D embed)   │
  │  └── Anomaly detector (health scoring)   │
  └──────────────────────────────────────────┘
```

> **Note:** The current demo runs entirely self-contained with **hardcoded in-memory data** — no MongoDB, MQTT broker, or IoT hardware is required. The ML modules under `ml/` contain the training and inference code that can be integrated when model weights are ready.

---

## Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| Python 3.12 | Core language |
| Flask 3.1.0 | REST API framework |
| flask-jwt-extended | JWT authentication |
| flask-cors | Cross-Origin Resource Sharing |
| bcrypt | Password hashing |
| Pillow | Image processing for uploads |
| NumPy | Numerical operations |

### Frontend

| Technology | Purpose |
|---|---|
| React 18 | UI library |
| Vite 5 | Build tool & dev server |
| Ant Design 5 | UI component library (tables, forms, cards, modals) |
| Recharts | Interactive charts (line, pie) |
| React-Leaflet + Leaflet | GPS map visualisation |
| Axios | HTTP client with JWT interceptor |
| React Router v6 | Client-side routing |
| Day.js | Date formatting |

### ML / AI (Training Code)

| Technology | Purpose |
|---|---|
| YOLOv8 (Ultralytics) | Cattle muzzle detection |
| ArcFace / ResNet-50 | Biometric embedding extraction |
| Scikit-learn | Anomaly detection (Isolation Forest) |
| OpenCV | Image preprocessing & augmentation |

---

## Team

| Member | Role | Responsibilities |
|---|---|---|
| **Ramakrishna** | AI/ML Lead | YOLOv8 muzzle detection, ArcFace recognition training, dataset preparation (`ml/detection/`, `ml/recognition/`) |
| **Jaswanth** | IoT & Edge Lead | Sensor simulation, MQTT worker, ESP32 firmware design (`iot/`) |
| **Akash** | Backend & API Lead | Flask REST API, authentication, route handlers, in-memory data store (`backend/`) |
| **Poshith** | Frontend & Dashboard | React SPA, Ant Design UI, charts, maps, all page components (`frontend/`) |
| **Aditi** | Health & Insurance | Health anomaly model, insurance claim verification, fraud detection, alerting (`ml/health/`, `insurance/`, `alerts/`) |

---

## Project Structure

```
cap/
├── backend/                    # Flask REST API
│   ├── run.py                  # Entry point — starts server on port 5000
│   ├── requirements.txt        # Python dependencies
│   └── app/
│       ├── __init__.py         # App factory (creates Flask app, registers blueprints)
│       ├── config.py           # Configuration (JWT secret, upload paths)
│       ├── extensions.py       # JWTManager initialisation
│       ├── data_store.py       # ★ Hardcoded in-memory data (cattle, alerts, claims, sensors)
│       ├── routes/
│       │   ├── auth.py         # POST /api/auth/login, /register, GET /profile
│       │   ├── cattle.py       # CRUD /api/cattle/
│       │   ├── sensors.py      # GET /api/sensors/<id>/latest, /history, /gps
│       │   ├── health.py       # GET /api/health/alerts, PUT /resolve
│       │   ├── insurance.py    # CRUD /api/insurance/claims, POST /verify
│       │   ├── identify.py     # POST /api/identify/ (image upload → demo match)
│       │   └── dashboard.py    # GET /api/dashboard/stats, /recent-alerts
│       ├── models/             # Marshmallow schemas
│       ├── services/           # ML service stubs
│       └── utils/              # Helper functions
│
├── frontend/                   # React 18 SPA (Vite)
│   ├── index.html              # HTML entry point
│   ├── package.json            # npm dependencies
│   ├── vite.config.js          # Dev server (port 3000) + proxy to backend
│   └── src/
│       ├── main.jsx            # React root with BrowserRouter + AuthProvider
│       ├── App.jsx             # Route definitions + ProtectedRoute wrapper
│       ├── index.css           # Global styles + Leaflet fix
│       ├── context/
│       │   └── AuthContext.jsx  # JWT token management via localStorage
│       ├── services/
│       │   ├── api.js           # Axios instance with JWT interceptor
│       │   ├── authService.js   # login, register, getProfile
│       │   ├── cattleService.js # list, getById, register, update, delete
│       │   ├── sensorService.js # getLatest, getHistory, getGpsPositions
│       │   └── dashboardService.js # getStats, getRecentAlerts
│       ├── components/
│       │   └── Layout/
│       │       └── AppLayout.jsx # Sidebar + Header + Content layout
│       └── pages/
│           ├── Login.jsx        # Login form with demo credentials
│           ├── Dashboard.jsx    # Stats cards + pie chart + alert table
│           ├── AnimalList.jsx   # Cattle table with health tags
│           ├── AnimalDetail.jsx # Cattle info + sensor stat cards + charts
│           ├── HealthAlerts.jsx # Alert table with severity filter + resolve
│           ├── InsuranceClaims.jsx # Claims table + new claim modal + verify
│           ├── LiveMap.jsx      # Leaflet map with polling GPS markers
│           └── IdentifyCattle.jsx # Image upload → biometric match result
│
├── ml/                         # Machine Learning modules
│   ├── detection/              # YOLOv8 muzzle detector (train + predict)
│   ├── recognition/            # ArcFace embedding (train + match)
│   ├── health/                 # Anomaly detection (Isolation Forest)
│   ├── utils/                  # Augmentation, preprocessing, evaluation
│   └── notebooks/              # Jupyter experiments
│
├── iot/                        # IoT & Simulation
│   ├── firmware/               # ESP32 PlatformIO project
│   ├── mqtt_worker/            # MQTT message handlers
│   └── simulation/             # Sensor data simulator
│
├── insurance/                  # Fraud detection & claim verification
├── alerts/                     # Email & SMS notification manager
├── scripts/                    # DB seeding & setup utilities
├── data/                       # Raw / processed datasets & annotations
├── docs/                       # Additional documentation
└── docker-compose.yml          # MongoDB + Mosquitto (optional)
```

---

## Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+** and **npm**

### 1. Clone the repository

```bash
git clone <repo-url>
cd cap
```

### 2. Start the Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

The API server starts at **http://localhost:5000**. No database or external service is needed — all data is served from the in-memory store.

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard opens at **http://localhost:3000**. Vite automatically proxies all `/api/*` requests to the backend.

### 4. Open the App

Visit **http://localhost:3000** in your browser. You will see the login page with pre-filled demo credentials — just click **Login**.

---

## API Endpoints

All endpoints (except login/register) require a JWT token in the `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/login` | Login → returns JWT token |
| `POST` | `/api/auth/register` | Register new user |
| `GET` | `/api/auth/profile` | Get current user profile |
| `GET` | `/api/dashboard/stats` | Dashboard summary (total cattle, healthy, alerts, claims) |
| `GET` | `/api/dashboard/recent-alerts` | Last 10 health alerts |
| `GET` | `/api/cattle/` | List all cattle (filter by `?breed=` or `?status=`) |
| `GET` | `/api/cattle/<id>` | Get single cattle details |
| `POST` | `/api/cattle/` | Register new cattle |
| `PUT` | `/api/cattle/<id>` | Update cattle record |
| `DELETE` | `/api/cattle/<id>` | Delete cattle record |
| `GET` | `/api/sensors/<id>/latest` | Latest sensor readings for a cattle |
| `GET` | `/api/sensors/<id>/history` | Sensor history (`?type=temperature&hours=24`) |
| `GET` | `/api/sensors/gps` | GPS positions for all cattle |
| `GET` | `/api/health/alerts` | Health alerts (filter by `?severity=` or `?status=`) |
| `GET` | `/api/health/alerts/<cattle_id>` | Alerts for specific cattle |
| `PUT` | `/api/health/alerts/<id>/resolve` | Mark alert as resolved |
| `GET` | `/api/insurance/claims` | List all insurance claims |
| `POST` | `/api/insurance/claims` | Submit a new claim |
| `GET` | `/api/insurance/claims/<id>` | Get claim details |
| `POST` | `/api/insurance/claims/<id>/verify` | Trigger fraud verification |
| `POST` | `/api/identify/` | Upload image → biometric cattle identification |

---

## Demo Credentials

| Email | Password | Role |
|---|---|---|
| `admin@cattle.com` | `admin123` | Admin |
| `rajesh@cattle.com` | `admin123` | Farmer |

The demo ships with **5 registered cattle** (Lakshmi, Ganga, Nandi, Kamadhenu, Surabhi), **5 health alerts**, and **3 insurance claims** pre-loaded in memory.

---

## Screenshots

### Login Page
Branded login form with pre-filled demo credentials and gradient background.

![Login Page](screenshorts_ui/Screenshot%202026-03-08%20143447.png)

---

### Dashboard
Summary stat cards (Total Cattle, Healthy, Active Alerts, Pending Claims), herd health pie chart, and recent alerts table.

![Dashboard](screenshorts_ui/Screenshot%202026-03-08%20143503.png)

---


### Animal Detail
Individual cattle information card with live sensor statistics (temperature, heart rate, activity) and interactive 24-hour history charts.

![Animal Detail](screenshorts_ui/Screenshot%202026-03-08%20143513.png)

---

### Health Alerts
Filterable alert table with severity badges (High / Medium / Low) and one-click resolve action.

![Health Alerts](screenshorts_ui/Screenshot%202026-03-08%20143513.png)

---

### Insurance Claims
Claims management table with status tags (Pending / Under Review / Approved), "New Claim" modal, and "Verify" fraud-check action.

![Insurance Claims](screenshorts_ui/Screenshot%202026-03-08%20143525.png)

---

### Live GPS Map
OpenStreetMap with cattle markers near Hyderabad that auto-refresh every 5 seconds.

![Live Map](screenshorts_ui/Screenshot%202026-03-08%20143538.png)

---

### Identify Cattle
Upload a muzzle/face photograph to identify the cattle using biometric matching — shows matched cattle name, breed, and confidence score.

![Identify Cattle](screenshorts_ui/Screenshot%202026-03-08%20143620.png)



---

## License

This project is developed as a capstone project for academic purposes.
