import traceback
import json

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

    def __init__(self, jid, workflow, graph, produced_components):
        super().__init__()
        self.jid = jid
        self.agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]
        self.workflow = workflow
        self.graph = graph
        # here we assume that component agent can handle only single part
        self.produced_component = produced_components[0]

    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            if msg is not None:
                await self.process_msg(msg)
            else:
                print("{}: I did not received any message".format(self.agent_id))

        except Exception as e:
            print("exception in ", self.jid)
            traceback.print_exc(e)

        if self.agent.respawn_after_breakdown:
            self.agent.send_respawn_notification()

    async def process_msg(self, msg):
        sender_id = AgentUsernameToIdMapper.agent_username_to_id[str(msg.sender)]

        received_thread = MessageThread(jsonStr=msg.thread)

        if msg.thread is None and msg.body == "respawn_notification":
            if self.agent.was_ever_revived:
                # we are also respawned, so to avoid copies, we should skip this step
                self.agent.was_ever_revived = False
                self.agent.respawn_after_breakdown = False
            else:
                self.agent.resend_missing_messages(msg.sender)
        else:
            AgentActivityLogger._log(
                dict(msg_type="receive", msg_id=msg.metadata["message_id"], sender=sender_id, receiver=self.agent_id,
                     thread=msg.thread, body=msg.body))

            if received_thread.message_direction == MessageDirection.Downward:
                message_thread_counter = MessageThreadCounter(received_thread.id)
                AgentActivityLogger._log("Thread with id {0} added to thread list of agent {1}"
                                            .format(received_thread.id, str(self.agent_id)))

                body = json.dumps(self.workflow.get_ingredients(self.produced_component))
                for predecessor in self.agent.predecessors:
                    message = _prepare_message(predecessor, dict(id=123, body=body,
                                                                                thread=msg.thread))

                    receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(predecessor)]
                    agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]

                    receiver_part = self.graph.nodes[receiver_id]["part"][0]
                    agent_part = self.graph.nodes[agent_id]["part"][0]

                    if receiver_part in self.workflow.get_base_materials():
                        index = 1
                    else:
                        index = self.workflow.get_complex_ingredients_for_part_with_quantities(agent_part).get(
                            receiver_part)

                    for i in range(index):
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
                            thread=msg.thread, body=body))

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
                            agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]
                            msg_body = self.graph.nodes[agent_id]["part"][0]

                            AgentActivityLogger._log("PART: " + msg_body + " CREATED")
                            message = _prepare_message(successor, dict(id=123, body=msg_body,
                                                                        thread=msg.thread))
                            receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(successor)]
                            await self.send(message)
                            AgentActivityLogger._log(
                                dict(msg_type="send", msg_id=msg.metadata["message_id"], sender=self.agent_id,
                                        receiver=receiver_id,
                                        thread=msg.thread, body=msg.body))