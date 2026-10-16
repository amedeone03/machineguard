import numpy as np

from machineguard.features.frequency_domain import (
    compute_dominant_frequency,
    compute_spectral_energy,
)


def test_compute_dominant_frequency():
    sampling_rate = 20_000
    duration = 1.0

    time = np.arange(
        0,
        duration,
        1 / sampling_rate,
    )

    signal = np.sin(2 * np.pi * 1000 * time)

    result = compute_dominant_frequency(
        signal,
        sampling_rate,
    )

    assert np.isclose(result, 1000.0)

def test_compute_spectral_energy_zero_signal():
    signal = np.zeros(1000)

    result = compute_spectral_energy(signal)

    assert np.isclose(result, 0.0)