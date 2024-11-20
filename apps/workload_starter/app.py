import sys, time, logging, os, json, socket, ssl
import paho.mqtt.client as mqtt
from ankaios_sdk import Workload, Ankaios, WorkloadStateEnum, WorkloadSubStateEnum, AnkaiosLogLevel, Manifest, Request, CompleteState, UpdateStateSuccess

NAME: str = "workload_starter"
VEHICLE_ID: str = os.environ.get("VIN")
MQTT_BROKER_ADDR: str = os.environ.get('MQTT_BROKER_ADDR')
MQTT_BROKER_PORT: int = int(os.environ.get('MQTT_BROKER_PORT'))
MQTT_BROKER_USER: str = os.environ.get('MQTT_BROKER_USER')
MQTT_BROKER_PASS: str = os.environ.get('MQTT_BROKER_PASS')
BASE_TOPIC: str = f"/vehicle/{VEHICLE_ID}"

logger: logging.Logger = logging.getLogger(NAME)
stdout: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)
formatter: logging.Formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
stdout.setFormatter(formatter)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

def run(mqtt_client: mqtt.Client) -> None:
    with Ankaios() as ankaios:

        # Callback when the client receives a CONNACK response from the MQTT server
        def on_connect(client, userdata, flags, reason_code, properties):
            for topic in ["start", "stop"]:
                client.subscribe(f"{BASE_TOPIC}/{topic}")
                logger.info(f"Subscribed to {BASE_TOPIC}/{topic}")

        # Callback when a PUBLISH message is received from the MQTT server
        def on_message(client, userdata, msg):
            try:
                logger.info(f"Received message on topic {msg.topic}")
                # Handle request for applying a manifest
                if msg.topic == f"{BASE_TOPIC}/start":
                    manifest: Manifest = Manifest.from_string(str(msg.payload.decode()))
                    workload_list: list = list(manifest._manifest['workloads'].keys())
                    logger.info(f"starting workloads {', '.join(workload_list)}")
                    ret: UpdateStateSuccess = ankaios.apply_manifest(manifest)
                    if ret is not None:
                        client.publish(f"{BASE_TOPIC}/status", json.dumps(ret.to_dict()))
                        created_workloads: list = [wl["workload_name"] for wl in ret.to_dict()['added_workloads']]
                        logger.info(f"workloads {', '.join(created_workloads)} started")
                # Handle request for deleting a manifest
                elif msg.topic == f"{BASE_TOPIC}/stop":
                    manifest: Manifest = Manifest.from_string(str(msg.payload.decode()))
                    workload_list: list = list(manifest._manifest['workloads'].keys())
                    logger.info(f"stopping workloads {', '.join(workload_list)}")
                    ret: UpdateStateSuccess = ankaios.delete_manifest(manifest)
                    if ret is not None:
                        client.publish(f"{BASE_TOPIC}/status", json.dumps(ret.to_dict()))
                        deleted_workloads: list = [wl["workload_name"] for wl in ret.to_dict()['deleted_workloads']]
                        logger.info(f"workloads {', '.join(deleted_workloads)} stopped")
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
            for agent, workload in states.items():
                for workload_name, workload_details in workload.items():
                    logger.info(f"{agent}: {workload_name} ({list(workload_details.values())[0]['substate']})")
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
        