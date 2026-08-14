# core/worker.py
import asyncio
from core.database import WazonDB

class WazonWorker:
    def __init__(self):
        self.is_running = False
        self.db = WazonDB()

    async def run_mission(self, module_instance, target):
        self.is_running = True
        try:
            print(f"[*] Wazon executing -> [{module_instance.name}] on target: {target}")
            result = await module_instance.execute(target)
            
            # Enregistrement automatique dans la base de données SQLite
            self.db.log_mission(module_instance.name, target, result.get("status", "unknown"), result)
            
            return {"status": "success", "data": result}
        except Exception as e:
            err_res = {"status": "error", "message": str(e)}
            self.db.log_mission(module_instance.name, target, "error", err_res)
            return err_res
        finally:
            self.is_running = False