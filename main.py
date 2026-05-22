"""Flask API for predicting house prices from square footage."""

import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join("models", "model.joblib"))


def load_data():
    """Load the square footage and price training data."""
    return {
        "sqft": np.array([[1500], [2000], [2500], [3000]]),
        "price": np.array([300000, 400000, 500000, 600000]),
    }


def train_and_validate(data):
    """Train a linear regression model and return its accuracy."""
    trained_model = LinearRegression().fit(data["sqft"], data["price"])
    accuracy = trained_model.score(data["sqft"], data["price"])
    return trained_model, accuracy


def load_model():
    """Load model from joblib if exists, else train in-memory (fallback)."""
    if os.path.exists(MODEL_PATH):
        print(f"Loading model from {MODEL_PATH}")
        return joblib.load(MODEL_PATH)
    print("No saved model found, training in-memory (fallback).")
    trained, _ = train_and_validate(load_data())
    return trained


model = load_model()


@app.route("/", methods=["GET"])
def index():
    """Return a basic service status for browser and Cloud Run checks."""
    return jsonify(
        {
            "service": "mlops-house-prices",
            "status": "ok",
            "prediction_endpoint": "/predict",
        }
    )


@app.route("/health", methods=["GET"])
def health():
    """Return a lightweight health response."""
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    """Accepts JSON like {"sqft": 3500} and returns price."""
    data = request.get_json()
    prediction = model.predict([[data["sqft"]]])
    return jsonify({"price": float(prediction[0])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
