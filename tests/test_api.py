from fastapi.testclient import TestClient

from machineguard.api.main import app

from unittest.mock import patch

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "machineguard",
    }

def test_predict_healthy():
    payload = {
        "rms": 0.10902049,
        "std": 0.06008455,
        "peak": 0.413,
        "crest_factor": 3.7882787,
        "kurtosis": 3.7902499,
        "dominant_frequency": 986.328125,
        "spectral_energy": 757118.612018,
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    result = response.json()

    assert result["anomaly_flag"] is False
    assert result["status"] == "NORMAL"
    assert "anomaly_score" in result

def test_predict_rejects_negative_rms():
    payload = {
        "rms": -1,
        "std": 0.1,
        "peak": 1.0,
        "crest_factor": 2.0,
        "kurtosis": 3.0,
        "dominant_frequency": 1000,
        "spectral_energy": 100000,
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 422

def test_predict_returns_404_when_measurement_not_found():
    payload = {
        "bearing_id": 1,
        "timestamp": "2099-01-01T00:00:00",
        "rms": 0.10902049,
        "std": 0.06008455,
        "peak": 0.413,
        "crest_factor": 3.7882787,
        "kurtosis": 3.7902499,
        "dominant_frequency": 986.328125,
        "spectral_energy": 757118.612018,
    }

    with patch(
        "machineguard.api.main.update_measurement_prediction",
        return_value=0,
    ):
        response = client.post(
            "/predict",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Measurement not found."
    }