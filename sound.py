"""
.. module:: sound
    :synopsis: This module provides sounds creation.
"""

from math import pi
import wave
from numpy import linspace, int16, sin


def note(freq, duration, amp=10000, rate=44100):
    """
    :param freq: frequency of the wave.
    :param duration: duration of the sound in seconds.
    :param amp: amplitude of the wave
    :param rate: audio sample rate
    :returns: numpy.array -- evenly spaced sine wave values
    """
    t = linspace(0, duration, duration * rate)
    data = sin(2 * pi * freq * t) * amp
    return data

f = wave.open('tone.wav', 'w')
f.setparams((1, 2, 44100, 0, "NONE", "Uncompressed"))

# A 2-second 440 Hz tone
tone = note(440, 2)
f.writeframes(tone.astype(int16))
f.close()
