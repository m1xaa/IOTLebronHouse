import threading

from components.real_code.dms import run_membrane_loop
from components.simulated_code.dms import run_membrane_simulator

def run_dms(settings, threads, stop_event, callback):
    delay = settings.get("delay", 1)

    if settings.get("simulated", True):
        t = threading.Thread(
            target=run_membrane_simulator,
            args=(delay, callback, stop_event)
        )
        t.start()
        threads.append(t)
    else:
        rows = settings["rows"]
        cols = settings["cols"]

        t = threading.Thread(
            target=run_membrane_loop,
            args=(rows, cols, delay, callback, stop_event)
        )
        t.start()
        threads.append(t)
