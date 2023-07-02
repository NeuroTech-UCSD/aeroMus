# Description: This file contains the code for the classification
#              task. It is a modified version of the EMG task.
#

import time
import pylsl
import random
import numpy as np
from psychopy import event, visual
import threading
import sys

# custom functions
sys.path.append('utils')
from signal_processing import *
from features import *
#from process_data_online import *

# Global variables
my_window = None
bg_color = [-1, -1, -1]
win_w = 800
win_h = 600
eeg_inlet = None
FS = 250
THRESHOLD = 8

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import pyemgpipeline as pep
from scipy.signal import butter, iirnotch, firwin, filtfilt, periodogram

def classify_motion(chunk, rest_peaks, threshold=8):
    proc_chunk = process_chunk(chunk)
    chunk_peaks = find_peaks(proc_chunk)
    amp_factor = compute_amp_factor(chunk_peaks, rest_peaks)
    print(amp_factor)
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

#========================================================
# High Level Functions
#========================================================
def lsl_thread():
    global eeg_inlet
    global my_window

    print('LSL thread awake')
    sys.stdout.flush()

    # Initialize current instruction
    cur = visual.TextStim(my_window, text='X', units='norm', alignText='center')
    cur.setHeight(0.1)
    cur.pos = (0, 0)
    
    # Read LSL
    while True:
        chunk, timestamps = eeg_inlet.pull_chunk(timeout=3)

        # process signal
        chunk = np.array(chunk)
        e1 = filter_signal(tripolar_laplacian(chunk[:, 1], chunk[:, 0]))
        # can take mean over multiple electrodes

        # classify
        metric = mean_absolute_value(e1)
        print(metric)

        if metric > THRESHOLD:
            cur.text = 'CLENCH'
        else:
            cur.text = 'REST'

        cur.draw()
        my_window.flip()

if __name__ == "__main__":
    # Create PsychoPy window
    my_window = visual.Window(
        screen=0,
        size=[win_w, win_h],
        units="pix",
        fullscr=False,
        color=bg_color,
        gammaErrorPolicy="ignore"
    )

    eeg_streams = pylsl.resolve_stream('type', 'EEG')
    eeg_inlet = pylsl.stream_inlet(eeg_streams[0], recover=False)
    print('Inlet Created')
    sys.stdout.flush()

    # Initialize current instruction
    cur = visual.TextStim(my_window, text='X', units='norm', alignText='center')
    cur.setHeight(0.1)
    cur.pos = (0, 0)
    '''
    rest_peaks = np.zeros((4,))
    for i in range(6):
        chunk, timestamps = eeg_inlet.pull_chunk(timeout=0.5)
        #chunk = np.array(chunk)
        rest_peaks += find_peaks(process_chunk(chunk))
        e1 = filter_emg(tripolar_laplacian(chunk[:, 1], chunk[:, 0]), FS)
        e2 = filter_emg(tripolar_laplacian(chunk[:, 3], chunk[:, 2]), FS)
        e3 = filter_emg(tripolar_laplacian(chunk[:, 5], chunk[:, 4]), FS)
        e4 = filter_emg(tripolar_laplacian(chunk[:, 7], chunk[:, 6]), FS)
        #THRESHOLD = np.mean([mean_absolute_value(x) for x in [e1, e2, e3, e4]])
    rest_peaks = rest_peaks/6
    print(rest_peaks)
    '''
    # Read LSL
    while True:
        chunk, timestamps = eeg_inlet.pull_chunk(timeout=0.5)

        # process signal
        '''
        chunk = np.array(chunk)
        
        e1 = filter_emg(tripolar_laplacian(chunk[:, 1], chunk[:, 0]), FS)
        e2 = filter_emg(tripolar_laplacian(chunk[:, 3], chunk[:, 2]), FS)
        e3 = filter_emg(tripolar_laplacian(chunk[:, 5], chunk[:, 4]), FS)
        e4 = filter_emg(tripolar_laplacian(chunk[:, 7], chunk[:, 6]), FS)
        
        metric = np.mean([mean_absolute_value(x) for x in [e1, e2, e3, e4]])
        '''
        proc_chunk = process_chunk(chunk)
        mav_metric = np.mean([mean_absolute_value(proc_chunk[:,i]) for i in range(proc_chunk.shape[1])])
        # can take mean over multiple electrodes
        
        # classify
        # metric = mean_absolute_value(e1)
        print(mav_metric)
        
        #motion = classify_motion(chunk, rest_peaks, threshold=4)
        #if motion:
        if mav_metric > THRESHOLD:
            cur.text = 'CLENCH'
        else:
            cur.text = 'REST'

        cur.draw()
        my_window.flip()

    # Launch LSL thread
    # lsl = threading.Thread(target=lsl_thread, args=())
    # lsl.setDaemon(True)
    # lsl.start()

    time.sleep(5)
