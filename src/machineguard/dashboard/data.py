import pandas as pd

from machineguard.dashboard.api_client import API_BASE_URL

import httpx


def load_measurements():
    response = httpx.get(
        f"{API_BASE_URL}/measurements",
        timeout=30.0,
    )

    response.raise_for_status()

    measurements = response.json()

    dataframe = pd.DataFrame(measurements)

    if not dataframe.empty:
        dataframe["timestamp"] = pd.to_datetime(
            dataframe["timestamp"]
        )

    return dataframe