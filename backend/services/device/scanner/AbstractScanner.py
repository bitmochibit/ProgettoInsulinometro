from abc import abstractmethod, ABC
from typing import Dict

from backend.device.info.DeviceInfo import DeviceInfo


class AbstractScanner(ABC):

	@abstractmethod
	def get_devices(self) -> Dict[str, DeviceInfo]:
		pass

	@abstractmethod
	def start_scan(self, max_time):
		pass

	@abstractmethod
	def stop_scan(self):
		pass