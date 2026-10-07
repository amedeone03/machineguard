import numpy as np

from machineguard.features.time_domain import compute_rms


def test_compute_rms():
    signal = np.array([0.2, -0.2, 0.2, -0.2])

    result = compute_rms(signal)

    assert np.isclose(result, 0.2)