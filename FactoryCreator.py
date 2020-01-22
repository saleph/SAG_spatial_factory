from Config.factory_workflow import Workflow
from FactoryAgent import FactoryAgent
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.initialize_logger import initialize_logger
import networkx as nx
from typing import Dict


class FactoryCreator:
    """"
    Simulation and agent initializer
    """

    def __init__(self, graph: nx.DiGraph, workflow: Workflow, hostname: str = "localhost"):
        """"
        :param graph: graph representing connections and trust between agents (as edge parameter 'trust')
        :param hostname: hostname of the nodes in spade
        """
        self.graph = graph
        self.workflow = workflow
        self.hostname = hostname
        self.root = None
        self.agents = dict()
        self.full_neighbours_map = dict()
        self.agent_usernames = dict()
        self.respawn_after_breakdown = False
        storage_id = [id for id, attr in self.graph.nodes.items() if attr["type"] == "storage"][0]
        self.storage_username = "agent_{}@{}".format(storage_id, hostname)

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
        self._initialize_agents(agents_ids, neighbours, hostname=self.hostname)
        initialize_logger()
        for agent in self.agents.values():
            agent.start()

        self.root = self.agents[root_id]

        return self.agents

    def _initialize_agents(self, agent_ids, neighbours_lists,
                           basename="agent", hostname="localhost"):
        self.agent_usernames = dict([(agent_id, "{}_{}@{}".format(basename, agent_id, hostname))
                                     for agent_id in agent_ids])
        agent_username_to_id = {v: k for k, v in self.agent_usernames.items()}
        AgentUsernameToIdMapper.agent_username_to_id = agent_username_to_id

        self.full_neighbours_map = dict([
            (self.agent_usernames[agent_id], dict(
                successors=[self.agent_usernames[neighbour_id] for neighbour_id in
                            neighbours_lists[agent_id]['successors']],
                predecessors=[self.agent_usernames[neighbour_id] for neighbour_id in
                              neighbours_lists[agent_id]['predecessors']]
            )
             ) for agent_id in agent_ids])

        for agent_id in agent_ids:
            self.create_agent(agent_id)

    def create_agent(self, agent_id, respawn_after_breakdown=False):
        username = self.agent_usernames[agent_id]

        node = self.graph.nodes[agent_id]
        agent_type = node["type"]
        produced_components = node["part"]

        agent = FactoryAgent(username, username, workflow=self.workflow, factory_creator=self, storage_username=self.storage_username,
                             neighbours=self.full_neighbours_map[username], agent_type=agent_type, 
                             produced_components=produced_components)
        self.agents[agent_id] = agent
        self.agents[agent_id].respawn_after_breakdown = respawn_after_breakdown
        return agent
