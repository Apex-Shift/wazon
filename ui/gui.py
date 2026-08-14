# ui/gui.py
import sys
import asyncio
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QComboBox
from core.worker import WazonWorker

from modules.common.modbus_scanner import WazonModule as ModbusScanner
from modules.common.bacnet_enum import WazonModule as BACnetEnum
from modules.brand_tridium.rce_niagara import WazonModule as TridiumRCE
from modules.brand_schneider.overflow_tac import WazonModule as SchneiderProbe
from modules.brand_johnson.upload_metasys import WazonModule as JohnsonMetasys
from modules.brand_honeywell.default_creds import WazonModule as HoneywellCreds

class WorkerThread(QThread):
    finished = Signal(dict)

    def __init__(self, module, target):
        super().__init__()
        self.module = module
        self.target = target
        self.worker = WazonWorker()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.worker.run_mission(self.module, self.target))
        loop.close()
        self.finished.emit(result)

class WazonGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wazon Framework - BMS Infiltration Dashboard")
        self.resize(900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("<h2>Wazon - Mission Control (GUI Mode)</h2>"))
        layout.addWidget(QLabel("Select Module:"))
        self.module_combo = QComboBox()
        self.available_modules = {
            "Modbus TCP Scanner": ModbusScanner(),
            "BACnet UDP Discovery": BACnetEnum(),
            "Tridium Niagara Probe": TridiumRCE(),
            "Schneider TAC Probe": SchneiderProbe(),
            "Johnson Controls Metasys": JohnsonMetasys(),
            "Honeywell Default Creds": HoneywellCreds()
        }
        self.module_combo.addItems(self.available_modules.keys())
        layout.addWidget(self.module_combo)

        layout.addWidget(QLabel("Target IP / Host:"))
        self.target_input = QLineEdit("127.0.0.1")
        layout.addWidget(self.target_input)

        self.exec_btn = QPushButton("Deploy Agent / Run Mission")
        self.exec_btn.clicked.connect(self.start_mission)
        layout.addWidget(self.exec_btn)

        layout.addWidget(QLabel("Operation Logs:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #0b0b0b; color: #00FF00; font-family: monospace; font-size: 11pt;")
        layout.addWidget(self.log_output)

    def start_mission(self):
        selected_name = self.module_combo.currentText()
        target = self.target_input.text()
        module_instance = self.available_modules[selected_name]

        self.log_output.append(f"\n[*] Dispatched agent -> [{selected_name}] against target: {target}")
        self.exec_btn.setEnabled(False)

        self.thread = WorkerThread(module_instance, target)
        self.thread.finished.connect(self.handle_results)
        self.thread.start()

    def handle_results(self, result):
        self.log_output.append(f"[+] Mission Completed. Response:\n{result}\n")
        self.exec_btn.setEnabled(True)

def run_gui():
    app = QApplication(sys.argv)
    window = WazonGUI()
    window.show()
    sys.exit(app.exec())