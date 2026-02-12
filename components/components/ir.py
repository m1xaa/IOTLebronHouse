import threading
from typing import Any, Dict, List, Callable

from components.real_code.ir import run_ir_loop
from components.simulated_code.ir import run_ir_simulator


def run_ir(
    settings: Dict[str, Any],
    threads: List[threading.Thread],
    stop_event,
    callback: Callable[[str], None],
):
    if settings.get("simulated", True):
        t = threading.Thread(
            target=run_ir_simulator,
            args=(callback, stop_event),
            daemon=True
        )
        t.start()
        threads.append(t)
        return

    pin = int(settings["pin"])

    t = threading.Thread(
        target=run_ir_loop,
        args=(pin, callback, stop_event),
        daemon=True
    )
    t.start()
    threads.append(t)
