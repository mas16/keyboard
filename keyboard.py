"""
python keyboard

by matt stetz
2020.11
"""

import numpy as np
import utils
from scipy.io import wavfile
from frequencies import frequencies
from timing import fourfour as time_signature


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
    time_sig = utils.scale_time(time_signature, utils.tempo)

    # Instance attributes
    def __init__(self, note: list, tempo=utils.tempo,
                 amplitude=100, decay=0.5, rate=utils.rate):
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
        self.imaginary = None

    def generate_signal(self):
        self.signal = self.amplitude \
                     * np.exp(1j*self.frequency * self.time_domain * 2.0*np.pi)

        if self.decay != 0:
            self.signal = self.signal * np.exp(self.time_domain*(-self.decay))

        self.real = np.real(self.signal)
        self.imaginary = np.imag(self.signal)


def generate_tone(note):
    tone = Signal(note)
    tone.generate_signal()
    return tone.real


def generate_wave(notes):
    wave = np.array(0)
    for note in notes:
        wave = np.append(wave, generate_tone(note))
    return wave


def generate_notes(channel):
    music = SheetMusic(path=channel)
    notes = music.read_music()
    return notes


def main():
    treble = generate_wave(generate_notes(utils.treble_path))
    bass = generate_wave(generate_notes(utils.bass_path))
    wavfile.write(utils.output_path, utils.rate,
                  np.column_stack((treble, bass)))


if __name__ == '__main__':
    main()
