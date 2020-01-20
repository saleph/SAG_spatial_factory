import asyncio
from random import randint

from spade.behaviour import OneShotBehaviour

from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.message import _prepare_message


class RetransmissionBehaviour(OneShotBehaviour):

    def __init__(self, respawned_agent):
        super().__init__()
        self.respawned_agent = respawned_agent

    async def run(self):
        if len(self.agent.sent_messages_registry) == 0:
            print("no entries for ", self.jid)
            await asyncio.sleep(100)

        else:
            list_size= len(self.agent.sent_messages_registry)
            for i in range(list_size):
                respawned_agent_fullname = "{0}@{1}".format(self.respawned_agent.localpart, self.respawned_agent.domain)
                if self.agent.sent_messages_registry[i]["sender"] == respawned_agent_fullname:
                    message_thread_str = self.agent.sent_messages_registry[i]["thread"].ToJson()
                    message = _prepare_message(respawned_agent_fullname, dict(id=123,
                            body=self.agent.sent_messages_registry[i]["body"], thread=message_thread_str))
                    await self.send(message)
                    if message.sent:
                        AgentActivityLogger._log("Retransmitted message sent to {0} from {1}"
                                                 .format(self.respawned_agent, self.agent.jid))

        await asyncio.sleep(randint(3, 10))