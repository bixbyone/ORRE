# ORRE

Otimizando a Robustez da Rede Elétrica - ONS

O objetivo deste projeto é aumentar a robustez de uma rede elétrica, identificando de forma eficiente seus pontos de falha e calculando quais melhores linhas de transmissão a tornam mais redundante.

**Inspiração**
Tem havido um aumento do financiamento e da atenção para proteger a rede eléctrica e as suas muitas ineficiências Plano Orçamental Presidencial dos EUA Subestações alvo de ataques extremistas Aumento da procura e escassez de energia As falhas na rede eléctrica aumentaram principalmente devido a eventos relacionados com o clima

**O que faz**
A quantidade mínima de dados que uma nação/região pode fornecer para métricas da rede elétrica é puramente conectividade de certos nós com estimativas de distâncias insignificantes. Primeiro, precisamos importar os dados e registrar várias métricas aproximadas de centralidade: 
- EigenVector Centrality
- Katz Centrality
- e Degree Centrality.

A centralidade do vetor próprio pode ser mapeada para um problema QUBO. Verifique as interseções entre cada um dos 100 maiores e escolha o mais corroborado.
Então precisamos mapeá-lo para um problema de cobertura máxima de cliques entre o conjunto de todos os geradores de energia designados. É formulado que todos os nós excluídos da clique máxima são nós de alta prioridade aos quais adicionar links. Em seguida, calculamos o grau médio de geradores de energia para outros geradores de energia. Calculamos as menores distâncias entre os nós excluídos e os nós conectados e retornamos as arestas (ou linhas de transmissão entre os nós geradores que serão colocados). É aí que novas linhas de transmissão devem ser feitas

Como o construímos
Foi inteiramente um projeto de programação, escrito em Python (ambiente Google Colab) tendo as bibliotecas NetworkX e DWave como ferramentas principais.

**Desafios que enfrentamos**
O tempo de execução dos testes. Eles foram extremamente lentos para serem executados, uma vez que este é um projeto muito pesado em termos computacionais, portanto, ajustar as restrições na alocação de tempo dada foi um desafio definitivo.

**Realizações das quais nos orgulhamos**
Quão eficazes foram as alterações no gráfico, dadas as restrições de tempo para pensar no algoritmo.

**O que aprendemos**
Que este algoritmo foi bastante eficaz na identificação de pontos de falha e na formulação das melhores arestas a serem colocadas.

**O que vem a seguir para otimizar a robustez da rede elétrica**
Acessando hardware quântico para a resolução do problema QUBO e mapeando o algoritmo BFS implementado para outro problema QUBO.

**Construído com**
dwave
logging-tables
networkx
numpy
pandas
python
wolfram-technologies

**Experimente:***
 colab.research.google.com

**Referencia:**
https://devpost.com/software/optimizing-power-grid-network-robustness
