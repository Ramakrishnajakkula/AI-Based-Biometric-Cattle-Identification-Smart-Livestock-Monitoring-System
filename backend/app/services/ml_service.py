"""
ML Service — Interface between Flask routes and ML pipeline
Author: Akash

Wraps Ramakrishna's ML modules for use within Flask routes.
"""

import os
import logging
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from joblib import load

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TABULAR_MODEL_PATH = ROOT / "ml" / "health" / "weights" / "tabular_health_model.joblib"
MASTER_DATASET_PATH = ROOT / "data" / "processed" / "cattle_master" / "cattle_master_dataset.csv"

_TABULAR_MODEL_ARTIFACT: dict[str, Any] | None = None
_MASTER_DATASET_DF: pd.DataFrame | None = None


def detect_and_identify(image_path: str) -> dict:
    """
    Detect cattle face in image and identify via muzzle embedding.
    
    Returns:
        dict with keys: identified, cattle_id, confidence, detected
    """
    try:
        from ml.recognition.face_matcher import identify_cattle as identify_pipeline

        result = identify_pipeline(image_path)
        return {
            "identified": bool(result.get("status") == "matched"),
            "detected": bool(result.get("detected", False)),
            "cattle_id": result.get("cattle_id"),
            "confidence": float(result.get("confidence", 0.0)),
            "status": result.get("status", "no_match"),
            "bbox": result.get("bbox"),
            "message": result.get("error") if result.get("status") == "error" else None,
        }
    
    except Exception as e:
        logger.error(f"ML identification error: {e}")
        return {"identified": False, "detected": False, "status": "error", "error": str(e)}


def detect_health_issues(image_path: str) -> dict:
    """
    Detect visible health issues from cattle image.
    
    Returns:
        dict with detected conditions and severity.
    """
    try:
        from ml.health.predict_health import detect_health_issues as ml_detect

        conditions = ml_detect(image_path)
        return {"conditions": conditions, "count": len(conditions)}
    
    except Exception as e:
        logger.error(f"Health detection error: {e}")
        return {"conditions": [], "error": str(e)}


def _load_tabular_model_artifact() -> dict[str, Any]:
    global _TABULAR_MODEL_ARTIFACT

    if _TABULAR_MODEL_ARTIFACT is not None:
        return _TABULAR_MODEL_ARTIFACT

    if not TABULAR_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Tabular health model not found at {TABULAR_MODEL_PATH}. "
            "Run ml/health/train_tabular_health_model.py first."
        )

    artifact = load(TABULAR_MODEL_PATH)
    if not isinstance(artifact, dict) or "model" not in artifact or "feature_columns" not in artifact:
        raise ValueError("Invalid tabular model artifact format")

    _TABULAR_MODEL_ARTIFACT = artifact
    return artifact


def _load_master_dataset() -> pd.DataFrame:
    global _MASTER_DATASET_DF

    if _MASTER_DATASET_DF is not None:
        return _MASTER_DATASET_DF

    if not MASTER_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Master dataset not found at {MASTER_DATASET_PATH}. "
            "Run scripts/create_cattle_master_dataset.py first."
        )

    _MASTER_DATASET_DF = pd.read_csv(MASTER_DATASET_PATH)
    return _MASTER_DATASET_DF


def get_tabular_features_by_tag_id(tag_id: str) -> dict[str, Any]:
    """
    Fetch feature values from generated master dataset using cattle tag_id.
    """
    artifact = _load_tabular_model_artifact()
    feature_columns = artifact["feature_columns"]

    df = _load_master_dataset()
    row = df[df["tag_id"] == tag_id]
    if row.empty:
        raise ValueError(f"No dataset row found for tag_id={tag_id}")

    sample = row.iloc[0].to_dict()
    return {col: sample.get(col) for col in feature_columns}


def predict_tabular_health_status(features: dict[str, Any]) -> dict[str, Any]:
    """
    Predict cattle health_status from tabular feature fields.

    Expected fields are those saved in model artifact under feature_columns.
    Missing fields are allowed and will be imputed by the model pipeline.
    """
    try:
        artifact = _load_tabular_model_artifact()
        model = artifact["model"]
        feature_columns = artifact["feature_columns"]

        row = {col: features.get(col) for col in feature_columns}
        frame = pd.DataFrame([row], columns=feature_columns)

        pred = model.predict(frame)[0]

        probabilities = None
        confidence = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(frame)[0]
            labels = list(model.classes_)
            probabilities = {str(label): float(score) for label, score in zip(labels, proba)}
            confidence = float(max(probabilities.values()))

        return {
            "predicted_health_status": str(pred),
            "confidence": confidence,
            "probabilities": probabilities,
            "features_used": feature_columns,
        }
    except Exception as e:
        logger.error(f"Tabular health prediction error: {e}")
        return {"error": str(e)}
