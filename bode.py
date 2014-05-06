"""
 Bode plot script

 Requires: matplotlib, numpy

 Author: Alfredo 'IceCoder' Mungo <chimeranet89@gmail.com>
 Copyright: 2013
 License: LGPL (GPLv3)
"""

if __name__ == '__main__':
    raise RuntimeError('This is a python module, not a script')

__version__ = "0.1"

from matplotlib import pyplot as plt
from numpy import (angle, pi, log10 as log)
from types import FunctionType
from itertools import tee

__doc__ = \
"This module provides the function to plot the bode diagrams of a function\
and to get the values of a bode plot as a generator function."

_fsam = .001 # Default initial sampling frequency (rad/s)

def plot(f, min_freq, max_freq, fsam = _fsam):
    freq, mag, phase = bode(f, min_freq, max_freq, fsam)
    freq, freq2 = tee(freq)

    fig = plt.figure()
    fig.canvas.set_window_title('Bode diagram')
    plt.ioff()
    plt.subplot(211)
    plt.title('Magnitude')
    plt.ylabel('dB')
    plt.xlabel(r'$\omega$')
    plt.semilogx()
    plt.grid()
    plt.plot([f for f in freq], [m for m in mag])
    plt.subplot(212)
    plt.title('Phase')
    plt.ylabel('deg')
    plt.xlabel(r'$\omega$')
    plt.semilogx()
    plt.grid()
    plt.plot([f for f in freq2], [p for p in phase])
    plt.tight_layout()
    plt.show(block=False)

def bode(f, min_freq, max_freq, fsam = _fsam):
    if not isinstance(f, FunctionType):
        raise TypeError('Argument \'f\' is not a function')

    min_freq = min_freq if min_freq > 0 else fsam #Freq must be > 0

    freq_gen = bode.__dict__['freq_gen']
    freq, freq1, freq2 = tee(freq_gen(min_freq, max_freq, fsam), 3)
    mag_v = mag(f, freq1)
    phi_v = phase(f, freq2)

    return (freq, mag_v, phi_v)

def mag(f, freq_gen):
    for freq in freq_gen:
        yield 20 * log(abs(f(complex(0, freq))))

def phase(f, freq_gen):
    for freq in freq_gen:
        a = angle(f(complex(0, freq))) * 180 / pi

        if a > 180:
            a = 360 - a
        elif a < -180:
            a += 360
        elif a == 360:
            a = 0

        yield a

def _freq_gen_lin(min_freq, max_freq, fsam):
    """
    Linear frequency axis generator
    """
    f = min_freq
    while f < max_freq:
        yield f
        f += fsam

def _freq_gen_exp(min_freq, max_freq, fsam):
    """
    Exponential (base 10) frequency axis generator
    """
    f_step = _freq_gen_exp.__dict__['f_step']

    f = min_freq
    _f_step = f_step
    while f < max_freq:
        yield f
        f += fsam

        _f_step -= 1
        if _f_step <= 0:
            _f_step = f_step
            fsam *= 10 # next decade

bode.__dict__['freq_gen'] = _freq_gen_exp # default frequency axis generator
_freq_gen_exp.__dict__['f_step'] = 60 # produce 'f_step' points for each decade
