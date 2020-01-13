from Utils import graph_utils
from Config.factory_workflow import Workflow
from FactoryCreator import FactoryCreator
import time


graph_file = "Config/factory_graph.json"
G = graph_utils.load_json(graph_file)
# graph_utils.draw_with_node_attrib(G, 'part')
workflow = Workflow("Config/factory_materials.json")

factoryCreator = FactoryCreator(G)
factoryCreator.initialize_simulation()

# wait for agents initialization
time.sleep(5)

factoryCreator.root.one_shot()
# while True:
#     number = input("Give number of cars: ")
#     for i in range(int(number)):
#         factoryCreator.root.one_shot()
