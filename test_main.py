"""
Standard test module for Chapter 4 validation.
"""
from main import load_data, train_and_validate

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