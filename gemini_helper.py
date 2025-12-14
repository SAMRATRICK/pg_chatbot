import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # reads .env

def ask_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key is not configured on the server (env var missing)."

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Sorry, I had a problem contacting the Gemini service: {e}"
