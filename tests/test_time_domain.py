import numpy as np

from machineguard.features.time_domain import (
    compute_rms,
    compute_std,
    compute_peak,
    compute_crest_factor,
    compute_kurtosis,
    extract_time_features
)

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

def test_compute_crest_factor():
    signal = np.array([1.0, -1.0, 1.0, -1.0])

    result = compute_crest_factor(signal)

    assert np.isclose(result, 1.0)

def test_compute_crest_factor_zero_signal():
    signal = np.array([0.0, 0.0, 0.0])

    result = compute_crest_factor(signal)

    assert result == 0.0

def test_compute_kurtosis():
    signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

    result = compute_kurtosis(signal)

    expected = 1.7

    assert np.isclose(result, expected)

def test_extract_time_features():
    signal = np.array([1.0, -1.0, 1.0, -1.0])

    features = extract_time_features(signal)

    assert set(features.keys()) == {
        "rms",
        "std",
        "peak",
        "crest_factor",
        "kurtosis",
    }

    assert np.isclose(features["rms"], compute_rms(signal))
    assert np.isclose(features["std"], compute_std(signal))
    assert np.isclose(features["peak"], compute_peak(signal))
    assert np.isclose(
        features["crest_factor"],
        compute_crest_factor(signal),
    )
    assert np.isclose(
        features["kurtosis"],
        compute_kurtosis(signal),
    )
