"""
Cattle Face Matching - Compare embeddings against gallery database
Author: Ramakrishna
"""

import numpy as np
from typing import Optional


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Calculate cosine similarity between two embeddings."""
    dot = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    return float(dot / (norm1 * norm2))


def match_cattle(
    query_embedding: np.ndarray,
    gallery: list,
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
    if not gallery:
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
    # TODO: Implement full pipeline
    # 1. Load detection model → detect face/muzzle
    # 2. Crop muzzle region
    # 3. Load embedding model → generate embedding
    # 4. Load gallery from MongoDB
    # 5. Match against gallery
    # 6. Return result
    pass
