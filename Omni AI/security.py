import os

class SecurityManager:
    _SENSITIVE_COMMANDS = ["rm", "del", "format", "mkfs", "chmod", "chown"]

    @staticmethod
    def is_safe_command(command):
        command_lower = command.lower()
        for sensitive in SecurityManager._SENSITIVE_COMMANDS:
            if sensitive in command_lower.split():
                return False
        return True

    @staticmethod
    def check_permission(action_type):
        # In a real app, this could check a config file or prompt user
        # For now, we return True but log the check
        print(f"[Security] Permission check for: {action_type}")
        return True
