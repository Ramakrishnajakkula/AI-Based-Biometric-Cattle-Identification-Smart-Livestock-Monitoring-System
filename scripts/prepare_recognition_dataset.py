"""
Prepare a recognition ImageFolder dataset from Beef Cattle Muzzle data.

Input expected after extraction:
  data/raw/beef_muzzle/BeefCattle_Muzzle_Individualized/<cattle_id>/*.jpg

Output:
  ml/recognition/datasets_real/<cattle_id>/*.jpg

Usage:
  python scripts/prepare_recognition_dataset.py
  python scripts/prepare_recognition_dataset.py --max-classes 120 --max-images-per-class 20
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "beef_muzzle" / "BeefCattle_Muzzle_Individualized"
DEFAULT_OUTPUT = ROOT / "ml" / "recognition" / "datasets_real"


def prepare_dataset(
    input_dir: Path,
    output_dir: Path,
    max_classes: int | None,
    max_images_per_class: int | None,
) -> tuple[int, int]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    class_dirs = sorted([p for p in input_dir.iterdir() if p.is_dir()])
    if max_classes is not None:
        class_dirs = class_dirs[:max_classes]

    copied_classes = 0
    copied_images = 0

    for class_dir in class_dirs:
        images = sorted([p for p in class_dir.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}])
        if not images:
            continue

        if max_images_per_class is not None:
            images = images[:max_images_per_class]

        out_class = output_dir / class_dir.name
        out_class.mkdir(parents=True, exist_ok=True)

        class_copied = 0
        for img in images:
            dst = out_class / img.name
            if dst.exists():
                continue
            shutil.copy2(img, dst)
            copied_images += 1
            class_copied += 1

        if class_copied > 0:
            copied_classes += 1

    return copied_classes, copied_images


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare recognition dataset from Beef Cattle Muzzle data")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT), help="Input extracted dataset directory")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT), help="Output ImageFolder dataset directory")
    parser.add_argument("--max-classes", type=int, default=None, help="Optional cap on number of classes")
    parser.add_argument("--max-images-per-class", type=int, default=None, help="Optional cap on images per class")
    args = parser.parse_args()

    classes, images = prepare_dataset(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        max_classes=args.max_classes,
        max_images_per_class=args.max_images_per_class,
    )

    print(f"Prepared classes: {classes}")
    print(f"Prepared images: {images}")
    print(f"Output directory: {Path(args.output_dir)}")


if __name__ == "__main__":
    main()
