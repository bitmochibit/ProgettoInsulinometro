from dataclasses import dataclass
from typing import Any


@dataclass
class DeviceInfo:
    id: str
    name: str
    details: Any