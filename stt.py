import pyaudio
from scipy.io.wavfile import write
import numpy as np
import keyboard
import time
import openai
import wave

def listen():
    # this function needs to record audio when a keybind is pressed
    # and then save it to a file. That file will then be sent to whisper for
    # speech to text
    print("Listening...")
    while True:
            keyboard.wait('`')
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            WAVE_OUTPUT_FILENAME = "speech.wav"
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
            frames = []
            
            print("Recording...")

            while keyboard.is_pressed('`'):
                # record audio
                data = stream.read(CHUNK)
                frames.append(data)
            
            print("Done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            return send_to_whisper()

def send_to_whisper():
    # this function will send the audio file to whisper for speech to text
    # and then return the text to the main function
    print("Sending to whisper...")
    audio_file = open("speech.wav", "rb")
    try:
        response = openai.Audio.transcribe("whisper-1",audio_file)
        response['voice'] = True
        # print(response)
        return response
    except:
        print("Error: Whisper is not responding. Please try again later.")
        return

