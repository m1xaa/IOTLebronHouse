import threading
from typing import Any, Dict, List, Callable

from components.real_code.gsg.gsg import run_gsg_loop
from components.simulated_code.gsg import run_gsg_simulator


def run_gsg(
    settings: Dict[str, Any],
    threads: List[threading.Thread],
    stop_event,
    callback: Callable[[bool], None],
):
    poll_delay = float(settings.get("delay_sec", 0.2))
    threshold = float(settings.get("threshold", 0.5))

    if settings.get("simulated", True):
        t = threading.Thread(
            target=run_gsg_simulator,
            args=(poll_delay, threshold, callback, stop_event),
            daemon=True
        )
        t.start()
        threads.append(t)
        return


    t = threading.Thread(
        target=run_gsg_loop,
        args=(poll_delay, threshold, callback, stop_event),
        daemon=True
    )
    t.start()
    threads.append(t)
