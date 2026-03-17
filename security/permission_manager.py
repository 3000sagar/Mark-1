from security.command_whitelist import ALLOWED_COMMANDS, BLOCKED_PATTERNS

class PermissionManager:

    @staticmethod
    def is_command_allowed(command: str) -> bool:
        command = command.strip().lower()

        for pattern in BLOCKED_PATTERNS:
            if pattern in command:
                return False
            
        base_command = command.split(" ")[0]

        if base_command not in ALLOWED_COMMANDS:
            return False
        
        return True