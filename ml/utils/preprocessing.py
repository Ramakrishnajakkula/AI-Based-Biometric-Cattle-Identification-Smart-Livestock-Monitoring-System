"""
Image Preprocessing Utilities (Shared by Ramakrishna + Aditi)
"""

import cv2
import numpy as np


def preprocess_image(image_path: str, target_size: tuple = (640, 640)) -> np.ndarray:
    """Load and resize image to target size."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    image = cv2.resize(image, target_size)
    return image


def crop_region(image: np.ndarray, bbox: list) -> np.ndarray:
    """Crop a region from image using bounding box [x1, y1, x2, y2]."""
    x1, y1, x2, y2 = [int(c) for c in bbox]
    return image[y1:y2, x1:x2].copy()


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize pixel values to [0, 1] range."""
    return image.astype(np.float32) / 255.0


def resize_for_embedding(image: np.ndarray, size: tuple = (112, 112)) -> np.ndarray:
    """Resize cropped muzzle image for ArcFace embedding input."""
    return cv2.resize(image, size)
