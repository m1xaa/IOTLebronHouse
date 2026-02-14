from __future__ import annotations
import time
from typing import Callable
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

def run_button_loop(pin: int, pull_up: bool, delay: float, callback, stop_event):
    ensure_gpio_bcm_mode()
    if not gpio_availability().has_gpio:
        raise RuntimeError("RPi.GPIO not available")

    pud = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
    GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

    last = False
    pressed_since = None
    long_sent = False
    LONG_THRESHOLD = 5

    while not stop_event.is_set():
        pressed = (GPIO.input(pin) == (0 if pull_up else 1))
        now = time.time()

        if pressed and not last:
            pressed_since = now
            long_sent = False
            callback("PRESS")

        elif pressed and last and not long_sent:
            if pressed_since and (now - pressed_since) >= LONG_THRESHOLD:
                callback("LONG_PRESS")
                long_sent = True

        elif not pressed and last:
            callback("RELEASE")
            pressed_since = None
            long_sent = False

        last = pressed
        time.sleep(delay)

