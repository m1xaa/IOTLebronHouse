import random
import time

KEYS = ['1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D']

def run_membrane_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        pin = "".join(str(random.randint(0, 9)) for _ in range(4))
        callback(pin)
        time.sleep(delay + random.uniform(1, 2))
