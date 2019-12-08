from spade import agent
from SimulationAgent import FactoryAgent
from initialize_logger import initialize_logger
import networkx as nx
from typing import Dict
import sys


def initialize_simulation(graph: nx.DiGraph, hostname: str = "localhost") -> Dict[int, FactoryAgent]:
    """
    Initialize simulation for some graph.
    :param graph: graph representing connections and trust between agents (as edge parameter 'trust')
    :param hostname: hostname of the nodes in spade
    :return: dictionary with (node_id, ExampleAgent) mapping
    """
    agents_ids = graph.nodes()
    neighbours = dict([(agent_id, list(graph.neighbors(agent_id))) for agent_id in agents_ids])
    agents = _initialize_agents(agents_ids, neighbours, hostname=hostname)
    initialize_logger()
    for agent in agents.values():
        agent.start()

    for agent in agents.values():
        agent.stop()

    return agents

def _initialize_agents(agent_ids, neighbours_lists,
                       basename="agent", hostname="localhost"):
    agent_usernames = dict([(agent_id, "{}_{}@{}".format(basename, agent_id, hostname))
                            for agent_id in agent_ids])
    agent_username_to_id = {v: k for k, v in agent_usernames.items()}
    FactoryAgent.agent_username_to_id = agent_username_to_id

    neighbours = dict([(agent_usernames[agent_id],
                        [agent_usernames[neighbour_id] for neighbour_id in neighbours_lists[agent_id]])
                       for agent_id in agent_ids])
    agents = dict()
    for agent_id in agent_ids:
        username = agent_usernames[agent_id]
        agents[agent_id] = FactoryAgent(username, username, neighbours=neighbours[username])
    return agents