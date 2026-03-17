import subprocess
from tools.base_tool import BaseTool
from security.permission_manager import PermissionManager

class RunCommandTool(BaseTool):
    name = "run_command"
    description = "Execute a terminal command"

    def execute(self, **kwargs):
        try:
            command = kwargs.get("command")

            if not PermissionManager.is_command_allowed(command):
                return {
                    "success": False,
                    "result": None,
                    "error": "Command not allowed for security reasons"
                }

            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "success": True,
                "result": result.stdout,
                "error": result.stderr if result.stderr else None
            }
        
        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}