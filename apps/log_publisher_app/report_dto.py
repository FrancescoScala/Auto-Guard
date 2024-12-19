from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from signals import Signals
import json
from enum import Enum


@dataclass
class ReportDTO:
    schema_version: str
    vehicle_id: str
    stop_timestamp: str
    vehicle_dynamics: List
        
    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "vehicle_id": self.vehicle_id,
            "stop_timestamp": self.stop_timestamp,
            "vehicle_dynamics": [signal.to_dict() for signal in self.vehicle_dynamics]
        }