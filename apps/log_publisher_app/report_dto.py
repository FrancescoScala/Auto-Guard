from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from signals import Signals

@dataclass
class ReportDTO:
    schema_version: str
    vehicle_id: str
    start_timestamp: str
    stop_timestamp: str
    criticality_level: str
    vehicle_dynamics: List[Signals] = field(default_factory=list)