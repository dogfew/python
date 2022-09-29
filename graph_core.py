import networkx as nx
from itertools import product, combinations

G1 = nx.DiGraph()
edges = [('a', 'b'), ('a', 'd'), ('d', 'c'), ('c', 'd'), ('c', 'a')]
G1.add_edges_from(edges)

def get_all_subsets(set_):
    return [frozenset(i) for n in range(len(set_) + 1) for i in combinations(set_, n)]

def get_internally_stable(G):
    out = set()
    for set_ in get_all_subsets(set(G)):
        all_pairs = frozenset(product(set_, repeat=2))
        if all_pairs & set(G.edges) == set():
            out.add(set_)
    return out

def get_outwardly_stable(G):
    out = set()
    for set_ in get_all_subsets(set(G)):  
        out_of_set = set(G) - set_ 
        if all(any((y, x) in G.edges() for y in set_) for x in out_of_set):
            out.add(set_)
    return out

def get_core(G):
    return get_outwardly_stable(G) & get_internally_stable(G)

print(f"For graph \n\t{G1.edges()}\nCore is\n\t{get_core(G1)}\n")


G2 = nx.DiGraph()
nodes = list('abcdefa')
for x, y in zip(nodes[:-1], nodes[1:]):
    G2.add_edge(x, y)
G2.add_edge('b', 'e')

print(f"For graph\n\t{G2.edges()}\nCore is\n\t{get_core(G2)}")

