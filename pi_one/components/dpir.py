from __future__ import annotations
import threading
from typing import Any, Dict, List

from simulators.pir import run_pir_simulator

def run_dpir(settings: Dict[str, Any], threads: List[threading.Thread], stop_event, callback):
    delay = float(settings.get("delay_sec", settings.get("poll_delay_sec", 2)))
    if settings.get("simulated", True):
        t = threading.Thread(target=run_pir_simulator, args=(delay, callback, stop_event), daemon=True)
        t.start()
        threads.append(t)
        return

    from sensors.pir import run_pir_loop
    pin = int(settings["pin"])
    t = threading.Thread(target=run_pir_loop, args=(pin, delay, callback, stop_event), daemon=True)
    t.start()
    threads.append(t)
