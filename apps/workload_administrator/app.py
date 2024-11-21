import sys, time, logging, os, json, socket, ssl
import paho.mqtt.client as mqtt
from ankaios_sdk import Ankaios, Manifest, UpdateStateSuccess, Workload

# env vars
NAME: str = "workload_administrator"
VEHICLE_ID: str = os.environ.get("VIN")
MQTT_BROKER_ADDR: str = os.environ.get('MQTT_BROKER_ADDR')
MQTT_BROKER_PORT: int = int(os.environ.get('MQTT_BROKER_PORT'))
MQTT_BROKER_USER: str = os.environ.get('MQTT_BROKER_USER')
MQTT_BROKER_PASS: str = os.environ.get('MQTT_BROKER_PASS')
BASE_TOPIC: str = f"/vehicle/{VEHICLE_ID}"
ALL_BASE_TOPIC: str = f"/vehicle/all"

# logging
logger: logging.Logger = logging.getLogger(NAME)
stdout: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)
formatter: logging.Formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
stdout.setFormatter(formatter)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

def send_workload_change(client: mqtt.Client, ret: UpdateStateSuccess, key: str) -> None:
    if ret is None:
        return
    logger.debug(json.dumps(ret.to_dict()))
    created_workloads: list[str] = [wl["workload_name"] for wl in ret.to_dict()[key]]
    if created_workloads:
        message: str = f"Workloads {', '.join(created_workloads)} {key.split('_')[0]}"
    else:
        message: str = f"No workloads {key.split('_')[0]}"
    logger.info(message)
    client.publish(f"{BASE_TOPIC}/change", message)

def send_workload_state(client: mqtt.Client, messages: list[str]) -> None:
    logger.info("current status:\n\t" + "\n\t".join(messages))
    client.publish(f"{BASE_TOPIC}/status", "\n".join(messages))

def run(mqtt_client: mqtt.Client) -> None:
    with Ankaios() as ankaios:

        # Callback when the client receives a CONNACK response from the MQTT server
        def on_connect(client, userdata, flags, reason_code, properties):
            for topic in ["manifest/apply", "manifest/delete", "workload/start", "workload/stop"]:
                client.subscribe(f"{BASE_TOPIC}/{topic}")
                logger.info(f"Subscribed to {BASE_TOPIC}/{topic}")
                client.subscribe(f"{ALL_BASE_TOPIC}/{topic}")
                logger.info(f"Subscribed to {ALL_BASE_TOPIC}/{topic}")

        # Callback when a PUBLISH message is received from the MQTT server
        def on_message(client, userdata, msg):
            try:
                logger.debug(f"Received message on topic {msg.topic}")

                # handle manifest request
                if msg.topic.startswith(f"{BASE_TOPIC}/manifest/") or msg.topic.startswith(f"{ALL_BASE_TOPIC}/manifest/"):
                    # apply
                    manifest: Manifest = Manifest.from_string(str(msg.payload.decode()))
                    workload_list: list = list(manifest._manifest['workloads'].keys())
                    if msg.topic in [f"{BASE_TOPIC}/manifest/apply", f"{ALL_BASE_TOPIC}/manifest/apply"]:
                        logger.info(f"starting workloads {', '.join(workload_list)}")
                        ret: UpdateStateSuccess = ankaios.apply_manifest(manifest)
                        send_workload_change(client, ret, 'added_workloads')

                    # delete
                    elif msg.topic in [f"{BASE_TOPIC}/manifest/delete", f"{ALL_BASE_TOPIC}/manifest/delete"]:
                        logger.info(f"stopping workloads {', '.join(workload_list)}")
                        ret: UpdateStateSuccess = ankaios.delete_manifest(manifest)
                        send_workload_change(client, ret, 'deleted_workloads')

                # handle workload requests
                elif msg.topic.startswith(f"{BASE_TOPIC}/workload/") or msg.topic.startswith(f"{ALL_BASE_TOPIC}/workload/"):
                    payload: str = str(msg.payload.decode())
                    # start
                    if msg.topic in [f"{BASE_TOPIC}/workload/start", f"{ALL_BASE_TOPIC}/workload/start"]:
                        details: dict = json.loads(payload)
                        workload: Workload = Workload(details["name"])
                        workload.update_agent_name(details["agent"])
                        workload.update_restart_policy(details["restart_policy"].upper())
                        workload.update_runtime_config(f"image: {details['image']}\ncommandOptions: {json.dumps(details['options'])}")
                        workload.update_runtime("podman")
                        ret: UpdateStateSuccess = ankaios.apply_workload(workload)
                        send_workload_change(client, ret, 'added_workloads')
                    # stop
                    if msg.topic in [f"{BASE_TOPIC}/workload/stop", f"{ALL_BASE_TOPIC}/workload/stop"]:
                        ret: UpdateStateSuccess = ankaios.delete_workload(payload)
                        send_workload_change(client, ret, 'deleted_workloads')
            except Exception as e:
                logger.error(f"Error processing message: {e}")

        # Connect to the MQTT broker
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        logger.info(f"Connecting to MQTT broker {MQTT_BROKER_ADDR}:{MQTT_BROKER_PORT}")
        mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        mqtt_client.tls_insecure_set(False)
        mqtt_client.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PASS)
        mqtt_client.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)
        logger.info("Successfully connected to the MQTT broker")
        mqtt_client.loop_start()

        while True:
            states: dict = ankaios.get_state(field_masks=["workloadStates"]).to_dict()['workload_states']
            messages: list[str] = []
            for agent, workload in states.items():
                for workload_name, workload_details in workload.items():
                    messages.append(f"{agent}: {workload_name} ({list(workload_details.values())[0]['substate']})")
            send_workload_state(mqtt_client, messages)
            time.sleep(10)


if __name__ == "__main__":
    logger.info(f"Starting {NAME} on {VEHICLE_ID}...")
    mqtt_client: mqtt.Client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        protocol=mqtt.MQTTv5,
        transport="websockets",
        client_id=f"vehicle_{VEHICLE_ID}")

    try:
        run(mqtt_client)
    except socket.gaierror:
        logger.fatal("Could not connect to the MQTT broker")
    except:
        pass
    finally:
        mqtt_client.disconnect()
        