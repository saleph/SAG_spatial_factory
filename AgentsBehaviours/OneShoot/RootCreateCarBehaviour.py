import asyncio
from random import randint
import uuid

from spade.behaviour import OneShotBehaviour

from DataTypes.MessageDirection import MessageDirection
from DataTypes.MessageThread import MessageThread
from DataTypes.MessageThreadCounter import MessageThreadCounter
from DataTypes.MessageThreadType import MessageThreadType
from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.message import _prepare_message


class RootCreateCarBehaviour(OneShotBehaviour):

    def __init__(self, jid):
        super().__init__()
        self.jid = jid

    async def run(self):
        if len(self.agent.predecessors) == 0:
            print("no neigbhours in", self.jid)
            await asyncio.sleep(100)

        thread_id = str(uuid.uuid4())
        message_thread = MessageThread(thread_id, message_thread_type=MessageThreadType.CarProduction,
                                       message_direction=MessageDirection.Downward)
        message_thread_str = message_thread.ToJson()

        message_thread_counter = MessageThreadCounter(thread_id)
        AgentActivityLogger._log("Thread with id {0} added to thread list of agent {1}"
                                 .format(thread_id, '1'))

        for predecessor in self.agent.predecessors:
            message = _prepare_message(predecessor, dict(id=123, body="Root -> Components and Storage",
                                                         thread=message_thread_str))
            await self.send(message)
            if(message.sent):
                message_thread_counter.increaseCounter()
                AgentActivityLogger._log("Counter of thread {0} for agent {1} increased to {2}"
                                         .format(thread_id, '1', str(message_thread_counter.getCounterValue())))

            receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(predecessor)]
            agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]
            AgentActivityLogger._log(
                dict(msg_type="send", msg_id=message.metadata["message_id"], sender=agent_id,
                     receiver=receiver_id, thread=message_thread_str, body=message.body))

        if(message_thread_counter.getCounterValue() != 0):
            self.agent.message_thread_counter_list.append(message_thread_counter)


        await asyncio.sleep(randint(3, 10))