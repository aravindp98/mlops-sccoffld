"""
Standard test module for Chapter 4 validation.
"""
import pytest

from main import app, load_data, train_and_validate


def test_data_loading():
    """Verify that data loads with the correct keys."""
    data = load_data()
    assert "sqft" in data
    assert "price" in data


def test_model_accuracy():
    """Verify that the model logic is still perfect."""
    data = load_data()
    _, accuracy = train_and_validate(data)
    # Our data is perfectly linear, so accuracy should be 1.0
    assert accuracy == 1.0


def test_index_endpoint():
    """Verify that the root endpoint returns service status."""
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_predict_endpoint():
    """Verify that the prediction endpoint returns a price."""
    response = app.test_client().post("/predict", json={"sqft": 3500})
    assert response.status_code == 200
    assert response.get_json()["price"] == pytest.approx(700000.0)
