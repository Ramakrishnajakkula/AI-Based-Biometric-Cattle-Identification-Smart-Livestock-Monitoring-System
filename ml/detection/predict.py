"""
YOLOv8 Cattle Face/Muzzle Detection - Inference Script
Author: Ramakrishna
"""

from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path


def load_model(weights_path: str = "weights/best.pt") -> YOLO:
    """Load trained YOLOv8 detection model."""
    model = YOLO(weights_path)
    return model


def detect_cattle_face(model: YOLO, image_path: str, conf_threshold: float = 0.5) -> list:
    """
    Detect cattle face/muzzle in an image.
    
    Args:
        model: Loaded YOLO model
        image_path: Path to input image
        conf_threshold: Minimum confidence threshold
    
    Returns:
        List of detections: [{"bbox": [x1,y1,x2,y2], "confidence": float, "class": str}]
    """
    results = model.predict(source=image_path, conf=conf_threshold, verbose=False)
    
    detections = []
    for result in results:
        for box in result.boxes:
            detection = {
                "bbox": box.xyxy[0].tolist(),
                "confidence": float(box.conf[0]),
                "class": result.names[int(box.cls[0])]
            }
            detections.append(detection)
    
    return detections


def crop_muzzle(image_path: str, bbox: list) -> np.ndarray:
    """Crop the muzzle region from image using bounding box."""
    image = cv2.imread(image_path)
    x1, y1, x2, y2 = [int(coord) for coord in bbox]
    cropped = image[y1:y2, x1:x2]
    return cropped


if __name__ == "__main__":
    # Example usage
    model = load_model()
    detections = detect_cattle_face(model, "test_image.jpg")
    print(f"Found {len(detections)} cattle face(s)")
    for det in detections:
        print(f"  Confidence: {det['confidence']:.2f}, BBox: {det['bbox']}")
