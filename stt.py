import sounddevice as sd
from scipy.io.wavfile import write

def listen():
    fs = 44100  # Sample rate
    seconds = 10  # Duration of recording

    print("Recording...")

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('speech.wav', fs, myrecording)  # Save as WAV file