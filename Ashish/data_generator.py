#!/usr/bin/env python3
"""
SentinX — Synthetic Transaction Dataset Generator
===================================================
Generates realistic synthetic UPI transaction data for the SentinX
risk-detection system.

The dataset contains two classes:
  • Normal transactions  (~80%)  — low amounts, no suspicious signals
  • Fraudulent/coerced   (~20%)  — high amounts, active calls, foreign
    country codes, screen sharing, high NLP coercion scores

Usage:
    python data_generator.py                # 2000 records (default)
    python data_generator.py --count 5000   # custom count

Author : AI Developer — SentinX SIH 2026
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd

from config import (
    COL_ACTIVE_CALL,
    COL_AMOUNT,
    COL_FOREIGN_CALL,
    COL_FRAUD,
    COL_NLP_SCORE,
    COL_SCREEN_SHARING,
    COL_SIM_CHANGED,
    DATASET_COLUMNS,
    DATASET_NUM_SAMPLES,
    DATASET_OUTPUT_FILE,
    DATASET_RANDOM_SEED,
    FRAUD_AMOUNT_MAX,
    FRAUD_AMOUNT_MIN,
    FRAUD_NLP_MAX,
    FRAUD_NLP_MIN,
    NORMAL_GAMMA_SCALE,
    NORMAL_GAMMA_SHAPE,
    NORMAL_NLP_MAX,
    NORMAL_NLP_MIN,
    NORMAL_RATIO,
)


# ──────────────────────────────────────────────────────────────
#  Core generator
# ──────────────────────────────────────────────────────────────

def generate_sentinx_dataset(
    num_samples: int = DATASET_NUM_SAMPLES,
    output_file: str = DATASET_OUTPUT_FILE,
    random_seed: int = DATASET_RANDOM_SEED,
) -> pd.DataFrame:
    """Generate a synthetic transaction dataset and save it as CSV.

    Parameters
    ----------
    num_samples : int
        Total number of records to generate.
    output_file : str
        Path for the output CSV file.
    random_seed : int
        Seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        The generated dataset.
    """
    if num_samples is None:
        raise ValueError("num_samples cannot be None")

    try:
        num_samples = int(num_samples)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"num_samples must be a valid integer, got {num_samples!r}") from exc

    if num_samples <= 0:
        raise ValueError(f"num_samples must be a positive integer (> 0), got {num_samples}")

    np.random.seed(random_seed)

    n_normal = int(num_samples * NORMAL_RATIO)
    n_fraud = num_samples - n_normal

    # ── Normal transactions ──────────────────────────────────
    normal_amounts = (
        np.random.gamma(
            shape=NORMAL_GAMMA_SHAPE, scale=NORMAL_GAMMA_SCALE, size=n_normal
        )
        if n_normal > 0
        else np.array([], dtype=float)
    )
    normal_calls = np.zeros(n_normal, dtype=int)
    normal_foreign = np.zeros(n_normal, dtype=int)
    normal_screen = np.zeros(n_normal, dtype=int)
    normal_sim = np.zeros(n_normal, dtype=int)
    normal_nlp = (
        np.random.uniform(NORMAL_NLP_MIN, NORMAL_NLP_MAX, size=n_normal)
        if n_normal > 0
        else np.array([], dtype=float)
    )
    normal_labels = np.zeros(n_normal, dtype=int)

    # ── Fraud / coerced transactions ─────────────────────────
    fraud_amounts = (
        np.random.uniform(FRAUD_AMOUNT_MIN, FRAUD_AMOUNT_MAX, size=n_fraud)
        if n_fraud > 0
        else np.array([], dtype=float)
    )
    fraud_calls = (
        np.random.choice([0, 1], size=n_fraud, p=[0.1, 0.9])
        if n_fraud > 0
        else np.array([], dtype=int)
    )
    fraud_foreign = (
        np.where(
            fraud_calls == 1,
            np.random.choice([0, 1], size=n_fraud, p=[0.3, 0.7]),
            0,
        )
        if n_fraud > 0
        else np.array([], dtype=int)
    )
    fraud_screen = (
        np.random.choice([0, 1], size=n_fraud, p=[0.2, 0.8])
        if n_fraud > 0
        else np.array([], dtype=int)
    )
    fraud_sim = (
        np.random.choice([0, 1], size=n_fraud, p=[0.7, 0.3])
        if n_fraud > 0
        else np.array([], dtype=int)
    )
    fraud_nlp = (
        np.random.uniform(FRAUD_NLP_MIN, FRAUD_NLP_MAX, size=n_fraud)
        if n_fraud > 0
        else np.array([], dtype=float)
    )
    fraud_labels = np.ones(n_fraud, dtype=int)

    # ── Combine & shuffle ────────────────────────────────────
    df = pd.DataFrame(
        {
            COL_AMOUNT: np.round(
                np.concatenate([normal_amounts, fraud_amounts]), 2
            ),
            COL_ACTIVE_CALL: np.concatenate([normal_calls, fraud_calls]),
            COL_FOREIGN_CALL: np.concatenate([normal_foreign, fraud_foreign]),
            COL_SCREEN_SHARING: np.concatenate([normal_screen, fraud_screen]),
            COL_SIM_CHANGED: np.concatenate([normal_sim, fraud_sim]),
            COL_NLP_SCORE: np.round(
                np.concatenate([normal_nlp, fraud_nlp]), 2
            ),
            COL_FRAUD: np.concatenate([normal_labels, fraud_labels]),
        }
    )

    df = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    df.to_csv(output_file, index=False)

    return df


# ──────────────────────────────────────────────────────────────
#  Validation
# ──────────────────────────────────────────────────────────────

def validate_dataset(df: pd.DataFrame, expected_count: int) -> bool:
    """Run sanity checks on the generated dataset.

    Returns True if all checks pass, False otherwise.
    """
    errors: list[str] = []

    # Record count
    if len(df) != expected_count:
        errors.append(
            f"Record count mismatch: expected {expected_count}, got {len(df)}"
        )

    # Required columns
    missing = set(DATASET_COLUMNS) - set(df.columns)
    if missing:
        errors.append(f"Missing columns: {missing}")

    # No unexpected NaN values
    nan_counts = df.isna().sum()
    if nan_counts.any():
        cols_with_nan = nan_counts[nan_counts > 0].to_dict()
        errors.append(f"NaN values found: {cols_with_nan}")

    # Amount validity
    if (df[COL_AMOUNT] < 0).any():
        errors.append("Negative amounts detected")

    # Binary columns must be 0 or 1
    binary_cols = [
        COL_ACTIVE_CALL,
        COL_FOREIGN_CALL,
        COL_SCREEN_SHARING,
        COL_SIM_CHANGED,
        COL_FRAUD,
    ]
    for col in binary_cols:
        unique_vals = set(df[col].unique())
        if not unique_vals.issubset({0, 1}):
            errors.append(f"Column '{col}' has invalid values: {unique_vals}")

    # NLP coercion score in [0, 1]
    if (df[COL_NLP_SCORE] < 0).any() or (df[COL_NLP_SCORE] > 1).any():
        errors.append("NLP coercion scores outside [0, 1] range")

    # Fraud distribution check (~20%) — applicable for standard dataset sizes (>= 20)
    if expected_count >= 20:
        fraud_ratio = df[COL_FRAUD].mean()
        if not (0.15 <= fraud_ratio <= 0.25):
            errors.append(
                f"Fraud ratio {fraud_ratio:.2%} is outside expected 15-25% range"
            )

    if errors:
        print("\nDataset validation: FAILED")
        for err in errors:
            print(f"  ✗ {err}")
        return False

    print("\nDataset validation: PASSED")
    return True


# ──────────────────────────────────────────────────────────────
#  CLI entry point
# ──────────────────────────────────────────────────────────────

def main() -> None:
    """Parse arguments, generate dataset, validate, and print summary."""
    parser = argparse.ArgumentParser(
        description="SentinX Synthetic Transaction Dataset Generator"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DATASET_NUM_SAMPLES,
        help=f"Number of records to generate (default: {DATASET_NUM_SAMPLES})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DATASET_OUTPUT_FILE,
        help=f"Output CSV path (default: {DATASET_OUTPUT_FILE})",
    )
    args = parser.parse_args()

    print("SentinX Synthetic Dataset Generator")
    print("-" * 38)

    df = generate_sentinx_dataset(
        num_samples=args.count,
        output_file=args.output,
    )

    n_normal = int((df[COL_FRAUD] == 0).sum())
    n_fraud = int((df[COL_FRAUD] == 1).sum())
    fraud_pct = (n_fraud / len(df)) * 100

    print(f"Total records : {len(df)}")
    print(f"Normal records: {n_normal}")
    print(f"Fraud records : {n_fraud}")
    print(f"Fraud ratio   : {fraud_pct:.2f}%")

    passed = validate_dataset(df, expected_count=args.count)
    print(f"\nSaved to: {args.output}")

    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
