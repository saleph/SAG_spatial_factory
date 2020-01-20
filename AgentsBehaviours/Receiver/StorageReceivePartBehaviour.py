import traceback

from spade.behaviour import CyclicBehaviour

from DataTypes.MessageThread import MessageThread
from DataTypes.MessageThreadType import MessageThreadType
from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.message import _prepare_message


class StorageReceivePartBehaviour(CyclicBehaviour):
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
                receivedThread.ChangeMessageDirection()
                message_thread_str = receivedThread.ToJson()


                if receivedThread.message_thread_type == MessageThreadType.CarProduction:

                    # storage should only send back message to sender, not to all successors
                    for successor in self.agent.successors:
                        if AgentUsernameToIdMapper.agent_username_to_id[str(successor)] == sender_id:
                            message = _prepare_message(successor, dict(id=123, body="Storage -> Components and Root",
                                                                         thread=message_thread_str))
                            receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(successor)]
                            AgentActivityLogger._log(
                                "Message arrived at storage, so storage can take some resources and send message back upward")

                            #TODO Checking needed resources from body and fetching them from storage.
                            # Amount of stuff is about to be changed and it should take a few secs

                            await self.send(message)
                            if message.sent:
                                AgentActivityLogger._log(
                                    dict(msg_type="send", msg_id=msg.metadata["message_id"], sender=agent_id, receiver=receiver_id,
                                    thread=msg.thread, body=msg.body))
                            break



            else:
                print("{}: I did not received any message".format(agent_id))
        except Exception as e:
            print("exception in ", self.jid)
            traceback.print_exc(e)