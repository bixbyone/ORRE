
pip install networkx

import networkx as nx
import numpy as np
import pandas as pd
     

G = nx.Graph()
G = nx.read_gml('western_interconnection.gml', label=None)
_G = G.copy()
def normalize(v):

    min, max = np.min(v), np.max(v)
    return((v - min)/(max - min))

from networkx.algorithms.bipartite.centrality import degree_centrality
centrality = {}
centrality['degree'] = nx.degree_centrality(G)
centrality['eigenvector'] = nx.eigenvector_centrality(G, max_iter=1000)
centrality['katz'] = nx.katz_centrality(G)

degree = nx.degree_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
katz = nx.katz_centrality(G)

centrality_data= pd.DataFrame(centrality)

for node in sorted(degree, key=degree.get, reverse=True):
  print(node, degree[node])

for node in sorted(eigenvector, key=eigenvector.get, reverse=True):
  print(node, eigenvector[node])
     

for node in sorted(katz, key=katz.get, reverse=True):
  print(node, katz[node])

for v in centrality_data.columns:
    centrality_data[v] = normalize(centrality_data[v])

centrality_correlations = centrality_data.corr('pearson')
centrality_correlations
     

sorted_degree = sorted(degree, key=degree.get, reverse=True)
sorted_eigenvector = sorted(eigenvector, key=eigenvector.get, reverse=True)
sorted_katz = sorted(katz, key=katz.get, reverse=True)

def sample_central_nodes(G):
  central_nodes = []
  i = 0
  for node in sorted(G, key=G.get, reverse=True):
    if(i<100):
      central_nodes.append(node)
      i = i + 1
  return central_nodes
     

central_nodes_degree = sample_central_nodes(degree)
central_nodes_eigenvector = sample_central_nodes(eigenvector)
central_nodes_katz = sample_central_nodes(katz)

def intersections(list1, list2, list3):
    s1 = set(list1)
    s2 = set(list2)
    s3 = set(list3)
    set1 = s1.intersection(s2)
    set1 =  (s2 & s3)
    result = list(set1 & s3)
    #intersections = list(set1)
    return result

influential_nodes = intersections(central_nodes_degree, central_nodes_eigenvector, central_nodes_katz)
     

_G = G.copy()
     

#_G = G.copy()
for n, d in G.copy().nodes(data=True):
  if(n not in influential_nodes):
    G.remove_node(n)

print(G)
     

#!pip3 install dwave_networkx.maximum_clique
!git clone https://github.com/hvidberrrg/d-wave.git

!cd d-wave && pip install -r requirements.txt
    
import dwave_networkx as dnx
import neal
solver = neal.SimulatedAnnealingSampler()
    

from networkx.algorithms.connectivity.connectivity import average_node_connectivity

recursed_graph = G.copy()
_cliques = []
def recursive_maximal_cliques(G, cliques):

  if(len(G.nodes) == 0):
    #print(cliques)
    return cliques
  else:
    clique = dnx.maximum_clique(G, solver)
    cliques.append(clique)
    for n in clique:
      if(n in G.nodes):
        G.remove_node(n)
    recursive_maximal_cliques(G, _cliques)
    return cliques

_cliques = recursive_maximal_cliques(recursed_graph, _cliques)
print(_cliques)
  

def connectivity_metric_and_high_priority_nodes(G, cliques):
  node_connectivities = []
  high_priority_nodes = []
  for idx, x in enumerate(cliques):
    print(idx, x)
    if(len(cliques[idx]) > 1):
      induced_subgraph = nx.induced_subgraph(G, cliques[idx])
      avg_node_connectivity = nx.average_node_connectivity(induced_subgraph)
      node_connectivities.append(avg_node_connectivity)
    else:
      high_priority_nodes.append(x.copy().pop())
  print(node_connectivities)
  print(high_priority_nodes)
  return node_connectivities, high_priority_nodes
avg_clique_connectivitities, high_priority_nodes = connectivity_metric_and_high_priority_nodes(G.copy(), _cliques)
total_avg_clique_connectivities = np.sum(avg_clique_connectivitities) / len(avg_clique_connectivitities)
print(total_avg_clique_connectivities)    

def influential_node_distances(G, influential_nodes):
  distance_matrix = []
  distance = []
  for idx, x in enumerate(influential_nodes):
    for idy, y in enumerate(influential_nodes):
      try:
        distance = nx.shortest_path_length(G, x, y)
      except nx.NetworkXNoPath:
          continue
      if(distance is not None):
        distance_matrix.append([idx, idy, distance])
  print(distance_matrix)
  return distance_matrix

node_distances = influential_node_distances(G.copy(), influential_nodes)  

from tables.utils import list_logged_instances
from random import randint
intersection = set(influential_nodes).intersection(set(high_priority_nodes))
#print(intersection)
def get_indices(influential_nodes, intersection):
  indices = []
  for i in intersection:
    indices.append(influential_nodes.index(i))
  #print(indices)
  return indices

indices = get_indices(influential_nodes.copy(), intersection)

print(indices)
#t_node_distances = np.transpose(node_distances.copy())
addressed_priority_distances = []
priority_node_distances = []

arr_list = sorted(node_distances, key=lambda x: x[2], reverse=False)
list_of_lists = [sub_arr for sub_arr in arr_list]
print(list_of_lists)
#print(list_of_lists[:])

#print(decr_sort_distances)
#print(decr_sort_distances)
#arr_sorted = np.sort(node_distances, axis=1)

def select_elements(list_of_lists, indices, influential_nodes, average_clique_connectiveness):
    transmission_line_possibilities = []

    for sublist in list_of_lists:
        if sublist[0] in indices and sublist[2] < 3:
            transmission_line_possibilities.append(sublist)
        if sublist[0] == sublist[1]:
          for i in indices:
            transmission_line_possibilities.append([sublist[0], i])



    # transmission_line_redirect_list = sorted(transmission_line_possibilities, key=lambda x: x[2])
    return transmission_line_possibilities

transmission_line_redirect_list =  select_elements(list_of_lists, indices, influential_nodes, total_avg_clique_connectivities)
print(transmission_line_redirect_list)
len(transmission_line_redirect_list)

#print(result)
#sorted_dist = decr_sort_distances.copy()
#print(sorted_dist)

#for i in indices:
  #priority_node_distances.append(np.where(sorted_dist[i]) != 0)
#len(priority_node_distances)
#print(priority_node_distances)

     

def convert_elements_to_nodes(list_of_lists, influential_nodes):
    converted_list = []
    list_copy = list_of_lists.copy()
    influential_nodes_copy = influential_nodes.copy()
    for sublist in list_copy:
        sublist[0] = influential_nodes_copy[sublist[0]]
        sublist[1] = influential_nodes_copy[sublist[1]]
        converted_list.append([sublist[0], sublist[1]])
    return converted_list

converted = convert_elements_to_nodes(transmission_line_redirect_list, influential_nodes)
len(converted)

print(converted)
#increment in greater random amounts of these edges being formed and see how the robustness of the netowrk changes
     

def add_edges(edges, G):
    G2 = nx.Graph()
    G2 = G.copy()
    for sublist in edges:
        G2.add_edge(sublist[0], sublist[1])
    nx.write_gexf(G, 'MODIFIED_GRAPH.gexf')
    return G2
G2 = add_edges(converted, _G)


     

def BFS(G, init_node, distances_family):
    queue = [init_node]
    distances_family [init_node] = (0, init_node)
    while queue:
        node = queue.pop(0)
        for neighbour in G.neighbors(node):
            if distances_family[node][0] + 1 <= distances_family[neighbour][0]:
                queue.append(neighbour)
                distances_family[neighbour] = (distances_family[node][0] + 1, init_node)
    return distances_family


def calculate_distances(G, list_of_generators):
    distances = [(100, -1)]*(G.number_of_nodes() + 1)

    for node in list_of_generators:
        distances = BFS(G, node, distances)

    return distances

distances_family_G1 = calculate_distances(_G, influential_nodes)
distances_family_G2 = calculate_distances(G2, influential_nodes)

     

def get_consumers(G, list_of_generators):
    consumers = {}
    distances_family = calculate_distances(G, list_of_generators)
    for node in G.nodes:
        family = distances_family[node][1]
        if family not in consumers.keys():
            consumers[family] = [node]
        else:
            consumers[family].append(node)
    return consumers

consumers_1 = get_consumer(_G, influential_nodes)
consumers_2 = get_consumers(G2, influential_nodes)

     

def get_capacities(G, list_of_generators):
    capacities = {}
    consumers = get_consumers(G, list_of_generators)
    for generator in consumers.keys():
        capacities[generator] = len(consumers[generator])
    return capacities

def shutdown_evaluations(G, closed_gen, list_of_generators):
    G2 = nx.Graph()
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
            if new_capacities[node] > 2*capacities_original[node]:
                if node not in nodes_to_remove:
                    nodes_to_remove.append(node)
    return removed_nodes

def simulate(G, list_of_generators):
    for generator in list_of_generators:
        aux_list = list_of_generators.copy()
        affected_generators = shutdown_evaluations(G, generator, aux_list)
        if(len(affected_generators)>0):
            print(generator,len(affected_generators))

def add_random_edges(G, num_edges):
    """Adds a specified number of random edges to a graph."""
    possible_edges = []
    for u in G.nodes():
        for v in G.nodes():
            if u != v and not G.has_edge(u, v):
                possible_edges.append((u, v))

    if num_edges > len(possible_edges):
        raise ValueError("Cannot add more edges than possible.")

    random.shuffle(possible_edges)
    for _ in range(num_edges):
        u, v = possible_edges.pop()
        G.add_edge(u, v)

def simulate(G, list_of_generators, num_suggested_edges=0, num_random_edges=0):
    print("Original Simulation:")
    for generator in list_of_generators:
        aux_list = list_of_generators.copy()
        affected_generators = shutdown_evaluations(G, generator, aux_list)
        if len(affected_generators) > 0:
            print(generator, len(affected_generators))

    if num_suggested_edges > 0:
        G_suggested = G.copy()
        add_edges(converted, G_suggested)

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
     


     
