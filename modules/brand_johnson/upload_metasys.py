# modules/brand_johnson/upload_metasys.py
import asyncio
import aiohttp
from core.engine import BaseWazonModule

class WazonModule(BaseWazonModule):
    def __init__(self):
        super().__init__()
        self.name = "Johnson Controls Metasys Endpoint Enumerator"
        self.category = "recon/exploit"
        self.description = "Checks Johnson Controls Metasys UI endpoints for unauthenticated file access."
        self.options = {
            "TARGET": {"value": "127.0.0.1", "required": True, "description": "Target IP or Domain"},
            "PORT": {"value": 80, "required": True, "description": "Web port"}
        }

    async def execute(self, target=None):
        ip = self.options["TARGET"]["value"] if not target else target
        port = self.options["PORT"]["value"]
        url = f"http://{ip}:{port}/metasys/login.xhtml"

        print(f"[*] Wazon [Johnson Engine] -> Checking Metasys interface at {url}...")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._check_metasys_sync, url)
        return result

    def _check_metasys_sync(self, url):
        import requests
        try:
            response = requests.get(url, timeout=5, verify=False)
            is_metasys = "metasys" in response.text.lower() or "jci" in response.text.lower()
            return {
                "status": "success",
                "url": url,
                "status_code": response.status_code,
                "metasys_detected": is_metasys,
                "message": "Metasys panel identified." if is_metasys else "Standard HTTP response."
            }
        except Exception as e:
            return {"status": "fail", "message": f"Target unreachable: {str(e)}"}