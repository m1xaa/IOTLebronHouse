from __future__ import annotations
import random
import time
from typing import Callable

def run_button_simulator(delay: float, callback: Callable[[bool], None], stop_event):
    pressed = False
    while True:
        if random.random() < 0.2:
            pressed = not pressed
            callback(pressed)
        if stop_event.is_set():
            break
        time.sleep(delay)
