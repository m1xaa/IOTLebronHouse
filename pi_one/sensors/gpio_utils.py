from __future__ import annotations
from dataclasses import dataclass

try:
    import RPi.GPIO as GPIO  # type: ignore
    _HAS_GPIO = True
except Exception:
    GPIO = None  # type: ignore
    _HAS_GPIO = False

@dataclass(frozen=True)
class GpioAvailability:
    has_gpio: bool

def gpio_availability() -> GpioAvailability:
    return GpioAvailability(has_gpio=_HAS_GPIO)

def ensure_gpio_bcm_mode():
    if not _HAS_GPIO:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
