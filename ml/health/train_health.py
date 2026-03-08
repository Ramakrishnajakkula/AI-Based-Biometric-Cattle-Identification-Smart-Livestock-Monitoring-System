"""
YOLOv8 Health Condition Detection - Training Script
Author: Aditi
"""

from ultralytics import YOLO


def train_health_detector(
    model_size: str = "yolov8s.pt",
    data_yaml: str = "data.yaml",
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16
):
    """
    Train YOLOv8 model for cattle health condition detection.
    
    Classes: wound, eye_redness, skin_lesion, lameness, healthy
    """
    model = YOLO(model_size)
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project="runs/health",
        name="cattle_health",
        patience=20,
        save=True,
        verbose=True
    )
    
    return results


if __name__ == "__main__":
    train_health_detector()
