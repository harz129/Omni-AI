import asyncio
import sys
from workflows import WorkflowLoader
from engine import OmniEngine
from intents import IntentDetector
from voice import VoiceModule

async def main():
    print("--- OmniAI Starting ---")
    
    # Initialization
    loader = WorkflowLoader("config.yaml")
    workflows = loader.load_workflows()
    
    if not workflows:
        print("No workflows found. Please check config.yaml.")
        return

    engine = OmniEngine(workflows)
    detector = IntentDetector(workflows)
    voice = VoiceModule()

    voice.speak("Omni AI is now online and ready to assist you.")

    while True:
        mode = input("\nEnter 'v' for Voice command, 't' for Text command, or 'q' to Quit: ").lower()
        
        command = ""
        if mode == 'v':
            command = voice.listen()
        elif mode == 't':
            command = input("Enter command: ")
        elif mode == 'q':
            voice.speak("Shutting down Omni AI. Goodbye.")
            break
        else:
            print("Invalid mode.")
            continue

        if command:
            # Detect intent
            workflow_name = detector.detect_intent(command)
            
            if workflow_name:
                print(f"Match found: {workflow_name}")
                await engine.execute_workflow(workflow_name)
            else:
                print("I couldn't find a matching workflow for that command.")
                voice.speak("I'm sorry, I don't know how to handle that.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
