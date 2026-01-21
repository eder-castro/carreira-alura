from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
cont = 0
print("=== LISTA DE MODELOS ===")
# Removemos o filtro 'if' que estava dando erro
for modelo in client.models.list():
    cont +=1
    print(f"{cont} - Modelo: {modelo.name} - {modelo.input_token_limit}")