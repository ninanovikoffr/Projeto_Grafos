# Trabalho Prático Final

## Modelagem Logística com Grafos em Python

Implementação do projeto final da disciplina de Algoritmos em Grafos, utilizando Python.

📍 Universidade Federal de Lavras
👨‍🏫 Prof. Mayron César O. Moreira

---

## 🎯 Sobre o projeto

Neste trabalho buscamos aplicar os principais conceitos aprendidos na disciplina até agora, modelando um problema logístico por meio de um grafo misto (direcionado e não direcionado). Na etapa atual, o programa é capaz de:

* 📂 Ler um arquivo de entrada com dados de nós e arestas/arcos;
* 🧠 Armazenar esses dados em uma estrutura de grafo;
* 🧹 Utilizar o algoritmo de *Floyd-Warshall* para encontrar os caminhos mínimos entre os nós e produzir a matriz de predecessores;
* 📊 Calcular métricas importantes do grafo:
  * Quantidade total de vértices, arestas e arcos
  * Quantidade de vértices, arestas e arcos obrigatórios
  * Densidade
  * Grau dos nós
  * Centralidade de intermediação
  * Caminho médio
  * Diâmetro
* 📋 Salvar as estatísticas de cada instância em uma planilha
* 🧩 Utilizar uma heurística baseada em Clarke & Wright  para encontrar a solução para cada instância
* 🗂 Armazenar os resultados em arquivos para cada instância, em uma pasta

---

## 🧠 Interpretação do Problema

Este projeto simula um cenário logístico urbano representado por um *grafo misto e conexo*, onde:

- *Vértices* representam interseções ou pontos de interesse em uma cidade;
- *Arestas* representam ruas de mão dupla;
- *Arcos* representam ruas de mão única;
- Um subconjunto desses elementos (vértices, arestas e arcos) deve obrigatoriamente ser atendido.

O objetivo é determinar rotas de custo mínimo que atendam todas as demandas, respeitando a *capacidade dos veículos* e sempre partindo e retornando a um *depósito central*.

---

## 📁 Estrutura do Projeto

- proj.py: arquivo contendo todas as funções principais.

- visualizacao.ipynb: notebook usado como *main interativa*, com células que chamam as funções e exibem os resultados de forma separada.

- instancias: pasta que contem as bases de dados utilizadas.

- solucoes: pasta que será criada automaticamente para armazenar as soluções do problema.

- estatísticas: planilha que armazena as estatísticas de todas as instâncias.

---

## 🔹 Padrão de Saída das Soluções

Cada solução gerada segue rigorosamente este formato:


<linha 1> custo total da solução
<linha 2> total de rotas
<linha 3> total de clocks para execução do algoritmo de referência
<linha 4> total de clocks para encontrar a solução de referência
<linha 5+> 0 1 <id_rota> <demanda_total_rota> <custo_total_rota> <total_visitas> (D 0,1,1) (S id,origem,destino) ... (D 0,1,1)


* *(D 0,1,1)* indica a parada no depósito.
* *(S id, origem, destino)* representa um serviço realizado (vértice, aresta ou arco).

---

## 🧠 Observações

- O grafo é representado por uma matriz de adjacência, mais especificamente uma matriz em que cada célula é uma lista de dicionários, para caso haja arestas e arcos no mesmo vértice seja possível armazenar as informações de ambos caminhos.
- A indexação começa em 1 (posição 0 é ignorada).

---

## ⚙ Como executar

1. 🐍 Certifique-se de ter o *Python 3.x* e o *Jupyter Notebook* instalados.
2. 📁 Coloque todos os arquivos e a pasta de instâncias (proj.py, visualizacao.ipynb, instancias) na mesma pasta.
3. 📓 Abra o Jupyter e execute o notebook visualizacao.ipynb, célula por célula.
4. ✅ Os resultados dos cálculos e algoritmos serão criados em uma pasta "solucoes", e as estatísticas serão armazenadas em um arquivo .csv "estatisticas\_gerais"

> O notebook está pronto para ler os arquivos e salvar os resultados automaticamente!

* Caso ocorra erro como NameError ou KeyError, verifique:

  * Se o proj.py foi importado corretamente
  * Se os arquivos .dat foram carregados com sucesso.

---

## 👩‍💼 Autoras

* *Lana da Silva Miranda*
* *Nina Tobias Novikoff da Cunha Ribeiro*