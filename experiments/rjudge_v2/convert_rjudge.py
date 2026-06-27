"""
convert_rjudge.py
=================
Download and convert the R-Judge dataset (EMNLP Findings 2024) into a
standardized JSONL format that the rest of the rjudge_v2 pipeline can consume.

R-Judge source: https://github.com/Lordog/R-Judge

Each converted record contains:
  - id: original record id
  - scenario: application scenario
  - profile: user profile
  - goal: user goal
  - contents: list of turns (each turn = list of messages)
  - label: 0 (safe) or 1 (unsafe)
  - risk_description: human-written risk explanation
  - attack_type: "injection" or "unintended"

Usage:
    python experiments/rjudge_v2/convert_rjudge.py [--data-dir DIR] [--output PATH]

If --data-dir is not specified, this script will attempt to clone the
R-Judge repository into <project_root>/rjudge_data/ automatically.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Dict, List

RJUDGE_REPO = "https://github.com/Lordog/R-Judge.git"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DATA_DIR = os.path.join(PROJECT_ROOT, "rjudge_data")
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "results", "rjudge_v2", "rjudge_converted.jsonl")


def ensure_data(data_dir: str) -> str:
    """Clone R-Judge repo if data directory does not exist."""
    if os.path.isdir(data_dir):
        return data_dir
    print(f"R-Judge data not found at {data_dir}. Cloning from GitHub...")
    subprocess.check_call(["git", "clone", "--depth", "1", RJUDGE_REPO, data_dir])
    print(f"Cloned to {data_dir}")
    return data_dir


def load_rjudge_records(data_dir: str) -> List[Dict]:
    """Load all R-Judge JSON files from the data directory."""
    import glob
    records = []
    search_pattern = os.path.join(data_dir, "**", "*.json")
    for f in sorted(glob.glob(search_pattern, recursive=True)):
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                records.extend(data)
            elif isinstance(data, dict):
                records.append(data)
    return records


def convert_records(records: List[Dict]) -> List[Dict]:
    """Normalize records to a consistent format."""
    converted = []
    for r in records:
        rec = {
            "id": r.get("id", ""),
            "scenario": r.get("scenario", ""),
            "profile": r.get("profile", ""),
            "goal": r.get("goal", ""),
            "contents": r.get("contents", []),
            "label": r.get("label", -1),
            "risk_description": r.get("risk_description", ""),
            "attack_type": r.get("attack_type", ""),
        }
        converted.append(rec)
    return converted


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert R-Judge dataset")
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR,
                        help="Directory containing R-Judge data")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Output JSONL path")
    args = parser.parse_args()

    data_dir = ensure_data(args.data_dir)
    records = load_rjudge_records(data_dir)
    print(f"Loaded {len(records)} records from {data_dir}")

    converted = convert_records(records)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for rec in converted:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Print label distribution
    from collections import Counter
    labels = Counter(r["label"] for r in converted)
    attacks = Counter(r["attack_type"] for r in converted)
    print(f"Label distribution: {dict(labels)}")
    print(f"Attack type distribution: {dict(attacks)}")
    print(f"Saved {len(converted)} records to {args.output}")


if __name__ == "__main__":
    main()
