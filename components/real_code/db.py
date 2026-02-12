from __future__ import annotations
import time
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

class Buzzer:
    def __init__(self, pin: int, active_high: bool = True):
        ensure_gpio_bcm_mode()
        if not gpio_availability().has_gpio:
            raise RuntimeError("RPi.GPIO not available")

        self.pin = pin
        self.active_high = active_high
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin, self.active_high)

    def off(self):
        GPIO.output(self.pin, not self.active_high)

    def cleanup(self):
        self.off()

