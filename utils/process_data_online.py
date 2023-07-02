import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../')
from utils.signal_processing import *
import pyemgpipeline as pep
from scipy.signal import butter, iirnotch, firwin, filtfilt, periodogram

def classify_motion(chunk, rest_peaks, threshold=8):
    """
    Classifies motion based on the amplitude factor of the chunk compared to the rest peaks.

    Parameters:
    - chunk: Chunk of data for motion analysis.
    - rest_peaks: Peaks from the rest period used for amplitude factor calculation.
    - threshold: Threshold value for motion classification. Default is 8.

    Returns:
    - motion_detected: Boolean indicating whether motion is detected (True) or not (False).
    """
    proc_chunk = process_chunk(chunk)
    chunk_peaks = find_peaks(proc_chunk)
    amp_factor = compute_amp_factor(chunk_peaks, rest_peaks)

    return (amp_factor > threshold)


def compute_amp_factor(sample_peaks, rest_peaks):
    """
    Computes the amplitude factor between sample peaks and rest peaks.

    Parameters:
    - sample_peaks: Peaks from the sample period.
    - rest_peaks: Peaks from the rest period.

    Returns:
    - amp_factor: Mean amplitude factor between sample peaks and rest peaks.
    """
    amp_factors = []
    for i in range(len(sample_peaks)):
        amp_factor = sample_peaks[i] / rest_peaks[i]
        amp_factors.append(amp_factor)

    return np.mean(amp_factors)


def find_peaks(chunk):
    """
    Finds the maximum peaks for each channel in the chunk.

    Parameters:
    - chunk: Chunk of data.

    Returns:
    - peaks: Array of maximum peaks for each channel in the chunk.
    """
    peaks = []
    for i in range(chunk.shape[1]):
        peak = np.max(chunk[:, i])
        peaks.append(peak)

    return np.array(peaks)


def process_chunk(chunk):
    """
    Processes the chunk of data by applying tripolar laplacian, filtering, and rectification.

    Parameters:
    - chunk: Chunk of data.

    Returns:
    - proc_chunk: Processed chunk of data after tripolar laplacian, filtering, and rectification.
    """
    chunk = np.array(chunk)
    proc_chunk = np.zeros((chunk.shape[0], 4))
    for i in np.arange(0, 8, 2):
        lap = tripolar_laplacian(chunk[:, i + 1], chunk[:, i])
        proc_lap = process_signal(lap, low=5, high=124, Q=30)
        proc_chunk[:, int(i / 2)] = proc_lap

    return proc_chunk


def process_signal(signal, low, high, Q):
    """
    Processes the EMG signal by applying notch filter, DC offset removal, bandpass filter, and rectification.

    Parameters:
    - signal: EMG signal as a NumPy array or list of numeric values.
    - low: Lower cutoff frequency for bandpass filter.
    - high: Upper cutoff frequency for bandpass filter.
    - Q: Q factor for notch filter.

    Returns:
    - processed_signal: Processed EMG signal after applying notch filter, DC offset removal, bandpass filter, and rectification.
    """
    signal = np.array(signal)

    if not Q == 0:
        signal = butter_notch(signal, Q)

    emg = pep.wrappers.EMGMeasurement(signal, hz=250)
    emg.apply_dc_offset_remover()
    emg.apply_bandpass_filter(2, low, high)
    emg.apply_full_wave_rectifier()

    return emg.data


def butter_notch(chan_data, Q, Fs=250, notch_freq=60.0):
    """
    Applies a notch filter to remove noise at a specific frequency.

    Parameters:
    - chan_data: EMG data as a NumPy array or list of numeric values.
    - Q: Q factor for the notch filter.
    - Fs: Sampling frequency. Default is 250 Hz.
    - notch_freq: Notch frequency to remove. Default is 60.0 Hz.

    Returns:
    - notched_data: Notched data after applying the filter.
    """
    w0 = notch_freq / (Fs / 2)
    b, a = iirnotch(w0, Q)
    notched_data = filtfilt(b, a, chan_data)

    return notched_data

        