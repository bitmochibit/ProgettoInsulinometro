from typing import Dict, cast

from backend.device.info.DeviceInfo import DeviceInfo
from backend.device.info.SerialDeviceInfo import SerialDeviceInfo
from backend.services.device.scanner.AbstractScanner import AbstractScanner


class SerialScannerController:
	def __init__(self, scanner_service: AbstractScanner):
		self.scanner_service = scanner_service

	def get_devices(self) -> Dict[str, SerialDeviceInfo]:
		return cast(Dict[str, SerialDeviceInfo], self.scanner_service.get_devices())
		pass

	def start_scan(self, time):
		self.scanner_service.start_scan(time)
		pass

	def stop_scan(self):
		self.scanner_service.stop_scan()
		pass
