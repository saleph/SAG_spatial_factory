import asyncio

from spade.behaviour import OneShotBehaviour

from Utils.AgentActivityLogger import AgentActivityLogger
from Utils.message import _prepare_respawn_notification


class AgentAfterBreakDownBehaviour(OneShotBehaviour):

    def __init__(self):
        super().__init__()

    async def run(self):
        if len(self.agent.successors) == 0:
            print("no neigbhours in", self.jid)
            await asyncio.sleep(100)
        else:
            for successor in self.agent.successors:
                message = _prepare_respawn_notification(successor)
                await self.send(message)
                if (message.sent):
                    self.agent.respawn_after_breakdown = False
                    AgentActivityLogger._log("Agent sends notification about its rebirth to successors")