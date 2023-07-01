import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../')
from utils.signal_processing import *
import pyemgpipeline as pep
from scipy.signal import butter, iirnotch, firwin, filtfilt, periodogram

def classify_motion(chunk, rest_peaks, threshold=8):
    proc_chunk = process_chunk(chunk)
    chunk_peaks = find_peaks(proc_chunk)
    amp_factor = compute_amp_factor(chunk_peaks, rest_peaks)
    return (amp_factor > threshold)
    
def compute_amp_factor(sample_peaks, rest_peaks):
    amp_factors = []
    for i in range(len(sample_peaks)):
        amp_factor = sample_peaks[i]/rest_peaks[i]
        amp_factors.append(amp_factor)
    return np.mean(amp_factors)

def find_peaks(chunk):
    peaks = []
    for i in range(chunk.shape[1]):
        peak = np.max(chunk[:,i])
        peaks.append(peak)
    return np.array(peaks)

def process_chunk(chunk):
    chunk = np.array(chunk)
    proc_chunk = np.zeros((chunk.shape[0],4))
    for i in np.arange(0,8,2):
        lap = tripolar_laplacian(chunk[:,i+1],chunk[:,i])
        proc_lap = process_signal(lap,low=5,high=124,Q=30)
        proc_chunk[:,int(i/2)] = proc_lap
    return proc_chunk

def process_signal(signal, low, high, Q):
    signal = np.array(signal)
    if not Q==0:
        signal = butter_notch(signal,Q)
    emg = pep.wrappers.EMGMeasurement(signal, hz=250)
    emg.apply_dc_offset_remover()
    emg.apply_bandpass_filter(2,low,high)
    #emg.apply_amplitude_normalizer(100)
    emg.apply_full_wave_rectifier()
    #emg.apply_end_frame_cutter(n_end_frames=50)
    return emg.data

def butter_notch(chan_data, Q, Fs=250, notch_freq=60.0):
    # Define the filter parameters
    #Q = 30.0

    # Calculate the notch filter coefficients
    w0 = notch_freq / (Fs / 2)
    b, a = iirnotch(w0, Q)

    # Apply the filter to the EEG data
    notched_data = filtfilt(b, a, chan_data)
    return notched_data
        