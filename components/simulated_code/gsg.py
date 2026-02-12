import random
import time

def run_gsg_simulator(delay, threshold, callback, stop_event):
    while not stop_event.is_set():
        if random.random() < 0.05:
            callback(True)
        time.sleep(delay)
