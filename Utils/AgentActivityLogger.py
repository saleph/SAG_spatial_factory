import logging


class AgentActivityLogger():
    logger = logging.getLogger("factory")

    @classmethod
    def _log(cls, message: dict):
        cls.logger.debug(message)