'''
python keyboard

by matt stetz
2020.11
'''

import numpy as np
import scipy as sp
import os
import sys
from scipy.io import wavfile
from scipy.fftpack import fft
from pathlib import Path
from frequencies import frequencies
from timing import fourfour as time_signature

# Set working directory
base_path: str = os.getcwd()

bass_file: str = 'tolb.txt'
treble_file: str = 'tol3.txt'

bass_path: str = Path(base_path, bass_file)
treble_path: str = Path(base_path, treble_file)

tempo: int = 175

def scale_time(dictionary, tempo=tempo):
    scale = 120.0 / tempo
    for key in dictionary.keys():
        dictionary[key] *= scale
    return dictionary


class SheetMusic:
    def __init__(self, path):
        self.path = path

    def read_music(self):
        with open(self.path) as f:
            raw_music = f.read()
            raw_music = raw_music.split('\n')
            notes = [entry.split(',') for entry in raw_music if len(entry) > 0]
        return notes


class Signal:

    # Class attributes
    frequencies: dict = frequencies

    # 4/4 as default
    time_sig = scale_time(time_signature)

    # Instance attributes
    def __init__(self, note: list, tempo: int,
                 amplitude=100, decay=0.5, rate=2048):
        self.tempo = tempo
        self.amplitude = amplitude
        self.decay = decay
        self.rate = rate
        self.dwell = 1 / rate
        self.frequency = self.frequencies[note[0]]
        self.acq_time = self.time_sig[note[1]]
        self.points = self.acq_time / self.dwell
        self.time_domain = np.linspace(0, self.acq_time, self.points)
        self.signal = None
        self.real = None
        self.complex = None


    def generate_signal(self):
        self.signal = self.amplitude \
                     * np.exp(1j*self.frequency * self.time_domain * 2.0*np.pi)

        if self.decay != 0:
            self.signal = self.signal * np.exp(self.time_domain*(-self.decay))

        self.real = np.real(self.signal)
        self.imaginary = np.imag(self.signal)



music = SheetMusic(path=treble_file)
notes = music.read_music()
wave = np.empty(0)


def generate_tone(note, tempo=tempo):
    tone = Signal(note, tempo=tempo)
    tone.generate_signal()
    return tone.real


for note in notes:
    wave = np.append(wave, generate_tone(note))

out = os.path.join(base_path, 'test.wav')

wavfile.write(out, 2048, wave)
