import time
from typing import Dict

from backend.device.info.SerialDeviceInfo import SerialDeviceInfo
from backend.services.device.scanner.AbstractScanner import AbstractScanner

from serial.tools.list_ports import comports

class SerialScanner(AbstractScanner):
	def __init__(self):
		self.device_dict: Dict[str, SerialDeviceInfo] = {}

	def get_devices(self) -> Dict[str, SerialDeviceInfo]:
		return self.device_dict


	def start_scan(self):
		ports = comports()
		# Loop through all available ports, and add them to the device_dict (possibly by reading the name of the device)
		for port in sorted(ports):
			if port.hwid is None:
				continue

			self.device_dict[port.hwid] = SerialDeviceInfo.from_device(port)

		pass

	def stop_scan(self):
		pass