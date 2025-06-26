import importlib
import proj
import time
import os 

from leitura_escrita import *
from estatisticas import *
from heuristica import *

# * Processa uma única instância: lê, extrai, calcula rota e salva
def processar_instancia(arquivo_entrada, pasta_saida):
    nome_base = os.path.basename(arquivo_entrada).replace(".dat", "")
    cabecalho, grafo, servicos_obrigatorios = ler_entrada(arquivo_entrada)

    inicio_total = time.perf_counter_ns()

    dist, _ = floyd_warshall(grafo, cabecalho)
    servicos = servicos_obrigatorios
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
    

processar_todos()