class SimRGB:

    def __init__(self):
        self.state = (0, 0, 0)

    def on(self):
        self.state = (1, 1, 1)
        print("[BRGB] ON (white)")

    def off(self):
        self.state = (0, 0, 0)
        print("[BRGB] OFF")

    def set_color(self, r, g, b):
        self.state = (r, g, b)
        print(f"[BRGB] Color set to R:{r} G:{g} B:{b}")

    def cleanup(self):
        self.off()
