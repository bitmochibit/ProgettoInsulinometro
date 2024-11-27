from abc import ABC, abstractmethod
from typing import Callable, Any

from backend.device.info import DeviceInfo
from backend.device.DeviceProperty import DeviceProperty


class DeviceService(ABC):
	@abstractmethod
	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		pass

	@abstractmethod
	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		pass

	@abstractmethod
	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		pass

	@abstractmethod
	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None) -> Any:
		pass

	@abstractmethod
	def is_connected(self) -> bool:
		pass

	@abstractmethod
	def last_connected_device(self) -> DeviceInfo:
		pass