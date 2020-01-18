import traceback

import networkx as nx
from spade.behaviour import CyclicBehaviour
import asyncio
import time
from Utils.AgentUsernameToIdMapper import AgentUsernameToIdMapper
from Utils.message import _prepare_system_control_message
from Utils.AgentActivityLogger import AgentActivityLogger


class HeartbeatVerificator(CyclicBehaviour):
    """
    Heartbeat receiver implementation. Restores the agent after lost contact.
    """
    # how many seconds heartbeats has to be lacking to trigger recovery procedure
    recovery_threshold = 5

    def __init__(self, predecessors, *, agent_factory, owning_agent):
        super().__init__()
        self.last_heartbeat_time = dict.fromkeys(predecessors, time.time())
        self.agent_factory = agent_factory
        self.owning_agent = owning_agent

    async def run(self):
        msg = await self.receive(timeout=2)
        if msg is not None:
            sender = "{}@{}".format(msg.sender.localpart, msg.sender.domain)
            self.last_heartbeat_time[sender] = time.time()
        await self.verify_and_recover()

    async def verify_and_recover(self):
        for predecessor, last_heartbeat in self.last_heartbeat_time.items():
            current_time = time.time()
            if current_time - last_heartbeat < HeartbeatVerificator.recovery_threshold:
                continue
            await self.recover(predecessor)
            self.last_heartbeat_time[predecessor] = time.time()

    async def recover(self, predecessor):
        print(">>>>>>>>>")
        AgentActivityLogger._log(dict(action="agent_recovery", actor=self.owning_agent, recovering_actor=predecessor))
        agent_id = AgentUsernameToIdMapper.agent_username_to_id[predecessor]
        agent = self.agent_factory.create_agent(agent_id)
        await agent.start()
