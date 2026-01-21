from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY_01 = os.getenv("GEMINI_API_KEY_01")
GOOGLE_API_KEY_02 = os.getenv("GEMINI_API_KEY_02")

cliente1 = genai.Client(api_key=GOOGLE_API_KEY_01)
cliente2 = genai.Client(api_key=GOOGLE_API_KEY_02)

print("Modelos disponíveis para você:")
for model in cliente1.models.list():
    if "flash" in model.name:
        print(f"- {model.name}") # Copie o nome que aparecer aqui (ex: models/gemini-3.0-flash)