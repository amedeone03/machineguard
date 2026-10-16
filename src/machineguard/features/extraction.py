from pathlib import Path

import pandas as pd

from machineguard.features.time_domain import extract_time_features
from machineguard.features.frequency_domain import (
    compute_dominant_frequency,
    compute_spectral_energy,
)


def extract_snapshot_features(
    file_path,
    channel_index,
    sampling_rate=20_000,
):
    file_path = Path(file_path)

    snapshot = pd.read_csv(
        file_path,
        sep="\t",
        header=None,
    )

    signal = snapshot.iloc[:, channel_index]

    features = extract_time_features(signal)

    features["dominant_frequency"] = compute_dominant_frequency(
        signal,
        sampling_rate,
    )

    features["spectral_energy"] = compute_spectral_energy(signal)

    features["timestamp"] = pd.to_datetime(
        file_path.name,
        format="%Y.%m.%d.%H.%M.%S",
    )

    return features

def extract_dataset_features(directory, channel_index):
    directory = Path(directory)

    files = sorted(directory.iterdir())

    feature_rows = []

    for file_path in files:
        features = extract_snapshot_features(
            file_path,
            channel_index=channel_index,
        )

        feature_rows.append(features)

    return pd.DataFrame(feature_rows)