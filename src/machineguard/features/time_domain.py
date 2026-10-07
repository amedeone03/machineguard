import numpy as np


def compute_rms(signal):
    return np.sqrt(np.mean(signal**2))

def compute_std(signal):
    return np.std(signal)

def compute_peak(signal):
    return np.max(np.abs(signal))