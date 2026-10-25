from pathlib import Path
import json
import tempfile

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


ML_FEATURES = [
    "rms",
    "std",
    "peak",
    "crest_factor",
    "kurtosis",
    "dominant_frequency",
    "spectral_energy",
]

HEALTHY_TRAIN_END = pd.Timestamp("2003-11-15")


def train_isolation_forest(
    csv_path,
    n_estimators=200,
    threshold_percentile=5,
):
    features_df = pd.read_csv(
        csv_path,
        parse_dates=["timestamp"],
    )

    X = features_df[ML_FEATURES]

    healthy_mask = (
        features_df["timestamp"] < HEALTHY_TRAIN_END
    )

    X_healthy = X[healthy_mask]

    scaler = StandardScaler()

    X_healthy_scaled = scaler.fit_transform(
        X_healthy
    )

    model = IsolationForest(
        n_estimators=n_estimators,
        contamination="auto",
        random_state=42,
    )

    model.fit(X_healthy_scaled)

    healthy_scores = model.decision_function(
        X_healthy_scaled
    )

    threshold = np.percentile(
        healthy_scores,
        threshold_percentile,
    )

    return model, scaler, threshold


if __name__ == "__main__":
    csv_path = Path(
        "data/processed/ims_set1_bearing4_x_features.csv"
    )

    n_estimators = 200
    threshold_percentile = 5

    mlflow.set_experiment(
        "machineguard-isolation-forest"
    )

    with mlflow.start_run():
        model, scaler, threshold = train_isolation_forest(
            csv_path=csv_path,
            n_estimators=n_estimators,
            threshold_percentile=threshold_percentile,
        )

        features_df = pd.read_csv(
            csv_path,
            parse_dates=["timestamp"],
        )

        healthy_samples = (
            features_df["timestamp"] < HEALTHY_TRAIN_END
        ).sum()

        mlflow.log_param(
            "n_estimators",
            n_estimators,
        )

        mlflow.log_param(
            "threshold_percentile",
            threshold_percentile,
        )

        mlflow.log_param(
            "healthy_train_end",
            str(HEALTHY_TRAIN_END),
        )

        mlflow.log_metric(
            "healthy_threshold",
            threshold,
        )

        mlflow.log_metric(
            "total_samples",
            len(features_df),
        )

        mlflow.log_metric(
            "healthy_training_samples",
            int(healthy_samples),
        )

        mlflow.sklearn.log_model(
            sk_model=model,
            name="isolation_forest",
            skops_trusted_types=[
                "sklearn.tree._tree.Tree",
            ],
        )

        mlflow.sklearn.log_model(
            sk_model=scaler,
            name="scaler",
        )

        threshold_data = {
            "healthy_threshold": float(threshold)
        }

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
        ) as temp_file:
            json.dump(
                threshold_data,
                temp_file,
            )

            threshold_path = temp_file.name

        mlflow.log_artifact(
            threshold_path,
            artifact_path="configuration",
        )

        print(
            "Healthy anomaly threshold:",
            threshold,
        )