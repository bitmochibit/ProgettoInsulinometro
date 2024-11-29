from typing import Dict, cast

from dependency_injector.providers import Selector

from backend.device.info.DeviceInfo import DeviceInfo
from backend.services.device.scanner.AbstractScanner import AbstractScanner


class ScannerController:
	def __init__(self, scanner_service: Selector[AbstractScanner]):
		self.scanner_service = scanner_service

	def get_devices(self) -> Dict[str, DeviceInfo]:
		return self.scanner_service.get_devices()
		pass

	def start_scan(self, time):
		self.scanner_service.start_scan(time)
		pass

	def stop_scan(self):
		self.scanner_service.stop_scan()
		pass

	pass