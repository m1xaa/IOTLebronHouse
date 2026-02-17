import random
import time

def run_btn_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        if random.random() < 0.003:
            callback()
        time.sleep(delay)
