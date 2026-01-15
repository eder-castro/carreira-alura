import pandas as pd
from google import genai
#caminho = "./lista_medias.csv"
#df = pd.read_csv(caminho)
#print (df)

lista_perguntas = [
    "Qual time paulista é conhecido como o 'Timão'?",
    "Em que ano a Ponte Preta foi fundada?",
    "Qual é o mascote do Juventude?",
    "Qual estádio é a casa do Juventus?",
    "Quantos títulos da Libertadores o Cruzeiro já conquistou?",
    "Em que cidade fica a sede do Red Bull Bragantino?",
    "Qual é o maior rival do Corinthians?",
    "Qual o técnico que mais comandou o Pelé?",
    "Qual é a cor predominante no uniforme do Fluminense de feira?",
    "Qual o primeiro time paulista a vencer o Mundial de Clubes da FIFA?"
]

with open("lista_perguntas.csv", "w", encoding="utf-8") as arquivo:
    for pergunta in lista_perguntas:
        arquivo.write(pergunta + "\n")

df = pd.read_csv("./lista_perguntas.csv")
print(df)
