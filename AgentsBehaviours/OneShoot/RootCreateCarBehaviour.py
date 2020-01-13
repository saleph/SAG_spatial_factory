import asyncio
from random import randint

from spade.behaviour import OneShotBehaviour

from DataTypes.MessageDirection import MessageDirection
from DataTypes.MessageThread import MessageThread
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

        message_thread = MessageThread(id=0, message_thread_type=MessageThreadType.CarProduction,
                                       message_direction=MessageDirection.Downward)
        message_thread_str = message_thread.ToJson()

        for predecessor in self.agent.predecessors:
            message = _prepare_message(predecessor, dict(id=123, body="Root -> Components and Storage",
                                                         thread=message_thread_str))
            await self.send(message)

            receiver_id = AgentUsernameToIdMapper.agent_username_to_id[str(predecessor)]
            agent_id = AgentUsernameToIdMapper.agent_username_to_id[str(self.jid)]
            AgentActivityLogger._log(
                dict(msg_type="send", msg_id=message.metadata["message_id"], sender=agent_id,
                     receiver=receiver_id, thread=message_thread_str, body=message.body))

        ##TODO Waiting until all responses come back and finishing production

        await asyncio.sleep(randint(3, 10))