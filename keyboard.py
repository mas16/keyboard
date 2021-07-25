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

import sys
import numpy as np
import utilities.utils as u
import utilities.functions as fu
from scipy.io import wavfile


def main():
    """
    Main function - generate the treble and bass channels then combined
    into a 2 channel .wav file
    """
    flag = []

    try:
        treble = fu.generate_wave(fu.generate_notes(u.treble_path))
    except FileNotFoundError:
        print(f'Warning: {u.treble_path} File Not Found')
        flag.append('t')
        treble = None
    else:
        print('treble:', len(treble))

    try:
        bass = fu.generate_wave(fu.generate_notes(u.bass_path))
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
