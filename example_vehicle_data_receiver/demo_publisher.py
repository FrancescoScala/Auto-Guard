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

import sys
import time

import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher

if __name__ == "__main__":
  # initialize eCAL API. The name of our Process will be "Vehicle Data Publisher"
  ecal_core.initialize(sys.argv, "Vehicle Data Publisher")

  # Create a String Publisher that publishes on the topic "vehicle_data_topic"
  pub = StringPublisher("vehicle_data_topic")
  
  # Create a counter, so something changes in our message
  counter = 0
  
  # Infinite loop (using ecal_core.ok() will enable us to gracefully shutdown
  # the process from another application)
  while ecal_core.ok():
    # Create a message with a counter an publish it to the topic
    current_message = f'{{"front-radar": {{"objects": []}}, "front-left-radar": {{"objects": []}}, "front-right-radar": {{"objects": []}}, "traffic-sign-detections": {{"signs": [], "probabilities": [], "boxes": []}}}}'
    print(f"Sending: {current_message}")
    pub.send(current_message)
    
    # Sleep 500 ms
    time.sleep(0.5)
    
    counter = counter + 1
  
  # finalize eCAL API
  ecal_core.finalize()