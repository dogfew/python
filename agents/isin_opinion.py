 
import random
import networkx as nx
import numpy as np
import pandas as pd

# constants
N = 20
M = 3
mu = 0
sigma = 1
J = 0.25
iters = 20


def init_network():
    G = nx.barabasi_albert_graph(N, M, seed=42)
    states = np.random.choice([-1, 1], size=len(G.nodes))
    df = pd.DataFrame({"node": G.nodes, "state": states})
    df['neighbors'] = df['node'].apply(lambda node: list(G.neighbors(node)))
    df.index = df.node
    df = df.drop(columns=['node'])
    return df

def compute_iter(df):
    # calc neighbor thoughts for each node
    df['neighbor_thoughts'] = df['neighbors'].map(lambda x: df.iloc[x]['state'].sum())
    # calc eps
    eps_minus = np.random.gumbel(mu, sigma, size=len(df))
    eps_plus = np.random.gumbel(mu, sigma, size=len(df))
    # generate utility
    u_minus = -J * df['neighbor_thoughts'] + eps_minus
    u_plus = J * df['neighbor_thoughts'] + eps_plus
    new_state = np.sign(u_plus - u_minus)
    # change states
    df['state'] = new_state
    return df

if __name__ == '__main__':
    df = init_network()
    for i in range(iters):
        df = compute_iter(df)
        print(f"Iter: {i + 1}, plus_%: {(df['state'] == 1).sum() / len(df)}, neg_%: {(df['state'] == -1).sum() / len(df)}, mean: {df['state'].mean()}")
