import time
import pylsl
import numpy as np
import threading
import sys
import pyautogui

eeg_inlet = None

def lsl_thread():
    global eeg_inlet
    print('LSL thread awake'); sys.stdout.flush();

    
    # Read LSL
    while True:
        sample, times = eeg_inlet.pull_sample()
        pyautogui.move(sample[0]*12,  sample[1] * 12)



if __name__ == "__main__":
    # initialize pyautogui window and set cursor in middle
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth/2, screenHeight/2)



    # Initialize LSL marker/ stream
    eeg_streams = pylsl.resolve_stream('type', 'EEG')
    eeg_inlet = pylsl.stream_inlet(eeg_streams[0], recover = False)
    print('Inlet Created'); sys.stdout.flush();
    
    # Launch LSL thread
    lsl = threading.Thread(target = lsl_thread, args = ())
    lsl.setDaemon(True) 
    lsl.start()
    
    time.sleep(30)