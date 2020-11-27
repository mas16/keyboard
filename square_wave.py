import numpy as np
import utils as u
from scipy.io import wavfile
from frequencies import frequencies
from timing import fourfour as time_signature
import keyboard as kb

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
                 amplitude=1, decay=0.5, rate=u.rate):
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
        self.abs_val = None

    def generate_signal(self):
        """
        Generate the time domain complex representation of the note

        Assigns the array of complex values to self.signal
        Assigns the array of real values to self.real
        Assigns the array of imaginary values to self.imaginary
        """
        self.signal = self.amplitude * \
                      np.exp(1j*self.frequency * self.time_domain * 2.0*np.pi)

        if self.decay != 0:
            self.signal = self.signal * np.exp(self.time_domain*(-self.decay))

        self.real = np.real(self.signal)
        self.imaginary = np.imag(self.signal)

    def generate_square(self):
        """
        Generate the time domain complex representation of the note

        Assigns the array of complex values to self.signal
        Assigns the array of real values to self.real
        Assigns the array of imaginary values to self.imaginary
        """
        self.square= self.amplitude *\
                          np.sign(
                          np.sin(self.frequency*self.time_domain*2.0*np.pi))

        self.real = np.real(self.square)
        self.imaginary = np.imag(self.square)
        self.abs_val = np.abs(self.square)

    def generate_sawtooth(self):
        """
        Generate the time domain complex representation of the note

        Assigns the array of complex values to self.signal
        Assigns the array of real values to self.real
        Assigns the array of imaginary values to self.imaginary
        """
        self.sawtooth = self.amplitude * -2.0 / np.pi * \
                          np.arctan(1.0/np.tan(self.frequency*self.time_domain*2.0*np.pi))

        self.real = np.real(self.sawtooth)
        self.imaginary = np.imag(self.sawtooth)

    def generate_triangle(self):
        """
        Generate the time domain complex representation of the note

        Assigns the array of complex values to self.signal
        Assigns the array of real values to self.real
        Assigns the array of imaginary values to self.imaginary
        """
        self.triangle = np.abs(self.amplitude * -2.0 / np.pi * \
                          np.arctan(1.0/np.tan(self.frequency*self.time_domain*2.0*np.pi)))

        self.real = np.real(self.triangle)
        self.imaginary = np.imag(self.triangle)


test_path = u.treble_path
test = kb.SheetMusic(test_path)
test.read_music()
print(test.notes)

wave = np.array([])

notes = [['x','w']]

for bar in notes:

    temp = []

    for note in bar[0].split('+'):
        tone = Signal(note=note, rest=bar[1])
        tone.generate_square()
        if len(bar[0].split('+')) >1:
            temp.append(tone.square)
        else:
            wave = np.append(wave, tone.square)

    if  np.array(temp).ndim > 1:
        temp = np.vstack(temp)
        temp = np.sum(temp, axis=0)
        wave = np.append(wave, temp)

print(len(wave))
wavfile.write(u.output_path, u.rate, wave)