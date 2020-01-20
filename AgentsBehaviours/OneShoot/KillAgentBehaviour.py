from spade.behaviour import OneShotBehaviour


class KillAgentBehaviour(OneShotBehaviour):

    def __init__(self):
        super().__init__()

    async def run(self):
        self.exit_code = "Agent killed manually"
        await self.agent.stop()