from __future__ import annotations
import time
from typing import Callable
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

def run_button_loop(pin: int, pull_up: bool, delay: float, callback: Callable[[bool], None], stop_event):
    """Reads a digital button. callback(pressed: bool)"""
    ensure_gpio_bcm_mode()
    if not gpio_availability().has_gpio:
        raise RuntimeError("RPi.GPIO not available (not running on Raspberry Pi?)")

    pud = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
    GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

    last = None
    while True:
        pressed = (GPIO.input(pin) == (0 if pull_up else 1))
        if pressed != last:
            callback(pressed)
            last = pressed
        if stop_event.is_set():
            break
        time.sleep(delay)
