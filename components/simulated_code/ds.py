import random
import time
from typing import Callable

def run_button_simulator(
    delay: float,
    callback: Callable[[str], None],
    stop_event
):
    pressed = False
    pressed_since = None
    long_sent = False
    LONG_THRESHOLD = 5

    while not stop_event.is_set():
        now = time.time()

        if random.random() < 0.1:
            if not pressed:
                pressed = True
                pressed_since = now
                long_sent = False
                callback("PRESS")
            else:
                pressed = False
                pressed_since = None
                long_sent = False
                callback("RELEASE")

        if pressed and pressed_since and not long_sent:
            if (now - pressed_since) >= LONG_THRESHOLD:
                callback("LONG_PRESS")
                long_sent = True

        time.sleep(delay)
