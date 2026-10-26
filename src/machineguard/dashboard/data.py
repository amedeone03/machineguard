import pandas as pd

from machineguard.database.connection import get_connection


def load_measurements():
    query = """
        SELECT
            timestamp,
            rms,
            std,
            peak,
            crest_factor,
            kurtosis,
            dominant_frequency,
            spectral_energy,
            anomaly_score,
            anomaly_flag
        FROM measurements
        ORDER BY timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql(query, connection)