# security/command_whitelist.py

ALLOWED_COMMANDS = {
    "python",
    "pip",
    "node",
    "npm",
    "git",
    "echo"
}

BLOCKED_PATTERNS = [
    "rm",
    "del",
    "format",
    "shutdown",
    "reboot",
    "system32",
    "mkfs"
]