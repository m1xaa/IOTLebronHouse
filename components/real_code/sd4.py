import threading
import time
from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability

NUM_MAP = {
    '0': (1,1,1,1,1,1,0),
    '1': (0,1,1,0,0,0,0),
    '2': (1,1,0,1,1,0,1),
    '3': (1,1,1,1,0,0,1),
    '4': (0,1,1,0,0,1,1),
    '5': (1,0,1,1,0,1,1),
    '6': (1,0,1,1,1,1,1),
    '7': (1,1,1,0,0,0,0),
    '8': (1,1,1,1,1,1,1),
    '9': (1,1,1,1,0,1,1),
    ' ': (0,0,0,0,0,0,0)
}

class FourDigitDisplay:

    def __init__(self, segments, digits):
        GPIO.setmode(GPIO.BCM)

        self.segments = segments
        self.digits = digits

        for s in segments:
            GPIO.setup(s, GPIO.OUT)
            GPIO.output(s, 0)

        for d in digits:
            GPIO.setup(d, GPIO.OUT)
            GPIO.output(d, 1)

        self._seconds = 0
        self._running = False
        self._blinking = False
        self._stop_event = threading.Event()

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def set_time(self, seconds: int):
        self._seconds = max(0, seconds)

    def add_seconds(self, n: int):
        self._seconds += n

    def start(self):
        self._running = True
        self._blinking = False

    def stop(self):
        self._running = False

    def blink(self):
        self._blinking = True
        self._running = False

    def stop_blink(self):
        self._blinking = False

    def _format(self):
        m = self._seconds // 60
        s = self._seconds % 60
        return f"{m:02}{s:02}"

    def _display_number(self, s):
        for i in range(4):
            for seg in range(7):
                GPIO.output(self.segments[seg], NUM_MAP[s[i]][seg])
            GPIO.output(self.digits[i], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[i], 1)

    def _loop(self):
        last_tick = time.time()
        blink_state = False
        blink_timer = time.time()

        while not self._stop_event.is_set():
            now = time.time()

            if self._running and self._seconds > 0:
                if now - last_tick >= 1:
                    self._seconds -= 1
                    last_tick = now
                    if self._seconds == 0:
                        self.blink()

            if self._blinking:
                if now - blink_timer >= 0.5:
                    blink_state = not blink_state
                    blink_timer = now
                display_value = "0000" if blink_state else "    "
            else:
                display_value = self._format()

            self._display_number(display_value)

    def cleanup(self):
        self._stop_event.set()
        GPIO.cleanup()
