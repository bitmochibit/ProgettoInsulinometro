from dataclasses import dataclass
from datetime import datetime


@dataclass
class DeviceInfo:
    id: str
    name: str
    update_time: datetime
