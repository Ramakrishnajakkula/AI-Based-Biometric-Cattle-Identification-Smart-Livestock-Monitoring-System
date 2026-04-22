# YOLO Conversion Checklist for This Project

Use this checklist before training detection models in this repository.

## Target folder layout

Detection dataset target:
- ml/detection/datasets/images/train
- ml/detection/datasets/images/val
- ml/detection/datasets/labels/train
- ml/detection/datasets/labels/val

Health dataset target:
- ml/health/datasets/images/train
- ml/health/datasets/images/val
- ml/health/datasets/labels/train
- ml/health/datasets/labels/val

## Steps

1. Download source dataset archive/repo to a temp folder.
2. Verify license allows your usage (academic/demo).
3. Inspect annotation format:
- If YOLO txt exists: map folders to project layout.
- If COCO/VOC/CSV only: convert to YOLO txt.
4. Ensure class map is fixed and documented:
- Detection: class 0 should be `cattle_face` in `ml/detection/data.yaml`.
- Health: classes should match `ml/health/data.yaml`:
  - 0: wound
  - 1: eye_redness
  - 2: skin_lesion
  - 3: lameness
  - 4: healthy
5. Run integrity checks:
- every image has matching label txt (for labeled sets)
- no empty train/val folders
- no invalid bbox values
6. Run a tiny smoke training:
- `python ml/detection/train_detector.py`
- `python ml/health/train_health.py`

## YOLO label format reminder

Each line in label file:

`class_id x_center y_center width height`

All box values are normalized to [0, 1].

## Recommended tools

- Roboflow export to YOLO format
- FiftyOne dataset conversion
- Custom conversion scripts for COCO/VOC
