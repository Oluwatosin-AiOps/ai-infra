"""Tests for POST /predict."""
from fastapi.testclient import TestClient


def test_predict_returns_probability_and_label(client: TestClient) -> None:
    # Feature vector of 29 values (V1-V28, Amount)
    body = {
        "V1": -1.0, "V2": 0.5, "V3": -0.2, "V4": 0.1, "V5": -0.5,
        "V6": 0.3, "V7": 0.0, "V8": -0.1, "V9": 0.2, "V10": -0.3,
        "V11": 0.1, "V12": 0.0, "V13": -0.2, "V14": 0.1, "V15": 0.0,
        "V16": -0.1, "V17": 0.0, "V18": 0.1, "V19": -0.1, "V20": 0.0,
        "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
        "V26": 0.0, "V27": 0.0, "V28": 0.0, "Amount": 10.0,
    }
    response = client.post("/api/v1/predict", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_probability" in data
    assert "is_fraud" in data
    assert 0 <= data["fraud_probability"] <= 1
    assert isinstance(data["is_fraud"], bool)


def test_predict_rejects_negative_amount(client: TestClient) -> None:
    body = {
        "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": 0.0, "V5": 0.0,
        "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0,
        "V11": 0.0, "V12": 0.0, "V13": 0.0, "V14": 0.0, "V15": 0.0,
        "V16": 0.0, "V17": 0.0, "V18": 0.0, "V19": 0.0, "V20": 0.0,
        "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
        "V26": 0.0, "V27": 0.0, "V28": 0.0, "Amount": -1.0,
    }
    response = client.post("/api/v1/predict", json=body)
    assert response.status_code == 422
