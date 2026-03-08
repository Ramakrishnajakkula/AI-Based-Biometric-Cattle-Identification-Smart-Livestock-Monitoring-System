# Ramakrishna — AI/ML Lead Workflow

## Role: Cattle Face Detection & Biometric Recognition

**Member:** Ramakrishna
**Module:** `ml/detection/` + `ml/recognition/` + `ml/notebooks/` + `ml/utils/`
**Python Version:** 3.12
**Primary Tech:** YOLOv8, ArcFace/InsightFace, PyTorch, OpenCV

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│               RAMAKRISHNA's AI/ML PIPELINE ARCHITECTURE                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐     ┌──────────────────┐     ┌────────────────────┐   │
│  │  INPUT       │     │   STAGE 1:       │     │   STAGE 2:         │   │
│  │              │     │   DETECTION      │     │   RECOGNITION      │   │
│  │  📷 Camera   │────▶│                  │────▶│                    │   │
│  │  Image/Video │     │  YOLOv8s/n       │     │  ArcFace           │   │
│  │              │     │  - Detect face   │     │  (ResNet-50)       │   │
│  │  Resolution: │     │  - Crop muzzle   │     │  - 512-d embedding │   │
│  │  640x640     │     │  - Bounding box  │     │  - Feature vector  │   │
│  └──────────────┘     └──────────────────┘     └────────┬───────────┘   │
│                                                          │               │
│                     ┌────────────────────────────────────┘               │
│                     │                                                    │
│                     ▼                                                    │
│  ┌──────────────────────────────────┐     ┌──────────────────────────┐   │
│  │   STAGE 3: MATCHING             │     │   STAGE 4: RESULT        │   │
│  │                                  │     │                          │   │
│  │  Embedding DB (MongoDB/FAISS)   │     │  ✅ Cattle ID matched    │   │
│  │  - Cosine similarity            │────▶│  ❌ No match (new)       │   │
│  │  - Threshold: 0.6               │     │  ⚠️ Low confidence       │   │
│  │  - Top-K nearest neighbors      │     │                          │   │
│  └──────────────────────────────────┘     └──────────────────────────┘   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  MODEL TRAINING PIPELINE                                                │
│                                                                         │
│  Raw Images ──▶ Roboflow Annotation ──▶ Augmentation ──▶ Training      │
│       │              │                       │               │          │
│       │         YOLO format             Albumentations    YOLOv8 CLI    │
│       │         (bbox labels)           - Flip, Rotate    ultralytics   │
│       │                                 - Brightness                    │
│       │                                 - Crop                          │
│       └── ArcFace Dataset ──▶ Pairs ──▶ ArcFace Loss ──▶ ResNet-50    │
│              (ID-labeled)                                               │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  EXPLAINABILITY                                                         │
│                                                                         │
│  Grad-CAM ──▶ Heatmap overlay on muzzle region ──▶ Validate model      │
│               attention is on unique features                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Model Architecture Details

```
DETECTION MODEL (YOLOv8s):
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Backbone   │────▶│    Neck      │────▶│   Head      │
│  CSPDarknet │     │  PANet/FPN   │     │  Detect     │
│  (Feature   │     │  (Multi-     │     │  - BBox     │
│   Extract)  │     │   scale      │     │  - Class    │
│             │     │   fusion)    │     │  - Conf     │
└─────────────┘     └──────────────┘     └─────────────┘

RECOGNITION MODEL (ArcFace):
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Input      │────▶│  ResNet-50   │────▶│  ArcFace    │
│  112x112    │     │  Backbone    │     │  Head       │
│  cropped    │     │  (Feature    │     │  512-dim    │
│  muzzle     │     │   extract)   │     │  embedding  │
└─────────────┘     └──────────────┘     └─────────────┘
```

---

## Folder Structure (Ramakrishna's Files)

```
cap/
├── ml/
│   ├── detection/                     # 🎯 YOLOv8 face/muzzle detection
│   │   ├── train_detector.py          #   Training script
│   │   ├── predict.py                 #   Single image inference
│   │   ├── batch_predict.py           #   Batch inference
│   │   ├── evaluate.py                #   Model evaluation metrics
│   │   ├── data.yaml                  #   Dataset config for YOLO
│   │   ├── datasets/
│   │   │   ├── images/
│   │   │   │   ├── train/             #   Training images (~400)
│   │   │   │   └── val/               #   Validation images (~100)
│   │   │   └── labels/
│   │   │       ├── train/             #   YOLO format annotations
│   │   │       └── val/
│   │   └── weights/
│   │       ├── yolov8s.pt             #   Pretrained weights
│   │       └── best.pt               #   Best trained weights
│   │
│   ├── recognition/                   # 🔐 ArcFace embedding & matching
│   │   ├── train_embedding.py         #   Train ArcFace model
│   │   ├── inference.py               #   Generate embedding for an image
│   │   ├── face_matcher.py            #   Compare embedding vs gallery
│   │   ├── gallery_builder.py         #   Build/update embedding gallery
│   │   ├── evaluate_recognition.py    #   Recognition accuracy metrics
│   │   └── weights/
│   │       └── arcface_cattle.pth     #   Trained ArcFace weights
│   │
│   ├── notebooks/                     # 📓 Jupyter experiments
│   │   ├── 01_data_exploration.ipynb  #   Dataset statistics & samples
│   │   ├── 02_model_comparison.ipynb  #   YOLOv8n vs v8s vs v8m
│   │   ├── 03_gradcam_analysis.ipynb  #   Explainability heatmaps
│   │   └── 04_embedding_tsne.ipynb    #   t-SNE visualization of embeddings
│   │
│   ├── utils/                         # 🔧 Shared ML utilities
│   │   ├── __init__.py
│   │   ├── preprocessing.py           #   Resize, normalize, color convert
│   │   ├── augmentation.py            #   Albumentations pipelines
│   │   └── evaluation.py              #   mAP, accuracy, confusion matrix
│   │
│   └── requirements.txt
```

---

## Dependencies (ml/requirements.txt)

```txt
# Core ML
ultralytics==8.3.40
torch==2.2.2
torchvision==0.17.2
onnx==1.16.0
onnxruntime==1.18.0

# Computer Vision
opencv-python-headless==4.10.0.84
Pillow==10.4.0
albumentations==1.4.3

# Face Recognition
insightface==0.7.3

# Data & Visualization
numpy==1.26.4
pandas==2.2.2
matplotlib==3.9.0
seaborn==0.13.2
scikit-learn==1.5.0

# Explainability
grad-cam==1.5.0

# Notebooks
jupyter==1.0.0
ipykernel==6.29.0

# Utilities
tqdm==4.66.4
pyyaml==6.0.1
python-dotenv==1.0.1
```

---

## Setup Instructions

```bash
# 1. Make sure Python 3.12 is installed
python --version   # Must show 3.12.x

# 2. Navigate to project root
cd cap

# 3. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# 4. Install ML dependencies
pip install -r ml/requirements.txt

# 5. Verify GPU (optional but recommended)
python -c "import torch; print(torch.cuda.is_available())"

# 6. Download YOLOv8 pretrained weights
python -c "from ultralytics import YOLO; model = YOLO('yolov8s.pt')"

# 7. Set up Roboflow for annotation
# Go to https://roboflow.com → Create project → Upload images → Annotate
```

---

## 4-Week Schedule

### WEEK 1 (Feb 11–17): Data Collection & Pipeline Setup

| Day | Date   | Tasks                                                                                         | Deliverable                               |
| --- | ------ | --------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Tue | Feb 11 | Set up Python 3.12 venv, install ML dependencies, verify GPU support                          | Working environment                       |
| Wed | Feb 12 | Research cattle muzzle print datasets (Kaggle, papers), download existing datasets            | Dataset links list                        |
| Thu | Feb 13 | Collect additional cattle face images (500+ target), organize into folders                    | `ml/detection/datasets/images/` populated |
| Fri | Feb 14 | Annotate images in Roboflow (bounding boxes around muzzle/face region)                        | YOLO format labels exported               |
| Sat | Feb 15 | Set up `data.yaml`, configure training parameters, run first YOLOv8 training (10 epochs test) | `train_detector.py` working               |
| Sun | Feb 16 | Data augmentation pipeline with Albumentations, expand dataset                                | `ml/utils/augmentation.py` ready          |
| Mon | Feb 17 | Write `preprocessing.py`, test end-to-end detection on sample images                          | ✅ Detection pipeline basic version       |

**Coordination:**

- Share with **Akash**: Expected input/output format for identification API
- Share with **Aditi**: `ml/utils/` — shared preprocessing functions

---

### WEEK 2 (Feb 18–24): Model Training & Recognition

| Day | Date   | Tasks                                                                                      | Deliverable                     |
| --- | ------ | ------------------------------------------------------------------------------------------ | ------------------------------- |
| Tue | Feb 18 | Full YOLOv8 training (100 epochs), monitor loss curves                                     | Trained detection model         |
| Wed | Feb 19 | Evaluate detection model (mAP, precision, recall), iterate if needed                       | `evaluate.py` + metrics report  |
| Thu | Feb 20 | Set up ArcFace training pipeline — prepare ID-labeled dataset (crop muzzles per cattle)    | ArcFace dataset ready           |
| Fri | Feb 21 | Train ArcFace embedding model on cattle muzzle crops                                       | `train_embedding.py` working    |
| Sat | Feb 22 | Build `inference.py` (generate embedding) + `face_matcher.py` (cosine similarity matching) | Recognition pipeline working    |
| Sun | Feb 23 | Build `gallery_builder.py` — store embeddings in MongoDB-compatible format                 | Gallery system ready            |
| Mon | Feb 24 | End-to-end test: Image → Detect → Crop → Embed → Match → Cattle ID                         | ✅ Full identification pipeline |

**Coordination:**

- Deliver to **Akash**: `identification_service.py` interface — function that takes image, returns cattle_id + confidence
- Share model weights location with team

---

### WEEK 3 (Feb 25–Mar 3): Integration & Optimization

| Day | Date   | Tasks                                                                          | Deliverable                 |
| --- | ------ | ------------------------------------------------------------------------------ | --------------------------- |
| Tue | Feb 25 | Integrate with Akash's Flask API — create `identification_service.py` wrapper  | API-callable identification |
| Wed | Feb 26 | Test integration: POST image to `/api/identify` → get cattle ID response       | Integration working         |
| Thu | Feb 27 | Optimize model — try different YOLOv8 sizes (n/s/m), compare accuracy vs speed | Best model selected         |
| Fri | Feb 28 | Grad-CAM explainability analysis — verify model looks at muzzle features       | `03_gradcam_analysis.ipynb` |
| Sat | Mar 1  | Handle edge cases: poor lighting, angles, partial occlusion                    | Robust inference            |
| Sun | Mar 2  | t-SNE visualization of embeddings — verify cattle cluster separately           | `04_embedding_tsne.ipynb`   |
| Mon | Mar 3  | Multi-angle testing, create evaluation report                                  | ✅ Optimized & integrated   |

**Coordination:**

- With **Akash**: Debug API integration issues
- With **Poshith**: Confirm frontend image upload format (multipart/form-data)

---

### WEEK 4 (Mar 4–11): Documentation & Polish

| Day | Date   | Tasks                                                                         | Deliverable                 |
| --- | ------ | ----------------------------------------------------------------------------- | --------------------------- |
| Tue | Mar 4  | Write model comparison notebook (YOLOv8n vs s vs m accuracy table)            | `02_model_comparison.ipynb` |
| Wed | Mar 5  | Create confusion matrix, precision-recall curves, ROC curves                  | Evaluation visuals          |
| Thu | Mar 6  | Export best model to ONNX format for deployment                               | `scripts/export_model.py`   |
| Fri | Mar 7  | Write documentation — training procedure, dataset details, model architecture | ML section of report        |
| Sat | Mar 8  | Create demo script — identify cattle from webcam/uploaded images              | Demo-ready                  |
| Sun | Mar 9  | Final testing with team — full system demo walkthrough                        | System verified             |
| Mon | Mar 11 | Code cleanup, add docstrings, final commit                                    | ✅ Complete                 |

---

## Key Technical Decisions

| Decision           | Choice              | Why                                                                    |
| ------------------ | ------------------- | ---------------------------------------------------------------------- |
| Detection model    | YOLOv8s             | Best balance of speed (45 FPS) and accuracy for object detection       |
| Recognition model  | ArcFace (ResNet-50) | State-of-the-art for face/muzzle embedding with angular margin loss    |
| Biometric feature  | Muzzle print        | Unique per cattle (like fingerprints), more reliable than face shape   |
| Similarity metric  | Cosine similarity   | Standard for embedding comparison, threshold-tunable                   |
| Embedding size     | 512 dimensions      | Standard ArcFace output, good balance of expressiveness and storage    |
| Dataset annotation | Roboflow            | Free tier sufficient, exports YOLO format natively                     |
| Training framework | Ultralytics CLI     | Simplest API for YOLOv8, handles augmentation/validation automatically |

---

## Output Contracts (for other team members)

### For Akash (Backend):

```python
# Function signature Akash will call:
def identify_cattle(image_path: str) -> dict:
    """
    Takes an image path, returns identification result.

    Returns:
        {
            "cattle_id": "CTL-001" or None,
            "confidence": 0.87,
            "embedding": [0.12, -0.34, ...],  # 512-d vector
            "bbox": [x1, y1, x2, y2],          # muzzle bounding box
            "status": "matched" | "no_match" | "low_confidence"
        }
    """
```

### For Aditi (shared utils):

```python
# Shared preprocessing functions in ml/utils/preprocessing.py
def preprocess_image(image_path: str, target_size: tuple = (640, 640)) -> np.ndarray
def crop_region(image: np.ndarray, bbox: list) -> np.ndarray
def normalize_image(image: np.ndarray) -> np.ndarray
```

---

## Verification Checklist

- [ ] Python 3.12 virtual environment created and working
- [ ] YOLOv8 installed and pretrained weights downloaded
- [ ] Dataset collected (500+ cattle muzzle images)
- [ ] Dataset annotated in YOLO format
- [ ] Detection model trained (mAP > 0.7)
- [ ] ArcFace model trained (Top-1 accuracy > 85%)
- [ ] `face_matcher.py` correctly matches known cattle
- [ ] Gallery builder stores embeddings in correct format for MongoDB
- [ ] Integration with Flask API tested (`/api/identify`)
- [ ] Grad-CAM analysis shows model focuses on muzzle features
- [ ] Edge cases handled (poor lighting, angles)
- [ ] Model exported to ONNX
- [ ] Jupyter notebooks run end-to-end
- [ ] Code documented with docstrings
- [ ] Evaluation report generated (metrics + visuals)
