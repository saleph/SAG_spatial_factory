from spade.agent import Agent
from spade.template import Template

from AgentsBehaviours.OneShoot.AgentAfterBreakDownBehaviour import AgentAfterBreakDownBehaviour
from AgentsBehaviours.OneShoot.RetransmissionBehaviour import RetransmissionBehaviour
from AgentsBehaviours.OneShoot.RootCreateCarBehaviour import RootCreateCarBehaviour
from AgentsBehaviours.OneShoot.KillAgentBehaviour import KillAgentBehaviour
from AgentsBehaviours.Receiver.ComponentReceivePartBehaviour import ComponentReceivePartBehaviour
from AgentsBehaviours.Receiver.RootReceivePartBehaviour import RootReceivePartBehaviour
from AgentsBehaviours.Receiver.StorageReceivePartBehaviour import StorageReceivePartBehaviour
from AgentsBehaviours.Robustness.Heartbeat import Heartbeat
from AgentsBehaviours.Robustness.HeartbeatVerificator import HeartbeatVerificator
from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper


class FactoryAgent(Agent):
    """
    Spade agent of the factory process.
    """

    def kill(self):
        self.add_behaviour(KillAgentBehaviour())

    def one_shot(self):
        self.add_behaviour(RootCreateCarBehaviour(self.jid, self.workflow))

    def send_respawn_notification(self):
        self.add_behaviour(AgentAfterBreakDownBehaviour())

    def resend_missing_messages(self, respawned_target):
        self.add_behaviour(RetransmissionBehaviour(respawned_target))


    def __init__(self, jid, password, *, workflow, factory_creator, storage_username, verify_security=False, neighbours=None, agent_type=None, produced_components=None):
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
        self.produced_components = produced_components
        self.workflow = workflow

        template = Template()
        template.set_metadata("performative", "inform")
        self.common_template = template

        self.message_thread_counter_list = []
        self.sent_messages_registry = []
        self.respawn_after_breakdown = False

    def setAgentAsRootAgent(self):
        self.prepare_heartbeat()
        self.listen_behav = RootReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav, self.common_template)

    def setAgentAsComponentAgent(self):
        self.prepare_heartbeat()
        self.listen_behav = ComponentReceivePartBehaviour(self.jid, self.workflow, self.produced_components)
        self.add_behaviour(self.listen_behav, self.common_template)

    def setAgentAsStarageAgent(self):
        self.listen_behav = StorageReceivePartBehaviour(self.jid, self.workflow)
        self.add_behaviour(self.listen_behav, self.common_template)


    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))

        agentTypeSwitch = {
            "root": self.setAgentAsRootAgent,
            "component": self.setAgentAsComponentAgent,
            "storage": self.setAgentAsStarageAgent
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

    def remove_entry_from_sent_messages_registry(self, sender_id = None, thread_id = None):

        entries_ids_to_remove = []
        include_all_threads = True if thread_id is None else False

        for i in range(len(self.sent_messages_registry)):
            temp_sender_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.sent_messages_registry[i]["sender"])]
            if sender_id == temp_sender_id and \
                    (include_all_threads is True or self.sent_messages_registry[i]["thread"].id == thread_id):
                entries_ids_to_remove.append(i)

        listSize = len(entries_ids_to_remove)

        for i in range(listSize):
            j = listSize - i - 1
            AgentActivityLogger._log("Deleted entry of {0} for thread {1} from {2} "
                                     .format(self.username, self.sent_messages_registry[entries_ids_to_remove[j]]["thread"].id,
                                    self.sent_messages_registry[entries_ids_to_remove[j]]["sender"]))
            del self.sent_messages_registry[entries_ids_to_remove[j]]






