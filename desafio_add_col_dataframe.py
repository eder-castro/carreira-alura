import pandas as pd
import os
import time
from google import genai
import dotenv
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
cliente = genai.Client()

df_reviews_01 = pd.read_csv("reviews-01.csv",encoding="utf-8")
df_reviews_02 = pd.read_csv("reviews-02.csv",encoding="utf-8")

nova_coluna = []

def obter_sentimento(review):
    contador = 0
    for item in review:
        resposta = cliente.models.generate_content(
            model = "gemini-flash-lite-latest",
            contents = f'''Vou te enviar um review de um produto/servico e preciso que classifique o texto em 3 categorias: Positivo, Negativo ou Neutro. Nao quero justificativa, nao quero nenhum outro texto, o retorno deve ser somente uma das 3 palavras. Segue texto: {item}'''
        )
        #print("Esperando 5 segundos para não ser bloqueado pela API...\n")
        time.sleep(5)
        nova_coluna.append(resposta.text)
        contador += 1
        print(contador)
obter_sentimento(df_reviews_01.reviewText)
df_reviews_01["Sentimento"] = nova_coluna
print(df_reviews_01)
#obter_sentimento(df_reviews_02.reviewText)
#print(nova_coluna)