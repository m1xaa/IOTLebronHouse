import random
import time
from typing import Callable

def run_button_simulator(delay: float, callback: Callable[[float], None], stop_event):
    pressed = False
    pressed_since = None
    long_sent = False
    LONG_THRESHOLD = 5

    while not stop_event.is_set():
        now = time.time()

        # random promena stanja
        if random.random() < 0.1:
            if not pressed:
                # tek pritisnuto
                pressed = True
                pressed_since = now
                long_sent = False
                callback(0.001)
            else:
                # pušteno
                pressed = False
                pressed_since = None
                long_sent = False

        # ako se drži, proveri long press
        if pressed and pressed_since and not long_sent:
            duration = now - pressed_since
            if duration >= LONG_THRESHOLD:
                callback(duration)
                long_sent = True

        time.sleep(delay)
