"""
Suggest ID mappings from gallery IDs to app tag IDs using embedding similarity.

Expected enrollment structure:
  backend/uploads/cattle_images/<TAG_ID>/*.jpg

This script computes mean embedding per app tag from enrollment images,
then matches each gallery embedding to the closest app tag by cosine similarity.

Usage:
  python scripts/suggest_id_mapping.py --show-top 10
  python scripts/suggest_id_mapping.py --threshold 0.75 --apply
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.recognition.inference import load_embedding_model, generate_embedding
from ml.recognition.gallery_builder import build_gallery, load_id_mapping, save_id_mapping


ENROLLMENT_DIR = ROOT / "backend" / "uploads" / "cattle_images"
SUGGESTIONS_PATH = ROOT / "ml" / "recognition" / "weights" / "id_mapping_suggestions.json"


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return -1.0
    return float(np.dot(a, b) / (na * nb))


def build_tag_centroids(model, enrollment_dir: Path) -> Dict[str, np.ndarray]:
    centroids: Dict[str, np.ndarray] = {}

    tag_dirs = sorted([p for p in enrollment_dir.iterdir() if p.is_dir()])
    for tag_dir in tag_dirs:
        vectors: List[np.ndarray] = []
        for img_path in sorted(tag_dir.iterdir()):
            if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
                continue
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            vectors.append(generate_embedding(model, img))

        if vectors:
            centroids[tag_dir.name] = np.mean(np.stack(vectors, axis=0), axis=0)

    return centroids


def suggest_mappings(
    gallery: List[Dict],
    tag_centroids: Dict[str, np.ndarray],
) -> List[Dict[str, object]]:
    suggestions: List[Dict[str, object]] = []

    for entry in gallery:
        gallery_id = str(entry["cattle_id"])
        emb = np.asarray(entry["embedding"], dtype=np.float32)

        best_tag = None
        best_score = -1.0
        for tag, centroid in tag_centroids.items():
            score = cosine_similarity(emb, centroid)
            if score > best_score:
                best_score = score
                best_tag = tag

        if best_tag is not None:
            suggestions.append({
                "source_id": gallery_id,
                "suggested_tag": best_tag,
                "similarity": round(float(best_score), 6),
            })

    suggestions.sort(key=lambda x: float(x["similarity"]), reverse=True)
    return suggestions


def apply_suggestions(suggestions: List[Dict[str, object]], threshold: float) -> int:
    mapping = load_id_mapping()
    applied = 0

    for item in suggestions:
        score = float(item["similarity"])
        if score < threshold:
            continue

        source_id = str(item["source_id"])
        target_tag = str(item["suggested_tag"])
        mapping[source_id] = target_tag
        applied += 1

    save_id_mapping(mapping)
    return applied


def main() -> None:
    parser = argparse.ArgumentParser(description="Suggest gallery-to-app ID mappings")
    parser.add_argument("--enrollment-dir", default=str(ENROLLMENT_DIR), help="Enrollment root with per-tag subfolders")
    parser.add_argument("--threshold", type=float, default=0.75, help="Minimum similarity to apply mapping")
    parser.add_argument("--apply", action="store_true", help="Apply suggestions to id_mapping.json")
    parser.add_argument("--show-top", type=int, default=20, help="Number of top suggestions to print")
    args = parser.parse_args()

    enrollment_dir = Path(args.enrollment_dir)
    if not enrollment_dir.exists():
        raise FileNotFoundError(f"Enrollment directory not found: {enrollment_dir}")

    model = load_embedding_model("weights/arcface_cattle.pth")
    tag_centroids = build_tag_centroids(model, enrollment_dir)
    if not tag_centroids:
        print("No enrollment embeddings found. Add images under backend/uploads/cattle_images/<TAG_ID>/")
        return

    gallery = build_gallery()
    if not gallery:
        print("Gallery is empty. Seed gallery first.")
        return

    suggestions = suggest_mappings(gallery, tag_centroids)

    SUGGESTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUGGESTIONS_PATH.open("w", encoding="utf-8") as f:
        json.dump(suggestions, f, indent=2)

    top_n = max(1, args.show_top)
    print(f"Top {top_n} suggestions:")
    for item in suggestions[:top_n]:
        print(item)

    print(f"Saved suggestions: {SUGGESTIONS_PATH}")

    if args.apply:
        applied = apply_suggestions(suggestions, threshold=args.threshold)
        print(f"Applied mappings (threshold={args.threshold}): {applied}")


if __name__ == "__main__":
    main()
