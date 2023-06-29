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

acc_inlet = None
emg_inlet = None
scale = 1
buffer = None
clench = False

LCLICK = 0
RCLICK = 1
CLENCH = 2

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
            pyautogui.move(-1 * sample[0]*scale, -1 * sample[1] * scale)

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
            # do something with output 
            
            buffer.clear()


        
def validation(time, sensitivity):
    assert time > 0, "Time must be greater than 0"
    assert sensitivity > 0, "Sensitivity must be greater than 0"
    return True


##########################################################################
##########################################################################

if __name__ == "__main__":
    DEQUE_SIZE = 50

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='EMG mouse script')

    # Add command line arguments
    parser.add_argument('-s', '--sensitivity', default=5, type=int, help='Sensitivity of cursor movements out of 10 where 1 is least sensitive and 10 is most. Default is 5.')
    parser.add_argument('-t', '--time', default=60, type=int, help='Time in seconds of how long EMG mouse is turned on. Default = 60 seconds.')

    # Parse the command line arguments
    args = parser.parse_args()
    sensitivity = args.sensitivity
    time = args.time


    #validate input
    validation(time, sensitivity)

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
    time.sleep(time)
    print('Time is up!'); sys.stdout.flush();