# core/database.py
import sqlite3
import json
from datetime import datetime

class WazonDB:
    def __init__(self, db_name="wazon_vault.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                module_name TEXT,
                target TEXT,
                status TEXT,
                result_data TEXT
            )
        """)
        self.conn.commit()

    def log_mission(self, module_name, target, status, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_str = json.dumps(data)
        self.cursor.execute(
            "INSERT INTO missions (timestamp, module_name, target, status, result_data) VALUES (?, ?, ?, ?, ?)",
            (timestamp, module_name, target, status, data_str)
        )
        self.conn.commit()

    def get_history(self):
        self.cursor.execute("SELECT timestamp, module_name, target, status FROM missions ORDER BY id DESC")
        return self.cursor.fetchall()