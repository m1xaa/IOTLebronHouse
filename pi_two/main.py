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


def ts():
    t = time.localtime()
    return time.strftime('%H:%M:%S', t)


def print_event(label: str, payload: str):
    print("=" * 28)
    print(f"[{ts()}] {label}")
    print(payload)


def btn_cb():
    is_sim = settings["BTN"]["simulated"]
    name = settings["BTN"]["name"]
    publisher.publish(name, True, is_sim)
    print_event("[BTN] (Button)", f"pressed={True}")


def dht3_cb(payload):
    is_sim = settings["DHT3"]["simulated"]
    name = settings["DHT3"]["name"]

    publisher.publish(name, payload, is_sim)
    print_event("[DHT3] (Temp/Humidity)", str(payload))


def gsg_cb(detected: bool):
    is_sim = settings["GSG"]["simulated"]
    name = settings["GSG"]["name"]

    publisher.publish(name, detected, is_sim)
    print_event("[GSG] (Gas Sensor)", str(detected))


def ds2_cb(duration: float):
    is_sim = settings["DS2"]["simulated"]
    name = settings["DS2"]["name"]
    publisher.publish(name, duration, is_sim)
    print_event("[DS2] (Door Sensor)", f"duration={duration}")


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


# ===== CLI (za 4SD kontrolu) =====

def cli_loop(display, stop_event):
    help_text = (
        "\nCommands:\n"
        "  set <seconds>\n"
        "  add <seconds>\n"
        "  start\n"
        "  stop\n"
        "  blink\n"
        "  clear\n"
        "  help\n"
        "  exit\n"
    )

    print(help_text)

    name = settings['4SD']["name"]
    simulated = settings['4SD']["simulated"]

    while not stop_event.is_set():
        try:
            cmd = input("pi2> ").strip()
        except (EOFError, KeyboardInterrupt):
            cmd = "exit"

        if not cmd:
            continue

        parts = cmd.split()
        c = parts[0].lower()

        if c == "help":
            print(help_text)

        elif c == "set" and len(parts) == 2:
            try:
                sec = int(parts[1])
                display.set_time(sec)
                publisher.publish(name, sec, simulated)
                print_event("[4SD]", f"set={sec}")
            except ValueError:
                print("Invalid number.")

        elif c == "add" and len(parts) == 2:
            try:
                sec = int(parts[1])
                display.add_seconds(sec)
                publisher.publish(name, sec, simulated)
                print_event("[4SD]", f"add={sec}")
            except ValueError:
                print("Invalid number.")

        elif c == "start":
            display.start()
            print_event("[4SD]", "started")

        elif c == "stop":
            display.stop()
            print_event("[4SD]", "stopped")

        elif c == "blink":
            display.blink()
            print_event("[4SD]", "blinking")

        elif c == "clear":
            display.set_time(0)
            display.stop()
            print_event("[4SD]", "cleared")

        elif c == "exit":
            stop_event.set()

        else:
            print("Unknown command.")



# ===== MAIN =====

def main():
    global publisher, settings

    print("Starting PI2 app")

    settings = load_settings("pi_two")
    publisher = MqttHandler(settings)

    poll_delay = float(settings.get("delay_sec", 2))

    threads = []
    stop_event = threading.Event()

    # --- Actuator ---
    display = create_4sd(settings["4SD"])

    # --- Sensors ---
    run_btn({**settings["BTN"], "delay_sec": 0.1}, threads, stop_event, btn_cb)
    run_dht({**settings["DHT3"], "delay_sec": 3}, threads, stop_event, dht3_cb)
    run_gsg({**settings["GSG"], "delay_sec": 0.2}, threads, stop_event, gsg_cb)
    run_ds({**settings["DS2"], "delay_sec": poll_delay}, threads, stop_event, ds2_cb)
    run_dpir({**settings["DPIR2"], "delay_sec": poll_delay}, threads, stop_event, dpir2_cb)
    run_dus({**settings["DUS2"], "delay_sec": poll_delay}, threads, stop_event, dus2_cb)

    try:
        cli_loop(display, stop_event)
    finally:
        try:
            display.cleanup()
        except Exception:
            pass

        stop_event.set()

        for t in threads:
            t.join()

        publisher.stop()
        time.sleep(0.2)


if __name__ == "__main__":
    main()
