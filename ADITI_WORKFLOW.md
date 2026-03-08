# Aditi — Health & Insurance Lead Workflow

## Role: Health Detection AI + Fraud Detection + Alert System

**Member:** Aditi
**Module:** `ml/health/` + `insurance/` + `alerts/`
**Python Version:** 3.12
**Primary Tech:** YOLOv8 (health detection), Scikit-learn (anomaly), SMTP/Twilio (alerts)

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│               ADITI's HEALTH & INSURANCE ARCHITECTURE                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════════  │
│  MODULE 1: HEALTH DETECTION (Vision-Based)                               │
│  ═══════════════════════════════════════════════════════════════════════  │
│                                                                          │
│  ┌──────────────┐     ┌──────────────────────┐     ┌────────────────┐   │
│  │  📷 Camera   │     │  YOLOv8 Health       │     │  RESULT        │   │
│  │  Image/      │────▶│  Detector            │────▶│                │   │
│  │  Video Frame │     │                      │     │  Classes:      │   │
│  │              │     │  Fine-tuned from     │     │  - wound       │   │
│  │              │     │  yolov8s.pt          │     │  - eye_redness │   │
│  │              │     │  640x640             │     │  - skin_lesion │   │
│  │              │     │                      │     │  - lameness    │   │
│  │              │     │  Classes: 5          │     │  - healthy     │   │
│  └──────────────┘     └──────────────────────┘     └────────┬───────┘   │
│                                                              │           │
│  ═══════════════════════════════════════════════════════════════════════  │
│  MODULE 2: HEALTH DETECTION (Sensor-Based Anomaly)                       │
│  ═══════════════════════════════════════════════════════════════════════  │
│                                                              │           │
│  ┌──────────────┐     ┌──────────────────────┐     ┌────────▼────────┐  │
│  │  📡 Sensor   │     │  Anomaly Detector    │     │  HEALTH ALERT   │  │
│  │  Data from   │────▶│                      │────▶│  GENERATOR      │  │
│  │  Jaswanth's  │     │  - IsolationForest   │     │                 │  │
│  │  MQTT Worker │     │  - Threshold rules   │     │  Combines:      │  │
│  │              │     │  - Rolling averages  │     │  - Vision AI    │  │
│  │  Inputs:     │     │  - Z-score detection │     │  - Sensor AI    │  │
│  │  - temp      │     │                      │     │  - Rule engine  │  │
│  │  - heartrate │     │  Detects:            │     │                 │  │
│  │  - activity  │     │  - Fever             │     │  → severity     │  │
│  │  - gps       │     │  - Illness           │     │  → alert_type   │  │
│  └──────────────┘     │  - Low activity      │     │  → confidence   │  │
│                       │  - Abnormal heart    │     └────────┬────────┘  │
│                       └──────────────────────┘              │           │
│                                                              │           │
│  ═══════════════════════════════════════════════════════════════════════  │
│  MODULE 3: INSURANCE & FRAUD DETECTION                                   │
│  ═══════════════════════════════════════════════════════════════════════  │
│                                                              │           │
│  ┌──────────────────────────────────────────────────────────┐│           │
│  │  INSURANCE VERIFICATION PIPELINE                         ││           │
│  │                                                          ││           │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ ││           │
│  │  │ STEP 1   │  │ STEP 2   │  │ STEP 3   │  │ STEP 4  │ ││           │
│  │  │          │  │          │  │          │  │         │ ││           │
│  │  │ Face     │  │ Geo      │  │ Fraud    │  │ Final   │ ││           │
│  │  │ Verify   │──▶│ Verify   │──▶│ Score    │──▶│ Decision│ ││           │
│  │  │          │  │          │  │          │  │         │ ││           │
│  │  │ Is this  │  │ Is cow   │  │ Pattern  │  │ Approve │ ││           │
│  │  │ the same │  │ on the   │  │ analysis │  │ Reject  │ ││           │
│  │  │ cattle?  │  │ farm?    │  │ anomaly  │  │ Manual  │ ││           │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────┘ ││           │
│  └──────────────────────────────────────────────────────────┘│           │
│                                                              │           │
│  ═══════════════════════════════════════════════════════════════════════  │
│  MODULE 4: ALERT & NOTIFICATION SYSTEM                                   │
│  ═══════════════════════════════════════════════════════════════════════  │
│                                                              │           │
│  ┌──────────────────────────────────────────────┐            │           │
│  │  NOTIFICATION MANAGER                        │◀───────────┘           │
│  │                                              │                        │
│  │  notification_manager.py                     │                        │
│  │  ├── Route by severity                       │                        │
│  │  │   ├── HIGH   → SMS + Email + Dashboard    │                        │
│  │  │   ├── MEDIUM → Email + Dashboard          │                        │
│  │  │   └── LOW    → Dashboard only             │                        │
│  │  │                                           │                        │
│  │  ├── sms_alert.py     (Twilio API)           │                        │
│  │  ├── email_alert.py   (SMTP / SendGrid)      │                        │
│  │  └── dashboard push   (Flask-SocketIO event)  │                        │
│  └──────────────────────────────────────────────┘                        │
└──────────────────────────────────────────────────────────────────────────┘
```

### Fraud Detection Decision Tree

```
                    INSURANCE CLAIM RECEIVED
                            │
                    ┌───────▼───────┐
                    │ Face Verified? │
                    └───┬───────┬───┘
                    YES │       │ NO
                        │    ┌──▼──────────┐
                        │    │ REJECT      │
                        │    │ Fraud Score: │
                        │    │ 0.95        │
                        │    └─────────────┘
                    ┌───▼──────────────┐
                    │ Geo Verified?     │
                    │ (Cow on farm?)    │
                    └───┬──────────┬───┘
                    YES │          │ NO
                        │     ┌────▼──────────┐
                        │     │ FLAG          │
                        │     │ Fraud Score:  │
                        │     │ 0.70          │
                        │     └───────────────┘
                    ┌───▼──────────────┐
                    │ Duplicate Claim?  │
                    │ (Same cow, same   │
                    │  time period?)    │
                    └───┬──────────┬───┘
                     NO │          │ YES
                        │     ┌────▼──────────┐
                        │     │ REJECT        │
                        │     │ Fraud Score:  │
                        │     │ 0.99          │
                        │     └───────────────┘
                    ┌───▼──────────────┐
                    │ Pattern Analysis  │
                    │ (Frequent claims? │
                    │  Cluster farm?)   │
                    └───┬──────────┬───┘
                 NORMAL │       ANOMALY
                        │     ┌────▼──────────┐
                        │     │ FLAG FOR       │
                        │     │ MANUAL REVIEW  │
                        │     │ Fraud Score:   │
                        │     │ 0.50-0.70      │
                        │     └───────────────┘
                    ┌───▼──────────────┐
                    │ ✅ APPROVED       │
                    │ Fraud Score: 0.05 │
                    └──────────────────┘
```

---

## Folder Structure (Aditi's Files)

```
cap/
├── ml/
│   └── health/                        # 🏥 Health Detection AI
│       ├── train_health.py            #   Train YOLOv8 health detector
│       ├── predict_health.py          #   Run health detection on image
│       ├── anomaly_detector.py        #   Sensor-based anomaly detection
│       ├── health_classifier.py       #   Combine vision + sensor results
│       ├── data.yaml                  #   Health dataset config for YOLO
│       ├── datasets/                  #   Health condition images
│       │   ├── images/
│       │   │   ├── train/             #     Training images
│       │   │   └── val/               #     Validation images
│       │   └── labels/
│       │       ├── train/             #     YOLO annotations
│       │       └── val/
│       ├── weights/
│       │   └── health_best.pt         #   Trained health detection model
│       └── evaluation/
│           ├── confusion_matrix.png   #   Model evaluation visuals
│           └── metrics_report.txt     #   Precision/recall/F1 report
│
├── insurance/                         # 🛡️ Insurance & Fraud Module
│   ├── __init__.py
│   ├── claim_verifier.py              #   Main claim verification pipeline
│   ├── fraud_detector.py              #   Fraud scoring algorithm
│   ├── subsidy_tracker.py             #   Government subsidy tracking
│   ├── geo_verifier.py                #   Geo-fence based verification
│   ├── death_claim_handler.py         #   Special logic for death claims
│   ├── duplicate_checker.py           #   Check for duplicate registrations
│   ├── models.py                      #   Insurance data models
│   ├── config.py                      #   Thresholds, rules configuration
│   └── requirements.txt               #   Insurance module dependencies
│
├── alerts/                            # 🔔 Alert & Notification Module
│   ├── __init__.py
│   ├── notification_manager.py        #   Central alert router
│   ├── sms_alert.py                   #   SMS via Twilio
│   ├── email_alert.py                 #   Email via SMTP/SendGrid
│   ├── alert_rules.py                 #   Alert severity rules engine
│   ├── templates/                     #   Notification templates
│   │   ├── health_alert_sms.txt
│   │   ├── health_alert_email.html
│   │   ├── fraud_alert_email.html
│   │   └── geofence_alert_sms.txt
│   └── config.py                      #   Twilio/SMTP credentials
```

---

## Dependencies

### ml/requirements.txt (shared with Ramakrishna — add these)

```txt
# Anomaly Detection
scikit-learn==1.5.0

# Health-specific
scipy==1.13.0
```

### insurance/requirements.txt

```txt
# Core
numpy==1.26.4
pandas==2.2.2

# Geospatial
geopy==2.4.1
shapely==2.0.4

# Database
pymongo==4.10.1

# Utilities
python-dotenv==1.0.1
```

### alerts/requirements.txt (in alerts/ folder — not separate install)

```txt
# Notifications
twilio==9.3.0

# Email
secure-smtplib==0.1.1

# Templating
jinja2==3.1.4

# Utilities
python-dotenv==1.0.1
```

---

## Setup Instructions

```bash
# 1. Python 3.12 environment
cd cap
python -m venv venv
venv\Scripts\activate

# 2. Install ML dependencies (shared with Ramakrishna)
pip install -r ml/requirements.txt

# 3. Install insurance module dependencies
pip install -r insurance/requirements.txt

# 4. Install alert dependencies
pip install twilio jinja2

# 5. Verify installations
python -c "from ultralytics import YOLO; print('YOLOv8 OK')"
python -c "from sklearn.ensemble import IsolationForest; print('scikit-learn OK')"
python -c "from geopy.distance import geodesic; print('geopy OK')"

# 6. Set up Twilio (for SMS alerts — optional for demo)
# Sign up at https://www.twilio.com/ (free trial)
# Add to .env:
# TWILIO_ACCOUNT_SID=your_sid
# TWILIO_AUTH_TOKEN=your_token
# TWILIO_PHONE_NUMBER=+1234567890

# 7. Set up email (for email alerts)
# Add to .env:
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your_email@gmail.com
# SMTP_PASSWORD=your_app_password  (use Gmail App Password)
# ALERT_RECIPIENT=farmer@example.com
```

---

## 4-Week Schedule

### WEEK 1 (Feb 11–17): Dataset + Anomaly Detector + Research

| Day | Date   | Tasks                                                                                                            | Deliverable                |
| --- | ------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------- |
| Tue | Feb 11 | Set up Python 3.12 venv, install all dependencies (ML + insurance + alerts)                                      | Environment ready          |
| Wed | Feb 12 | Research cattle health conditions (wound types, eye diseases, lameness signs). Collect reference images          | Research notes             |
| Thu | Feb 13 | Collect health condition images (Roboflow Universe, Google Images, veterinary databases) — target 300+ per class | Image dataset started      |
| Fri | Feb 14 | Annotate health images in Roboflow — classes: wound, eye_redness, skin_lesion, lameness, healthy                 | Annotations in YOLO format |
| Sat | Feb 15 | Build `anomaly_detector.py` — IsolationForest on sensor data. Define normal ranges for temp, heartrate, activity | Anomaly detector ready     |
| Sun | Feb 16 | Build threshold-based rules engine (`alert_rules.py`) — simple rules for fever (>39.5°C), low activity, etc.     | Rule engine ready          |
| Mon | Feb 17 | Study insurance fraud patterns — research duplicate claims, ghost cattle, common scams in India                  | ✅ Research + data ready   |

**Coordination:**

- Share with **Ramakrishna**: Use same `ml/utils/` preprocessing functions
- Get from **Jaswanth**: Sensor data format and normal value ranges
- Discuss with **Akash**: Health alert MongoDB schema

---

### WEEK 2 (Feb 18–24): Health Model + Fraud Detection + Alerts

| Day | Date   | Tasks                                                                                                   | Deliverable                 |
| --- | ------ | ------------------------------------------------------------------------------------------------------- | --------------------------- |
| Tue | Feb 18 | Train YOLOv8 health detection model (fine-tune from yolov8s.pt, 100 epochs)                             | `train_health.py` running   |
| Wed | Feb 19 | Evaluate health model (per-class precision/recall). Iterate on dataset if needed                        | Metrics report              |
| Thu | Feb 20 | Build `predict_health.py` — inference function: image → health alerts list                              | Health prediction working   |
| Fri | Feb 21 | Build `claim_verifier.py` — main pipeline: face verify → geo verify → fraud score → decision            | Claim verification pipeline |
| Sat | Feb 22 | Build `fraud_detector.py` — scoring algorithm with weighted factors (duplicate check, pattern analysis) | Fraud detector ready        |
| Sun | Feb 23 | Build `geo_verifier.py` — check if cattle GPS is within farm boundary using Shapely                     | Geo-verification ready      |
| Mon | Feb 24 | Build `notification_manager.py` + `sms_alert.py` + `email_alert.py`                                     | ✅ Alert system functional  |

**Coordination:**

- Get from **Ramakrishna**: Face verification function (for insurance claim verification step)
- Share with **Akash**: `predict_health()`, `verify_claim()`, `calculate_fraud_score()` interfaces

---

### WEEK 3 (Feb 25–Mar 3): Integration & Combined Testing

| Day | Date   | Tasks                                                                                                    | Deliverable               |
| --- | ------ | -------------------------------------------------------------------------------------------------------- | ------------------------- |
| Tue | Feb 25 | Integrate health detection with Akash's Flask API (`/api/health/detect`)                                 | Health API working        |
| Wed | Feb 26 | Integrate insurance verification with Flask API (`/api/insurance/verify`)                                | Insurance API working     |
| Thu | Feb 27 | Build `health_classifier.py` — combine vision results + sensor anomaly results into unified health score | Combined health scoring   |
| Fri | Feb 28 | Test alert flow: sensor anomaly → health alert → notification_manager → SMS/email                        | End-to-end alerts working |
| Sat | Mar 1  | Test insurance flow: submit claim → face verify → geo verify → fraud score → approve/reject              | Insurance flow tested     |
| Sun | Mar 2  | Build `duplicate_checker.py` — detect same cattle registered under multiple owners/farms                 | Duplicate detection ready |
| Mon | Mar 3  | Debug integration issues, refine fraud scoring thresholds                                                | ✅ Fully integrated       |

**Coordination:**

- With **Akash**: Debug health and insurance API integration
- With **Jaswanth**: Test anomaly detection on live sensor data
- With **Poshith**: Verify health alerts + insurance claims display on frontend
- With **Ramakrishna**: Debug face verification in insurance pipeline

---

### WEEK 4 (Mar 4–11): Documentation & Demo Scenarios

| Day | Date   | Tasks                                                                                          | Deliverable          |
| --- | ------ | ---------------------------------------------------------------------------------------------- | -------------------- |
| Tue | Mar 4  | Create demo scenarios for health detection (provide sample images for each condition)          | Demo dataset ready   |
| Wed | Mar 5  | Create demo scenarios for fraud detection (duplicate claim, geo-fence mismatch, pattern fraud) | Fraud demo scenarios |
| Thu | Mar 6  | Write evaluation report — health model metrics, fraud detection accuracy on test cases         | Evaluation report    |
| Fri | Mar 7  | Write alert notification templates (professional SMS/email text)                               | Templates polished   |
| Sat | Mar 8  | Build `subsidy_tracker.py` — track which cattle are eligible for government subsidies          | Subsidy module       |
| Sun | Mar 9  | Full team demo — demonstrate all health, insurance, and alert features                         | Demo ready           |
| Mon | Mar 11 | Code cleanup, add docstrings, final commit                                                     | ✅ Complete          |

---

## Output Contracts (for other team members)

### For Akash (Backend) — Health Detection:

```python
# Function signature for health service:
def detect_health_issues(image_path: str) -> list:
    """
    Detect health conditions in a cattle image.

    Returns:
        [
            {
                "condition": "wound",
                "severity": "high",
                "confidence": 0.89,
                "bbox": [x1, y1, x2, y2],
                "description": "Open wound detected on left flank"
            },
            {
                "condition": "eye_redness",
                "severity": "medium",
                "confidence": 0.76,
                "bbox": [x1, y1, x2, y2],
                "description": "Redness detected in left eye"
            }
        ]
    """
```

### For Akash (Backend) — Sensor Anomaly:

```python
# Function signature for anomaly detection:
def check_sensor_anomaly(cattle_id: str, sensor_data: dict) -> dict:
    """
    Check sensor data for anomalies.

    Input sensor_data:
        {"temperature": 40.1, "heartrate": 95, "activity_level": 0.2}

    Returns:
        {
            "is_anomaly": True,
            "anomalies": [
                {"type": "fever", "severity": "high", "value": 40.1, "threshold": 39.5},
                {"type": "elevated_heartrate", "severity": "medium", "value": 95, "threshold": 80}
            ],
            "overall_health_score": 0.35,   # 0 = critical, 1 = healthy
            "recommendation": "Veterinary visit recommended"
        }
    """
```

### For Akash (Backend) — Insurance Verification:

```python
# Function signature for claim verification:
def verify_insurance_claim(claim_data: dict) -> dict:
    """
    Verify an insurance claim.

    Input claim_data:
        {
            "claim_id": "CLM-001",
            "cattle_id": "CTL-001",
            "owner_id": "OWN-001",
            "claim_type": "illness",
            "cattle_image": "/path/to/image.jpg",
            "cattle_location": {"lat": 17.385, "lng": 78.486}
        }

    Returns:
        {
            "claim_id": "CLM-001",
            "face_verified": True,
            "geo_verified": True,
            "duplicate_check": False,
            "fraud_score": 0.12,        # 0 = clean, 1 = fraud
            "fraud_flags": [],
            "decision": "approved",     # approved | rejected | manual_review
            "reason": "All verification checks passed"
        }
    """
```

---

## Health Condition Classes

| Class | Condition     | Visual Signs                     | Severity |
| ----- | ------------- | -------------------------------- | -------- |
| 0     | `wound`       | Open cuts, lacerations, bleeding | High     |
| 1     | `eye_redness` | Red/swollen eyes, discharge      | Medium   |
| 2     | `skin_lesion` | Patches, lumps, hair loss        | Medium   |
| 3     | `lameness`    | Abnormal gait, favoring leg      | High     |
| 4     | `healthy`     | Normal appearance                | Low      |

### Sensor Anomaly Thresholds

| Sensor      | Normal Range         | Alert Threshold | Condition        |
| ----------- | -------------------- | --------------- | ---------------- |
| Temperature | 37.5 – 39.5°C        | > 39.5°C        | Fever            |
| Temperature | 37.5 – 39.5°C        | < 37.0°C        | Hypothermia      |
| Heart Rate  | 40 – 80 bpm          | > 80 bpm        | Stress/illness   |
| Heart Rate  | 40 – 80 bpm          | < 40 bpm        | Bradycardia      |
| Activity    | 500+ steps/day       | < 200 steps     | Lethargy/illness |
| GPS         | Within farm boundary | Outside farm    | Escape/theft     |

---

## Key Technical Decisions

| Decision            | Choice                  | Why                                                 |
| ------------------- | ----------------------- | --------------------------------------------------- |
| Health detection    | YOLOv8 (object detect)  | Can localize condition on specific body part        |
| Anomaly detection   | IsolationForest + Rules | Combined ML + rule-based for reliability            |
| Fraud scoring       | Weighted multi-factor   | Interpretable, adjustable thresholds                |
| Geo-verification    | Shapely (polygon check) | Standard geospatial library, lightweight            |
| SMS alerts          | Twilio                  | Free trial, easy Python SDK, reliable               |
| Email alerts        | SMTP (Gmail)            | Free, built-in Python support                       |
| Alert routing       | Severity-based          | Prevents alert fatigue (SMS only for high severity) |
| Duplicate detection | MongoDB query           | Check cattle_id + time window for existing claims   |

---

## Verification Checklist

- [ ] Python 3.12 environment with all dependencies
- [ ] Health dataset collected (300+ images per class)
- [ ] Health dataset annotated in YOLO format
- [ ] YOLOv8 health model trained (mAP > 0.6)
- [ ] `predict_health.py` detects conditions in test images
- [ ] `anomaly_detector.py` flags abnormal sensor values
- [ ] `health_classifier.py` combines vision + sensor results
- [ ] `claim_verifier.py` runs full verification pipeline
- [ ] `fraud_detector.py` calculates fraud scores correctly
- [ ] `geo_verifier.py` checks GPS within farm boundary
- [ ] `duplicate_checker.py` detects duplicate claims
- [ ] `notification_manager.py` routes alerts by severity
- [ ] `sms_alert.py` sends SMS (tested with Twilio trial)
- [ ] `email_alert.py` sends email (tested with Gmail)
- [ ] Alert templates formatted professionally
- [ ] Integration with Flask API endpoints tested
- [ ] Demo scenarios created for all fraud types
- [ ] Evaluation report with metrics generated
- [ ] Code documented with docstrings
