# Python Keyboard
## Description
This Python app creates an audio file from a simple text representation of sheet music. The app currently supports mono (1 channel) and stereo (2 channel) audio.  
## Example Usage  
### Sheet Music  
A musical note and its timing (number of beats) are represented as a single line of text:  
> E4,qd  
> G4,e   
> E4,qd  

Each note / timing pair is given as comma separated strings. The notes are defined using the standard names (E4, G4, etc.) and the timings are defined using abbreviations (h = 'half note', qd = 'dotted quarter note', etc.).  

Chords are also supported using the `+` operator to link multiple notes together:  
> C3+G3,w  
> C3+G#3,w  
> G2+F3,h  

Example sheet music files for a 2 channel version of 'Largo' from Dvorak's New World Symphony are provided in this repo: `largo_treble.txt` for the treble channel and `largo_bass.txt` for the bass channel.  

### Running the App
Clone this repo and run the app from the command line. To ensure proper functionality, first create a virtual environment using the `py36_env.yml` file. If using Anaconda:    
> ```conda env create -f py36_env.yml```  

Then activate the environment:  
> ```conda activate py36```  

Run the app using the command line:  
> ```python keyboard.py -tr largo_treble.txt -b largo_bass.txt -o largo.wav```  

The complete list of command line arguments is shown below:
> `-tr` : Path to treble sheet music file  
> `-b` : Path to bass sheet music file  
> `-o`: File name for output `.wav` file (include `.wav` extension)  
> `-t`: Tempo (default is 120 bpm)
