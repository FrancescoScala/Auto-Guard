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

class LogPublisherApp(object):
    criticial_speed_thresholds = {20: 1, 30: 2, 40: 3}
    vehicle_dynamics_samples = deque(maxlen=50)

        
    def run(self):
        vehicle_dynamics_sub = StringSubscriber("vehicle_dynamics")
        vehicle_dynamics_sub.set_callback(self.vehicle_dynamics_callback)

        # object_detection_sub = StringSubscriber("object_detection") # to detect the construction site sign
        # object_detection_sub.set_callback(object_detection_callback)
        
        while ecal_core.ok():
            time.sleep(0.5)

    def publish_report(self, critical_level, timestamp):
        report = ReportDTO(
            schema_version="1.0",
            vehicle_id="XYZ123", 
            stop_timestamp=timestamp, 
            criticality_level=critical_level, 
            vehicle_dynamics=self.vehicle_dynamics_samples
        )
        
        report_json = json.dumps(report.to_dict())
        logger.info('report', report_json)
        url = "http://example.com/api/report"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=report_json)
        logger.info(response.status_code, response.text)

    # Callback for receiving vehicle_dynamics messages
    def vehicle_dynamics_callback(self, topic_name, msg, time):
        def add_signal():
            signal_schema: Signals = parse_signals(msg)
            self.vehicle_dynamics_samples.append(signal_schema)

        def detect_trigger() -> int:
            curr_signal = self.vehicle_dynamics_samples[-1]
            last_signal = self.vehicle_dynamics_samples[-2]

            if curr_signal.speed < last_signal.speed:
                speed_diff = last_signal.speed - curr_signal.speed

                for key, value in self.criticial_speed_thresholds.items():
                    if speed_diff > key:
                        return value
                return 0

        try:
            add_signal()
            critical_level = detect_trigger()
            if critical_level > 0:
                self.publish_report(critical_level, time)

        except json.JSONDecodeError:
            logger.error(f"Error: Could not decode message: '{msg}'")
        except Exception as e:
            logger.error(f"Error: {e}")


# def object_detection_callback(topic_name, msg, time):
#     try:
#         json_msg = json.loads(msg)
#         logger.info(f"Received Object Detection: {msg}")
#     except json.JSONDecodeError:
#         logger.error(f"Error: Could not decode message: '{msg}'")
#     except Exception as e:
#         logger.error(f"Error: {e}")

def main():
    logger.info("Starting Log Publisher App")
    ecal_core.initialize(sys.argv, "Log Publisher App")
    log_publisher_app = LogPublisherApp()
    log_publisher_app.run()
    ecal_core.finalize()


if __name__ == "__main__":
    # main()
    main()
