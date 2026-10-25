from pathlib import Path
import time

import pandas as pd

from machineguard.data.ingestion import insert_measurement
from machineguard.features.extraction import extract_snapshot_features


def replay_feature_csv(
    csv_path,
    bearing_id,
    delay_seconds=0.1,
    max_snapshots=None,
):
    features_df = pd.read_csv(
        csv_path,
        parse_dates=["timestamp"],
    )

    features_df = features_df.sort_values("timestamp")

    if max_snapshots is not None:
        features_df = features_df.head(max_snapshots)

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

        print(
            f"Replayed snapshot: {row['timestamp']}"
        )

        time.sleep(delay_seconds)


def replay_raw_snapshots(
    directory,
    bearing_id,
    channel_index,
    delay_seconds=0.1,
    max_snapshots=None,
):
    directory = Path(directory)

    files = sorted(directory.iterdir())

    if max_snapshots is not None:
        files = files[:max_snapshots]

    for file_path in files:
        features = extract_snapshot_features(
            file_path=file_path,
            channel_index=channel_index,
        )

        insert_measurement(
            bearing_id=bearing_id,
            timestamp=features["timestamp"],
            rms=features["rms"],
            std=features["std"],
            peak=features["peak"],
            crest_factor=features["crest_factor"],
            kurtosis=features["kurtosis"],
            dominant_frequency=features["dominant_frequency"],
            spectral_energy=features["spectral_energy"],
        )

        print(
            f"Processed and replayed: {features['timestamp']}"
        )

        time.sleep(delay_seconds)