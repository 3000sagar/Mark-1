from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """
    Base class for all MARK-1 tools.
    Every tool must define:
      - name
      - description
      - execute()
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool.

        Returns a dict like:
        {
            "success": True/False,
            "result": ...,
            "error": None or str
        }
        """
        pass