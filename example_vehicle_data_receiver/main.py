# Copyright (c) 2024 Elektrobit Automotive GmbH and others

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0

import sys, time, json

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

from queue import Queue

# setup logging
import os, logging
def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "INFO")

    if log_level.upper() not in ("TRACE", "INFO", "DEBUG", "WARN", "ERROR"):
        print(f"Invalid log level: '{log_level}'. Use one of TRACE, INFO, DEBUG, WARN, ERROR", file=sys.stderr)
        exit(1)
    logging.basicConfig(level=log_level, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    return logging.getLogger(__name__)

logger = setup_logger()
msg_queue = Queue() # already synchronized queue

# Callback for receiving messages
def callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        msg_queue.put(json_msg)
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Vehicle Data Subscriber")

    # Create a subscriber that listenes on the "vehicle_data_topic"
    sub = StringSubscriber("vehicle_data_topic")

    # Set the Callback
    sub.set_callback(callback)
    
    while ecal_core.ok():
        # Check if there are new messages
        if not msg_queue.empty():
            msg = msg_queue.get()
            logger.info(f"Vehicle data: {msg}")
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()