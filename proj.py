"""
PROJETO DE ALGORITMOS EM GRAFOS (GCC218)- Modelagem Logística com Grafos em Python

Alunas: Lana da Silva Miranda, Nina Tobias Novikoff da Cunha Ribeiro
___________________________________________________________________________________
"""
# LEITURA DO ARQUIVO DE ENTRADA
arq_entrada = input("Digite o nome da instância: ")

# Dicionário para armazenar os dados do cabeçalho
cabecalho = {}

# Leitura do cabeçalho
with open(arq_entrada, "r", encoding="utf-8") as arq:       # "r" modo de leitura (read)
    
    for _ in range(11):                                     # Já que todo cabeçalho tem 11 linhas
        linha = arq.readline().strip()                      # Strip pra remover espaços em branco e readline para ler a linha toda
        
        if ":" in linha:
                chave, valor = linha.split(":", 1)          # split divide a linha uma vez em relação ao ":"
                cabecalho[chave.strip()] = valor.strip()    # armazena no dicionário as duas partes da linha

'''Para depuração:
print ("\n Cabeçalho extraído:")
for chave, valor in cabecalho.items(): # Retorna todos os pares chave-valor do dicionário como tuplas.
    print(f"{chave}: {valor}")'
'''
