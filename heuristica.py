import csv
import pandas as pd
import os
import time

from leitura_escrita import *
from estatisticas import *


# Implementaçao do CARP

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

def two_opt(rota, matriz_custos):
    servicos = rota['servicos']
    melhor = servicos[:]
    melhor_custo = custo_rota({'servicos': melhor}, matriz_custos)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(1, len(melhor) - 1):
            for j in range(i + 1, len(melhor)):
                if j - i == 1:
                    continue
                nova = melhor[:i] + melhor[i:j][::-1] + melhor[j:]
                novo_custo = custo_rota({'servicos': nova}, matriz_custos)
                if novo_custo < melhor_custo:
                    melhor = nova
                    melhor_custo = novo_custo
                    melhorou = True
        servicos = melhor[:]
    return melhor

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

                custo_antigo_origem = custo_rota(rota_atual, matriz_custos)
                custo_antigo_destino = custo_rota(destino, matriz_custos)

                servicos_origem_novo = [s for s in rota_atual['servicos'] if s != serv_id]

                # Testa todas as posições possíveis de inserção
                melhor_custo_novo_destino = None
                melhor_pos = None
                for pos in range(len(destino['servicos']) + 1):
                    servicos_destino_novo = destino['servicos'][:pos] + [serv_id] + destino['servicos'][pos:]
                    custo_novo_destino = custo_rota({'servicos': servicos_destino_novo}, matriz_custos)
                    if (melhor_custo_novo_destino is None) or (custo_novo_destino < melhor_custo_novo_destino):
                        melhor_custo_novo_destino = custo_novo_destino
                        melhor_pos = pos

                custo_novo_origem = custo_rota({'servicos': servicos_origem_novo}, matriz_custos) if servicos_origem_novo else 0

                # Critério correto: só realoca se a soma dos custos das rotas diminuir
                if custo_novo_origem + melhor_custo_novo_destino < custo_antigo_origem + custo_antigo_destino:
                    # Realoca na melhor posição
                    destino['servicos'].insert(melhor_pos, serv_id)
                    destino['carga'] = nova_carga
                    rota_atual['servicos'].remove(serv_id)
                    rota_atual['carga'] -= servico['demanda']
                    # Aplica 2-opt na rota destino
                    destino['servicos'] = two_opt(destino, matriz_custos)
                    realocado = True
                    break

            if realocado:
                break

        if realocado:
            # Remove rota se ficou vazia
            if not rota_atual['servicos']:
                rotas.pop(i)
            else:
                # Aplica 2-opt na rota de origem também
                rota_atual['servicos'] = two_opt(rota_atual, matriz_custos)
                i += 1
        else:
            i += 1

    return rotas

# Refinamento: compara realocação com critério correto (custo total) e critério ruim (ex: número de rotas)
def refinar_rotas_duplo_criterio(rotas, servicos, matriz_custos, capacidade):
    import copy
    # Critério correto: custo total
    rotas_correto = copy.deepcopy(rotas)
    rotas_correto = refinar_rotas_por_realocacao(rotas_correto, servicos, matriz_custos, capacidade)
    custo_correto = sum(custo_rota(r, matriz_custos) for r in rotas_correto)

    # Critério ruim: apenas número de rotas (realoca se diminuir número de rotas, mesmo que o custo aumente)
    def refinar_rotas_num_rotas(rotas, servicos, matriz_custos, capacidade):
        rotas.sort(key=lambda r: len(r['servicos']))
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
                    # Critério ruim: realoca se rota de origem ficar vazia (diminui número de rotas)
                    if len(rota_atual['servicos']) == 1:
                        destino['servicos'].append(serv_id)
                        destino['carga'] = nova_carga
                        rota_atual['servicos'].remove(serv_id)
                        rota_atual['carga'] -= servico['demanda']
                        destino['servicos'] = two_opt(destino, matriz_custos)
                        realocado = True
                        break
                if realocado:
                    break
            if realocado:
                if not rota_atual['servicos']:
                    rotas.pop(i)
                else:
                    rota_atual['servicos'] = two_opt(rota_atual, matriz_custos)
                    i += 1
            else:
                i += 1
        return rotas

    rotas_ruim = copy.deepcopy(rotas)
    rotas_ruim = refinar_rotas_num_rotas(rotas_ruim, servicos, matriz_custos, capacidade)
    custo_ruim = sum(custo_rota(r, matriz_custos) for r in rotas_ruim)

    # Retorna a solução de menor custo total
    if custo_correto <= custo_ruim:
        return rotas_correto
    else:
        return rotas_ruim

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