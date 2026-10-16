import numpy as np


def compute_fft(signal, sampling_rate):
    spectrum = np.fft.rfft(signal)
    frequencies = np.fft.rfftfreq(
        len(signal),
        d=1 / sampling_rate,
    )

    amplitudes = np.abs(spectrum)

    return frequencies, amplitudes

def compute_dominant_frequency(signal, sampling_rate):
    signal_centered = signal - np.mean(signal)

    frequencies, amplitudes = compute_fft(
        signal_centered,
        sampling_rate,
    )

    dominant_index = np.argmax(amplitudes[1:]) + 1

    return frequencies[dominant_index]

def compute_spectral_energy(signal):
    signal_centered = signal - np.mean(signal)

    spectrum = np.fft.rfft(signal_centered)

    return np.sum(np.abs(spectrum) ** 2)