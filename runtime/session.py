import uuid
from datetime import datetime

class Session:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.command_history = []

    def add_command(self, command : str):
        self.command_history.append(command)

    def get_history(self):
        return self.command_history