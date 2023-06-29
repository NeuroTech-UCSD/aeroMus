import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../')
from utils.signal_processing import *
import pyemgpipeline as pep

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

def plot_emg(cat_dict, category, instance, electrode, plot=True):
    signal = cat_dict[category][instance][electrode]
    emg = process_signal(signal)
    if plot:
        emg.plot()
        #plt.plot(signal)
        #plt.title(f'{category}: {instance}, electrode {electrode}')
    return emg #signal #

def process_signal(signal):
    signal = np.array(signal)
    #signal = np.array(signal - signal.mean())
    emg = pep.wrappers.EMGMeasurement(signal, hz=250)
    emg.apply_dc_offset_remover()
    emg.apply_bandpass_filter(2,5,124)
    #emg.apply_full_wave_rectifier()
    #emg.apply_end_frame_cutter(n_end_frames=50)
    return emg