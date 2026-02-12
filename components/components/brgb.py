from ctypes.wintypes import RGB
from typing import Any, Dict

from components.simulated_code.brgb import SimRGB

def create_brgb(settings: Dict[str, Any]):
    if settings.get("simulated", True):
        return SimRGB()

    return RGB(
        red_pin=settings["red_pin"],
        green_pin=settings["green_pin"],
        blue_pin=settings["blue_pin"],
        active_high=settings.get("active_high", True)
    )
