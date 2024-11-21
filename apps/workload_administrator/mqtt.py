""" MQTT functionality """
# pylint: disable=unused-argument,line-too-long

import json
import ssl
import logging
from ankaios_sdk import Ankaios, Manifest, UpdateStateSuccess, Workload
from config import NAME, BASE_TOPIC, ALL_BASE_TOPIC, MQTT_BROKER_ADDR, MQTT_BROKER_PASS, MQTT_BROKER_PORT, MQTT_BROKER_USER
import paho.mqtt.client as mqtt

logger: logging.Logger = logging.getLogger(NAME)

def send_workload_change(mqtt_client: mqtt.Client, ret: UpdateStateSuccess, key: str) -> None:
    """
    send the workload change via MQTT and also log to the console
    """
    if ret is None:
        return
    logger.debug(json.dumps(ret.to_dict()))
    created_workloads: list[str] = [wl["workload_name"] for wl in ret.to_dict()[key]]
    if created_workloads:
        message: str = f"Workloads {', '.join(created_workloads)} {key.split('_')[0]}"
    else:
        message: str = f"No workloads {key.split('_')[0]}"
    logger.info(message)
    mqtt_client.publish(f"{BASE_TOPIC}/change", message)

def send_workload_state(mqtt_client: mqtt.Client, messages: list[str]) -> None:
    """
    send the workload state (which workloads are currently in which state) via MQTT and also log to the console
    """
    logger.info("current status:\n\t%s", "\n\t".join(messages))
    mqtt_client.publish(f"{BASE_TOPIC}/status", "\n".join(messages))

def mqtt_setup(ankaios: Ankaios, mqtt_client: mqtt.Client) -> None:
    """
    set up the MQTT connection; also includes the MQTT callback functions
    """
    # callback when the client receives a CONNACK response from the MQTT server
    def on_connect(client_obj, userdata, flags, reason_code, properties):
        # subscribe to the required topics
        for topic in ["manifest/apply", "manifest/delete", "workload/start", "workload/stop"]:
            client_obj.subscribe(f"{BASE_TOPIC}/{topic}")
            logger.info("Subscribed to %s/%s", BASE_TOPIC, topic)
            client_obj.subscribe(f"{ALL_BASE_TOPIC}/{topic}")
            logger.info("Subscribed to %s/%s", ALL_BASE_TOPIC, topic)

    # callback when a PUBLISH message is received from the MQTT server
    def on_message(client_obj, userdata, msg):
        try:
            logger.debug("Received message on topic %s", msg.topic)

            # handle manifest request
            if msg.topic.startswith(f"{BASE_TOPIC}/manifest/") or msg.topic.startswith(f"{ALL_BASE_TOPIC}/manifest/"):
                # manifest apply
                manifest: Manifest = Manifest.from_string(str(msg.payload.decode()))
                workload_list: list = list(manifest._manifest['workloads'].keys())# pylint:disable=protected-access
                if msg.topic in [f"{BASE_TOPIC}/manifest/apply", f"{ALL_BASE_TOPIC}/manifest/apply"]:
                    logger.info("starting workloads %s", ", ".join(workload_list))
                    ret: UpdateStateSuccess = ankaios.apply_manifest(manifest)
                    send_workload_change(client_obj, ret, 'added_workloads')

                # manifest delete
                elif msg.topic in [f"{BASE_TOPIC}/manifest/delete", f"{ALL_BASE_TOPIC}/manifest/delete"]:
                    logger.info("stopping workloads %s", ", ".join(workload_list))
                    ret: UpdateStateSuccess = ankaios.delete_manifest(manifest)
                    send_workload_change(client_obj, ret, 'deleted_workloads')

            # handle workload requests
            elif msg.topic.startswith(f"{BASE_TOPIC}/workload/") or msg.topic.startswith(f"{ALL_BASE_TOPIC}/workload/"):
                payload: str = str(msg.payload.decode())
                # workload start
                if msg.topic in [f"{BASE_TOPIC}/workload/start", f"{ALL_BASE_TOPIC}/workload/start"]:
                    details: dict = json.loads(payload)
                    workload: Workload = Workload(details["name"])
                    workload.update_agent_name(details["agent"])
                    workload.update_restart_policy(details["restart_policy"].upper())
                    workload.update_runtime_config(f"image: {details['image']}\ncommandOptions: {json.dumps(details['options'])}")
                    workload.update_runtime("podman")
                    ret: UpdateStateSuccess = ankaios.apply_workload(workload)
                    send_workload_change(client_obj, ret, 'added_workloads')
                # workload stop
                if msg.topic in [f"{BASE_TOPIC}/workload/stop", f"{ALL_BASE_TOPIC}/workload/stop"]:
                    ret: UpdateStateSuccess = ankaios.delete_workload(payload)
                    send_workload_change(client_obj, ret, 'deleted_workloads')
        except Exception as e: # pylint:disable=broad-exception-caught
            logger.error("Error processing message: %s", str(e))

    # Connect to the MQTT broker using TLS secured websocket
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    logger.info("Connecting to MQTT broker %s:%i", MQTT_BROKER_ADDR, MQTT_BROKER_PORT)
    mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    mqtt_client.tls_insecure_set(False)
    mqtt_client.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PASS)
    mqtt_client.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)
    logger.info("Successfully connected to the MQTT broker")

    # run the MQTT routine in the background
    mqtt_client.loop_start()
