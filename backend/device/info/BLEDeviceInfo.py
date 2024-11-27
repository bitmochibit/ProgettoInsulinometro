from dataclasses import dataclass
from datetime import datetime

from bleak import BLEDevice, AdvertisementData

from backend.device.info.DeviceInfo import DeviceInfo


@dataclass
class BLEDeviceInfo(DeviceInfo):
    local_name: str
    rssi: int
    tx_power: int
    service_uuids: list[str]

    @staticmethod
    def from_device(device: BLEDevice, adv: AdvertisementData):
        return BLEDeviceInfo(
            name=device.name,
            id=device.address,
            local_name=adv.local_name,
            rssi=adv.rssi,
            tx_power=adv.tx_power,
            service_uuids=adv.service_uuids,
            update_time=datetime.now()
        )

    def update(self, device: BLEDevice, adv: AdvertisementData):
        self.id = device.address
        self.name = device.name
        self.local_name = adv.local_name
        self.rssi = adv.rssi
        self.tx_power = adv.tx_power
        self.service_uuids = adv.service_uuids
        self.update_time = datetime.now()
