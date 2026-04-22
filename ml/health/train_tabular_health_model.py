"""
Train a tabular health-status model from the generated cattle master dataset.

Input (default):
    data/processed/cattle_master/cattle_master_dataset.csv

Outputs:
    ml/health/weights/tabular_health_model.joblib
    ml/health/weights/tabular_health_metrics.json

Usage:
    python ml/health/train_tabular_health_model.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "data" / "processed" / "cattle_master" / "cattle_master_dataset.csv"
DEFAULT_OUTPUT_DIR = ROOT / "ml" / "health" / "weights"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train tabular cattle health model")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET), help="Path to cattle_master_dataset.csv")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Folder to save model and metrics")
    parser.add_argument("--test-size", type=float, default=0.2, help="Validation split ratio")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args()


def pick_features(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric = [
        "age_years",
        "weight_kg",
        "loan_amount_inr",
        "interest_rate_annual_pct",
        "tenure_months",
        "emi_inr",
        "outstanding_amount_inr",
        "temperature_c",
        "heart_rate_bpm",
        "respiration_rate_per_min",
        "body_condition_score",
    ]
    categorical = [
        "breed",
        "gender",
        "farm_id",
        "loan_type",
        "repayment_status",
        "disease_label",
        "activity_level",
        "vaccination_status",
    ]

    numeric = [c for c in numeric if c in df.columns]
    categorical = [c for c in categorical if c in df.columns]
    return numeric, categorical


def main() -> None:
    args = parse_args()
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)
    if "health_status" not in df.columns:
        raise ValueError("Dataset must contain a 'health_status' column")

    y = df["health_status"].astype(str)
    numeric_features, categorical_features = pick_features(df)
    feature_cols = numeric_features + categorical_features
    if not feature_cols:
        raise ValueError("No valid feature columns found for training")

    x = df[feature_cols].copy()

    # Use stratified split only when each class has enough samples.
    class_counts = y.value_counts()
    can_stratify = bool((class_counts >= 2).all())
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=y if can_stratify else None,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                    ]
                ),
                numeric_features,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=args.seed,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    model.fit(x_train, y_train)
    preds = model.predict(x_test)

    accuracy = float(accuracy_score(y_test, preds))
    report = classification_report(y_test, preds, output_dict=True, zero_division=0)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "tabular_health_model.joblib"
    metrics_path = output_dir / "tabular_health_metrics.json"

    dump(
        {
            "model": model,
            "feature_columns": feature_cols,
            "target_column": "health_status",
            "classes": sorted(y.unique().tolist()),
        },
        model_path,
    )

    metrics_payload = {
        "dataset": str(dataset_path),
        "num_rows": int(len(df)),
        "num_train": int(len(x_train)),
        "num_test": int(len(x_test)),
        "accuracy": accuracy,
        "classification_report": report,
    }
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print("Training complete")
    print(f"- accuracy: {accuracy:.4f}")
    print(f"- model: {model_path}")
    print(f"- metrics: {metrics_path}")


if __name__ == "__main__":
    main()
