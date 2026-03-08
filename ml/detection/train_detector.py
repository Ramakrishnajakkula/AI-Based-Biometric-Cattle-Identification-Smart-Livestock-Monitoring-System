"""
YOLOv8 Cattle Face/Muzzle Detection - Training Script
Author: Ramakrishna
"""

from ultralytics import YOLO
import os

def train_detector(
    model_size: str = "yolov8s.pt",
    data_yaml: str = "data.yaml",
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    project: str = "runs/detect",
    name: str = "cattle_face"
):
    """
    Train YOLOv8 model for cattle face/muzzle detection.
    
    Args:
        model_size: Pretrained model (yolov8n/s/m/l/x.pt)
        data_yaml: Path to dataset configuration
        epochs: Number of training epochs
        imgsz: Input image size
        batch: Batch size
        project: Output directory
        name: Experiment name
    """
    model = YOLO(model_size)
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        patience=20,
        save=True,
        verbose=True
    )
    
    return results


if __name__ == "__main__":
    train_detector()
