"""
Create or update cattle ID mapping used by identify route.

Maps predicted gallery IDs (for example cattle_0900) to app tag IDs
(for example CTL-001).

Usage:
  python scripts/set_id_mapping.py --source-id cattle_0900 --target-tag CTL-001
  python scripts/set_id_mapping.py --show
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.recognition.gallery_builder import load_id_mapping, save_id_mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="Set mapping from predicted gallery ID to app tag ID")
    parser.add_argument("--source-id", help="Predicted gallery cattle ID (example: cattle_0900)")
    parser.add_argument("--target-tag", help="App tag ID (example: CTL-001)")
    parser.add_argument("--show", action="store_true", help="Print current mapping and exit")
    args = parser.parse_args()

    mapping = load_id_mapping()

    if args.show:
        print(mapping)
        return

    if not args.source_id or not args.target_tag:
        raise ValueError("Provide --source-id and --target-tag, or use --show")

    mapping[args.source_id] = args.target_tag
    save_id_mapping(mapping)
    print(f"Mapped {args.source_id} -> {args.target_tag}")


if __name__ == "__main__":
    main()
