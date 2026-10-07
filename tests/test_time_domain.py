import numpy as np

from machineguard.features.time_domain import compute_rms, compute_std, compute_peak

def test_compute_rms():
    signal = np.array([0.2, -0.2, 0.2, -0.2])

    result = compute_rms(signal)

    assert np.isclose(result, 0.2)

def test_compute_std():
    signal = np.array([1.0, 2.0, 3.0])

    result = compute_std(signal)

    assert np.isclose(result, np.std(signal))

def test_compute_peak():
    signal = np.array([-0.2, 0.1, -0.8, 0.4])

    result = compute_peak(signal)

    assert np.isclose(result, 0.8)