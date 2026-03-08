"""
Gallery Builder - Build and manage embedding gallery for cattle identification
Author: Ramakrishna
"""

import numpy as np
from pymongo import MongoClient
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


def build_gallery_from_db() -> List[Dict]:
    """
    Load all cattle embeddings from MongoDB into memory for matching.
    
    Returns:
        List of {"cattle_id": str, "embedding": np.ndarray}
    """
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


def add_to_gallery(cattle_id: str, embedding: np.ndarray, model_version: str = "v1"):
    """
    Add a new cattle embedding to the gallery database.
    
    Args:
        cattle_id: Unique cattle identifier
        embedding: 512-d embedding vector
        model_version: Version of the embedding model used
    """
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


if __name__ == "__main__":
    gallery = build_gallery_from_db()
    print(f"Gallery loaded: {len(gallery)} cattle embeddings")
