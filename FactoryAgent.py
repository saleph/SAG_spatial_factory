import asyncio
import logging
import traceback
from random import sample, randint

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
import time
from spade.template import Template


def _prepare_message(receiver, information):
    msg = Message(to=receiver)
    msg.body = information['body']
    msg.set_metadata("performative", "inform")
    msg.set_metadata("message_id", str(information['id']))
    return msg


class FactoryAgent(Agent):
    """
    Spade agent of the factory process.
    """
    logger = logging.getLogger("factory")
    agent_username_to_id = dict()

    @classmethod
    def _log(cls, message: dict):
        cls.logger.debug(message)

    def one_shot(self):
        self.add_behaviour(self.InitCarCreationBehaviour(self.jid))

    class InitCarCreationBehaviour(OneShotBehaviour):

        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            if len(self.agent.predecessors) == 0:
                print("no neigbhours in", self.jid)
                await asyncio.sleep(100)

            for predecessor in self.agent.predecessors:
                message = _prepare_message(predecessor, dict(id=123, body="hood (here will go class instance)"))
                await self.send(message)

                receiver_id = FactoryAgent.agent_username_to_id[str(predecessor)]
                agent_id = FactoryAgent.agent_username_to_id[str(self.jid)]
                FactoryAgent._log(
                    dict(msg_type="send", msg_id=message.metadata["message_id"], sender=agent_id,
                         receiver=receiver_id,
                         body=message.body))

            await asyncio.sleep(randint(3, 10))

    # class ProducePartCyclicBehaviour(CyclicBehaviour):
    #     """
    #     Part assembly behaviour as spade CyclicBehaviour.
    #     """
    #     def __init__(self, jid):
    #         super().__init__()
    #         self.jid = jid
    #
        # async def run(self):
        #     if len(self.agent.successors) == 0:
        #         print("no neigbhours in", self.jid)
        #         await asyncio.sleep(100)
        #
        #     for successor in self.agent.successors:
        #         message = _prepare_message(successor, dict(id=123, body="hood (here will go class instance)"))
        #         await self.send(message)
        #
        #         receiver_id = FactoryAgent.agent_username_to_id[str(successor)]
        #         agent_id = FactoryAgent.agent_username_to_id[str(self.jid)]
        #         FactoryAgent._log(
        #             dict(msg_type="send", msg_id=message.metadata["message_id"], sender=agent_id, receiver=receiver_id,
        #                     body=message.body))
        #
        #     await asyncio.sleep(randint(3, 10))

    class ReceivePartBehaviour(CyclicBehaviour):
        """
        Gossip receiver behaviour as spade CyclicBehaviour.
        """
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            try:
                msg = await self.receive(timeout=10)
                agent_id = FactoryAgent.agent_username_to_id[str(self.jid)]
                if msg is not None:
                    sender_id = FactoryAgent.agent_username_to_id[str(msg.sender)]
                    FactoryAgent._log(
                        dict(msg_type="receive", msg_id=msg.metadata["message_id"], sender=sender_id, receiver=agent_id,
                             body=msg.body))
                else:
                    print("{}: I did not received any message".format(agent_id))
            except Exception as e:
                print("exception in ", self.jid)
                traceback.print_exc(e)

    def __init__(self, jid, password, verify_security=False, neighbours=None):
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

    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))

        # if self.successors:
        #     self.propagate_behav = self.ProducePartCyclicBehaviour(self.jid)
        #     self.add_behaviour(self.propagate_behav)
        
        # if self.predecessors:
        self.listen_behav = self.ReceivePartBehaviour(self.jid)
        self.add_behaviour(self.listen_behav)
