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

# Set working directory
base_path: str = os.getcwd()
music_file: str = 'song.txt'
music_path: str = Path(base_path, music_file)

