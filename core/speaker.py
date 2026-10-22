import asyncio
import os
import tempfile
import time

import edge_tts
import pygame


class FridaySpeaker:

    def __init__(self):
        self.voice = "en-US-AriaNeural"
        self.rate = "+20%"
        self.volume = "+0%"

        pygame.mixer.init()

    async def _generate_audio(self, text, output_file):
        communication = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume
        )

        await communication.save(output_file)

    def speak(self, text):
        audio_file = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            ) as temp_file:
                audio_file = temp_file.name

            asyncio.run(
                self._generate_audio(text, audio_file)
            )

            print(f"FRIDAY: {text}")

            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.unload()

        except Exception as error:
            print("Voice error:", error)

        finally:
            if audio_file and os.path.exists(audio_file):
                try:
                    os.remove(audio_file)
                except OSError:
                    pass

    def set_voice(self, voice_name):
        self.voice = voice_name

    def set_speed(self, speed):
        self.rate = speed

    def stop(self):
        pygame.mixer.music.stop()


if __name__ == "__main__":
    friday = FridaySpeaker()

    friday.speak(
        "Hello! I am Friday. Your assistant is ready."
    )