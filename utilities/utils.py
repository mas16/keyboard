import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("-tr", "--treble",
                    dest="treble", help='Treble file')
parser.add_argument("-b", "--bass",
                    dest="bass", help='Bass file')
parser.add_argument("-t", "--tempo",
                    dest="tempo", default=120, help='Tempo in bpm', type=int)
parser.add_argument("-o", "--out",
                    dest="out", default="song.wav", help="Wav file name")

args = parser.parse_args()

# Tempo
tempo: int = args.tempo

# Output File
output_file: str = args.out

# Bass sheet music
bass_file: str = args.bass

# Treble sheet music
treble_file: str = args.treble

# Set working directory
base_path: str = os.getcwd()

# File path to bass sheet music file
bass_path = Path(base_path, bass_file)

# File path to treble sheet music file
treble_path = Path(base_path, treble_file)

# File path to output wav file
output_path = Path(base_path, output_file)

# Group channels
channels = [treble_path, bass_path]

# Digitization
rate = 2**16


def scale_time(dictionary, tempo_value):
    scale = 60 / tempo_value
    for key in dictionary.keys():
        dictionary[key] *= scale
    return dictionary
