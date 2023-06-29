import numpy as np
import pyemgpipeline as pep


### Time-Domain Features

def mean_absolute_value(data):
    return np.mean(np.abs(data))

def slope_sign_changes(data):
    return np.diff((np.diff(data) < 0)).sum() # astypefloatnecessary?

def waveform_length(data):
    return np.sum(np.abs(np.diff(data)))

def zero_crossings(data):
    return np.sum(np.diff(data > 0).astype(float)) # astypefloatnecessary?

def root_mean_square(data):
    # requires that data is np.array
    return np.sqrt(np.mean(data**2))


### Frequency-Domain Features

def to_fdomain(data, sampling_rate):
    return np.abs(np.fft.fft(data))**2, np.fft.fftfreq(len(data), 1/sampling_rate)

def peak_frequencies(power, freqs):
    from scipy.signal import find_peaks
    peak_indices = find_peaks(power)[0]
    return freqs[peak_indices]

def mean_frequency(power, freqs):
    return np.sum(freqs*power)/np.sum(psd)

def median_frequency(power, freqs):
    # Sort the power spectrum and frequencies in ascending order
    sorted_indices = np.argsort(power)
    sorted_spectrum = power[sorted_indices]
    sorted_frequencies = freqs[sorted_indices]
    
    # Calculate the cumulative sum of the power spectrum
    cumulative_sum = np.cumsum(sorted_spectrum)
    
    # Find the index where cumulative sum crosses half of the total power
    median_index = np.argmax(cumulative_sum >= np.sum(sorted_spectrum) / 2)
    
    # Get the median frequency
    mdf = sorted_frequencies[median_index]
    
    return mdf




### Time-Frequency Domain Features


def calculate_wavelet_coefficients(data, wavelet='morl'):
    import pywt
    # Perform Continuous Wavelet Transform
    coefficients, _ = pywt.cwt(data, scales=range(1, len(data)+1), wavelet=wavelet)
    
    return coefficients



### Other

def filter_emg(sig, fs):

    m = pep.wrappers.EMGMeasurement(sig, hz=fs)

    m.apply_dc_offset_remover()

    #m.apply_bandpass_filter(bf_cutoff_fq_hi=fs/2 - 1)

    #m.apply_full_wave_rectifier()

    #m.apply_linear_envelope()

    #m.apply_end_frame_cutter(n_end_frames=2)

    #m.apply_amplitude_normalizer(max_amplitude=8.5)

    #m.apply_segmenter(beg_ts=0, end_ts=0.015)

    return m.data