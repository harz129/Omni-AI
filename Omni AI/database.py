import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="database/omni.db"):
        self.db_path = db_path
        # Ensure the directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # History of executed workflows
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_name TEXT,
                timestamp DATETIME,
                status TEXT
            )
        ''')
        # User completion metrics for learning
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_name TEXT,
                interaction_type TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def log_workflow(self, name, status="executed"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (workflow_name, timestamp, status) VALUES (?, ?, ?)',
                       (name, datetime.now(), status))
        conn.commit()
        conn.close()

    def add_metric(self, name, interaction):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO metrics (workflow_name, interaction_type, timestamp) VALUES (?, ?, ?)',
                       (name, interaction, datetime.now()))
        conn.commit()
        conn.close()
