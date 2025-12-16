import random
import time

KEYS = ['1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D']

def run_membrane_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        key = random.choice(KEYS)
        callback(key)
        time.sleep(delay + random.uniform(0.5, 1.5))
