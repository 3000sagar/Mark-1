import logging
import os


class Logger:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("MARK1")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        agent_log = logging.FileHandler("logs/agent.log")
        agent_log.setFormatter(formatter)

        console_log = logging.StreamHandler()
        console_log.setFormatter(formatter)

        self.logger.addHandler(agent_log)
        self.logger.addHandler(console_log)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)


# global logger instance
logger = Logger()