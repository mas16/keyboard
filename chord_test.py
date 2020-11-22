import keyboard as kb
import numpy as np
import utils as u
from scipy.io import wavfile


chord = u.chord_path

with open(chord) as f:
    raw_music = f.read().split('\n')
    raw_music = [entry.split(',') for entry in raw_music if len(entry) > 0]

print(raw_music)

wave = np.array([])
for bar in raw_music:
    temp = np.zeros(2*u.rate)
    for note in bar[0].split('+'):
        tone = kb.Signal(note=note, rest=bar[1])
        tone.generate_signal()
        temp += tone.real
    wave = np.append(wave, temp)

wavfile.write(u.output_path, u.rate, wave)