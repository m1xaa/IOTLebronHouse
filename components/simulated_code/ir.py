import random
import time

COMMANDS = [
    "LEFT", "RIGHT", "UP", "DOWN",
    "1", "2", "3", "OK",
    "RED", "GREEN", "BLUE"
]

def run_ir_simulator(callback, stop_event):
    while not stop_event.is_set():
        if random.random() < 0.1:
            callback(random.choice(COMMANDS))
        time.sleep(0.5)
