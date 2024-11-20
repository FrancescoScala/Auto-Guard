import sys, time, json, logging

import ecal.core.core as ecal_core
import requests
from ecal.core.subscriber import StringSubscriber
from enum import Enum
from signals import Signals, parse_signals
from report_dto import ReportDTO
from collections import deque

logger = logging.getLogger("Log Publisher App")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)


'''
negative acc for brake
we have timestamp
if the speed change from 50 to 10 in small amount of time.

collection of records
'''

def push_reportdto(report):
     # Serialize the report to JSON 
    report_json = json.dumps(report, default=lambda o: o.__dict__, indent=4)
    print(report_json)
    # TODO: think about how to set the uri
    url = "http://example.com/api/report"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=report_json)
    print(response.status_code, response.text)

class CriticalLevel(Enum):
    LOW_LEVEL = 0
    MID_LEVEL = 1
    HIGH_LEVEL = 2


class LogPublisherApp(object):
    def __init__(self):
        # Create a subscriber that listens on the "traffic_sign_detection"
        self.sub = StringSubscriber("vehicle_dynamics")
        self.prev_long_acc = 0
        self.prev_lat_acc = 0
        self.emergency_brake = False
        self.prev_timestamp = 0
        self.speed_threshold = 10 # threshold for the speed
        self.criticial_speed_thresholds = {
            20: CriticalLevel.LOW_LEVEL,
            30: CriticalLevel.MID_LEVEL,
            40: CriticalLevel.HIGH_LEVEL
            }
        self.previous_speed = 100
        self.signals_list = deque(maxlen=50)

        
    def run(self):
        # object_detection_sub = StringSubscriber("object_detection") # to detect the construction site sign

        # Set the Callback
        self.sub.set_callback(self.callback)

        # object_detection_sub.set_callback(object_detection_callback)
        
        # Just don't exit
        while ecal_core.ok():
            time.sleep(0.5)

    # Callback for receiving messages
    def callback(self, topic_name, msg, time):
        try:
            # json_msg = json.loads(msg)
            signal_schema: Signals = parse_signals(msg)
            self.signals_list.append(signal_schema)
            # print(f"Received: {msg}")
            # Detect acceleration and set emergency brake flag
            long_acc = signal_schema.longAcc
            timestamp = signal_schema.timestamp
            speed = signal_schema.speed
            # if (long_acc - self.prev_long_acc) < 0: # means it is decelerating
            #     self.emergency_brake = True
            #     print("emegency brake because of long acc")

            if speed < self.previous_speed:
                speed_diff = abs(speed - self.previous_speed)
                critical_level = None

                for key, value in self.criticial_speed_thresholds.items():
                    if speed_diff > key:
                        critical_level = value
                        self.emergency_brake = True

                print(f"speed diff is {speed_diff} and critical level is {critical_level}")

            if self.emergency_brake:
                report = ReportDTO(
                    schema_version="1.0",
                    vehicle_id="XYZ123", 
                    start_timestamp=self.prev_timestamp, 
                    stop_timestamp=timestamp, 
                    criticality_level=critical_level, 
                    vehicle_dynamics=self.signals_list
                )
                
                push_reportdto(report)

            print(f"Emergency Brake: {self.emergency_brake}")

            self.prev_long_acc = long_acc
            print(f"timestamp difference: {timestamp-self.prev_timestamp}")
            self.prev_timestamp = timestamp

            self.previous_speed = speed
            self.emergency_brake = False # reset

        except json.JSONDecodeError:
            logger.error(f"Error: Could not decode message: '{msg}'")
        except Exception as e:
            logger.error(f"Error: {e}")

# def object_detection_callback(topic_name, msg, time):
#     try:
#         json_msg = json.loads(msg)
#         print(f"Received Object Detection: {msg}")
#     except json.JSONDecodeError:
#         logger.error(f"Error: Could not decode message: '{msg}'")
#     except Exception as e:
#         logger.error(f"Error: {e}")

def main():
    log_publisher_app = LogPublisherApp()
    log_publisher_app.run()

if __name__ == "__main__":
    # main()
    logger.info("Starting Log Publisher App")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Log Publisher App")
    main()
    # finalize eCAL API
    ecal_core.finalize()
