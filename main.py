"""Flask API for predicting house prices from square footage."""

from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)


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


# Pre-train the model (In the book, you'd usually load a saved .joblib file)
model, _ = train_and_validate(load_data())

@app.route('/predict', methods=['POST'])
def predict():
    """Accepts JSON like {"sqft": 3500} and returns price."""
    data = request.get_json()
    prediction = model.predict([[data['sqft']]])
    return jsonify({"price": float(prediction[0])})

if __name__ == "__main__":
    # Page 76: Running the server on port 8080
    app.run(host='0.0.0.0', port=8080)
