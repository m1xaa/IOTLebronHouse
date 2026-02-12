from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

url = "http://localhost:8086"
token = "v5HvugmRZJSuBkx7ajUtO1Bvy-i1faZCytQJQ02fim2B8SaV8TM8GfEYI_HDPenh5XEtYb2p73ZjZG3MjSZxYg=="
org = "iot"
bucket = "home"

influx_client = InfluxDBClient(url=url, token=token, org=org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

MQTT_BROKER = "localhost"
MQTT_TOPIC = "home/sensors"

def save_to_influx(data_point, pi_id):
    try:
        p = Point(data_point["component"]) \
            .tag("pi_id", pi_id) \
            .tag("simulated", str(data_point["is_simulated"])) \
            .field("value", data_point["value"])
            # InfluxDB adds the timestamp 
        
        write_api.write(bucket=bucket, org=org, record=p)
        print(f"Saved: {data_point['component']} = {data_point['value']}")
    except Exception as e:
        print(f"Error saving to InfluxDB: {e}")

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        pi_id = payload.get("pi_id", "unknown")

        # save batch
        if "batch" in payload:
            for item in payload["batch"]:
                save_to_influx(item, pi_id)

    except Exception as e:
        print(f"Message Error: {e}")

# run MQTT in a background thread so Flask can run
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    return "IoT Server Running"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)