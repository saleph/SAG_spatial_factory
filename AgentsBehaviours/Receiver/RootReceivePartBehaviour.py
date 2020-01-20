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


                received_thread = MessageThread(jsonStr=msg.thread)

                if msg.thread is None and msg.body == "respawn_notification":
                    self.agent.resend_missing_messages(msg.sender)

                elif received_thread.message_thread_type == MessageThreadType.CarProduction:

                    AgentActivityLogger._log(
                        dict(msg_type="receive", msg_id=msg.metadata["message_id"], sender=sender_id, receiver=agent_id,
                             thread=msg.thread, body=msg.body))

                    message_thread_id = received_thread.id

                    index = -1
                    for i, thread in enumerate(self.agent.message_thread_counter_list):
                        if thread.thread_id == message_thread_id:
                            index = i
                            break

                    if index != -1:
                        AgentActivityLogger._log("Counter of thread {0} for agent {1} decreased to {2}"
                            .format(received_thread.id, '1', str(self.agent.message_thread_counter_list[index].getCounterValue()-1)))
                        self.agent.remove_entry_from_sent_messages_registry(sender_id, received_thread.id)
                        if self.agent.message_thread_counter_list[index].decreaseCounter():
                            del self.agent.message_thread_counter_list[index]
                            AgentActivityLogger._log("Thread with id {0} removed from thread list of agent {1}"
                                                     .format(received_thread.id, '1'))
                            AgentActivityLogger._log("CAR CREATED")




            else:
                print("{}: I did not received any message".format(agent_id))
        except Exception as e:
            print("exception in ", self.jid)
            traceback.print_exc(e)