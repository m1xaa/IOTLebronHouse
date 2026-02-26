import threading
import time

from components.components.sd4 import create_4sd
from components.components.btn import run_btn
from components.components.dht import run_dht
from components.components.gsg import run_gsg
from components.components.ds import run_ds
from components.components.dpir import run_dpir
from components.components.dus import run_dus

from settings import load_settings
from mqtt_handler import MqttHandler


publisher = None
settings = None

seconds_increment = 10
increment_lock = threading.Lock()

display_device = None


def ts():
    t = time.localtime()
    return time.strftime('%H:%M:%S', t)


def print_event(label: str, payload: str):
    print("=" * 28)
    print(f"[{ts()}] {label}")
    print(payload)


def btn_cb():
    global seconds_increment

    is_sim = settings["BTN"]["simulated"]
    name = settings["BTN"]["name"]

    publisher.publish(name, True, is_sim)
    print_event("[BTN] (Button)", f"pressed={True}")

    if not display_device:
        return

    if display_device._blinking:
        display_device.stop_blink()
        display_device.set_time(0)
        print_event("[4SD]", "blink stopped")
        return

    if display_device._running:
        with increment_lock:
            inc = seconds_increment

        display_device.add_seconds(inc)
        print_event("[4SD]", f"added={inc}")
    else:
        print_event("[4SD]", "ignored (not running)")




def dht3_cb(payload):
    is_sim = settings["DHT3"]["simulated"]
    name = settings["DHT3"]["name"]

    publisher.publish(name, payload, is_sim)
    print_event("[DHT3] (Temp/Humidity)", str(payload))


def gsg_cb(detected: bool):
    is_sim = settings["GSG"]["simulated"]
    name = settings["GSG"]["name"]

    publisher.publish(name, detected, is_sim)
    print_event("[GSG] (Gyro movement)", str(detected))


def ds2_cb(event):
    is_sim = settings["DS2"]["simulated"]
    name = settings["DS2"]["name"]
    publisher.publish(name, event, is_sim)
    print_event("[DS2] (Door Sensor)", f"event={event}")


def dpir2_cb(motion: bool):
    is_sim = settings["DPIR2"]["simulated"]
    name = settings["DPIR2"]["name"]
    publisher.publish(name, motion, is_sim)
    print_event("[DPIR2] (PIR)", f"motion={motion}")


def dus2_cb(distance_cm):
    is_sim = settings["DUS2"]["simulated"]
    name = settings["DUS2"]["name"]

    if distance_cm is not None:
        publisher.publish(name, distance_cm, is_sim)

    print_event("[DUS2] (Ultrasonic)", f"distance_cm={distance_cm}")



def mqtt_message_handler(topic, payload):
    global seconds_increment, publisher, settings

    if 'type' not in payload:
        return


    if payload['type'] == "SD4":
        seconds = payload.get("seconds")
        if seconds is not None and display_device:
            display_device.set_time(int(seconds))
            display_device.start()
            publisher.publish(settings['4SD']['name'], seconds, settings['4SD']['simulated'])
            print_event("[SD4]", f"set_time={seconds}")

    elif payload['type'] == "BTN":
        sec = payload.get("seconds")
        if sec is not None:
            with increment_lock:
                seconds_increment = int(sec)
            print_event("[BTN CONFIG]", f"increment={seconds_increment}")


def main():
    global publisher, settings, display_device

    print("Starting PI2 app")

    settings = load_settings("pi_two")
    publisher = MqttHandler(settings, mqtt_message_handler)

    poll_delay = float(settings.get("delay_sec", 2))

    threads = []
    stop_event = threading.Event()

    display_device = create_4sd(settings["4SD"])


    run_btn({**settings["BTN"], "delay_sec": 0.1}, threads, stop_event, btn_cb)
    run_dht({**settings["DHT3"], "delay_sec": 3}, threads, stop_event, dht3_cb)
    run_gsg({**settings["GSG"], "delay_sec": 0.2}, threads, stop_event, gsg_cb)
    run_ds({**settings["DS2"], "delay_sec": poll_delay}, threads, stop_event, ds2_cb)
    run_dpir({**settings["DPIR2"], "delay_sec": poll_delay}, threads, stop_event, dpir2_cb)
    run_dus({**settings["DUS2"], "delay_sec": poll_delay}, threads, stop_event, dus2_cb)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        
    try:
        display_device.cleanup()
    except Exception:
        pass

    stop_event.set()

    for t in threads:
        t.join()

    publisher.stop()
    time.sleep(0.2)


if __name__ == "__main__":
    main()
