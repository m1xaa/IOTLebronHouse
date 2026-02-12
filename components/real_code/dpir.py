from __future__ import annotations
import time
from typing import Callable
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

def run_pir_loop(pin: int, delay: float, callback: Callable[[bool], None], stop_event):
    ensure_gpio_bcm_mode()
    if not gpio_availability().has_gpio:
        raise RuntimeError("RPi.GPIO not available")

    GPIO.setup(pin, GPIO.IN)
    last = None
    while True:
        motion = bool(GPIO.input(pin))
        if motion != last:
            callback(motion)
            last = motion
        if stop_event.is_set():
            break
        time.sleep(delay)
