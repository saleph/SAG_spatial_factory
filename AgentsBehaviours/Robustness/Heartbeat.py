import traceback

from spade.behaviour import CyclicBehaviour
import asyncio

from Utils.message import _prepare_system_control_message


class Heartbeat(CyclicBehaviour):
    """
    Heartbeat sender implementation.
    """
    # heartbeat rate in Hz
    rate = 0.5
    performative = "heartbeat"

    def __init__(self, successors):
        super().__init__()
        self.successors = successors

    async def run(self):
        for successor in self.successors:
            try:
                await self.send_heartbeat(successor)
            except Exception as e:
                print("exception in Heartbeat sender")
                traceback.print_exc(e)
        await asyncio.sleep(1/Heartbeat.rate)

    async def send_heartbeat(self, successor):
        msg = _prepare_system_control_message(successor, performative=Heartbeat.performative)
        await self.send(msg)