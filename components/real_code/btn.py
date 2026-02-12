import time
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

def run_btn_loop(pin, pull_up, delay, callback, stop_event):
    ensure_gpio_bcm_mode()

    if not gpio_availability().has_gpio:
        raise RuntimeError("RPi.GPIO not available")

    pud = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
    GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

    last = False

    while not stop_event.is_set():
        pressed = (GPIO.input(pin) == (0 if pull_up else 1))

        # rising edge detekcija
        if pressed and not last:
            callback()

        last = pressed
        time.sleep(delay)
