from __future__ import annotations
import random
import time
from typing import Callable, Optional

def run_ultrasonic_simulator(delay: float, max_cm: float, callback: Callable[[Optional[float]], None], stop_event):
    d = random.uniform(30, 120)
    while True:
        # smooth drift + occasional approach
        d += random.uniform(-5, 5)
        if random.random() < 0.1:
            d -= random.uniform(10, 40)
        d = max(2.0, min(max_cm, d))
        callback(round(d, 1))
        if stop_event.is_set():
            break
        time.sleep(delay)
