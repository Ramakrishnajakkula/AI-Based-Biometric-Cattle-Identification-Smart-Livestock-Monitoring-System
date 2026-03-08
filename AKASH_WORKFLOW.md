# Akash — Backend & API Lead Workflow

## Role: Flask REST API + MongoDB + System Integration

**Member:** Akash
**Module:** `backend/` (Flask app, routes, models, services)
**Python Version:** 3.12
**Primary Tech:** Flask 3.x, PyMongo, Flask-SocketIO, Flask-JWT-Extended, Marshmallow

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   AKASH's BACKEND ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │  FLASK APPLICATION (App Factory Pattern)                          │   │
│  │                                                                    │   │
│  │  create_app()                                                      │   │
│  │  ├── Config (Dev / Prod / Test)                                    │   │
│  │  ├── Extensions (PyMongo, JWT, SocketIO, CORS)                     │   │
│  │  └── Blueprints (Routes)                                           │   │
│  │                                                                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  ROUTES (Flask Blueprints)                                   │   │   │
│  │  │                                                               │   │   │
│  │  │  /api/auth/         ──▶  auth.py        (Login, Register)    │   │   │
│  │  │  /api/cattle/       ──▶  cattle.py      (CRUD operations)    │   │   │
│  │  │  /api/owners/       ──▶  owner.py       (Owner management)   │   │   │
│  │  │  /api/sensors/      ──▶  sensor.py      (Sensor data query)  │   │   │
│  │  │  /api/health/       ──▶  health.py      (Health alerts)      │   │   │
│  │  │  /api/insurance/    ──▶  insurance.py   (Claims & fraud)     │   │   │
│  │  │  /api/identify/     ──▶  identification.py (Face matching)   │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  SERVICES (Business Logic)                                   │   │   │
│  │  │                                                               │   │   │
│  │  │  identification_service.py  ←── Calls Ramakrishna's ML model │   │   │
│  │  │  health_service.py          ←── Calls Aditi's health model   │   │   │
│  │  │  insurance_service.py       ←── Calls Aditi's fraud logic    │   │   │
│  │  │  mqtt_service.py            ←── Bridge to Jaswanth's worker  │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  MODELS (Marshmallow Schemas)                                │   │   │
│  │  │                                                               │   │   │
│  │  │  cattle.py       → CattleSchema (validate cattle data)       │   │   │
│  │  │  owner.py        → OwnerSchema                               │   │   │
│  │  │  sensor_data.py  → SensorDataSchema                          │   │   │
│  │  │  health_alert.py → HealthAlertSchema                         │   │   │
│  │  │  insurance.py    → InsuranceClaimSchema                      │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                           │           │                                  │
│               ┌───────────┘           └──────────┐                      │
│               ▼                                  ▼                      │
│  ┌────────────────────────┐     ┌────────────────────────────────┐      │
│  │  MongoDB Database      │     │  Flask-SocketIO                │      │
│  │                        │     │  (Real-time push)              │      │
│  │  Collections:          │     │                                │      │
│  │  ├── cattle            │     │  Events:                       │      │
│  │  ├── owners            │     │  ├── sensor_update             │      │
│  │  ├── sensor_readings   │     │  ├── health_alert              │      │
│  │  ├── health_alerts     │     │  ├── geofence_breach           │      │
│  │  ├── insurance_claims  │     │  └── device_status             │      │
│  │  ├── users             │     │                                │      │
│  │  └── embeddings        │     │  Port: 5000                    │      │
│  │                        │     │  WebSocket: /socket.io          │      │
│  │  Port: 27017           │     └────────────────────────────────┘      │
│  └────────────────────────┘                                             │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│  REQUEST FLOW                                                            │
│                                                                          │
│  Client ──HTTP──▶ Route ──▶ Validate (Marshmallow) ──▶ Service ──▶ DB   │
│  Client ◀──JSON──◀ Route ◀── Format Response ◀── Service ◀── DB         │
│                                                                          │
│  REAL-TIME FLOW                                                          │
│  MQTT Worker ──▶ Flask-SocketIO ──WebSocket──▶ React Frontend            │
└──────────────────────────────────────────────────────────────────────────┘
```

### MongoDB Schema Design

```
┌──────────────────────────────────────────────────────────────────┐
│  DATABASE: cattle_monitoring                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  COLLECTION: cattle                                               │
│  {                                                                │
│    "_id": ObjectId,                                               │
│    "cattle_id": "CTL-001",                                        │
│    "name": "Lakshmi",                                             │
│    "breed": "Gir",                                                │
│    "age_years": 4,                                                │
│    "gender": "female",                                            │
│    "owner_id": "OWN-001",                                         │
│    "photo_url": "/uploads/cattle/CTL-001.jpg",                    │
│    "muzzle_embedding": [0.12, -0.34, ...],  // 512-d vector       │
│    "insurance": {                                                 │
│      "policy_number": "INS-2026-001",                             │
│      "provider": "NAIS",                                          │
│      "insured_value": 50000,                                      │
│      "status": "active"                                           │
│    },                                                             │
│    "vaccination_records": [...],                                   │
│    "farm_id": "FARM-01",                                          │
│    "created_at": ISODate,                                         │
│    "updated_at": ISODate                                          │
│  }                                                                │
│                                                                   │
│  COLLECTION: owners                                               │
│  {                                                                │
│    "_id": ObjectId,                                               │
│    "owner_id": "OWN-001",                                         │
│    "name": "Raju",                                                │
│    "phone": "+91-9876543210",                                     │
│    "aadhaar": "XXXX-XXXX-1234",                                   │
│    "farm_location": {"lat": 17.385, "lng": 78.486},               │
│    "farm_id": "FARM-01",                                          │
│    "cattle_ids": ["CTL-001", "CTL-002"],                          │
│    "created_at": ISODate                                          │
│  }                                                                │
│                                                                   │
│  COLLECTION: sensor_readings                                      │
│  {                                                                │
│    "_id": ObjectId,                                               │
│    "cattle_id": "CTL-001",                                        │
│    "farm_id": "FARM-01",                                          │
│    "sensor_type": "temperature",                                  │
│    "data": {"value": 38.5, "unit": "celsius"},                    │
│    "device_id": "ESP32-FARM01-CTL001",                            │
│    "timestamp": ISODate,                                          │
│    "received_at": ISODate                                         │
│  }                                                                │
│                                                                   │
│  COLLECTION: health_alerts                                        │
│  {                                                                │
│    "_id": ObjectId,                                               │
│    "cattle_id": "CTL-001",                                        │
│    "alert_type": "fever",                                         │
│    "severity": "high",                                            │
│    "source": "sensor" | "vision",                                 │
│    "details": {"temperature": 40.1, "threshold": 39.5},           │
│    "image_url": "/uploads/health/alert-001.jpg",                  │
│    "resolved": false,                                             │
│    "timestamp": ISODate                                           │
│  }                                                                │
│                                                                   │
│  COLLECTION: insurance_claims                                     │
│  {                                                                │
│    "_id": ObjectId,                                               │
│    "claim_id": "CLM-001",                                         │
│    "cattle_id": "CTL-001",                                        │
│    "owner_id": "OWN-001",                                         │
│    "claim_type": "death" | "illness" | "theft",                   │
│    "claimed_amount": 50000,                                       │
│    "verification": {                                              │
│      "face_verified": true,                                       │
│      "geo_verified": true,                                        │
│      "fraud_score": 0.12,                                         │
│      "status": "approved" | "rejected" | "pending"                │
│    },                                                             │
│    "created_at": ISODate                                          │
│  }                                                                │
│                                                                   │
│  COLLECTION: users                                                │
│  {                                                                │
│    "_id": ObjectId,                                               │
│    "username": "admin",                                           │
│    "password_hash": "bcrypt...",                                   │
│    "role": "admin" | "farmer" | "inspector",                      │
│    "created_at": ISODate                                          │
│  }                                                                │
│                                                                   │
│  INDEXES:                                                         │
│    cattle.cattle_id          (unique)                              │
│    sensor_readings.cattle_id (compound with timestamp)             │
│    sensor_readings.timestamp (TTL index: 30 days)                  │
│    health_alerts.cattle_id                                        │
│    insurance_claims.claim_id (unique)                              │
│    users.username            (unique)                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Folder Structure (Akash's Files)

```
cap/
├── backend/
│   ├── app/
│   │   ├── __init__.py                # create_app() factory function
│   │   ├── config.py                  # Dev/Prod/Test config classes
│   │   ├── extensions.py             # PyMongo, JWT, SocketIO, CORS init
│   │   │
│   │   ├── routes/                    # Flask Blueprints
│   │   │   ├── __init__.py            #   register_blueprints() function
│   │   │   ├── auth.py                #   POST /register, /login
│   │   │   ├── cattle.py              #   GET/POST/PUT/DELETE /api/cattle
│   │   │   ├── owner.py               #   GET/POST /api/owners
│   │   │   ├── sensor.py              #   GET /api/sensors/<id>, /latest
│   │   │   ├── health.py              #   GET/POST /api/health
│   │   │   ├── insurance.py           #   GET/POST /api/insurance
│   │   │   └── identification.py      #   POST /api/identify
│   │   │
│   │   ├── models/                    # Marshmallow schemas
│   │   │   ├── __init__.py
│   │   │   ├── cattle.py              #   CattleSchema
│   │   │   ├── owner.py               #   OwnerSchema
│   │   │   ├── sensor_data.py         #   SensorDataSchema
│   │   │   ├── health_alert.py        #   HealthAlertSchema
│   │   │   └── insurance_claim.py     #   InsuranceClaimSchema
│   │   │
│   │   ├── services/                  # Business logic / ML bridges
│   │   │   ├── __init__.py
│   │   │   ├── identification_service.py  # Loads Ramakrishna's model
│   │   │   ├── health_service.py      #     Loads Aditi's model
│   │   │   ├── insurance_service.py   #     Fraud detection wrapper
│   │   │   └── mqtt_service.py        #     SocketIO bridge from MQTT
│   │   │
│   │   └── utils/                     # Helpers
│   │       ├── __init__.py
│   │       ├── auth.py                #   Password hashing, JWT
│   │       ├── helpers.py             #   ID generators, date utils
│   │       ├── validators.py          #   Custom validations
│   │       └── file_upload.py         #   Image upload handling
│   │
│   ├── tests/                         # Unit & integration tests
│   │   ├── __init__.py
│   │   ├── conftest.py                #   Pytest fixtures
│   │   ├── test_cattle.py             #   Cattle CRUD tests
│   │   ├── test_auth.py               #   Auth tests
│   │   ├── test_insurance.py          #   Insurance tests
│   │   └── test_identification.py     #   Identification tests
│   │
│   ├── uploads/                       #   Uploaded images (gitignored)
│   │   ├── cattle/
│   │   └── health/
│   │
│   ├── requirements.txt               # Backend dependencies
│   ├── run.py                         # Entry point: python run.py
│   └── .env                           # Environment variables (gitignored)
```

---

## Dependencies (backend/requirements.txt)

```txt
# Web Framework
Flask==3.1.0
flask-cors==5.0.0
flask-socketio==5.4.1
eventlet==0.37.0

# Authentication
Flask-JWT-Extended==4.7.1
bcrypt==4.2.1

# Database
pymongo==4.10.1

# Validation
marshmallow==3.23.1

# MQTT Bridge
paho-mqtt==2.1.0

# Image Handling
Pillow==10.4.0

# Utilities
python-dotenv==1.0.1
numpy==1.26.4

# Testing
pytest==8.3.2
pytest-flask==1.3.0
```

---

## Setup Instructions

```bash
# 1. Python 3.12 environment
cd cap
python -m venv venv
venv\Scripts\activate

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Start MongoDB (if not already running)
docker run -d --name mongodb -p 27017:27017 mongo:7

# 4. Create .env file
# backend/.env
# MONGO_URI=mongodb://localhost:27017/cattle_monitoring
# JWT_SECRET_KEY=your-secret-key-change-in-production
# MQTT_BROKER=localhost
# MQTT_PORT=1883
# FLASK_ENV=development
# FLASK_DEBUG=1

# 5. Run Flask server
cd backend
python run.py
# Server starts at http://localhost:5000

# 6. Test API
curl http://localhost:5000/api/cattle
# Should return: {"cattle": [], "total": 0}

# 7. Run tests
cd backend
pytest tests/ -v
```

---

## 4-Week Schedule

### WEEK 1 (Feb 11–17): Flask Setup + MongoDB + Base Routes

| Day | Date   | Tasks                                                                                    | Deliverable                |
| --- | ------ | ---------------------------------------------------------------------------------------- | -------------------------- |
| Tue | Feb 11 | Set up Python 3.12 venv. Install Flask, PyMongo, dependencies. Start MongoDB Docker      | Environment ready          |
| Wed | Feb 12 | Create Flask app factory (`__init__.py`), config classes, extensions setup               | `create_app()` working     |
| Thu | Feb 13 | Design MongoDB schemas (all 6 collections). Set up indexes. Create Marshmallow schemas   | All model schemas defined  |
| Fri | Feb 14 | Build `cattle.py` routes — full CRUD (GET list, GET by ID, POST, PUT, DELETE)            | `/api/cattle` CRUD working |
| Sat | Feb 15 | Build `owner.py` routes. Build `auth.py` — register + login with JWT                     | Auth + owner routes done   |
| Sun | Feb 16 | Build `sensor.py` routes — GET latest readings, GET history by cattle_id with pagination | Sensor routes ready        |
| Mon | Feb 17 | Build `health.py` and `insurance.py` base routes (CRUD for alerts & claims)              | ✅ All base routes created |

**Coordination:**

- Agree with **Jaswanth**: MongoDB document format for `sensor_readings`
- Agree with **Ramakrishna**: Cattle registration flow (with or without muzzle embedding)
- Agree with **Poshith**: API response format (standardize JSON structure)

### Standard API Response Format:

```json
// Success
{
    "success": true,
    "data": { ... },
    "message": "Cattle registered successfully"
}

// Error
{
    "success": false,
    "error": "Cattle not found",
    "code": 404
}

// List
{
    "success": true,
    "data": [ ... ],
    "total": 25,
    "page": 1,
    "per_page": 10
}
```

---

### WEEK 2 (Feb 18–24): Services + File Upload + SocketIO

| Day | Date   | Tasks                                                                                            | Deliverable                      |
| --- | ------ | ------------------------------------------------------------------------------------------------ | -------------------------------- |
| Tue | Feb 18 | Build `identification_service.py` — wrapper that loads Ramakrishna's ML model and runs inference | Identification service ready     |
| Wed | Feb 19 | Build `identification.py` route — POST image → detect → embed → match → return cattle ID         | `/api/identify` endpoint working |
| Thu | Feb 20 | Build `file_upload.py` utility — handle multipart image uploads, save to `uploads/` folder       | Image upload working             |
| Fri | Feb 21 | Build `health_service.py` — wrapper for Aditi's health detection model                           | Health detection API             |
| Sat | Feb 22 | Build `insurance_service.py` — wrapper for Aditi's fraud detection + claim verification          | Insurance verification API       |
| Sun | Feb 23 | Set up Flask-SocketIO — bridge MQTT sensor data to WebSocket events for frontend                 | Real-time push working           |
| Mon | Feb 24 | Build `mqtt_service.py` — subscribe to MQTT in background thread, forward to SocketIO            | ✅ Full backend functional       |

**Coordination:**

- Get from **Ramakrishna**: `identify_cattle()` function, model weights path
- Get from **Aditi**: `detect_health()` and `verify_claim()` function interfaces
- Share with **Poshith**: Complete API documentation (all endpoints, request/response formats)

---

### WEEK 3 (Feb 25–Mar 3): Integration & Testing

| Day | Date   | Tasks                                                                             | Deliverable                    |
| --- | ------ | --------------------------------------------------------------------------------- | ------------------------------ |
| Tue | Feb 25 | Integration with Ramakrishna's ML — test `/api/identify` with real model          | ML integration verified        |
| Wed | Feb 26 | Integration with Jaswanth's MQTT — test sensor data flow end-to-end               | IoT integration verified       |
| Thu | Feb 27 | Integration with Aditi's modules — test health detection + insurance verification | Insurance integration verified |
| Fri | Feb 28 | Integration with Poshith's frontend — CORS, response format, WebSocket            | Frontend integration verified  |
| Sat | Mar 1  | Write unit tests — cattle CRUD, auth, identification                              | `tests/` directory populated   |
| Sun | Mar 2  | Write integration tests — full pipeline scenarios                                 | Pipeline tests passing         |
| Mon | Mar 3  | Fix integration bugs found by team. Stress test API with concurrent requests      | ✅ Stable integrated backend   |

**Coordination:**

- Debug sessions with ALL team members
- API response format adjustments based on Poshith's frontend needs

---

### WEEK 4 (Mar 4–11): Polish & Documentation

| Day | Date   | Tasks                                                                                | Deliverable           |
| --- | ------ | ------------------------------------------------------------------------------------ | --------------------- |
| Tue | Mar 4  | API documentation — document all 16+ endpoints with request/response examples        | API spec complete     |
| Wed | Mar 5  | Seed database script (`seed_db.py`) — populate with 20 cattle, 5 owners, sample data | Demo data ready       |
| Thu | Mar 6  | Error handling improvements — proper HTTP codes, validation messages                 | Robust error handling |
| Fri | Mar 7  | Add pagination to all list endpoints, add search/filter to cattle listing            | Performance features  |
| Sat | Mar 8  | Security audit — verify JWT, password hashing, input sanitization                    | Security hardened     |
| Sun | Mar 9  | Final testing with full team demo walkthrough                                        | System verified       |
| Mon | Mar 11 | Code cleanup, docstrings, final commit                                               | ✅ Complete           |

---

## Complete API Endpoint Reference

| Method | Endpoint                   | Body/Params                             | Response                          | Auth        |
| ------ | -------------------------- | --------------------------------------- | --------------------------------- | ----------- |
| POST   | `/api/auth/register`       | `{username, password, role}`            | `{token, user}`                   | No          |
| POST   | `/api/auth/login`          | `{username, password}`                  | `{token, user}`                   | No          |
| GET    | `/api/cattle`              | `?page=1&per_page=10&breed=Gir`         | `{data: [...], total}`            | Yes         |
| GET    | `/api/cattle/<cattle_id>`  | —                                       | `{data: {cattle}}`                | Yes         |
| POST   | `/api/cattle`              | `{name, breed, age, owner_id, photo}`   | `{data: {cattle_id}}`             | Yes         |
| PUT    | `/api/cattle/<cattle_id>`  | `{fields to update}`                    | `{data: {cattle}}`                | Yes         |
| DELETE | `/api/cattle/<cattle_id>`  | —                                       | `{message}`                       | Yes (admin) |
| POST   | `/api/identify`            | `multipart: image file`                 | `{cattle_id, confidence, status}` | Yes         |
| GET    | `/api/owners`              | `?page=1`                               | `{data: [...], total}`            | Yes         |
| POST   | `/api/owners`              | `{name, phone, aadhaar, farm_location}` | `{data: {owner_id}}`              | Yes         |
| GET    | `/api/sensors/<cattle_id>` | `?type=temperature&limit=100`           | `{data: [...]}`                   | Yes         |
| GET    | `/api/sensors/latest`      | `?farm_id=FARM-01`                      | `{data: [...]}`                   | Yes         |
| GET    | `/api/health/alerts`       | `?severity=high&resolved=false`         | `{data: [...]}`                   | Yes         |
| POST   | `/api/health/detect`       | `multipart: image file`                 | `{alerts: [...]}`                 | Yes         |
| GET    | `/api/insurance/claims`    | `?status=pending`                       | `{data: [...]}`                   | Yes         |
| POST   | `/api/insurance/verify`    | `{claim_id, cattle_image, location}`    | `{verification}`                  | Yes         |

---

## Key Technical Decisions

| Decision     | Choice                   | Why                                               |
| ------------ | ------------------------ | ------------------------------------------------- |
| Framework    | Flask 3.x                | Simple, well-documented, team familiarity         |
| App pattern  | Factory pattern          | Testable, configurable, scalable                  |
| Database     | MongoDB                  | Flexible schema for varied sensor/cattle data     |
| ORM/Driver   | PyMongo (raw)            | Direct control, no ORM overhead                   |
| Validation   | Marshmallow              | Robust schema validation, serialization           |
| Auth         | JWT (Flask-JWT-Extended) | Stateless, standard for REST APIs                 |
| Password     | bcrypt                   | Industry-standard password hashing                |
| Real-time    | Flask-SocketIO           | Integrates directly with Flask, WebSocket support |
| CORS         | flask-cors               | Required for React frontend on different port     |
| Async worker | eventlet                 | Required by Flask-SocketIO for WebSocket          |

---

## Verification Checklist

- [ ] Python 3.12 environment with Flask running
- [ ] MongoDB connection working (docker + pymongo)
- [ ] App factory pattern (`create_app()`) working
- [ ] All 7 blueprint routes registered
- [ ] Cattle CRUD operations working
- [ ] JWT auth (register + login + protected routes)
- [ ] Image upload + storage working
- [ ] `/api/identify` calls ML model successfully
- [ ] `/api/health/detect` calls health model
- [ ] `/api/insurance/verify` runs fraud detection
- [ ] Flask-SocketIO emits real-time sensor updates
- [ ] MQTT bridge receives from Mosquitto
- [ ] Marshmallow validation on all inputs
- [ ] Proper error handling (400, 401, 404, 500)
- [ ] Unit tests passing (pytest)
- [ ] CORS working with React frontend
- [ ] Seed script populates demo data
- [ ] API documented with examples
