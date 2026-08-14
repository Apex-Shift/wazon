# modules/common/modbus_scanner.py
import asyncio
from core.engine import BaseWazonModule

try:
    from pymodbus.client import ModbusTcpClient
    PYMODBUS_AVAILABLE = True
except ImportError:
    PYMODBUS_AVAILABLE = False

class WazonModule(BaseWazonModule):
    def __init__(self):
        super().__init__()
        self.name = "Modbus TCP Holding Registers Enumerator"
        self.category = "recon"
        self.description = "Connects to Modbus TCP (port 502) and reads actual holding registers from controllers."
        self.options = {
            "TARGET": {"value": "127.0.0.1", "required": True, "description": "Target IP address"},
            "PORT": {"value": 502, "required": True, "description": "Modbus port"},
            "REG_START": {"value": 0, "required": True, "description": "Start register address"},
            "REG_COUNT": {"value": 20, "required": True, "description": "Number of registers to read"}
        }

    async def execute(self, target=None):
        if not PYMODBUS_AVAILABLE:
            return {"status": "error", "message": "Missing dependency: pip install pymodbus"}

        ip = self.options["TARGET"]["value"] if not target else target
        port = int(self.options["PORT"]["value"])
        start = int(self.options["REG_START"]["value"])
        count = int(self.options["REG_COUNT"]["value"])

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._real_modbus_exploit, ip, port, start, count)

    def _real_modbus_exploit(self, ip, port, start, count):
        client = ModbusTcpClient(ip, port=port, timeout=3)
        try:
            if not client.connect():
                return {"status": "fail", "message": f"Connection refused to Modbus service at {ip}:{port}"}

            # Lecture réelle des registres (Fonction 03)
            response = client.read_holding_registers(address=start, count=count, slave=1)
            
            if response.isError():
                return {"status": "error", "message": f"Modbus device returned exception: {response}"}

            parsed_data = {start + i: val for i, val in enumerate(response.registers)}
            return {
                "status": "success",
                "target": ip,
                "registers_read": count,
                "data": parsed_data,
                "message": "Successfully dumped holding registers from industrial controller."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            client.close()