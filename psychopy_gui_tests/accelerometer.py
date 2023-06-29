import time
#import pylsl-1.13.0.b4-py_0    #with conda install pyxdf and psychopy, and with pip install pylsl globally
import pylsl
import random
import numpy as np
import psychopy 
from psychopy import event
from psychopy import visual
import threading
import sys
import pyautogui

eeg_inlet = None
buffer_x = []
buffer_y = []
buffer_z = []

def lsl_thread():
    global eeg_inlet
    print('LSL thread awake'); sys.stdout.flush();

    
    # Read LSL
    while True:
        
        sample, times = eeg_inlet.pull_sample()
        pyautogui.move(sample[0]*12,  sample[1] * 12)



if __name__ == "__main__":
    # SET GLOBALS 
    session = 0

    prefix = "/Users/jfaybishenko/projects/TNT/Project-TNNI-ACD/data/eeg_recordings/sess{}/".format(session) + 'accelerometer'

    # initialize pyautogui window and set cursor in middle
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth/2, screenHeight/2)



    # Initialize LSL marker/ stream
    # mrkstream = CreateMrkStream();
    
    eeg_streams = pylsl.resolve_stream('type', 'EEG')
    eeg_inlet = pylsl.stream_inlet(eeg_streams[0], recover = False)
    print('Inlet Created'); sys.stdout.flush();
    
    # Launch LSL thread
    lsl = threading.Thread(target = lsl_thread, args = ())
    lsl.setDaemon(True) 
    lsl.start()
    
    time.sleep(30)