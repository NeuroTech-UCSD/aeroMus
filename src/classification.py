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

# Global variables
my_window = None
bg_color = [-1, -1, -1]
win_w = 800
win_h = 600
eeg_inlet = None
FS = 250
THRESHOLD = 1200

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
    
    # Read LSL
    while True:
        chunk, timestamps = eeg_inlet.pull_chunk(timeout=0.35)

        # process signal
        chunk = np.array(chunk)
        e1 = filter_emg(tripolar_laplacian(chunk[:, 1], chunk[:, 0]), FS)
        e2 = filter_emg(tripolar_laplacian(chunk[:, 3], chunk[:, 2]), FS)
        e3 = filter_emg(tripolar_laplacian(chunk[:, 5], chunk[:, 4]), FS)
        e4 = filter_emg(tripolar_laplacian(chunk[:, 7], chunk[:, 6]), FS)

        metric = np.mean([mean_absolute_value(x) for x in [e1, e2, e3, e4]])
        # can take mean over multiple electrodes

        # classify
        # metric = mean_absolute_value(e1)
        # print(metric)

        if metric > THRESHOLD:
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
