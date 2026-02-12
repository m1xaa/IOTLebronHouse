from .PCF8574 import PCF8574_GPIO
from .Adafruit_LCD1602 import Adafruit_CharLCD

class LCD:

    def __init__(self, address=0x27, cols=16, rows=2):
        try:
            mcp = PCF8574_GPIO(address)
        except:
            raise RuntimeError("LCD I2C address error")

        self.lcd = Adafruit_CharLCD(
            pin_rs=0,
            pin_e=2,
            pins_db=[4,5,6,7],
            GPIO=mcp
        )

        self.cols = cols
        self.rows = rows

        mcp.output(3,1)  # backlight ON
        self.lcd.begin(cols, rows)
        self.clear()

    def clear(self):
        self.lcd.clear()

    def display(self, line1: str, line2: str):
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        self.lcd.message(line1[:self.cols] + "\n")
        self.lcd.message(line2[:self.cols])

    def cleanup(self):
        self.clear()
