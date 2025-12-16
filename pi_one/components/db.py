from __future__ import annotations
from typing import Any, Dict
import time

class SimBuzzer:
    def __init__(self):
        self._on = False
    def on(self):
        self._on = True
        print("[DB] BUZZER -> ON (simulated)")
    def off(self):
        self._on = False
        print("[DB] BUZZER -> OFF (simulated)")
    def beep(self, seconds: float = 0.2):
        print(f"[DB] BUZZER -> BEEP {seconds:.2f}s (simulated)")
        time.sleep(seconds)
    def cleanup(self):
        self.off()

def create_db(settings: Dict[str, Any]):
    if settings.get("simulated", False):
        return SimBuzzer()
    from sensors.buzzer import Buzzer
    return Buzzer(pin=int(settings["pin"]), active_high=bool(settings.get("active_high", True)))
