import networkx as nx
import pandas as pd
import numpy as np
import requests
import random
from collections import defaultdict
import dwave_networkx as dnx
from networkx.algorithms.bipartite.centrality import degree_centrality
from networkx.algorithms.connectivity.connectivity import average_node_connectivity
import neal

# Instalando pacotes necessários
!pip install networkx
!pip install pandas
!pip install dwave-networkx

def load_data(url):
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print("Erro ao carregar os dados:", e)
        return None

def create_graph_from_data(data):
    G = nx.Graph()
    # Adicionar nós e arestas ao grafo, conforme necessário
    return G

def calculate_centralities(G):
    centrality = {}
    centrality['degree'] = nx.degree_centrality(G)
    centrality['eigenvector'] = nx.eigenvector_centrality(G, max_iter=1000)
    centrality['katz'] = nx.katz_centrality(G)
    return centrality

def sample_central_nodes(G, centrality_measure):
    central_nodes = sorted(G, key=centrality_measure.get, reverse=True)[:100]
    return central_nodes

def intersections(list1, list2, list3):
    s1 = set(list1)
    s2 = set(list2)
    s3 = set(list3)
    result = list(s1.intersection(s2, s3))
    return result

def add_random_edges(G, num_edges):
    possible_edges = [(u, v) for u in G.nodes() for v in G.nodes() if u != v and not G.has_edge(u, v)]
    random.shuffle(possible_edges)
    for _ in range(min(num_edges, len(possible_edges))):
        u, v = possible_edges.pop()
        G.add_edge(u, v)

def shutdown_evaluations(G, closed_gen, list_of_generators):
    G2 = G.copy()
    capacities_original = get_capacities(G2, list_of_generators)

    removed_nodes = []
    nodes_to_remove = [closed_gen]
    while nodes_to_remove:
        node_to_remove = nodes_to_remove.pop(0)
        removed_nodes.append(node_to_remove)
        list_of_generators.remove(node_to_remove)
        new_capacities = get_capacities(G2, list_of_generators)
        for node in list_of_generators:
            if new_capacities[node] > 2 * capacities_original[node]:
                if node not in nodes_to_remove:
                    nodes_to_remove.append(node)
    return removed_nodes

def simulate_shutdowns(G, list_of_generators, num_suggested_edges=0, num_random_edges=0):
    print("Original Simulation:")
    for generator in list_of_generators:
        aux_list = list_of_generators.copy()
        affected_generators = shutdown_evaluations(G, generator, aux_list)
        if len(affected_generators) > 0:
            print(generator, len(affected_generators))

    if num_suggested_edges > 0:
        G_suggested = G.copy()
        # Adicionar arestas sugeridas
        print("Simulation with Suggested Edges:")
        for generator in list_of_generators:
            aux_list = list_of_generators.copy()
            affected_generators = shutdown_evaluations(G_suggested, generator, aux_list)
            if len(affected_generators) > 0:
                print(generator, len(affected_generators))

    if num_random_edges > 0:
        G_random = G.copy()
        add_random_edges(G_random, num_random_edges)
        print("Simulation with Random Edges:")
        for generator in list_of_generators:
            aux_list = list_of_generators.copy()
            affected_generators = shutdown_evaluations(G_random, generator, aux_list)
            if len(affected_generators) > 0:
                print(generator, len(affected_generators))

def main():
    # Carregar dados
    url = "https://raw.githubusercontent.com/bixbyone/ORRE/main/src/DataRecords.json"
    data = load_data(url)
    if data is None:
        return

    G = create_graph_from_data(data)
    if G is None:
        return

    centrality = calculate_centralities(G)
    degree_centrality_measure = centrality['degree']
    eigenvector_centrality_measure = centrality['eigenvector']
    katz_centrality_measure = centrality['katz']

    central_nodes_degree = sample_central_nodes(G, degree_centrality_measure)
    central_nodes_eigenvector = sample_central_nodes(G, eigenvector_centrality_measure)
    central_nodes_katz = sample_central_nodes(G, katz_centrality_measure)

    influential_nodes = intersections(central_nodes_degree, central_nodes_eigenvector, central_nodes_katz)

    simulate_shutdowns(G, influential_nodes, num_suggested_edges=0, num_random_edges=10)

if __name__ == "__main__":
    main()
