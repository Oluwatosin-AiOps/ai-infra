#!/usr/bin/env python3
"""
Download the Credit Card Fraud dataset from Kaggle.
Requires: pip install kaggle, and Kaggle API credentials in ~/.kaggle/kaggle.json
Dataset: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Usage:
  From backend/: uv run python scripts/download_data.py
  Output: data/creditcard.csv
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    out_csv = data_dir / "creditcard.csv"

    try:
        subprocess.run(
            [
                "kaggle",
                "datasets",
                "download",
                "-d",
                "mlg-ulb/creditcardfraud",
                "-p",
                str(data_dir),
                "--unzip",
            ],
            check=True,
        )
    except FileNotFoundError:
        print(
            "Kaggle CLI not found. Install with: pip install kaggle\n"
            "Then add your API key from https://www.kaggle.com/settings to ~/.kaggle/kaggle.json",
            file=sys.stderr,
        )
        return 1
    except subprocess.CalledProcessError as e:
        print(f"Kaggle download failed: {e}", file=sys.stderr)
        return 1

    # Dataset unzips as creditcard.csv into data_dir
    if not out_csv.exists():
        print(f"Expected {out_csv} after unzip; not found.", file=sys.stderr)
        return 1
    print(f"Downloaded {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
