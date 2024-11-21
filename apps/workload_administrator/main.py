""" main file """
# pylint: disable=unused-argument,line-too-long

import time
import logging
import socket
from paho.mqtt.client import Client, CallbackAPIVersion, MQTTv5
from ankaios_sdk import Ankaios
from config import NAME, VEHICLE_ID
from logger import setup_logger
from mqtt import mqtt_setup, send_workload_state

# logging setup
logger: logging.Logger = setup_logger()

def run(mqtt_client: Client) -> None:
    """
    run the main routine
    """
    with Ankaios() as ankaios:
        # set up MQTT connection which runs in a separate thread
        mqtt_setup(ankaios, mqtt_client)

        # run forever, determining the workloads' states every 3 seconds
        while True:
            states: dict = ankaios.get_state(field_masks=["workloadStates"]).to_dict()['workload_states']
            messages: list[str] = []
            for agent, workload in states.items():
                for workload_name, workload_details in workload.items():
                    messages.append(f"{agent}: {workload_name} ({list(workload_details.values())[0]['substate']})")
            send_workload_state(mqtt_client, messages)
            time.sleep(3)

if __name__ == "__main__":
    logger.info("Starting %s on %s...", NAME, VEHICLE_ID)

    # create an MQTT client object
    client: Client = Client(
        CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
        transport="websockets",
        client_id=f"vehicle_{VEHICLE_ID}")

    # error handling for the main routine
    try:
        # run the main routine
        run(client)
    except socket.gaierror:
        logger.fatal("Could not connect to the MQTT broker")
    except Exception as error: # pylint:disable=broad-exception-caught
        logger.error("Error in main routine: %s", str(error))
    finally:
        # gracefully disconnect from MQTT broker
        logger.info("shutting down gracefully")
        client.disconnect()
