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
        self.agents = dict()
        self.full_neighbours_map = dict()
        self.agent_usernames = dict()
        self.respawn_after_breakdown = False;

    def initialize_simulation(self) -> Dict[int, FactoryAgent]:
        """
        Initialize simulation for some graph.
        :return: dictionary with (node_id, ExampleAgent) mapping
        """
        agents_ids = self.graph.nodes()
        root_id = int()
        storage_username = ""
        agent_type_setter = {}

        for a_id in agents_ids:
            if str("car") in self.graph.nodes[a_id]["part"]:
                root_id = a_id
                agent_type_setter[a_id] = AgentType.CAR
            elif str("wheel") in self.graph.nodes[a_id]["part"]:
                agent_type_setter[a_id] = AgentType.WHEEL
            elif str("door") in self.graph.nodes[a_id]["part"]:
                agent_type_setter[a_id] = AgentType.DOOR
            elif str("engine") in self.graph.nodes[a_id]["part"]:
                agent_type_setter[a_id] = AgentType.ENGINE
            else:
                agent_type_setter[a_id] = AgentType.STORAGE
                storage_username = "agent_" + str(a_id) + "@localhost"

        neighbours = dict([
            (agent_id, dict(
                successors=list(self.graph.successors(agent_id)),
                predecessors=list(self.graph.predecessors(agent_id))
            )
             ) for agent_id in agents_ids
        ])
        self._initialize_agents(agents_ids, neighbours, storage_username, agent_type_setter, hostname=self.hostname)
        initialize_logger()
        for agent in self.agents.values():
            agent.start()

        self.root = self.agents[root_id]

        return self.agents

    def _initialize_agents(self, agent_ids, neighbours_lists, storage_username, agent_type_setter,
                           basename="agent", hostname="localhost"):
        self.agent_usernames = dict([(agent_id, "{}_{}@{}".format(basename, agent_id, hostname))
                                for agent_id in agent_ids])
        agent_username_to_id = {v: k for k, v in self.agent_usernames.items()}
        AgentUsernameToIdMapper.agent_username_to_id = agent_username_to_id

        self.full_neighbours_map = dict([
            (self.agent_usernames[agent_id], dict(
                successors=[self.agent_usernames[neighbour_id] for neighbour_id in neighbours_lists[agent_id]['successors']],
                predecessors=[self.agent_usernames[neighbour_id] for neighbour_id in
                              neighbours_lists[agent_id]['predecessors']]
            )
             ) for agent_id in agent_ids])

        for agent_id in agent_ids:
            self.create_agent(agent_id, storage_username, agent_type_setter)


    def create_agent(self, agent_id, storage_username, agent_type_setter, respawn_after_breakdown = False):
        username = self.agent_usernames[agent_id]

        agent = FactoryAgent(username, username, factory_creator=self, storage_username=storage_username,
                neighbours=self.full_neighbours_map[username], agent_type=agent_type_setter.get(agent_id))
        self.agents[agent_id] = agent
        self.agents[agent_id].respawn_after_breakdown = respawn_after_breakdown;
        return agent

