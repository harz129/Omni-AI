import yaml
import os

class WorkflowLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.workflows = {}

    def load_workflows(self):
        if not os.path.exists(self.config_path):
            print(f"Config file not found: {self.config_path}")
            return {}
        
        with open(self.config_path, 'r') as file:
            try:
                self.workflows = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(f"Error parsing YAML: {exc}")
                self.workflows = {}
        return self.workflows

    def get_workflow(self, trigger_name):
        # Find workflow by trigger string or name
        for name, data in self.workflows.items():
            if data.get('trigger') == trigger_name or name == trigger_name:
                return data
        return None
