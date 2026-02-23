#!/usr/bin/env python3
"""
Train a lightweight fraud detection model (RandomForest) on the Credit Card Fraud dataset.
Expects data/creditcard.csv (Kaggle) or generates synthetic data for testing.

Usage:
  From backend/: uv run python scripts/train_model.py
  With custom data: uv run python scripts/train_model.py --data path/to/creditcard.csv
  Output: app/model/model.joblib
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# Credit Card Fraud dataset schema (Kaggle: mlg-ulb/creditcardfraud)
FEATURE_COLUMNS = [f"V{i}" for i in range(1, 29)] + ["Amount"]  # optional: "Time"
TARGET = "Class"


def load_data(csv_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(csv_path)
    if TARGET not in df.columns:
        raise ValueError(f"CSV must contain column '{TARGET}'")
    for c in FEATURE_COLUMNS:
        if c not in df.columns:
            raise ValueError(f"CSV must contain feature column '{c}'")
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET]
    return X, y


def make_synthetic_data(n_samples: int = 5_000, seed: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    """Generate minimal synthetic data with same schema for testing when CSV is missing."""
    import numpy as np

    rng = np.random.default_rng(seed)
    X = pd.DataFrame(
        rng.standard_normal((n_samples, len(FEATURE_COLUMNS))),
        columns=FEATURE_COLUMNS,
    )
    X["Amount"] = np.clip(rng.exponential(100, size=n_samples), 0, 25_000)
    # ~0.17% fraud (similar to real dataset)
    y = (rng.random(n_samples) < 0.0017).astype(int)
    return X, pd.Series(y, name=TARGET)


def main() -> int:
    parser = argparse.ArgumentParser(description="Train fraud detection model")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/creditcard.csv"),
        help="Path to creditcard.csv (default: data/creditcard.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("app/model/model.joblib"),
        help="Output path for joblib model (default: app/model/model.joblib)",
    )
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data only")
    parser.add_argument("--n-samples", type=int, default=5000, help="Synthetic sample size (default 5000)")
    args = parser.parse_args()

    if args.synthetic or not args.data.exists():
        if not args.synthetic:
            print(f"Data not found at {args.data}; using synthetic data.", file=sys.stderr)
        X, y = make_synthetic_data(n_samples=args.n_samples)
    else:
        X, y = load_data(args.data)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Model accuracy (test): {score:.4f}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.output)
    print(f"Saved model to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
