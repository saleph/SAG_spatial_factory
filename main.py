from Utils import graph_utils
from Config.factory_workflow import Workflow
from FactoryCreator import FactoryCreator
import time
import sys
import random

graph_file = "Config/factory_graph.json"
G = graph_utils.load_json(graph_file)
# graph_utils.draw_with_node_attrib(G, 'part')
workflow = Workflow("Config/factory_materials.json")

factoryCreator = FactoryCreator(G, workflow)

agents_ids = []
for n in G.nodes:
    agents_ids.append(n)

if len(sys.argv) <= 1:
    print("Scenario was not selected")
else:
    scenario = int(sys.argv[1])
    if scenario == 1:
        """"
            killing one random agent
        """
        factoryCreator.initialize_simulation()
        # wait for agents initialization
        time.sleep(5)
        factoryCreator.root.one_shot()
        factoryCreator.agents[random.choice(agents_ids)].kill()
    elif scenario == 2:
        """"
            killing half of agents        
        """
        factoryCreator.initialize_simulation()
        # wait for agents initialization
        time.sleep(5)
        factoryCreator.root.one_shot()
        for e in random.sample(agents_ids, int(len(agents_ids)/2)):
            factoryCreator.agents[e].kill()
    elif scenario == 3:
        """"
            killing whole agents
        """
        factoryCreator.initialize_simulation()
        # wait for agents initialization
        time.sleep(5)
        factoryCreator.root.one_shot()
        for e in agents_ids:
            factoryCreator.agents[e].kill()
    else:
        print("Wrong number of scenario")
