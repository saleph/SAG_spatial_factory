import traceback

from spade.behaviour import CyclicBehaviour

from DataTypes.MessageDirection import MessageDirection
from DataTypes.MessageThread import MessageThread
from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.message import _prepare_message


class ComponentReceivePartBehaviour(CyclicBehaviour):
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

                if receivedThread.message_direction == MessageDirection.Downward:

                    for predecessor in self.agent.predecessors:
                        message = _prepare_message(predecessor, dict(id=123, body="Component -> Components and Storage",
                                                                                  thread=msg.thread))
                        receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(predecessor)]
                        await self.send(message)
                        AgentActivityLogger._log(
                            dict(msg_type="send", msg_id=msg.metadata["message_id"], sender=agent_id, receiver=receiver_id,
                             thread=msg.thread, body=msg.body))

                ##TODO Waiting until all responses come back and sending them upward

                else:

                    ##########################Temporary section#########################################################
                    ##this section should be handled in component one shoot after all request bring responses
                    for successor in self.agent.successors:
                        message = _prepare_message(successor, dict(id=123, body="Component -> Components and Root",
                                                                   thread=msg.thread))
                        receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(successor)]
                        await self.send(message)
                        AgentActivityLogger._log(
                            dict(msg_type="send", msg_id=msg.metadata["message_id"], sender=agent_id,
                                 receiver=receiver_id,
                                 thread=msg.thread, body=msg.body))
                    ##########################Temporary section#########################################################

            else:
                print("{}: I did not received any message".format(agent_id))
        except Exception as e:
            print("exception in ", self.jid)
            traceback.print_exc(e)