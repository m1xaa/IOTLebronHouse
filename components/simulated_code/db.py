class SimBuzzer:
    def __init__(self):
        self._on = False

    def on(self):
        if not self._on:
            self._on = True
            print("[DB] BUZZER -> ON (simulated)")

    def off(self):
        if self._on:
            self._on = False
            print("[DB] BUZZER -> OFF (simulated)")

    def cleanup(self):
        self.off()
