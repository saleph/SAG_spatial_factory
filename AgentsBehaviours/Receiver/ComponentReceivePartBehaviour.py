import traceback

from spade.behaviour import CyclicBehaviour

from DataTypes.MessageDirection import MessageDirection
from DataTypes.MessageThread import MessageThread
from DataTypes.MessageThreadCounter import MessageThreadCounter
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
        self.agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]

    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            if msg is not None:
                await self.process_msg(msg)
            else:
                print("{}: I did not received any message".format(self.agent_id))

            if self.agent.respawn_after_breakdown is True:
                self.agent.send_respawn_notification();

        except Exception as e:
            print("exception in ", self.jid)
            traceback.print_exc(e)

    async def process_msg(self, msg):
        sender_id = AgentUsernameToIdMapper.agent_username_to_id[str(msg.sender)]

        received_thread = MessageThread(jsonStr=msg.thread)

        if msg.thread is None and msg.body == "respawn_notification":
            self.agent.resend_missing_messages(msg.sender)
        else:
            AgentActivityLogger._log(
                dict(msg_type="receive", msg_id=msg.metadata["message_id"], sender=sender_id, receiver=self.agent_id,
                     thread=msg.thread, body=msg.body))

            if received_thread.message_direction == MessageDirection.Downward:
                message_thread_counter = MessageThreadCounter(received_thread.id)
                AgentActivityLogger._log("Thread with id {0} added to thread list of agent {1}"
                                            .format(received_thread.id, str(self.agent_id)))

                body="Component -> Components and Storage"

                #TODO Body content filtering. It's not so diffucult as the desc is very long.
                # We want to check what agent can do with list of resources.
                # As if we have non-storage component, so it doesnt know what can do with 'steel', because it produces
                # engines (for instance this is a engine actor). It should remove basic resources from list of resouces in body
                # like steel or complex resources which it doesnt produce like doors and wheels. Otherwise,
                # many agents multiplies the same order from root and storage uses a few times more resources than it should.
                # So main task for that kind of agent is to remove 'unknown' resources and convert its known resource like 'engine'
                # into basic resources and just send such resticted list of resources as body to its predecessors (children)
                # Agent is obligated to know stuff from factory_material.json like "what is engine made of?"

                for predecessor in self.agent.predecessors:
                    message = _prepare_message(predecessor, dict(id=123, body=body,
                                                                                thread=msg.thread))
                    receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(predecessor)]
                    await self.send(message)
                    if message.sent:
                        self.agent.sent_messages_registry.append(dict(sender=predecessor,
                                                                      thread=received_thread, body=body))
                        AgentActivityLogger._log("response added to registry")
                        message_thread_counter.increaseCounter()
                        AgentActivityLogger._log("Counter of thread {0} for agent {1} increased to {2}"
                                                    .format(message_thread_counter.thread_id, self.agent_id,
                                                            str(message_thread_counter.getCounterValue())))
                    AgentActivityLogger._log(
                        dict(msg_type="send", msg_id=msg.metadata["message_id"], sender=self.agent_id, receiver=receiver_id,
                            thread=msg.thread, body=msg.body))

                if message_thread_counter.getCounterValue() != 0:
                    self.agent.message_thread_counter_list.append(message_thread_counter)
                    pass

            else:
                index = -1
                for i, thread in enumerate(self.agent.message_thread_counter_list):
                    if thread.thread_id == received_thread.id:
                        index = i
                        break

                if index != -1:
                    AgentActivityLogger._log("Counter of thread {0} for agent {1} decreased to {2}"
                        .format(received_thread.id, self.agent_id, str(self.agent.message_thread_counter_list[index].getCounterValue() - 1)))

                    self.agent.remove_entry_from_sent_messages_registry(sender_id, received_thread.id)
                    if self.agent.message_thread_counter_list[index].decreaseCounter():
                        del self.agent.message_thread_counter_list[index]
                        AgentActivityLogger._log("Thread with id {0} removed from thread list of agent {1}"
                                                    .format(received_thread.id, str(self.agent_id)))

                        for successor in self.agent.successors:
                            message = _prepare_message(successor, dict(id=123, body="Component -> Components and Root",
                                                                        thread=msg.thread))
                            receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(successor)]
                            await self.send(message)
                            AgentActivityLogger._log(
                                dict(msg_type="send", msg_id=msg.metadata["message_id"], sender=self.agent_id,
                                        receiver=receiver_id,
                                        thread=msg.thread, body=msg.body))