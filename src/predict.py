
from pathlib import Path
import argparse
import json

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "rf3_pipeline.joblib"
POLICY_PATH = PROJECT_ROOT / "models" / "rf3_policy.json"


def load_artifacts():
    """Load the trusted fitted model and frozen policy."""

    model = joblib.load(MODEL_PATH)

    with POLICY_PATH.open("r", encoding="utf-8") as file:
        policy = json.load(file)

    low = float(policy["lower_threshold"])
    high = float(policy["upper_threshold"])

    if not (0 <= low < high <= 1):
        raise ValueError("Invalid policy thresholds.")

    if policy["features"] != ["amount", "category"]:
        raise ValueError("Unexpected model feature schema.")

    return model, policy


def predict_transactions(transactions, model, policy):
    """
    Score transactions and assign operational actions.

    Required input columns:
        amount: nonnegative, finite numeric value
        category: nonempty string

    Returns a DataFrame with risk scores and actions.
    """

    required = policy["features"]

    if not all(column in transactions.columns for column in required):
        raise ValueError(
            f"Required input columns: {required}"
        )

    X = transactions[required].copy()

    X["amount"] = pd.to_numeric(
        X["amount"], errors="raise"
    )

    if (
        X["amount"].isna().any()
        or not np.isfinite(X["amount"].to_numpy()).all()
        or (X["amount"] < 0).any()
    ):
        raise ValueError(
            "Transaction amounts must be finite and nonnegative."
        )

    if (
        X["category"].isna().any()
        or not X["category"].map(
            lambda value: isinstance(value, str)
            and bool(value.strip())
        ).all()
    ):
        raise ValueError(
            "Transaction categories must be nonempty strings."
        )

    scores = model.predict_proba(X)[:, 1]

    low = float(policy["lower_threshold"])
    high = float(policy["upper_threshold"])

    actions = np.where(
        scores >= high,
        "Escalate",
        np.where(
            scores >= low,
            "Review",
            "Approve"
        )
    )

    result = X.copy()
    result["fraud_risk_score"] = scores
    result["recommended_action"] = actions

    return result


def main():

    parser = argparse.ArgumentParser(
        description="RF-3 transaction fraud-risk inference"
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input CSV containing amount and category."
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output CSV with scores and recommendations."
    )

    args = parser.parse_args()

    model, policy = load_artifacts()

    transactions = pd.read_csv(args.input)

    if transactions.empty:
        raise ValueError("Input CSV contains no transactions.")

    results = predict_transactions(
        transactions, model, policy
    )

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )

    results.to_csv(args.output, index=False)

    print(f"Transactions processed: {len(results):,}")
    print(f"Output saved to: {args.output}")

    print("\nAction counts:")
    print(
        results["recommended_action"]
        .value_counts()
        .reindex(
            ["Approve", "Review", "Escalate"],
            fill_value=0
        )
    )


if __name__ == "__main__":
    main()
