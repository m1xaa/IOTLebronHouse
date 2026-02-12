from typing import Any, Dict

from components.real_code.sd4 import FourDigitDisplay
from components.simulated_code.sd4 import Sim4SD

def create_4sd(settings: Dict[str, Any]):
    if settings.get("simulated", True):
        return Sim4SD()

    return FourDigitDisplay(
        segments=settings["segments"],
        digits=settings["digits"]
    )
