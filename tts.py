from google.cloud import texttospeech
import os


def speak(text):
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-F"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "llamachoptest-90319ad5895d.json"