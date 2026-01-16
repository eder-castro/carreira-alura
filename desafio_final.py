#1-Carregar un arquivo .txt, onde cada linha será um elemento de uma lista do Python
#2-Mandar a lista para um modelo local retornar lista de dicionarios com:
    #usuario, resenha original, resenha pt, avaliacao (positiva, negativa, neutra)
#3-Transformar resposta em uma lista de dicionarios Python
#4-Criar funcao que dada a lista de dicionarios, percorre a lista e:
    #Conta a quantidade de avaliacoes positivas
    # Une cada item da lista em uma variavel tipo string com algum separador
# Ao final retorna a quantidade e a variavel do passo 4 
from openai import OpenAI
import os
import pandas as pd

### Importando o arquivo .txt para dentro de um dataframe pandas
df_resenhas = pd.read_csv('resenhas.txt', sep='$', names=['ID', 'USER', "RESENHA"], encoding="utf-8")
#print(df_resenhas)
coluna_resenhas = df_resenhas["RESENHA"]
#print(coluna_resenhas)

nova_coluna = []

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def obter_classificacoes(resenhas):
    for linha in resenhas:
        retorno_llm = client_openai.chat.completions.create(
            model="google/gemma-3-4b",
            messages=[{"role": "user",
                "content":f"Vou te enviar uma lista de resenhas sobre produtos ou serviços e preciso que você classifique o texto em 3 categorias: Positivo, Neutro ou Negativo. Na dúvida, use 'NEUTRO'. Não quero justificativa, não quero nenhum outro texto, o retorno deve ser somente uma das 3 palavras. Segue lista: {linha}"
            }],
        )
        nova_coluna.append(retorno_llm.choices[0].message.content.strip())

obter_classificacoes(coluna_resenhas)
#print(nova_coluna)
df_resenhas["AVALIACAO"] = nova_coluna
print(df_resenhas)
