import networkx as nx
import sys
import graph_utils
from factory_workflow import Workflow
from FactoryCreator import FactoryCreator
import time


graph_file = "factory_graph.json"
G = graph_utils.load_json(graph_file)
# graph_utils.draw_with_node_attrib(G, 'part')
workflow = Workflow("factory_materials.json")

factoryCreator = FactoryCreator(G)
factoryCreator.initialize_simulation()
factoryCreator.root.one()

# while True:
#     number = input("Give number of cars: ")
#     for i in range(int(number)):
#         factoryCreator.root.one
