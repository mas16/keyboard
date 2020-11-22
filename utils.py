import os
from pathlib import Path

# Tempo
tempo: int = 175

# Output File
output_file: str = 'test.wav'

# Set working directory
base_path: str = os.getcwd()

# Bass sheet music
bass_file: str = 'tolb.txt'

# Treble sheet music
treble_file: str = 'tol3.txt'

# File path to bass sheet music file
bass_path: str = Path(base_path, bass_file)

# File path to treble sheet music file
treble_path: str = Path(base_path, treble_file)

# File path to output wav file
output_path: str = Path(base_path, output_file)

channels = [treble_path, bass_path]

rate = 2048


def scale_time(dictionary, tempo_value):
    scale = 120.0 / tempo_value
    for key in dictionary.keys():
        dictionary[key] *= scale
    return dictionary
