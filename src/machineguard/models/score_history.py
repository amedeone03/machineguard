import pandas as pd

from machineguard.database.connection import get_connection
from machineguard.models.inference import (
    load_inference_pipeline,
    predict_anomaly,
)
from machineguard.models.train import ML_FEATURES


def score_historical_measurements():
    model, scaler, threshold = load_inference_pipeline()

    select_query = """
        SELECT
            id,
            rms,
            std,
            peak,
            crest_factor,
            kurtosis,
            dominant_frequency,
            spectral_energy
        FROM measurements
        ORDER BY timestamp;
    """

    with get_connection() as connection:
        measurements = pd.read_sql(
            select_query,
            connection,
        )

        print(
            f"Scoring {len(measurements)} measurements..."
        )

        update_query = """
            UPDATE measurements
            SET
                anomaly_score = %s,
                anomaly_flag = %s
            WHERE id = %s;
        """

        with connection.cursor() as cursor:
            for _, row in measurements.iterrows():
                features = {
                    feature: row[feature]
                    for feature in ML_FEATURES
                }

                prediction = predict_anomaly(
                    features=features,
                    model=model,
                    scaler=scaler,
                    threshold=threshold,
                )

                cursor.execute(
                    update_query,
                    (
                        prediction["anomaly_score"],
                        prediction["anomaly_flag"],
                        int(row["id"]),
                    ),
                )

    print("Historical scoring complete.")


if __name__ == "__main__":
    score_historical_measurements()