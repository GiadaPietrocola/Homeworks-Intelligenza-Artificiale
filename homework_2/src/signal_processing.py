"""Signal Processing Exercise""" 
import numpy as np 
import matplotlib.pyplot as plt 
 
 
def analyze_signal(time, clean, noisy):
    """
    Exercise 1: Signal Processing with NumPy
    ---------------------------------------
    Task: Analyze and visualize a signal with noise.
    
    Required steps:
    1. Calculate basic signal statistics:
       - Mean and standard deviation
       - Maximum and minimum values
       - Signal-to-noise ratio
    
    2. Process the signal:
       - Apply a moving average filter (window size = 5)
       - Perform frequency analysis using FFT
    
    3. Create visualizations:
       - Plot original clean signal
       - Plot noisy signal
       - Plot filtered signal
       - Show frequency spectrum
    
    Parameters:
    -----------
    time : numpy.ndarray
        Time points for the signal
    clean : numpy.ndarray
        Original clean signal values
    noisy : numpy.ndarray
        Signal with added noise
    
    Expected Output:
    --------------
    1. Two subplot figure showing:
       - Time domain: clean, noisy, and filtered signals
       - Frequency domain: frequency spectrum
    2. Dictionary with signal statistics
    
    Hint: Use np.fft for frequency analysis
    """

    mean_noisy = np.mean(noisy)   # Mean
    std_noisy = np.std(noisy)     # Standard Deviation
    max_noisy = np.max(noisy)     # Maximum value
    min_noisy = np.min(noisy)     # Minimum value

    # Signal-to-noise ratio
    signal_power = np.mean(clean ** 2)
    noise_power = np.mean((noisy - clean) ** 2)
    snr = 10 * np.log10(signal_power / noise_power)

    # Dictionary with signal statistics
    stats = {
        "Mean": mean_noisy,
        "Standard Deviation": std_noisy,
        "Maximum value": max_noisy,
        "Minimum value": min_noisy,
        "Signal-to-noise ratio": snr
    }

    # Moving average filter
    window_size = 5
    filtered = np.convolve(noisy, np.ones(window_size) / window_size, mode='same') # same = forces the result to be the same size as "noisy" (for plotting matters)

    # Frequency analysis
    freq = np.fft.fftfreq(len(time), time[1] - time[0])
    fft_filtered = np.fft.fft(filtered)

    # Plots
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Time domain
    axes[0].plot(time, clean, label='Clean Signal', color='blue')
    axes[0].plot(time, noisy, label='Noisy Signal', linestyle="dotted", color='red')
    axes[0].plot(time, filtered, label='Filtered Signal', color='green')
    axes[0].set_title('Signal Analysis (mean= , std= )')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()
    axes[0].grid()

    # Mask for positive frequencies
    positive_freq = freq >= 0
    freq_positive = freq[positive_freq]
    fft_positive = fft_filtered[positive_freq]

    # Frequency domain
    axes[1].plot(freq_positive, fft_positive, label='Filtered Signal', color='blue')
    axes[1].set_title('Frequency Spectrum')
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].set_ylabel('Amplitude')
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    plt.show()

    return stats

