"""
Download and prepare online datasets for YOLO training.

This script downloads dataset archives from public URLs and reshapes them
into the repository layout expected by:
- ml/detection/data.yaml
- ml/health/data.yaml

Usage:
    python scripts/download_datasets.py --config scripts/dataset_sources.example.json

Override any URL via environment variables:
    DETECTION_DATASET_URL
    HEALTH_DATASET_URL
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parent.parent
DETECTION_DATASET_DIR = ROOT / "ml" / "detection" / "datasets"
HEALTH_DATASET_DIR = ROOT / "ml" / "health" / "datasets"


def load_config(config_path: Path) -> Dict[str, Dict[str, str]]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise ValueError("Config must be a JSON object")

    return raw


def download_file(url: str, destination: Path) -> None:
    print(f"[download] {url}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response, destination.open("wb") as out:
        shutil.copyfileobj(response, out)

    print(f"[saved] {destination}")


def extract_archive(archive_path: Path, extract_to: Path) -> Path:
    extract_to.mkdir(parents=True, exist_ok=True)

    if archive_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(extract_to)
    elif archive_path.suffix.lower() in {".tar", ".gz", ".tgz", ".bz2", ".xz"}:
        with tarfile.open(archive_path, "r:*") as tf:
            tf.extractall(extract_to)
    else:
        raise ValueError(f"Unsupported archive format: {archive_path.name}")

    children = [p for p in extract_to.iterdir() if p.is_dir()]
    if len(children) == 1:
        return children[0]

    return extract_to


def ensure_clean_layout(dataset_dir: Path) -> None:
    for rel in ("images/train", "images/val", "labels/train", "labels/val"):
        (dataset_dir / rel).mkdir(parents=True, exist_ok=True)


def copy_matching_files(src: Path, dst: Path, patterns: tuple[str, ...]) -> int:
    copied = 0
    for pattern in patterns:
        for file in src.rglob(pattern):
            if file.is_file():
                out = dst / file.name
                # Keep unique files when names collide.
                if out.exists():
                    out = dst / f"{file.stem}_{copied}{file.suffix}"
                shutil.copy2(file, out)
                copied += 1
    return copied


def map_roboflow_layout(extracted_root: Path, target_dir: Path) -> bool:
    train_dir = extracted_root / "train"
    valid_dir = extracted_root / "valid"
    val_dir = extracted_root / "val"

    if not train_dir.exists() or not (valid_dir.exists() or val_dir.exists()):
        return False

    val_source = valid_dir if valid_dir.exists() else val_dir

    print("[prepare] Detected Roboflow-style layout")
    copied = 0
    copied += copy_matching_files(train_dir / "images", target_dir / "images" / "train", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))
    copied += copy_matching_files(train_dir / "labels", target_dir / "labels" / "train", ("*.txt",))
    copied += copy_matching_files(val_source / "images", target_dir / "images" / "val", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))
    copied += copy_matching_files(val_source / "labels", target_dir / "labels" / "val", ("*.txt",))

    print(f"[prepare] Copied {copied} files")
    return copied > 0


def map_yolo_images_labels_layout(extracted_root: Path, target_dir: Path) -> bool:
    images = extracted_root / "images"
    labels = extracted_root / "labels"
    if not images.exists() or not labels.exists():
        return False

    print("[prepare] Detected images/labels layout")
    copied = 0
    copied += copy_matching_files(images / "train", target_dir / "images" / "train", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))
    copied += copy_matching_files(labels / "train", target_dir / "labels" / "train", ("*.txt",))

    # Accept either val or valid in source.
    val_image_source = images / "val" if (images / "val").exists() else images / "valid"
    val_label_source = labels / "val" if (labels / "val").exists() else labels / "valid"
    copied += copy_matching_files(val_image_source, target_dir / "images" / "val", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))
    copied += copy_matching_files(val_label_source, target_dir / "labels" / "val", ("*.txt",))

    print(f"[prepare] Copied {copied} files")
    return copied > 0


def prepare_dataset_from_archive(url: str, target_dir: Path) -> None:
    ensure_clean_layout(target_dir)

    with tempfile.TemporaryDirectory(prefix="cap_dataset_") as tmp:
        tmp_path = Path(tmp)
        archive_path = tmp_path / "dataset_archive"

        # Add extension so archive detection works.
        lower_url = url.lower()
        if lower_url.endswith(".zip"):
            archive_path = archive_path.with_suffix(".zip")
        elif lower_url.endswith(".tar.gz") or lower_url.endswith(".tgz"):
            archive_path = archive_path.with_suffix(".tar.gz")
        elif lower_url.endswith(".tar"):
            archive_path = archive_path.with_suffix(".tar")
        else:
            archive_path = archive_path.with_suffix(".zip")

        download_file(url, archive_path)
        extracted_root = extract_archive(archive_path, tmp_path / "extracted")

        mapped = map_roboflow_layout(extracted_root, target_dir)
        if not mapped:
            mapped = map_yolo_images_labels_layout(extracted_root, target_dir)

        if not mapped:
            raise RuntimeError(
                "Could not recognize dataset structure. Expected Roboflow-style "
                "(train/valid with images+labels) or YOLO-style (images/labels with train+val)."
            )


def get_dataset_url(
    config: Dict[str, Dict[str, str]],
    section: str,
    env_key: str,
) -> Optional[str]:
    env_value = os.getenv(env_key)
    if env_value:
        return env_value.strip()

    section_data = config.get(section, {})
    if isinstance(section_data, dict):
        value = section_data.get("url")
        if isinstance(value, str) and value.strip():
            return value.strip()

    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and prepare datasets")
    parser.add_argument(
        "--config",
        default=str(ROOT / "scripts" / "dataset_sources.example.json"),
        help="Path to dataset source config JSON",
    )
    parser.add_argument(
        "--skip-detection",
        action="store_true",
        help="Skip detection dataset download",
    )
    parser.add_argument(
        "--skip-health",
        action="store_true",
        help="Skip health dataset download",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    if not args.skip_detection:
        detection_url = get_dataset_url(config, "detection", "DETECTION_DATASET_URL")
        if detection_url:
            print("\n=== Detection dataset ===")
            prepare_dataset_from_archive(detection_url, DETECTION_DATASET_DIR)
        else:
            print("\n[skip] Detection dataset URL not provided")

    if not args.skip_health:
        health_url = get_dataset_url(config, "health", "HEALTH_DATASET_URL")
        if health_url:
            print("\n=== Health dataset ===")
            prepare_dataset_from_archive(health_url, HEALTH_DATASET_DIR)
        else:
            print("\n[skip] Health dataset URL not provided")

    print("\nDone. Datasets are available under:")
    print(f"- {DETECTION_DATASET_DIR}")
    print(f"- {HEALTH_DATASET_DIR}")


if __name__ == "__main__":
    main()
