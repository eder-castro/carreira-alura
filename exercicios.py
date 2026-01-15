'''
-Configure a estrutura de repetição for para iterar sobre listas e dicionários;
-Imprima cada item de uma lista individualmente;
-Utilize o operador += para atualizar índices em loops;
'''
frutas = ['maçã', 'banana', 'cereja', 'pera', 'laranja', 'uva', 'manga']
for fruta in frutas:
    print(fruta)

for i in range(len(frutas)):
    print(f'Índice {i}: {frutas[i]}')
i = 0
print('------------------')
while i < len(frutas):
    print(f'Fruta {i+1}: {frutas[i]}')
    i += 1
'''
-Percorra dicionários exibindo chaves e pares chave-valor;
'''
print('------------------')
pessoa = {'nome': 'Ana', 'idade': 28, 'cidade': 'São Paulo'}
for chave in pessoa:
    print(f'Chave: {chave}, Valor: {pessoa[chave]}')
print('------------------')
'''
-Gere sequências numéricas com a função range;
'''
for num in range(5):
    print(num+1)
print('------------------')
'''
-Valide números pares usando a operação de resto (%);
'''
for num in range(10):
    if (num + 1) % 2 == 0:
        print(f'{num + 1} é par')
    else:
        print(f'{num + 1} é ímpar')
print('------------------')

'''
-Crie funções para processar strings com strip, upper e replace;
-Aplique o método split para eliminar espaços extras;
-Reúna as palavras com o método join para formatar textos;
-Implemente funções que retornem valores processados;
-Integre a correção de nomes com funções personalizadas;
-Padronize diferentes textos usando a função criada;
-Utilize random.choice para alocar elementos de forma aleatória;
-Monte dicionários contendo nomes corrigidos e dados associados;
-Crie uma função que percorra uma lista de e-mails com for;
-Faça chamadas de API para resumir o conteúdo de e-mails;
-Empregue f-strings para formatar os resumos dinamicamente;
-Utilize enumerate para numerar os e-mails na iteração;
-Teste a função e verifique a saída dos resumos com separadores.
'''