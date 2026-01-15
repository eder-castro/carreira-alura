from google import genai
import time
import os
import dotenv
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

cliente = genai.Client()

lista_perguntas = []
with open("lista_perguntas.csv", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        lista_perguntas.append(linha.strip())
perguntas_e_respostas = []
def obter_respostas(lista_de_perguntas):
    for posicao, pergunta in enumerate(lista_de_perguntas, start=1):
        resposta = cliente.models.generate_content(
            model = "gemini-flash-lite-latest",
            contents = f'''Vou te enviar uma pergunta e quero que você obtenha a resposta e resuma em 1 linha. Segue pergunta: {pergunta}'''
        )
        #print("Esperando 60 segundos para não bloquear...\n")
        time.sleep(60)
        perguntas_e_respostas.append({f"Pergunta:":pergunta ,"Resposta:":resposta.text})
obter_respostas(lista_perguntas)
df_perguntas_e_respostas = pd.DataFrame(perguntas_e_respostas)
df_perguntas_e_respostas.to_csv("perguntas_e_respostas.csv",index="false", encoding="utf-8")
