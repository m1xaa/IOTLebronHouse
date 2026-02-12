from typing import Any, Dict

from components.real_code.lcd.lcd import LCD
from components.simulated_code.lcd import SimLCD

def create_lcd(settings: Dict[str, Any]):
    if settings.get("simulated", True):
        return SimLCD()

    return LCD(
        address=settings.get("address", 0x27),
        cols=settings.get("cols", 16),
        rows=settings.get("rows", 2)
    )
