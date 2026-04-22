"""
Gallery Builder - Build and manage embedding gallery for cattle identification
Author: Ramakrishna
"""

import numpy as np
from typing import List, Dict
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCAL_GALLERY = ROOT / "ml" / "recognition" / "weights" / "gallery.json"
DEFAULT_ID_MAPPING = ROOT / "ml" / "recognition" / "weights" / "id_mapping.json"


def _try_import_mongo_client():
    try:
        from pymongo import MongoClient  # type: ignore
        return MongoClient
    except Exception:
        return None


def _load_gallery_from_local_json(path: Path = DEFAULT_LOCAL_GALLERY) -> List[Dict]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        docs = json.load(f)

    gallery = []
    for doc in docs:
        gallery.append({
            "cattle_id": doc["cattle_id"],
            "embedding": np.array(doc["embedding_vector"], dtype=np.float32),
        })
    return gallery


def _save_gallery_to_local_json(entries: List[Dict], path: Path = DEFAULT_LOCAL_GALLERY) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = [
        {
            "cattle_id": item["cattle_id"],
            "embedding_vector": np.asarray(item["embedding"], dtype=np.float32).tolist(),
            "model_version": item.get("model_version", "v1"),
        }
        for item in entries
    ]

    with path.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


def load_id_mapping(path: Path = DEFAULT_ID_MAPPING) -> Dict[str, str]:
    """Load optional mapping from gallery cattle IDs to app tag IDs."""
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        mapping = json.load(f)

    if not isinstance(mapping, dict):
        return {}

    return {str(k): str(v) for k, v in mapping.items()}


def save_id_mapping(mapping: Dict[str, str], path: Path = DEFAULT_ID_MAPPING) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)


def resolve_cattle_id(cattle_id: str) -> str:
    """Resolve a predicted gallery cattle ID to app tag ID when mapping exists."""
    if not cattle_id:
        return cattle_id

    mapping = load_id_mapping()
    return mapping.get(cattle_id, cattle_id)


def build_gallery_from_db() -> List[Dict]:
    """
    Load all cattle embeddings from MongoDB into memory for matching.
    
    Returns:
        List of {"cattle_id": str, "embedding": np.ndarray}
    """
    MongoClient = _try_import_mongo_client()
    if MongoClient is None:
        return []

    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/cattle_monitoring"))
    db = client["cattle_monitoring"]
    
    gallery = []
    for doc in db.embeddings.find({}):
        gallery.append({
            "cattle_id": doc["cattle_id"],
            "embedding": np.array(doc["embedding_vector"])
        })
    
    client.close()
    return gallery


def build_gallery() -> List[Dict]:
    """Build gallery from MongoDB if available; fallback to local JSON."""
    gallery = build_gallery_from_db()
    if gallery:
        return gallery
    return _load_gallery_from_local_json()


def add_to_gallery(cattle_id: str, embedding: np.ndarray, model_version: str = "v1"):
    """
    Add a new cattle embedding to the gallery database.
    
    Args:
        cattle_id: Unique cattle identifier
        embedding: 512-d embedding vector
        model_version: Version of the embedding model used
    """
    MongoClient = _try_import_mongo_client()
    if MongoClient is not None:
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/cattle_monitoring"))
        db = client["cattle_monitoring"]

        db.embeddings.update_one(
            {"cattle_id": cattle_id},
            {"$set": {
                "cattle_id": cattle_id,
                "embedding_vector": embedding.tolist(),
                "model_version": model_version
            }},
            upsert=True
        )

        client.close()
        return

    # Local fallback storage for demo/no-DB mode.
    gallery = _load_gallery_from_local_json()
    updated = False
    for item in gallery:
        if item["cattle_id"] == cattle_id:
            item["embedding"] = np.asarray(embedding, dtype=np.float32)
            item["model_version"] = model_version
            updated = True
            break

    if not updated:
        gallery.append({
            "cattle_id": cattle_id,
            "embedding": np.asarray(embedding, dtype=np.float32),
            "model_version": model_version,
        })

    _save_gallery_to_local_json(gallery)


if __name__ == "__main__":
    gallery = build_gallery()
    print(f"Gallery loaded: {len(gallery)} cattle embeddings")
