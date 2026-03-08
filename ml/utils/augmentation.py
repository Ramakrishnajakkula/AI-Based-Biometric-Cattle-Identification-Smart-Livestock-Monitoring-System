"""
Data Augmentation Pipelines (Shared by Ramakrishna + Aditi)
"""

import albumentations as A
from albumentations.pytorch import ToTensorV2


def get_training_augmentation():
    """Standard augmentation pipeline for training."""
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.Rotate(limit=15, p=0.3),
        A.GaussNoise(var_limit=(10, 50), p=0.2),
        A.Blur(blur_limit=3, p=0.1),
        A.CLAHE(clip_limit=2.0, p=0.3),
    ])


def get_validation_augmentation():
    """Minimal augmentation for validation (just resize)."""
    return A.Compose([
        A.Resize(640, 640),
    ])
