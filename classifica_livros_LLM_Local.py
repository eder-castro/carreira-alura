from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import time
load_dotenv()

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

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
    global contador
    ##### Chama o LLM passando o nome do livro e armazena o Genero devolvido na variavel "resposta"
    resposta = client_openai.chat.completions.create(
        model="google/gemma-3-4b",
        messages=[
            {"role": "system", "content":'''
            Vou te enviar o nome de um livro e quero que você obtenha o genero literario 
            deste livro em no maximo duas palavras.
            Você deve retornar somente a categoria, sem explicações nem textos adicionais.
            Exemplo:
            Livro: A arte da guerra
            Genero: AutoAjuda'''},
            {"role": "user", "content": f"Segue nome do livro: {nome_do_livro}"}
        ]
    )
    ##### Atualiza o último dicionário existente dentro da lista de dicionários com a chave-valor do genero
    classificacoes[-1].update({f"Gênero:":resposta.choices[0].message.content})
    ##### INCREMENTA CONTADOR E IMPRIME NUMERO DO LIVRO PROCESSADO
    #print(f"Livro {contador} OK!")
    print("Processando [","*" * contador," " * (len(lista_livros)-contador),"]", end='\r', flush=True)

##### CRIA FUNCAO PARA OBTER RESENHA DOS LIVROS #####
def obter_resenhas(lista_de_livros):
    global contador
    ##### Chama o LLM passando o nome do livro e armazena Resenha devolvida na variavel "resposta"
    for livro in lista_de_livros:
        contador+=1
        resposta = client_openai.chat.completions.create(
            model="google/gemma-3-4b",
            messages=[
                {"role": "system", "content":'''
                Vou te enviar o nome de um livro e quero que você obtenha uma resenha curta, 
                em no máximo 1 linha.
                Você deve retornar somente a resenha, sem título, sem explicações nem textos adicionais.
                Exemplo:
                Livro: A arte da guerra
                Resenha: Um clássico atemporal sobre estratégia militar e filosofia, 
                suas lições se aplicam a conflitos e à vida cotidiana com sabedoria duradoura.'''},
                {"role": "user", "content": f"Segue nome do livro: {livro}"}
            ]
        )
        ##### Insere um dicionário dentro da lista de dicionários com a chave-valor do nome do livro e a chave-valor da resenha
        classificacoes.append({f"Livro": livro, "Resenha": resposta.choices[0].message.content})
        ##### CHAMA A FUNCAO "OBTER CATEGORIAS"
        obter_categorias(livro)

# ##### CHAMA A FUNCAO "OBTER RESENHAS"
obter_resenhas(lista_livros)

# ##### TRANSFORMA A LISTA DE DICIONARIOS EM UM DATAFRAME
df_resenhas = pd.DataFrame(classificacoes)

# ##### EXPORTA O DATAFRAME PARA UM ARQUIVO CSV
df_resenhas.to_csv("livros_classificados.csv",index="false", encoding="utf-8")

# ##### APOS FINALIZAR O PROCESSO, MOSTRA UM TEXTO INDICANDO QUE OS DADOS ESTAO NO ARQUIVO CRIADO
print('Resenha e Classificação obtidas. Veja o resultado no arquivo "livros_classificados.csv"')

# ##### IMPRIME A LISTA DE DICIONARIOS COM NOME DOS LIVROS, RESENHAS E CLASSIFICACOES
# #print(classificacoes)