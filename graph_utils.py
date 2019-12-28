# -*- coding: utf-8 -*-
import networkx as nx
import json
import os
import pathlib
import matplotlib.pyplot as plt
import pylab
from operator import itemgetter
from statistics import mean 

def dump(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    print("Dumping the graph into pickle in", filename)
    nx.write_gpickle(G, filename)
    print("Dumping sucessful")

def dump_geffi(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    print("Dumping the graph into gexf format in", filename)
    nx.write_gexf(G, filename)
    print("Dumping sucessful")

def load_geffi(filename):
    return nx.read_gexf(filename)

def load(filename):
    print("Loading pickled graph from", filename)
    if not os.path.isfile(filename):
        print("There is no cached graph")
        return None
    G = nx.read_gpickle(filename)
    print("Graph loaded from pickle")
    return G

def draw(G):
    # nx.draw_shell(G, with_labels=True, font_weight='bold')
    # plt.show()
    print("Start drawing the graph...")
    node_and_degree = G.degree()
    (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    # Create ego graph of main hub
    hub_ego = nx.ego_graph(G, largest_hub)
    # Draw graph
    pos = nx.spring_layout(hub_ego)
    nx.draw(hub_ego, pos, node_color='b', node_size=10, with_labels=False)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego, pos, nodelist=[largest_hub], node_size=50, node_color='r')
    plt.show()