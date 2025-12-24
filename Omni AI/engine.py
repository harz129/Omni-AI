import asyncio
from actions import ActionExecutor
from database import DatabaseManager
from security import SecurityManager

class OmniEngine:
    def __init__(self, workflows):
        self.workflows = workflows
        self.executor = ActionExecutor()
        self.db = DatabaseManager()
        self.security = SecurityManager()

    async def execute_workflow(self, workflow_name):
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            print(f"Workflow {workflow_name} not found.")
            return

        actions = workflow.get('actions', [])
        print(f"Executing workflow: {workflow_name}")
        self.db.log_workflow(workflow_name, "started")

        for action_packet in actions:
            if isinstance(action_packet, dict):
                for action_type, params in action_packet.items():
                    if self.security.check_permission(action_type):
                        await self._run_action(action_type, params)
            elif isinstance(action_packet, str):
                if self.security.check_permission(action_packet):
                    await self._run_action(action_packet, None)
        
        self.db.log_workflow(workflow_name, "completed")

    async def _run_action(self, action_type, params):
        print(f"Running action: {action_type} with {params}")
        
        if action_type == "open_app":
            print(self.executor.open_app(params))
        elif action_type == "block_sites":
            print(self.executor.block_sites(params))
        elif action_type == "start_timer":
            print(self.executor.start_timer(params))
        elif action_type == "speak":
            # We will integrate the voice engine here
            print(self.executor.speak(params))
        elif action_type == "open_url":
            print(self.executor.open_url(params))
        elif action_type == "run_command":
            print(self.executor.run_command(params))
        else:
            print(f"Unknown action type: {action_type}")

        # Small delay between actions
        await asyncio.sleep(0.5)
