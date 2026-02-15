import time
import json
import threading
import paho.mqtt.client as mqtt

class MqttHandler:
    def __init__(self, settings, on_message_callback=None):
        self.broker = settings["mqtt"]["broker"]
        self.port = settings["mqtt"]["port"]
        self.topic = settings["mqtt"]["topic"]
        self.pi_id = settings["PI_ID"]
        self.on_message_callback = on_message_callback
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        self.batch = []
        self.batch_lock = threading.Lock()
        self.stop_event = threading.Event()

        self.batch_thread = threading.Thread(target=self._batch_loop, daemon=True)
        self.batch_thread.start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT Broker with code {rc}")
        client.subscribe("home/all")
        print(f"[MQTT] Subscribed to: home/all")
        
        pi_topic = f"home/{self.pi_id}"
        client.subscribe(pi_topic)
        print(f"[MQTT] Subscribed to: {pi_topic}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            print(f"[MQTT] Received on {msg.topic}: {payload}")
            
            if self.on_message_callback:
                self.on_message_callback(msg.topic, payload)
                
        except json.JSONDecodeError:
            print(f"[MQTT] Invalid JSON received on {msg.topic}")
        except Exception as e:
            print(f"[MQTT] Error processing message: {e}")

    def _batch_loop(self):
        while not self.stop_event.is_set():
            time.sleep(5)
            with self.batch_lock:
                if self.batch:
                    payload = {
                        "pi_id": self.pi_id,
                        "batch": self.batch
                    }
                    self.client.publish(self.topic, json.dumps(payload))
                    print(f"[MQTT] Published batch of {len(self.batch)} items.")
                    self.batch = []

    def publish(self, component, value, is_simulated):
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        
        data_point = {
            "component": component,
            "value": value,
            "is_simulated": is_simulated,
            "timestamp": timestamp
        }
        with self.batch_lock:
            self.batch.append(data_point)
            print(f"[MQTT] Queued: {component}={value} (simulated={is_simulated})")

       
    def stop(self):
        self.stop_event.set()
        self.batch_thread.join(timeout=1)
        self.client.loop_stop()
        self.client.disconnect()