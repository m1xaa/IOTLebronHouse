import threading
from typing import Any, Dict, List, Callable

from components.real_code.btn import run_btn_loop
from components.simulated_code.btn import run_btn_simulator

def run_btn(
    settings: Dict[str, Any],
    threads: List[threading.Thread],
    stop_event,
    callback: Callable[[], None],
):
    delay = float(settings.get("delay_sec", 0.1))

    if settings.get("simulated", True):
        t = threading.Thread(
            target=run_btn_simulator,
            args=(delay, callback, stop_event),
            daemon=True
        )
        t.start()
        threads.append(t)
        return

    pin = int(settings["pin"])
    pull_up = bool(settings.get("pull_up", True))

    t = threading.Thread(
        target=run_btn_loop,
        args=(pin, pull_up, delay, callback, stop_event),
        daemon=True
    )
    t.start()
    threads.append(t)
