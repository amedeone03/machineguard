import os

import httpx


API_BASE_URL = os.getenv(
    "MACHINEGUARD_API_URL",
    "http://machineguard-api-alb-352184873.eu-north-1.elb.amazonaws.com",
)


def check_api_health():
    response = httpx.get(
        f"{API_BASE_URL}/health",
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()


def predict_anomaly(features):
    response = httpx.post(
        f"{API_BASE_URL}/predict",
        json=features,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()