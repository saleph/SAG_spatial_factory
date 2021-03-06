import asyncio
from random import randint
import uuid
import json

from spade.behaviour import OneShotBehaviour

from DataTypes.MessageDirection import MessageDirection
from DataTypes.MessageThread import MessageThread
from DataTypes.MessageThreadCounter import MessageThreadCounter
from DataTypes.MessageThreadType import MessageThreadType
from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.message import _prepare_message


class RootCreateCarBehaviour(OneShotBehaviour):

    def __init__(self, jid, workflow, graph):
        super().__init__()
        self.jid = jid
        self.workflow = workflow
        self.graph = graph
        self.agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]

    async def run(self):
        if len(self.agent.predecessors) == 0:
            print("no neigbhours in", self.jid)
            await asyncio.sleep(100)

        thread_id = str(uuid.uuid4())
        message_thread = MessageThread(thread_id, message_thread_type=MessageThreadType.RootComponentProduction,
                                       message_direction=MessageDirection.Downward)
        message_thread_str = message_thread.ToJson()

        message_thread_counter = MessageThreadCounter(thread_id)
        AgentActivityLogger._log("Thread with id {0} added to thread list of agent {1}"
                                 .format(thread_id, '1'))

        for predecessor in self.agent.predecessors:
            body = json.dumps(self.workflow.get_ingredients("car"))
            message = _prepare_message(predecessor, dict(id=123, body=body,
                                                         thread=message_thread_str))

            receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(predecessor)]
            agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]

            receiver_part = self.graph.nodes[receiver_id]["part"][0]
            agent_part = self.graph.nodes[agent_id]["part"][0]

            if receiver_part in self.workflow.get_base_materials():
                index = 1
            else:
                index = self.workflow.get_complex_ingredients_for_part_with_quantities(agent_part).get(receiver_part)

            for i in range(index):
                await self.send(message)
                if(message.sent):
                    self.agent.sent_messages_registry.append(dict(sender=predecessor,thread=message_thread,body=body))
                    AgentActivityLogger._log("response added to registry")
                    message_thread_counter.increaseCounter()
                    AgentActivityLogger._log("Counter of thread {0} for agent {1} increased to {2}"
                                             .format(thread_id, '1', str(message_thread_counter.getCounterValue())))

            AgentActivityLogger._log(
                dict(msg_type="send", msg_id=message.metadata["message_id"], sender=agent_id,
                     receiver=receiver_id, thread=message_thread_str, body=message.body))

        if(message_thread_counter.getCounterValue() != 0):
            self.agent.message_thread_counter_list.append(message_thread_counter)


        await asyncio.sleep(randint(3, 10))