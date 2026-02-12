from __future__ import annotations
from typing import Any, Dict

from components.real_code.dl import Led
from components.simulated_code.dl import SimLed


def create_dl(settings: Dict[str, Any]):
    if settings.get("simulated", True):
        return SimLed()
    return Led(pin=int(settings["pin"]), active_high=bool(settings.get("active_high", True)))
