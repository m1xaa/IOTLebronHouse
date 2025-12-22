import RPi.GPIO as GPIO
import time

KEYMAP = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

def run_membrane_loop(rows, cols, delay, callback, stop_event):
    GPIO.setmode(GPIO.BCM)

    for r in rows:
        GPIO.setup(r, GPIO.OUT)
        GPIO.output(r, GPIO.LOW)

    for c in cols:
        GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while not stop_event.is_set():
        for i, r in enumerate(rows):
            GPIO.output(r, GPIO.HIGH)
            for j, c in enumerate(cols):
                if GPIO.input(c) == GPIO.HIGH:
                    key = KEYMAP[i][j]
                    callback(key)
                    time.sleep(0.3)
            GPIO.output(r, GPIO.LOW)

        time.sleep(delay)
