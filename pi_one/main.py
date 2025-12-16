import threading
import time
from settings import load_settings

from components.ds import run_ds
from components.dpir import run_dpir
from components.dus import run_dus
from components.dms import run_dms
from components.dl import create_dl
from components.db import create_db

def ts():
    t = time.localtime()
    return time.strftime('%H:%M:%S', t)

def print_event(label: str, payload: str):
    print("=" * 28)
    print(f"[{ts()}] {label}")
    print(payload)

def ds1_cb(pressed: bool):
    print_event("[DS1] (Door Sensor / Button)", f"pressed={pressed}")

def dpir1_cb(motion: bool):
    print_event("[DPIR1] (Door Motion / PIR)", f"motion={motion}")

def dus1_cb(distance_cm):
    print_event("[DUS1] (Door Ultrasonic)", f"distance_cm={distance_cm}")

def dms_cb(key):
    print(f"[DMS] Pressed key: {key}")

def cli_loop(actuators, stop_event):
    help_text = (
        "\nCommands:\n"
        "  led on|off\n"
        "  buzzer on|off\n"
        "  beep [seconds]\n"
        "  status\n"
        "  help\n"
        "  exit\n"
    )
    print(help_text)
    while not stop_event.is_set():
        try:
            cmd = input("pi1> ").strip()
        except (EOFError, KeyboardInterrupt):
            cmd = "exit"

        if not cmd:
            continue
        parts = cmd.split()
        c = parts[0].lower()

        if c == "help":
            print(help_text)
        elif c == "status":
            print("Actuators:", ", ".join(sorted(actuators.keys())))
        elif c == "led" and len(parts) >= 2:
            if parts[1].lower() == "on":
                actuators["DL"].on()
            elif parts[1].lower() == "off":
                actuators["DL"].off()
        elif c == "buzzer" and len(parts) >= 2:
            if parts[1].lower() == "on":
                actuators["DB"].on()
            elif parts[1].lower() == "off":
                actuators["DB"].off()
        elif c == "beep":
            seconds = 0.2
            if len(parts) >= 2:
                try:
                    seconds = float(parts[1])
                except ValueError:
                    pass
            actuators["DB"].beep(seconds)
        elif c == "exit":
            stop_event.set()
        else:
            print("Unknown command. Type 'help'.")

def main():
    print("Starting PI1 app")
    settings = load_settings()
    poll_delay = float(settings.get("poll_delay_sec", 2))

    threads = []
    stop_event = threading.Event()

    actuators = {
        "DL": create_dl(settings["DL"]),
        "DB": create_db(settings["DB"]),
    }
    
    run_ds({**settings["DS1"], "poll_delay_sec": poll_delay}, threads, stop_event, ds1_cb)
    run_dpir({**settings["DPIR1"], "poll_delay_sec": poll_delay}, threads, stop_event, dpir1_cb)
    run_dus({**settings["DUS1"], "poll_delay_sec": poll_delay}, threads, stop_event, dus1_cb)
    run_dms(settings["DMS"], threads, stop_event, dms_cb)

    try:
        cli_loop(actuators, stop_event)
    finally:
        for a in actuators.values():
            try:
                a.cleanup()
            except Exception:
                pass
        stop_event.set()
        time.sleep(0.2)

if __name__ == "__main__":
    main()
