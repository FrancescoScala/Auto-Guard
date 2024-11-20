from dataclasses import dataclass
from typing import List
import json

@dataclass
class Signals:
    vehicle_id: int
    timestamp: int
    speed: float
    speedDisplayed: float
    speedPerWheel: List[float]
    longAcc: float
    latAcc: float
    yawrate: float
    steeringWheelAngle: float
    steeringWheelAngleSpeed: float
    drvSteerTorque: float
    timeSinceLastClick: float
    wheelSteeringAngleFront: float
    wheelSteeringAngleRear: float


def parse_signals(json_data, vehicle_id=1):
    data = json.loads(json_data)
    signals_data = data["signals"]
    return Signals(
        vehicle_id=vehicle_id,
        timestamp=int(data["header"]["timestamp"]),
        speed=signals_data["speed"],
        speedDisplayed=signals_data["speedDisplayed"],
        speedPerWheel=signals_data["speedPerWheel"],
        longAcc=signals_data["longAcc"],
        latAcc=signals_data["latAcc"],
        yawrate=signals_data["yawrate"],
        steeringWheelAngle=signals_data["steeringWheelAngle"],
        steeringWheelAngleSpeed=signals_data["steeringWheelAngleSpeed"],
        drvSteerTorque=signals_data["drvSteerTorque"],
        timeSinceLastClick=signals_data["timeSinceLastClick"],
        wheelSteeringAngleFront=signals_data["wheelSteeringAngleFront"],
        wheelSteeringAngleRear=signals_data["wheelSteeringAngleRear"]
    )