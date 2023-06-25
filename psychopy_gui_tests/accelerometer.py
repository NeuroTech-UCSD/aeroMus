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
    global prefix 
    global buffer_x
    global buffer_y
    global buffer_z
    
    x = 0
    z = 0
    
    print('LSL thread awake'); sys.stdout.flush();

    
    # Read LSL
    # end loop after 10 seconds
    start_time = time.time()
    while True:
        
        sample, times = eeg_inlet.pull_sample()
        
        if sample[0] > 0.2: 
            x = 1
        elif sample[0] < -0.2:
            x = -1
        if sample[2] > 1.2:
            z = 1
        elif sample[2] < 0.8:
            z = -1
        

        pyautogui.move(x, z)
        x = 0
        z = 0
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            break



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
    
    time.sleep(12)