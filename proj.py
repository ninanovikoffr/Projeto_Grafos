"""
PROJETO DE ALGORITMOS EM GRAFOS (GCC218)- Modelagem Logística com Grafos em Python

Alunas: Lana da Silva Miranda, Nina Tobias Novikoff da Cunha Ribeiro
___________________________________________________________________________________
"""

import csv
import pandas as pd
import os
import time


# Tratamento de erro
def transforma(valor):
    # Tenta converter para inteiro ou retorna 0. Evita quebras em campos mal formatados.
    
    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0

# Leitura de arquivo de entrada .dat 
def ler_entrada(arq_entrada):

    '''
    * Lê arquivos .dat com dados de grafos logísticos.
    * Identifica e organiza os elementos:

    * ReN. = nós obrigatórios com demanda
    * ReE. = arestas obrigatórias (bidirecionais)
    * ReA. = arcos obrigatórios (direcionais)
    * EDGE = arestas opcionais
    * ARC = arcos opcionais
    * Armazena tudo em uma matriz grafo[i][j] com listas de dicionários descrevendo conexões.
    '''

    cabecalho = {}

    # Leitura do cabeçalho
    with open(arq_entrada, "r", encoding="utf-8") as arq:
        for _ in range(11):
            linha = arq.readline().strip()
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                cabecalho[chave.strip()] = valor.strip()

    N = int(cabecalho['#Nodes'])
    grafo = [[[] for _ in range(N + 1)] for _ in range(N + 1)]

    with open(arq_entrada, "r", encoding="utf-8") as arq:
        linhas = arq.readlines()[11:]

        tabela_atual = None

        for linha in linhas:
            linha = linha.strip()
            if not linha or linha.startswith("the data is"):
                continue

            # Detectar seção atual
            if linha.startswith("ReN."):
                tabela_atual = 'ReN'
                continue
            elif linha.startswith("ReE."):
                tabela_atual = 'ReE'
                continue
            elif linha.startswith("ReA."):
                tabela_atual = 'ReA'
                continue
            elif linha.startswith("EDGE"):
                tabela_atual = 'Edge'
                continue
            elif linha.startswith("ARC"):
                tabela_atual = 'Arc'
                continue

            partes = linha.split()
            try:
                if tabela_atual == 'ReE' and len(partes) == 6:
                    _, u, v, custo, demanda, servico = partes
                    u, v = int(u), int(v)
                    aresta = {
                        'tipo': 'aresta',
                        'obrigatoria': True,
                        'custo_transito': int(custo),
                        'demanda': int(demanda),
                        'custo_servico': int(servico)
                    }
                    grafo[u][v].append(aresta)
                    grafo[v][u].append(aresta)

                elif tabela_atual == 'Edge' and len(partes) == 4:
                    _, u, v, custo = partes
                    u, v = int(u), int(v)
                    aresta = {
                        'tipo': 'aresta',
                        'obrigatoria': False,
                        'custo_transito': int(custo)
                    }
                    grafo[u][v].append(aresta)
                    grafo[v][u].append(aresta)

                elif tabela_atual == 'ReA' and len(partes) == 6:
                    _, u, v, custo, demanda, servico = partes
                    u, v = int(u), int(v)
                    arco = {
                        'tipo': 'arco',
                        'obrigatoria': True,
                        'custo_transito': int(custo),
                        'demanda': int(demanda),
                        'custo_servico': int(servico)
                    }
                    grafo[u][v].append(arco)

                elif tabela_atual == 'Arc' and len(partes) == 4:
                    _, u, v, custo = partes
                    u, v = int(u), int(v)
                    arco = {
                        'tipo': 'arco',
                        'obrigatoria': False,
                        'custo_transito': int(custo)
                    }
                    grafo[u][v].append(arco)

                elif tabela_atual == 'ReN' and len(partes) == 3:
                    nome_no, demanda, servico = partes
                    noh = int(nome_no[1:])
                    grafo[noh][noh].append({
                        'tipo': 'noh',
                        'obrigatoria': True,
                        'demanda': int(demanda),
                        'custo_servico': int(servico)
                    })

            except Exception as e:
                print(f"⚠ Erro ao processar linha da tabela {tabela_atual}: {linha}")
                print(f"   Detalhes: {e}")

    return cabecalho, grafo


# Funçoes auxiliares extraem e limpam os dados do cabeçalho do arquivo .dat.
def quant_vertices(cabecalho):
    return transforma(cabecalho.get('#Nodes'))

def quant_arestas(cabecalho):
    return transforma(cabecalho.get('#Edges'))

def quant_arcos(cabecalho):
    return transforma(cabecalho.get('#Arcs'))

def quant_vertices_requeridos(cabecalho):
    return transforma(cabecalho.get('#Required N'))

def quant_arestas_requeridas(cabecalho):
    return transforma(cabecalho.get('#Required E'))

def quant_arcos_requeridos(cabecalho):
    return transforma(cabecalho.get('#Required A'))

def capacidade_veiculo(cabecalho):
    return transforma(cabecalho.get('Capacity'))

def deposito(cabecalho):
    return transforma(cabecalho.get('Depot Node'))

# Calcula a densidade real do grafo
def densidade_grafo (cabecalho):
    N = int(cabecalho['#Nodes'])
    E = int(cabecalho['#Edges'])
    A = int(cabecalho['#Arcs'])

    return (E + A)/((N * (N-1))/2)

# Calcula grau total, de entrada e de saída de cada nó
def graus_nohs (grafo, cabecalho):
    quant_nohs = int(cabecalho['#Nodes'])
    grau_total = [0] * (quant_nohs +1) # Ignorar indice 0 pra facilitar
    grau_entrada = [0] * (quant_nohs +1)
    grau_saida = [0] * (quant_nohs +1)

    for i in range (1,len(grafo)):
        for j in range (1, len(grafo[i])):
            celula = grafo[i][j]

            if not celula == None:
                for conexao in celula:
                    tipo = conexao ['tipo']
                
                    if tipo == 'aresta':
                        if i < j:  # Só processa uma vez para evitar contagem duplicada
                            grau_total[i] += 1
                            grau_total[j] += 1

                    elif tipo == 'arco':
                        grau_entrada [j] += 1
                        grau_saida [i] += 1
                        grau_total[i] += 1 # porque grau_total += grau_entrada + grau_saida
                        grau_total[j] += 1

    return grau_total, grau_entrada, grau_saida

# Pega os maiores graus de cada tipo
def grau_maximo (grau_total, grau_entrada, grau_saida):
    # Ignora o índice 0
    grau_total_max = max (grau_total[1:])
    grau_entrada_max = max (grau_entrada[1:])
    grau_saida_max = max (grau_saida[1:])

    return grau_total_max, grau_entrada_max, grau_saida_max

# Pega os menores graus de cada tipo
def grau_minimo(grau_total, grau_entrada, grau_saida):

    grau_total_min = min(grau_total[1:])
    grau_entrada_min = min(grau_entrada[1:])
    grau_saida_min = min(grau_saida[1:])
    
    return grau_total_min, grau_entrada_min, grau_saida_min

# Floyd-Warshall 
def floyd_warshall(grafo, cabecalho):

    '''
    * Calcula *distância mínima* entre todos os pares de vértices usando o algoritmo clássico de Floyd-Warshall.
    * Cria também matriz de predecessores (pred) para reconstruir caminhos.
    '''

    n = int(cabecalho['#Nodes'])
    INF = float('inf') #infinito para inicializar as distâncias entre vértices que ainda não têm ligação direta

    dist = [[INF] * (n+1) for _ in range(n+1)] # Matriz de distâncias
    pred = [[None] * (n+1) for _ in range(n+1)] # Matriz de predecessores

    
    for i in range(1, n+1):
        dist[i][i] = 0 # Distância de cada nó a ele mesmo é 0
        pred[i][i] = i

        for j in range(1, n+1):

            celula = grafo[i][j]
            if celula: # Se não for vazia ou nula

                for conexao in celula:
                    tipo = conexao['tipo']

                    if tipo == 'aresta' or tipo == 'arco':
                        custo = conexao['custo_transito']

                        if tipo == 'aresta' and i < j: # Para evitar duplicação
                            dist[i][j] = min(dist[i][j], custo)
                            dist[j][i] = min(dist[j][i], custo)
                            pred[i][j] = i
                            pred[j][i] = j

                        elif tipo == 'arco':
                            dist[i][j] = min(dist[i][j], custo)
                            pred[i][j] = i

    # Algoritmo principal
    for k in range(1, n+1):
        for i in range(1, n+1):
            for j in range(1, n+1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]

    return dist, pred

# Reconstroi o caminho entre dois nós usando a matriz pred.
def reconstruir_caminho(pred, i, j):
    if pred[i][j] is None:
        return []
    
    caminho = [j]
    while i != j:
        j = pred[i][j]
        caminho.append(j)

    caminho.reverse()
    return caminho

#  Mede intermediação dos nós: quantas vezes cada nó aparece nos caminhos mínimos entre todos os pares.
def calculo_intermediacao (grafo, cabecalho):
    n = int(cabecalho['#Nodes'])
    _, pred = floyd_warshall(grafo, cabecalho)

    intermediacao = [0] * (n + 1)  # índice 0 ignorado

    for s in range(1, n + 1):
        for t in range(1, n + 1):
            if s != t:
                caminho = reconstruir_caminho(pred, s, t)
                for v in caminho[1:-1]:  # ignora origem e destino
                    intermediacao[v] += 1

    return intermediacao

# Calcula o comprimento médio dos caminhos
def caminho_medio(grafo, cabecalho):
    dist, _ = floyd_warshall(grafo, cabecalho)
    n = int(cabecalho['#Nodes'])
    
    soma = 0
    contagem = 0
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and dist[i][j] != float('inf'):
                soma += dist[i][j]
                contagem += 1

    if contagem == 0:
        return 0  
    
    return soma / contagem

# Calcula o diâmetro (maior distância entre dois nós).
def diametro_grafo(grafo, cabecalho):
    dist, _ = floyd_warshall(grafo, cabecalho)
    n = int(cabecalho['#Nodes'])
    
    max_dist = 0
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and dist[i][j] != float('inf'):
                if dist[i][j] > max_dist:
                    max_dist = dist[i][j]

    return max_dist


estatisticas_gerais = []

# Coleta estatísticas para salvar num .csv no final (opcional)
def adicionar_estatisticas(nome_base, cabecalho, grafo):
    grau_total, grau_entrada, grau_saida = graus_nohs(grafo, cabecalho)

    grau_total_max = max(grau_total[1:]) if any(grau_total[1:]) else 0
    grau_entrada_max = max(grau_entrada[1:]) if any(grau_entrada[1:]) else 0
    grau_saida_max = max(grau_saida[1:]) if any(grau_saida[1:]) else 0
    grau_total_min = min(grau_total[1:]) if any(grau_total[1:]) else 0
    grau_entrada_min = min(grau_entrada[1:]) if any(grau_entrada[1:]) else 0
    grau_saida_min = min(grau_saida[1:]) if any(grau_saida[1:]) else 0
    densidade = densidade_grafo(cabecalho)

    estatisticas_gerais.append({
    "Instância": nome_base,
    "Qtde Vértices": transforma(cabecalho.get('#Nodes')),
    "Qtde Arestas": transforma(cabecalho.get('#Edges')),
    "Qtde Arcos": transforma(cabecalho.get('#Arcs')),
    "Qtde Vértices Req.": transforma(cabecalho.get('#Required N')),
    "Qtde Arestas Req.": transforma(cabecalho.get('#Required E')),
    "Qtde Arcos Req.": transforma(cabecalho.get('#Required A')),
    "Densidade": round(densidade, 4),
    "Grau Total Máx": grau_total_max,
    "Grau Entrada Máx": grau_entrada_max,
    "Grau Saída Máx": grau_saida_max,
    "Grau Total Mín": grau_total_min,
    "Grau Entrada Mín": grau_entrada_min,
    "Grau Saída Mín": grau_saida_min
})


# Implementaçao do CARP
def extrair_obrigatorios(grafo, cabecalho):
    #Extrai os serviços obrigatórios (nós, arestas e arcos obrigatórios) com suas demandas e custos
    
    servicos = [];

    N = quant_vertices(cabecalho)
    for i in range(1, N+1):
        for j in range(1, N+1):
            celula = grafo[i][j]
            if celula: 
                for conexao in celula: 
                    if conexao.get('obrigatoria', False):
                        custo_total = conexao.get('custo_transito', 0) + conexao.get('custo_servico', 0)
                        if conexao['tipo'] == 'aresta':

                            servicos.append({
                                'origem' : i,
                                'destino' : j,
                                'demanda' : conexao.get('demanda', 0),
                                'custo_total' : custo_total,
                                'tipo' : 'aresta'
                            })
                            servicos.append({
                                'origem' : j,
                                'destino' : i,
                                'demanda' : conexao.get('demanda', 0),
                                'custo_total' : custo_total,
                                'tipo' : 'aresta'
                            })

                        elif conexao['tipo'] == 'arco':
                            servicos.append({
                                'origem' : i,
                                'destino' : j,
                                'demanda' : conexao.get('demanda', 0),
                                'custo_total' : custo_total,
                                'tipo' : 'arco'
                            })
                        
    return servicos 

# Matriz menores caminhos dentre os obrigatorios 
def matriz_obrigatorios(servicos, distancias):
    # Cria uma matriz de custos entre os serviços, somando deslocamento e custo do serviço destino

    n = len(servicos)
    matriz_custos = [[float('inf')]* n for _ in range(n)]

    for i in range(n): 
        for j in range(n):
            if i == j:
                matriz_custos[i][j] = 0 
                continue

            origemJ = servicos[j]['origem']
            destinoI = servicos[i]['destino']

            deslocamento = distancias[destinoI][origemJ]

            custo_servicoJ = servicos[j]['custo_total']

            matriz_custos[i][j] = deslocamento + custo_servicoJ

    return matriz_custos

# Otimizacao da heuristica Clarke e Wright
def clarke_wright_otimizado(servicos, matriz_custos, capacidade):
    n = len(servicos)

    # Inicializa uma rota para cada serviço (cada rota começa e termina no depósito)
    rotas = [{'servicos': [i], 'carga': servicos[i]['demanda'], 'inicio': i, 'fim': i} for i in range(n)]

    # Calcula economias para todas as combinações possíveis entre serviços
    economias = []
    for i in range(n):
        for j in range(n):
            if i != j:
                economia = matriz_custos[0][i] + matriz_custos[0][j] - matriz_custos[i][j]
                economias.append((economia, i, j))
    
    # Ordena as economias em ordem decrescente
    economias.sort(reverse=True)

    # União das rotas
    for economia, i, j in economias:
        rota_i = next((r for r in rotas if r['fim'] == i), None)
        rota_j = next((r for r in rotas if r['inicio'] == j), None)

        if rota_i is None or rota_j is None or rota_i == rota_j:
            continue

        nova_carga = rota_i['carga'] + rota_j['carga']
        if nova_carga <= capacidade:

            # Penalização para evitar rotas ruins
            if economia < 0 and len(rota_i['servicos']) + len(rota_j['servicos']) <= 3:
                continue

            # Une rotas
            rota_i['servicos'].extend(rota_j['servicos'])
            rota_i['fim'] = rota_j['fim']
            rota_i['carga'] = nova_carga
            rotas.remove(rota_j)

    return rotas

def refinar_rotas_por_realocacao(rotas, servicos, matriz_custos, capacidade):
    rotas.sort(key=lambda r: len(r['servicos']))  # Começa tentando remover as menores

    i = 0
    while i < len(rotas):
        rota_atual = rotas[i]
        realocado = False

        for serv_id in rota_atual['servicos']:
            servico = servicos[serv_id]

            for j in range(len(rotas)):
                if i == j:
                    continue

                destino = rotas[j]
                nova_carga = destino['carga'] + servico['demanda']

                if nova_carga > capacidade:
                    continue

                # Simula custo atual e com a realocação
                custo_antigo = custo_rota(destino, matriz_custos)
                destino_simulada = destino['servicos'] + [serv_id]
                destino_simulada.sort()
                destino_tmp = {'servicos': destino_simulada}
                custo_novo = custo_rota(destino_tmp, matriz_custos)

                if custo_novo < custo_antigo + matriz_custos[0][serv_id] + matriz_custos[serv_id][0]:
                    # Realoca
                    destino['servicos'].append(serv_id)
                    destino['carga'] = nova_carga
                    realocado = True
                    break

            if realocado:
                break

        if realocado:
            rotas.pop(i)
        else:
            i += 1

    return rotas

# Custo total da rota
def custo_rota(rota, matriz_custos):
    # Soma os custos de ida, entre serviços, e volta ao depósito

    servicos = rota['servicos']
    custo = 0

    # Custo ida do depósito (índice 0) até o primeiro serviço
    custo += matriz_custos[0][servicos[0]]

    # Custo entre serviços consecutivos
    for i in range(len(servicos) - 1):
        custo += matriz_custos[servicos[i]][servicos[i + 1]]

    # Custo retorno do último serviço até o depósito
    custo += matriz_custos[servicos[-1]][0]

    return custo

# Salva os resultados no formato padronizado
def salvar_rotas_em_arquivo(nome_saida, rotas, servicos, custo_total, matriz_custos, clocks_alg, clocks_total):
    
    # Linha por rota: ID, demanda, custo, visitas e sequência de serviços com (S id,origem,destino)
    
    with open(nome_saida, "w", encoding="utf-8") as f:
        f.write(f"{int(custo_total)}\n")
        f.write(f"{len(rotas)}\n")
        f.write(f"{clocks_alg}\n")     # clocks do algoritmo
        f.write(f"{clocks_total}\n")   # clocks do programa 

        for idx, rota in enumerate(rotas, 1):
            carga_total = sum([servicos[i]['demanda'] for i in set(rota['servicos'])])
            custo_rota_valor = custo_rota(rota, matriz_custos)
            f.write(f"0 1 {idx} {carga_total} {int(custo_rota_valor)} {len(rota['servicos']) + 2} {' '}")
            f.write("(D 0,1,1) ")
            for i in rota['servicos']:
                s = servicos[i]
                f.write(f"(S {i+1},{s['origem']},{s['destino']}) ")
            f.write("(D 0,1,1)\n")

# * Processa uma única instância: lê, extrai, calcula rota e salva
def processar_instancia(arquivo_entrada, pasta_saida):
    nome_base = os.path.basename(arquivo_entrada).replace(".dat", "")
    cabecalho, grafo = ler_entrada(arquivo_entrada)

    inicio_total = time.perf_counter_ns()

    dist, _ = floyd_warshall(grafo, cabecalho)
    servicos = extrair_obrigatorios(grafo, cabecalho)
    matriz_custos = matriz_obrigatorios(servicos, dist)
    capacidade = capacidade_veiculo(cabecalho)


    inicio_alg = time.perf_counter_ns()
    rotas = clarke_wright_otimizado(servicos, matriz_custos, capacidade)
    rotas = refinar_rotas_por_realocacao(rotas, servicos, matriz_custos, capacidade)
    fim_alg = time.perf_counter_ns()

    custo = sum(custo_rota(rota, matriz_custos) for rota in rotas)

    fim_total = time.perf_counter_ns()

    clocks_alg = fim_alg - inicio_alg          # clocks do algoritmo
    clocks_total = fim_total - inicio_total    # clocks do programa todo

    nome_saida = os.path.join(pasta_saida, f"sol-{nome_base}.dat")
    salvar_rotas_em_arquivo(nome_saida, rotas, servicos, custo, matriz_custos, clocks_alg, clocks_total)

    try:
        adicionar_estatisticas(nome_base, cabecalho, grafo)
    except Exception as e:
        print(f"❌ Erro ao adicionar estatísticas de {nome_base}: {e}")

# Processa todos os arquivos .dat da pasta instancias/ e salva as soluções na pasta solucoes/
def processar_todos():
    import sys
    import os
    import pandas as pd

    pasta_entrada = "instancias/"
    pasta_saida = "G12/"
    os.makedirs(pasta_saida, exist_ok=True)

    import re

    def ordenar(nome):
    # Divide o nome do arquivo em blocos de texto e números
        return [int(bloco) if bloco.isdigit() else bloco.lower() 
            for bloco in re.split(r'(\d+)', nome)]

    arquivos = sorted([
        f.strip() for f in os.listdir(pasta_entrada)
        if f.lower().strip().endswith(".dat")
    ], key=ordenar)


    for idx, arq in enumerate(arquivos, start=1):
        print(f"\n🟡 ({idx}/{len(arquivos)}) Processando {arq}...")
        sys.stdout.flush()  # força exibir print antes da execução

        caminho = os.path.join(pasta_entrada, arq)

        try:
            processar_instancia(caminho, pasta_saida)
            print(f"✅ {arq} processado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao processar {arq}: {e}")

    try:
        df = pd.DataFrame(estatisticas_gerais)
        df.to_csv("estatisticas_gerais.csv", index=False, sep=';', encoding="utf-8")
        print("📁 Estatísticas salvas com sucesso em 'estatisticas_gerais.csv'")
    except Exception as e:
        print(f"❌ Erro ao salvar o CSV: {e}")