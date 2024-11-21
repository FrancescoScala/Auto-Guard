import os

import paho.mqtt.client as mqtt

MQTT_BROKER_ADDR: str = os.environ.get('MQTT_BROKER_ADDR',
                                       default="3345d71141b94f0eb2ec8c60a153d4d3.s1.eu.hivemq.cloud")
MQTT_BROKER_PORT: int = int(os.environ.get('MQTT_BROKER_PORT', default=8884))
MQTT_BROKER_USER: str = os.environ.get('MQTT_BROKER_USER', default="hackathon")
MQTT_BROKER_PASS: str = os.environ.get('MQTT_BROKER_PASS', default="CaliperKing7")


# Define callback functions
def on_connect(client, userdata, flags, rc, props):
    if rc == 0:
        print("Connected successfully!")
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")


def publish_config(config_data):
    try:
        mqttc.publish("hackathon/triggers/config", config_data, retain=True).wait_for_publish(timeout=20)
        print("Message sent successfully")
    except Exception as e:
        print(f"Error publishing config: {e}")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5, transport="websockets",
                    client_id="hackathon_backend_service")
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
mqttc.tls_insecure_set(False)
mqttc.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PASS)
mqttc.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)
mqttc.loop_start()
