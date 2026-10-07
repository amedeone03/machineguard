import numpy as np

from scipy.stats import kurtosis

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

def compute_kurtosis(signal):
    return kurtosis(signal, fisher=False)


def extract_time_features(signal):
    return {
        "rms": compute_rms(signal),
        "std": compute_std(signal),
        "peak": compute_peak(signal),
        "crest_factor": compute_crest_factor(signal),
        "kurtosis": compute_kurtosis(signal),
    }