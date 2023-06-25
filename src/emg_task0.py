# 6-class EMG paradigm
#
# 1. Fingers extended (relaxed)
# 2. Fingers clenched
# 3. L. Planar movement
# 4. R. Planar movement
# 5. U. Planar movement
# 6. D. Planar movement
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! MAKE SURE refresh_rate IS SET TO YOUR MONITOR'S REFRESH RATE !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Created........: 04Feb2022 [ollie-d]
# Last Modified..: 04Feb2022 [ollie-d]



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

from itertools import chain
from math import atan2, degrees


# Global variables
win = None          # Global variable for window (Initialized in main)
mrkstream = None    # Global variable for LSL marker stream (Initialized in main)
photosensor = None  # Global variable for photosensor (Initialized in main)
triangle = None     # Global variable for stimulus (Initialized in main)
fixation = None     # Global variable for fixation cross (Initialized in main)

bg_color = [-1, -1, -1]
win_w = 800
win_h = 600
refresh_rate = 60. # Monitor refresh rate (CRITICAL FOR TIMING)
prefix = None
eeg_inlet = None
session = None
metadata = []
timepoints = []


#========================================================
# High Level Functions
#========================================================
def lsl_thread():
    global eeg_inlet
    global prefix 

    out_path = prefix + "_data.txt"
    print('LSL thread awake'); sys.stdout.flush();
    
    # Read LSL
    while True:
        sample, times = eeg_inlet.pull_sample()
        # Append sample if exists (from single channel, ch) to file
        with open(out_path,"a") as fo:
            fo.write(f"{str(times)}, {str(sample)[1:-1]}\n")
    


def Paradigm(n):
    global refresh_rate
    global win
    global photosensor
    global fixation
    global triangle
    global mrkstream
    global bg_color
    global metadata
    global timepoints
    
    met_value = 0 # metronome value
    
    # Compute sequence of stimuli
    sequence = CreateSequence(n)
    
    # Initialize metronome, primary and secondary text
    met = psychopy.visual.TextStim(win, text = 'X', units = 'norm', alignText = 'center');
    met.setHeight(0.1);
    met.pos = (-0.4, 0)
    met.draw()
    
    # Initialize current instruction
    cur = psychopy.visual.TextStim(win, text = 'X', units = 'norm', alignText = 'center');
    cur.setHeight(0.1);
    cur.pos = (0, 0)
    cur.draw()
    
    # Initialize next instruction
    nxt = psychopy.visual.TextStim(win, text = 'X', units = 'norm', alignText = 'center', color = (0.05, 0.05, 0.05));
    nxt.setHeight(0.1);
    nxt.pos = (0, -0.1)
    nxt.draw()

    # set text to be appropriate sequences
    #cur.text = sequence[0]
    #nxt.text = sequence[1]

    #win.flip()
    
    # Iterate through remaining sequence
    for i in range(0, len(sequence)):
        # Set LSL marker with current stim
        #mrk = pylsl.vectorstr([sequence[i]]) # TODO LOOK HERE
        #print(mrk)
        mrk = sequence[i]

        # Update texts
        cur.text = sequence[i]
        if i < len(sequence)-1:
            nxt.text = sequence[i+1]
        else:
            nxt.text = 'End'
        
        # Cycle through 4 beats (120bpm) of the metronome. On final, change sequence
        # Make it 8 beats for rests
        nbeats = 1
        if sequence[i] == 'REST' or sequence[i][:4] == 'HOLD': #changed from C to U ***********************
            nbeats = 4
        for count in range(nbeats, 0, -1):
            # Set metronome
            met.text = f'{count}'
            
            # Spend 1 beat (500ms) drawing text
            for frame in range(MsToFrames(1000, refresh_rate)):
                if frame == 0 and count == nbeats:
                    sample, times = eeg_inlet.pull_sample()
                    timepoints.append(times)
                    metadata.append(mrk) 
                    #mrkstream.push_sample(mrk);
                met.draw()
                nxt.draw()
                cur.draw()
                win.flip()
        
    return metadata
    
    '''
    for i, s in enumerate(sequence):
        # 250ms Bold fixation cross
        fixation.lineWidth = 1
        fixation.lineColor = [1, 1, 1]
        SetStimulus(fixation, 'on')
        for frame in range(MsToFrames(250, refresh_rate)):
            fixation.draw()
            win.flip()
            
        # 500ms Normal fixation cross
        fixation.lineColor = bg_color
        for frame in range(MsToFrames(500, refresh_rate)):
            fixation.draw()
            win.flip()
    
        # 500ms Stimulus presentation (w/ fixation)
        RotateTriangle(triangle, 180)   # <-- Standard (S)
        mrk = pylsl.vectorstr(['0'])
        if s == 'T':
            RotateTriangle(triangle, 0) # <-- Target (T)
            mrk = pylsl.vectorstr(['1'])
        SetStimulus(photosensor, 'on')
        for frame in range(MsToFrames(500, refresh_rate)):
            # Send LSL marker on first frame
            if frame == 0:
                mrkstream.push_sample(mrk);
            photosensor.draw()
            triangle.draw()
            fixation.draw()
            win.flip()
        
        # 1000ms darkness
        for frame in range(MsToFrames(1000, refresh_rate)):
            win.flip()
    '''
#========================================================
# Low Level Functions
#========================================================
def CreateSequence(n):
    # code between horizontal lines is Ollie's code for this function. I'm leaving it in case 
    # we need to refer back to it
    #_____________________________________________________________________________________
    # Create "n" of each movement type
    #
    # C is clenched
    # L is left
    # R is right
    # U is up
    # D is down
    # O is open (relaxed)
    #
    # Relaxed will always be between other movements

    # ['WrD', 'WrU', 'ClQ', 'ThO', 'PP', 'ClH', 'InU', 'InD', 'ThD', 'MiD', 'RiD', 'PiD']
    movements = ['CLENCH']

    seq = movements*n
    # for i in ['Clench','Tinca']:
    #    seq.append([i for x in range(n)])
    # seq = listFlatten(seq)

    random.seed()
    random.shuffle(seq) # shuffles in-place
    
    # Iterate through shuffled seq and add relaxed
    seq_ = []
    for s in seq:
       seq_.extend(['REST', s, 'HOLD ' + s, 'STOP ' + s]) #changed from C to U to Re ***********************
        
    seq = None

    # ________________________________________________________________

    # U = wrist up
    # O = rest / open
    # C = clench
    # D = down 
    # T = thumb
    # I = index finger
    # M = middle finger
    # R = ring finger
    # P = pinky
    
    return seq_

def InitFixation(size=50):
    return psychopy.visual.ShapeStim(
                win=win,
                units='pix',
                size = size,
                fillColor=[1, 1, 1],
                lineColor=[1, 1, 1],
                lineWidth = 1,
                vertices = 'cross',
                name = 'off', # Used to determine state
                pos = [0, 0]
            )

def InitPhotosensor(size=50):
    # Create a circle in the lower right-hand corner
    # Will be size pixels large
    # Initiate as color of bg (off)
    return psychopy.visual.Circle(
            win=win,
            units="pix",
            radius=size,
            fillColor=bg_color,
            lineColor=bg_color,
            lineWidth = 1,
            edges = 32,
            name = 'off', # Used to determine state
            pos = ((win_w / 2) - size, -((win_h / 2) - size))
        )

def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

def DegToPix(h, d, r, deg):
    # Source: https://osdoc.cogsci.nl/3.2/visualangle/
    deg_per_px = degrees(atan2(.5*h, d)) / (.5*r)
    size_in_px = deg / deg_per_px
    return size_in_px

def listFlatten(l):
    return list(chain.from_iterable(l))

def CreateMrkStream():
    info = pylsl.stream_info('EMG_Markers', 'Markers', 1, 0, pylsl.cf_string, 'unsampledStream');
    outlet = pylsl.stream_outlet(info, 1, 1)
    return outlet;

if __name__ == "__main__":
    # TODO: updaute two variables here every round 
    # SET GLOBALS 
    session = 1
    paradigm_repeats = 10

    prefix = "/Users/soysa/Documents/Git/Project-TNNI-ACD/data/emg_recordings/test_sess{}".format(session) # + 'EMG'


    # Create PsychoPy window
    win = psychopy.visual.Window(
        screen = 0,
        size=[win_w, win_h],
        units="pix",
        fullscr=True,
        color=bg_color,
        gammaErrorPolicy = "ignore"
    );

    # Initialize LSL marker/ stream
    # mrkstream = CreateMrkStream();

    eeg_streams = pylsl.resolve_stream('type', 'EEG')
    eeg_inlet = pylsl.stream_inlet(eeg_streams[0], recover = False)
    print('Inlet Created'); sys.stdout.flush();
    
    # Launch LSL thread
    lsl = threading.Thread(target = lsl_thread, args = ())
    lsl.setDaemon(True)
    lsl.start()
    
    time.sleep(5)
    


    # Run through paradigm
    metadata = Paradigm(paradigm_repeats)

    out_path = prefix + "_metadata.txt"
    with open(out_path,"a") as fo:
        for i in range(len(timepoints)):
            fo.write(str(timepoints[i]) + ', ')
            fo.write(metadata[i])
            fo.write('\n')