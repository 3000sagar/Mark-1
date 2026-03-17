from runtime.session import Session
from runtime.command_handler import CommandHandler

class CLI:
    def __init__(self):
        self.session = Session()
        self.handler = CommandHandler(self.session)
        self.running = True

    def start(self):
        print("Mark-1 Started...")
        while self.running:

            command = input("Mark-1 > ")

            self.session.add_command(command)
            
            self.running = self.handler.handle(command)

