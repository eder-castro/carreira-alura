from google import genai
import time
import os
import dotenv
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
GOOGLE_API_KEY_01 = os.getenv("GEMINI_API_KEY_01")
GOOGLE_API_KEY_02 = os.getenv("GEMINI_API_KEY_02")

lista_livros = []
with open("livros.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        lista_livros.append(linha.strip())

classificacoes = []
def obter_resenhas(lista_de_livros):
    cliente = genai.Client(api_key=GOOGLE_API_KEY_01)
    cont = 0
    for livro in lista_de_livros:
        resposta = cliente.models.generate_content(
            model = "gemini-flash-lite-latest",
            contents = f'''Vou te enviar o nome de um livro e quero que você obtenha uma resenha curta, em no máximo 2 linhas. Você deve retornar somente a resenha, sem explicações nem textos adicionais.
            
            Exemplo:
            Livro: A arte da guerra
            Resenha: Um clássico atemporal sobre estratégia militar e filosofia, suas lições se aplicam a conflitos e à vida cotidiana com sabedoria duradoura

            Segue nome do livro: {livro}'''
        )
        print("Esperando 60 segundos para não bloquear...\n")
        time.sleep(60)
        classificacoes.append({f"Livro:":livro ,"Resenha:":resposta.text})
        cont+=1
        print(f"Livro {cont}")
        print(classificacoes)

obter_resenhas(lista_livros)
print("Resenhas OK")


def obter_categorias(lista_de_livros):
    cliente = genai.Client(api_key=GOOGLE_API_KEY_02)
    for livro in lista_de_livros:
        resposta = cliente.models.generate_content(
            model = "gemini-flash-lite-latest",
            contents = f'''Vou te enviar o nome de um livro e quero que você obtenha a categoria deste livro de forma sucinta. Você deve retornar somente a categoria, sem explicações nem textos adicionais.
            
            Exemplo:
            Livro: A arte da guerra
            Resenha: Auto-Ajuda

            Segue nome do livro: {livro}'''
        )
        print("Esperando 60 segundos para não bloquear...\n")
        time.sleep(60)
        classificacoes.append({f"Categoria:":resposta.text})
        print(classificacoes)

obter_categorias(lista_livros)
print("Categorias OK")

print(classificacoes)
df_resenhas = pd.DataFrame(classificacoes)
df_resenhas.to_csv("livros_classificados.csv",index="false", encoding="utf-8")
