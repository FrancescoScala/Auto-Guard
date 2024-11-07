from ankaios_sdk import Workload, Ankaios, WorkloadStateEnum, WorkloadSubStateEnum, AnkaiosLogLevel, Manifest, Request, CompleteState
import json
import os
import logging
import sys
import time

logger = logging.getLogger("symphony_provider")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

# Get config over environment variables
VEHICLE_ID = os.environ.get('VIN')

# Create a new Ankaios object.
# The connection to the control interface is automatically done at this step.
ankaios = Ankaios()


while True:
    # The following lines just showcase a simple interaction with Ankaios.
    # For more information checkout out the Ankaios fleet management tutorial: 
    # https://eclipse-ankaios.github.io/ankaios/latest/usage/tutorial-fleet-management/
    state = ankaios.get_state(field_masks=["workloadStates"])
    logger.info(f"Hello from vehicle {VEHICLE_ID}")
    logger.info(f"Got the following workload execution states from Ankaios: {state.to_dict()["workload_states"]}")
    time.sleep(3.14)
