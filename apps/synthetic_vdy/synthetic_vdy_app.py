"""
This a synthetic data measurement generator and published to eCAL broker as a message
It provides the test environment for the  
"""
import sys
import time
import random
import json
import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher

class SyntheticDataGenerator():
    def __init__(self):
        self.min_speed = 0.0
        self.max_speed = 65.0
        self.target_speed = None

        self.current_speed = 0.0
        self.current_acceleration = 0.0


    def update(self):
        if self.current_speed >= self.max_speed:
            self.current_acceleration = 0.0
        if self.current_speed <= self.min_speed and self.current_acceleration <= 0.0:
            self.current_speed = 0.0

        if self.target_speed is not None  and self.target_speed > 0 and abs (self.target_speed - self.current_speed) <= 0.3:
            self.current_acceleration = 0

        if self.current_speed + self.current_acceleration * 0.1 < 0.0:
            self.current_speed = 0.0
            self.current_acceleration = 0
        else:
            self.current_speed = abs(self.current_speed + self.current_acceleration * 0.1)

        #print(self.current_speed, self.current_acceleration)
        return [self.current_speed, self.current_acceleration]


    def emergency_breaking(self):
        min_break_dist = (self.current_speed * self.current_speed) / (10.0 * 3.0 )
        break_value = 0 - (self.current_speed * self.current_speed) / (2 * min_break_dist)
        self.current_acceleration = break_value
        self.target_speed = 0

    def apply_normal_break(self):
        normal_break_dist = (self.current_speed * self.current_speed) / (10.0)
        break_value = 0 - (self.current_speed * self.current_speed) / (2 * normal_break_dist)
        self.current_acceleration = break_value
        self.target_speed = 0

    def release_break(self):
        self.current_acceleration = 0

    def increase_acceleration(self, delta, target = None):
        self.current_acceleration += delta
        self.target_speed = target


def create_message(current_speed, current_acceleration):
    pass


    # v = vo + a*t
    # d = vo t + 0.5 * a*t*t  
    template_message = {
	"header": {
		"timestamp": f"{int(time.time_ns()/1000)}"
	},
	"errs": {
		"speed": "STATE_FAULT",
		"speedDisplayed": "STATE_FAULT",
		"longAcc": "STATE_FAULT",
		"latAcc": "STATE_FAULT",
		"yawrate": "STATE_FAULT",
		"steeringWheelAngle": "STATE_FAULT",
		"steeringWheelAngleSpeed": "STATE_FAULT",
		"drvSteerTorque": "STATE_FAULT",
		"timeSinceLastClick": "STATE_FAULT",
		"wheelSteeringAngleFront": "STATE_FAULT",
		"wheelSteeringAngleRear": "STATE_FAULT"
	},
	"signals": {
		"speed": current_speed,
		"speedDisplayed": current_speed + random.uniform(-0.005, 0.005),
		"speedPerWheel": [
			current_speed + random.uniform(-0.005, -0.01),
			current_speed + random.uniform(-0.005, -0.01),
			current_speed + random.uniform(-0.005, -0.01),
			current_speed + random.uniform(-0.005, -0.01)
		],
		"longAcc":current_acceleration,
		"latAcc": random.uniform(-0.02, -0.02),
		"yawrate": random.uniform(-0.012, 0.012) ,
		"steeringWheelAngle": random.uniform(-0.05, 0.05),
		"steeringWheelAngleSpeed": random.uniform(0.01, 0.1),
		"drvSteerTorque": 0.0,
		"timeSinceLastClick": 0.0,
		"wheelSteeringAngleFront": 0.0,
		"wheelSteeringAngleRear": 0.0
	},
	"variances": {
		"speed": 0.0,
		"speedDisplayed": 0.0,
		"longAcc": 0.0,
		"latAcc": 0.0,
		"yawrate": 0.0,
		"steeringWheelAngle": 0.0,
		"steeringWheelAngleSpeed": 0.0,
		"drvSteerTorque": 0.0,
		"timeSinceLastClick": 0.0,
		"wheelSteeringAngleFront": 0.0,
		"wheelSteeringAngleRear": 0.0
	},
	"timestamps": {
		"speed": "0",
		"speedDisplayed": "0",
		"longAcc": "0",
		"latAcc": "0",
		"yawrate": "0",
		"steeringWheelAngle": "0",
		"steeringWheelAngleSpeed": "0",
		"drvSteerTorque": "0",
		"timeSinceLastClick": "0",
		"wheelSteeringAngleFront": "0",
		"wheelSteeringAngleRear": "0"
	}
}
    return template_message



if __name__ == "__main__":
    # initialize eCAL API. The name of our Process will be "Python Hello World Publisher"
    ecal_core.initialize(sys.argv, "SyntheticEcalMesurement")

    pub = StringPublisher("vehicle_dynamics_synthetic")

    s = SyntheticDataGenerator()
    # s.increase_acceleration(0.78, target = 40)
    #
    # for i in range(1000):
    #     s.update()
    sections = []
    s.increase_acceleration(0.78, target=55)
    section1= [s.update() for i in range(1000)]  
    sections.append(section1)
    s.apply_normal_break()
    section2= [s.update() for i in range(1000)]  
    sections.append(section2)
    
    s.increase_acceleration(0.78, target=55)
    section3= [s.update() for i in range(1000)]  
    sections.append(section3)

    s.emergency_breaking()
    section4 = [s.update() for i in range(1000)]  
    sections.append(section4)    

    while ecal_core.ok():
        print("Publishing message")
    # Create a message with a counter an publish it to the topic
        for sec in sections:
            for i in sec:
                current_message = create_message(i[0], i[1])
                print(current_message)
                pub.send(json.dumps(current_message))
                print("sent")
                time.sleep(0.1)

    # finalize eCAL API
    ecal_core.finalize()
    sys.exit(0)

