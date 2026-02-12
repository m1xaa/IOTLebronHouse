import random
import time

def run_dht_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        data = {
            "temperature": round(random.uniform(18, 28), 1),
            "humidity": round(random.uniform(30, 70), 1)
        }
        callback(data)
        time.sleep(delay)
