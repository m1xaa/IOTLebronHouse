from __future__ import annotations
import random
import time
from typing import Callable

def run_pir_simulator(delay: float, callback: Callable[[bool], None], stop_event):
    motion = False
    while True:
        # bursty motion: sometimes true for a few cycles
        if random.random() < 0.15:
            motion = True
        elif random.random() < 0.35:
            motion = False
        callback(motion)
        if stop_event.is_set():
            break
        time.sleep(delay)
