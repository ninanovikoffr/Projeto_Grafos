"""
PROJETO DE ALGORITMOS EM GRAFOS (GCC218)- Modelagem Logística com Grafos em Python

Alunas: Lana da Silva Miranda, Nina Tobias Novikoff da Cunha Ribeiro
___________________________________________________________________________________
"""

# LEITURA DO ARQUIVO DE ENTRADA
def ler_entrada(arq_entrada):

    # Dicionário para armazenar os dados do cabeçalho
    cabecalho = {}

    # Leitura do cabeçalho
    with open(arq_entrada, "r", encoding="utf-8") as arq:       # "r" modo de leitura (read)
        
        for _ in range(11):                                     # Já que todo cabeçalho tem 11 linhas
            linha = arq.readline().strip()                      # Strip pra remover espaços em branco e readline para ler a linha toda
            
            if ":" in linha:
                    chave, valor = linha.split(":", 1)          # split divide a linha uma vez em relação ao ":"
                    cabecalho[chave.strip()] = valor.strip()    # armazena no dicionário as duas partes da linha

    # print (cabecalho) # Para depuração

    # CRIANDO O GRAFO
    N = int (cabecalho['#Nodes'])
    grafo = [[None for _ in range(N + 1)] for _ in range(N + 1)]    # Ignorar o indice 0

    # Continuar a leitura a partir da linha 12
    with open(arq_entrada, "r", encoding="utf-8") as arq:
        linhas = arq.readlines()[11:]                           # Pula as 11 primeiras do cabeçalho

        tabela_atual = None                                     # para definir a categoria da tabela

        for linha in linhas:
            linha = linha.strip()
            if not linha or linha.startswith("the data is"):
                continue                                        # Se a linha estiver vazia ou for o "the data is based on...", pula a linha (continue).

            # Detectar qual tabela está lendo
            if linha.startswith("ReN."):                        # Define a categoria de acordo com o início da linha
                tabela_atual = 'ReN' # Nó obrigatório (required node)
                continue

            elif linha.startswith("ReE."):
                tabela_atual = 'ReE' # Aresta obrigatória (required edge)
                continue

            elif linha.startswith("ReA."):
                tabela_atual = 'ReA' # Arco obrigatório (required arc)
                continue

            elif linha.startswith("EDGE"): 
                tabela_atual = 'Edge' # Aresta não obrigatória
                continue

            elif linha.startswith("ARC"):
                tabela_atual = 'Arc' # Arco não obrigatória
                continue


            # Lendo as linhas com base na tabela
            if tabela_atual == 'ReE':

                # Definindo variáveis para armazenar as informações da linha da tabela
                _, noh_origem, noh_destino, custo_transito, demanda, custo_servico = linha.split()

                noh_origem, noh_destino = int(noh_origem), int(noh_destino)


                grafo[noh_origem][noh_destino] = {
                    'tipo': 'aresta',
                    'obrigatoria': True,
                    'custo_transito': int(custo_transito),
                    'demanda': int(demanda),
                    'custo_servico': int(custo_servico)
                }
                grafo[noh_destino][noh_origem] = grafo[noh_origem][noh_destino]  # Bidirecional porque é via de mão dupla

            if tabela_atual == 'Edge':

                _, noh_origem, noh_destino, custo_transito = linha.split()

                noh_origem, noh_destino = int(noh_origem), int(noh_destino)

                grafo[noh_origem][noh_destino] = {
                    'tipo': 'aresta',
                    'obrigatoria': False,
                    'custo_transito': int(custo_transito),
                    # Não tem demanda nem custo_serviço pois não é obrigatório
                }
                grafo[noh_destino][noh_origem] = grafo[noh_origem][noh_destino]  # Bidirecional porque é via de mão dupla   
                
            elif tabela_atual == 'ReA':

                _, noh_origem, noh_destino, custo_transito, demanda, custo_servico = linha.split()

                noh_origem, noh_destino = int(noh_origem), int(noh_destino)

                grafo[noh_origem][noh_destino] = {
                    'tipo': 'arco',
                    'obrigatoria': True,
                    'custo_transito': int(custo_transito),
                    'demanda': int(demanda),
                    'custo_servico': int(custo_servico)
                }
                # Não será bidirecional porque é via de mão única

            elif tabela_atual == 'Arc':

                _, noh_origem, noh_destino, custo_transito = linha.split()

                noh_origem, noh_destino = int(noh_origem), int(noh_destino)

                grafo[noh_origem][noh_destino] = {
                    'tipo': 'arco',
                    'obrigatoria': False,
                    'custo_transito': int(custo_transito),
                    # Não tem demanda nem custo_serviço pois não é obrigatório
                }
                # Não será bidirecional porque é via de mão única

            elif tabela_atual == 'ReN':

                nome_noh, demanda, custo_servico = linha.split()

                noh = int(nome_noh[1:])                             # tira o "N" e converte o número
        
                grafo[noh][noh] = {
                    'tipo': 'noh',
                    'obrigatoria': True,
                    # custo_transito não existe já refere-se ao próprio nó
                    'demanda': int(demanda),
                    'custo_servico': int(custo_servico)
                }

    return cabecalho, grafo

def imprimir_matriz(grafo):
    # Impressão da matriz de adjacência (valores de T. COST)
    print("\nMatriz de adjacência (valores de T. COST):\n")
    print("     ", end="")
    for j in range(1, len(grafo)):
        print(f"{j:>4}", end="")  # Alinhamento com 4 espaços
    print()

    # Separador
    print("    " + "----" * (len(grafo) - 1))

    # Linhas da matriz
    for i in range(1, len(grafo)):
        print(f"{i:>3} |", end="")  # Número da linha (nó)
        for j in range(1, len(grafo)):
            if grafo[i][j] is not None and 'custo_transito' in grafo[i][j]:
                print(f"{grafo[i][j]['custo_transito']:>4}", end="")
            else:
                print("   .", end="")  # Mostra ponto se não há ligação
        print()  # Quebra de linha para próxima linha da matriz

def quant_vertices(cabecalho):
    return int(cabecalho['#Nodes'])

def quant_arestas(cabecalho):
    return int(cabecalho['#Edges'])

def quant_arcos(cabecalho):
    return int(cabecalho['#Arcs'])

def quant_vertices_requeridos(cabecalho):
    return int(cabecalho['#Required N'])

def quant_arestas_requeridas(cabecalho):
    return int(cabecalho['#Required E'])

def quant_arcos_requeridos(cabecalho):
    return int(cabecalho['#Required A'])


def densidade_grafo (cabecalho):
    N = quant_vertices (cabecalho)
    E = quant_arestas (cabecalho)
    A = quant_arcos (cabecalho)

    return (E + A)/(N * (N-1))



