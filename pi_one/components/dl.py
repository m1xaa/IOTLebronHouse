from __future__ import annotations
from typing import Any, Dict

class SimLed:
    def __init__(self):
        self._on = False
    def on(self):
        self._on = True
        print("[DL] LED -> ON (simulated)")
    def off(self):
        self._on = False
        print("[DL] LED -> OFF (simulated)")
    def cleanup(self):
        self.off()

def create_dl(settings: Dict[str, Any]):
    if settings.get("simulated", True):
        return SimLed()
    from sensors.led import Led
    return Led(pin=int(settings["pin"]), active_high=bool(settings.get("active_high", True)))
