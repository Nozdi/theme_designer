"""
.. module:: sound
    :synopsis: This module provides sounds creation.
"""

from math import pi
from io import BytesIO
from numpy import linspace, int16, sin, concatenate
import wave


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
        while duration < 1.2:
            duration += 2*period

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


def create_sound(music_string):
    """
    :param music_string: string with sounds separated with space
    :returns: numpy.array -- concatenated wave
    """
    sounds = []
    for strnote in music_string.upper().strip().split():
        hz = OCTAVE.get(strnote)
        if hz:
            sounds.append(note(hz))
        else:
            pause = int(strnote)
            sounds.append(note(20, pause/500.))

    return concatenate(sounds)


def create_wav(filename, music_string):
    """
    :param filename: name of file where the wav will be saved
    :music_string: string with sounds separated with space
    """
    wave = create_sound(music_string)
    write_wave(filename, wave)


def get_sound_in_bytes(music_string):
    """
    :param music_string: string with sounds separated with space
    :returns: BytesIO -- file buffer with sound
    """
    wave = create_sound(music_string)
    sound_bytes = BytesIO()
    write_wave(sound_bytes, wave)
    sound_bytes.seek(0)
    return sound_bytes


if __name__ == '__main__':
    # create_wav("tone.wav", "G C G C G C G C D D D D G C")
    create_wav("tone.wav", "A C D C A A A A C D F G#")
    # sound_bytes = get_sound_in_bytes("C C# D D# E F F# 1000 G G# A A# B C1")
    # with open("tone.wav", "wb") as f:
    #     f.write(sound_bytes.read())
