import threading
from typing import Any, Dict, List, Callable

from components.real_code.dht import run_dht_loop
from components.simulated_code.dht import run_dht_simulator



def run_dht(
    settings: Dict[str, Any],
    threads: List[threading.Thread],
    stop_event,
    callback: Callable[[dict], None],
):
    poll_delay = float(settings.get("poll_delay_sec", 2))

    if settings.get("simulated", True):
        t = threading.Thread(
            target=run_dht_simulator,
            args=(poll_delay, callback, stop_event),
            daemon=True
        )
        t.start()
        threads.append(t)
        return


    pin = int(settings["pin"])

    t = threading.Thread(
        target=run_dht_loop,
        args=(pin, poll_delay, callback, stop_event),
        daemon=True
    )
    t.start()
    threads.append(t)
