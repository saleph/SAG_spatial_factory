import traceback

from spade.behaviour import CyclicBehaviour

from DataTypes.MessageThread import MessageThread
from DataTypes.MessageThreadType import MessageThreadType
from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper


class RootReceivePartBehaviour(CyclicBehaviour):
    """
    Gossip receiver behaviour as spade CyclicBehaviour.
    """

    def __init__(self, jid):
        super().__init__()
        self.jid = jid

    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]
            if msg is not None:
                sender_id = AgentUsernameToIdMapper.agent_username_to_id[str(msg.sender)]

                AgentActivityLogger._log(
                    dict(msg_type="receive", msg_id=msg.metadata["message_id"], sender=sender_id, receiver=agent_id,
                         thread=msg.thread, body=msg.body))

                receivedThread = MessageThread(jsonStr=msg.thread)

                ##########################Temporary section#############################################################
                ##this section should be handled in component one shoot after all request bring responses
                if receivedThread.message_thread_type == MessageThreadType.CarProduction:
                    pass
                ########################################################################################################

            else:
                print("{}: I did not received any message".format(agent_id))
        except Exception as e:
            print("exception in ", self.jid)
            traceback.print_exc(e)