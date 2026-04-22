"""
Seed local gallery embeddings from a recognition dataset.

This generates one embedding per class folder and writes to gallery storage
(MongoDB if available, otherwise local JSON fallback).

Usage:
  python scripts/seed_gallery_from_dataset.py
  python scripts/seed_gallery_from_dataset.py --dataset-dir ml/recognition/datasets_real --limit 50
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.recognition.inference import load_embedding_model, generate_embedding
from ml.recognition.gallery_builder import add_to_gallery

DEFAULT_DATASET = ROOT / "ml" / "recognition" / "datasets_real"


def seed_gallery(dataset_dir: Path, limit: int | None = None) -> int:
    model = load_embedding_model("weights/arcface_cattle.pth")

    class_dirs = sorted([p for p in dataset_dir.iterdir() if p.is_dir()])
    if limit is not None:
        class_dirs = class_dirs[:limit]

    seeded = 0
    for class_dir in class_dirs:
        img_files = sorted([p for p in class_dir.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}])
        if not img_files:
            continue

        img = cv2.imread(str(img_files[0]))
        if img is None:
            continue

        emb = generate_embedding(model, img)
        add_to_gallery(class_dir.name, emb)
        seeded += 1

    return seeded


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed gallery from class folders")
    parser.add_argument("--dataset-dir", default=str(DEFAULT_DATASET), help="ImageFolder recognition dataset path")
    parser.add_argument("--limit", type=int, default=None, help="Optional cap for number of classes to seed")
    args = parser.parse_args()

    dataset_dir = Path(args.dataset_dir)
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset path not found: {dataset_dir}")

    seeded = seed_gallery(dataset_dir, args.limit)
    print(f"Gallery seeded classes: {seeded}")


if __name__ == "__main__":
    main()
