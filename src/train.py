"""
train.py — Processed data load panni model train pannudu, joblib save pannudu.
DVC Stage 2: train
MLflow tracking added — every run automatically logged.
"""
import json
import os
import joblib
import numpy as np
import pandas as pd
import yaml
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression

TRAIN_PATH = os.path.join("data", "processed", "train.csv")
MODEL_PATH = os.path.join("models", "model.joblib")
PARAMS_PATH = "params.yaml"
METRICS_PATH = os.path.join("metrics", "scores.json")

MLFLOW_ARTIFACT_URI = os.environ.get(
    "MLFLOW_ARTIFACT_URI",
    "gs://devmlops-496015-mlops-artifacts/mlflow"
)
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")


def load_params() -> dict:
    if os.path.exists(PARAMS_PATH):
        with open(PARAMS_PATH) as f:
            return yaml.safe_load(f)
    return {}


def train(train_path: str = TRAIN_PATH) -> LinearRegression:
    df = pd.read_csv(train_path)
    X = df[["sqft"]].values
    y = df["price"].values
    model = LinearRegression()
    model.fit(X, y)
    print(f"Model trained. Coef: {model.coef_[0]:.2f}, Intercept: {model.intercept_:.2f}")
    return model, X, y


def save_model(model: LinearRegression, path: str = MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    params = load_params()
    prepare_params = params.get("prepare", {})
    train_params = params.get("train", {})

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Experiment already iruka check pannuvom, illana GCS artifact location-a set panni create pannuvom
    from mlflow.tracking import MlflowClient
    client = MlflowClient()
    experiment = client.get_experiment_by_name("house-price-prediction")
    if experiment is None:
        client.create_experiment(
            name="house-price-prediction",
            artifact_location=MLFLOW_ARTIFACT_URI,
        )
    mlflow.set_experiment("house-price-prediction")

    with mlflow.start_run(run_name="linear_regression"):

        # Log params
        mlflow.log_param("model_type", train_params.get("model_type", "linear_regression"))
        mlflow.log_param("test_size", prepare_params.get("test_size", 0.2))
        mlflow.log_param("random_state", train_params.get("random_state", 42))
        mlflow.log_param("train_data", TRAIN_PATH)

        # Train
        model, X, y = train()

        # Log model-level params
        mlflow.log_param("coef", round(float(model.coef_[0]), 4))
        mlflow.log_param("intercept", round(float(model.intercept_), 4))

        # Evaluate on train set
        r2 = model.score(X, y)
        from sklearn.metrics import mean_squared_error, mean_absolute_error
        preds = model.predict(X)
        rmse = float(np.sqrt(mean_squared_error(y, preds)))
        mae = float(mean_absolute_error(y, preds))

        # Log metrics
        mlflow.log_metric("r2_score", round(r2, 4))
        mlflow.log_metric("rmse", round(rmse, 2))
        mlflow.log_metric("mae", round(mae, 2))

        # Log model artifact + register to Model Registry
        model_info = mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="house-price-model",  # Registry-la auto register
        )

        # Log params.yaml as artifact
        mlflow.log_artifact(PARAMS_PATH)

        print(f"MLflow run logged — r2: {r2:.4f}, rmse: {rmse:.2f}, mae: {mae:.2f}")
        print(f"Model registered: {model_info.model_uri}")

        # Save joblib for DVC + serving
        save_model(model)

    print("Training done.")
