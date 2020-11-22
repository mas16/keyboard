"""
python keyboard

by matt stetz
2020.11
"""

import numpy as np
import utils as u
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
    time_sig = u.scale_time(time_signature, u.tempo)

    # Instance attributes
    def __init__(self, note, rest, tempo=u.tempo,
                 amplitude=100, decay=0.5, rate=u.rate):
        self.tempo = tempo
        self.amplitude = amplitude
        self.decay = decay
        self.rate = rate
        self.dwell = 1 / rate
        self.frequency = self.frequencies[note]
        self.acq_time = self.time_sig[rest]
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


def generate_tone(bar):
    tones = []
    for note in bar[0].split('+'):
        tone = Signal(note=note, rest=bar[1])
        tone.generate_signal()
        tones.append(tone.real)
    if np.array(tones).ndim > 1:
        tones = np.vstack(tones)
        tones = np.sum(tones, axis=0)
    return tones


def generate_wave(music):
    wave = np.array([])
    for bar in music:
        wave = np.append(wave, generate_tone(bar))
    return wave


def generate_notes(channel):
    music = SheetMusic(path=channel)
    notes = music.read_music()
    return notes


def main():
    treble = generate_wave(generate_notes(u.treble_path))
    bass = generate_wave(generate_notes(u.bass_path))
    wavfile.write(u.output_path, u.rate,
                  np.column_stack((treble, bass)))


if __name__ == '__main__':
    main()
