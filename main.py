from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

# Pre-train the model (In the book, you'd usually load a saved .joblib file)
X = np.array([[1500], [2000], [2500], [3000]])
y = np.array([300000, 400000, 500000, 600000])
model = LinearRegression().fit(X, y)

@app.route('/predict', methods=['POST'])
def predict():
    """Accepts JSON like {"sqft": 3500} and returns price."""
    data = request.get_json()
    prediction = model.predict([[data['sqft']]])
    return jsonify({"price": float(prediction[0])})

if __name__ == "__main__":
    # Page 76: Running the server on port 8080
    app.run(host='0.0.0.0', port=8080)