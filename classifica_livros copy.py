from google import genai
import time
import os
import json
import dotenv
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
GOOGLE_API_KEY_01 = os.getenv("GEMINI_API_KEY_01")
GOOGLE_API_KEY_02 = os.getenv("GEMINI_API_KEY_02")
GOOGLE_API_KEY_03 = os.getenv("GEMINI_API_KEY_03")
GOOGLE_API_KEY_04 = os.getenv("GEMINI_API_KEY_04")

cliente1 = genai.Client(api_key=GOOGLE_API_KEY_01)
cliente2 = genai.Client(api_key=GOOGLE_API_KEY_02)
cliente3 = genai.Client(api_key=GOOGLE_API_KEY_03)
cliente4 = genai.Client(api_key=GOOGLE_API_KEY_04)

contador = 0
##### CRIA LISTA DE LIVROS #####
lista_livros = []

##### ABRE O ARQUIVO TXT E CARREGA NA LISTA DE LIVROS #####
with open("livros.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        lista_livros.append(linha.strip())

##### CRIA LISTA DE CLASSIFICACOES #####
classificacoes = []

##### CRIA FUNCAO PARA OBTER RESENHA DOS LIVROS #####
def obter_resenhas(lista_de_livros):
    ##### Se contador chegou a 19, usa outra chave de API
    global contador
    if contador <= 19:
        cliente = cliente2
    else:
        cliente = cliente1
    ##### Chama o LLM passando o nome do livro e armazena Resenha e Genero obtidos na variavel "resposta"
    for livro in lista_de_livros:
        ##### INCREMENTA CONTADOR E IMPRIME NUMERO DO LIVRO A SER PROCESSADO
        contador+=1
        print(f"Analisando Livro {contador}!")
        resposta = cliente.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = f'''Vou te enviar o nome de um livro e quero que você obtenha:
            1 - uma resenha curta do livro, em no máximo 1 linha. Você deve retornar somente a resenha, sem explicações nem textos adicionais.
            Exemplo: Um clássico atemporal sobre estratégia militar e filosofia, suas lições se aplicam a conflitos e à vida cotidiana com sabedoria duradoura.
            2 - o genero literário deste livro em uma palavra. Você deve retornar somente o genero literário, sem explicações nem textos adicionais.
            Exemplos: Romance, Biografia, Suspense, Autoajuda
            Segue nome do livro: {livro}
            Retorne APENAS um objeto JSON neste formato exato, sem Markdown:
            {{
                "livro": "{livro}"
                "resenha": "texto aqui",
                "classificacao": "texto aqui"
            }}'''
        )

        ##### Exibe uma contagem regressiva na tela, aguardando para enviar requisicao ao LLM depois deste tempo, evitando estouro de cota
        for cont in range(15, -1, -1):
            print(f"{cont:02d}", end='\r', flush=True)
            time.sleep (1)

        ##### Insere um dicionário dentro da lista de dicionários com a chave-valor do nome do livro, chave-valor da resenha e chave-valor do genero
        print(resposta.text)
        resultado = json.loads(resposta.text)
        classificacoes.append(resultado)
        
        print(classificacoes)
        print(f"Informações do Livro {contador} Obtidas!")

##### CHAMA A FUNCAO "OBTER RESENHAS"
obter_resenhas(lista_livros)

##### TRANSFORMA A LISTA DE DICIONARIOS EM UM DATAFRAME
df_resenhas = pd.DataFrame(classificacoes)

##### EXPORTA O DATAFRAME PARA UM ARQUIVO CSV
df_resenhas.to_csv("livros_classificados.csv",index="false", encoding="utf-8")

##### APOS FINALIZAR O PROCESSO, MOSTRA UM TEXTO INDICANDO QUE OS DADOS ESTAO NO ARQUIVO CRIADO
print('Resenha e Classificação obtidas. Veja o resultado no arquivo "livros_classificados.csv"')

##### IMPRIME A LISTA DE DICIONARIOS COM NOME DOS LIVROS, RESENHAS E CLASSIFICACOES
#print(classificacoes)