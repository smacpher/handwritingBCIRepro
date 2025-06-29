import numpy as np
from scipy.stats import norm
from scipy.signal import lfilter

# TODO: Better understand how this works.
def gauss_smooth_fast(time_series, width):
    """Applies Gaussian smoothing with edge correction, mimicking MATLAB's filter-based approach.

    Args:
        time_series (ndarray): shape (time, channels)
        width (float): std dev (sigma) of Gaussian kernel

    Returns:
        ndarray: smoothed time series of same shape
    """
    if width == 0:
        return time_series.copy()

    time_steps, channels = time_series.shape

    # Build Gaussian kernel (same as normpdf in MATLAB)
    wing_size = int(np.ceil(width * 5))
    x = np.arange(-wing_size, wing_size + 1)
    g_kernel = norm.pdf(x, 0, width)
    g_kernel /= np.sum(g_kernel)  # Normalize kernel sum to 1

    # Causal-style filtering (zero-padded at the end)
    padded = np.vstack([time_series, np.zeros((len(g_kernel) - 1, channels))])  # pad below
    y = lfilter(g_kernel, 1, padded, axis=0)  # forward filter only

    # Edge correction (start)
    norm_factor = np.cumsum(g_kernel)
    for i in range(len(g_kernel) - 1):
        y[i, :] /= norm_factor[i]

    # Edge correction (end)
    for i in range(len(g_kernel) - 1):
        y[-(i + 1), :] /= norm_factor[i]

    # Trim padded rows to recover original size
    trim = (len(g_kernel) - 1) // 2
    y = y[trim: trim + time_steps, :]

    return y
