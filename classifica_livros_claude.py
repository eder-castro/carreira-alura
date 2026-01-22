from google import genai
import time
import os
import dotenv
from dotenv import load_dotenv
import pandas as pd

############################################  C  O  D  I  G  O    D  O    C  L  A  U  D  E  ####################################################


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
arquivo_csv = "livros_classificados.csv"

##### CRIA LISTA DE LIVROS #####
lista_livros = []

##### ABRE O ARQUIVO TXT E CARREGA NA LISTA DE LIVROS #####
with open("livros.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        lista_livros.append(linha.strip())

##### VERIFICA QUAIS LIVROS JÁ FORAM PROCESSADOS #####
livros_processados = set()
if os.path.exists(arquivo_csv):
    try:
        df_existente = pd.read_csv(arquivo_csv, encoding="utf-8")
        livros_processados = set(df_existente["Livro:"].tolist())
        print(f"Encontrados {len(livros_processados)} livros já processados. Continuando de onde parou...")
    except:
        print("Iniciando novo arquivo CSV...")

##### CRIA LISTA DE CLASSIFICACOES #####
classificacoes = []

##### CRIA FUNCAO PARA OBTER CATEGORIA DOS LIVROS #####
def obter_categorias(nome_do_livro):
    global contador
    if contador <= 19:
        cliente = cliente3
        print("Usando cliente 3")
    else:
        cliente = cliente4
        print("Usando cliente 4")
    
    resposta = cliente.models.generate_content(
        model = "gemini-1.5-flash",
        contents = f'''Vou te enviar o nome de um livro e quero que você obtenha a categoria deste livro em uma palavra. Você deve retornar somente a categoria, sem explicações nem textos adicionais.
        Exemplo:
        "Livro: A arte da guerra
        Resenha: AutoAjuda"
        Segue nome do livro: {nome_do_livro}'''
    )
    
    classificacoes[-1].update({f"Categoria:":resposta.text})

##### FUNCAO PARA SALVAR INCREMENTALMENTE NO CSV #####
def salvar_no_csv(dados):
    df_novo = pd.DataFrame([dados])
    
    # Se arquivo não existe, cria com cabeçalho
    if not os.path.exists(arquivo_csv):
        df_novo.to_csv(arquivo_csv, mode='w', index=False, encoding="utf-8")
    else:
        # Se existe, adiciona sem cabeçalho
        df_novo.to_csv(arquivo_csv, mode='a', header=False, index=False, encoding="utf-8")

##### CRIA FUNCAO PARA OBTER RESENHA DOS LIVROS #####
def obter_resenhas(lista_de_livros):
    global contador
    
    for livro in lista_de_livros:
        # Pula livros já processados
        if livro in livros_processados:
            print(f"Livro '{livro}' já processado. Pulando...")
            continue
        
        if contador <= 19:
            cliente = cliente1
            print("Usando cliente 1")
        else:
            cliente = cliente2
            print("Usando cliente 2")
        
        try:
            resposta = cliente.models.generate_content(
                model = "gemini-1.5-flash",
                contents = f'''Vou te enviar o nome de um livro e quero que você obtenha uma resenha curta, em no máximo 2 linhas. Você deve retornar somente a resenha, sem explicações nem textos adicionais.
                
                Exemplo:
                Livro: A arte da guerra
                Resenha: Um clássico atemporal sobre estratégia militar e filosofia, suas lições se aplicam a conflitos e à vida cotidiana com sabedoria duradoura

                Segue nome do livro: {livro}'''
            )
            
            for cont in range(60, -1, -1):
                print(f"{cont:02d}", end='\r', flush=True)
                time.sleep(1)
            
            # Cria dicionário com dados do livro
            classificacoes.append({f"Livro:":livro ,"Resenha:":resposta.text})
            
            # Obtém categoria
            obter_categorias(livro)
            
            # SALVA IMEDIATAMENTE NO CSV
            salvar_no_csv(classificacoes[-1])
            
            contador += 1
            print(f"Livro {contador} OK e salvo no CSV!")
            
        except Exception as e:
            print(f"Erro ao processar '{livro}': {e}")
            print("Dados já salvos estão preservados no CSV!")
            break

##### CHAMA A FUNCAO "OBTER RESENHAS"
obter_resenhas(lista_livros)

##### APOS FINALIZAR O PROCESSO, MOSTRA UM TEXTO INDICANDO QUE OS DADOS ESTAO NO ARQUIVO CRIADO
print(f'Processo finalizado! Resenhas e Classificações salvas em "{arquivo_csv}"')
print(f"Total de livros processados nesta execução: {contador}")