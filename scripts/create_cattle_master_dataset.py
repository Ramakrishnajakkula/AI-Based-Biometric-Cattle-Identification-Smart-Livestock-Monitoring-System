"""
Create a custom cattle master dataset by combining online image data with
generated metadata for ownership, loans, health, and GPS tracks.

Typical usage:
    python scripts/create_cattle_master_dataset.py --download-online --num-cattle 300

This script can:
1) Optionally call scripts/download_datasets.py to fetch online cattle images.
2) Build a unified dataset under data/processed/cattle_master.
3) Export both JSON and CSV files for easy ML and backend usage.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, List


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed" / "cattle_master"
DETECTION_IMAGES_DIR = ROOT / "ml" / "detection" / "datasets" / "images"
HEALTH_IMAGES_DIR = ROOT / "ml" / "health" / "datasets" / "images"
DEFAULT_SOURCE_CONFIG = ROOT / "scripts" / "dataset_sources.example.json"


BREEDS = [
    "Gir",
    "Sahiwal",
    "Red Sindhi",
    "Tharparkar",
    "Ongole",
    "Jersey",
    "Holstein Friesian",
]

OWNER_FIRST_NAMES = [
    "Ravi",
    "Suresh",
    "Lakshmi",
    "Anitha",
    "Praveen",
    "Divya",
    "Kiran",
    "Madhavi",
    "Arjun",
    "Pooja",
]

OWNER_LAST_NAMES = [
    "Reddy",
    "Kumar",
    "Naik",
    "Patel",
    "Sharma",
    "Yadav",
    "Singh",
    "Rao",
    "Das",
    "Chowdary",
]

FARM_NAMES = [
    "Green Valley Farm",
    "Lakshmi Dairy",
    "Sunrise Agro Farm",
    "Annapurna Cattle Shed",
    "Sri Sai Livestock",
]


@dataclass
class FarmCenter:
    farm_id: str
    farm_name: str
    lat: float
    lng: float


FARM_CENTERS = [
    FarmCenter("FARM-01", FARM_NAMES[0], 17.3850, 78.4867),
    FarmCenter("FARM-02", FARM_NAMES[1], 17.4005, 78.4709),
    FarmCenter("FARM-03", FARM_NAMES[2], 17.4483, 78.3915),
    FarmCenter("FARM-04", FARM_NAMES[3], 17.3201, 78.5616),
    FarmCenter("FARM-05", FARM_NAMES[4], 17.2956, 78.5021),
]


def run_online_download(config_path: Path) -> None:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "download_datasets.py"),
        "--config",
        str(config_path),
    ]
    print("[step] Downloading online datasets...")
    subprocess.run(command, check=True)


def collect_image_paths(image_roots: Iterable[Path]) -> List[Path]:
    supported = {".jpg", ".jpeg", ".png", ".bmp"}
    images: List[Path] = []
    for root in image_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in supported:
                images.append(path)
    return sorted(images)


def random_owner(rng: random.Random, idx: int) -> dict:
    first = rng.choice(OWNER_FIRST_NAMES)
    last = rng.choice(OWNER_LAST_NAMES)
    owner_id = f"OWN-{idx:04d}"
    return {
        "owner_id": owner_id,
        "owner_name": f"{first} {last}",
        "owner_phone": f"+91{rng.randint(7000000000, 9999999999)}",
        "owner_village": f"Village-{rng.randint(1, 80)}",
        "owner_district": rng.choice(["Hyderabad", "Medchal", "Rangareddy", "Sangareddy"]),
        "owner_state": "Telangana",
    }


def generate_loan_info(rng: random.Random, age_years: int, weight_kg: int) -> dict:
    has_loan = rng.random() < 0.62
    if not has_loan:
        return {
            "has_loan": False,
            "loan_id": None,
            "loan_type": None,
            "loan_amount_inr": 0,
            "interest_rate_annual_pct": 0.0,
            "tenure_months": 0,
            "emi_inr": 0,
            "outstanding_amount_inr": 0,
            "repayment_status": "not_applicable",
            "last_payment_date": None,
        }

    amount = rng.randint(15000, 120000) + max(0, (weight_kg - 250) * 35)
    interest = round(rng.uniform(7.5, 16.5), 2)
    tenure = rng.choice([12, 18, 24, 36, 48])
    monthly_rate = interest / 1200.0
    emi = int((amount * monthly_rate * (1 + monthly_rate) ** tenure) / (((1 + monthly_rate) ** tenure) - 1))
    paid_ratio = min(0.95, max(0.05, age_years / 10.0 + rng.uniform(-0.1, 0.2)))
    outstanding = int(amount * (1.0 - paid_ratio))

    return {
        "has_loan": True,
        "loan_id": f"LN-{rng.randint(100000, 999999)}",
        "loan_type": rng.choice(["livestock", "farm_equipment", "working_capital"]),
        "loan_amount_inr": amount,
        "interest_rate_annual_pct": interest,
        "tenure_months": tenure,
        "emi_inr": emi,
        "outstanding_amount_inr": max(0, outstanding),
        "repayment_status": rng.choices(
            ["on_time", "delayed", "default_risk"],
            weights=[70, 23, 7],
            k=1,
        )[0],
        "last_payment_date": (datetime.now(timezone.utc) - timedelta(days=rng.randint(3, 65))).date().isoformat(),
    }


def generate_health_profile(rng: random.Random) -> dict:
    base_temp = round(rng.uniform(38.0, 39.4), 1)
    heart_rate = rng.randint(48, 88)
    activity = rng.choice(["low", "normal", "high"])
    disease = rng.choices(
        ["none", "mastitis", "foot_and_mouth_suspected", "skin_infection", "fever"],
        weights=[72, 8, 3, 7, 10],
        k=1,
    )[0]

    if disease == "none" and base_temp <= 39.2 and activity != "low":
        status = "healthy"
    elif disease in {"foot_and_mouth_suspected", "fever"} or base_temp >= 39.5:
        status = "critical"
    else:
        status = "watch"

    return {
        "health_status": status,
        "disease_label": disease,
        "temperature_c": base_temp,
        "heart_rate_bpm": heart_rate,
        "respiration_rate_per_min": rng.randint(16, 36),
        "activity_level": activity,
        "body_condition_score": round(rng.uniform(2.0, 4.5), 1),
        "vaccination_status": rng.choice(["up_to_date", "partial", "overdue"]),
        "last_health_check_date": (datetime.now(timezone.utc) - timedelta(days=rng.randint(1, 60))).date().isoformat(),
    }


def generate_gps_track(rng: random.Random, center: FarmCenter, points: int = 24) -> list[dict]:
    now = datetime.now(timezone.utc)
    rows = []
    lat = center.lat
    lng = center.lng
    for i in range(points):
        ts = now - timedelta(hours=(points - 1 - i))
        lat += rng.uniform(-0.0009, 0.0009)
        lng += rng.uniform(-0.0009, 0.0009)
        rows.append(
            {
                "timestamp": ts.isoformat(),
                "lat": round(lat, 6),
                "lng": round(lng, 6),
                "speed_kmph": round(max(0.0, rng.gauss(2.5, 1.2)), 2),
                "within_geofence": rng.random() > 0.06,
            }
        )
    return rows


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: object) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def write_flat_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    headers = sorted(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def build_dataset(
    num_cattle: int,
    seed: int,
    image_paths: list[Path],
    output_dir: Path,
) -> dict:
    if not image_paths:
        raise RuntimeError(
            "No images found. Download datasets first using scripts/download_datasets.py "
            "or run this script with --download-online."
        )

    rng = random.Random(seed)
    rows = []
    gps_rows = []

    for idx in range(1, num_cattle + 1):
        image = image_paths[(idx - 1) % len(image_paths)]
        breed = rng.choice(BREEDS)
        age_years = rng.randint(1, 12)
        weight_kg = rng.randint(180, 650)
        farm = rng.choice(FARM_CENTERS)
        owner = random_owner(rng, idx)
        loan_info = generate_loan_info(rng, age_years, weight_kg)
        health_info = generate_health_profile(rng)
        tag_id = f"CTL-{idx:05d}"

        gps_track = generate_gps_track(rng, farm)
        latest_gps = gps_track[-1]

        record = {
            "cattle_id": f"c{idx}",
            "tag_id": tag_id,
            "name": f"Cattle-{idx:05d}",
            "breed": breed,
            "age_years": age_years,
            "gender": rng.choice(["female", "male"]),
            "weight_kg": weight_kg,
            "farm_id": farm.farm_id,
            "farm_name": farm.farm_name,
            "registered_at": (datetime.now(timezone.utc) - timedelta(days=rng.randint(20, 1200))).date().isoformat(),
            "image_path": str(image.relative_to(ROOT).as_posix()),
            "gps_last_lat": latest_gps["lat"],
            "gps_last_lng": latest_gps["lng"],
        }
        record.update(owner)
        record.update(loan_info)
        record.update(health_info)
        rows.append(record)

        for point in gps_track:
            gps_rows.append(
                {
                    "tag_id": tag_id,
                    "farm_id": farm.farm_id,
                    "timestamp": point["timestamp"],
                    "lat": point["lat"],
                    "lng": point["lng"],
                    "speed_kmph": point["speed_kmph"],
                    "within_geofence": point["within_geofence"],
                }
            )

    payload = {
        "meta": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "num_cattle": len(rows),
            "num_gps_points": len(gps_rows),
            "seed": seed,
            "source_images_count": len(image_paths),
            "note": "Loan, health, and GPS fields are synthetic but structured for app/ML usage.",
        },
        "cattle": rows,
        "gps_history": gps_rows,
    }

    ensure_output_dir(output_dir)
    write_json(output_dir / "cattle_master_dataset.json", payload)
    write_flat_csv(output_dir / "cattle_master_dataset.csv", rows)
    write_flat_csv(output_dir / "cattle_gps_history.csv", gps_rows)

    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create custom cattle master dataset")
    parser.add_argument("--num-cattle", type=int, default=200, help="Number of cattle records to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible generation")
    parser.add_argument("--download-online", action="store_true", help="First download online datasets via download_datasets.py")
    parser.add_argument(
        "--source-config",
        default=str(DEFAULT_SOURCE_CONFIG),
        help="Config path used by download_datasets.py",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for generated dataset files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.num_cattle <= 0:
        raise ValueError("--num-cattle must be > 0")

    if args.download_online:
        run_online_download(Path(args.source_config))

    image_paths = collect_image_paths(
        [
            DETECTION_IMAGES_DIR,
            HEALTH_IMAGES_DIR,
        ]
    )

    payload = build_dataset(
        num_cattle=args.num_cattle,
        seed=args.seed,
        image_paths=image_paths,
        output_dir=Path(args.output_dir),
    )

    meta = payload["meta"]
    print("\nDataset generation complete")
    print(f"- cattle records: {meta['num_cattle']}")
    print(f"- gps points: {meta['num_gps_points']}")
    print(f"- source images used: {meta['source_images_count']}")
    print(f"- output folder: {Path(args.output_dir)}")


if __name__ == "__main__":
    main()
