import networkx as nx
import sys
from initialize_simulation import initialize_simulation
import graph_utils
from factory_workflow import Workflow

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(2, 1)
G.add_edge(3, 1)
G.add_edge(3, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)

#graph_utils.dump_geffi(G, "geffi.gmfx")
#graph_utils.draw(graph_utils.load_geffi("geffi.gmfx"))
#factory_workflow.dump_json(factory_workflow.parts, "factory_desc.json")

workflow = Workflow("factory_desc.json")
print(workflow)
print(workflow.get_base_materials())
print(workflow.get_ingredients('car'))
#initialize_simulation(G)
#while True:
#    data = sys.stdin.read()
#    if data == 'x':
#        break