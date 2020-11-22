import os
from pathlib import Path

# Tempo
tempo: int = 120

# Output File
output_file: str = 'chord_test.wav'

# Set working directory
base_path: str = os.getcwd()

# Bass sheet music
bass_file: str = 'tolb.txt'

# Treble sheet music
treble_file: str = 'tol3.txt'

# Chord sheet music
chord_file: str = 'chord.txt'

# File path to bass sheet music file
bass_path: str = Path(base_path, bass_file)

# File path to treble sheet music file
treble_path: str = Path(base_path, treble_file)

# File path to chord sheet music file
chord_path: str = Path(base_path, chord_file)

# File path to output wav file
output_path: str = Path(base_path, output_file)

channels = [treble_path, bass_path]

rate = 2048


def scale_time(dictionary, tempo_value):
    scale = 120.0 / tempo_value
    for key in dictionary.keys():
        dictionary[key] *= scale
    return dictionary
