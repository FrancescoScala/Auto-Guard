import os

import paho.mqtt.client as mqtt

MQTT_BROKER_ADDR: str = os.environ.get('MQTT_BROKER_ADDR',
                                       default="3345d71141b94f0eb2ec8c60a153d4d3.s1.eu.hivemq.cloud")
MQTT_BROKER_PORT: int = int(os.environ.get('MQTT_BROKER_PORT', default=8884))
MQTT_BROKER_USER: str = os.environ.get('MQTT_BROKER_USER', default="hackathon")
MQTT_BROKER_PASS: str = os.environ.get('MQTT_BROKER_PASS', default="CaliperKing7")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")


def on_connect(client, userdata, flags, rc, props):
    if rc == 0:
        pass
        # print("Connected successfully!")
    else:
        print(f"Connection failed with code {rc}")


class MqttClient:
    def __init__(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5, transport="websockets",
                            client_id="hackathon_backend_service")
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message
        self.mqttc.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.mqttc.tls_insecure_set(False)
        self.mqttc.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PASS)
        self.mqttc.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)
        self.mqttc.loop_start()

    # Define callback functions

    def publish_config(self, config_data):
        try:
            self.mqttc.publish("hackathon/triggers/config", config_data, retain=True).wait_for_publish(timeout=20)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error publishing config: {e}")