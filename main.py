import networkx as nx
import sys
from initialize_simulation import initialize_simulation
import graph_utils
from factory_workflow import Workflow
import time

# G = nx.DiGraph()
# nodes = [
#     (1, dict(part=["car"])),
#     (2, dict(part=["wheel"])),
#     (3, dict(part=["door"])),
#     (4, dict(part=["engine"])),

#     (69, dict(part=["steel", "gum", "paint", "aluminum", "glass"]))  # storage
# ]
# G.add_nodes_from(nodes)
# edges = [
#     # car
#     (2, 1),
#     (3, 1),
#     (4, 1),
#     (69, 1),
#     # wheel
#     (69, 2),
#     # door
#     (69, 3),
#     # engine
#     (69, 4)
# ]
# G.add_edges_from(edges)

graph_file = "factory_graph.json"
G = graph_utils.load_json(graph_file)
graph_utils.draw_with_node_attrib(G, 'part')
workflow = Workflow("factory_materials.json")

#initialize_simulation(G)
