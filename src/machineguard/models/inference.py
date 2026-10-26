import json
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd

from machineguard.models.train import ML_FEATURES


EXPERIMENT_NAME = "machineguard-isolation-forest-serving"


def get_latest_run():
    experiment = mlflow.get_experiment_by_name(
        EXPERIMENT_NAME
    )

    if experiment is None:
        raise RuntimeError(
            f"MLflow experiment '{EXPERIMENT_NAME}' not found."
        )

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="attributes.status = 'FINISHED'",
        order_by=["start_time DESC"],
        max_results=1,
    )

    if runs.empty:
        raise RuntimeError(
            "No successful MLflow run found."
        )

    return runs.iloc[0]["run_id"]


def load_threshold(run_id):
    threshold_path = mlflow.artifacts.download_artifacts(
        run_id=run_id,
        artifact_path="configuration",
    )

    configuration_dir = Path(threshold_path)

    json_file = next(
        configuration_dir.glob("*.json")
    )

    with open(json_file, "r") as file:
        configuration = json.load(file)

    return configuration["healthy_threshold"]


def predict_anomaly(
    features,
    model,
    scaler,
    threshold,
):
    feature_df = pd.DataFrame(
        [features],
        columns=ML_FEATURES,
    )

    features_scaled = scaler.transform(
        feature_df
    )

    anomaly_score = model.decision_function(
        features_scaled
    )[0]

    anomaly_flag = anomaly_score < threshold

    return {
        "anomaly_score": float(anomaly_score),
        "anomaly_flag": bool(anomaly_flag),
    }

def load_logged_model(run_id, model_name):
    experiment = mlflow.get_experiment_by_name(
        EXPERIMENT_NAME
    )

    logged_models = mlflow.search_logged_models(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"name = '{model_name}'",
        output_format="list",
    )

    for logged_model in logged_models:
        if logged_model.source_run_id == run_id:
            return mlflow.sklearn.load_model(
                logged_model.model_uri
            )

    raise RuntimeError(
        f"Model '{model_name}' not found for run {run_id}."
    )

def load_inference_pipeline():
    run_id = get_latest_run()

    model = load_logged_model(
        run_id,
        "isolation_forest",
    )

    scaler = load_logged_model(
        run_id,
        "scaler",
    )

    threshold = load_threshold(run_id)

    return model, scaler, threshold