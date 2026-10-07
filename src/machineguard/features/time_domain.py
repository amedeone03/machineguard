import numpy as np


def compute_rms(signal):
    return np.sqrt(np.mean(signal**2))

def compute_std(signal):
    return np.std(signal)

def compute_peak(signal):
    return np.max(np.abs(signal))

def compute_crest_factor(signal):
    rms = compute_rms(signal)

    if rms == 0:
        return 0.0

    return compute_peak(signal) / rms