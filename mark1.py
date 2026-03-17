from runtime.cli import CLI
from utils.logger import logger


def main():
    logger.info("Mark-1 Started...")
    cli = CLI()
    cli.start()


    logger.info("Mark-1 Stopped.")

if __name__ == "__main__":
    main()