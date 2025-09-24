import os
from google import genai
import dotenv
from dotenv import load_dotenv
import e_mails
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

cliente = genai.Client()

def tratamento(emails):
    for numero, email in enumerate(emails):
        resposta = cliente.models.generate_content(
            model = "gemini-2.5-flash",
            contents = f'''Vou te enviar o corpo de um e-mail e quero que você resuma em 1 linha, 
                            definindo o intuito do e-mail. Segue e-mail: {email}'''
        )
        print(f"E-mail {numero + 1}: {resposta.text}")
        print("-"* 50)

tratamento(e_mails.lista_de_emails)