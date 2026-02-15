import threading
import time

from components.components.ir import run_ir
from components.components.brgb import create_brgb
from components.components.lcd import create_lcd
from components.components.dht import run_dht
from components.components.dpir import run_dpir

from settings import load_settings
from mqtt_handler import MqttHandler


publisher = None
settings = None

recentDhtMetrics = []
metrics_lock = threading.Lock()


def ts():
    t = time.localtime()
    return time.strftime('%H:%M:%S', t)


def print_event(label: str, payload: str):
    print("=" * 28)
    print(f"[{ts()}] {label}")
    print(payload)


# ===== CALLBACKS =====

def ir_cb(button_name: str):
    is_sim = settings["IR"]["simulated"]
    name = settings["IR"]["name"]

    publisher.publish(name, button_name, is_sim)
    print_event("[IR]", f"button={button_name}")



def dht1_cb(payload):
    is_sim = settings["DHT1"]["simulated"]
    name = settings["DHT1"]["name"]

    publisher.publish(name, payload, is_sim)
    #print_event("[DHT1]", str(payload))


def dht2_cb(payload):
    is_sim = settings["DHT2"]["simulated"]
    name = settings["DHT2"]["name"]

    publisher.publish(name, payload, is_sim)
    #print_event("[DHT2]", str(payload))


def dpir3_cb(motion: bool):
    is_sim = settings["DPIR3"]["simulated"]
    name = settings["DPIR3"]["name"]

    publisher.publish(name, motion, is_sim)
    print_event("[DPIR3]", f"motion={motion}")


# ===== CLI (RGB + LCD kontrola) =====

def cli_loop(rgb, lcd, stop_event):
    help_text = (
        "\nCommands:\n"
        "  rgb on\n"
        "  rgb off\n"
        "  rgb r g b   (0 or 1)\n"
        "  lcd <line1> | <line2>\n"
        "  clear\n"
        "  help\n"
        "  exit\n"
    )

    print(help_text)

    name_rgb = settings["BRGB"]["name"]
    is_sim_rgb = settings["BRGB"]['simulated']

    name_lcd = settings["LCD"]["name"]
    is_sim_lcd = settings["LCD"]['simulated']

    while not stop_event.is_set():
        try:
            cmd = input("pi3> ").strip()
        except (EOFError, KeyboardInterrupt):
            cmd = "exit"

        if not cmd:
            continue

        parts = cmd.split()
        c = parts[0].lower()

        if c == "help":
            print(help_text)

        elif c == "rgb":

            if len(parts) == 2 and parts[1].lower() == "on":
                rgb.on()
                publisher.publish(name_rgb, {"r":1,"g":1,"b":1}, is_sim_rgb)
                print_event("[BRGB]", "on")

            elif len(parts) == 2 and parts[1].lower() == "off":
                rgb.off()
                publisher.publish(name_rgb, {"r":0,"g":0,"b":0}, is_sim_rgb)
                print_event("[BRGB]", "off")

            elif len(parts) == 4:
                try:
                    r = int(parts[1])
                    g = int(parts[2])
                    b = int(parts[3])

                    if r in (0,1) and g in (0,1) and b in (0,1):
                        rgb.set_color(r, g, b)
                        publisher.publish(name_rgb, {"r":r,"g":g,"b":b}, is_sim_rgb)
                        print_event("[BRGB]", f"{r},{g},{b}")
                    else:
                        print("Values must be 0 or 1.")
                except ValueError:
                    print("Invalid RGB values.")

        elif c == "lcd":

            text = cmd[4:].strip()

            if "|" in text:
                line1, line2 = text.split("|", 1)
                line1 = line1.strip()
                line2 = line2.strip()
                lcd.display(line1, line2)

                publisher.publish(
                    name_lcd,
                    {"line1": line1, "line2": line2},
                    is_sim_lcd
                )

                print_event("[LCD]", f"{line1} | {line2}")

            else:
                lcd.display(text, "")
                publisher.publish(
                    name_lcd,
                    {"line1": text, "line2": ""},
                    is_sim_lcd
                )

                print_event("[LCD]", text)

        elif c == "clear":
            lcd.clear()
            publisher.publish(
                name_lcd,
                {"line1": "", "line2": ""},
                is_sim_lcd
            )
            print_event("[LCD]", "cleared")

        elif c == "exit":
            stop_event.set()

        else:
            print("Unknown command.")



def mqtt_message_handler(topic, payload):
    global recentDhtMetrics

    if "type" not in payload or payload['type'] != "DHT":
        return

    with metrics_lock:
        recentDhtMetrics = payload['metrics']

def lcd_rotation_loop(lcd, stop_event):
    index = 0

    name_lcd = settings["LCD"]["name"]
    is_sim_lcd = settings["LCD"]['simulated']

    last_display = None

    while not stop_event.is_set():

        with metrics_lock:
            metrics_copy = list(recentDhtMetrics)

        if metrics_copy:
            if index >= len(metrics_copy):
                index = 0

            metric = metrics_copy[index]

            temp = metric.get("temperature")
            hum = metric.get("humidity")

            line1 = f"Temp: {temp:.1f} C" if temp is not None else "Temp: --"
            line2 = f"Hum:  {hum:.1f} %" if hum is not None else "Hum:  --"

            line1 = line1[:16]
            line2 = line2[:16]

            display_tuple = (line1, line2)

            if display_tuple != last_display:
                lcd.display(line1, line2)

                publisher.publish(
                    name_lcd,
                    {"line1": line1, "line2": line2},
                    is_sim_lcd
                )

                last_display = display_tuple

            index += 1
        else:
            display_tuple = ("Waiting DHT...", "")

        time.sleep(10)




def main():
    global publisher, settings

    print("Starting PI3 app")

    settings = load_settings("pi_three")
    publisher = MqttHandler(settings, mqtt_message_handler)

    threads = []
    stop_event = threading.Event()

    rgb = create_brgb(settings["BRGB"])
    lcd = create_lcd(settings["LCD"])

    # run_ir({**settings["IR"], "delay_sec": poll_delay}, threads, stop_event, ir_cb)
    run_dht({**settings["DHT1"], "delay_sec": 3}, threads, stop_event, dht1_cb)
    run_dht({**settings["DHT2"], "delay_sec": 3}, threads, stop_event, dht2_cb)
    # run_dpir({**settings["DPIR3"], "delay_sec": poll_delay}, threads, stop_event, dpir3_cb)

    rotation_thread = threading.Thread(
        target=lcd_rotation_loop,
        args=(lcd, stop_event),
        daemon=True
    )
    rotation_thread.start()
    threads.append(rotation_thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()

    for t in threads:
        t.join()

    try:
        rgb.cleanup()
    except:
        pass

    try:
        lcd.cleanup()
    except:
        pass

    publisher.stop()



if __name__ == "__main__":
    main()
