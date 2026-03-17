from tools.tool_registry import ToolRegistry
from tools.file_tools import ReadFileTool, WriteFileTool, ListDirectoryTool
from tools.terminal_tools import RunCommandTool
from core.planner import Planner
from core.executor import Executor
from core.goal_engine import GoalEngine
from models.ollama_model import OllamaModel


class CommandHandler:
    def __init__(self, session):
        self.session = session

        # 🔥 Core components
        self.registry = ToolRegistry()
        self.model = OllamaModel()
        self.planner = Planner()
        self.executor = Executor(self.registry, self.model, self.planner)
        self.goal_engine = GoalEngine(self.planner, self.executor, self.model)

        # 🔧 Register tools
        self.registry.register(ReadFileTool())
        self.registry.register(WriteFileTool())
        self.registry.register(ListDirectoryTool())
        self.registry.register(RunCommandTool())

    def handle(self, command: str):
        command = command.strip()

        # 🔹 Basic commands
        if command == "help":
            self.show_help()
            return True

        if command == "exit":
            print("      Mark1 is shutting Down...")
            return False

        if command == "":
            return True

        # 🔥 GOAL MODE
        if command.startswith("goal "):
            goal = command.replace("goal ", "")
            self.goal_engine.run(goal)
            return True

        # 🔥 INTENT DETECTION (CRITICAL FIX)
        if not self.is_task(command):
            response = self.model.generate(command)
            print(response)
            return True

        # 🔥 MEMORY STORE
        self.executor.memory.add("user", command)

        # 🔥 NORMAL FLOW (Planner → Executor)
        context = self.executor.memory.get_recent_context(3)
        plan = self.planner.plan(command, context)

        if not plan:
            print("⚠️ Failed to generate plan.")
            return True

        try:
            result = self.executor.execute(plan, command)
            print(result)

        except Exception as e:
            print("⚠️ Execution failed:", e)

        return True

    def is_task(self, command: str) -> bool:
        """
        Decide whether input is TASK or CHAT using LLM
        """
        prompt = f"""
Classify the user input:

"{command}"

Is this a TASK (requires tools like file, command, system action)
or just CHAT (conversation, question, greeting)?

Answer ONLY:
TASK or CHAT
"""
        response = self.model.generate(prompt)

        return "TASK" in response.upper()

    def show_help(self):
        print("Available Commands:- ")
        print("  help                - show available commands")
        print("  exit                - shutdown MARK-1")
        print("  read <file>         - read file from workspace")
        print("  write <file> <txt>  - write content to file")
        print("  list [dir]          - list directory contents")
        print("  run <command>       - execute terminal command")
        print("  goal <task>         - run autonomous goal")