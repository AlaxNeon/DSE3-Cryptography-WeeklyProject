"""
fft_demo.py
===========

A tiny, self-contained demonstration of the Fast Fourier Transform (FFT).

This has nothing to do with signing or verifying messages -- it exists so a
beginner can *see* what an FFT actually does: it takes a signal described
sample-by-sample over time (the "time domain") and re-describes the exact
same information in terms of which frequencies are present and how strongly
(the "frequency domain").

Falcon relies on fast polynomial arithmetic over a ring, and its reference
implementation performs the Gaussian sampling step of signing using
floating-point FFT techniques to keep that arithmetic efficient. This demo
does not implement any part of Falcon -- it only shows the general FFT idea
that such implementations build on.
"""

from __future__ import annotations

import numpy as np


def demonstrate_fft() -> None:
    """Build a small signal, run an FFT on it, and print/explain the result."""

    print("Original signal (time domain):")
    print("  This is a list of numbers, one per moment in time -- like")
    print("  8 samples taken evenly across one second.")

    # A small signal made of two combined frequencies (2 Hz and 4 Hz),
    # sampled 8 times over 1 second.
    sample_count = 8
    t = np.linspace(0, 1, sample_count, endpoint=False)
    signal = np.sin(2 * np.pi * 2 * t) + 0.5 * np.sin(2 * np.pi * 4 * t)
    signal_rounded = np.round(signal, 3)

    print(f"  {signal_rounded.tolist()}")

    fft_result = np.fft.fft(signal)
    magnitudes = np.round(np.abs(fft_result), 2)

    print()
    print("FFT result (frequency domain, magnitude per frequency bin):")
    print(f"  {magnitudes.tolist()}")

    print()
    print("What this means:")
    print("  The original signal was built from a 2 Hz wave and a smaller")
    print("  4 Hz wave added together. Looking only at the raw sample list,")
    print("  that is not obvious. The FFT result shows large values at the")
    print("  frequency bins that correspond to 2 Hz and 4 Hz, and small")
    print("  values everywhere else -- exposing the frequencies that were")
    print("  hidden inside the time-domain samples.")
    print()
    print("  The FFT converts information from the time domain into the")
    print("  frequency domain without losing any information: an inverse")
    print("  FFT could reconstruct the original signal exactly.")


if __name__ == "__main__":
    demonstrate_fft()
