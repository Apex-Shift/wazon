# modules/brand_schneider/overflow_tac.py
import asyncio
import socket
from core.engine import BaseWazonModule

class WazonModule(BaseWazonModule):
    def __init__(self):
        super().__init__()
        self.name = "Schneider TAC/EcoStruxure Port & Service Probe"
        self.category = "recon"
        self.description = "Probes proprietary ports on Schneider building automation controllers."
        self.options = {
            "TARGET": {"value": "127.0.0.1", "required": True, "description": "Target IP address"},
            "PORT": {"value": 44818, "required": True, "description": "Default industrial/BMS port (e.g., 44818 for CIP/Modbus or custom TAC ports)"}
        }

    async def execute(self, target=None):
        ip = self.options["TARGET"]["value"] if not target else target
        port = int(self.options["PORT"]["value"])
        
        print(f"[*] Wazon [Schneider Engine] -> Probing TAC controller at {ip}:{port}...")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._probe_tcp_sync, ip, port)
        return result

    def _probe_tcp_sync(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            # Envoi d'une bannière de test générique pour réveiller le service
            s.sendall(b"\x00\x00\x00\x04\x00\x00\x00\x01")
            banner = s.recv(1024)
            s.close()
            return {
                "status": "success",
                "target": ip,
                "port": port,
                "response_hex": banner.hex(),
                "message": "Port is open and responding to raw payloads."
            }
        except Exception as e:
            return {"status": "fail", "message": f"Port closed or filtered: {str(e)}"}