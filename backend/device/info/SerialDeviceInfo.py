from dataclasses import dataclass
from datetime import datetime

from serial.tools.list_ports_common import ListPortInfo

from backend.device.info.DeviceInfo import DeviceInfo


@dataclass
class SerialDeviceInfo(DeviceInfo):
    description: str = None

    @staticmethod
    def from_device(list_port_info: ListPortInfo):
        return SerialDeviceInfo(
            id=list_port_info.hwid,
            name=list_port_info.name,
            description=list_port_info.description,
            update_time=datetime.now()
        )

    def update(self, list_port_info: ListPortInfo):
        self.id = list_port_info.hwid
        self.name = list_port_info.name
        self.description = list_port_info.description

        self.update_time = datetime.now()
