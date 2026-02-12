from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability
from datetime import datetime
import time

BUTTONS = [
    0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857,
    0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd,
    0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef,
    0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5,
    0x300ff52ad
]

BUTTON_NAMES = [
    "LEFT", "RIGHT", "UP", "DOWN",
    "2", "3", "1", "OK",
    "4", "5", "6", "7",
    "8", "9", "*", "0", "#"
]

def get_binary(pin):
    num1s = 0
    binary = 1
    command = []
    previous = 0
    value = GPIO.input(pin)

    while value:
        time.sleep(0.0001)
        value = GPIO.input(pin)

    start_time = datetime.now()

    while True:
        if previous != value:
            now = datetime.now()
            pulse_time = now - start_time
            start_time = now
            command.append((previous, pulse_time.microseconds))

        if value:
            num1s += 1
        else:
            num1s = 0

        if num1s > 10000:
            break

        previous = value
        value = GPIO.input(pin)

    for (typ, tme) in command:
        if typ == 1:
            if tme > 1000:
                binary = binary * 10 + 1
            else:
                binary *= 10

    if len(str(binary)) > 34:
        binary = int(str(binary)[:34])

    return binary


def convert_hex(binary_value):
    tmp = int(str(binary_value), 2)
    return hex(tmp)


def run_ir_loop(pin, callback, stop_event):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)

    while not stop_event.is_set():
        try:
            in_data = convert_hex(get_binary(pin))

            for i in range(len(BUTTONS)):
                if hex(BUTTONS[i]) == in_data:
                    callback(BUTTON_NAMES[i])
        except Exception:
            pass

        time.sleep(0.1)
