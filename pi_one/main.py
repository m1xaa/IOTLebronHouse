import threading
import time
from components.components.db import create_db
from components.components.dl import create_dl
from components.components.dms import run_dms
from components.components.dpir import run_dpir
from components.components.ds import run_ds
from components.components.dus import run_dus
from settings import load_settings
from mqtt_handler import MqttHandler


publisher = None
settings = None
dl_timer = None
dl_lock = threading.Lock()
actuators = {}

def ts():
    t = time.localtime()
    return time.strftime('%H:%M:%S', t)

def print_event(label: str, payload: str):
    print("=" * 28)
    print(f"[{ts()}] {label}")
    print(payload)

def ds1_cb(event):
    is_sim = settings["DS1"]["simulated"]
    name = settings["DS1"]["name"]
    publisher.publish(name, event, is_sim)
    print_event("[DS1] (Door Sensor / Button)", f"event={event}")

def dpir1_cb(motion: bool):
    global dl_timer

    is_sim = settings["DPIR1"]["simulated"]
    name = settings["DPIR1"]["name"]
    publisher.publish(name, motion, is_sim)
    print_event("[DPIR1] (Door Motion / PIR)", f"motion={motion}")

    if not motion:
        return

    with dl_lock:
        actuators["DL"].on()
        publisher.publish(settings['DL']['name'], True, settings['DL']['simulated'])
        print_event("[DL1]", "on (motion), scheduling off in 10s")

        if dl_timer is not None:
            dl_timer.cancel()
        dl_timer = threading.Timer(10.0, dl_off)
        dl_timer.daemon = True
        dl_timer.start()

def dus1_cb(distance_cm):
    is_sim = settings["DUS1"]["simulated"]
    name = settings["DUS1"]["name"]
    if distance_cm is not None:
        publisher.publish(name, distance_cm, is_sim)
    print_event("[DUS1] (Door Ultrasonic)", f"distance_cm={distance_cm}")

def dms_cb(pin: str):
    is_sim = settings["DMS"]["simulated"]
    name = settings["DMS"]["name"]
    publisher.publish(name, pin, is_sim)
    print_event("[DMS] (Membrane Switch)", f"PIN entered: {pin}")

def dl_off():
    with dl_lock:
        try:
            actuators["DL"].off()
            publisher.publish(settings['DL']['name'], False, settings['DL']['simulated'])
            print_event("[DL1]", "auto-off after 10s")
        except Exception as e:
            print_event("[DL1]", f"auto-off error: {e}")

def cli_loop(actuators, stop_event):
    help_text = (
        "\nCommands:\n"
        "  led on|off\n"
        "  buzzer on|off\n"
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

        name_dl = settings['DL']['name']
        name_db = settings['DB']['name']

        if c == "help":
            print(help_text)

        elif c == "status":
            print("Actuators:", ", ".join(sorted(actuators.keys())))

        elif c == "led" and len(parts) >= 2:
            is_sim = settings["DL"].get("simulated", True)
            if parts[1].lower() == "on":
                actuators["DL"].on()
                publisher.publish(name_dl, True, is_sim)
            elif parts[1].lower() == "off":
                actuators["DL"].off()
                publisher.publish(name_dl, False, is_sim)

        elif c == "buzzer" and len(parts) >= 2:
            is_sim = settings["DB"].get("simulated", True)
            if parts[1].lower() == "on":
                actuators["DB"].on()
                publisher.publish(name_db, True, is_sim)
            elif parts[1].lower() == "off":
                actuators["DB"].off()
                publisher.publish(name_db, False, is_sim)

        elif c == "exit":
            stop_event.set()

        else:
            print("Unknown command. Type 'help'.")

def mqtt_message_handler(topic, payload):
    if payload.get("type") == "ALARM":
        handle_alarm_state_changed(payload)

def handle_alarm_state_changed(payload):
    global actuators, settings

    state = payload.get("state")
    print_event("[ALARM MESSAGE]", f"state={state}")

    name_dl = settings["DL"]["name"]
    name_db = settings["DB"]["name"]

    is_sim_dl = settings["DL"].get("simulated", True)
    is_sim_db = settings["DB"].get("simulated", True)

    if state == "ALARM":
        actuators["DL"].on()
        actuators["DB"].on()

        publisher.publish(name_dl, True, is_sim_dl)
        publisher.publish(name_db, True, is_sim_db)

        print_event("[ALARM ACTION]", "DL + DB ON")

    else:  
        actuators["DL"].off()
        actuators["DB"].off()

        publisher.publish(name_dl, False, is_sim_dl)
        publisher.publish(name_db, False, is_sim_db)

        print_event("[ALARM ACTION]", "DL + DB OFF")

def main():
    global publisher, settings, dl_timer, dl_lock, actuators

    print("Starting PI1 app")

    settings = load_settings("pi_one")
    publisher = MqttHandler(settings, mqtt_message_handler)
    poll_delay = float(settings.get("delay_sec", 2))

    threads = []
    stop_event = threading.Event()

    actuators = {
        "DL": create_dl(settings["DL"]),
        "DB": create_db(settings["DB"]),
    }



    run_ds({**settings["DS1"], "delay_sec": poll_delay}, threads, stop_event, ds1_cb)
    # run_dpir({**settings["DPIR1"], "delay_sec": poll_delay}, threads, stop_event, dpir1_cb)
    # run_dus({**settings["DUS1"], "delay_sec": poll_delay}, threads, stop_event, dus1_cb)
    # run_dms(settings["DMS"], threads, stop_event, dms_cb)

    try:
        cli_loop(actuators, stop_event)
    finally:
        for a in actuators.values():
            try:
                a.cleanup()
            except Exception:
                pass

        stop_event.set()
        publisher.stop()
        time.sleep(0.2)

if __name__ == "__main__":
    main()
