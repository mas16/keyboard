import keyboard as kb
import numpy as np
import utils as u
from scipy.io import wavfile


chord = u.chord_path
print(chord)

with open(chord) as f:
    raw_music = f.read().split('\n')
    raw_music = [entry.split(',') for entry in raw_music if len(entry) > 0]


wave = np.array([])

for bar in raw_music:

    temp = []

    for note in bar[0].split('+'):
        tone = kb.Signal(note=note, rest=bar[1])
        tone.generate_signal()
        if len(bar[0].split('+')) >1:
            temp.append(tone.real)
        else:
            wave = np.append(wave, tone.real)

    if  np.array(temp).ndim > 1:
        temp = np.vstack(temp)
        temp = np.sum(temp, axis=0)
        wave = np.append(wave, temp)

print(len(wave))
wavfile.write(u.output_path, u.rate, wave)