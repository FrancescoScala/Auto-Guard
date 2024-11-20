import sys, time, json, logging

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

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
    def __init__(self):
        # Create a subscriber that listens on the "traffic_sign_detection"
        self.sub = StringSubscriber("vehicle_dynamics")
        self.prev_long_acc = 0
        self.prev_lat_acc = 0
        self.emergency_brake = False
        self.prev_timestamp = 0
        self.speed_threshold = 10 # threshold for the spee
        self.previous_speed = 100
        
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
            json_msg = json.loads(msg)
            # print(f"Received: {msg}")
            # Detect acceleration and set emergency brake flag
            long_acc = float(json_msg["signals"]["longAcc"])
            timestamp = int(json_msg["header"]["timestamp"])
            speed = float(json_msg["signals"]["speed"])
            if (long_acc - self.prev_long_acc) < 0: # means it is decelerating
                self.emergency_brake = True
                print("emegency brake because of long acc")


            if speed - self.previous_speed < self.speed_threshold:
                self.emergency_brake = True
                print("emegency brake because of speed")
                
            print(f"Emergency Brake: {self.emergency_brake}")

            self.prev_long_acc = long_acc
            print(f"timestamp difference: {timestamp-self.prev_timestamp}")
            self.prev_timestamp = timestamp

            self.previous_speed = speed

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
