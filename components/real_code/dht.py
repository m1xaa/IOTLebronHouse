from .gpio_utils import GPIO, ensure_gpio_bcm_mode, gpio_availability
import time

class DHT:
    DHTLIB_OK = 0
    DHTLIB_ERROR_CHECKSUM = -1
    DHTLIB_ERROR_TIMEOUT = -2
    DHTLIB_INVALID_VALUE = -999

    DHTLIB_DHT11_WAKEUP = 0.020
    DHTLIB_TIMEOUT = 0.0001

    def __init__(self, pin):
        self.pin = pin
        self.bits = [0, 0, 0, 0, 0]
        self.humidity = 0
        self.temperature = 0
        GPIO.setmode(GPIO.BCM)

    def readSensor(self):
        mask = 0x80
        idx = 0
        self.bits = [0, 0, 0, 0, 0]

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(self.DHTLIB_DHT11_WAKEUP)
        GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.IN)

        t = time.time()
        while GPIO.input(self.pin) == GPIO.LOW:
            if (time.time() - t) > self.DHTLIB_TIMEOUT:
                return self.DHTLIB_ERROR_TIMEOUT

        t = time.time()
        while GPIO.input(self.pin) == GPIO.HIGH:
            if (time.time() - t) > self.DHTLIB_TIMEOUT:
                return self.DHTLIB_ERROR_TIMEOUT

        for _ in range(40):
            t = time.time()
            while GPIO.input(self.pin) == GPIO.LOW:
                if (time.time() - t) > self.DHTLIB_TIMEOUT:
                    return self.DHTLIB_ERROR_TIMEOUT

            t = time.time()
            while GPIO.input(self.pin) == GPIO.HIGH:
                if (time.time() - t) > self.DHTLIB_TIMEOUT:
                    return self.DHTLIB_ERROR_TIMEOUT

            if (time.time() - t) > 0.00005:
                self.bits[idx] |= mask

            mask >>= 1
            if mask == 0:
                mask = 0x80
                idx += 1

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        return self.DHTLIB_OK

    def readDHT11(self):
        rv = self.readSensor()
        if rv != self.DHTLIB_OK:
            self.humidity = self.DHTLIB_INVALID_VALUE
            self.temperature = self.DHTLIB_INVALID_VALUE
            return rv

        self.humidity = self.bits[0]
        self.temperature = self.bits[2] + self.bits[3] * 0.1

        checksum = (self.bits[0] + self.bits[1] +
                    self.bits[2] + self.bits[3]) & 0xFF

        if self.bits[4] != checksum:
            return self.DHTLIB_ERROR_CHECKSUM

        return self.DHTLIB_OK


def run_dht_loop(pin, delay, callback, stop_event):
    dht = DHT(pin)

    while not stop_event.is_set():
        chk = dht.readDHT11()

        if chk == DHT.DHTLIB_OK:
            data = {
                "temperature": dht.temperature,
                "humidity": dht.humidity
            }
            callback(data)

        time.sleep(delay)
