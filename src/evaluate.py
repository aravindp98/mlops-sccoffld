"""
evaluate.py — Saved model load panni test data-la evaluate pannudu, metrics save pannudu.
DVC Stage 3: evaluate
"""
import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

TEST_PATH = os.path.join("data", "processed", "test.csv")
MODEL_PATH = os.path.join("models", "model.joblib")
METRICS_PATH = os.path.join("metrics", "scores.json")


def evaluate(model_path: str = MODEL_PATH, test_path: str = TEST_PATH) -> dict:
    model = joblib.load(model_path)
    df = pd.read_csv(test_path)
    X = df[["sqft"]].values
    y = df["price"].values

    predictions = model.predict(X)
    r2 = model.score(X, y)
    rmse = float(np.sqrt(mean_squared_error(y, predictions)))
    mae = float(mean_absolute_error(y, predictions))

    metrics = {"r2_score": round(r2, 4), "rmse": round(rmse, 2), "mae": round(mae, 2)}
    print(f"Metrics: {metrics}")
    return metrics


def save_metrics(metrics: dict, path: str = METRICS_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {path}")


if __name__ == "__main__":
    metrics = evaluate()
    save_metrics(metrics)
    print("Evaluation done.")
