import asyncio
import traceback
from random import sample, randint

from spade.agent import Agent
from spade.template import Template

from AgentsBehaviours.OneShoot.RootCreateCarBehaviour import RootCreateCarBehaviour
from AgentsBehaviours.OneShoot.KillAgentBehaviour import KillAgentBehaviour
from AgentsBehaviours.Receiver.ComponentReceivePartBehaviour import ComponentReceivePartBehaviour
from AgentsBehaviours.Receiver.RootReceivePartBehaviour import RootReceivePartBehaviour
from AgentsBehaviours.Receiver.StorageReceivePartBehaviour import StorageReceivePartBehaviour
from AgentsBehaviours.Robustness.Heartbeat import Heartbeat
from AgentsBehaviours.Robustness.HeartbeatVerificator import HeartbeatVerificator
from DataTypes.AgentType import AgentType


class FactoryAgent(Agent):
    """
    Spade agent of the factory process.
    """

    def kill(self):
        self.add_behaviour(KillAgentBehaviour())

    def one_shot(self):
        self.add_behaviour(RootCreateCarBehaviour(self.jid))


    def __init__(self, jid, password, *, factory_creator, storage_username, verify_security=False, neighbours=None, agent_type=None):
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
        self.factory_creator = factory_creator
        self.storage_username = storage_username

        template = Template()
        template.set_metadata("performative", "inform")
        self.common_template = template

        self.message_thread_counter_list = []

    def setAgentAsRootAgent(self):
        self.prepare_heartbeat()
        self.listen_behav = RootReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav, self.common_template)

    def setAgentAsComponentAgent(self):
        self.prepare_heartbeat()
        self.listen_behav = ComponentReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav, self.common_template)

    def setAgentAsStarageAgent(self):
        self.listen_behav = StorageReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav, self.common_template)


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

    def prepare_heartbeat(self):
        if self.successors:
            self.add_behaviour(Heartbeat(self.successors))

        predecessors_wo_storage = {v for v in self.predecessors if v != self.storage_username}
        if predecessors_wo_storage:
            template = Template()
            template.set_metadata("performative", Heartbeat.performative)
            heartbeat_verificator = HeartbeatVerificator(predecessors_wo_storage, agent_factory=self.factory_creator, owning_agent=self.name)
            self.add_behaviour(heartbeat_verificator, template)





