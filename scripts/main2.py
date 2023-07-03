"""
This script runs the entire project pipeline
"""

## IMPORTS
import time
import numpy as np
import threading
import sys
import pyautogui
import pylsl
import argparse
from collections import deque
from scipy.signal import butter, iirnotch, firwin, filtfilt, periodogram

sys.path.append('utils')
from signal_processing import *
from features import *
#from process_data_online import *

acc_inlet = None
emg_inlet = None
scale = 1
stop = False
calibrate = None

FS = 250
THRESHOLD = 50

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


def processing_function(chunk):
    """
    Processes the chunk of data by applying tripolar laplacian, filtering, and rectification.
    Parameters:
    - chunk: Chunk of EMG data
    """
    proc_chunk = process_chunk(chunk)
    mav_metric = np.max([mean_absolute_value(proc_chunk[:,i]) for i in range(proc_chunk.shape[1])])
    print(mav_metric)
    if mav_metric > THRESHOLD:
        return True
    else:
        return False
    
def get_baseline():
    """
    This thread reads the accelerometer LSL stream and creates a baseline for ACC normalization
    """
    global acc_inlet
    global calibrate


    print('Keep hand still')
    data = []

    start = time.time()
    # Read LSL stream
    while time.time()-start<6:
        sample, times = acc_inlet.pull_sample()
        data.append([sample[0],sample[1]])
    
    calibrate = np.mean(np.array(data),axis=0)
    
    

        
    
def acc_lsl_thread():
    """
    This thread reads the accelerometer LSL stream and moves the mouse accordingly
    """
    global acc_inlet
    global scale
    global stop
    global calibrate


    print('LSL thread awake'); sys.stdout.flush();
    
    threshold_xL =  calibrate[0]-0.4
    threshold_xR =  calibrate[0]+0.4
    threshold_yD =  calibrate[1]-0.4
    threshold_yU =  calibrate[1]+0.4
    
    
    
    # Read LSL stream
    while True:
        chunk, times = acc_inlet.pull_chunk(timeout=0.25)
        sample = np.mean(np.array(chunk),axis=0)
        x= (sample[0]-calibrate[0]) * scale
        y= (sample[1]-calibrate[1]) * scale
        pyautogui.move(x, y)
        
        if (np.abs(x)>4) or  (np.abs(y)>4):
            stop = True            
            continue
        stop=False

def emg_lsl_thread():
    """
    This thread reads the emg LSL stream and moves the mouse accordingly
    """
    global emg_inlet
    global stop

    print('LSL thread awake'); sys.stdout.flush();

    
    # Read LSL stream
    while True:
        if stop==True:
            continue
        chunk, times = emg_inlet.pull_chunk(timeout=0.5)
        if processing_function(chunk):
            pyautogui.click()




        
def validation(runtime, sensitivity):
    """
    Validates the runtime and sensitivity parameters.
    """
    assert runtime > 0, "Time must be greater than 0"
    assert sensitivity > 0, "Sensitivity must be greater than 0"
    return True


##########################################################################
##########################################################################

if __name__ == "__main__":
    DEQUE_SIZE = 50
    pyautogui.FAILSAFE = True

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='EMG mouse script')

    # Add command line arguments
    parser.add_argument('-s', '--sensitivity', default=5, type=int, help='Sensitivity of cursor movements out of 10 where 1 is least sensitive and 10 is most. Default is 5.')
    parser.add_argument('-t', '--time', default=60, type=int, help='Time in seconds of how long EMG mouse is turned on. Default = 60 seconds.')

    # Parse the command line arguments
    args = parser.parse_args()
    sensitivity = args.sensitivity
    runtime = args.time


    #validate input
    validation(runtime, sensitivity)

    # Set global variables 
    scale = sensitivity * 5     

    # initialize pyautogui window and set cursor in middle
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth/2, screenHeight/2)

    # Initialize accelerometer LSL stream
    acc_streams = pylsl.resolve_stream('type', 'ACC')
    acc_inlet = pylsl.stream_inlet(acc_streams[0], recover = False)
    print('Accelerometer Inlet Created'); sys.stdout.flush();

    # Initialize EMG time series LSL stream
    emg_streams = pylsl.resolve_stream('type', 'EMG')
    emg_inlet = pylsl.stream_inlet(emg_streams[0], recover = False)
    print('EMG Inlet Created'); sys.stdout.flush();
    
    
    # Get accelerometer baseline 
    get_baseline()
    
    
    # Launch accelerometer LSL thread
    acc_lsl = threading.Thread(target = acc_lsl_thread, args = ())
    acc_lsl.setDaemon(True) 
    acc_lsl.start()
    
    # Launch accelerometer LSL thread
    emg_lsl = threading.Thread(target = emg_lsl_thread, args = ())
    emg_lsl.setDaemon(True) 
    emg_lsl.start()
    
    # Wait for time to pass and then exit
    time.sleep(runtime)
    print('Time is up!'); sys.stdout.flush();