# modules/brand_tridium/rce_niagara.py
import asyncio
import aiohttp
from core.engine import BaseWazonModule

class WazonModule(BaseWazonModule):
    def __init__(self):
        super().__init__()
        self.name = "Tridium Niagara Web Fingerprint & Default Check"
        self.category = "recon/exploit"
        self.description = "Checks for exposed Niagara web interfaces and common default paths."
        self.options = {
            "TARGET": {"value": "127.0.0.1", "required": True, "description": "Target IP or URL"},
            "PORT": {"value": 8080, "required": True, "description": "Web port (e.g., 80, 443, 8080)}"}
        }

    async def execute(self, target=None):
        ip = self.options["TARGET"]["value"] if not target else target
        port = self.options["PORT"]["value"]
        url = f"http://{ip}:{port}/"

        print(f"[*] Wazon [Tridium Engine] -> Probing web interface at {url}...")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._check_web_sync, url)
        return result

    def _check_web_sync(self, url):
        import requests
        try:
            response = requests.get(url, timeout=5, verify=False)
            headers = dict(response.headers)
            server_header = headers.get("Server", "Unknown")
            
            # Détection typique de Niagara / Fox protocol ou page de login
            is_niagara = "niagara" in response.text.lower() or "tridium" in response.text.lower() or "fox" in server_header.lower()
            
            return {
                "status": "success",
                "url": url,
                "status_code": response.status_code,
                "server": server_header,
                "suspected_niagara": is_niagara,
                "message": "Target responsive. Potential Niagara interface detected." if is_niagara else "Target alive, but signature unclear."
            }
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Connection failed to {url}: {str(e)}"}