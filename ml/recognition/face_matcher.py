"""
Cattle Face Matching - Compare embeddings against gallery database
Author: Ramakrishna
"""

import numpy as np
import cv2
from typing import Optional, List, Dict

try:
    from ml.detection.predict import load_model, detect_cattle_face, crop_muzzle
    from ml.recognition.inference import load_embedding_model, generate_embedding
    from ml.recognition.gallery_builder import build_gallery
except ImportError:
    from ..detection.predict import load_model, detect_cattle_face, crop_muzzle
    from .inference import load_embedding_model, generate_embedding
    from .gallery_builder import build_gallery


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Calculate cosine similarity between two embeddings."""
    if embedding1 is None or embedding2 is None:
        return -1.0

    if embedding1.ndim != 1:
        embedding1 = embedding1.reshape(-1)
    if embedding2.ndim != 1:
        embedding2 = embedding2.reshape(-1)

    dot = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    if norm1 == 0 or norm2 == 0:
        return -1.0
    return float(dot / (norm1 * norm2))


def match_cattle(
    query_embedding: np.ndarray,
    gallery: List[Dict],
    threshold: float = 0.6
) -> dict:
    """
    Match a query embedding against the gallery database.
    
    Args:
        query_embedding: 512-d embedding of query muzzle
        gallery: List of {"cattle_id": str, "embedding": np.ndarray}
        threshold: Minimum similarity to consider a match
    
    Returns:
        {
            "cattle_id": str or None,
            "confidence": float,
            "status": "matched" | "no_match" | "low_confidence"
        }
    """
    if not gallery or query_embedding is None:
        return {"cattle_id": None, "confidence": 0.0, "status": "no_match"}
    
    best_match = None
    best_score = -1.0
    
    for entry in gallery:
        score = cosine_similarity(query_embedding, entry["embedding"])
        if score > best_score:
            best_score = score
            best_match = entry["cattle_id"]
    
    if best_score >= threshold:
        return {
            "cattle_id": best_match,
            "confidence": best_score,
            "status": "matched"
        }
    elif best_score >= threshold - 0.1:
        return {
            "cattle_id": best_match,
            "confidence": best_score,
            "status": "low_confidence"
        }
    else:
        return {
            "cattle_id": None,
            "confidence": best_score,
            "status": "no_match"
        }


def identify_cattle(image_path: str) -> dict:
    """
    Full identification pipeline: detect → crop → embed → match.
    
    This is the main function called by Akash's backend service.
    
    Args:
        image_path: Path to input cattle image
    
    Returns:
        {
            "cattle_id": "CTL-001" or None,
            "confidence": 0.87,
            "embedding": [...],
            "bbox": [x1, y1, x2, y2],
            "status": "matched" | "no_match" | "low_confidence"
        }
    """
    try:
        detection_model = load_model()
        detections = detect_cattle_face(detection_model, image_path)
        detected = bool(detections)

        if detected:
            best_det = max(detections, key=lambda d: d["confidence"])
            bbox = best_det["bbox"]
            muzzle_crop = crop_muzzle(image_path, bbox)
        else:
            # Early model fallback: use the full image as a pseudo-crop.
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Unable to read image: {image_path}")
            h, w = image.shape[:2]
            bbox = [0.0, 0.0, float(w), float(h)]
            muzzle_crop = image

        embedding_model = load_embedding_model()
        query_embedding = generate_embedding(embedding_model, muzzle_crop)

        gallery = build_gallery()
        match = match_cattle(query_embedding, gallery)

        return {
            "cattle_id": match["cattle_id"],
            "confidence": float(match["confidence"]),
            "embedding": query_embedding.tolist(),
            "bbox": bbox,
            "status": match["status"],
            "detected": detected,
        }
    except Exception as exc:
        return {
            "cattle_id": None,
            "confidence": 0.0,
            "embedding": None,
            "bbox": None,
            "status": "error",
            "detected": False,
            "error": str(exc),
        }
