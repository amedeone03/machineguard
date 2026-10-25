from machineguard.database.connection import get_connection


def insert_measurement(
    bearing_id,
    timestamp,
    rms,
    std,
    peak,
    crest_factor,
    kurtosis,
    dominant_frequency,
    spectral_energy,
    anomaly_score=None,
    anomaly_flag=None,
):
    query = """
        INSERT INTO measurements (
            bearing_id,
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
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (bearing_id, timestamp)
        DO NOTHING;
    """

    values = (
        bearing_id,
        timestamp,
        rms,
        std,
        peak,
        crest_factor,
        kurtosis,
        dominant_frequency,
        spectral_energy,
        anomaly_score,
        anomaly_flag,
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

import pandas as pd


def ingest_feature_csv(
    csv_path,
    bearing_id,
):
    features_df = pd.read_csv(
        csv_path,
        parse_dates=["timestamp"],
    )

    for _, row in features_df.iterrows():
        insert_measurement(
            bearing_id=bearing_id,
            timestamp=row["timestamp"],
            rms=row["rms"],
            std=row["std"],
            peak=row["peak"],
            crest_factor=row["crest_factor"],
            kurtosis=row["kurtosis"],
            dominant_frequency=row["dominant_frequency"],
            spectral_energy=row["spectral_energy"],
        )