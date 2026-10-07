import numpy as np


def compute_rms(signal):
    return np.sqrt(np.mean(signal**2))