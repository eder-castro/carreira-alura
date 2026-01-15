lista_nomes = []
with open("arquivo_nomes.txt", "r", encoding="utf-8") as arq_nomes:
    for line in arq_nomes:
        lista_nomes.append(line.strip())

print(lista_nomes)