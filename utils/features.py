import numpy as np
import pyemgpipeline as pep


### Time-Domain Features

def mean_absolute_value(data):
    """
    Calculates the mean absolute value of the given data.

    Parameters:
    - data: NumPy array or list of numeric values.

    Returns:
    - mean_abs_value: Mean absolute value of the data.
    """
    return np.mean(np.abs(data))


def slope_sign_changes(data):
    """
    Counts the number of slope sign changes in the given data.

    Parameters:
    - data: NumPy array or list of numeric values.

    Returns:
    - num_changes: Number of slope sign changes in the data.
    """
    return np.diff((np.diff(data) < 0)).sum()


def waveform_length(data):
    """
    Calculates the waveform length of the given data.

    Parameters:
    - data: NumPy array or list of numeric values.

    Returns:
    - wave_length: Waveform length of the data.
    """
    return np.sum(np.abs(np.diff(data)))


def zero_crossings(data):
    """
    Counts the number of zero crossings in the given data.

    Parameters:
    - data: NumPy array or list of numeric values.

    Returns:
    - num_crossings: Number of zero crossings in the data.
    """
    return np.sum(np.diff(data > 0).astype(float))


def root_mean_square(data):
    """
    Calculates the root mean square (RMS) of the given data.

    Parameters:
    - data: NumPy array or list of numeric values.

    Returns:
    - rms: Root mean square of the data.
    """
    return np.sqrt(np.mean(data**2))


### Frequency-Domain Features ###

def to_fdomain(data, sampling_rate):
    """
    Converts the given time-domain data to the frequency domain using Fast Fourier Transform (FFT).

    Parameters:
    - data: NumPy array or list of numeric values.
    - sampling_rate: Sampling rate (in Hz) of the data.

    Returns:
    - power_spectrum: Power spectrum of the data.
    - frequencies: Frequencies corresponding to the power spectrum.
    """
    return np.abs(np.fft.fft(data))**2, np.fft.fftfreq(len(data), 1/sampling_rate)


def peak_frequencies(power, freqs):
    """
    Identifies the peak frequencies in the given power spectrum.

    Parameters:
    - power: Power spectrum of the data.
    - freqs: Frequencies corresponding to the power spectrum.

    Returns:
    - peak_freqs: Frequencies at which the peaks occur in the power spectrum.
    """
    from scipy.signal import find_peaks
    peak_indices = find_peaks(power)[0]
    return freqs[peak_indices]


def mean_frequency(power, freqs):
    """
    Calculates the mean frequency of the given power spectrum.

    Parameters:
    - power: Power spectrum of the data.
    - freqs: Frequencies corresponding to the power spectrum.

    Returns:
    - mean_freq: Mean frequency of the power spectrum.
    """
    return np.sum(freqs * power) / np.sum(power)


def median_frequency(power, freqs):
    """
    Calculates the median frequency of the given power spectrum.

    Parameters:
    - power: Power spectrum of the data.
    - freqs: Frequencies corresponding to the power spectrum.

    Returns:
    - median_freq: Median frequency of the power spectrum.
    """
    # Sort the power spectrum and frequencies in ascending order
    sorted_indices = np.argsort(power)
    sorted_spectrum = power[sorted_indices]
    sorted_frequencies = freqs[sorted_indices]
    
    # Calculate the cumulative sum of the power spectrum
    cumulative_sum = np.cumsum(sorted_spectrum)
    
    # Find the index where cumulative sum crosses half of the total power
    median_index = np.argmax(cumulative_sum >= np.sum(sorted_spectrum) / 2)
    
    # Get the median frequency
    median_freq = sorted_frequencies[median_index]
    
    return median_freq


def calculate_average_power(power, freqs, n):
    """
    Calculates the average power within frequency bands of the given power spectrum.

    Parameters:
    - power: Power spectrum of the data.
    - freqs: Frequencies corresponding to the power spectrum.
    - n: Number of frequency bands.

    Returns:
    - band_power: List of average power values for each frequency band.
    """
    num_bands = n
    band_power = []
    band_size = len(freqs) // num_bands

    for i in range(num_bands):
        start_index = i * band_size
        end_index = (i + 1) * band_size

        # Calculate the average power within the band
        avg_power = np.mean(power[start_index:end_index])
        band_power.append(avg_power)

    return band_power


### Time-Frequency Domain Features ###

def calculate_wavelet_coefficients(data, wavelet='morl'):
    """
    Calculates the wavelet coefficients of the given data using Continuous Wavelet Transform (CWT).

    Parameters:
    - data: NumPy array or list of numeric values.
    - wavelet: Wavelet function to use for CWT. Default is 'morl'.

    Returns:
    - coefficients: Wavelet coefficients of the data.
    """
    import pywt
    # Perform Continuous Wavelet Transform
    coefficients, _ = pywt.cwt(data, scales=range(1, len(data)+1), wavelet=wavelet)
    
    return coefficients


### Other ###

def filter_emg(sig, fs):
    """
    Applies a series of filters to the EMG signal.

    Parameters:
    - sig: EMG signal as a NumPy array or list of numeric values.
    - fs: Sampling rate (in Hz) of the EMG signal.

    Returns:
    - filtered_data: Filtered EMG signal.
    """
    m = pep.wrappers.EMGMeasurement(sig, hz=fs)

    m.apply_dc_offset_remover()
    #m.apply_bandpass_filter(bf_cutoff_fq_hi=fs/2 - 1)
    #m.apply_full_wave_rectifier()
    #m.apply_linear_envelope()
    #m.apply_end_frame_cutter(n_end_frames=2)
    #m.apply_amplitude_normalizer(max_amplitude=8.5)
    #m.apply_segmenter(beg_ts=0, end_ts=0.015)

    return m.data
