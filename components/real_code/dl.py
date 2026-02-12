from __future__ import annotations
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

class Led:
    def __init__(self, pin: int, active_high: bool = True):
        ensure_gpio_bcm_mode()
        if not gpio_availability().has_gpio:
            raise RuntimeError("RPi.GPIO not available")
        self.pin = pin
        self.active_high = active_high
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin, True if self.active_high else False)

    def off(self):
        GPIO.output(self.pin, False if self.active_high else True)

    def cleanup(self):
        self.off()
