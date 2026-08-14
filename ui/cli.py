# ui/cli.py
import asyncio
from art import tprint
from rich.console import Console
from rich.table import Table
from core.worker import WazonWorker

from modules.common.modbus_scanner import WazonModule as ModbusScanner
from modules.common.bacnet_enum import WazonModule as BACnetEnum
from modules.brand_tridium.rce_niagara import WazonModule as TridiumRCE
from modules.brand_schneider.overflow_tac import WazonModule as SchneiderProbe
from modules.brand_johnson.upload_metasys import WazonModule as JohnsonMetasys
from modules.brand_honeywell.default_creds import WazonModule as HoneywellCreds

console = Console()

class WazonCLI:
    def __init__(self):
        self.worker = WazonWorker()
        self.modules = {
            "1": ("Modbus TCP Register Scanner", ModbusScanner()),
            "2": ("BACnet UDP Discovery", BACnetEnum()),
            "3": ("Tridium Niagara Web Fingerprint", TridiumRCE()),
            "4": ("Schneider TAC Port Probe", SchneiderProbe()),
            "5": ("Johnson Controls Metasys Enum", JohnsonMetasys()),
            "6": ("Honeywell Default Creds Checker", HoneywellCreds())
        }

    def banner(self):
        console.print("[bold red]WAZON[/bold red]")
        console.print("[italic cyan]Building Management System Infiltration Framework (Mission Impossible Mode)[/italic cyan]\n")
    def list_modules(self):
        table = Table(title="Available Wazon Modules")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Module Name", style="magenta")
        table.add_column("Category", style="green")

        for key, (name, mod) in self.modules.items():
            table.add_row(key, name, mod.category)
        console.print(table)

    async def start(self):
        self.banner()
        self.list_modules()
        choice = console.input("\n[bold yellow]wazon > Select module ID: [/bold yellow]")
        if choice in self.modules:
            name, module = self.modules[choice]
            target = console.input(f"[bold yellow]wazon ({name}) > Enter Target IP: [/bold yellow]")
            console.print(f"\n[+] Deploying agent to {target}...")
            result = await self.worker.run_mission(module, target)
            console.print(f"\n[bold green][+] Mission Result:[/bold green]\n{result}")
        else:
            console.print("[bold red][!] Invalid selection.[/bold red]")

def run_cli():
    cli = WazonCLI()
    asyncio.run(cli.start())