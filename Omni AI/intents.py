import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class IntentDetector:
    def __init__(self, workflows):
        self.workflows = workflows
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found in environment.")

    def detect_intent(self, user_input):
        # 1. First check for exact trigger matches
        for name, data in self.workflows.items():
            if data.get('trigger', '').lower() == user_input.lower():
                return name

        # 2. If no exact match and LLM is available, use it to find the best workflow
        if self.model:
            workflow_list = list(self.workflows.keys())
            prompt = f"""
            Available workflows: {', '.join(workflow_list)}
            
            User command: "{user_input}"
            
            Identify which of the available workflows best matches the user's command. 
            Respond ONLY with the name of the workflow. If none match, respond with 'None'.
            """
            try:
                response = self.model.generate_content(prompt)
                match = response.text.strip()
                if match in workflow_list:
                    return match
            except Exception as e:
                print(f"LLM Error: {e}")
        
        return None
