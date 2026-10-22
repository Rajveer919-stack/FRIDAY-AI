import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def ask_gemini(question):
    """
    Send a question to Gemini and return its answer.
    Returns None if Gemini is unavailable.
    """

    if not client:
        return "Gemini API key nahi mili. Apni .env file check karo."

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You are Friday, a helpful Windows laptop voice assistant. "
                "Reply briefly and clearly. Use simple English unless the "
                "user asks in Hindi or Hinglish. Do not claim you performed "
                "computer actions unless a local command actually did them.\n\n"
                f"User: {question}"
            ),
        )

        answer = response.text

        if answer:
            return answer.strip()

        return "Sorry Boss, mujhe abhi jawab nahi mila."

    except Exception as error:
        print("Gemini error:", error)
        return "Boss Gemini se connect nahi ho pa raha. Internet aur API settings check karo."