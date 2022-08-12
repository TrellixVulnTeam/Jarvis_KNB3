import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv
import os
  
# Sampling frequency 
freq = 44100
  
# Recording duration 
duration = 5
  
# Start recorder with the given values  
# of duration and sample frequency
def audio_rec():
    recording = sd.rec(int(duration * freq),  
                       samplerate=freq, channels=2) 
      
    # Record audio for the given number of seconds 
    sd.wait() 
      
    # This will convert the NumPy array to an audio 
    # file with the given sampling frequency 
    write("recording0.wav", freq, recording) 
      
    # Convert the NumPy array to audio file
    try:
        os.system("mkdir tmp")
    except:
        pass
    wv.write("tmp/recording1.wav", recording, freq, sampwidth=2)