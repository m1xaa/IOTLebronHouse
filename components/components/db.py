from __future__ import annotations
from typing import Any, Dict
import time

from components.real_code.db import Buzzer
from components.simulated_code.db import SimBuzzer

def create_db(settings: Dict[str, Any]):
    if settings.get("simulated", False):
        return SimBuzzer()

    return Buzzer(
        pin=int(settings["pin"]),
        active_high=bool(settings.get("active_high", True))
    )

