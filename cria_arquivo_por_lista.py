lista_nomes = ["Eder", "Alvaro", "Adriano", "Vanderlei", "Goreti", "Irene","Pascoa", "Tina", "Rita", "Elena"]

with open("arquivo_nomes.txt", "w", encoding="utf-8") as arq_nomes:
    for nome in lista_nomes:
        arq_nomes.write(nome + "\n")