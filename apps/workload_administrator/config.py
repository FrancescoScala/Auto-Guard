""" config file """

import os

# env vars
VEHICLE_ID: str = os.environ["VIN"] # required
MQTT_BROKER_ADDR: str = os.environ['MQTT_BROKER_ADDR'] # required
MQTT_BROKER_PORT: int = int(os.environ['MQTT_BROKER_PORT']) # required
MQTT_BROKER_USER: str = os.environ['MQTT_BROKER_USER'] # required
MQTT_BROKER_PASS: str = os.environ['MQTT_BROKER_PASS'] # required

# configuration constants
NAME: str = "workload_administrator"
BASE_TOPIC: str = f"/vehicle/{VEHICLE_ID}"
ALL_BASE_TOPIC: str = "/vehicle/all"
