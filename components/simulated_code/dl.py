class SimLed:
    def __init__(self):
        self._on = False
    def on(self):
        self._on = True
        print("[DL] LED -> ON (simulated)")
    def off(self):
        self._on = False
        print("[DL] LED -> OFF (simulated)")
    def cleanup(self):
        self.off()