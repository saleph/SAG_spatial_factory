import logging
import time


def initialize_logger() -> logging.Logger:
    """
    Initialize and return default root logger. After this function is called,
    the logger can be also retried directly via logging.getLogger()
    :return: logger
    """
    logger = logging.getLogger("factory")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(
        'Logs/factory_{0}.log'.format(time.strftime("%Y%m%d-%H%M%S")))
    file_formatter = logging.Formatter(
        "{'time':'%(asctime)s', " +
        "'level': '%(levelname)s', 'message': %(message)s}"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        '%(asctime)-15s %(levelname)-8s %(message)s'
    )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger
