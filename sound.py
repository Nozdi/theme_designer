"""
.. module:: sound
    :synopsis: This module provides sounds creation.
"""

from math import pi
import wave
from numpy import linspace, int16, sin, concatenate, arcsin


SAMPLE_RATE = 44100

OCTAVE = {
    "C": 261.626,
    "C#": 277.183,
    "D": 293.665,
    "D#": 311.127,
    "E": 329.628,
    "F": 349.228,
    "F#": 369.994,
    "G": 391.995,
    "G#": 415.305,
    "A": 440.000,
    "A#": 466.164,
    "B": 493.883,
    "C1": 523.251,
}


def note(freq, duration=0, amp=10000):
    """
    :param freq: frequency of the wave.
    :param duration: duration of the sound in seconds.
    :param amp: amplitude of the wave
    :returns: numpy.array -- evenly spaced sine wave values
    """
    if not duration:
        period = 1/freq
        while duration < 1.5:
            duration += period

    t = linspace(0, duration, duration * SAMPLE_RATE)
    data = sin(2 * pi * freq * t) * amp

    return data


def write_wave(filename, sample_array):
    """
    :param filename: name of wave
    :param sample_array: array with sound
    """
    f = wave.open(filename, 'w')
    f.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "Uncompressed"))
    f.writeframes(sample_array.astype(int16))
    f.close()


def create_sound(wave_string):
    """
    :param wave_string: string with sounds separated with space
    """
    sounds = []
    for strnote in wave_string.strip().split():
        hz = OCTAVE.get(strnote)
        if hz:
            sounds.append(note(hz))
        else:
            pause = int(strnote)
            sounds.append(note(0, pause/500.))

    wave = concatenate(sounds)
    write_wave("tone.wav", wave)


if __name__ == '__main__':
    create_sound("C C# D D# E F F# G G# A A# B C1")
