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


class KillAgentBehaviour(OneShotBehaviour):

    def __init__(self):
        super().__init__()

    async def run(self):
        self.exit_code = "Agent killed manually"
        await self.agent.stop()