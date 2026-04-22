"""
ArcFace Cattle Muzzle Embedding - Training Script
Author: Ramakrishna
"""

from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


class CattleEmbeddingNet(nn.Module):
    """ResNet18 backbone + normalized embedding head."""

    def __init__(self, embedding_dim: int = 512):
        super().__init__()
        backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        in_features = backbone.fc.in_features
        backbone.fc = nn.Identity()

        self.backbone = backbone
        self.projection = nn.Linear(in_features, embedding_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)
        emb = self.projection(features)
        return nn.functional.normalize(emb, p=2, dim=1)


def train_embedding_model(
    data_dir: str = "datasets/",
    epochs: int = 50,
    batch_size: int = 32,
    embedding_dim: int = 512,
    lr: float = 0.001
):
    """
    Train ArcFace embedding model for cattle muzzle recognition.
    
    Args:
        data_dir: Directory with ID-labeled cattle muzzle crops
        epochs: Training epochs
        batch_size: Batch size
        embedding_dim: Embedding vector dimension
        lr: Learning rate
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {data_dir}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[train] device={device}")

    transform = transforms.Compose([
        transforms.Resize((112, 112)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    dataset = datasets.ImageFolder(root=str(data_path), transform=transform)
    if len(dataset.classes) < 2:
        raise ValueError("Need at least 2 cattle IDs (class folders) for training")

    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    num_classes = len(dataset.classes)

    model = CattleEmbeddingNet(embedding_dim=embedding_dim).to(device)
    classifier = nn.Linear(embedding_dim, num_classes).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(list(model.parameters()) + list(classifier.parameters()), lr=lr)

    best_loss = float("inf")
    out_dir = Path(__file__).resolve().parent / "weights"
    out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = out_dir / "arcface_cattle.pth"

    for epoch in range(epochs):
        model.train()
        classifier.train()

        running_loss = 0.0
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            embeddings = model(images)
            logits = classifier(embeddings)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item())

        epoch_loss = running_loss / max(1, len(loader))
        print(f"[epoch {epoch + 1}/{epochs}] loss={epoch_loss:.4f}")

        if epoch_loss < best_loss:
            best_loss = epoch_loss
            torch.save({
                "model_state_dict": model.state_dict(),
                "embedding_dim": embedding_dim,
                "class_to_idx": dataset.class_to_idx,
                "best_loss": best_loss,
            }, checkpoint_path)
            print(f"[save] best checkpoint -> {checkpoint_path}")

    return {
        "checkpoint": str(checkpoint_path),
        "classes": dataset.class_to_idx,
        "best_loss": best_loss,
    }


if __name__ == "__main__":
    train_embedding_model()
