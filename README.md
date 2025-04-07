# Trabalho Prático Final  
## Modelagem Logística com Grafos em Python

Implementação do projeto final da disciplina de Algoritmos em Grafos, utilizando Python.

📍 Universidade Federal de Lavras  
👨‍🏫 Prof. Mayron César O. Moreira  

---

## 🎯 Sobre o projeto

Neste trabalho buscamos aplicar os principais conceitos aprendidos na disciplina até agora, modelando um problema logístico por meio de um grafo misto (direcionado e não direcionado). Na etapa atual, o programa é capaz de:

- 📂 Ler um arquivo de entrada com dados de nós e arestas/arcos;
- 🧠 Armazenar esses dados em uma estrutura de grafo;
- 🧮 Utilizar o algoritmo de **Floyd-Warshall** para encontrar os caminhos mínimos entre os nós e produzir a matriz de predecessores;
- 📊 Calcular métricas importantes do grafo:
  - Quantidade total de vértices, arestas e arcos
  - Quuantidade de vértices, arestas e arcos obrigatórios
  - Densidade
  - Grau dos nós
  - Centralidade de intermediação
  - Caminho médio
  - Diâmetro

---

## 🧠 Interpretação do Problema

Este projeto simula um cenário logístico urbano representado por um **grafo misto e conexo**, onde:

- **Vértices** representam interseções ou pontos de interesse em uma cidade;
- **Arestas** representam ruas de mão dupla;
- **Arcos** representam ruas de mão única;
- Um subconjunto desses elementos (vértices, arestas e arcos) deve obrigatoriamente ser atendido.

O objetivo - que será cumprido nas etapas seguintes - é determinar rotas de custo mínimo que atendam todas as demandas, respeitando a **capacidade dos veículos** e sempre partindo e retornando a um **depósito central**.

---

## 📁 Estrutura do Projeto

- `proj.py`: arquivo contendo todas as funções principais:
  - Leitura de um arquivo base `.dat` (ler_entrada)
  - Funções para retornar as quantidades
  - Cálculo da densidade
  - Cálculo dos graus de cada vértice e funcões para retornar o grau máximo e mínimo
  - Algoritmo de Floyd-Warshall
  - Reconstrução de caminhos
  - Cálculo de intermediação
  - Cálculo do caminho médio
  - Cálculo do diâmetro do grafo
  - Impressão das matrizes de caminho mais curto e predecessores (para depuração)

- `visualizacao.ipynb`: notebook usado como **main interativa**, com células que chamam as funções e exibem os resultados de forma separada.

- `BHW1.dat`: uma das bases de dados com a matriz de adjacência do grafo.

---

## 🧠 Observações

- O grafo é representado por uma matriz de adjacência, mais especificamente uma matriz em que cada célula é uma lista de dicionários, para caso haja arestas e arcos no mesmo vértice seja possível armazenar as informações de ambos caminhos.
- A indexação começa em 1 (posição 0 é ignorada).

---

## ⚙️ Como executar

1. 🐍 Certifique-se de ter o **Python 3.x** e o **Jupyter Notebook** instalados.
2. 📁 Coloque todos os arquivos (`proj.py`, `visualizacao.ipynb`, `BHW1.dat`) na mesma pasta.
3. 📓 Abra o Jupyter e execute o notebook `visualizacao.ipynb`, célula por célula.
4. ✅ Os resultados dos cálculos e algoritmos serão exibidos no próprio notebook.

> O notebook está pronto para ler o arquivo automaticamente e mostrar os resultados de forma interativa!

- Caso ocorra erro como `NameError` ou `KeyError`, verifique:
  - Se o `proj.py` foi importado corretamente
  - Se o arquivo `.dat` foi carregado com sucesso

---

## 👩‍💻 Autoras

- **Lana da Silva Miranda**  
- **Nina Tobias Novikoff da Cunha Ribeiro**

