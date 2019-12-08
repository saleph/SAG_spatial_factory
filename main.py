import networkx as nx
import sys
from initialize_simulation import initialize_simulation

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 1)
G.add_edge(3, 1)
G.add_edge(3, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)
initialize_simulation(G)
while True:
    data = sys.stdin.read()
    if data == 'x':
        break