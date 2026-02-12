import threading
import time

class Sim4SD:

    def __init__(self):
        self._seconds = 0
        self._running = False
        self._blinking = False
        self._stop_event = threading.Event()

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def set_time(self, seconds: int):
        self._seconds = max(0, seconds)
        print(f"[4SD] Set time: {self._seconds}s")

    def add_seconds(self, n: int):
        self._seconds += n
        print(f"[4SD] Added {n}s")

    def start(self):
        self._running = True
        self._blinking = False
        print("[4SD] Started")

    def stop(self):
        self._running = False

    def blink(self):
        self._blinking = True
        self._running = False

    def stop_blink(self):
        self._blinking = False

    def _loop(self):
        while not self._stop_event.is_set():
            if self._running and self._seconds > 0:
                time.sleep(1)
                self._seconds -= 1
                print(f"[4SD] {self._seconds}s remaining")
                if self._seconds == 0:
                    self.blink()
            elif self._blinking:
                print("[4SD] BLINK 00:00")
                time.sleep(0.5)
            else:
                time.sleep(0.1)

    def cleanup(self):
        self._stop_event.set()
