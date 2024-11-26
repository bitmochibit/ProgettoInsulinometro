from dataclasses import dataclass

from backend.device.info.DeviceInfo import DeviceInfo


@dataclass
class BLEDeviceInfo(DeviceInfo):
    local_name: str
    rssi: int
    tx_power: int
    service_uuids: list[str]
