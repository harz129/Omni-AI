import subprocess
import os
import time
import webbrowser
import psutil
import pyautogui

class ActionExecutor:
    @staticmethod
    def open_app(app_path):
        try:
            os.startfile(app_path)
            return f"Opened {app_path}"
        except Exception as e:
            return f"Failed to open {app_path}: {e}"

    @staticmethod
    def block_sites(sites):
        # Simplified site blocking (requires admin for hosts file, usually not recommended for simple scripts)
        # For now, we'll just log this action or use a more complex method later.
        return f"Blocking sites: {', '.join(sites)} (Implementation pending security checks)"

    @staticmethod
    def start_timer(minutes):
        # This will be handled by the scheduler, but atomics can trigger it
        return f"Timer requested for {minutes} minutes"

    @staticmethod
    def speak(text):
        # Interaction with voice.py will happen here
        return f"Speaking: {text}"

    @staticmethod
    def run_command(command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return f"Executed: {command}. Output: {result.stdout}"
        except Exception as e:
            return f"Error executing command: {e}"

    @staticmethod
    def open_url(url):
        webbrowser.open(url)
        return f"Opened URL: {url}"

    @staticmethod
    def close_app(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                return f"Closed {process_name}"
        return f"Process {process_name} not found"
