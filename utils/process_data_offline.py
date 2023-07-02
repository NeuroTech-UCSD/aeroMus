import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../')
from utils.signal_processing import *
import pyemgpipeline as pep
from scipy.signal import butter, iirnotch, firwin, filtfilt, periodogram

def data_from_files(data, metadata, electrodes=[[3,2],[7,6]]):
    """
    Loads data from files and extracts instances for different categories and electrodes.

    Parameters:
    - data: File path of the data file (CSV format).
    - metadata: File path of the metadata file (CSV format).
    - electrodes: List of electrode pairs for tripolar laplacian calculation. Default is [[3,2],[7,6]].

    Returns:
    - category_instances: Dictionary containing instances for different categories and electrodes.
    """
    sess_data = pd.read_csv(data, header=None)
    sess_metadata = pd.read_csv(metadata, names=['start_time', 'category'])
    category_instances = {}

    for i, row in sess_metadata.iterrows():
        start_time = row['start_time']
        category = row['category'].strip()
        end_time = sess_metadata.iloc[i + 1]['start_time'] if i < (len(sess_metadata) - 1) else sess_data.iloc[-1][0]

        all_electrodes = []
        for electrode in electrodes:
            all_electrodes += electrode

        channels = sess_data.loc[(sess_data[0] >= start_time) & (sess_data[0] < end_time)].iloc[:, all_electrodes]

        instances = pd.DataFrame()
        for i, pair in enumerate(electrodes):
            instances[f'e{i+1}'] = tripolar_laplacian(channels[pair[0]], pair[1])

        if category not in category_instances:
            category_instances[category] = []
        category_instances[category].append(instances)

    return category_instances


def plot_emg(cat_dict, category, instance, electrode, low=5, high=124, Q=30, num_frames=50, plot=True):
    """
    Processes and plots the EMG signal for a specific category, instance, and electrode.

    Parameters:
    - cat_dict: Dictionary containing instances for different categories and electrodes.
    - category: Category of the signal.
    - instance: Instance number within the category.
    - electrode: Electrode number.
    - low: Lower cutoff frequency for bandpass filter. Default is 5 Hz.
    - high: Upper cutoff frequency for bandpass filter. Default is 124 Hz.
    - Q: Q factor for notch filter. Default is 30.
    - num_frames: Number of frames to keep after end frame cutting. Default is 50.
    - plot: Flag indicating whether to plot the EMG signal. Default is True.

    Returns:
    - emg: Processed EMG signal.
    """
    signal = cat_dict[category][instance][electrode]
    emg = process_signal(signal, low, high, Q, num_frames)

    if plot:
        emg.plot()

    return emg


def process_signal(signal, low, high, Q, num_frames):
    """
    Processes the EMG signal by applying various filters and transformations.

    Parameters:
    - signal: EMG signal as a NumPy array or list of numeric values.
    - low: Lower cutoff frequency for bandpass filter.
    - high: Upper cutoff frequency for bandpass filter.
    - Q: Q factor for notch filter.
    - num_frames: Number of frames to keep after end frame cutting.

    Returns:
    - emg: Processed EMG signal.
    """
    signal = np.array(signal)

    if not Q == 0:
        signal = butter_notch(signal, Q)

    emg = pep.wrappers.EMGMeasurement(signal, hz=250)
    emg.apply_dc_offset_remover()
    emg.apply_bandpass_filter(2, low, high)
    emg.apply_full_wave_rectifier()
    emg.apply_end_frame_cutter(n_end_frames=num_frames)

    return emg


def butter_notch(chan_data, Q, Fs=250, notch_freq=60.0):
    """
    Applies a notch filter to remove noise at a specific frequency.

    Parameters:
    - chan_data: EEG data as a NumPy array or list of numeric values.
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
