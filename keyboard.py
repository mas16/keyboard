"""
Python Keyboard
by mas 2020-11-22

This python module will generate a 2 channel wav file
from "sheet music" that is provided by the user. The sheet music
must be formatted as follows:

        note_1,beats_1
        note_2,beats_2
        ...
        note_n,beats_n

    Example Sheet Music Format:
        G5,q
        G5,h
        C4,h
        F3,qd

Where the notes follow the conventional scale:
    C4, C#4, D4, ...
with corresponding frequencies (Hz) defined in frequencies.py
and the beats are defined in timing.py

Chords are defined using the "+" operator to join individual notes
For example:
    C4+G4+A4,w

Rests are designated with the note 'O'

***

Use utils.py to define the paths to the sheet music files
and the file path where the output .wav file is to be written

As of 2020-11-22
    Add exception handling for the following:
        - Incorrectly formatted sheet music
        - Unequal number of beats in each channel
"""

import numpy as np
import utils as u
import sys
from scipy.io import wavfile
import scipy.signal as ssg
from frequencies import frequencies
from timing import fourfour as time_signature


class SheetMusic:
    """
    SheetMusic class defines sheet music objects with the following
    instance attributes:

        path: str - file path to sheet music for easy documentation

        note: list - 2D matrix of notes and rests in format
                     [[note_1, rest_1], [note_2, rest_2], ...]
                     Initialized to None then read from sheet music file

    """
    def __init__(self, path):
        self.path = path
        self.notes = None

    def read_music(self):
        """
        Read sheet music file and store notes as matrix
        Assign notes to instance attribute self.notes
        """
        with open(self.path) as f:
            try:
                raw_music = f.read()
            except FileNotFoundError:
                print(f'Error: {self.path} Not Found')
                sys.exit()
            else:
                raw_music = raw_music.split('\n')
                self.notes = [entry.split(',') for entry in raw_music
                              if len(entry) > 0]


class Signal:
    """
    Signal class defines a signal object. A signal object is the
    mathematical representation of a note.

    Class attributes:

        frequencies: dict - All frequencies a signal can have

        time_sig: dict - The time signature that defines the beats of the
                         notes and rests

    Instance attributes:

        tempo: int - Beats per minute, used to calculate the beats

        amplitude: int - Starting volume of the note

        decay: float - R2 relaxation rate of the signal determines the
                       decay rate of the note back to volume of 0

        rate: int - Sampling rate of the single, defined in utils.py

        dwell: float - The spacing in time between notes

        frequency: float - Frequency of the note

        acq_time: float - Acquisition time or total duration of the note

        points: int - The number of points needed to digitize a signal

        time_domain: array - The time points where the signal is sampled

        signal: array - The complex time domain representation of the note

        real: array - The real component of signal

        imaginary: array - The imaginary component of the signal
    """
    # Class attributes
    frequencies: dict = frequencies
    time_sig = u.scale_time(time_signature, u.tempo)

    # Instance attributes
    def __init__(self, note, rest, tempo=u.tempo,
                 amplitude=10, decay=0.5, rate=u.rate):
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
        self.square = None
        self.sawtooth = None

    def generate_signal(self):
        """
        Generate the time domain complex representation of the note

        Assigns the array of complex values to self.signal
        Assigns the array of real values to self.real
        Assigns the array of imaginary values to self.imaginary
        """
        self.signal = self.amplitude * np.exp(1j*self.frequency *
                                              self.time_domain * 2.0*np.pi)

        if self.decay != 0:
            self.signal = self.signal * np.exp(self.time_domain*(-self.decay))

        self.real = np.real(self.signal)

        self.imaginary = np.imag(self.signal)

    def generate_square(self):
        """
        Generate the time domain representation of the note
        as square waveform
        """
        self.square = ssg.square(2*np.pi * self.frequency * self.time_domain)

        if self.decay != 0:
            self.square = self.square * np.exp(self.time_domain*(-self.decay))

    def generate_sawtooth(self):
        """
        Generate the time domain representation of the note
        as sawtooth waveform
        """
        self.sawtooth = ssg.sawtooth(2*np.pi *
                                     self.frequency * self.time_domain)

        if self.decay != 0:
            self.sawtooth = self.sawtooth * \
                            np.exp(self.time_domain*(-self.decay))


def generate_tone(bar):
    """
    Function used to generate the signal for each note

    :param bar: list, [note(s),beats]

    :return:
        tones: array - 1D array of real component of complex time domain
                       signal representation of the note
                       Special case of chords, the array is the sum of each
                       note's signal representation
    """
    tones = []

    for note in bar[0].split('+'):
        tone = Signal(note=note, rest=bar[1])
        tone.generate_square()
        tones.append(tone.square)

    if np.array(tones).ndim > 1:
        tones = np.vstack(tones)
        tones = np.sum(tones, axis=0)

    return tones


def generate_wave(music):
    """
    Function used to generate the .wav file. Concatenates each individual
    signal's real time domain series into one continuous vector.

    :param music: list - List of notes, beats

    :return:
        wave: array - 1D array of concatenated signal time domains
    """
    wave = np.array([])

    for bar in music:
        wave = np.append(wave, generate_tone(bar))

    return wave


def generate_notes(channel):
    """
    Function to create a SheetMusic object
    :
    param channel: str - path to sheet music file for each channel,
                         defined in utils.py
    :return:
        music.notes: list - instance attribute, list of notes, beats
    """
    music = SheetMusic(path=channel)
    music.read_music()
    return music.notes


def main():
    """
    Main function - generate the treble and bass channels then combined
    into a 2 channel .wav file
    """
    flag = []

    try:
        treble = generate_wave(generate_notes(u.treble_path))
    except FileNotFoundError:
        print(f'Warning: {u.treble_path} File Not Found')
        flag.append('t')
        treble = None
    else:
        print('treble:', len(treble))

    try:
        bass = generate_wave(generate_notes(u.bass_path))
    except FileNotFoundError:
        print(f'Warning: {u.bass_path} File Not Found')
        flag.append('b')
        bass = None
    else:
        print('bass', len(bass))

    if len(flag) == 2:
        print('ERROR: Cannot make wav from specified input files')
        sys.exit()

    elif len(flag) == 1:

        if flag[0] == 't':
            treble = np.zeros(len(bass))
            print('Warning: No treble channel can be generated')

        elif flag[0] == 'b':
            bass = np.zeros(len(treble))
            print('Warning: No bass channel can be generated')

    try:
        wavfile.write(u.output_path, u.rate, np.column_stack((treble, bass)))
    except ValueError:
        print("Error: Invalid tempo selected")
        sys.exit()


if __name__ == '__main__':
    main()
