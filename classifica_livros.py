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
def obter_categorias(nome_do_livro):
    cliente = genai.Client(api_key=GOOGLE_API_KEY_02)
    resposta = cliente.models.generate_content(
        model = "gemini-flash-lite-latest",
        contents = f'''Vou te enviar o nome de um livro e quero que você obtenha a categoria deste livro em uma palavra. Você deve retornar somente a categoria, sem explicações nem textos adicionais.
        
        Exemplo:
        Livro: A arte da guerra
        Resenha: AutoAjuda

        Segue nome do livro: {nome_do_livro}'''
    )
    #print("Esperando 60 segundos para não bloquear...\n")
    #time.sleep(30)
    classificacoes[-1].update({f"Categoria:":resposta.text})

def obter_resenhas(lista_de_livros):
    cliente = genai.Client(api_key=GOOGLE_API_KEY_01)
    conta = 0
    for livro in lista_de_livros:
        resposta = cliente.models.generate_content(
            model = "gemini-flash-lite-latest",
            contents = f'''Vou te enviar o nome de um livro e quero que você obtenha uma resenha curta, em no máximo 2 linhas. Você deve retornar somente a resenha, sem explicações nem textos adicionais.
            
            Exemplo:
            Livro: A arte da guerra
            Resenha: Um clássico atemporal sobre estratégia militar e filosofia, suas lições se aplicam a conflitos e à vida cotidiana com sabedoria duradoura

            Segue nome do livro: {livro}'''
        )
        #print("Esperando 30 segundos para não bloquear...\n")
        for cont in range(30, -1, -1):
            print(f"{cont:02d}", end='\r', flush=True)
            time.sleep (1)
        #time.sleep(30)
        classificacoes.append({f"Livro:":livro ,"Resenha:":resposta.text})
        obter_categorias(livro)
        conta+=1
        print(f"Livro {conta} OK!")
        #print("OK")
print(classificacoes)

obter_resenhas(lista_livros)
print('Resenha e Classificação obtidas. Veja o resultado no arquivo "livros_classificados.csv"')

#print(classificacoes)
df_resenhas = pd.DataFrame(classificacoes)
df_resenhas.to_csv("livros_classificados.csv",index="false", encoding="utf-8")
