# Python Keyboard
## Description
This Python app creates an audio file from a simple text representation of sheet music. The app currently supports mono (1 channel) and stereo (2 channel) audio.  
## Example Usage  
### Sheet Music  
A musical note and its timing (number of beats) are represented as a single line of text:  
> E4,qd  
> G4,e  
> ... 
> E4,qd  

Each note / timing pair is given as comma separated strings. The notes are defined using the standard names (E4, G4, etc.) and the timings are defined using abbreviations (h = 'half note', qd = 'dotted quarter note', etc.).  

Chords are also supported using the `+` operator to link multiple notes together:  
> C3+G3,w  
> C3+G#3,w  
> ...
> G2+F3,h  

Example sheet music files for a 2 channel version of 'Largo' from Dvorak's New World Symphony are provided in this repo: `largo_treble.txt` for the treble channel and `largo_bass.txt` for the bass channel.  

### Running the App  