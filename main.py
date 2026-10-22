import speech_recognition as sr

from core.speaker import FridaySpeaker
from core.commands import execute_command
from gemini_ai import ask_gemini


class FridayAI:

    def __init__(self):
        self.speaker = FridaySpeaker()
        self.recognizer = sr.Recognizer()
        self.running = True

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("\nListening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=7
                )

            command = self.recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            command = command.lower().strip()
            print("You:", command)
            return command

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            print("Internet connection is required for voice recognition.")
            return ""

        except Exception as error:
            print("Listening error:", error)
            return ""

    def handle_command(self, command):
        command = command.strip().lower()

        if not command:
            return True

        # Wake word handling
        if "hey friday" in command:
            command = command.replace("hey friday", "", 1).strip()

            if not command:
                self.speaker.speak(
                    "Yes, Boss. I am listening. How can I help?"
                )

                command = self.listen()

                if not command:
                    return True

        # Try existing local commands first.
        # Gemini should only be used if the local handler
        # explicitly returns None for an unknown command.
        try:
            result = execute_command(command, self.speaker)
        except Exception as error:
            print("Local command error:", error)
            self.speaker.speak(
                "Sorry, there was a problem running that command."
            )
            return True

        if result is not None:
            return result

        # Unknown command: ask Gemini
        print("Friday is thinking...")

        answer = ask_gemini(command)

        if answer:
            print("Friday:", answer)
            self.speaker.speak(answer)
        else:
            self.speaker.speak(
                "Sorry, I could not get an answer right now."
            )

        return True

    def run(self):
        # Calibrate microphone once
        try:
            with sr.Microphone() as source:
                print("Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

        except Exception as error:
            print("Microphone setup error:", error)
            return

        self.speaker.speak(
            "Hello Boss! Friday is ready. Say Hey Friday."
        )

        print("\n================================")
        print("             FRIDAY AI")
        print("================================")
        print("Say: Hey Friday, open Google")
        print("Ask: Hey Friday, what is artificial intelligence?")
        print("Say: Exit Friday to stop.")
        print("Press Ctrl+C to stop manually.")

        while self.running:
            command = self.listen()

            if not command:
                continue

            result = self.handle_command(command)

            if not result:
                self.running = False

        print("FRIDAY AI stopped.")


if __name__ == "__main__":
    try:
        FridayAI().run()

    except KeyboardInterrupt:
        print("\nFRIDAY AI stopped.")