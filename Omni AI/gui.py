import sys
import asyncio
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QLineEdit, QHBoxLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette

from workflows import WorkflowLoader
from engine import OmniEngine
from intents import IntentDetector
from voice import VoiceModule

class OmniWorker(QThread):
    log_signal = pyqtSignal(str)
    
    def __init__(self, workflows):
        super().__init__()
        self.engine = OmniEngine(workflows)
        self.detector = IntentDetector(workflows)
        self.voice = VoiceModule()
        self.current_command = None
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def process_command(self, command):
        if not command: return
        self.log_signal.emit(f"User: {command}")
        
        workflow_name = self.detector.detect_intent(command)
        if workflow_name:
            self.log_signal.emit(f"OmniAI: Found workflow '{workflow_name}'")
            asyncio.run_coroutine_threadsafe(self.engine.execute_workflow(workflow_name), self.loop)
        else:
            self.log_signal.emit("OmniAI: Unknown command")
            self.voice.speak("I couldn't find a matching workflow.")

class OmniDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader = WorkflowLoader("config.yaml")
        self.workflows = self.loader.load_workflows()
        
        self.worker = OmniWorker(self.workflows)
        self.worker.log_signal.connect(self.update_log)
        self.worker.start()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OmniAI Dashboard")
        self.setFixedSize(600, 500)
        
        # Style
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; font-size: 14px; }
            QTextEdit { background-color: #313244; color: #cdd6f4; border: none; border-radius: 8px; padding: 10px; font-size: 13px; }
            QLineEdit { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; border-radius: 5px; padding: 8px; }
            QPushButton { background-color: #89b4fa; color: #1e1e2e; border-radius: 5px; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #b4befe; }
        """)

        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)

        self.title_label = QLabel("OmniAI Personal Assistant")
        self.title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.layout.addWidget(self.log_view)

        input_layout = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Type a command...")
        self.cmd_input.returnPressed.connect(self.send_text_command)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_text_command)
        
        self.voice_btn = QPushButton("Voice")
        self.voice_btn.setStyleSheet("background-color: #f38ba8;")
        self.voice_btn.clicked.connect(self.listen_voice)

        input_layout.addWidget(self.cmd_input)
        input_layout.addWidget(self.send_btn)
        input_layout.addWidget(self.voice_btn)
        self.layout.addLayout(input_layout)

        self.setCentralWidget(central_widget)
        self.update_log("OmniAI system online.")

    def update_log(self, message):
        self.log_view.append(message)

    def send_text_command(self):
        cmd = self.cmd_input.text()
        self.cmd_input.clear()
        self.worker.process_command(cmd)

    def listen_voice(self):
        # We need to run voice listening in a separate thread to not block UI
        pass # To be fully implemented with a separate thread for blocking listening

def main():
    app = QApplication(sys.argv)
    window = OmniDashboard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
