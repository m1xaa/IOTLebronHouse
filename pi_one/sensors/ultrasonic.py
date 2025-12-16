from __future__ import annotations
import time
from typing import Callable, Optional
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

SPEED_OF_SOUND_CM_S = 34300.0  # ~343 m/s

def measure_distance_cm(trig_pin: int, echo_pin: int, timeout_s: float = 0.02) -> Optional[float]:
    # Trigger pulse
    GPIO.output(trig_pin, False)
    time.sleep(0.0002)
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    start = time.time()
    while GPIO.input(echo_pin) == 0:
        if time.time() - start > timeout_s:
            return None
    pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        if time.time() - pulse_start > timeout_s:
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * SPEED_OF_SOUND_CM_S) / 2.0
    return distance

def run_ultrasonic_loop(trig_pin: int, echo_pin: int, delay: float, max_cm: float,
                        callback: Callable[[Optional[float]], None], stop_event):
    """Measures distance in cm. callback(distance_cm or None)"""
    ensure_gpio_bcm_mode()
    if not gpio_availability().has_gpio:
        raise RuntimeError("RPi.GPIO not available")

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    while True:
        d = measure_distance_cm(trig_pin, echo_pin)
        if d is not None and d > max_cm:
            d = None
        callback(d)
        if stop_event.is_set():
            break
        time.sleep(delay)
