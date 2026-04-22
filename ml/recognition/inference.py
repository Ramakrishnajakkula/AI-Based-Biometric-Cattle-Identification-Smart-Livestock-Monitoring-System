"""
ArcFace Cattle Muzzle Embedding - Inference Script
Author: Ramakrishna
"""

import torch
import torch.nn as nn
import numpy as np
import cv2
from pathlib import Path
from torchvision import models, transforms


class CattleEmbeddingNet(nn.Module):
    """Lightweight embedding model with a ResNet18 backbone."""

    def __init__(self, embedding_dim: int = 512):
        super().__init__()
        backbone = models.resnet18(weights=None)
        in_features = backbone.fc.in_features
        backbone.fc = nn.Identity()

        self.backbone = backbone
        self.projection = nn.Linear(in_features, embedding_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)
        emb = self.projection(features)
        return nn.functional.normalize(emb, p=2, dim=1)


def _default_preprocess() -> transforms.Compose:
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])


def load_embedding_model(weights_path: str = "weights/arcface_cattle.pth"):
    """Load trained embedding model checkpoint.

    Checkpoint format supported:
    - raw state_dict (legacy)
    - dict with keys: model_state_dict, embedding_dim
    """
    path = Path(weights_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    if not path.exists():
        raise FileNotFoundError(f"Embedding weights not found: {path}")

    checkpoint = torch.load(path, map_location="cpu")
    embedding_dim = 512
    state_dict = checkpoint

    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
        embedding_dim = int(checkpoint.get("embedding_dim", 512))

    model = CattleEmbeddingNet(embedding_dim=embedding_dim)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def generate_embedding(model, image: np.ndarray) -> np.ndarray:
    """
    Generate 512-d embedding vector for a cattle muzzle image.
    
    Args:
        model: Loaded ArcFace model
        image: Cropped muzzle image (numpy array)
    
    Returns:
        512-dimensional embedding vector (numpy array)
    """
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a valid numpy array")

    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError("Unsupported image format")

    preprocess = _default_preprocess()
    tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        embedding = model(tensor).squeeze(0).cpu().numpy()

    return embedding.astype(np.float32)


if __name__ == "__main__":
    model = load_embedding_model()
    print("Embedding model loaded successfully")
