from DataTypes.AgentType import AgentType
from FactoryAgent import FactoryAgent
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.initialize_logger import initialize_logger
import networkx as nx
from typing import Dict


class FactoryCreator:
    """"
    Simulation and agent initializer
    """

    def __init__(self, graph: nx.DiGraph, hostname: str = "localhost"):
        """"
        :param graph: graph representing connections and trust between agents (as edge parameter 'trust')
        :param hostname: hostname of the nodes in spade
        """
        self.graph = graph
        self.hostname = hostname
        self.root = None

    def initialize_simulation(self) -> Dict[int, FactoryAgent]:
        """
        Initialize simulation for some graph.
        :return: dictionary with (node_id, ExampleAgent) mapping
        """
        agents_ids = self.graph.nodes()
        root_id = int()

        for a_id in agents_ids:
            if str("car") in self.graph.nodes[a_id]["part"]:
                root_id = a_id

        neighbours = dict([
            (agent_id, dict(
                successors=list(self.graph.successors(agent_id)),
                predecessors=list(self.graph.predecessors(agent_id))
            )
             ) for agent_id in agents_ids
        ])
        agents = self._initialize_agents(agents_ids, neighbours, hostname=self.hostname)
        initialize_logger()
        for agent in agents.values():
            agent.start()

        self.root = agents[root_id]

        return agents

    def _initialize_agents(self, agent_ids, neighbours_lists,
                           basename="agent", hostname="localhost"):
        agent_usernames = dict([(agent_id, "{}_{}@{}".format(basename, agent_id, hostname))
                                for agent_id in agent_ids])
        agent_username_to_id = {v: k for k, v in agent_usernames.items()}
        AgentUsernameToIdMapper.agent_username_to_id = agent_username_to_id

        neighbours = dict([
            (agent_usernames[agent_id], dict(
                successors=[agent_usernames[neighbour_id] for neighbour_id in neighbours_lists[agent_id]['successors']],
                predecessors=[agent_usernames[neighbour_id] for neighbour_id in
                              neighbours_lists[agent_id]['predecessors']]
            )
             ) for agent_id in agent_ids])
        agents = dict()
        for agent_id in agent_ids:
            username = agent_usernames[agent_id]

            ##TODO It should be loaded from config
            agent_type_setter = {
                1:  AgentType.CAR,
                2:  AgentType.WHEEL,
                3:  AgentType.DOOR,
                4:  AgentType.ENGINE,
                69: AgentType.STORAGE
            }

            agents[agent_id] = FactoryAgent(username, username, neighbours=neighbours[username], agent_type=agent_type_setter.get(agent_id))
        return agents

