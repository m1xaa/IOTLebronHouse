from __future__ import annotations
import threading
from typing import Any, Dict, List, Callable

from components.real_code.ds import run_button_loop
from components.simulated_code.ds import run_button_simulator


def run_ds(
    settings: Dict[str, Any],
    threads: List[threading.Thread],
    stop_event,
    callback: Callable[[float], None],
):
    delay = float(settings.get("delay_sec", settings.get("poll_delay_sec", 2)))

    if settings.get("simulated", True):
        t = threading.Thread(
            target=run_button_simulator,
            args=(delay, callback, stop_event),
            daemon=True
        )
        t.start()
        threads.append(t)
        return


    pin = int(settings["pin"])
    pull_up = bool(settings.get("pull_up", True))

    t = threading.Thread(
        target=run_button_loop,
        args=(pin, pull_up, delay, callback, stop_event),
        daemon=True
    )
    t.start()
    threads.append(t)
