import asyncio
import traceback
from random import sample, randint

from spade.agent import Agent

from AgentsBehaviours.OneShoot.RootCreateCarBehaviour import RootCreateCarBehaviour
from AgentsBehaviours.Receiver.ComponentReceivePartBehaviour import ComponentReceivePartBehaviour
from AgentsBehaviours.Receiver.RootReceivePartBehaviour import RootReceivePartBehaviour
from AgentsBehaviours.Receiver.StorageReceivePartBehaviour import StorageReceivePartBehaviour
from DataTypes.AgentType import AgentType


class FactoryAgent(Agent):
    """
    Spade agent of the factory process.
    """


    def one_shot(self):
        self.add_behaviour(RootCreateCarBehaviour(self.jid))


    def __init__(self, jid, password, verify_security=False, neighbours=None, agent_type=None):
        """
        Simulation agent initializer.
        :param jid: agent username in XMPP server, e.g. 'agent 0'
        :param password: agent password in XMPP server, e.g. 'agent 0'
        :param verify_security: XMPP server parameter - whether agents should be verified or not
        :param neighbours: list of agents' username (e.g. 'agent 0') being the agent neighbours (for whom the agent can
        sent a message)
        """
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        if neighbours is None:
            neighbours = dict()
        self.username = jid
        self.neighbours = neighbours
        self.successors = self.neighbours['successors']
        self.predecessors = self.neighbours['predecessors']
        self.propagate_behav = None
        self.listen_behav = None
        self.agentType = agent_type

        self.message_thread_counter_list = []

    def setAgentAsRootAgent(self):
        self.listen_behav = RootReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav)

    def setAgentAsComponentAgent(self):
        self.listen_behav = ComponentReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav)

    def setAgentAsStarageAgent(self):
        self.listen_behav = StorageReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav)


    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))

        # if self.successors:
        #     self.propagate_behav = self.ProducePartCyclicBehaviour(self.jid)
        #     self.add_behaviour(self.propagate_behav)
        
        # if self.predecessors:

        agentTypeSwitch = {
            AgentType.CAR: self.setAgentAsRootAgent,
            AgentType.DOOR: self.setAgentAsComponentAgent,
            AgentType.WHEEL: self.setAgentAsComponentAgent,
            AgentType.ENGINE: self.setAgentAsComponentAgent,
            AgentType.STORAGE: self.setAgentAsStarageAgent,
            AgentType.UNKNOWN: Exception("Invalid agent type")
        }

        agentTypeSwitch.get(self.agentType, "Done")()





