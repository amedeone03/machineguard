import numpy as np
import pandas as pd

from machineguard.features.extraction import extract_snapshot_features


def test_extract_snapshot_features(tmp_path):
    signal_data = np.array([
        [1.0, 10.0],
        [-1.0, 20.0],
        [1.0, 30.0],
        [-1.0, 40.0],
    ])

    file_path = tmp_path / "2003.10.22.12.06.24"

    np.savetxt(
        file_path,
        signal_data,
        delimiter="\t",
    )

    features = extract_snapshot_features(
        file_path,
        channel_index=0,
    )

    assert np.isclose(features["rms"], 1.0)
    assert np.isclose(features["std"], 1.0)
    assert np.isclose(features["peak"], 1.0)
    assert np.isclose(features["crest_factor"], 1.0)

    assert features["timestamp"] == pd.Timestamp(
        "2003-10-22 12:06:24"
    )