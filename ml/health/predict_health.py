"""
Health Condition Detection - Inference Script
Author: Aditi
"""

from ultralytics import YOLO
from typing import List, Dict


SEVERITY_MAP = {
    "wound": "high",
    "eye_redness": "medium",
    "skin_lesion": "medium",
    "lameness": "high",
    "healthy": "low"
}

DESCRIPTION_MAP = {
    "wound": "Open wound or laceration detected",
    "eye_redness": "Redness or swelling detected in eye region",
    "skin_lesion": "Skin lesion, lumps, or hair loss detected",
    "lameness": "Abnormal gait or lameness indicator detected",
    "healthy": "No health issues detected"
}


def load_health_model(weights_path: str = "weights/health_best.pt") -> YOLO:
    """Load trained health detection model."""
    return YOLO(weights_path)


def detect_health_issues(image_path: str, model: YOLO = None, conf_threshold: float = 0.5) -> List[Dict]:
    """
    Detect health conditions in a cattle image.
    
    Called by Akash's health_service.py in the backend.
    
    Args:
        image_path: Path to cattle image
        model: Loaded YOLO model (loads default if None)
        conf_threshold: Minimum confidence threshold
    
    Returns:
        [
            {
                "condition": "wound",
                "severity": "high",
                "confidence": 0.89,
                "bbox": [x1, y1, x2, y2],
                "description": "Open wound detected on left flank"
            }
        ]
    """
    if model is None:
        model = load_health_model()
    
    results = model.predict(source=image_path, conf=conf_threshold, verbose=False)
    
    detections = []
    for result in results:
        for box in result.boxes:
            class_name = result.names[int(box.cls[0])]
            if class_name == "healthy":
                continue
            
            detection = {
                "condition": class_name,
                "severity": SEVERITY_MAP.get(class_name, "medium"),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist(),
                "description": DESCRIPTION_MAP.get(class_name, "Health issue detected")
            }
            detections.append(detection)
    
    return detections


if __name__ == "__main__":
    # Example usage
    model = load_health_model()
    issues = detect_health_issues("test_cattle.jpg", model)
    print(f"Found {len(issues)} health issue(s)")
    for issue in issues:
        print(f"  {issue['condition']} ({issue['severity']}): {issue['confidence']:.2f}")
