from typing import Dict
from tools.base_tool import BaseTool



class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        if tool.name in self.tools:
            raise ValueError(f"Tool '{tool.name}' already registered")

        self.tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")

        return self.tools[name]

    def list_tools(self):
        return list(self.tools.keys())
    
