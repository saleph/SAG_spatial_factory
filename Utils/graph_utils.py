# -*- coding: utf-8 -*-
import networkx as nx
import json
import os
import pathlib
import matplotlib.pyplot as plt
import pylab
from operator import itemgetter
from statistics import mean 

def dump_binary(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    nx.write_gpickle(G, filename)

def load_binary(filename):
    if not os.path.isfile(filename):
        return None
    G = nx.read_gpickle(filename)
    return G

def dump_json(G, filename):
    directory = pathlib.Path(filename).parent
    directory.mkdir(parents=True, exist_ok=True)
    with open(filename, "w") as f:
        f.write(json.dumps(nx.node_link_data(G), indent=4))

def load_json(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, "r") as f:
        return nx.node_link_graph(json.loads(f.read()))

def draw_ego(G):
    # nx.draw_shell(G, with_labels=True, font_weight='bold')
    # plt.show()
    print("Start drawing the graph...")
    node_and_degree = G.degree()
    (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    # Create ego graph of main hub
    hub_ego = nx.ego_graph(G, largest_hub)
    # Draw graph
    pos = nx.spring_layout(hub_ego)
    nx.draw(hub_ego, pos, node_color='b', node_size=50, with_labels=False)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego, pos, nodelist=[largest_hub], node_size=100, node_color='r')
    plt.show()

def draw_with_node_attrib(G, attrib_name):
    labels = nx.get_node_attributes(G, attrib_name)
    pos = nx.spring_layout(G)
    nx.draw_networkx_labels(G, pos=pos, labels={n:lab for n,lab in labels.items() if n in pos})
    nx.draw(G, pos=pos)
    plt.show()