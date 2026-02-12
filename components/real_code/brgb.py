import RPi.GPIO as GPIO

class RGB:

    def __init__(self, red_pin, green_pin, blue_pin, active_high=True):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.active_high = active_high

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

        self.off()

    def _write(self, pin, state):
        if self.active_high:
            GPIO.output(pin, state)
        else:
            GPIO.output(pin, not state)

    def on(self):
        self.set_color(1, 1, 1)

    def off(self):
        self.set_color(0, 0, 0)

    def set_color(self, r, g, b):
        self._write(self.red_pin, bool(r))
        self._write(self.green_pin, bool(g))
        self._write(self.blue_pin, bool(b))

    def cleanup(self):
        self.off()
        GPIO.cleanup()
