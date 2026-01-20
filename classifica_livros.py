from google import genai
import time
import os
import dotenv
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
GOOGLE_API_KEY_01 = os.getenv("GEMINI_API_KEY_01")
GOOGLE_API_KEY_02 = os.getenv("GEMINI_API_KEY_02")
GOOGLE_API_KEY_03 = os.getenv("GEMINI_API_KEY_02")
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

##### CRIA FUNCAO PARA OBTER CATEGORIA DOS LIVROS #####
def obter_categorias(nome_do_livro):
    ##### Se contador chegou a 19, usa outra chave de API
    global contador
    if contador <= 19:
        cliente = cliente3
    else:
        cliente = cliente4
    ##### Chama o LLM passando o nome do livro e armazena Categoria devolvida na variavel "resposta"
    resposta = cliente.models.generate_content(
        model = "gemini-flash-lite-latest",
        contents = f'''Vou te enviar o nome de um livro e quero que você obtenha a categoria deste livro em uma palavra. Você deve retornar somente a categoria, sem explicações nem textos adicionais.
        Exemplo:
        "Livro: A arte da guerra
        Resenha: AutoAjuda"
        Segue nome do livro: {nome_do_livro}'''
    )
    ##### Atualiza o último dicionário existente dentro da lista de dicionários com a chave-valor da categoria
    classificacoes[-1].update({f"Categoria:":resposta.text})

##### CRIA FUNCAO PARA OBTER RESENHA DOS LIVROS #####
def obter_resenhas(lista_de_livros):
    ##### Se contador chegou a 19, usa outra chave de API
    global contador
    if contador <= 19:
        cliente = cliente1
    else:
        cliente = cliente2
    ##### Chama o LLM passando o nome do livro e armazena Resenha devolvida na variavel "resposta"
    for livro in lista_de_livros:
        resposta = cliente.models.generate_content(
            model = "gemini-flash-lite-latest",
            contents = f'''Vou te enviar o nome de um livro e quero que você obtenha uma resenha curta, em no máximo 2 linhas. Você deve retornar somente a resenha, sem explicações nem textos adicionais.
            
            Exemplo:
            Livro: A arte da guerra
            Resenha: Um clássico atemporal sobre estratégia militar e filosofia, suas lições se aplicam a conflitos e à vida cotidiana com sabedoria duradoura

            Segue nome do livro: {livro}'''
        )
        ##### Exibe uma contagem regressiva na tela, aguardando para enviar requisicao ao LLM depois deste tempo, evitando estouro de cota
        for cont in range(30, -1, -1):
            print(f"{cont:02d}", end='\r', flush=True)
            time.sleep (1)

        ##### Insere um dicionário dentro da lista de dicionários com a chave-valor do nome do livro e a chave-valor da resenha
        classificacoes.append({f"Livro:":livro ,"Resenha:":resposta.text})
        ##### CHAMA A FUNCAO "OBTER CATEGORIAS"
        obter_categorias(livro)
        ##### INCREMENTA CONTADOR E IMPRIME NUMERO DO LIVRO PROCESSADO
        contador+=1
        print(f"Livro {contador} OK!")

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