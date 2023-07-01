import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../')
from utils.signal_processing import *
import pyemgpipeline as pep
from scipy.signal import butter, iirnotch, firwin, filtfilt, periodogram

def data_from_files(data, metadata, electrodes=[[3,2],[7,6]]):
    sess_data = pd.read_csv(data,header=None)
    sess_metadata = pd.read_csv(metadata, names=['start_time','category'])
    category_instances = {}
    for i, row in sess_metadata.iterrows():
        start_time = row['start_time']
        category = row['category'].strip()
        end_time = sess_metadata.iloc[i + 1]['start_time'] if i < (len(sess_metadata) - 1) else sess_data.iloc[-1][0]
        all_electrodes = []
        for electrode in electrodes:
            all_electrodes += electrode
        channels = sess_data.loc[(sess_data[0] >= start_time) & (sess_data[0] < end_time)].iloc[:,all_electrodes]

        instances = pd.DataFrame()
        for i,pair in enumerate(electrodes):
            instances[f'e{i+1}'] = tripolar_laplacian(channels[pair[0]],pair[1])
        #instances['e2'] = tripolar_laplacian(channels[7],channels[6])

        if category not in category_instances:
            category_instances[category] = []
        category_instances[category].append(instances)
    return category_instances

def plot_emg(cat_dict, category, instance, electrode, low=5, high=124, Q=30, num_frames=50, plot=True):
    signal = cat_dict[category][instance][electrode]
    emg = process_signal(signal, low, high, Q, num_frames)
    if plot:
        emg.plot()
        #plt.plot(signal)
        #plt.title(f'{category}: {instance}, electrode {electrode}')
    return emg #signal #

def process_signal(signal, low, high, Q, num_frames):
    signal = np.array(signal)
    if not Q==0:
        signal = butter_notch(signal,Q)
    emg = pep.wrappers.EMGMeasurement(signal, hz=250)
    emg.apply_dc_offset_remover()
    emg.apply_bandpass_filter(2,low,high)
    #emg.apply_amplitude_normalizer(100)
    emg.apply_full_wave_rectifier()
    emg.apply_end_frame_cutter(n_end_frames=num_frames)
    return emg

def butter_notch(chan_data, Q, Fs=250, notch_freq=60.0):
    # Define the filter parameters
    #Q = 30.0

    # Calculate the notch filter coefficients
    w0 = notch_freq / (Fs / 2)
    b, a = iirnotch(w0, Q)

    # Apply the filter to the EEG data
    notched_data = filtfilt(b, a, chan_data)
    return notched_data