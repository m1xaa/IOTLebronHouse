from __future__ import annotations
import threading
from typing import Any, Dict, List, Optional

from simulators.ultrasonic import run_ultrasonic_simulator

def run_dus(settings: Dict[str, Any], threads: List[threading.Thread], stop_event, callback):
    delay = float(settings.get("delay_sec", settings.get("poll_delay_sec", 2)))
    max_cm = float(settings.get("max_cm", 400))
    if settings.get("simulated", True):
        t = threading.Thread(target=run_ultrasonic_simulator, args=(delay, max_cm, callback, stop_event), daemon=True)
        t.start()
        threads.append(t)
        return

    from sensors.ultrasonic import run_ultrasonic_loop
    trig = int(settings["trig_pin"])
    echo = int(settings["echo_pin"])
    t = threading.Thread(target=run_ultrasonic_loop, args=(trig, echo, delay, max_cm, callback, stop_event), daemon=True)
    t.start()
    threads.append(t)
