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
rgb_device = None



rgb_state = {"r": 0, "g": 0, "b": 0}
rgb_lock = threading.Lock()



recentDhtMetrics = []
metrics_lock = threading.Lock()



def ts():
    return time.strftime('%H:%M:%S', time.localtime())


def print_event(label: str, payload: str):
    print("=" * 28)
    print(f"[{ts()}] {label}")
    print(payload)



def set_rgb_state(r, g, b):
    global rgb_state

    name_rgb = settings["BRGB"]["name"]
    is_sim_rgb = settings["BRGB"]["simulated"]

    with rgb_lock:
        if rgb_state == {"r": r, "g": g, "b": b}:
            return

        rgb_device.set_color(r, g, b)
        rgb_state = {"r": r, "g": g, "b": b}

    publisher.publish(name_rgb, rgb_state, is_sim_rgb)
    print_event("[BRGB]", rgb_state)



def ir_cb(button_name: str):
    is_sim = settings["IR"]["simulated"]
    name = settings["IR"]["name"]

 
    publisher.publish(name, button_name, is_sim)


    if button_name == "1":
        set_rgb_state(1, 0, 0)      
    elif button_name == "2":
        set_rgb_state(0, 1, 0)      
    elif button_name == "3":
        set_rgb_state(0, 0, 1)     
    elif button_name == "OK":
        set_rgb_state(1, 1, 1)     
    elif button_name == "#":
        set_rgb_state(0, 0, 0)     


def dht1_cb(payload):
    publisher.publish(settings["DHT1"]["name"], payload, settings["DHT1"]["simulated"])


def dht2_cb(payload):
    publisher.publish(settings["DHT2"]["name"], payload, settings["DHT2"]["simulated"])


def dpir3_cb(motion: bool):
    publisher.publish(settings["DPIR3"]["name"], motion, settings["DPIR3"]["simulated"])



def mqtt_message_handler(topic, payload):
    global recentDhtMetrics

    if "type" not in payload:
        return

    if payload.get("type") == "DHT":
        with metrics_lock:
            recentDhtMetrics = payload["metrics"]

    if payload.get("type") == "BRGB":
        set_rgb_state(payload['red'], payload['green'], payload['blue'])



def lcd_rotation_loop(lcd, stop_event):
    index = 0

    name_lcd = settings["LCD"]["name"]
    is_sim_lcd = settings["LCD"]["simulated"]

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

            line1 = f"Temp: {temp:.1f} C" if temp else "Temp: --"
            line2 = f"Hum:  {hum:.1f} %" if hum else "Hum:  --"

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

            if display_tuple != last_display:
                lcd.display("Waiting DHT...", "")
                publisher.publish(
                    name_lcd,
                    {"line1": "Waiting DHT...", "line2": ""},
                    is_sim_lcd
                )
                last_display = display_tuple

        time.sleep(10)



def main():
    global publisher, settings, rgb_device

    print("Starting PI3 app")

    settings = load_settings("pi_three")
    publisher = MqttHandler(settings, mqtt_message_handler)

    threads = []
    stop_event = threading.Event()
    
    rgb_device = create_brgb(settings["BRGB"])
    lcd = create_lcd(settings["LCD"])


    #run_ir(settings["IR"], threads, stop_event, ir_cb)
    # run_dht({**settings["DHT1"], "delay_sec": 3}, threads, stop_event, dht1_cb)
    # run_dht({**settings["DHT2"], "delay_sec": 3}, threads, stop_event, dht2_cb)
    #run_dpir({**settings["DPIR3"], "delay_sec": 3}, threads, stop_event, dpir3_cb)


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
        rgb_device.cleanup()
    except:
        pass

    try:
        lcd.cleanup()
    except:
        pass

    publisher.stop()


if __name__ == "__main__":
    main()
