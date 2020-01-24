from spade.behaviour import OneShotBehaviour
from Utils.AgentActivityLogger import AgentActivityLogger

class KillAgentBehaviour(OneShotBehaviour):

    def __init__(self):
        super().__init__()

    async def run(self):
        self.exit_code = "Agent killed manually"
        AgentActivityLogger._log("######## about to kill agent {}".format(self.agent.jid))
        await self.agent.stop()