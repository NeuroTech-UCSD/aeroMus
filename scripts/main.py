"""
TODO: fix description
This script runs the entire project pipeline
Notes:
- requires calibration.py, preprocessing.py, analysis.py ...
- run by typing 'python main.py' in the terminal or console
- ...
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

sys.path.append('utils')
from signal_processing import *
from features import *

acc_inlet = None
emg_inlet = None
scale = 1
buffer = None
clench = False

LCLICK = 0
RCLICK = 1
CLENCH_TRUE = 2
CLENCH_FALSE = 3
FS = 250
THRESHOLD = 1200

def processing_function(chunk):
    chunk = np.array(chunk)
    e1 = filter_emg(tripolar_laplacian(chunk[:, 1], chunk[:, 0]), FS)
    e2 = filter_emg(tripolar_laplacian(chunk[:, 3], chunk[:, 2]), FS)
    e3 = filter_emg(tripolar_laplacian(chunk[:, 5], chunk[:, 4]), FS)
    e4 = filter_emg(tripolar_laplacian(chunk[:, 7], chunk[:, 6]), FS)

    metric = np.mean([mean_absolute_value(x) for x in [e1, e2, e3, e4]])
    print(metric)
    if metric > THRESHOLD:
        return CLENCH_TRUE
    else:
        return 0

def acc_lsl_thread():
    """
    This thread reads the accelerometer LSL stream and moves the mouse accordingly
    """
    global acc_inlet
    global scale
    global clench


    print('LSL thread awake'); sys.stdout.flush();

    
    # Read LSL stream
    while True:
        if clench:
            sample, times = acc_inlet.pull_sample()
            pyautogui.move(sample[0]*scale, sample[1] * scale)

def emg_lsl_thread():
    """
    This thread reads the emg LSL stream and moves the mouse accordingly
    """
    global emg_inlet
    global buffer
    global clench

    print('LSL thread awake'); sys.stdout.flush();

    
    # Read LSL stream
    while True:
        sample, times = emg_inlet.pull_sample()
        buffer.append(sample)
        if len(buffer) == buffer.maxlen:
            # send to processing pipeline 
            prediction = processing_function(buffer)
            buffer.clear()

            # check if clenching, if so ignore all other predictions until not clenching
            if clench: 
                if prediction != CLENCH_TRUE:
                    continue
                else:
                    clench = False 
                    print("Resting")
                    continue 
            # if not clenching, look for other predictions 
            if prediction == CLENCH_TRUE:
                clench = True
                print("Clenching")
            else:
                continue
            '''elif prediction == RCLICK:
                pyautogui.rightClick()
            elif prediction == LCLICK:
                clench = True'''



        
def validation(runtime, sensitivity):
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
    scale = sensitivity * 2 
    buffer = deque(maxlen=DEQUE_SIZE)

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