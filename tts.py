from google.cloud import texttospeech
import vlc
import asyncio
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "llamachoptest-90319ad5895d.json"

class TTS:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.media = vlc.MediaPlayer()
        self.queue = asyncio.Queue()
        self.processing = False
        print("TTS initialized")

    async def add_text(self, text):
        await self.queue.put(text)
        print(f"Added to queue: {text}")
        print(self.queue)
        if not self.processing:
            print("Processing queue")
            self.processing = True
            asyncio.create_task(self.process_queue())

    async def process_queue(self):
        print("que not while")

        while not self.queue.empty():
            print("que while")
            text = await self.queue.get()
            print(f"Processing: {text}")

            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Neural2-F"
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            with open("output.mp3", "wb") as out:
                out.write(response.audio_content)
                print("Audio content written to file 'output.mp3'")

            self.media.stop()
            self.media.set_media(vlc.Media("output.mp3"))
            self.media.play()

            media_length = self.media.get_length() / 1000
            asyncio.sleep(media_length)

            while self.media.get_state() == vlc.State.Playing:
                await asyncio.sleep(0.1)

            self.queue.task_done()

        print(self.processing)
        self.processing = False
        print(self.processing)

